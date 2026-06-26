#!/usr/bin/env python3
"""搜索乐享知识库文档"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.lexiang.com/v1"

def search_docs(keyword: str, kb_id: str = None) -> dict:
    """搜索文档
    
    Args:
        keyword: 搜索关键词
        kb_id: 知识库 ID（可选）
    
    Returns:
        API 响应
    """
    token = os.environ.get("LEXIANG_TOKEN")
    if not token:
        raise ValueError("未设置 LEXIANG_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "keyword": keyword
    }
    
    if kb_id:
        params["kb_id"] = kb_id
    
    resp = requests.get(f"{API_BASE}/search", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    docs = data.get("docs", [])
    if not docs:
        return "未找到文档"
    
    output = f"## 搜索结果（共 {len(docs)} 条）\n\n"
    output += "| 标题 | 摘要 | 链接 |\n"
    output += "|------|------|------|\n"
    
    for doc in docs[:10]:
        title = doc.get("title", "-")
        summary = doc.get("summary", "-")[:50] + "..." if len(doc.get("summary", "")) > 50 else doc.get("summary", "-")
        url = doc.get("url", "-")
        output += f"| {title} | {summary} | {url} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="搜索乐享知识库文档")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--kb", help="知识库 ID")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = search_docs(args.keyword, args.kb)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"搜索失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
