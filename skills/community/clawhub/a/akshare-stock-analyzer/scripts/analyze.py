#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""策略分析脚本

- 依赖 fetchData.py 提供的原始数据 + 技术指标
- 按 分析.txt（优化版）中的规则，给出趋势、动能、RSI、交易信号和打分

分析结果字段含义（AnalysisResult）：

- ts_code: 股票代码或名称
- trend: 趋势方向
    - "bullish"  多头趋势（近期整体上涨）
    - "bearish"  空头趋势（近期整体下跌）
    - "sideways" 震荡趋势（涨跌幅不大、没有明显方向）
- macd_cross: MACD 金叉/死叉状态（当前版本仅作参考）
    - "golden"  最近出现金叉
    - "death"   最近出现死叉
    - "none"    最近无明显金叉/死叉
- macd_strength: MACD 强弱（仅作参考）
    - "strong"  DIF 和 DEA 均在 0 轴上方
    - "weak"    DIF 和 DEA 均在 0 轴下方
    - "neutral" 一上一下或接近 0 轴
- macd_momentum: MACD 柱动量变化（仅作参考）
    - "increasing"  最新一根 MACD 柱绝对值大于前一根，动能增强
    - "decreasing"  最新一根 MACD 柱绝对值小于前一根，动能减弱
- weekly_change_pct: 最近一周（约 5 个交易日）收盘价涨跌幅，单位为百分比
    - 计算方式：最新收盘价 / 5 个交易日前收盘价 - 1，再乘以 100
- today_change_pct: 今日相对上一交易日收盘价的涨跌幅，单位为百分比
    - 计算方式：最新收盘价 / 昨日收盘价 - 1，再乘以 100
- rsi: 当前 RSI14 数值（仅作参考）
- rsi_zone: RSI 所在区间（强/弱/中性，仅作参考）
    - "strong"  RSI >= 55
    - "weak"    RSI <= 45
    - "neutral" 45 < RSI < 55
- rsi_signal: RSI 信号（超买/超卖/正常，仅作参考）
    - "overbought" RSI >= 70，超买
    - "oversold"   RSI <= 30，超卖
    - "normal"     介于其间
- rsi_trend: RSI 方向（仅作参考）
    - "up"   RSI 相比前一日上升
    - "down" RSI 相比前一日下降
    - "flat" 基本持平
- signal: 交易信号
    - "buy"  短期状态较好，可以考虑买入或重点关注
    - "sell" 短期状态较差，可以考虑卖出或回避
    - "hold" 观望/持有，不建议新增仓位
- score: 评分（0~10），综合一周趋势和当天动量
    - 分数越高，短期状态越强；越低则越弱
    - 粗略可以理解为：0~2 很弱，3~5 一般，6~8 偏强，9~10 很强
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, asdict
from typing import Literal, List, Dict, Any

import pandas as pd

# 确保可以导入同目录的模块
PLAYGROUND_DIR = os.path.dirname(os.path.abspath(__file__))
if PLAYGROUND_DIR not in sys.path:
    sys.path.insert(0, PLAYGROUND_DIR)

from fetch import fetch_with_indicators  # type: ignore
from today import get_today_quote  # type: ignore


TrendType = Literal["bullish", "bearish", "sideways"]
MacdCrossType = Literal["golden", "death", "none"]
MacdStrengthType = Literal["strong", "weak", "neutral"]
MacdMomentumType = Literal["increasing", "decreasing"]
RsiZoneType = Literal["strong", "weak", "neutral"]
RsiSignalType = Literal["overbought", "oversold", "normal"]
RsiTrendType = Literal["up", "down", "flat"]
SignalType = Literal["buy", "sell", "hold"]
ReversalHintType = Literal["top_warning", "bottom_warning", "none"]
RiskLevelType = Literal["high_overbought", "high_oversold", "trend_overextended", "normal"]


@dataclass
class AnalysisResult:
    ts_code: str
    trend: TrendType
    macd_cross: MacdCrossType
    macd_strength: MacdStrengthType
    macd_momentum: MacdMomentumType
    weekly_change_pct: float
    today_change_pct: float
    rsi: float
    rsi_zone: RsiZoneType
    rsi_signal: RsiSignalType
    rsi_trend: RsiTrendType
    signal: SignalType
    score: int
    ma_pattern: str
    ma_bias: str
    ma_values: Dict[str, float]
    ma_spread: float
    trend_strength: float
    reversal_hint: ReversalHintType
    risk_level: RiskLevelType


