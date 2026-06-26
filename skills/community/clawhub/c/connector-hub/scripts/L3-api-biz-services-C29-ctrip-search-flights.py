#!/usr/bin/env python3
"""搜索航班（携程问道）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.ctrip.com/v1"

def search_flights(departure: str, arrival: str, date: str, return_date: str = None) -> dict:
    """搜索航班
    
    Args:
        departure: 出发城市
        arrival: 到达城市
        date: 出发日期（YYYY-MM-DD）
        return_date: 返回日期（可选）
    
    Returns:
        API 响应
    """
    api_key = os.environ.get("CTRIP_API_KEY")
    if not api_key:
        raise ValueError("未设置 CTRIP_API_KEY 环境变量")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    params = {
        "departure": departure,
        "arrival": arrival,
        "date": date
    }
    
    if return_date:
        params["return_date"] = return_date
    
    resp = requests.get(f"{API_BASE}/flights/search", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    flights = data.get("flights", [])
    if not flights:
        return "未找到航班"
    
    output = f"## 航班列表（共 {len(flights)} 个）\n\n"
    output += "| 航班号 | 出发时间 | 到达时间 | 价格（¥） |\n"
    output += "|--------|----------|----------|----------|\n"
    
    for flight in flights[:10]:  # 只显示前 10 个
        output += f"| {flight.get('flight_no', '-')} | {flight.get('departure_time', '-')} | {flight.get('arrival_time', '-')} | {flight.get('price', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="搜索航班")
    parser.add_argument("departure", help="出发城市")
    parser.add_argument("arrival", help="到达城市")
    parser.add_argument("date", help="出发日期（YYYY-MM-DD）")
    parser.add_argument("--return-date", help="返回日期（可选）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = search_flights(args.departure, args.arrival, args.date, args.return_date)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"搜索失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
