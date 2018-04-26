# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime, timedelta, timezone
import requests
import json

def get_day():
    youbi = ["月","火","水","木","金","土","日"]
    JST = timezone(timedelta(hours=+9), 'JST')
    d = datetime.now(JST)
    month = d.month
    day = d.day
    weekday = youbi[d.weekday()]
    return "今日は%s月%s日%s曜日です。" % (month, day, weekday)
    
def get_garbage():
    JST = timezone(timedelta(hours=+9), 'JST')
    d = datetime.now(JST)
    gomi = [
        "今日はプラスチックごみの日です。",
        "今日は可燃ごみの日です。",
        "今日は不燃ごみの日です。",
        "",
        "今日は可燃ごみの日です。",
        "今日は資源ごみの日です。",
        ""
        ]
    return gomi[d.weekday()]

def get_weather():
    weather_api_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    response_text = ''
    try:
        response = requests.get(weather_api_url, params={'city': 130010})
        response_dict = json.loads(response.text)
        description = response_dict["description"]["text"].split('\n')[0]
        forecasts = response_dict["forecasts"][0]
        temperature = forecasts['temperature']
        weather = forecasts['telop']
        response_text += '今日の東京都の天気は' + weather + "。"
        min_temp = temperature['min']
        max_temp = temperature['max']
        if min_temp is not None:
            response_text += '最低気温は' + min_temp["celsius"] + "度です。"
        if max_temp is not None:
            response_text += '最高気温は' + max_temp["celsius"] + "度です。"
        response_text += description
    except Exception as e:
        response_text = 'すいません。天気検索でエラーを起こしてしまいました'
    return response_text

# --------------- Main handler ------------------

def lambda_handler(event, context):
    text = "おはようございます。"
    text += get_day()
    text += get_weather()
    text += get_garbage()
    
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': text
            }
        }
    }
    return response
