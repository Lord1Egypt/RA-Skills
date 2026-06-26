#!/usr/bin/env python3
"""获取实时行情 - 一次性测试"""
from longport.openapi import QuoteContext, Config
from dotenv import load_dotenv
load_dotenv()

config = Config.from_env()
ctx = QuoteContext(config)

symbols = ['QQQ.US', 'NVDA.US', 'AAPL.US', 'TSLA.US', 'MSFT.US']
print("\n📊 长桥实时行情")
print("=" * 60)
for s in symbols:
    try:
        q = ctx.get_quote(s)
        print(f"{s:10} ${q.last_done:>8.2f}  ({q.change_rate*100:>+6.2f}%)")
    except Exception as e:
        print(f"{s:10} 获取失败：{e}")
print("=" * 60)
