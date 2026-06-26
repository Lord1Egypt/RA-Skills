#!/usr/bin/env python3
"""发送企业微信 Markdown 消息"""

import os
import sys
import json
import argparse
import requests

WEBHOOK_URL = os.environ.get("WECOM_WEBHOOK_URL")

def send_markdown(content: str) -> dict:
    """发送 Markdown 消息
    
    Args:
        content: Markdown 内容
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 WECOM_WEBHOOK_URL 环境变量")
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送企业微信 Markdown 消息")
    parser.add_argument("content", help="Markdown 内容")
    
    args = parser.parse_args()
    
    try:
        result = send_markdown(args.content)
        
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
