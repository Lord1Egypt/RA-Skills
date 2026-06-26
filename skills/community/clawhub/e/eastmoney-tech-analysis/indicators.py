#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票技术指标计算模块
KDJ, MACD, BOLL 指标
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional


def calculate_kdj(df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> Dict[str, List]:
    """
    计算KDJ指标

    Args:
        df: 包含 high/low/close 列的DataFrame
        n: RSV周期 (默认9)
        m1: K平滑因子 (默认3)
        m2: D平滑因子 (默认3)

    Returns:
        Dict: 包含 k, d, j, signal (金叉/死叉信号)
    """
    if len(df) < n:
        return {'k': [], 'd': [], 'j': [], 'signal': []}

    low_list = df['low'].rolling(window=n, min_periods=1).min()
    high_list = df['high'].rolling(window=n, min_periods=1).max()
    
    rsv = (df['close'] - low_list) / (high_list - low_list + 1e-8) * 100
    
    # 计算K, D, J
    k = rsv.ewm(alpha=1/m1, adjust=False).mean()
    d = k.ewm(alpha=1/m2, adjust=False).mean()
    j = 3 * k - 2 * d
    
    # 信号判断
    pre_j = j.shift(1).fillna(0)
    signal = []
    for i in range(len(j)):
        if i == 0:
            signal.append(0)
        else:
            if pre_j.iloc[i-1] < 20 and j.iloc[i] >= 20:
                signal.append(1)  # 金叉
            elif pre_j.iloc[i-1] > 80 and j.iloc[i] <= 80:
                signal.append(-1)  # 死叉
            else:
                signal.append(0)
    
    return {
        'k': k.fillna(0).tolist(),
        'd': d.fillna(0).tolist(),
        'j': j.fillna(0).tolist(),
        'signal': signal
    }


def calculate_macd(df: pd.DataFrame, short: int = 12, long: int = 26, mid: int = 9) -> Dict[str, List]:
    """
    计算MACD指标

    Args:
        df: 包含 close 列的DataFrame
        short: 短期EMA周期 (默认12)
        long: 长期EMA周期 (默认26)
        mid: DEA平滑周期 (默认9)

    Returns:
        Dict: 包含 dif, dea, macd, signal (金叉/死叉信号)
    """
    if len(df) < long:
        return {'dif': [], 'dea': [], 'macd': [], 'signal': []}
    
    close = df['close']
    
    # 计算EMA
    ema_short = close.ewm(span=short, adjust=False).mean()
    ema_long = close.ewm(span=long, adjust=False).mean()
    
    dif = ema_short - ema_long
    dea = dif.ewm(span=mid, adjust=False).mean()
    macd = (dif - dea) * 2
    
    # 信号判断
    pre_dif = dif.shift(1)
    pre_dea = dea.shift(1)
    
    signal = []
    for i in range(len(dif)):
        if i == 0:
            signal.append(0)
        else:
            if pre_dif.iloc[i-1] < pre_dea.iloc[i-1] and dif.iloc[i] > dea.iloc[i]:
                signal.append(1)  # 金叉
            elif pre_dif.iloc[i-1] > pre_dea.iloc[i-1] and dif.iloc[i] < dea.iloc[i]:
                signal.append(-1)  # 死叉
            else:
                signal.append(0)
    
    return {
        'dif': dif.fillna(0).tolist(),
        'dea': dea.fillna(0).tolist(),
        'macd': macd.fillna(0).tolist(),
        'signal': signal
    }


def calculate_boll(df: pd.DataFrame, period: int = 20, std_dev: int = 2) -> Dict[str, List]:
    """
    计算BOLL指标

    Args:
        df: 包含 close 列的DataFrame
        period: 中轨周期 (默认20)
        std_dev: 标准差倍数 (默认2)

    Returns:
        Dict: 包含 upper, middle, lower
    """
    if len(df) < period:
        return {'upper': [], 'middle': [], 'lower': []}
    
    close = df['close']
    
    middle = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    
    upper = middle + std_dev * std
    lower = middle - std_dev * std
    
    return {
        'upper': upper.fillna(0).tolist(),
        'middle': middle.fillna(0).tolist(),
        'lower': lower.fillna(0).tolist()
    }


def calculate_ma(df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> Dict[str, List]:
    """
    计算移动平均线

    Args:
        df: 包含 close 列的DataFrame
        periods: MA周期列表

    Returns:
        Dict: 包含各周期MA值
    """
    result = {}
    close = df['close']
    
    for p in periods:
        result[f'ma{p}'] = close.rolling(window=p).mean().fillna(0).tolist()
    
    return result


def get_latest_signals(df: pd.DataFrame) -> Dict:
    """
    获取最新交易信号

    Args:
        df: K线数据DataFrame

    Returns:
        Dict: 包含各指标的金叉/死叉状态
    """
    if len(df) < 30:
        return {'status': '数据不足'}
    
    kdj = calculate_kdj(df)
    macd = calculate_macd(df)
    
    latest_idx = -1
    
    # KDJ信号
    kdj_signal = kdj['signal'][latest_idx] if kdj['signal'] else 0
    kdj_status = "超买" if kdj['j'][latest_idx] > 80 else ("超卖" if kdj['j'][latest_idx] < 20 else "正常")
    
    # MACD信号
    macd_signal = macd['signal'][latest_idx] if macd['signal'] else 0
    macd_trend = "多头" if macd['dif'][latest_idx] > macd['dea'][latest_idx] else "空头"
    
    # 价格位置
    latest = df.iloc[-1]
    boll = calculate_boll(df)
    
    if boll['upper']:
        price_vs_boll = "突破上轨" if latest['close'] > boll['upper'][-1] else \
                       ("跌破下轨" if latest['close'] < boll['lower'][-1] else "震荡区间")
    else:
        price_vs_boll = "数据不足"
    
    return {
        'kdj': {'signal': kdj_signal, 'status': kdj_status, 'j': round(kdj['j'][latest_idx], 2)},
        'macd': {'signal': macd_signal, 'trend': macd_trend},
        'boll': price_vs_boll,
        'price': {'close': latest['close'], 'pct_chg': latest.get('pct_chg', 0)},
        'date': latest['date']
    }


if __name__ == "__main__":
    # 测试
    import eastmoney_spider
    
    spider = eastmoney_spider.EastmoneySpider()
    df = spider.get_stock_kline("600519", days=100)
    
    print("=== KDJ ===")
    kdj = calculate_kdj(df)
    print(f"最新K: {kdj['k'][-1]:.2f}, D: {kdj['d'][-1]:.2f}, J: {kdj['j'][-1]:.2f}")
    
    print("\n=== MACD ===")
    macd = calculate_macd(df)
    print(f"最新DIF: {macd['dif'][-1]:.4f}, DEA: {macd['dea'][-1]:.4f}, MACD: {macd['macd'][-1]:.4f}")
    
    print("\n=== BOLL ===")
    boll = calculate_boll(df)
    print(f"最新上轨: {boll['upper'][-1]:.2f}, 中轨: {boll['middle'][-1]:.2f}, 下轨: {boll['lower'][-1]:.2f}")
    
    print("\n=== 最新信号 ===")
    signals = get_latest_signals(df)
    print(signals)