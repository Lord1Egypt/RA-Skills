"""Technical indicator calculations. All functions take a DataFrame with OHLCV columns."""

import pandas as pd


def calc_rsi(prices: pd.Series, period: int = 14) -> float | None:
    if len(prices) < period + 1:
        return None
    delta = prices.diff()
    gains = delta.where(delta > 0, 0).rolling(window=period).mean()
    losses = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    val = rsi.iloc[-1]
    return float(val) if pd.notna(val) else None


def calc_kdj(hist: pd.DataFrame, n: int = 9, m: int = 3) -> tuple[float, float, float] | None:
    if len(hist) < n:
        return None
    low_n = hist["Low"].rolling(n).min()
    high_n = hist["High"].rolling(n).max()
    rsv = (hist["Close"] - low_n) / (high_n - low_n + 1e-9) * 100
    k = rsv.ewm(com=m - 1, adjust=False).mean()
    d = k.ewm(com=m - 1, adjust=False).mean()
    j = 3 * k - 2 * d
    if pd.isna(k.iloc[-1]):
        return None
    return float(k.iloc[-1]), float(d.iloc[-1]), float(j.iloc[-1])


def calc_adx(hist: pd.DataFrame, period: int = 14) -> float | None:
    if len(hist) < period * 2:
        return None
    high, low, close = hist["High"], hist["Low"], hist["Close"]
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    raw_plus = high.diff().clip(lower=0)
    raw_minus = (-low.diff()).clip(lower=0)
    cond = raw_plus > raw_minus
    dm_plus = raw_plus.where(cond, 0.0)
    dm_minus = raw_minus.where(~cond, 0.0)
    atr = tr.ewm(span=period, adjust=False).mean()
    di_plus = 100 * dm_plus.ewm(span=period, adjust=False).mean() / atr
    di_minus = 100 * dm_minus.ewm(span=period, adjust=False).mean() / atr
    dx = (100 * (di_plus - di_minus).abs() / (di_plus + di_minus + 1e-9)).fillna(0)
    adx = dx.ewm(span=period, adjust=False).mean()
    val = adx.iloc[-1]
    return float(val) if pd.notna(val) else None


def calc_obv(hist: pd.DataFrame) -> tuple[float, str] | None:
    if len(hist) < 20:
        return None
    direction = hist["Close"].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    obv = (direction * hist["Volume"]).cumsum()
    recent = obv.iloc[-10:].mean()
    prev = obv.iloc[-20:-10].mean()
    trend = "up" if recent > prev * 1.02 else ("down" if recent < prev * 0.98 else "flat")
    return float(obv.iloc[-1]), trend


def calc_mfi(hist: pd.DataFrame, period: int = 14) -> float | None:
    if len(hist) < period + 1:
        return None
    tp = (hist["High"] + hist["Low"] + hist["Close"]) / 3
    mf = tp * hist["Volume"]
    pos_mf = mf.where(tp > tp.shift(), 0.0).rolling(period).sum()
    neg_mf = mf.where(tp <= tp.shift(), 0.0).rolling(period).sum()
    mfi = 100 - 100 / (1 + pos_mf / neg_mf.replace(0, float("nan")))
    val = mfi.iloc[-1]
    return float(val) if pd.notna(val) else None


def calc_atr(hist: pd.DataFrame, period: int = 14) -> float | None:
    if len(hist) < period + 1:
        return None
    high, low, close = hist["High"], hist["Low"], hist["Close"]
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.ewm(span=period, adjust=False).mean()
    val = atr.iloc[-1]
    return float(val) if pd.notna(val) else None


def calc_cci(hist: pd.DataFrame, period: int = 20) -> float | None:
    if len(hist) < period:
        return None
    tp = (hist["High"] + hist["Low"] + hist["Close"]) / 3
    ma = tp.rolling(period).mean()
    md = tp.rolling(period).apply(lambda x: abs(x - x.mean()).mean())
    cci = (tp - ma) / (0.015 * md + 1e-9)
    val = cci.iloc[-1]
    return float(val) if pd.notna(val) else None


def calc_bb_bandwidth(close: pd.Series, period: int = 20) -> float | None:
    if len(close) < period:
        return None
    ma = close.rolling(period).mean()
    std = close.rolling(period).std()
    bw = (4 * std / ma * 100).iloc[-1]
    return float(bw) if pd.notna(bw) else None


def calc_hist_volatility(close: pd.Series, period: int = 20) -> float | None:
    if len(close) < period + 1:
        return None
    ret = close.pct_change().dropna()
    hv = float(ret.iloc[-period:].std() * (252 ** 0.5) * 100)
    return hv


def calc_pivot_points(hist: pd.DataFrame) -> dict | None:
    if len(hist) < 2:
        return None
    prev = hist.iloc[-2]
    pp = (prev["High"] + prev["Low"] + prev["Close"]) / 3
    r1 = 2 * pp - prev["Low"]
    s1 = 2 * pp - prev["High"]
    r2 = pp + (prev["High"] - prev["Low"])
    s2 = pp - (prev["High"] - prev["Low"])
    return {"pp": round(pp, 4), "r1": round(r1, 4), "s1": round(s1, 4), "r2": round(r2, 4), "s2": round(s2, 4)}


def detect_candlestick(hist: pd.DataFrame) -> tuple[str, float] | None:
    """Returns (pattern_name, signal_strength -1~+1) or None."""
    if len(hist) < 3:
        return None
    o2, c2 = hist["Open"].iloc[-3], hist["Close"].iloc[-3]
    o1, c1 = hist["Open"].iloc[-2], hist["Close"].iloc[-2]
    o0, h0, l0, c0 = hist["Open"].iloc[-1], hist["High"].iloc[-1], hist["Low"].iloc[-1], hist["Close"].iloc[-1]
    body0 = abs(c0 - o0)
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    rng0 = h0 - l0 if h0 != l0 else 1e-9
    lower0 = min(o0, c0) - l0
    upper0 = h0 - max(o0, c0)

    if c1 < o1 and c0 > o0 and c0 > o1 and o0 < c1:
        return "bullish_engulfing", 0.6
    if c1 > o1 and c0 < o0 and c0 < o1 and o0 > c1:
        return "bearish_engulfing", -0.6
    if body0 > 0 and lower0 > 2 * body0 and upper0 < body0 * 0.5:
        return "hammer", 0.5
    if body0 > 0 and upper0 > 2 * body0 and lower0 < body0 * 0.5:
        return "shooting_star", -0.5
    if c2 < o2 and body2 > 0 and body1 < body2 * 0.3 and c0 > o0 and c0 > (o2 + c2) / 2:
        return "morning_star", 0.7
    if c2 > o2 and body2 > 0 and body1 < body2 * 0.3 and c0 < o0 and c0 < (o2 + c2) / 2:
        return "evening_star", -0.7
    return None
