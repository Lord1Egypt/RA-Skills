#!/usr/bin/env python3
"""
独孤九剑 · 特征计算引擎
将原始K线数据转化为九式规则可用的 19+ 维特征向量

特征清单：
  A. 趋势类: 多周期均线、均线排列、趋势强度和方向
  B. 量能类: 量比、放量倍数、缩量程度、地量标志、量价关系
  C. 波动类: ATR、布林带宽度、振幅、标准差
  D. 位置类: 价格相对均线偏离、布林带%位、近期高低点位置
  E. 周期类: 斐波那契时间窗口标记、变盘日概率
  F. 形态类: 缺口检测、支撑阻力位、RSI、金叉死叉
  G. 资金类: 主力净流入、大单占比（如果有资金流向数据）
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd


# ══════════════════════════════════════════════════════════
# A. 趋势类特征
# ══════════════════════════════════════════════════════════

def compute_moving_averages(df: pd.DataFrame, periods: list = None) -> pd.DataFrame:
    """
    计算多周期均线
    默认: [5, 8, 13, 21, 34, 55, 89] — 斐波那契数列
    """
    if periods is None:
        periods = [5, 8, 13, 21, 34, 55, 89]
    for p in periods:
        df[f"ma{p}"] = df["close"].rolling(p).mean()
    return df


def compute_ma_arrangement(df: pd.DataFrame) -> pd.DataFrame:
    """
    均线排列状态
    - 多头排列: MA5 > MA8 > MA13 > MA21
    - 空头排列: MA5 < MA8 < MA13 > MA21
    - 交叉缠绕: 其他
    返回排列类型和强度（连续天数）
    """
    # 确保均线已计算
    if "ma5" not in df.columns:
        df = compute_moving_averages(df)

    arrangements = []
    for i in range(len(df)):
        row = df.iloc[i]
        if pd.isna(row["ma21"]):
            arrangements.append({"type": "unknown", "strength": 0})
            continue

        short_ma = [row[f"ma{p}"] for p in [5, 8]]
        mid_ma = [row[f"ma{p}"] for p in [13, 21]]

        if all(short_ma[i] > short_ma[i + 1] for i in range(len(short_ma) - 1)) and \
           all(mid_ma[i] > mid_ma[i + 1] for i in range(len(mid_ma) - 1)) and \
           short_ma[-1] > mid_ma[0]:
            arr_type = "bullish"  # 多头排列
        elif all(short_ma[i] < short_ma[i + 1] for i in range(len(short_ma) - 1)) and \
             all(mid_ma[i] < mid_ma[i + 1] for i in range(len(mid_ma) - 1)) and \
             short_ma[-1] < mid_ma[0]:
            arr_type = "bearish"  # 空头排列
        else:
            arr_type = "chaotic"  # 交叉缠绕

        # 统计连续同种排列天数
        if i > 0 and arrangements[i - 1]["type"] == arr_type:
            strength = arrangements[i - 1]["strength"] + 1
        else:
            strength = 1

        arrangements.append({"type": arr_type, "strength": strength})

    df["ma_arrangement"] = [a["type"] for a in arrangements]
    df["ma_arrangement_days"] = [a["strength"] for a in arrangements]
    return df


def compute_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    趋势判定：
    - 上涨趋势: close > MA21 且 MA21 斜率向上
    - 下跌趋势: close < MA21 且 MA21 斜率向下
    - 震荡: 其他
    """
    if "ma21" not in df.columns:
        df = compute_moving_averages(df)

    trends = []
    for i in range(len(df)):
        if i < 5 or pd.isna(df.iloc[i]["ma21"]):
            trends.append({"trend": "unknown", "slope": 0})
            continue

        close = df.iloc[i]["close"]
        ma21 = df.iloc[i]["ma21"]
        ma21_prev = df.iloc[i - 5]["ma21"]

        slope = (ma21 - ma21_prev) / ma21_prev * 100 if ma21_prev > 0 else 0

        if close > ma21 and slope > 0.05:
            trend = "up"
        elif close < ma21 and slope < -0.05:
            trend = "down"
        else:
            trend = "sideways"

        trends.append({"trend": trend, "slope": round(slope, 4)})

    df["trend"] = [t["trend"] for t in trends]
    df["ma21_slope"] = [t["slope"] for t in trends]
    return df


