#!/usr/bin/env python3
"""搜索酒店（携程问道）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.ctrip.com/v1"

def search_hotels(city: str, checkin: str, checkout: str, star: int = None) -> dict:
    """搜索酒店
    
    Args:
        city: 城市
        checkin: 入住日期（YYYY-MM-DD）
        checkout: 离店日期（YYYY-MM-DD）
        star: 酒店星级（可选）
    
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
        "city": city,
        "checkin": checkin,
        "checkout": checkout
    }
    
    if star:
        params["star"] = star
    
    resp = requests.get(f"{API_BASE}/hotels/search", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    hotels = data.get("hotels", [])
    if not hotels:
        return "未找到酒店"
    
    output = f"## 酒店列表（共 {len(hotels)} 个）\n\n"
    output += "| 酒店名称 | 星级 | 价格（¥） | 评分 |\n"
    output += "|----------|------|----------|------|\n"
    
    for hotel in hotels[:10]:  # 只显示前 10 个
        star = "⭐" * hotel.get("star", 0) if hotel.get("star") else "-"
        output += f"| {hotel.get('name', '-')} | {star} | {hotel.get('price', '-')} | {hotel.get('rating', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="搜索酒店")
    parser.add_argument("city", help="城市")
    parser.add_argument("checkin", help="入住日期（YYYY-MM-DD）")
    parser.add_argument("checkout", help="离店日期（YYYY-MM-DD）")
    parser.add_argument("--star", type=int, help="酒店星级")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = search_hotels(args.city, args.checkin, args.checkout, args.star)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"搜索失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
