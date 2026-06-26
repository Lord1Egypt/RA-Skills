#!/usr/bin/env python3
"""发送回复（腾讯企点客服）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.qidian.qq.com/v1"

def send_reply(session_id: str, content: str) -> dict:
    """发送回复
    
    Args:
        session_id: 会话 ID
        content: 回复内容
    
    Returns:
        API 响应
    """
    # 简化实现，实际需要 OAuth2 授权
    access_token = os.environ.get("QIDIAN_CS_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 QIDIAN_CS_ACCESS_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "content": content,
        "msg_type": "text"
    }
    
    resp = requests.post(f"{API_BASE}/sessions/{session_id}/messages", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送回复")
    parser.add_argument("session_id", help="会话 ID")
    parser.add_argument("content", help="回复内容")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = send_reply(args.session_id, args.content)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"回复发送成功：")
            print(f"  会话 ID：{args.session_id}")
            print(f"  消息 ID：{data.get('message_id', '-')}")
    except Exception as e:
        print(f"发送失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