# ══════════════════════════════════════════════════════════
# B. 量能类特征
# ══════════════════════════════════════════════════════════

def compute_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    量能特征：
    - volume_ma5/ma20: 成交量均线
    - volume_ratio: 当日量 / 5日均量（量比）
    - volume_ratio_20: 当日量 / 20日均量
    - volume_percentile_20: 20日内的量能分位数
    - is_surge: 是否放量（1.5倍以上）
    - is_shrink: 是否缩量（50%以下）
    - is_ground: 是否地量（20日分位 < 20%）
    """
    df["volume_ma5"] = df["volume"].rolling(5).mean()
    df["volume_ma20"] = df["volume"].rolling(20).mean()

    df["volume_ratio"] = df["volume"] / df["volume_ma5"]
    df["volume_ratio_20"] = df["volume"] / df["volume_ma20"]

    # 滚动分位数（地量检测）
    df["volume_percentile_20"] = (
        df["volume"].rolling(20).apply(
            lambda x: (x.iloc[-1] <= x).sum() / len(x) * 100, raw=False
        )
    )

    df["is_surge"] = df["volume_ratio"] >= 1.5
    df["is_shrink"] = df["volume_ratio"] <= 0.5
    df["is_ground"] = df["volume_percentile_20"] <= 20

    return df


def compute_price_volume_relation(df: pd.DataFrame) -> pd.DataFrame:
    """
    价量关系：
    - 价涨量增（健康）
    - 价涨量缩（背离/衰竭）
    - 价跌量增（恐慌/出货）
    - 价跌量缩（健康回调/无人接盘）
    """
    relations = []
    for i in range(len(df)):
        if i < 1:
            relations.append("unknown")
            continue

        price_up = df.iloc[i]["close"] > df.iloc[i - 1]["close"]
        vol_up = df.iloc[i]["volume"] > df.iloc[i - 1]["volume"]

        if price_up and vol_up:
            relations.append("price_up_vol_up")       # 价涨量增
        elif price_up and not vol_up:
            relations.append("price_up_vol_down")     # 价涨量缩（背离）
        elif not price_up and vol_up:
            relations.append("price_down_vol_up")     # 价跌量增（恐慌）
        else:
            relations.append("price_down_vol_down")   # 价跌量缩

    df["pv_relation"] = relations
    return df


# ══════════════════════════════════════════════════════════
# C. 波动类特征
# ══════════════════════════════════════════════════════════

def compute_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    波动特征：
    - atr: 平均真实波幅（14周期）
    - amplitude: 日内振幅 %
    - bollinger_upper/middle/lower: 布林带
    - bb_width: 布林带宽度 %
    - bb_position: 价格在布林带中的位置（%B指标）
    """
    # ATR
    df["tr"] = np.maximum(
        df["high"] - df["low"],
        np.maximum(
            abs(df["high"] - df["close"].shift(1)),
            abs(df["low"] - df["close"].shift(1)),
        ),
    )
    df["atr"] = df["tr"].rolling(14).mean()
    df["amplitude"] = (df["high"] - df["low"]) / df["close"].shift(1) * 100

    # Bollinger Bands
    df["bb_middle"] = df["close"].rolling(20).mean()
    bb_std = df["close"].rolling(20).std()
    df["bb_upper"] = df["bb_middle"] + 2 * bb_std
    df["bb_lower"] = df["bb_middle"] - 2 * bb_std
    df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_middle"] * 100
    df["bb_position"] = (df["close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])

    return df


# ══════════════════════════════════════════════════════════
# D. 位置类特征
# ══════════════════════════════════════════════════════════

def compute_position_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    位置特征：
    - n_day_high: N日内最高价
    - n_day_low: N日内最低价
    - position_in_n_day: 当前价在N日区间中的位置（0-1）
    - near_resistance: 是否接近压力位（在5%以内）
    - near_support: 是否接近支撑位（在5%以内）
    """
    for n in [5, 10, 20, 60]:
        df[f"high_{n}d"] = df["high"].rolling(n).max()
        df[f"low_{n}d"] = df["low"].rolling(n).min()
        df[f"pos_{n}d"] = (df["close"] - df[f"low_{n}d"]) / \
                          (df[f"high_{n}d"] - df[f"low_{n}d"])

    # 接近压力/支撑
    df["near_high_20d"] = (df["high_20d"] - df["close"]) / df["close"] * 100 < 3
    df["near_low_20d"] = (df["close"] - df["low_20d"]) / df["close"] * 100 < 3

    return df


# ══════════════════════════════════════════════════════════
# E. 周期类特征
# ══════════════════════════════════════════════════════════

def compute_cycle_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    斐波那契时间周期：
    - 标记距最近重要高低点的天数
    - 判断是否在斐波那契窗口（5/8/13/21/34 天）
    """
    fib_cycles = [3, 5, 8, 13, 21, 34]

    # 寻找最近的重要高点（20日内最高）
    high_points = []
    for i in range(len(df)):
        if i < 2:
            high_points.append(0)
            continue
        # 局部高点
        if df.iloc[i]["high"] >= df.iloc[max(0, i - 2):i + 1]["high"].max():
            high_points.append(i)
        elif i > 0:
            high_points.append(high_points[i - 1])

    # 寻找最近的重要低点（20日内最低）
    low_points = []
    for i in range(len(df)):
        if i < 2:
            low_points.append(0)
            continue
        if df.iloc[i]["low"] <= df.iloc[max(0, i - 2):i + 1]["low"].min():
            low_points.append(i)
        elif i > 0:
            low_points.append(low_points[i - 1])

    df["days_from_high"] = df.index - high_points
    df["days_from_low"] = df.index - low_points

    # 是否在斐波那契窗口
    df["in_fib_window_high"] = df["days_from_high"].apply(
        lambda d: any(abs(d - f) <= 1 for f in fib_cycles) and d > 0
    )
    df["in_fib_window_low"] = df["days_from_low"].apply(
        lambda d: any(abs(d - f) <= 1 for f in fib_cycles) and d > 0
    )
    df["in_fib_window"] = df["in_fib_window_high"] | df["in_fib_window_low"]

    return df


# ══════════════════════════════════════════════════════════
# F. 形态类特征
# ══════════════════════════════════════════════════════════

def compute_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """RSI 指标"""
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))
    return df