def _calc_trend(df: pd.DataFrame) -> TrendType:
    """基于均线结构判断趋势。

    规则：
    - MA7 > MA14 > MA20 > MA60 且 收盘 > MA20 -> bullish
    - MA7 < MA14 < MA20 < MA60             -> bearish
    - 其余                                   -> sideways
    """

    if df is None or df.empty:
        return "sideways"

    cur = df.iloc[-1]
    ma7 = cur.get("MA7")
    ma14 = cur.get("MA14")
    ma20 = cur.get("MA20")
    ma60 = cur.get("MA60")
    close = cur.get("收盘")

    required = [ma7, ma14, ma20, ma60, close]
    if any(pd.isna(x) for x in required):
        return "sideways"

    if ma7 > ma14 > ma20 > ma60 and close > ma20:
        return "bullish"
    if ma7 < ma14 < ma20 < ma60:
        return "bearish"
    return "sideways"


def _calc_macd_state(df: pd.DataFrame) -> tuple[MacdCrossType, MacdStrengthType, MacdMomentumType]:
    if len(df) < 2:
        return "none", "neutral", "decreasing"

    prev = df.iloc[-2]
    cur = df.iloc[-1]

    prev_dif = prev.get("DIF")
    prev_dea = prev.get("DEA")
    cur_dif = cur.get("DIF")
    cur_dea = cur.get("DEA")
    prev_macd = float(prev.get("MACD")) if not pd.isna(prev.get("MACD")) else 0.0
    cur_macd = float(cur.get("MACD")) if not pd.isna(cur.get("MACD")) else 0.0

    # 金叉 / 死叉
    cross: MacdCrossType = "none"
    if prev_dif is not None and cur_dif is not None and prev_dea is not None and cur_dea is not None:
        if prev_dif <= prev_dea and cur_dif > cur_dea:
            cross = "golden"
        elif prev_dif >= prev_dea and cur_dif < cur_dea:
            cross = "death"

    # 强弱（基于 0 轴位置）
    strength: MacdStrengthType = "neutral"
    if cur_dif is not None and cur_dea is not None:
        if cur_dif > 0 and cur_dea > 0:
            strength = "strong"
        elif cur_dif < 0 and cur_dea < 0:
            strength = "weak"

    # 动量（柱子绝对值放大/缩小）
    momentum: MacdMomentumType = "increasing" if abs(cur_macd) >= abs(prev_macd) else "decreasing"

    return cross, strength, momentum


def _calc_rsi_state(df: pd.DataFrame) -> tuple[float, RsiZoneType, RsiSignalType, RsiTrendType]:
    if len(df) < 2 or "RSI14" not in df.columns:
        return float("nan"), "neutral", "normal", "flat"

    prev_rsi = float(df.iloc[-2]["RSI14"])
    cur_rsi = float(df.iloc[-1]["RSI14"])

    # 区间
    if cur_rsi >= 55:
        zone: RsiZoneType = "strong"
    elif cur_rsi <= 45:
        zone = "weak"
    else:
        zone = "neutral"

    # 信号
    if cur_rsi >= 70:
        signal: RsiSignalType = "overbought"
    elif cur_rsi <= 30:
        signal = "oversold"
    else:
        signal = "normal"

    # 趋势
    if cur_rsi > prev_rsi:
        trend: RsiTrendType = "up"
    elif cur_rsi < prev_rsi:
        trend = "down"
    else:
        trend = "flat"

    return cur_rsi, zone, signal, trend


def _describe_ma_structure(df: pd.DataFrame) -> Dict[str, Any]:
    """返回均线结构解释层，便于直接阅读趋势结构。"""

    if df is None or df.empty:
        return {"ma_values": {}, "ma_pattern": "unknown", "ma_bias": "neutral", "ma_spread": float("nan")}

    cur = df.iloc[-1]
    ma7 = float(pd.to_numeric(cur.get("MA7"), errors="coerce"))
    ma14 = float(pd.to_numeric(cur.get("MA14"), errors="coerce"))
    ma20 = float(pd.to_numeric(cur.get("MA20"), errors="coerce"))
    ma60 = float(pd.to_numeric(cur.get("MA60"), errors="coerce"))
    close = float(pd.to_numeric(cur.get("收盘"), errors="coerce"))

    if any(pd.isna(x) for x in [ma7, ma14, ma20, ma60, close]):
        return {"ma_values": {}, "ma_pattern": "invalid", "ma_bias": "neutral", "ma_spread": float("nan")}

    if ma7 > ma14 > ma20 > ma60:
        pattern = "bullish_alignment"
    elif ma7 < ma14 < ma20 < ma60:
        pattern = "bearish_alignment"
    else:
        pattern = "mixed"

    bias = "above_ma20" if close >= ma20 else "below_ma20"

    # 均线“发散程度”（趋势强度）：ma7 相对 ma60 的偏离度
    ma_spread = float("nan")
    if ma60 != 0 and not pd.isna(ma60):
        ma_spread = (ma7 - ma60) / ma60

    return {
        "ma_values": {
            "MA7": ma7,
            "MA14": ma14,
            "MA20": ma20,
            "MA60": ma60,
            "close": close,
        },
        "ma_pattern": pattern,
        "ma_bias": bias,
        "ma_spread": ma_spread,
    }


