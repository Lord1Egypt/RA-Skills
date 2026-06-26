#!/usr/bin/env python3
"""发送钉钉 Markdown 消息"""

import os
import sys
import json
import time
import hmac
import hashlib
import base64
import argparse
import requests
from urllib.parse import quote_plus

WEBHOOK_URL = os.environ.get("DINGTALK_WEBHOOK_URL")
SECRET = os.environ.get("DINGTALK_SECRET")

def generate_sign() -> tuple:
    """生成签名"""
    if not SECRET:
        return None, None
    
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{SECRET}"
    hmac_code = hmac.new(
        SECRET.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    sign = quote_plus(base64.b64encode(hmac_code))
    
    return timestamp, sign

def send_markdown(title: str, text: str, at_mobiles: list = None, at_all: bool = False) -> dict:
    """发送 Markdown 消息
    
    Args:
        title: 消息标题
        text: Markdown 内容
        at_mobiles: @手机号列表
        at_all: @所有人
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 DINGTALK_WEBHOOK_URL 环境变量")
    
    # 构建请求 URL
    url = WEBHOOK_URL
    if SECRET:
        timestamp, sign = generate_sign()
        url = f"{url}&timestamp={timestamp}&sign={sign}"
    
    # 构建请求体
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        },
        "at": {
            "isAtAll": at_all
        }
    }
    
    if at_mobiles:
        payload["at"]["atMobiles"] = at_mobiles
    
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送钉钉 Markdown 消息")
    parser.add_argument("title", help="消息标题")
    parser.add_argument("text", help="Markdown 内容")
    parser.add_argument("--at-mobile", nargs="+", help="@手机号列表")
    parser.add_argument("--at-all", action="store_true", help="@所有人")
    
    args = parser.parse_args()
    
    try:
        result = send_markdown(args.title, args.text, args.at_mobile, args.at_all)
        
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
