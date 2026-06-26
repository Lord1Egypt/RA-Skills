#!/usr/bin/env python3
import os
import requests

api_key = 'sk-cp-xUTR3jpZvNlV77wV2Q80AckTfoATR3DmSe_WyEzbrLRkr7cE1nEybwDk4HKfZNKmThXRuLVxTh-NRgL-JBk5V57ohBD73NFUXHvRfyql_HCFuxsU_cAIaP8'

url = 'https://api.minimax.chat/v1/text/chatcompletion_v2'
headers = {
    'Authorization': 'Bearer ' + api_key,
    'Content-Type': 'application/json'
}

payload = {
    'model': 'MiniMax-M2.5',
    'messages': [
        {'role': 'system', 'content': '你是一个新闻搜索助手。请搜索并返回结构化结果。'},
        {'role': 'user', 'content': '搜索关于"人工智能"的最新新闻，返回 JSON 格式：标题、URL、摘要、来源'}
    ],
    'tools': [{'type': 'web_search'}],
    'temperature': 0.3
}

response = requests.post(url, headers=headers, json=payload, timeout=30)
print('Status:', response.status_code)
print('Response:', response.text[:2000])