def _calc_trend_strength(ma_values: Dict[str, float]) -> float:
    """基于 MA7/MA20/MA60 计算趋势强度，返回值限制在 [-1, 1]。

    建议公式：
      trend_strength = (MA7 - MA20) / MA20 + (MA20 - MA60) / MA60
    """

    ma7 = float(pd.to_numeric(ma_values.get("MA7", float("nan")), errors="coerce"))
    ma20 = float(pd.to_numeric(ma_values.get("MA20", float("nan")), errors="coerce"))
    ma60 = float(pd.to_numeric(ma_values.get("MA60", float("nan")), errors="coerce"))

    if any(pd.isna(x) for x in [ma7, ma20, ma60]) or ma20 == 0 or ma60 == 0:
        return float("nan")

    strength = (ma7 - ma20) / ma20 + (ma20 - ma60) / ma60
    if pd.isna(strength):
        return float("nan")

    # 限制在 [-1, 1] 区间
    return float(max(-1.0, min(1.0, strength)))


def _calc_reversal_hint(trend: TrendType, macd_momentum: MacdMomentumType) -> ReversalHintType:
    """基于趋势 + MACD 动量给出简单的转折预警。"""

    if trend == "bullish" and macd_momentum == "decreasing":
        return "top_warning"
    if trend == "bearish" and macd_momentum == "increasing":
        return "bottom_warning"
    return "none"


def _calc_risk_level(rsi: float, ma_spread: float) -> RiskLevelType:
    """结合 RSI 与均线发散程度给出当前风险等级。"""

    if not pd.isna(rsi):
        if rsi >= 75:
            return "high_overbought"
        if rsi <= 25:
            return "high_oversold"

    if not pd.isna(ma_spread) and abs(ma_spread) > 0.1:
        return "trend_overextended"

    return "normal"


def _calc_signal(
    trend: TrendType,
    macd_cross: MacdCrossType,
    macd_strength: MacdStrengthType,
    rsi_zone: RsiZoneType,
    rsi_trend: RsiTrendType,
    close: float,
    ma20: float,
) -> SignalType:
    if pd.isna(close) or pd.isna(ma20):
        return "hold"

    if (
        trend == "bullish"
        and macd_cross == "golden"
        and macd_strength == "strong"
        and rsi_zone == "strong"
        and rsi_trend == "up"
        and close >= ma20
    ):
        return "buy"

    if (
        macd_cross == "death"
        or (rsi_zone == "strong" and rsi_trend == "down")
        or close < ma20
    ):
        return "sell"

    return "hold"


def _calc_score(
    trend: TrendType,
    macd_cross: MacdCrossType,
    macd_strength: MacdStrengthType,
    rsi_zone: RsiZoneType,
    rsi_trend: RsiTrendType,
    close: float,
    ma20: float,
) -> int:
    score = 0

    if trend == "bullish":
        score += 3
    elif trend == "sideways":
        score += 1

    if macd_cross == "golden":
        score += 2
    elif macd_cross == "none":
        score += 1

    if macd_strength == "strong":
        score += 2
    elif macd_strength == "neutral":
        score += 1

    if rsi_zone == "strong":
        score += 1
    if rsi_trend == "up":
        score += 1

    if not pd.isna(close) and not pd.isna(ma20) and close >= ma20:
        score += 1

    return min(score, 10)


