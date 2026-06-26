#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试：查看活动详情的实际内容格式
"""

import json
import requests
import html
import re
import os

# 代理配置（从环境变量读取，可选）
PROXY_URL = os.environ.get("HTTP_PROXY", "")
PROXIES = {
    "http": PROXY_URL,
    "https": PROXY_URL,
} if PROXY_URL else {}

def strip_html_tags(html_text):
    """提取 HTML 或 JSON 结构中的纯文本"""
    try:
        parsed = json.loads(html_text)
        texts = []
        def extract(node):
            if isinstance(node, dict):
                if node.get('node') == 'text':
                    text = node.get('text', '')
                    text = html.unescape(text.replace('&nbsp;', ' '))
                    texts.append(text)
                elif 'child' in node:
                    for child in node['child']:
                        extract(child)
            elif isinstance(node, list):
                for item in node:
                    extract(item)
        extract(parsed)
        text = ' '.join(texts)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except (json.JSONDecodeError, TypeError):
        text = re.sub(r'<[^>]+>', ' ', html_text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

# 测试几个活动的 code
test_codes = [
    "7d3f8e9a2b1c4d5e6f7a8b9c0d1e2f3a",  # 示例
]

# 先获取活动列表
url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
params = {"type": "1", "pageNo": "1", "pageSize": "10", "catalogId": "93"}
headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

resp = requests.get(url, params=params, headers=headers, timeout=15, proxies=PROXIES)
data = resp.json()
articles = data.get("data", {}).get("catalogs", [{}])[0].get("articles", [])

print(f"获取到 {len(articles)} 个活动\n")

for i, article in enumerate(articles[:3], 1):
    code = article.get("code", "")
    title = article.get("title", "")
    print(f"{'='*80}")
    print(f"[{i}] {title}")
    print(f"Code: {code}")
    print()
    
    # 获取详情
    detail_url = "https://www.binance.com/bapi/composite/v1/public/cms/article/detail/query"
    detail_params = {"articleCode": code}
    detail_resp = requests.get(detail_url, params=detail_params, headers=headers, timeout=10, proxies=PROXIES)
    detail_data = detail_resp.json()
    
    body = detail_data.get("data", {}).get("body", "")
    pure_body = strip_html_tags(body)
    
    # 查找包含日期相关的段落
    print("📅 查找日期相关内容:")
    date_patterns = [
        r'Activity Period[^\n]{0,200}',
        r'End[^\n]{0,100}',
        r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
        r'[A-Za-z]+ \d{1,2},? \d{4}',
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, pure_body, re.IGNORECASE)
        if matches:
            for m in matches[:3]:
                print(f"  匹配：{m[:150]}")
    
    # 显示正文前 2000 字符
    print(f"\n📄 正文前 2000 字符:")
    print(pure_body[:2000])
    print()
