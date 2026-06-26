# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from a_stock_trader import (
    get_stock_info, get_stock_quote, get_stock_quotes,
    get_sina_kline, get_technical_analysis,
    screen_fundamental, get_yahoo_stock_info,
    get_market_sentiment, check_dragon_signals,
    risk_check, analyze_stock
)

print('=== 完整功能测试 ===\n')

# 测试股票
sym = 'sh600519'

# 1. 实时行情
print('【1. get_stock_info】')
info = get_stock_info(sym)
print(f"  名称: {info['name']}")
print(f"  现价: {info['price']}元")
print(f"  涨跌: {(info['price']-info['prev_close']):.2f}元 ({(info['price']-info['prev_close'])/info['prev_close']*100:.2f}%)")
print(f"  换手率: {info['turnover']}%")
print(f"  PE: {info['pe']}")
print()

# 2. 批量获取
print('【2. get_stock_quotes 批量】')
quotes = get_stock_quotes(['sh600519', 'sz000858', 'sz300750'])
print(f"  获取到 {len(quotes)} 只股票")
for code, q in quotes.items():
    print(f"  - {q['name']}: {q['price']}元")
print()

# 3. K线数据
print('【3. get_sina_kline 日K线】')
klines = get_sina_kline(sym, scale=240, datalen=5)
print(f"  获取到 {len(klines)} 根K线")
if klines:
    print(f"  最新: {klines[-1]}")
print()

# 4. 技术分析
print('【4. get_technical_analysis】')
tech = get_technical_analysis(sym)
if tech:
    print(f"  均线: MA5={tech['ma5']}, MA10={tech['ma10']}, MA20={tech['ma20']}")
    print(f"  KDJ: K={tech['kdj']['k']}, D={tech['kdj']['d']}, J={tech['kdj']['j']}")
    print(f"  MACD: DIF={tech['macd']['dif']}, DEA={tech['macd']['dea']}, MACD={tech['macd']['macd']}")
    print(f"  布林带: {tech['boll']}")
    print(f"  趋势: {tech['ma_trend']}")
    print(f"  量比: {tech['volume_ratio']} ({tech['volume_signal']})")
print()

# 5. 基本面筛选
print('【5. screen_fundamental】')
candidates = screen_fundamental(pe_max=50, roe_min=15, growth_min=20)
print(f"  符合条件: {len(candidates)} 只")
for c in candidates[:3]:
    print(f"  - {c['name']}: PE={c['pe']}, ROE={c['roe']}%, 增速={c['growth']}%")
print()

# 6. 市场情绪
print('【6. get_market_sentiment】')
sentiment = get_market_sentiment()
print(f"  阶段: {sentiment['phase']}")
print(f"  评分: {sentiment['score']}/100")
print(f"  建议: {sentiment['suggestion']}")
print()

# 7. 龙头战法
print('【7. check_dragon_signals】')
dragon = check_dragon_signals(sym)
print(f"  股票: {dragon.get('name')}")
print(f"  信号数: {len(dragon.get('signals', []))}")
for s in dragon.get('signals', [])[:3]:
    print(f"    {s['emoji']}{s['type']}: {s['desc']}")
print(f"  推荐动作: {dragon.get('action')}")
print()

# 8. 风险检查
print('【8. risk_check】')
risk = risk_check(sym)
print(f"  风险等级: {risk['risk_level']} (评分: {risk['risk_score']})")
for r in risk['risks']:
    print(f"    {r}")
print()

# 9. 综合分析
print('【9. analyze_stock 综合分析】')
result = analyze_stock(sym)
adv = result.get('advice', {})
print(f"  操作建议: {adv.get('action')}")
print(f"  理由: {adv.get('reason')}")
if adv.get('entry'):
    print(f"  买入价: {adv.get('entry')}元")
if adv.get('stop_loss'):
    print(f"  止损价: {adv.get('stop_loss')}元")
print()

print('=== 全部测试完成 ===')
