#!/usr/bin/env python3
"""港股行情 - 直接获取"""
from longport.openapi import QuoteContext, Config
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

config = Config.from_env()
qctx = QuoteContext(config)

HK_STOCKS = {
    "700.HK": "腾讯控股",
    "9988.HK": "阿里巴巴",
    "3690.HK": "美团",
    "1211.HK": "比亚迪股份",
    "9618.HK": "京东",
}

print("\n📊 港股实时行情")
print("=" * 70)
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

try:
    # 批量获取 - 传列表
    symbols = list(HK_STOCKS.keys())
    quotes = qctx.quote(symbols)
    
    for q in quotes:
        name = HK_STOCKS.get(q.symbol, "未知")
        change = (q.last_done - q.prev_close) / q.prev_close * 100 if q.prev_close > 0 else 0
        print(f"{q.symbol:10} | {name:8} | ${q.last_done:>8.2f} | {change:>+7.2f}%")
    
    print("=" * 70)
    print("✅ 行情获取成功！")
    
except Exception as e:
    print(f"❌ 获取失败：{e}")
    print("=" * 70)
