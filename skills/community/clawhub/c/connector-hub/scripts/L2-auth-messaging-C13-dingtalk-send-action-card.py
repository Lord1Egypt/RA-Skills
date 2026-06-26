#!/usr/bin/env python3
"""发送钉钉 ActionCard 消息"""

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

def send_action_card(title: str, text: str, buttons: list, btn_orientation: str = "0") -> dict:
    """发送 ActionCard 消息
    
    Args:
        title: 消息标题
        text: 消息内容（Markdown）
        buttons: 按钮列表，每个按钮包含 title 和 actionURL
        btn_orientation: 按钮排列方式，0-垂直 1-水平
    
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
        "msgtype": "actionCard",
        "actionCard": {
            "title": title,
            "text": text,
            "btnOrientation": btn_orientation,
            "btns": buttons
        }
    }
    
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送钉钉 ActionCard 消息")
    parser.add_argument("title", help="消息标题")
    parser.add_argument("text", help="消息内容（Markdown）")
    parser.add_argument("buttons", help="按钮列表（JSON 格式）")
    parser.add_argument("--orientation", choices=["0", "1"], default="0", 
                       help="按钮排列方式：0-垂直 1-水平")
    
    args = parser.parse_args()
    
    try:
        buttons = json.loads(args.buttons)
        result = send_action_card(args.title, args.text, buttons, args.orientation)
        
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
