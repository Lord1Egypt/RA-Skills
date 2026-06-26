#!/usr/bin/env python3
"""发送企业微信文本消息"""

import os
import sys
import json
import argparse
import requests

WEBHOOK_URL = os.environ.get("WECOM_WEBHOOK_URL")

def send_text(content: str, mentioned_list: list = None, mentioned_mobile_list: list = None) -> dict:
    """发送文本消息
    
    Args:
        content: 消息内容
        mentioned_list: @用户列表（userid）
        mentioned_mobile_list: @手机号列表
    
    Returns:
        API 响应
    """
    if not WEBHOOK_URL:
        raise ValueError("未设置 WECOM_WEBHOOK_URL 环境变量")
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    # @指定用户
    if mentioned_list or mentioned_mobile_list:
        payload["text"]["mentioned_list"] = mentioned_list or []
        payload["text"]["mentioned_mobile_list"] = mentioned_mobile_list or []
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送企业微信文本消息")
    parser.add_argument("content", help="消息内容")
    parser.add_argument("--at", nargs="+", help="@用户列表（userid）")
    parser.add_argument("--at-mobile", nargs="+", help="@手机号列表")
    parser.add_argument("--at-all", action="store_true", help="@所有人")
    
    args = parser.parse_args()
    
    try:
        mentioned_list = args.at or []
        if args.at_all:
            mentioned_list.append("all")
        
        result = send_text(args.content, mentioned_list, args.at_mobile)
        
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
