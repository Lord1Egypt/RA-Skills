#!/usr/bin/env python3
"""查询销售漏斗（销售易 CRM）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://open.neocrm.com/api/v1"

def query_pipeline(user_id: str = None, date_range: str = "month") -> dict:
    """查询销售漏斗
    
    Args:
        user_id: 用户 ID
        date_range: 日期范围（week, month, quarter, year）
    
    Returns:
        API 响应
    """
    # 简化实现，实际需要 OAuth2 授权
    access_token = os.environ.get("NEO_CRM_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 NEO_CRM_ACCESS_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "date_range": date_range  # week, month, quarter, year
    }
    
    if user_id:
        params["user_id"] = user_id
    
    resp = requests.get(f"{API_BASE}/pipeline", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    stages = data.get("stages", [])
    
    output = "## 销售漏斗\n\n"
    output += "| 阶段 | 商机数 | 金额（¥） | 转化率 |\n"
    output += "|------|--------|----------|--------|\n"
    
    total_amount = 0
    for stage in stages:
        amount = stage.get("amount", 0)
        total_amount += amount
        output += f"| {stage.get('name', '-')} | {stage.get('count', 0)} | ¥{amount:,.2f} | {stage.get('conversion_rate', '-')} |\n"
    
    output += f"\n**总金额：¥{total_amount:,.2f}**\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="查询销售漏斗")
    parser.add_argument("--user-id", help="用户 ID")
    parser.add_argument("--date-range", choices=["week", "month", "quarter", "year"], default="month")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = query_pipeline(args.user_id, args.date_range)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"查询失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
