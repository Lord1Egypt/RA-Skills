#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙选股系统 - 新旧策略对比演示
展示优化前后的选股差异
"""

import pandas as pd

# 模拟唐总反馈的问题场景
print("=" * 80)
print("📊 波龙选股系统 V2.1 - 新旧策略对比")
print("=" * 80)
print()

# 模拟历史数据（招商轮船、中远海能最近表现）
sample_stocks = pd.DataFrame([
    # 原策略可能选到的高位股
    {'name': '招商轮船', 'ts_code': '601872', 'return_3m': 120, 'rps_20d': 95, 'pe': 45, 'price': 15.8, 'is_high': True, 'reason': '已涨2-3倍'},
    {'name': '中远海能', 'ts_code': '600026', 'return_3m': 140, 'rps_20d': 97, 'pe': 52, 'price': 18.2, 'is_high': True, 'reason': '已涨2-3倍'},
    
    # 新策略应该选到的股票
    {'name': '平安银行', 'ts_code': '000001', 'return_3m': 15, 'rps_20d': 78, 'pe': 12, 'price': 12.5, 'is_high': False, 'reason': '刚启动'},
    {'name': '兴业银行', 'ts_code': '601166', 'return_3m': 12, 'rps_20d': 75, 'pe': 10, 'price': 21.8, 'is_high': False, 'reason': '底部蓄势'},
    {'name': '中国建筑', 'ts_code': '601668', 'return_3m': 8, 'rps_20d': 72, 'pe': 8, 'price': 5.6, 'is_high': False, 'reason': '低估值'},
    {'name': '工商银行', 'ts_code': '601398', 'return_3m': 5, 'rps_20d': 68, 'pe': 6, 'price': 5.2, 'is_high': False, 'reason': '稳健增长'},
    {'name': '中国铁建', 'ts_code': '601186', 'return_3m': 18, 'rps_20d': 82, 'pe': 9, 'price': 9.3, 'is_high': False, 'reason': 'RPS适中'},
])

print("【测试样本 - 唐总反馈的问题场景】")
print("-" * 80)
for _, row in sample_stocks.iterrows():
    status = "⚠️ 高位风险" if row['is_high'] else "✅ 健康"
    print(f"{row['name']:8s} | 3月涨幅: {row['return_3m']:4.0f}% | RPS: {row['rps_20d']:2.0f} | PE: {row['pe']:3.0f} | {status}")
print()

print("=" * 80)
print("【旧策略 V2.0】存在的问题")
print("=" * 80)
print("❌ 没有涨幅过滤")
print("❌ 没有RPS限制（选了RPS>90的高位股）")
print("❌ 估值过滤不严（PE>30也入选）")
print("❌ 没有位置判断")
print()
print("旧策略可能选到的股票：")
old_picks = sample_stocks[sample_stocks['return_3m'] > 50]  # 涨幅大的
for _, row in old_picks.iterrows():
    print(f"  ⚠️  {row['name']} - {row['reason']}，RPS={row['rps_20d']}，风险极高！")
print()

print("=" * 80)
print("【新策略 V2.1】价值投资优化")
print("=" * 80)
print("✅ 涨幅过滤：近3月涨幅≤50%")
print("✅ RPS优化：RPS 70-85最佳，排除>90的高位股")
print("✅ 估值严格：PE 5-30，PB<5")
print("✅ 位置判断：排除高位震荡")
print()

# 新策略筛选逻辑
def new_strategy_filter(row):
    filters = []
    
    # 涨幅过滤
    if row['return_3m'] > 50:
        filters.append("❌ 近3月涨幅>50%")
    
    # RPS过滤
    if row['rps_20d'] > 90:
        filters.append("❌ RPS>90，高位")
    elif row['rps_20d'] < 70:
        filters.append("❌ RPS<70，动量不足")
    
    # 估值过滤
    if row['pe'] > 30:
        filters.append("❌ PE>30，估值高")
    if row['pe'] < 5:
        filters.append("❌ PE<5，可能有问题")
    
    return filters

print("新策略筛选过程：")
for _, row in sample_stocks.iterrows():
    issues = new_strategy_filter(row)
    status = "❌ 被排除" if issues else "✅ 入选"
    print(f"\n  {row['name']}:")
    if issues:
        for issue in issues:
            print(f"    {issue}")
    else:
        print(f"    ✅ 符合条件 - {row['reason']}")

print()

# 新策略入选的股票
new_picks = sample_stocks[
    (sample_stocks['return_3m'] <= 50) &
    (sample_stocks['rps_20d'] >= 70) &
    (sample_stocks['rps_20d'] <= 90) &
    (sample_stocks['pe'] >= 5) &
    (sample_stocks['pe'] <= 30)
]

print("=" * 80)
print("【对比结果】")
print("=" * 80)
print(f"旧策略选股: {len(old_picks)}只 - 全是高位风险股！")
print(f"新策略选股: {len(new_picks)}只 - 价值投资导向，风险可控")
print()

print("新策略入选股票（价值投资推荐）：")
for _, row in new_picks.iterrows():
    print(f"  ✅ {row['name']:8s} | PE: {row['pe']:2.0f} | 3月涨幅: {row['return_3m']:2.0f}% | RPS: {row['rps_20d']:2.0f} | {row['reason']}")

print()
print("=" * 80)
print("【优化效果】")
print("=" * 80)
print("✅ 避免追涨杀跌，选择刚启动的股票")
print("✅ 排除高位震荡股（招商轮船、中远海能类股票）")
print("✅ 低估值优先（PE<30）")
print("✅ RPS 70-85最佳区间（刚启动）")
print()
print("🎯 投资理念：价值投资，不追高，不吃套")
print("=" * 80)
