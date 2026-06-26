#!/usr/bin/env python3
"""A股技术分析工具 - A-Share Technical Analysis Toolkit"""

import json
from datetime import datetime

def calculate_macd(closes, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    ema_fast = sum(closes[:fast]) / fast
    ema_slow = sum(closes[:slow]) / slow
    difs, deas, bars = [], [], []
    
    for i, price in enumerate(closes):
        if i == 0:
            continue
        ema_fast = price * 2/(fast+1) + ema_fast * (1 - 2/(fast+1))
        ema_slow = price * 2/(slow+1) + ema_slow * (1 - 2/(slow+1))
        dif = ema_fast - ema_slow
        dea = dif if i == 1 else deas[-1] * (signal-1)/(signal+1) + dif * 2/(signal+1)
        bar = (dif - dea) * 2
        difs.append(round(dif, 4))
        deas.append(round(dea, 4))
        bars.append(round(bar, 4))
    
    return {"dif": difs, "dea": deas, "macd_bar": bars}

def calculate_kdj(highs, lows, closes, n=9, k=3, d=3):
    """计算KDJ指标"""
    rsv_list, k_list, d_list = [], [], []
    
    for i in range(len(closes)):
        if i < n-1:
            rsv_list.append(50)
            k_list.append(50)
            d_list.append(50)
            continue
        hh = max(highs[i-n+1:i+1])
        ll = min(lows[i-n+1:i+1])
        rsv = (closes[i] - ll) / (hh - ll) * 100 if hh != ll else 50
        k_val = k_list[-1] * (k-1)/k + rsv / k if k_list else rsv
        d_val = d_list[-1] * (d-1)/d + k_val / d if d_list else k_val
        j_val = 3 * k_val - 2 * d_val
        rsv_list.append(round(rsv, 2))
        k_list.append(round(k_val, 2))
        d_list.append(round(d_val, 2))
    
    return {"k": k_list, "d": d_list, "j": [round(3*kv-2*dv, 2) for kv, dv in zip(k_list, d_list)]}

def calculate_rsi(closes, period=14):
    """计算RSI指标"""
    changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains, losses = [], []
    for c in changes:
        gains.append(max(c, 0))
        losses.append(max(-c, 0))
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rsis = []
    
    for i in range(period, len(closes)):
        if i > period:
            avg_gain = (avg_gain * (period-1) + gains[i-1]) / period
            avg_loss = (avg_loss * (period-1) + losses[i-1]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsis.append(round(100 - 100 / (1 + rs), 2))
    
    return {"rsi": rsis}

def find_support_resistance(highs, lows, lookback=20):
    """寻找近期支撑位和阻力位"""
    recent_highs = sorted(highs[-lookback:], reverse=True)[:3]
    recent_lows = sorted(lows[-lookback:])[:3]
    
    return {
        "resistance": recent_highs,
        "support": recent_lows,
        "current_range": f"{recent_lows[0]:.2f} - {recent_highs[0]:.2f}"
    }

def generate_brief(symbol, name, price, change_pct, closes, highs, lows):
    """生成每日复盘简报"""
    macd = calculate_macd(closes)
    kdj = calculate_kdj(highs, lows, closes)
    rsi = calculate_rsi(closes)
    levels = find_support_resistance(highs, lows)
    
    last_macd_bar = macd["macd_bar"][-1] if macd["macd_bar"] else 0
    prev_macd_bar = macd["macd_bar"][-2] if len(macd["macd_bar"]) > 1 else 0
    k = kdj["k"][-1] if kdj["k"] else 50
    last_rsi = rsi["rsi"][-1] if rsi["rsi"] else 50
    
    signals = []
    if last_macd_bar > 0 and prev_macd_bar <= 0:
        signals.append("MACD转红柱 ✅")
    elif last_macd_bar < 0 and prev_macd_bar >= 0:
        signals.append("MACD转绿柱 ⚠️")
    if k > 80:
        signals.append("KDJ超买区 ⚠️")
    elif k < 20:
        signals.append("KDJ超卖区 💡")
    if last_rsi > 70:
        signals.append("RSI超买 ⚠️")
    elif last_rsi < 30:
        signals.append("RSI超卖 💡")
    
    report = f"""
═══════════════════════════════
{name} ({symbol}) 技术面简报
{datetime.now().strftime('%Y-%m-%d %H:%M')}
───────────────────────────
当前价格: ¥{price:.2f}  ({change_pct:+.2f}%)
───────────────────────────
MACD柱: {last_macd_bar:+.4f}  {'📈' if last_macd_bar>0 else '📉'}
KDJ(K): {k:.1f}  {'⚠️' if k>80 else '💡' if k<20 else '✅'}
RSI(14): {last_rsi:.1f}  {'⚠️' if last_rsi>70 else '💡' if last_rsi<30 else '✅'}
───────────────────────────
支撑位: {', '.join(f'¥{s:.2f}' for s in levels['support'])}
阻力位: {', '.join(f'¥{r:.2f}' for r in levels['resistance'])}
───────────────────────────
信号: {' | '.join(signals) if signals else '暂无明确信号'}
═══════════════════════════════
"""
    return report

if __name__ == "__main__":
    # 示例数据
    closes = [10.5, 10.6, 10.8, 10.7, 10.9, 11.0, 10.8, 10.6, 10.7, 10.9,
              11.2, 11.5, 11.3, 11.1, 11.4, 11.6, 11.8, 11.5, 11.3, 11.0,
              11.2, 11.5, 11.7, 11.9, 12.0, 11.8, 11.6, 11.9, 12.2, 12.5]
    highs = [c+0.3 for c in closes]
    lows = [c-0.3 for c in closes]
    
    print(generate_brief("600519.SH", "贵州茅台", 120.0, 2.5, closes, highs, lows))
