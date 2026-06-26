"""Three-horizon analysis: short / medium / long term scoring."""

from dataclasses import dataclass
import pandas as pd

from indicators import (
    calc_rsi, calc_kdj, calc_cci, calc_adx, calc_obv, calc_mfi,
    calc_atr, calc_bb_bandwidth, calc_hist_volatility, calc_pivot_points,
    detect_candlestick,
)


@dataclass
class HorizonSignal:
    horizon: str
    recommendation: str
    confidence: float
    score: float
    points: list[str]


@dataclass
class MultiHorizonSignal:
    ticker: str
    name: str
    market: str
    short: HorizonSignal
    medium: HorizonSignal
    long: HorizonSignal
    timestamp: str


def _make_signal(horizon: str, scores: list[float], points: list[str]) -> HorizonSignal:
    if not scores:
        return HorizonSignal(horizon=horizon, recommendation="HOLD", confidence=0.0, score=0.0, points=["数据不足"])
    score = max(-1.0, min(1.0, sum(scores) / len(scores)))
    rec = "BUY" if score > 0.25 else ("SELL" if score < -0.25 else "HOLD")
    confidence = round(min(100.0, abs(score) * 100 * (1 + len(scores) * 0.05)), 1)
    return HorizonSignal(horizon=horizon, recommendation=rec, confidence=confidence, score=round(score, 4), points=points)


def analyze_short_term(current_price: float, hist: pd.DataFrame) -> HorizonSignal:
    """短期 (≤2周): KDJ, RSI(7), CCI, K线形态, 量比, Pivot Points"""
    scores, points = [], []

    rsi7 = calc_rsi(hist["Close"], period=7)
    if rsi7 is not None:
        if rsi7 < 25:
            scores.append(0.6); points.append(f"RSI(7) {rsi7:.0f} 超卖")
        elif rsi7 > 75:
            scores.append(-0.6); points.append(f"RSI(7) {rsi7:.0f} 超买")
        else:
            scores.append((50 - rsi7) / 50 * 0.3)

    kdj = calc_kdj(hist)
    if kdj:
        k, d, j = kdj
        if k < 20:
            scores.append(0.5); points.append(f"KDJ K={k:.0f} 超卖")
        elif k > 80:
            scores.append(-0.5); points.append(f"KDJ K={k:.0f} 超买")
        elif k > d:
            scores.append(0.2); points.append(f"KDJ 金叉 K={k:.0f}")
        else:
            scores.append(-0.2); points.append(f"KDJ 死叉 K={k:.0f}")

    cci = calc_cci(hist)
    if cci is not None:
        if cci < -100:
            scores.append(0.4); points.append(f"CCI {cci:.0f} 超卖")
        elif cci > 100:
            scores.append(-0.4); points.append(f"CCI {cci:.0f} 超买")
        else:
            scores.append(0.0)

    pattern = detect_candlestick(hist)
    if pattern:
        name, strength = pattern
        scores.append(strength * 0.8)
        points.append(f"K线: {name} ({'看涨' if strength > 0 else '看跌'})")

    if "Volume" in hist.columns and len(hist) >= 20:
        vol5 = hist["Volume"].iloc[-5:].mean()
        vol20 = hist["Volume"].iloc[-20:].mean()
        if vol20 > 0:
            ratio = vol5 / vol20
            chg = (hist["Close"].iloc[-1] - hist["Close"].iloc[-5]) / hist["Close"].iloc[-5] * 100
            if ratio > 1.5 and chg > 0:
                scores.append(0.3); points.append(f"放量上涨 量比{ratio:.1f}x")
            elif ratio > 1.5 and chg < 0:
                scores.append(-0.3); points.append(f"放量下跌 量比{ratio:.1f}x")

    pp = calc_pivot_points(hist)
    if pp:
        if current_price > pp["r1"]:
            scores.append(0.3); points.append(f"突破R1={pp['r1']:.2f}")
        elif current_price < pp["s1"]:
            scores.append(-0.3); points.append(f"跌破S1={pp['s1']:.2f}")

    return _make_signal("short", scores, points)


