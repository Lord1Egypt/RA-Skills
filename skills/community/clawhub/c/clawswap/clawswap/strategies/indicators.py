"""
Built-in indicator functions for custom strategies.

Usage in strategy(df):
    from strategies.indicators import rsi, macd, ema, bollinger, atr, adx, sma

All functions accept pandas Series or numpy arrays and return pandas Series.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Tuple


def sma(prices: pd.Series, period: int = 20) -> pd.Series:
    """Simple Moving Average."""
    return prices.rolling(window=period, min_periods=period).mean()


def ema(prices: pd.Series, period: int = 20) -> pd.Series:
    """Exponential Moving Average."""
    return prices.ewm(span=period, adjust=False).mean()


def rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (0-100)."""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100.0 - 100.0 / (1.0 + rs)


def macd(
    prices: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """MACD (line, signal, histogram)."""
    fast_ema = prices.ewm(span=fast, adjust=False).mean()
    slow_ema = prices.ewm(span=slow, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger(
    prices: pd.Series,
    period: int = 20,
    std_dev: float = 2.0,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Bollinger Bands (upper, middle, lower)."""
    middle = prices.rolling(window=period, min_periods=period).mean()
    std = prices.rolling(window=period, min_periods=period).std()
    upper = middle + std_dev * std
    lower = middle - std_dev * std
    return upper, middle, lower


def atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14,
) -> pd.Series:
    """Average True Range."""
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()


def adx(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Average Directional Index (ADX, +DI, -DI)."""
    prev_high = high.shift(1)
    prev_low = low.shift(1)

    plus_dm = (high - prev_high).where((high - prev_high) > (prev_low - low), 0.0)
    plus_dm = plus_dm.where(plus_dm > 0, 0.0)
    minus_dm = (prev_low - low).where((prev_low - low) > (high - prev_high), 0.0)
    minus_dm = minus_dm.where(minus_dm > 0, 0.0)

    tr = atr(high, low, close, period=1)  # True Range (not averaged)
    atr_val = tr.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()

    plus_di = 100 * (plus_dm.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean() / atr_val)
    minus_di = 100 * (minus_dm.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean() / atr_val)

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    adx_val = dx.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()

    return adx_val, plus_di, minus_di


def vwap(close: pd.Series, volume: pd.Series, period: int = 0) -> pd.Series:
    """Volume-Weighted Average Price. period=0 means cumulative (session VWAP)."""
    if period > 0:
        cum_vol = volume.rolling(period).sum()
        cum_pv = (close * volume).rolling(period).sum()
        return cum_pv / cum_vol.replace(0, np.nan)
    else:
        cum_vol = volume.cumsum()
        cum_pv = (close * volume).cumsum()
        return cum_pv / cum_vol.replace(0, np.nan)


def stochastic(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    k_period: int = 14,
    d_period: int = 3,
) -> Tuple[pd.Series, pd.Series]:
    """Stochastic Oscillator (%K, %D)."""
    lowest_low = low.rolling(k_period).min()
    highest_high = high.rolling(k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan)
    d = k.rolling(d_period).mean()
    return k, d


def supertrend(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 10,
    multiplier: float = 3.0,
) -> Tuple[pd.Series, pd.Series]:
    """Supertrend (line, direction). direction: 1=uptrend, -1=downtrend."""
    atr_val = atr(high, low, close, period)
    hl2 = (high + low) / 2

    upper = hl2 + multiplier * atr_val
    lower = hl2 - multiplier * atr_val

    st = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(index=close.index, dtype=float)
    st.iloc[0] = upper.iloc[0]
    direction.iloc[0] = 1

    for i in range(1, len(close)):
        if close.iloc[i] > upper.iloc[i - 1] if not np.isnan(upper.iloc[i - 1]) else False:
            st.iloc[i] = lower.iloc[i]
            direction.iloc[i] = 1
        elif close.iloc[i] < lower.iloc[i - 1] if not np.isnan(lower.iloc[i - 1]) else False:
            st.iloc[i] = upper.iloc[i]
            direction.iloc[i] = -1
        else:
            if direction.iloc[i - 1] == 1:
                st.iloc[i] = max(lower.iloc[i], st.iloc[i - 1]) if not np.isnan(st.iloc[i - 1]) else lower.iloc[i]
                direction.iloc[i] = 1
            else:
                st.iloc[i] = min(upper.iloc[i], st.iloc[i - 1]) if not np.isnan(st.iloc[i - 1]) else upper.iloc[i]
                direction.iloc[i] = -1

    return st, direction
