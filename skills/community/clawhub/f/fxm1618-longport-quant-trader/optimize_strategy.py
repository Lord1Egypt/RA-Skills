#!/usr/bin/env python3
"""
港股策略参数优化 - 网格搜索最优参数
测试多组参数组合，找出最佳配置
"""
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from itertools import product

# 配置
HK_STOCKS = ["9988.HK", "1211.HK", "9618.HK"]  # 排除美团（胜率低）
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=90)

# 参数网格
MOMENTUM_THRESHOLDS = [0.01, 0.015, 0.02, 0.025, 0.03]  # 1%-3%
REVERSION_THRESHOLDS = [-0.02, -0.025, -0.03, -0.035, -0.04]  # -2% to -4%
STOP_LOSSES = [-0.03, -0.04, -0.05, -0.06]  # -3% to -6%
TAKE_PROFITS = [0.08, 0.10, 0.12, 0.15]  # 8%-15%

print("\n" + "=" * 80)
print("🔬 策略参数优化 - 网格搜索")
print("=" * 80)
print(f"回测区间：{START_DATE.strftime('%Y-%m-%d')} 至 {END_DATE.strftime('%Y-%m-%d')}")
print(f"股票池：{', '.join(HK_STOCKS)}")
print(f"参数组合：{len(MOMENTUM_THRESHOLDS)} × {len(REVERSION_THRESHOLDS)} × {len(STOP_LOSSES)} × {len(TAKE_PROFITS)} = {len(MOMENTUM_THRESHOLDS)*len(REVERSION_THRESHOLDS)*len(STOP_LOSSES)*len(TAKE_PROFITS)} 组")
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
    except Exception as e:
        print(f"  ❌ {symbol}: {e}")

if not data:
    print("\n❌ 无可用数据")
    exit()

# 回测函数
def backtest_strategy(df, mom_thresh, rev_thresh, sl, tp):
    """回测单组参数"""
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    
    signals = []
    in_position = False
    entry_price = 0
    wins = 0
    losses = 0
    total_return = 0
    
    for i, row in df.iterrows():
        ret = row['Return']
        price = float(row['Close'])
        
        if pd.isna(ret):
            continue
        
        # 开仓信号
        if not in_position:
            if ret >= mom_thresh or ret <= rev_thresh:
                in_position = True
                entry_price = price
                signals.append({'type': 'BUY', 'price': price, 'date': i})
        
        # 平仓检查
        else:
            pnl = (price - entry_price) / entry_price
            
            # 止损
            if pnl <= sl:
                in_position = False
                total_return += pnl
                losses += 1
                signals.append({'type': 'SELL_SL', 'price': price, 'pnl': pnl})
            
            # 止盈
            elif pnl >= tp:
                in_position = False
                total_return += pnl
                wins += 1
                signals.append({'type': 'SELL_TP', 'price': price, 'pnl': pnl})
    
    # 计算绩效
    total_trades = wins + losses
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    return {
        'total_return': total_return * 100,
        'win_rate': win_rate,
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses
    }

# 网格搜索
print("\n🔬 开始网格搜索...")
print("=" * 80)

best_result = None
best_params = None
all_results = []

test_count = 0
for mom, rev, sl, tp in product(MOMENTUM_THRESHOLDS, REVERSION_THRESHOLDS, STOP_LOSSES, TAKE_PROFITS):
    test_count += 1
    
    # 对每只股票回测
    stock_results = []
    for symbol, df in data.items():
        result = backtest_strategy(df, mom, rev, sl, tp)
        stock_results.append(result)
    
    # 计算平均绩效
    avg_return = sum(r['total_return'] for r in stock_results) / len(stock_results)
    avg_win_rate = sum(r['win_rate'] for r in stock_results) / len(stock_results)
    total_trades = sum(r['total_trades'] for r in stock_results)
    
    # 综合评分（收益 60% + 胜率 40%）
    score = avg_return * 0.6 + avg_win_rate * 0.4
    
    all_results.append({
        'params': (mom, rev, sl, tp),
        'avg_return': avg_return,
        'avg_win_rate': avg_win_rate,
        'total_trades': total_trades,
        'score': score
    })
    
    # 更新最优
    if best_result is None or score > best_result.get('score', -999):
        best_result = {
            'avg_return': avg_return,
            'avg_win_rate': avg_win_rate,
            'total_trades': total_trades,
            'score': score
        }
        best_params = (mom, rev, sl, tp)
    
    # 进度
    if test_count % 50 == 0:
        print(f"  已测试 {test_count}/{len(MOMENTUM_THRESHOLDS)*len(REVERSION_THRESHOLDS)*len(STOP_LOSSES)*len(TAKE_PROFITS)} 组...")

# 输出最优结果
print("\n" + "=" * 80)
print("🏆 最优参数组合")
print("=" * 80)

if best_params:
    mom, rev, sl, tp = best_params
    print(f"\n参数配置：")
    print(f"  动量阈值：+{mom*100:.1f}%")
    print(f"  均值回归阈值：{rev*100:.1f}%")
    print(f"  止损：{sl*100:.1f}%")
    print(f"  止盈：+{tp*100:.1f}%")
    
    print(f"\n回测绩效：")
    print(f"  平均收益：{best_result['avg_return']:.2f}%")
    print(f"  平均胜率：{best_result['avg_win_rate']:.1f}%")
    print(f"  总交易数：{best_result['total_trades']} 次")
    print(f"  综合评分：{best_result['avg_return']*0.6 + best_result['avg_win_rate']*0.4:.2f}")

# Top 10 结果
print("\n" + "=" * 80)
print("📊 Top 10 参数组合")
print("=" * 80)

all_results.sort(key=lambda x: x['score'], reverse=True)

for i, r in enumerate(all_results[:10], 1):
    mom, rev, sl, tp = r['params']
    print(f"\n{i}. 评分：{r['score']:.2f}")
    print(f"   参数：+{mom*100:.1f}% / {rev*100:.1f}% / {sl*100:.1f}% / +{tp*100:.1f}%")
    print(f"   收益：{r['avg_return']:.2f}% | 胜率：{r['avg_win_rate']:.1f}% | 交易：{r['total_trades']}次")

print("\n" + "=" * 80)
print("✅ 参数优化完成")
print("=" * 80)