def _append_intraday_bar_if_needed(ts_code: str, df: pd.DataFrame) -> pd.DataFrame:
    """如有需要，将 today.py 的盘中快照拼接为一根“今日 K 线”。

    - 若 today.py 获取失败，或今日日期已在日线中，则原样返回；
    - 若 today.py 给出的日期晚于当前 df 最后一行日期，则在尾部追加一行，
      使用盘中最新价/最高/最低/成交量作为今日 K 线，并重算 MACD/RSI。
    """

    if df is None or df.empty or "日期" not in df.columns or "收盘" not in df.columns:
        return df

    try:
        quote = get_today_quote(ts_code)
    except Exception:  # noqa: BLE001
        # 实时接口不可用时，不影响原有日线分析
        return df

    today_str = str(quote.get("date"))
    today_dt = pd.to_datetime(today_str, errors="coerce")
    if pd.isna(today_dt):
        return df

    # 当前日线中最后一个交易日
    last_dt = pd.to_datetime(df["日期"], errors="coerce").max()
    if not pd.isna(last_dt) and today_dt.date() <= last_dt.date():
        # 已包含今天或 today 早于最后一根 K，直接返回
        return df

    last_row = df.iloc[-1].copy()

    # 构造一根“盘中 K 线”：
    # - 日期：today
    # - 收盘：使用盘中最新价
    # - 最高/最低/成交量：使用盘中对应字段
    # - 其他字段先沿用上一日或保持不变，之后会重算 MACD/RSI
    price = float(quote.get("price"))
    high = float(quote.get("high")) if quote.get("high") is not None else price
    low = float(quote.get("low")) if quote.get("low") is not None else price
    volume = float(quote.get("volume")) if quote.get("volume") is not None else last_row.get("成交量", 0.0)

    last_row["日期"] = today_dt.date()
    if "开盘" in last_row.index and pd.isna(last_row.get("开盘")):
        last_row["开盘"] = price
    last_row["收盘"] = price
    if "最高" in last_row.index:
        last_row["最高"] = high
    if "最低" in last_row.index:
        last_row["最低"] = low
    if "成交量" in last_row.index:
        last_row["成交量"] = volume

    # 先把新行追加到尾部
    df_ext = pd.concat([df, last_row.to_frame().T], ignore_index=True)

    # 追加盘中 K 线后，重算 MA / MACD / RSI
    closes = pd.to_numeric(df_ext["收盘"], errors="coerce")
    # MA
    df_ext["MA7"] = closes.rolling(window=7, min_periods=7).mean()
    df_ext["MA14"] = closes.rolling(window=14, min_periods=14).mean()
    df_ext["MA20"] = closes.rolling(window=20, min_periods=20).mean()
    df_ext["MA60"] = closes.rolling(window=60, min_periods=60).mean()

    # MACD(12,26,9)
    ema_fast = closes.ewm(span=12, adjust=False).mean()
    ema_slow = closes.ewm(span=26, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=9, adjust=False).mean()
    macd = dif - dea
    df_ext["DIF"] = dif
    df_ext["DEA"] = dea
    df_ext["MACD"] = macd

    # RSI(14)
    delta = closes.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df_ext["RSI14"] = rsi

    return df_ext


