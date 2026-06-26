#!/usr/bin/env python3
"""创建会话（腾讯企点客服）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.qidian.qq.com/v1"

def create_session(customer_name: str, channel: str = "web") -> dict:
    """创建会话
    
    Args:
        customer_name: 客户名称
        channel: 渠道（wechat, qq, web, app）
    
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
        "customer_name": customer_name,
        "channel": channel
    }
    
    resp = requests.post(f"{API_BASE}/sessions", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
会话创建成功：

| 字段 | 值 |
|------|-----|
| 会话 ID | {data.get('session_id', '-')} |
| 客户名称 | {data.get('customer_name', '-')} |
| 渠道 | {data.get('channel', '-')} |
| 状态 | {data.get('status', '-')} |
| 创建时间 | {data.get('created_at', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建会话")
    parser.add_argument("customer_name", help="客户名称")
    parser.add_argument("--channel", choices=["wechat", "qq", "web", "app"], default="web")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_session(args.customer_name, args.channel)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