def detect_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    缺口检测：
    - gap_up: 向上跳空（今日最低 > 昨日最高）
    - gap_down: 向下跳空（今日最高 < 昨日最低）
    - gap_size: 缺口大小 %
    - gap_filled: 是否已回补
    - gap_age: 距今多少天
    - unfilled_gaps: 所有未回补的缺口列表
    """
    gaps = []

    # 检测所有缺口
    for i in range(1, len(df)):
        prev_high = df.iloc[i - 1]["high"]
        prev_low = df.iloc[i - 1]["low"]
        cur_high = df.iloc[i]["high"]
        cur_low = df.iloc[i]["low"]

        if cur_low > prev_high:
            # 向上跳空缺口
            gap_size = (cur_low - prev_high) / prev_high * 100
            gaps.append({
                "index": i,
                "date": str(df.iloc[i]["date"]),
                "type": "up",
                "size_pct": round(gap_size, 2),
                "gap_top": float(cur_low),
                "gap_bottom": float(prev_high),
                "filled": False,
            })
        elif cur_high < prev_low:
            # 向下跳空缺口
            gap_size = (prev_low - cur_high) / prev_low * 100
            gaps.append({
                "index": i,
                "date": str(df.iloc[i]["date"]),
                "type": "down",
                "size_pct": round(gap_size, 2),
                "gap_top": float(prev_low),
                "gap_bottom": float(cur_high),
                "filled": False,
            })

    # 检查缺口是否回补
    for gap in gaps:
        gap_idx = gap["index"]
        future_data = df.iloc[gap_idx + 1:]
        if len(future_data) == 0:
            continue
        if gap["type"] == "up":
            # 向上缺口：后续有价格跌破缺口顶部即回补
            gap["filled"] = bool((future_data["low"] <= gap["gap_top"]).any())
        else:
            # 向下缺口：后续有价格突破缺口底部即回补
            gap["filled"] = bool((future_data["high"] >= gap["gap_bottom"]).any())

    # 计算最近缺口距今多少天
    if gaps:
        last_idx = len(df) - 1
        for gap in gaps:
            gap["age"] = last_idx - gap["index"]

    df.attrs["gaps"] = gaps
    return df


def compute_support_resistance(df: pd.DataFrame) -> pd.DataFrame:
    """
    支撑/阻力位：
    基于近期高低点、均线、斐波那契回调线

    返回:
    - 最近的重要支撑位（多个，按距离排序）
    - 最近的重要阻力位
    """
    if len(df) < 20:
        return df

    recent = df.iloc[-60:] if len(df) >= 60 else df
    current_price = float(recent.iloc[-1]["close"])

    supports = []
    resistances = []

    # 1. 均线支撑
    for p in [5, 8, 13, 21, 55]:
        ma_val = float(recent.iloc[-1].get(f"ma{p}", 0))
        if ma_val > 0:
            if ma_val < current_price:
                supports.append({"level": round(ma_val, 2), "type": f"MA{p}", "distance_pct": round((current_price - ma_val) / current_price * 100, 2)})
            else:
                resistances.append({"level": round(ma_val, 2), "type": f"MA{p}", "distance_pct": round((ma_val - current_price) / current_price * 100, 2)})

    # 2. 近期高低点
    high_20 = float(recent["high"].tail(20).max())
    low_20 = float(recent["low"].tail(20).min())
    if high_20 > current_price:
        resistances.append({"level": round(high_20, 2), "type": "20日高点", "distance_pct": round((high_20 - current_price) / current_price * 100, 2)})
    if low_20 < current_price:
        supports.append({"level": round(low_20, 2), "type": "20日低点", "distance_pct": round((current_price - low_20) / current_price * 100, 2)})

    # 3. 斐波那契回调线（基于最近一轮大波段）
    recent_high = float(recent["high"].max())
    recent_low = float(recent["low"].min())
    range_diff = recent_high - recent_low

    if range_diff > 0:
        for level in [0.236, 0.382, 0.5, 0.618, 0.786]:
            fib_price = round(recent_low + range_diff * level, 2) if recent_high > recent_low else round(recent_high + range_diff * level, 2)
            label = f"Fib {level}"
            if fib_price < current_price:
                supports.append({"level": fib_price, "type": label, "distance_pct": round((current_price - fib_price) / current_price * 100, 2)})
            elif fib_price > current_price:
                resistances.append({"level": fib_price, "type": label, "distance_pct": round((fib_price - current_price) / current_price * 100, 2)})

    # 排序（支撑从近到远，阻力从近到远）
    supports.sort(key=lambda x: x["level"], reverse=True)
    resistances.sort(key=lambda x: x["level"])

    df.attrs["supports"] = supports[:5]
    df.attrs["resistances"] = resistances[:5]
    return df


# ══════════════════════════════════════════════════════════
# G. 资金类特征（依赖 fetch_fund_flow 数据）
# ══════════════════════════════════════════════════════════

def compute_fund_features(fund_df: Optional[pd.DataFrame]) -> dict:
    """
    资金面特征（如果有资金流向数据）
    """
    if fund_df is None or fund_df.empty:
        return {"has_fund_data": False}

    result = {"has_fund_data": True}

    # 找到主力净流入列
    main_cols = [c for c in fund_df.columns if "主力" in c or "超大单" in c or "大单" in c]
    inflow_cols = [c for c in fund_df.columns if "净流入" in c or "净额" in c]

    try:
        recent = fund_df.tail(5)
        # 连续净流入天数
        if inflow_cols:
            col = inflow_cols[0]
            values = fund_df[col].values
            consecutive = 0
            for v in reversed(values):
                if float(v) > 0:
                    consecutive += 1
                else:
                    break
            result["consecutive_inflow_days"] = consecutive

        # 近5日累计
        if inflow_cols:
            result["recent_5d_net_flow"] = round(float(recent[inflow_cols[0]].sum()), 2)
    except Exception:
        pass

    return result


# ══════════════════════════════════════════════════════════
# 一站式特征计算
# ══════════════════════════════════════════════════════════

def compute_all_features(
    daily_df: pd.DataFrame,
    fund_df: Optional[pd.DataFrame] = None,
    minute_df: Optional[pd.DataFrame] = None,
) -> dict:
    """
    一站式计算全部特征

    Args:
        daily_df: 日K线 DataFrame（来自 fetch_data.fetch_daily_kline）
        fund_df: 资金流向 DataFrame（可选）
        minute_df: 分钟K线 DataFrame（可选）

    Returns:
        {
            "success": True,
            "data": DataFrame（所有特征列已附加），
            "summary": { 最新一日的特征摘要 },
            "supports": [...],
            "resistances": [...],
            "gaps": [...],
            "fund_features": {...},
            "minute_features": {...}
        }
    """
    # 空数据保护
    if daily_df is None or daily_df.empty:
        return {
            "success": True,
            "data": pd.DataFrame(),
            "summary": {},
            "supports": [],
            "resistances": [],
            "gaps": [],
            "fund_features": {"has_fund_data": False},
            "minute_features": {},
        }

    df = daily_df.copy()

    # A. 趋势类
    df = compute_moving_averages(df)
    df = compute_ma_arrangement(df)
    df = compute_trend(df)

    # B. 量能类
    df = compute_volume_features(df)
    df = compute_price_volume_relation(df)

    # C. 波动类
    df = compute_volatility_features(df)

    # D. 位置类
    df = compute_position_features(df)

    # E. 周期类
    df = compute_cycle_features(df)

    # F. 形态类
    df = compute_rsi(df)
    df = detect_gaps(df)
    df = compute_support_resistance(df)

    # G. 资金类
    fund_features = compute_fund_features(fund_df)

    # 分钟线特征（如果有）
    minute_features = {}
    if minute_df is not None and not minute_df.empty:
        minute_features = {
            "has_minute_data": True,
            "latest_price": float(minute_df.iloc[-1]["close"]),
            "intraday_high": float(minute_df["high"].max()),
            "intraday_low": float(minute_df["low"].min()),
            "intraday_vwap": float((minute_df["close"] * minute_df["volume"]).sum() / minute_df["volume"].sum()) if "volume" in minute_df.columns else 0,
        }

    # 提取最新一日的特征摘要
    latest = df.iloc[-1]
    summary = {
        "date": str(latest["date"]),
        "close": float(latest["close"]),
        "open": float(latest["open"]),
        "high": float(latest["high"]),
        "low": float(latest["low"]),
        "volume": float(latest["volume"]),
        "pct_change": float(latest.get("pct_change", 0)),
        "turnover": float(latest.get("turnover", 0)),
        "amplitude": float(latest.get("amplitude", 0)),

        # 趋势
        "trend": latest.get("trend", "unknown"),
        "ma_arrangement": latest.get("ma_arrangement", "unknown"),
        "ma_arrangement_days": int(latest.get("ma_arrangement_days", 0)),
        "ma5": float(latest.get("ma5", 0)),
        "ma8": float(latest.get("ma8", 0)),
        "ma13": float(latest.get("ma13", 0)),
        "ma21": float(latest.get("ma21", 0)),
        "ma55": float(latest.get("ma55", 0)),

        # 量能
        "volume_ratio": round(float(latest.get("volume_ratio", 1)), 2),
        "is_surge": bool(latest.get("is_surge", False)),
        "is_shrink": bool(latest.get("is_shrink", False)),
        "is_ground": bool(latest.get("is_ground", False)),
        "pv_relation": latest.get("pv_relation", "unknown"),

        # 波动
        "atr": round(float(latest.get("atr", 0)), 2),
        "bb_upper": float(latest.get("bb_upper", 0)),
        "bb_lower": float(latest.get("bb_lower", 0)),
        "bb_position": round(float(latest.get("bb_position", 0.5)), 3),
        "bb_width": round(float(latest.get("bb_width", 0)), 2),

        # 位置
        "pos_20d": round(float(latest.get("pos_20d", 0.5)), 3),
        "near_high_20d": bool(latest.get("near_high_20d", False)),
        "near_low_20d": bool(latest.get("near_low_20d", False)),

        # RSI
        "rsi": round(float(latest.get("rsi", 50)), 1),

        # 周期
        "days_from_high": int(latest.get("days_from_high", 0)),
        "days_from_low": int(latest.get("days_from_low", 0)),
        "in_fib_window": bool(latest.get("in_fib_window", False)),
    }

    return {
        "success": True,
        "data": df,
        "summary": summary,
        "supports": df.attrs.get("supports", []),
        "resistances": df.attrs.get("resistances", []),
        "gaps": df.attrs.get("gaps", []),
        "fund_features": fund_features,
        "minute_features": minute_features,
    }


# ── CLI 入口 ────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python compute_features.py <股票代码> [--json]")
        sys.exit(1)

    code = sys.argv[1]
    as_json = "--json" in sys.argv

    from fetch_data import fetch_all
    raw = fetch_all(code, days=120)

    if not raw["success"]:
        print(f"❌ 数据获取失败: {raw.get('errors', '未知错误')}")
        sys.exit(1)

    result = compute_all_features(
        raw["daily_kline"],
        raw.get("fund_flow"),
        raw.get("minute_60"),
    )

    if as_json:
        output = {
            "code": code,
            "name": raw["name"],
            "fetched_at": raw["fetched_at"],
            "summary": result["summary"],
            "supports": result["supports"],
            "resistances": result["resistances"],
            "gaps": result["gaps"],
            "fund_features": result["fund_features"],
            "minute_features": result["minute_features"],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"\n{'='*60}")
        print(f"  ⚔️ 独孤九剑 · 特征分析  |  {raw['name']}({code})")
        print(f"{'='*60}\n")

        s = result["summary"]
        print("📈 趋势与位置")
        print(f"  趋势: {s['trend']} | 均线排列: {s['ma_arrangement']}({s['ma_arrangement_days']}天)")
        print(f"  MA5/8/13/21/55: {s['ma5']:.2f}/{s['ma8']:.2f}/{s['ma13']:.2f}/{s['ma21']:.2f}/{s['ma55']:.2f}")
        print(f"  20日区间位置: {s['pos_20d']*100:.0f}% | RSI: {s['rsi']:.1f}")

        print(f"\n📊 量能与波动")
        print(f"  量比(5日): {s['volume_ratio']:.2f} | 放量: {s['is_surge']} | 缩量: {s['is_shrink']} | 地量: {s['is_ground']}")
        print(f"  价量关系: {s['pv_relation']}")
        print(f"  ATR: {s['atr']:.2f} | 布林带位置: {s['bb_position']:.2%}")

        print(f"\n🕐 周期与缺口")
        print(f"  距高点: {s['days_from_high']}天 | 距低点: {s['days_from_low']}天 | 斐波窗口: {s['in_fib_window']}")

        if result["gaps"]:
            unfilled = [g for g in result["gaps"] if not g["filled"]]
            print(f"  缺口总数: {len(result['gaps'])} | 未回补: {len(unfilled)}")
            for g in unfilled[:3]:
                print(f"    {g['date']} {g['type']}缺口 {g['size_pct']}% (已{g['age']}天)")

        if result["supports"]:
            print(f"\n🛡️ 支撑位:")
            for s in result["supports"][:3]:
                print(f"  {s['level']:.2f} ({s['type']}) 距现价 {s['distance_pct']}%")

        if result["resistances"]:
            print(f"⚔️ 阻力位:")
            for r in result["resistances"][:3]:
                print(f"  {r['level']:.2f} ({r['type']}) 距现价 {r['distance_pct']}%")

        if result["fund_features"].get("has_fund_data"):
            f = result["fund_features"]
            print(f"\n💰 资金面")
            print(f"  连续净流入: {f.get('consecutive_inflow_days', '?')}天")
            print(f"  近5日净流入: {f.get('recent_5d_net_flow', '?')}")
