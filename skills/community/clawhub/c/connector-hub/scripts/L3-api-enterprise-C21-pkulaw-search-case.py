#!/usr/bin/env python3
"""检索司法案例（北大法宝）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.pkulaw.com/v1"

def search_case(keyword: str, court: str = None, limit: int = 10) -> dict:
    """检索司法案例
    
    Args:
        keyword: 检索关键词
        court: 法院名称（可选）
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
    
    if court:
        params["court"] = court
    
    resp = requests.get(f"{API_BASE}/cases", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    cases = data.get("cases", [])
    if not cases:
        return "未找到司法案例"
    
    output = f"## 司法案例列表（共 {len(cases)} 条）\n\n"
    output += "| 标题 | 案号 | 法院 | 裁判日期 |\n"
    output += "|------|------|------|----------|\n"
    
    for case in cases:
        output += f"| {case.get('title', '-')} | {case.get('case_no', '-')} | {case.get('court', '-')} | {case.get('judgment_date', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="检索司法案例")
    parser.add_argument("keyword", help="检索关键词")
    parser.add_argument("--court", help="法院名称")
    parser.add_argument("--limit", type=int, default=10, help="返回数量限制")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = search_case(args.keyword, args.court, args.limit)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"检索失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
