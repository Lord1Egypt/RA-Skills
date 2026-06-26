#!/usr/bin/env python3
"""发送飞书富文本消息"""

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

def send_post(title: str, content_lines: list) -> dict:
    """发送富文本消息
    
    Args:
        title: 消息标题
        content_lines: 内容行列表
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 FEISHU_WEBHOOK_URL 环境变量")
    
    content = []
    for line in content_lines:
        content.append([{"tag": "text", "text": line}])
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": content
                }
            }
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
    parser = argparse.ArgumentParser(description="发送飞书富文本消息")
    parser.add_argument("title", help="消息标题")
    parser.add_argument("content", nargs="+", help="内容行")
    
    args = parser.parse_args()
    
    try:
        result = send_post(args.title, args.content)
        
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
