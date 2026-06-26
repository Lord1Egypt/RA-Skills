"""技术指标引擎"""
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Tuple

def compute_all(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _moving_averages(df)
    df = _volume_ma(df)
    df = _macd(df)
    df = _rsi(df)
    df = _kdj(df)
    df = _bollinger(df)
    df = _atr(df)
    return df

def _moving_averages(df):
    for p in [5, 10, 20, 60, 120]:
        df[f"ma{p}"] = df["close"].rolling(p, min_periods=1).mean()
    return df

def _volume_ma(df):
    for p in [5, 10]:
        df[f"vol_ma{p}"] = df["volume"].rolling(p, min_periods=1).mean()
    return df

def _macd(df):
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["dif"] = ema12 - ema26
    df["dea"] = df["dif"].ewm(span=9, adjust=False).mean()
    df["macd"] = (df["dif"] - df["dea"]) * 2
    return df

def _rsi(df, period=14):
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0).rolling(period, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period, min_periods=1).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))
    df["rsi"] = df["rsi"].fillna(50)
    return df

def _kdj(df, n=9):
    low_min = df["low"].rolling(n, min_periods=1).min()
    high_max = df["high"].rolling(n, min_periods=1).max()
    denom = (high_max - low_min).replace(0, np.nan)
    rsv = ((df["close"] - low_min) / denom * 100).fillna(50)
    df["k"] = rsv.ewm(com=2, adjust=False).mean()
    df["d"] = df["k"].ewm(com=2, adjust=False).mean()
    df["j"] = 3 * df["k"] - 2 * df["d"]
    return df

def _bollinger(df, period=20):
    df["boll_mid"] = df["close"].rolling(period, min_periods=1).mean()
    std = df["close"].rolling(period, min_periods=1).std().fillna(0)
    df["boll_upper"] = df["boll_mid"] + 2 * std
    df["boll_lower"] = df["boll_mid"] - 2 * std
    return df

def _atr(df, period=14):
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift()).abs()
    lc = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    df["atr"] = tr.rolling(period, min_periods=1).mean()
    return df

def latest_indicators(df: pd.DataFrame) -> Dict[str, float]:
    if df.empty: return {}
    last = df.iloc[-1]
    keys = ["close","ma5","ma10","ma20","ma60","ma120","vol_ma5","dif","dea","macd","rsi","k","d","j","boll_mid","boll_upper","boll_lower","atr"]
    return {k: round(float(last.get(k, 0)), 4) for k in keys}

def support_resistance(df: pd.DataFrame) -> Tuple[float, float]:
    last = df.iloc[-1]
    recent = df.tail(20)
    supports = [last.get("ma20",0), last.get("boll_lower",0), recent["low"].min(), last.get("ma60",0)]
    support = round(min(s for s in supports if s > 0), 2)
    current = float(last["close"])
    resistances = [last.get("ma60",current*2) if current < last.get("ma60",0) else last.get("ma120",current*2),
                   last.get("boll_upper",current*2), recent["high"].max(), current*1.08]
    resistance = round(min(r for r in resistances if r > current), 2)
    return support, resistance
