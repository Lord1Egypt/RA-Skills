#!/usr/bin/env python3
"""
Technical Indicator Calculator for Chinese Futures

Provides:
- sma(data, period)         — Simple Moving Average
- ema(data, period)         — Exponential Moving Average
- macd(data)                — MACD (DIF, DEA, histogram)
- rsi(data, period=14)      — Relative Strength Index
- bollinger(data, p=20, k=2) — Bollinger Bands
- kdj(data)                 — KDJ indicator
- golden_death_cross(short, long) — 金叉/死叉 detection
- composite_signal(data)    — Combined signal scoring
"""

def sma(data, period):
    """Simple Moving Average"""
    if len(data) < period:
        return []
    return [sum(data[i-period:i])/period for i in range(period, len(data)+1)]

def ema(data, period):
    """Exponential Moving Average"""
    if len(data) < period:
        return []
    k = 2 / (period + 1)
    result = [sum(data[:period])/period]
    for price in data[period:]:
        result.append(price * k + result[-1] * (1 - k))
    return result

def macd(data):
    """MACD: returns (dif, dea, histogram)"""
    if len(data) < 35:
        return [], [], []
    ema12 = ema(data, 12)
    ema26 = ema(data, 26)
    dif = [ema12[i] - ema26[i] for i in range(len(ema26))]
    dea = ema(dif, 9) if len(dif) >= 9 else []
    # Pad DIF to match DEA length
    hist = [2 * (dif[-len(dea)+i] - dea[i]) for i in range(len(dea))] if dea else []
    return dif, dea, hist

def rsi(data, period=14):
    """Relative Strength Index"""
    if len(data) <= period:
        return []
    gains = []
    losses = []
    for i in range(1, period+1):
        diff = data[i] - data[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains)/period
    avg_loss = sum(losses)/period
    result = []
    for i in range(period, len(data)):
        diff = data[i] - data[i-1]
        avg_gain = (avg_gain * (period-1) + max(diff, 0)) / period
        avg_loss = (avg_loss * (period-1) + max(-diff, 0)) / period
        if avg_loss == 0:
            result.append(100.0)
        else:
            rs = avg_gain / avg_loss
            result.append(100 - 100 / (1 + rs))
    return result

def bollinger(data, period=20, k=2):
    """Bollinger Bands: returns (middle, upper, lower)"""
    if len(data) < period:
        return [], [], []
    middle = sma(data, period)
    upper, lower = [], []
    for i in range(period-1, len(data)):
        window = data[i-period+1:i+1]
        std = (sum((x - sum(window)/period)**2 for x in window) / period) ** 0.5
        upper.append(middle[i-period+1] + k * std)
        lower.append(middle[i-period+1] - k * std)
    return middle, upper, lower

def kdj(data, n=9, k_period=3, d_period=3):
    """KDJ indicator: returns (k_values, d_values, j_values)"""
    if len(data) < n:
        return [], [], []
    rsv = []
    for i in range(n-1, len(data)):
        window = data[i-n+1:i+1]
        low = min(window)
        high = max(window)
        rsv.append((data[i] - low) / (high - low) * 100 if high != low else 50)
    k_vals = [50]
    for v in rsv:
        k_vals.append((2/3)*k_vals[-1] + (1/3)*v)
    k_vals = k_vals[1:]
    d_vals = [50]
    for k in k_vals:
        d_vals.append((2/3)*d_vals[-1] + (1/3)*k)
    d_vals = d_vals[1:]
    j_vals = [3*k - 2*d for k, d in zip(k_vals, d_vals)]
    return k_vals, d_vals, j_vals

def golden_death_cross(short_ma, long_ma):
    """Detect golden cross (金叉) and death cross (死叉).
    Returns: 'golden', 'death', or None"""
    if len(short_ma) < 2 or len(long_ma) < 2:
        return None
    if short_ma[-2] < long_ma[-2] and short_ma[-1] > long_ma[-1]:
        return 'golden'
    if short_ma[-2] > long_ma[-2] and short_ma[-1] < long_ma[-1]:
        return 'death'
    return None

if __name__ == "__main__":
    # Demo
    test_data = [100, 102, 101, 105, 107, 108, 106, 110, 112, 115, 116, 118, 120]
    print(f"SMA(5): {sma(test_data, 5)}")
    print(f"RSI(14): {rsi(test_data)}")
