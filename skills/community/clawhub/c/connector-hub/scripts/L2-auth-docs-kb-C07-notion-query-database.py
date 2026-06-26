#!/usr/bin/env python3
"""查询 Notion 数据库"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.notion.com/v1"

def query_database(database_id: str, filter_obj: dict = None, sorts: list = None) -> dict:
    """查询数据库
    
    Args:
        database_id: 数据库 ID
        filter_obj: 过滤条件
        sorts: 排序条件
    
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
    
    payload = {}
    
    if filter_obj:
        payload["filter"] = filter_obj
    
    if sorts:
        payload["sorts"] = sorts
    
    resp = requests.post(f"{API_BASE}/databases/{database_id}/query", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    results = data.get("results", [])
    if not results:
        return "数据库为空"
    
    output = f"## 数据库记录（共 {len(results)} 条）\n\n"
    
    for i, page in enumerate(results[:10], 1):
        properties = page.get("properties", {})
        title = "-"
        
        # 获取标题
        for prop_name, prop_value in properties.items():
            if prop_value.get("type") == "title":
                title_items = prop_value.get("title", [])
                if title_items:
                    title = title_items[0].get("text", {}).get("content", "-")
                break
        
        output += f"{i}. {title}\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="查询 Notion 数据库")
    parser.add_argument("database_id", help="数据库 ID")
    parser.add_argument("--filter", help="过滤条件（JSON 格式）")
    parser.add_argument("--sorts", help="排序条件（JSON 格式）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        filter_obj = json.loads(args.filter) if args.filter else None
        sorts = json.loads(args.sorts) if args.sorts else None
        
        data = query_database(args.database_id, filter_obj, sorts)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"查询失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
