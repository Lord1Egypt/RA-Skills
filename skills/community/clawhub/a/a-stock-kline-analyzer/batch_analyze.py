#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量K线分析"""

import sys
sys.path.insert(0, '.')
from scripts.kline_analyzer import analyze_stock

stocks = [
    ('600487', '亨通光电'),
    ('000573', '粤宏远A'),
    ('002428', '云南锗业'),
    ('002155', '湖南黄金'),
    ('600392', '盛和资源'),
    ('603618', '杭电股份'),
    ('600561', '江西长运'),
    ('002969', '嘉美包装'),
    ('000021', '深科技'),
    ('300189', '神农种业'),
    ('600871', '石化油服'),
    ('600759', '洲际油气')
]

print("=" * 70)
print("批量K线分析 - 12只股票")
print("=" * 70)

results = []
for code, name in stocks:
    print(f"\n分析 {code} {name}...")
    try:
        result = analyze_stock(code, days=30, realtime=True)
        if result:
            results.append((code, name, result))
            print(f"✓ {name} 分析完成")
    except Exception as e:
        print(f"✗ {name} 分析失败: {e}")

print("\n" + "=" * 70)
print("汇总结果")
print("=" * 70)

for code, name, result in results:
    print(f"\n{name} ({code}):")
    print(f"  价格: {result.get('price', 'N/A')} ({result.get('change_pct', 'N/A')}%)")
    print(f"  MACD: {result.get('macd_signal', 'N/A')}")
    print(f"  RSI: {result.get('rsi', 'N/A')}")
    print(f"  趋势: {result.get('trend', 'N/A')}")
