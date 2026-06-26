#!/usr/bin/env python3
"""发送飞书文本消息"""

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
    """生成签名（如果启用了签名校验）
    
    Args:
        secret: 签名密钥
    
    Returns:
        (timestamp, sign)
    """
    import time
    timestamp = str(int(time.time()))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return timestamp, sign

def send_text(content: str, at_user: str = None) -> dict:
    """发送文本消息
    
    Args:
        content: 消息内容
        at_user: @用户 ID（open_id）
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 FEISHU_WEBHOOK_URL 环境变量")
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    
    # 如果启用了签名校验
    if WEBHOOK_SECRET:
        timestamp, sign = gen_sign(WEBHOOK_SECRET)
        payload["timestamp"] = timestamp
        payload["sign"] = sign
    
    # @指定用户
    if at_user:
        payload["content"]["text"] = f"<at user_id=\"{at_user}\">用户</at> {content}"
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送飞书文本消息")
    parser.add_argument("content", help="消息内容")
    parser.add_argument("--at", help="@用户 ID（open_id）")
    
    args = parser.parse_args()
    
    try:
        result = send_text(args.content, args.at)
        
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
