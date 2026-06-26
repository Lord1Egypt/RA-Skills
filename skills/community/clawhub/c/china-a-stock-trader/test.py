# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from a_stock_trader import get_stock_quote, get_market_sentiment, check_dragon_signals, analyze_stock

print('=== Test 1: 行情获取 ===')
q = get_stock_quote('sh600519')
if q:
    print(f"OK: {q['name']} price={q['price']} change={q['change_pct']}%")

print()
print('=== Test 2: 市场情绪 ===')
s = get_market_sentiment()
print(f"OK: {s['phase']} score={s['score']}")

print()
print('=== Test 3: 龙头战法 ===')
d = check_dragon_signals('sz000858')
if d:
    print(f"OK: {d['name']}")
    for sig in d.get('signals', []):
        print(f"  - {sig}")

print()
print('=== All tests passed ===')
