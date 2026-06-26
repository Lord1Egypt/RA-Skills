#!/usr/bin/env python3
"""发送企业微信图文消息"""

import os
import sys
import json
import argparse
import requests

WEBHOOK_URL = os.environ.get("WECOM_WEBHOOK_URL")

def send_news(articles: list) -> dict:
    """发送图文消息
    
    Args:
        articles: 文章列表，每篇文章包含 title, description, url, picurl
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 WECOM_WEBHOOK_URL 环境变量")
    
    payload = {
        "msgtype": "news",
        "news": {
            "articles": articles
        }
    }
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送企业微信图文消息")
    parser.add_argument("articles", help="文章列表（JSON 格式）")
    
    args = parser.parse_args()
    
    try:
        articles = json.loads(args.articles)
        result = send_news(articles)
        
        if result.get("errcode") == 0:
            print("消息发送成功")
        else:
            print(f"发送失败：{result.get('errmsg')}")
            sys.exit(1)
    except Exception as e:
        print(f"发送失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
