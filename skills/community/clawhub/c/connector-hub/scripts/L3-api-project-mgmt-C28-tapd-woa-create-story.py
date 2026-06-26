#!/usr/bin/env python3
"""创建 TAPD 司内版需求"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.tapd.woa.com/stories"

def create_story(title: str, description: str = "", priority: str = "2", owner: str = "") -> dict:
    """创建需求"""
    workspace_id = os.environ.get("TAPD_WOA_WORKSPACE_ID")
    api_token = os.environ.get("TAPD_WOA_API_TOKEN")
    
    if not workspace_id or not api_token:
        raise ValueError("未设置 TAPD_WOA_WORKSPACE_ID 或 TAPD_WOA_API_TOKEN 环境变量")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "workspace_id": workspace_id,
        "name": title,
        "description": description or f"需求：{title}",
        "priority": priority,
        "owner": owner,
        "status": "planning"
    }
    
    resp = requests.post(
        API_BASE,
        headers=headers,
        json=payload,
        auth=(workspace_id, api_token)
    )
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    story = data.get("Story", {})
    return f"""
需求创建成功：

| 字段 | 值 |
|------|-----|
| ID | {story.get('id', '-')} |
| 标题 | {story.get('name', '-')} |
| 状态 | {story.get('status', '-')} |
| 优先级 | {story.get('priority', '-')} |
| 负责人 | {story.get('owner', '-')} |
| 创建时间 | {story.get('created', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建 TAPD 司内版需求")
    parser.add_argument("title", help="需求标题")
    parser.add_argument("--desc", help="需求描述")
    parser.add_argument("--priority", choices=["1", "2", "3", "4"], default="2")
    parser.add_argument("--owner", help="负责人")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_story(args.title, args.desc, args.priority, args.owner)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
