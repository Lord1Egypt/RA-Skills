#!/usr/bin/env python3
"""创建服务请求（福帮手）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.fbs.com/v1"

def create_request(category: str, description: str, priority: str = "medium") -> dict:
    """创建服务请求
    
    Args:
        category: 服务类别
        description: 请求描述
        priority: 优先级（low/medium/high/urgent）
    
    Returns:
        API 响应
    """
    api_key = os.environ.get("FBS_API_KEY")
    if not api_key:
        raise ValueError("未设置 FBS_API_KEY 环境变量")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "category": category,
        "description": description,
        "priority": priority
    }
    
    resp = requests.post(f"{API_BASE}/requests", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
服务请求创建成功：

| 字段 | 值 |
|------|-----|
| 请求 ID | {data.get('id', '-')} |
| 类别 | {data.get('category', '-')} |
| 描述 | {data.get('description', '-')} |
| 优先级 | {data.get('priority', '-')} |
| 状态 | {data.get('status', '-')} |
| 创建时间 | {data.get('created_at', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建服务请求")
    parser.add_argument("category", help="服务类别")
    parser.add_argument("description", help="请求描述")
    parser.add_argument("--priority", choices=["low", "medium", "high", "urgent"], default="medium")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_request(args.category, args.description, args.priority)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
