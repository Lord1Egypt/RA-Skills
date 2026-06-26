"""技术指标计算工具 - MACD/KDJ/RSI/布林带/成交量异动

用法:
    from scripts.technical_indicators import add_all_indicators, detect_signals
    df = add_all_indicators(df)
    signals = detect_signals(df)
"""

import numpy as np
import pandas as pd


def calc_ema(series: pd.Series, period: int) -> pd.Series:
    """指数移动平均线"""
    return series.ewm(span=period, adjust=False).mean()


def calc_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """MACD指标。

    Returns:
        (macd_line, signal_line, histogram)
    """
    ema_fast = calc_ema(close, fast)
    ema_slow = calc_ema(close, slow)
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    hist = (dif - dea) * 2
    return dif, dea, hist


def calc_kdj(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 9, m1: int = 3, m2: int = 3):
    """KDJ指标。

    Returns:
        (K, D, J)
    """
    lowest_low = low.rolling(n, min_periods=1).min()
    highest_high = high.rolling(n, min_periods=1).max()
    rsv = (close - lowest_low) / (highest_high - lowest_low + 1e-9) * 100

    k = pd.Series(np.nan, index=close.index)
    d = pd.Series(np.nan, index=close.index)
    k.iloc[0] = 50.0
    d.iloc[0] = 50.0

    for i in range(1, len(close)):
        k.iloc[i] = (m1 - 1) / m1 * k.iloc[i - 1] + 1 / m1 * rsv.iloc[i]
        d.iloc[i] = (m2 - 1) / m2 * d.iloc[i - 1] + 1 / m2 * k.iloc[i]

    j = 3 * k - 2 * d
    return k, d, j


def calc_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """RSI相对强弱指标"""
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    return 100 - 100 / (1 + rs)


def calc_bollinger(close: pd.Series, period: int = 20, num_std: float = 2.0):
    """布林带。

    Returns:
        (upper, middle, lower)
    """
    mid = close.rolling(period).mean()
    std = close.rolling(period).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    return upper, mid, lower


def calc_volume_ratio(volume: pd.Series, period: int = 5) -> pd.Series:
    """量比 = 当日成交量 / 过去N日平均成交量"""
    avg_vol = volume.rolling(period, min_periods=1).mean()
    return volume / (avg_vol + 1e-9)


def calc_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """ATR平均真实波幅"""
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """一键计算全部技术指标，直接在df上添加列。

    需要df包含: date, open, high, low, close, volume
    """
    df = df.copy()
    df["macd"], df["signal"], df["hist"] = calc_macd(df["close"])
    df["k"], df["d"], df["j"] = calc_kdj(df["high"], df["low"], df["close"])
    df["rsi"] = calc_rsi(df["close"])
    df["boll_upper"], df["boll_mid"], df["boll_lower"] = calc_bollinger(df["close"])
    df["vol_ratio"] = calc_volume_ratio(df["volume"])
    df["atr"] = calc_atr(df["high"], df["low"], df["close"])
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()
    return df


def detect_signals(df: pd.DataFrame) -> pd.DataFrame:
    """检测交易信号（需先调用add_all_indicators）。

    Returns:
        DataFrame with signal column: 1=买入, -1=卖出, 0=持有
    """
    df = df.copy()
    df["signal"] = 0

    # MACD金叉/死叉
    df.loc[df["hist"] > 0, "signal"] = df.loc[df["hist"] > 0, "signal"] | 0  # neutral
    df.loc[(df["hist"] > 0) & (df["hist"].shift(1) <= 0), "signal"] = 1
    df.loc[(df["hist"] < 0) & (df["hist"].shift(1) >= 0), "signal"] = -1

    # KDJ超卖反弹 / 超买回落
    df.loc[(df["j"] < 20) & (df["j"].shift(1) >= 20), "signal"] = 1
    df.loc[(df["j"] > 80) & (df["j"].shift(1) <= 80), "signal"] = -1

    # RSI超卖/超买
    df.loc[df["rsi"] < 30, "signal"] = df.loc[df["rsi"] < 30, "signal"].clip(lower=0) + 1
    df.loc[df["rsi"] > 70, "signal"] = df.loc[df["rsi"] > 70, "signal"].clip(upper=0) - 1

    # 均线交叉
    df.loc[(df["ma5"] > df["ma20"]) & (df["ma5"].shift(1) <= df["ma20"].shift(1)), "signal"] = 1
    df.loc[(df["ma5"] < df["ma20"]) & (df["ma5"].shift(1) >= df["ma20"].shift(1)), "signal"] = -1

    # 布林带回归
    df.loc[(df["close"] <= df["boll_lower"]) & (df["signal"] >= 0), "signal"] = 1
    df.loc[(df["close"] >= df["boll_upper"]) & (df["signal"] <= 0), "signal"] = -1

    # 量价异动：放量+上涨
    df.loc[(df["vol_ratio"] > 2) & (df["close"] > df["open"]), "signal"] = 1

    return df


if __name__ == "__main__":
    from fetch_data import fetch_stock_daily
    df = fetch_stock_daily("000001", "20250101", "20260301")
    if df.empty:
        print("无数据，请检查网络或代码")
    else:
        df = add_all_indicators(df)
        signals = detect_signals(df)
        buys = signals[signals["signal"] == 1]
        sells = signals[signals["signal"] == -1]
        print(f"买入信号: {len(buys)} 个")
        print(f"卖出信号: {len(sells)} 个")
        print(signals[["date", "close", "signal"]].tail(10).to_string(index=False))
