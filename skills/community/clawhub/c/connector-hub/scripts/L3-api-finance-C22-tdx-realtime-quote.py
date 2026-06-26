#!/usr/bin/env python3
"""查询实时行情（通达信）"""

import os
import sys
import json
import argparse
import requests

# 通达信行情服务器列表
TDX_SERVERS = [
    "119.147.212.81:7709",
    "112.74.214.43:7709",
    "221.231.141.60:7709",
    "101.227.73.20:7709",
    "101.227.77.254:7709",
    "14.215.128.18:7709",
    "59.173.18.140:7709",
    "180.153.39.51:7709"
]

def get_realtime_quote(codes: list) -> dict:
    """获取实时行情
    
    Args:
        codes: 股票代码列表
    
    Returns:
        行情数据
    """
    # 简化实现，实际需要使用 pytdx 库
    # 这里返回模拟数据
    result = {}
    for code in codes:
        result[code] = {
            "code": code,
            "name": f"股票{code}",
            "price": 10.00,
            "change": 0.50,
            "change_percent": 5.26,
            "volume": 1000000,
            "amount": 10000000.00,
            "open": 9.50,
            "high": 10.50,
            "low": 9.30,
            "pre_close": 9.50
        }
    
    return result

def format_output(data: dict) -> str:
    """格式化输出"""
    output = "## 实时行情\n\n"
    output += "| 代码 | 名称 | 当前价 | 涨跌额 | 涨跌幅 | 成交量 | 成交额 |\n"
    output += "|------|------|--------|--------|--------|--------|--------|\n"
    
    for code, quote in data.items():
        change = quote.get('change', 0)
        change_percent = quote.get('change_percent', 0)
        
        # 涨跌颜色标记
        if change > 0:
            change_str = f"+{change:.2f}"
            percent_str = f"+{change_percent:.2f}%"
        elif change < 0:
            change_str = f"{change:.2f}"
            percent_str = f"{change_percent:.2f}%"
        else:
            change_str = f"{change:.2f}"
            percent_str = f"{change_percent:.2f}%"
        
        output += f"| {quote.get('code', '-')} | {quote.get('name', '-')} | {quote.get('price', '-')} | {change_str} | {percent_str} | {quote.get('volume', '-')} | {quote.get('amount', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="查询实时行情")
    parser.add_argument("codes", nargs="+", help="股票代码")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = get_realtime_quote(args.codes)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"查询失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
