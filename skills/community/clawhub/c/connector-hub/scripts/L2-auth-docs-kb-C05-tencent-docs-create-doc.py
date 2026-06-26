#!/usr/bin/env python3
"""创建腾讯文档"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://docs.qq.com/openapi/drive/v2"

def create_document(title: str, doc_type: str = "doc", access_token: str = None, 
                   client_id: str = None, open_id: str = None) -> dict:
    """创建文档
    
    Args:
        title: 文档标题
        doc_type: 文档类型（doc, sheet, slide）
        access_token: 访问令牌
        client_id: 应用 ID
        open_id: 用户 Open-Id
    
    Returns:
        API 响应
    """
    if not access_token:
        access_token = os.environ.get("TENCENT_DOCS_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 TENCENT_DOCS_ACCESS_TOKEN 环境变量")
    
    headers = {
        "Access-Token": access_token,
        "Client-Id": client_id or os.environ.get("TENCENT_DOCS_CLIENT_ID", ""),
        "Open-Id": open_id or os.environ.get("TENCENT_DOCS_OPEN_ID", ""),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "title": title,
        "type": doc_type  # doc, sheet, slide
    }
    
    resp = requests.post(f"{API_BASE}/files", headers=headers, data=data)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="创建腾讯文档")
    parser.add_argument("title", help="文档标题")
    parser.add_argument("--type", choices=["doc", "sheet", "slide"], default="doc", 
                       help="文档类型")
    parser.add_argument("--token", help="访问令牌")
    parser.add_argument("--client-id", help="应用 ID")
    parser.add_argument("--open-id", help="用户 Open-Id")
    
    args = parser.parse_args()
    
    try:
        result = create_document(args.title, args.type, args.token, args.client_id, args.open_id)
        
        if result.get("ret") == 0:
            data = result.get("data", {})
            print(f"文档创建成功：")
            print(f"  标题：{data.get('title')}")
            print(f"  链接：{data.get('url')}")
            print(f"  ID：{data.get('ID')}")
            print(f"  类型：{data.get('type')}")
        else:
            print(f"创建失败：{result.get('msg')}")
            sys.exit(1)
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
