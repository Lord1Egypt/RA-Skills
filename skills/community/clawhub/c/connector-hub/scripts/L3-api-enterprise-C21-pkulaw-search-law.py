#!/usr/bin/env python3
"""检索法律法规（北大法宝）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.pkulaw.com/v1"

def search_law(keyword: str, limit: int = 10) -> dict:
    """检索法律法规
    
    Args:
        keyword: 检索关键词
        limit: 返回数量限制
    
    Returns:
        API 响应
    """
    api_key = os.environ.get("PKULAW_API_KEY")
    if not api_key:
        raise ValueError("未设置 PKULAW_API_KEY 环境变量")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    params = {
        "keyword": keyword,
        "limit": limit
    }
    
    resp = requests.get(f"{API_BASE}/laws", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    laws = data.get("laws", [])
    if not laws:
        return "未找到法律法规"
    
    output = f"## 法律法规列表（共 {len(laws)} 条）\n\n"
    output += "| 标题 | 发布日期 | 效力级别 |\n"
    output += "|------|----------|----------|\n"
    
    for law in laws:
        output += f"| {law.get('title', '-')} | {law.get('publish_date', '-')} | {law.get('level', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="检索法律法规")
    parser.add_argument("keyword", help="检索关键词")
    parser.add_argument("--limit", type=int, default=10, help="返回数量限制")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = search_law(args.keyword, args.limit)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"检索失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
