#!/usr/bin/env python3
"""发送飞书卡片消息"""

import os
import sys
import json
import hmac
import hashlib
import base64
import argparse
import requests

WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL")
WEBHOOK_SECRET = os.environ.get("FEISHU_WEBHOOK_SECRET")

def gen_sign(secret: str) -> tuple:
    """生成签名"""
    import time
    timestamp = str(int(time.time()))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return timestamp, sign

def send_card(title: str, content: str, color: str = "blue") -> dict:
    """发送卡片消息
    
    Args:
        title: 卡片标题
        content: 卡片内容（Markdown）
        color: 卡片颜色（blue, green, red, orange, purple, indigo, grey）
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 FEISHU_WEBHOOK_URL 环境变量")
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": color
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    if WEBHOOK_SECRET:
        timestamp, sign = gen_sign(WEBHOOK_SECRET)
        payload["timestamp"] = timestamp
        payload["sign"] = sign
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送飞书卡片消息")
    parser.add_argument("title", help="卡片标题")
    parser.add_argument("content", help="卡片内容（Markdown）")
    parser.add_argument("--color", default="blue", 
                       choices=["blue", "green", "red", "orange", "purple", "indigo", "grey"],
                       help="卡片颜色")
    
    args = parser.parse_args()
    
    try:
        result = send_card(args.title, args.content, args.color)
        
        if result.get("code") == 0:
            print("消息发送成功")
        else:
            print(f"发送失败：{result.get('msg')}")
            sys.exit(1)
    except Exception as e:
        print(f"发送失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