def analyze_single(ts_code: str, df: pd.DataFrame) -> AnalysisResult:
    """对单只股票（已包含指标的 DataFrame）做分析。

    df 需至少包含：日期/收盘/MA7/MA20/MA60/DIF/DEA/MACD/RSI14
    """

    df = df.copy().sort_values("日期").reset_index(drop=True)
    # 如有需要，将 today.py 的盘中快照拼到日线末尾，模拟“如果现在就收盘”的状态
    df = _append_intraday_bar_if_needed(ts_code, df)

    # 计算最近一周（约 5 个交易日）及今日涨跌幅（百分比）
    weekly_change_pct = float("nan")
    today_change_pct = float("nan")
    if "收盘" in df.columns:
        closes = pd.to_numeric(df["收盘"], errors="coerce")
        if len(closes) >= 2 and closes.iloc[-2] != 0:
            today_change_pct = (closes.iloc[-1] / closes.iloc[-2] - 1.0) * 100.0
        if len(closes) >= 6 and closes.iloc[-6] != 0:
            weekly_change_pct = (closes.iloc[-1] / closes.iloc[-6] - 1.0) * 100.0

    trend = _calc_trend(df)
    macd_cross, macd_strength, macd_momentum = _calc_macd_state(df)
    rsi, rsi_zone, rsi_signal, rsi_trend = _calc_rsi_state(df)
    ma_info = _describe_ma_structure(df)
    cur_close = float(pd.to_numeric(df.iloc[-1].get("收盘"), errors="coerce")) if not df.empty else float("nan")
    cur_ma20 = float(pd.to_numeric(df.iloc[-1].get("MA20"), errors="coerce")) if not df.empty else float("nan")
    ma_spread_val = float(ma_info.get("ma_spread", float("nan")))
    trend_strength = _calc_trend_strength(ma_info.get("ma_values", {}))
    reversal_hint = _calc_reversal_hint(trend, macd_momentum)
    risk_level = _calc_risk_level(rsi, ma_spread_val)
    signal = _calc_signal(
        trend=trend,
        macd_cross=macd_cross,
        macd_strength=macd_strength,
        rsi_zone=rsi_zone,
        rsi_trend=rsi_trend,
        close=cur_close,
        ma20=cur_ma20,
    )
    score = _calc_score(
        trend=trend,
        macd_cross=macd_cross,
        macd_strength=macd_strength,
        rsi_zone=rsi_zone,
        rsi_trend=rsi_trend,
        close=cur_close,
        ma20=cur_ma20,
    )

    return AnalysisResult(
        ts_code=ts_code,
        trend=trend,
        macd_cross=macd_cross,
        macd_strength=macd_strength,
        macd_momentum=macd_momentum,
        weekly_change_pct=weekly_change_pct,
        today_change_pct=today_change_pct,
        rsi=rsi,
        rsi_zone=rsi_zone,
        rsi_signal=rsi_signal,
        rsi_trend=rsi_trend,
        signal=signal,
        score=score,
        ma_pattern=str(ma_info["ma_pattern"]),
        ma_bias=str(ma_info["ma_bias"]),
        ma_values=ma_info["ma_values"],
        ma_spread=ma_spread_val,
        trend_strength=trend_strength,
        reversal_hint=reversal_hint,
        risk_level=risk_level,
    )


def analyze_many(data: Dict[str, pd.DataFrame]) -> List[AnalysisResult]:
    """对多只股票进行分析。

    参数 data: {ts_code: df_with_indicators}
    """

    results: List[AnalysisResult] = []
    for ts_code, df in data.items():
        if df is not None and not df.empty:
            results.append(analyze_single(ts_code, df))
    return results


def summarize(results: List[AnalysisResult]) -> Dict[str, Any]:
    """按规则返回：所有买入信号 + Top 10。"""

    # 按 score 降序
    sorted_results = sorted(results, key=lambda r: r.score, reverse=True)

    buys = [asdict(r) for r in sorted_results if r.signal == "buy"]
    top10 = [asdict(r) for r in sorted_results[:10]]

    return {"buy_list": buys, "top10": top10}


def main() -> None:
    """命令行示例：先拉数据再分析单只股票。

    示例：
      python strategy_analyzer.py 招商银行 --days 120
      python strategy_analyzer.py 600036 --start 20250101 --end 20250320 --prefer tx
    """

    import argparse

    parser = argparse.ArgumentParser(description="单股票策略分析")
    parser.add_argument("symbol", help="股票代码或名称，例如 600036 / 招商银行 / sz159339")
    parser.add_argument("--start", help="开始日期，YYYYMMDD 或 YYYY-MM-DD")
    parser.add_argument("--end", help="结束日期，YYYYMMDD 或 YYYY-MM-DD")
    parser.add_argument(
        "--days",
        type=int,
        default=120,
        help="若未提供 start/end，则向前回溯的天数，默认 120 天",
    )
    parser.add_argument(
        "--prefer",
        choices=["sina", "tx"],
        default="sina",
        help="优先数据源，默认新浪",
    )
    parser.add_argument(
        "--adjust",
        choices=["", "qfq", "hfq"],
        default="",
        help="复权方式，默认不复权",
    )

    args = parser.parse_args()

    if args.start and args.end:
        start_str = args.start
        end_str = args.end
    else:
        end_dt = pd.Timestamp.utcnow().tz_localize(None)
        start_dt = end_dt - pd.Timedelta(days=args.days)
        start_str = start_dt.strftime("%Y-%m-%d")
        end_str = end_dt.strftime("%Y-%m-%d")

    df = fetch_with_indicators(
        symbol_or_name=args.symbol,
        start_date=start_str,
        end_date=end_str,
        adjust=args.adjust,
        prefer=args.prefer,
    )

    res = analyze_single(ts_code=args.symbol, df=df)

    print("分析结果：")
    print(asdict(res))


if __name__ == "__main__":
    main()
