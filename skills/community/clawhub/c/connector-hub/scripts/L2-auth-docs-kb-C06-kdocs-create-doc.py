#!/usr/bin/env python3
"""创建金山文档"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://open.kdocs.cn/api/v1"

def create_document(title: str, doc_type: str = "doc") -> dict:
    """创建文档
    
    Args:
        title: 文档标题
        doc_type: 文档类型（doc, sheet, slide）
    
    Returns:
        API 响应
    """
    # 简化实现，实际需要 OAuth2 授权
    access_token = os.environ.get("KDOCS_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 KDOCS_ACCESS_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "type": doc_type
    }
    
    resp = requests.post(f"{API_BASE}/documents", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="创建金山文档")
    parser.add_argument("title", help="文档标题")
    parser.add_argument("--type", choices=["doc", "sheet", "slide"], default="doc")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_document(args.title, args.type)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"文档创建成功：")
            print(f"  标题：{data.get('title')}")
            print(f"  链接：{data.get('url')}")
            print(f"  ID：{data.get('id')}")
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
