#!/usr/bin/env python3
"""查询 K 线数据（通达信）"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta

def get_kline_data(code: str, period: str = "daily", days: int = 30) -> dict:
    """获取 K 线数据
    
    Args:
        code: 股票代码
        period: 周期（daily, weekly, monthly, 5min, 15min, 30min, 60min）
        days: 获取天数
    
    Returns:
        K 线数据
    """
    # 简化实现，实际需要使用 pytdx 库
    # 这里返回模拟数据
    result = {
        "code": code,
        "period": period,
        "data": []
    }
    
    # 生成模拟数据
    base_date = datetime.now()
    for i in range(days):
        date = base_date - timedelta(days=i)
        result["data"].append({
            "date": date.strftime("%Y-%m-%d"),
            "open": 10.00 + i * 0.1,
            "high": 10.50 + i * 0.1,
            "low": 9.50 + i * 0.1,
            "close": 10.20 + i * 0.1,
            "volume": 1000000 + i * 10000,
            "amount": 10000000 + i * 100000
        })
    
    return result

def format_output(data: dict) -> str:
    """格式化输出"""
    code = data.get("code", "-")
    period = data.get("period", "-")
    klines = data.get("data", [])
    
    output = f"## K 线数据（{code} - {period}）\n\n"
    output += "| 日期 | 开盘 | 最高 | 最低 | 收盘 | 成交量 | 成交额 |\n"
    output += "|------|------|------|------|------|--------|--------|\n"
    
    for kline in klines[:20]:  # 只显示前 20 条
        output += f"| {kline.get('date', '-')} | {kline.get('open', '-')} | {kline.get('high', '-')} | {kline.get('low', '-')} | {kline.get('close', '-')} | {kline.get('volume', '-')} | {kline.get('amount', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="查询 K 线数据")
    parser.add_argument("code", help="股票代码")
    parser.add_argument("--period", choices=["daily", "weekly", "monthly", "5min", "15min", "30min", "60min"], 
                       default="daily", help="K 线周期")
    parser.add_argument("--days", type=int, default=30, help="获取天数")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = get_kline_data(args.code, args.period, args.days)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"查询失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