def analyze_medium_term(current_price: float, hist: pd.DataFrame) -> HorizonSignal:
    """中期 (2周~6月): MACD, RSI(14), ADX, 布林带, OBV, MA排列, MFI"""
    close = hist["Close"]
    scores, points = [], []

    rsi14 = calc_rsi(close, period=14)
    if rsi14 is not None:
        if rsi14 < 30:
            scores.append(0.5); points.append(f"RSI(14) {rsi14:.0f} 超卖")
        elif rsi14 > 70:
            scores.append(-0.5); points.append(f"RSI(14) {rsi14:.0f} 超买")
        else:
            scores.append((50 - rsi14) / 100)

    # MACD
    if len(close) >= 35:
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        sig = macd.ewm(span=9, adjust=False).mean()
        mv, sv = float(macd.iloc[-1]), float(sig.iloc[-1])
        if mv > sv and mv > 0:
            scores.append(0.4); points.append("MACD 金叉（零轴上方）")
        elif mv > sv:
            scores.append(0.2); points.append("MACD 金叉")
        elif mv < sv and mv < 0:
            scores.append(-0.4); points.append("MACD 死叉（零轴下方）")
        else:
            scores.append(-0.2); points.append("MACD 死叉")

    adx = calc_adx(hist)
    if adx is not None:
        points.append(f"ADX {adx:.0f} {'趋势强' if adx > 25 else '震荡市'}")

    # MA排列
    if len(close) >= 60:
        ma5 = float(close.rolling(5).mean().iloc[-1])
        ma20 = float(close.rolling(20).mean().iloc[-1])
        ma60 = float(close.rolling(60).mean().iloc[-1])
        if current_price > ma5 > ma20 > ma60:
            scores.append(0.5); points.append("多头排列 P>MA5>MA20>MA60")
        elif current_price < ma5 < ma20 < ma60:
            scores.append(-0.5); points.append("空头排列 P<MA5<MA20<MA60")
        elif current_price > ma20:
            scores.append(0.2)
        else:
            scores.append(-0.2)

    # 布林带
    if len(close) >= 20:
        ma20s = close.rolling(20).mean()
        std20 = close.rolling(20).std()
        bb_upper = float((ma20s + 2 * std20).iloc[-1])
        bb_lower = float((ma20s - 2 * std20).iloc[-1])
        bb_range = bb_upper - bb_lower
        if bb_range > 0:
            bb_pos = (current_price - bb_lower) / bb_range
            if bb_pos > 0.95:
                scores.append(-0.3); points.append("触及布林上轨")
            elif bb_pos < 0.05:
                scores.append(0.3); points.append("触及布林下轨")

    obv_result = calc_obv(hist)
    if obv_result:
        _, obv_trend = obv_result
        if obv_trend == "up":
            scores.append(0.3); points.append("OBV 上升（资金流入）")
        elif obv_trend == "down":
            scores.append(-0.3); points.append("OBV 下降（资金流出）")

    mfi = calc_mfi(hist)
    if mfi is not None:
        if mfi < 20:
            scores.append(0.4); points.append(f"MFI {mfi:.0f} 超卖")
        elif mfi > 80:
            scores.append(-0.4); points.append(f"MFI {mfi:.0f} 超买")

    return _make_signal("medium", scores, points)


def analyze_long_term(current_price: float, hist: pd.DataFrame, financials: dict, analyst_forecasts: list[dict] | None) -> HorizonSignal:
    """长期 (6月+): EMA200, MA120, 基本面, 估值, 分析师, 波动率"""
    close = hist["Close"]
    scores, points = [], []

    if len(close) >= 200:
        ema200 = float(close.ewm(span=200, adjust=False).mean().iloc[-1])
        pct = (current_price - ema200) / ema200 * 100
        if current_price > ema200:
            scores.append(0.4); points.append(f"价格在EMA200上方 +{pct:.1f}%")
        else:
            scores.append(-0.4); points.append(f"价格在EMA200下方 {pct:.1f}%")

    if len(close) >= 120:
        ma120 = float(close.rolling(120).mean().iloc[-1])
        if current_price > ma120:
            scores.append(0.3); points.append("价格在MA120上方")
        else:
            scores.append(-0.3); points.append("价格在MA120下方")

    hv = calc_hist_volatility(close)
    if hv is not None:
        points.append(f"历史波动率(20日) {hv:.0f}%")

    # 基本面
    roe = financials.get("roe")
    if roe is not None:
        if roe > 15:
            scores.append(0.5); points.append(f"ROE {roe:.1f}% 优秀")
        elif roe > 8:
            scores.append(0.1)
        elif roe > 0:
            scores.append(-0.2)
        else:
            scores.append(-0.5); points.append(f"ROE {roe:.1f}% 亏损")

    pg = financials.get("profit_growth")
    if pg is not None:
        if pg > 20:
            scores.append(0.5); points.append(f"净利润增长 {pg:.1f}%")
        elif pg > 0:
            scores.append(0.1)
        elif pg > -10:
            scores.append(-0.3)
        else:
            scores.append(-0.5); points.append(f"净利润下滑 {pg:.1f}%")

    pe, pb = financials.get("pe"), financials.get("pb")
    if pe is not None and pe > 0:
        if pe < 10:
            scores.append(0.5); points.append(f"P/E {pe:.1f} 低估")
        elif pe < 20:
            scores.append(0.2); points.append(f"P/E {pe:.1f}")
        elif pe > 35:
            scores.append(-0.4); points.append(f"P/E {pe:.1f} 高估")
    if pb is not None and pb > 0:
        if pb < 1:
            scores.append(0.4); points.append(f"P/B {pb:.1f} 破净")
        elif pb > 5:
            scores.append(-0.2); points.append(f"P/B {pb:.1f}")

    if analyst_forecasts:
        targets = [f["target_price"] for f in analyst_forecasts if f.get("target_price")]
        if targets:
            avg_t = sum(targets) / len(targets)
            upside = (avg_t - current_price) / current_price * 100
            if upside > 20:
                scores.append(0.6); points.append(f"分析师目标价上行 {upside:+.1f}%")
            elif upside > 10:
                scores.append(0.3); points.append(f"分析师目标价上行 {upside:+.1f}%")
            elif upside < -10:
                scores.append(-0.4); points.append(f"分析师目标价下行 {upside:+.1f}%")

    return _make_signal("long", scores, points)
