#!/usr/bin/env python3
"""
港股策略回测 - 动量 + 均值回归
回测过去 3 个月的策略表现
"""
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# 配置
HK_STOCKS = ["700.HK", "9988.HK", "3690.HK", "1211.HK", "9618.HK"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=90)  # 回测 3 个月

# 策略参数
STRATEGY = {
    "momentum_threshold": 0.02,  # 涨幅>2%
    "reversion_threshold": -0.03,  # 跌幅>3%
    "position_size": 0.1,  # 10% 仓位
    "stop_loss": -0.05,  # -5% 止损
    "take_profit": 0.10,  # +10% 止盈
}

print("\n" + "=" * 80)
print("📊 港股策略回测")
print("=" * 80)
print(f"回测区间：{START_DATE.strftime('%Y-%m-%d')} 至 {END_DATE.strftime('%Y-%m-%d')}")
print(f"股票池：{', '.join(HK_STOCKS)}")
print(f"策略：动量 + 均值回归")
print("=" * 80)

# 下载数据
print("\n📥 下载历史数据...")
data = {}
for symbol in HK_STOCKS:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=START_DATE, end=END_DATE)
        if len(df) > 0:
            data[symbol] = df
            print(f"  ✅ {symbol}: {len(df)} 天数据")
        else:
            print(f"  ⚠️ {symbol}: 无数据")
    except Exception as e:
        print(f"  ❌ {symbol}: {e}")

if not data:
    print("\n❌ 无可用数据，回测终止")
    exit()

# 回测每个股票
print("\n" + "=" * 80)
print("📈 回测结果")
print("=" * 80)

results = []
for symbol, df in data.items():
    # 计算每日涨跌幅
    df['Return'] = df['Close'].pct_change()
    
    # 生成信号
    signals = []
    for i, row in df.iterrows():
        ret = row['Return']
        if pd.isna(ret):
            continue
        
        signal = None
        if ret >= STRATEGY["momentum_threshold"]:
            signal = "BUY_MOMENTUM"
        elif ret <= STRATEGY["reversion_threshold"]:
            signal = "BUY_REVERSION"
        
        if signal:
            signals.append({
                "date": i,
                "price": float(row['Close']),
                "return": ret,
                "signal": signal
            })
    
    # 计算绩效
    total_signals = len(signals)
    if total_signals > 0:
        avg_return = sum(s['return'] for s in signals) / total_signals
        win_rate = sum(1 for s in signals if s['return'] > 0) / total_signals * 100
    else:
        avg_return = 0
        win_rate = 0
    
    # 买入持有收益
    if len(df) > 1:
        buy_hold_return = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100
    else:
        buy_hold_return = 0
    
    results.append({
        "symbol": symbol,
        "signals": total_signals,
        "avg_return": avg_return * 100,
        "win_rate": win_rate,
        "buy_hold_return": buy_hold_return
    })
    
    print(f"\n{symbol}:")
    print(f"  交易信号：{total_signals} 次")
    print(f"  平均收益：{avg_return*100:.2f}%")
    print(f"  胜率：{win_rate:.1f}%")
    print(f"  买入持有收益：{buy_hold_return:.2f}%")

# 汇总
print("\n" + "=" * 80)
print("📊 策略汇总")
print("=" * 80)

if results:
    total_signals = sum(r['signals'] for r in results)
    avg_win_rate = sum(r['win_rate'] for r in results) / len(results)
    total_return = sum(r['avg_return'] for r in results)
    
    print(f"总交易信号：{total_signals} 次")
    print(f"平均胜率：{avg_win_rate:.1f}%")
    print(f"总平均收益：{total_return:.2f}%")
    
    # 策略评估
    print("\n🎯 策略评估")
    if avg_win_rate >= 60:
        print("  ✅ 胜率优秀 (>60%)")
    elif avg_win_rate >= 50:
        print("  ⭐ 胜率良好 (>50%)")
    else:
        print("  ⚠️ 胜率需优化 (<50%)")
    
    if total_return > 10:
        print("  ✅ 收益优秀 (>10%)")
    elif total_return > 0:
        print("  ⭐ 收益为正")
    else:
        print("  ⚠️ 收益为负，需优化参数")

print("\n" + "=" * 80)
print("✅ 回测完成")
print("=" * 80)
