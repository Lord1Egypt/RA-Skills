#!/usr/bin/env python3
"""创建 Notion 页面"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.notion.com/v1"

def create_page(title: str, parent_id: str, is_database: bool = False) -> dict:
    """创建页面
    
    Args:
        title: 页面标题
        parent_id: 父页面或数据库 ID
        is_database: 是否为数据库
    
    Returns:
        API 响应
    """
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("未设置 NOTION_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    if is_database:
        parent = {"database_id": parent_id}
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
    else:
        parent = {"page_id": parent_id}
        properties = {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    
    payload = {
        "parent": parent,
        "properties": properties
    }
    
    resp = requests.post(f"{API_BASE}/pages", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="创建 Notion 页面")
    parser.add_argument("title", help="页面标题")
    parser.add_argument("parent", help="父页面或数据库 ID")
    parser.add_argument("--database", action="store_true", help="是否为数据库")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_page(args.title, args.parent, args.database)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"页面创建成功：")
            print(f"  标题：{args.title}")
            print(f"  链接：{data.get('url')}")
            print(f"  ID：{data.get('id')}")
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
