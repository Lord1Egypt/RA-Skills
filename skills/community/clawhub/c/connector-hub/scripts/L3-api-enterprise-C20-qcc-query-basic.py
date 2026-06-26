#!/usr/bin/env python3
"""查询企业基础信息（企查查）"""

import os
import sys
import json
import time
import hashlib
import argparse
import requests

API_BASE = "https://api.qichacha.com"

def generate_token(app_key: str, secret_key: str) -> tuple:
    """生成动态 Token
    
    Args:
        app_key: 应用 Key
        secret_key: 密钥
    
    Returns:
        (token, timestamp)
    """
    timestamp = str(int(time.time()))
    raw_str = f"{app_key}{timestamp}{secret_key}"
    token = hashlib.md5(raw_str.encode()).hexdigest().upper()
    return token, timestamp

def query_basic(keyword: str) -> dict:
    """查询企业基础信息
    
    Args:
        keyword: 企业名称或统一社会信用代码
    
    Returns:
        API 响应
    """
    app_key = os.environ.get("QCC_APP_KEY")
    secret_key = os.environ.get("QCC_SECRET_KEY")
    
    if not app_key or not secret_key:
        raise ValueError("未设置 QCC_APP_KEY 或 QCC_SECRET_KEY 环境变量")
    
    token, timestamp = generate_token(app_key, secret_key)
    
    headers = {
        "Token": token,
        "Timespan": timestamp
    }
    
    params = {
        "key": app_key,
        "searchKey": keyword
    }
    
    resp = requests.get(f"{API_BASE}/FuzzySearch/GetList", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    results = data.get("Result", [])
    if not results:
        return "未找到企业信息"
    
    result = results[0]
    return f"""
| 字段 | 值 |
|------|-----|
| 企业名称 | {result.get('Name', '-')} |
| 统一社会信用代码 | {result.get('CreditCode', '-')} |
| 法定代表人 | {result.get('OperName', '-')} |
| 注册资本 | {result.get('RegistCapi', '-')} |
| 成立日期 | {result.get('StartDate', '-')} |
| 经营状态 | {result.get('Status', '-')} |
| 所属行业 | {result.get('Industry', '-')} |
| 注册地址 | {result.get('Address', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="查询企业基础信息（企查查）")
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
