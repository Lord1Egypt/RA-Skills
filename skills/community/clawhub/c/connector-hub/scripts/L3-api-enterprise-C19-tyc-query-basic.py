#!/usr/bin/env python3
"""查询企业基础信息（天眼查）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://open.tianyancha.com/services/open/ic"

def query_basic(keyword: str) -> dict:
    """查询企业基础信息
    
    Args:
        keyword: 企业名称或统一社会信用代码
    
    Returns:
        API 响应
    """
    token = os.environ.get("TIANYANCHA_TOKEN")
    if not token:
        raise ValueError("未设置 TIANYANCHA_TOKEN 环境变量")
    
    params = {
        "appKey": token,
        "keyword": keyword
    }
    
    resp = requests.get(f"{API_BASE}/baseinfo", params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    result = data.get("result", {})
    if not result:
        return "未找到企业信息"
    
    return f"""
| 字段 | 值 |
|------|-----|
| 企业名称 | {result.get('name', '-')} |
| 统一社会信用代码 | {result.get('creditCode', '-')} |
| 法定代表人 | {result.get('legalPersonName', '-')} |
| 注册资本 | {result.get('regCapital', '-')} |
| 成立日期 | {result.get('estiblishTime', '-')} |
| 经营状态 | {result.get('regStatus', '-')} |
| 所属行业 | {result.get('industry', '-')} |
| 注册地址 | {result.get('regLocation', '-')} |
| 经营范围 | {result.get('businessScope', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="查询企业基础信息（天眼查）")
    parser.add_argument("keyword", help="企业名称或统一社会信用代码")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = query_basic(args.keyword)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"查询失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
