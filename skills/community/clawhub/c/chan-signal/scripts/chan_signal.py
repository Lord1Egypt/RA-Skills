#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ChanSignal - 缠论买卖点分析脚本
自包含的缠论引擎，通过 pytdx 获取 K 线数据，输出 JSON 格式的买卖点分析结果。

用法:
    python chan_signal.py 000001              # 默认日线分析
    python chan_signal.py 000001 --period 6   # 60分钟线
    python chan_signal.py 000001 --period 9 --count 500
    python chan_signal.py 000001 --recent 5   # 只输出最近5根K线内的信号

输出: JSON 格式，包含股票信息、缠论结构、买卖点信号、分析建议
"""
import argparse
import json
import os
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# ═══════════════════════════════════════════════════════════════════
#  配置
# ═══════════════════════════════════════════════════════════════════

MIN_BI_LENGTH = 4
ZHONGSHU_TOLERANCE = 0.01
KLINE_COUNT = 500

PERIOD_MAP = {9: "日线", 7: "周线", 5: "30分钟", 6: "60分钟"}

DEFAULT_SERVERS = [
    ("119.6.200.40", 7709),
    ("182.140.139.191", 7709),
    ("218.200.222.134", 7709),
    ("182.150.28.166", 7709),
    ("119.147.212.81", 7709),
    ("112.74.142.218", 7709),
]

CACHE_DIR = os.path.join(tempfile.gettempdir(), "chansignal_cache")

SH_A_STOCK_PREFIXES = ("600", "601", "603", "605", "688", "689")
SZ_A_STOCK_PREFIXES = (
    "000", "001", "002", "003", "300", "301",
    "430", "831", "832", "833", "834", "835", "836", "837", "838",
    "839", "870", "871", "872", "873", "874", "875", "876", "877",
    "878", "879", "920",
)

LEVEL_NAMES = {1: "一", 2: "二", 3: "三"}
TYPE_NAMES = {"buy": "买", "sell": "卖"}


# ═══════════════════════════════════════════════════════════════════
#  数据获取
# ═══════════════════════════════════════════════════════════════════

def _normalize_code(code: str) -> str:
    return str(code).strip().zfill(6)


def _code_to_market(code: str) -> Tuple[str, int]:
    """返回 (完整代码, 市场代码: 0=深圳, 1=上海)"""
    code = code.strip()
    if code.startswith(("6", "9")):
        return code, 1
    elif code.startswith(("0", "3")):
        return code, 0
    elif code.startswith(("4", "8")):
        return code, 0
    else:
        return code, 1


def fetch_kline(code: str, category: int = 9, count: int = KLINE_COUNT) -> pd.DataFrame:
    """通过 pytdx 获取 K 线数据

    返回 DataFrame: date, open, close, high, low, vol, amount
    """
    from pytdx.hq import TdxHq_API

    code = _normalize_code(code)
    full_code, market = _code_to_market(code)

    # 尝试缓存
    cache_path = os.path.join(CACHE_DIR, str(category), f"{code}.csv")
    disk_cached = pd.DataFrame()
    if os.path.isfile(cache_path):
        try:
            disk_cached = pd.read_csv(cache_path, encoding="utf-8-sig")
            if "date" in disk_cached.columns:
                disk_cached["date"] = pd.to_datetime(disk_cached["date"], errors="coerce")
                disk_cached = disk_cached.dropna(subset=["date"])
            for c in ("open", "close", "high", "low", "vol", "amount"):
                if c in disk_cached.columns:
                    disk_cached[c] = pd.to_numeric(disk_cached[c], errors="coerce").fillna(0)
            disk_cached = disk_cached.sort_values("date").reset_index(drop=True)
            if len(disk_cached) >= count:
                return disk_cached.iloc[-count:].copy()
        except Exception:
            pass

    # 连接服务器
    api = TdxHq_API()
    connected = False
    for ip, port in DEFAULT_SERVERS:
        try:
            result = api.connect(ip, port, time_out=5)
            if not result:
                continue
            # 验证连接
            test_bars = api.get_security_bars(9, 0, "000001", 0, 1)
            if test_bars is not None:
                connected = True
                break
            api.disconnect()
        except Exception:
            try:
                api.disconnect()
            except Exception:
                pass
            continue

    if not connected:
        if not disk_cached.empty:
            return disk_cached.iloc[-count:].copy()
        raise ConnectionError("无法连接到通达信服务器，请检查网络连接")

    try:
        bars = api.get_security_bars(category, market, full_code, 0, count)
    except Exception as e:
        if not disk_cached.empty:
            return disk_cached.iloc[-count:].copy()
        raise RuntimeError(f"获取 K 线失败: {e}")
    finally:
        try:
            api.disconnect()
        except Exception:
            pass

    if bars is None or len(bars) == 0:
        if not disk_cached.empty:
            return disk_cached.iloc[-count:].copy()
        return pd.DataFrame(columns=["date", "open", "close", "high", "low", "vol", "amount"])

    df = pd.DataFrame(bars)
    if "datetime" in df.columns:
        df["date"] = pd.to_datetime(df["datetime"])
    elif "year" in df.columns:
        df["date"] = pd.to_datetime(
            df[["year", "month", "day"]].astype(str).agg("-".join, axis=1)
        )

    for c in ("open", "close", "high", "low", "vol", "amount"):
        if c not in df.columns:
            df[c] = 0.0

    df = df[["date", "open", "close", "high", "low", "vol", "amount"]].copy()
    df.sort_values("date", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 合并缓存
    if not disk_cached.empty:
        df = pd.concat([disk_cached, df], ignore_index=True)
        df = df.drop_duplicates(subset=["date"], keep="last")
        df = df.sort_values("date").reset_index(drop=True)

    # 保存缓存
    try:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        df.to_csv(cache_path, index=False, encoding="utf-8-sig")
    except Exception:
        pass

    return df.iloc[-count:].copy()


# ═══════════════════════════════════════════════════════════════════
#  缠论引擎 - 1. K线包含处理
# ═══════════════════════════════════════════════════════════════════

def _is_contain(h1, l1, h2, l2) -> bool:
    return (h1 >= h2 and l1 <= l2) or (h2 >= h1 and l2 <= l1)


def process_inclusion(klines: pd.DataFrame) -> pd.DataFrame:
    """K线包含处理: 上升取高高, 下降取低低"""
    if klines is None or len(klines) < 3:
        return klines.copy() if klines is not None else pd.DataFrame()

    df = klines.copy().reset_index(drop=True)
    df["_raw_index"] = df.index
    df["raw_start_index"] = df["_raw_index"]
    df["raw_end_index"] = df["_raw_index"]
    df["high_raw_index"] = df["_raw_index"]
    df["low_raw_index"] = df["_raw_index"]
    df["high_date"] = df["date"]
    df["low_date"] = df["date"]
    df["_up"] = df["close"] >= df["open"]

    result = []
    i = 0
    n = len(df)

    while i < n:
        if i == 0:
            result.append(df.iloc[i].to_dict())
            i += 1
            continue

        current = df.iloc[i]
        prev_s_idx = len(result) - 1
        prev = result[prev_s_idx]

        if _is_contain(prev["high"], prev["low"], current["high"], current["low"]):
            prev_up = prev["_up"]
            if prev_up:
                if prev["high"] >= current["high"]:
                    new_high, hi_ri, hi_d = prev["high"], prev["high_raw_index"], prev["high_date"]
                else:
                    new_high, hi_ri, hi_d = current["high"], current["high_raw_index"], current["high_date"]
                if prev["low"] >= current["low"]:
                    new_low, lo_ri, lo_d = prev["low"], prev["low_raw_index"], prev["low_date"]
                else:
                    new_low, lo_ri, lo_d = current["low"], current["low_raw_index"], current["low_date"]
            else:
                if prev["high"] <= current["high"]:
                    new_high, hi_ri, hi_d = prev["high"], prev["high_raw_index"], prev["high_date"]
                else:
                    new_high, hi_ri, hi_d = current["high"], current["high_raw_index"], current["high_date"]
                if prev["low"] <= current["low"]:
                    new_low, lo_ri, lo_d = prev["low"], prev["low_raw_index"], prev["low_date"]
                else:
                    new_low, lo_ri, lo_d = current["low"], current["low_raw_index"], current["low_date"]

            result[prev_s_idx]["high"] = new_high
            result[prev_s_idx]["low"] = new_low
            result[prev_s_idx]["raw_end_index"] = current["raw_end_index"]
            result[prev_s_idx]["date"] = current["date"]
            result[prev_s_idx]["high_raw_index"] = hi_ri
            result[prev_s_idx]["low_raw_index"] = lo_ri
            result[prev_s_idx]["high_date"] = hi_d
            result[prev_s_idx]["low_date"] = lo_d
            result[prev_s_idx]["vol"] = prev.get("vol", 0) + current.get("vol", 0)
            result[prev_s_idx]["_up"] = result[prev_s_idx]["close"] >= result[prev_s_idx]["open"]
        else:
            result.append(current.to_dict())
        i += 1

    out = pd.DataFrame(result)
    drop_cols = [c for c in ("_up", "_raw_index") if c in out.columns]
    if drop_cols:
        out.drop(columns=drop_cols, inplace=True)
    return out


# ═══════════════════════════════════════════════════════════════════
#  缠论引擎 - 2. 分型识别
# ═══════════════════════════════════════════════════════════════════

def find_fractals(klines: pd.DataFrame) -> pd.DataFrame:
    """识别顶分型和底分型"""
    if klines is None or len(klines) < 3:
        df = klines.copy() if klines is not None else pd.DataFrame()
        df["fractal"] = None
        df["fractal_value"] = np.nan
        df["fractal_raw_index"] = np.nan
        df["fractal_date"] = None
        return df

    df = klines.copy().reset_index(drop=True)
    df["fractal"] = None
    df["fractal_value"] = np.nan
    df["fractal_raw_index"] = np.nan
    df["fractal_date"] = None
    n = len(df)

    for i in range(1, n - 1):
        h_p, h_c, h_n = df.loc[i-1, "high"], df.loc[i, "high"], df.loc[i+1, "high"]
        l_p, l_c, l_n = df.loc[i-1, "low"], df.loc[i, "low"], df.loc[i+1, "low"]

        if h_c > h_p and h_c > h_n and l_c > l_p and l_c > l_n:
            df.loc[i, "fractal"] = "top"
            df.loc[i, "fractal_value"] = h_c
            df.loc[i, "fractal_raw_index"] = int(df.loc[i, "high_raw_index"]) if "high_raw_index" in df.columns else i
            df.loc[i, "fractal_date"] = df.loc[i, "high_date"] if "high_date" in df.columns else df.loc[i, "date"]
        elif l_c < l_p and l_c < l_n and h_c < h_p and h_c < h_n:
            df.loc[i, "fractal"] = "bottom"
            df.loc[i, "fractal_value"] = l_c
            df.loc[i, "fractal_raw_index"] = int(df.loc[i, "low_raw_index"]) if "low_raw_index" in df.columns else i
            df.loc[i, "fractal_date"] = df.loc[i, "low_date"] if "low_date" in df.columns else df.loc[i, "date"]

    return df


def get_fractal_list(df: pd.DataFrame) -> List[Dict]:
    fractals = df[df["fractal"].notna()].copy()
    result = []
    for _, row in fractals.iterrows():
        result.append({
            "index": int(row.name),
            "date": row.get("fractal_date", row["date"]),
            "price": row["fractal_value"],
            "fractal_type": row["fractal"],
            "raw_index": int(row.get("fractal_raw_index", row.name)),
        })
    return result


# ═══════════════════════════════════════════════════════════════════
#  缠论引擎 - 3. 笔划分
# ═══════════════════════════════════════════════════════════════════

def divide_bi(df: pd.DataFrame, min_bi_length: int = MIN_BI_LENGTH) -> List[Dict]:
    """连接相邻顶底分型构成笔"""
    if df is None or len(df) < 3:
        return []

    fractal_rows = df[df["fractal"].notna()].copy()
    if len(fractal_rows) < 2:
        return []

    fractal_rows = fractal_rows.sort_index()
    bi_list = []
    prev_fractal = None

    def _meta(idx, row):
        raw_index = row.get("fractal_raw_index", idx)
        if pd.isna(raw_index):
            raw_index = idx
        date_value = row.get("fractal_date", row["date"])
        if date_value is None or pd.isna(date_value):
            date_value = row["date"]
        return {"index": idx, "raw_index": int(raw_index), "date": date_value,
                "price": row["fractal_value"], "type": row["fractal"]}

    for idx, row in fractal_rows.iterrows():
        current_type = row["fractal"]
        current_price = row["fractal_value"]
        current_fractal = _meta(idx, row)

        if prev_fractal is None:
            prev_fractal = current_fractal
            continue

        if current_type == prev_fractal["type"]:
            if (current_type == "top" and current_price > prev_fractal["price"]) \
               or (current_type == "bottom" and current_price < prev_fractal["price"]):
                prev_fractal = current_fractal
            continue

        kline_count = abs(idx - prev_fractal["index"])
        if kline_count < min_bi_length:
            continue

        bi_type = "up" if current_type == "top" else "down"
        start_idx = prev_fractal["index"]
        end_idx = idx
        segment = df.loc[start_idx:end_idx]
        high = segment["high"].max()
        low = segment["low"].min()

        bi_list.append({
            "start_index": start_idx, "end_index": end_idx,
            "raw_start_index": prev_fractal["raw_index"],
            "raw_end_index": current_fractal["raw_index"],
            "start_date": prev_fractal["date"], "end_date": current_fractal["date"],
            "start_price": prev_fractal["price"], "end_price": current_price,
            "bi_type": bi_type, "high": high, "low": low,
            "strength": abs(current_price - prev_fractal["price"]),
        })
        prev_fractal = current_fractal

    return bi_list


# ═══════════════════════════════════════════════════════════════════
#  缠论引擎 - 4. 中枢识别
# ═══════════════════════════════════════════════════════════════════

def identify_zhongshu(bi_list: List[Dict], tolerance: float = ZHONGSHU_TOLERANCE) -> List[Dict]:
    """滑动窗口扫描连续三笔的重叠区间"""
    if not bi_list or len(bi_list) < 3:
        return []

    zhongshu_list = []
    i = 0
    while i <= len(bi_list) - 3:
        three_bis = bi_list[i:i+3]
        lows = [b["low"] for b in three_bis]
        highs = [b["high"] for b in three_bis]
        zs_low = max(lows)
        zs_high = min(highs)

        if zs_low < zs_high * (1 - tolerance):
            zs_mid = (zs_low + zs_high) / 2
            j = i + 3
            while j < len(bi_list):
                bi = bi_list[j]
                if bi["low"] < zs_high and bi["high"] > zs_low:
                    j += 1
                else:
                    break

            zhongshu_list.append({
                "start_bi_index": i, "end_bi_index": j - 1,
                "start_date": bi_list[i]["start_date"],
                "end_date": bi_list[j-1]["end_date"],
                "zs_high": zs_high, "zs_low": zs_low, "zs_mid": zs_mid,
                "bi_count": j - i,
            })
            i = j
        else:
            i += 1

    return zhongshu_list


# ═══════════════════════════════════════════════════════════════════
#  缠论引擎 - 5. MACD计算
# ═══════════════════════════════════════════════════════════════════

def calc_macd(df: pd.DataFrame, fast=12, slow=26, signal=9) -> pd.DataFrame:
    df = df.copy()
    close = df["close"].values.astype(float)

    def ema(arr, period):
        result = np.zeros_like(arr)
        multiplier = 2.0 / (period + 1)
        result[0] = arr[0]
        for i in range(1, len(arr)):
            result[i] = (arr[i] - result[i-1]) * multiplier + result[i-1]
        return result

    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line

    df["macd"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_hist"] = histogram
    return df


# ═══════════════════════════════════════════════════════════════════
#  缠论引擎 - 6. 买卖点判定
# ═══════════════════════════════════════════════════════════════════

def _check_divergence(bi_list, macd_hist, direction="bottom") -> bool:
    if len(bi_list) < 4:
        return False

    same_bis = []
    for bi in reversed(bi_list):
        if (direction == "bottom" and bi["bi_type"] == "down") \
           or (direction == "top" and bi["bi_type"] == "up"):
            same_bis.append(bi)
            if len(same_bis) == 2:
                break

    if len(same_bis) < 2:
        return False

    areas = []
    for bi in same_bis:
        s = int(bi.get("raw_start_index", bi["start_index"]))
        e = int(bi.get("raw_end_index", bi["end_index"]))
        if e < s:
            s, e = e, s
        if s >= len(macd_hist) or e >= len(macd_hist):
            return False
        area = np.sum(np.abs(macd_hist[s:e+1]))
        areas.append(area)

    if direction == "bottom":
        price_cond = same_bis[0]["end_price"] < same_bis[1]["end_price"]
    else:
        price_cond = same_bis[0]["end_price"] > same_bis[1]["end_price"]
    area_cond = areas[0] < areas[1] * 0.9

    return price_cond and area_cond


def find_signals(df_raw, df_processed, bi_list, zhongshu_list,
                 min_bi_length=MIN_BI_LENGTH, tolerance=ZHONGSHU_TOLERANCE) -> List[Dict]:
    if not bi_list or len(bi_list) < 2:
        return []

    df_macd = calc_macd(df_raw)
    macd_hist = df_macd["macd_hist"].values

    signals = []

    # 一买
    buy1 = _find_first_buy(bi_list, macd_hist, zhongshu_list)
    if buy1:
        signals.append(buy1)

    # 二买
    buy2 = _find_second_buy(bi_list, buy1)
    if buy2:
        signals.append(buy2)

    # 三买
    buy3 = _find_third(bi_list, zhongshu_list, "buy")
    if buy3:
        signals.append(buy3)

    # 一卖
    sell1 = _find_first_sell(bi_list, macd_hist, zhongshu_list)
    if sell1:
        signals.append(sell1)

    # 二卖
    sell2 = _find_second_sell(bi_list, sell1)
    if sell2:
        signals.append(sell2)

    # 三卖
    sell3 = _find_third(bi_list, zhongshu_list, "sell")
    if sell3:
        signals.append(sell3)

    return signals


def _find_first_buy(bi_list, macd_hist, zhongshu_list):
    if len(bi_list) < 2:
        return None
    last_bi = bi_list[-1]
    if last_bi["bi_type"] != "down":
        return None

    has_zs = any(zs["end_bi_index"] >= len(bi_list) - 3 for zs in zhongshu_list)
    if not has_zs:
        return None

    beichi = _check_divergence(bi_list, macd_hist, "bottom")
    confidence = 0.8 if beichi else 0.5

    return {
        "date": str(last_bi["end_date"])[:10],
        "price": round(float(last_bi["end_price"]), 3),
        "signal_type": "buy", "level": 1,
        "description": "一买：下跌背驰底分型" + ("（MACD底背驰确认）" if beichi else "（无背驰，信号较弱）"),
        "confidence": confidence,
    }


def _find_first_sell(bi_list, macd_hist, zhongshu_list):
    if len(bi_list) < 2:
        return None
    last_bi = bi_list[-1]
    if last_bi["bi_type"] != "up":
        return None

    has_zs = any(zs["end_bi_index"] >= len(bi_list) - 3 for zs in zhongshu_list)
    beichi = _check_divergence(bi_list, macd_hist, "top")
    confidence = 0.8 if (beichi and has_zs) else 0.5

    return {
        "date": str(last_bi["end_date"])[:10],
        "price": round(float(last_bi["end_price"]), 3),
        "signal_type": "sell", "level": 1,
        "description": "一卖：上涨背驰顶分型" + ("（MACD顶背驰确认）" if beichi else "（无背驰，信号较弱）"),
        "confidence": confidence,
    }


def _find_second_buy(bi_list, buy1_signal):
    if buy1_signal is None:
        return None
    buy1_price = buy1_signal["price"]
    for bi in bi_list:
        if bi["bi_type"] == "down":
            if bi["end_price"] >= buy1_price * 0.995:
                return {
                    "date": str(bi["end_date"])[:10],
                    "price": round(float(bi["end_price"]), 3),
                    "signal_type": "buy", "level": 2,
                    "description": "二买：回调不破一买低点",
                    "confidence": 0.7,
                }
    return None


def _find_second_sell(bi_list, sell1_signal):
    if sell1_signal is None:
        return None
    sell1_price = sell1_signal["price"]
    for bi in bi_list:
        if bi["bi_type"] == "up":
            if bi["end_price"] <= sell1_price * 1.005:
                return {
                    "date": str(bi["end_date"])[:10],
                    "price": round(float(bi["end_price"]), 3),
                    "signal_type": "sell", "level": 2,
                    "description": "二卖：反弹不过一卖高点",
                    "confidence": 0.7,
                }
    return None


def _find_third(bi_list, zhongshu_list, mode="buy"):
    if not zhongshu_list or len(bi_list) < 3:
        return None
    zs = zhongshu_list[-1]

    if mode == "buy":
        for bi in reversed(bi_list):
            if bi["bi_type"] == "up" and bi["end_price"] > zs["zs_high"]:
                idx = bi_list.index(bi)
                for jb in bi_list[idx+1:]:
                    if jb["bi_type"] == "down":
                        if jb["low"] > zs["zs_high"]:
                            return {
                                "date": str(jb["end_date"])[:10],
                                "price": round(float(jb["end_price"]), 3),
                                "signal_type": "buy", "level": 3,
                                "description": "三买：突破中枢后回踩不进入",
                                "confidence": 0.75,
                            }
                        break
                break
    else:
        for bi in reversed(bi_list):
            if bi["bi_type"] == "down" and bi["end_price"] < zs["zs_low"]:
                idx = bi_list.index(bi)
                for jb in bi_list[idx+1:]:
                    if jb["bi_type"] == "up":
                        if jb["high"] < zs["zs_low"]:
                            return {
                                "date": str(jb["end_date"])[:10],
                                "price": round(float(jb["end_price"]), 3),
                                "signal_type": "sell", "level": 3,
                                "description": "三卖：跌破中枢后反弹不进入",
                                "confidence": 0.75,
                            }
                        break
                break
    return None


# ═══════════════════════════════════════════════════════════════════
#  完整引擎运行
# ═══════════════════════════════════════════════════════════════════

def run_engine(df_raw: pd.DataFrame) -> Dict:
    """运行完整缠论分解，返回所有结果"""
    result = {
        "klines_processed": None,
        "fractals": [],
        "bi_list": [],
        "zhongshu_list": [],
        "signals": [],
    }

    if df_raw is None or len(df_raw) < 5:
        return result

    # 1. 包含处理
    klines_processed = process_inclusion(df_raw)
    if len(klines_processed) < 3:
        return result
    result["klines_processed"] = klines_processed

    # 2. 分型识别
    klines_with_fractal = find_fractals(klines_processed)
    result["fractals"] = get_fractal_list(klines_with_fractal)

    # 3. 笔划分
    result["bi_list"] = divide_bi(klines_with_fractal)

    # 4. 中枢识别
    result["zhongshu_list"] = identify_zhongshu(result["bi_list"])

    # 5. 买卖点判定
    result["signals"] = find_signals(
        df_raw, klines_with_fractal,
        result["bi_list"], result["zhongshu_list"],
    )

    return result


# ═══════════════════════════════════════════════════════════════════
#  分析结果整理
# ═══════════════════════════════════════════════════════════════════

def _date_str(value) -> str:
    if value is None or value == "":
        return ""
    try:
        return pd.Timestamp(value).date().isoformat()
    except Exception:
        text = str(value)
        return text[:10] if len(text) >= 10 else text


def _signal_name(signal: Dict) -> str:
    level = int(signal.get("level", 0) or 0)
    sig_type = signal.get("signal_type", "")
    return f"{LEVEL_NAMES.get(level, str(level))}{TYPE_NAMES.get(sig_type, '')}"


def extract_recent_signals(signals: List[Dict], df_raw: pd.DataFrame,
                           recent_bars: int = 5) -> List[Dict]:
    """筛选最近 N 根 K 线内的信号"""
    if not signals or df_raw is None or df_raw.empty:
        return signals if recent_bars <= 0 else []

    if recent_bars <= 0:
        return signals

    date_index = {}
    for idx, date_value in enumerate(df_raw["date"]):
        date_index[_date_str(date_value)] = idx

    min_index = max(0, len(df_raw) - recent_bars)
    recent = []
    for signal in signals:
        key = _date_str(signal.get("date"))
        bar_index = date_index.get(key)
        if bar_index is not None and bar_index >= min_index:
            recent.append(signal)

    return recent


def build_analysis(code: str, df_raw: pd.DataFrame, engine_result: Dict,
                   category: int = 9, recent_bars: int = 0) -> Dict:
    """构建完整的分析结果 JSON"""
    latest = df_raw.iloc[-1]
    latest_close = float(latest.get("close", 0) or 0)
    prev_close = float(df_raw.iloc[-2].get("close", latest_close)) if len(df_raw) >= 2 else latest_close
    change_pct = round((latest_close - prev_close) / prev_close * 100, 2) if prev_close else 0.0

    bi_list = engine_result["bi_list"]
    zhongshu_list = engine_result["zhongshu_list"]
    signals = engine_result["signals"]

    # 筛选近期信号
    if recent_bars > 0:
        signals = extract_recent_signals(signals, df_raw, recent_bars)

    # 当前趋势判断
    current_trend = "未知"
    if bi_list:
        last_bi = bi_list[-1]
        if last_bi["bi_type"] == "up":
            current_trend = "向上"
        else:
            current_trend = "向下"

    # 当前价格相对于中枢的位置
    price_vs_zs = "无中枢参考"
    if zhongshu_list:
        zs = zhongshu_list[-1]
        if latest_close > zs["zs_high"]:
            price_vs_zs = f"在中枢上方（中枢上沿:{zs['zs_high']:.2f} 下沿:{zs['zs_low']:.2f}）"
        elif latest_close < zs["zs_low"]:
            price_vs_zs = f"在中枢下方（中枢上沿:{zs['zs_high']:.2f} 下沿:{zs['zs_low']:.2f}）"
        else:
            price_vs_zs = f"在中枢内部（中枢上沿:{zs['zs_high']:.2f} 下沿:{zs['zs_low']:.2f}）"

    # 信号分类
    buy_signals = [s for s in signals if s["signal_type"] == "buy"]
    sell_signals = [s for s in signals if s["signal_type"] == "sell"]

    # 最近笔信息
    last_bi_info = None
    if bi_list:
        lb = bi_list[-1]
        last_bi_info = {
            "direction": "向上" if lb["bi_type"] == "up" else "向下",
            "start_date": _date_str(lb["start_date"]),
            "end_date": _date_str(lb["end_date"]),
            "start_price": round(float(lb["start_price"]), 3),
            "end_price": round(float(lb["end_price"]), 3),
            "strength": round(float(lb["strength"]), 3),
        }

    # 中枢信息
    zhongshu_info = []
    for zs in zhongshu_list[-3:]:  # 最近3个中枢
        zhongshu_info.append({
            "start_date": _date_str(zs["start_date"]),
            "end_date": _date_str(zs["end_date"]),
            "high": round(float(zs["zs_high"]), 3),
            "low": round(float(zs["zs_low"]), 3),
            "mid": round(float(zs["zs_mid"]), 3),
            "bi_count": zs["bi_count"],
        })

    # 构建信号列表
    signal_list = []
    for s in signals:
        signal_list.append({
            "name": _signal_name(s),
            "type": s["signal_type"],
            "level": s["level"],
            "date": s["date"],
            "price": s["price"],
            "confidence": s["confidence"],
            "description": s["description"],
        })

    # 按日期排序
    signal_list.sort(key=lambda x: x["date"], reverse=True)

    result = {
        "code": _normalize_code(code),
        "period": PERIOD_MAP.get(category, str(category)),
        "latest_date": _date_str(latest.get("date", "")),
        "latest_close": round(latest_close, 3),
        "change_pct": change_pct,
        "kline_count": len(df_raw),
        "structure": {
            "fractal_count": len(engine_result["fractals"]),
            "bi_count": len(bi_list),
            "zhongshu_count": len(zhongshu_list),
            "current_trend": current_trend,
            "price_vs_zs": price_vs_zs,
            "last_bi": last_bi_info,
            "recent_zhongshu": zhongshu_info,
        },
        "signals": signal_list,
        "buy_signal_count": len(buy_signals),
        "sell_signal_count": len(sell_signals),
        "latest_signal": signal_list[0] if signal_list else None,
    }

    return result


# ═══════════════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════════════

def analyze(code: str, category: int = 9, count: int = KLINE_COUNT,
            recent_bars: int = 0) -> Dict:
    """分析单只股票的缠论买卖点

    参数:
        code: 6位股票代码
        category: 周期 (9=日线, 7=周线, 5=30分钟, 6=60分钟)
        count: K线条数
        recent_bars: 只返回最近N根K线内的信号，0=全部

    返回: 分析结果字典
    """
    df_raw = fetch_kline(code, category=category, count=count)
    if df_raw is None or df_raw.empty:
        return {"error": f"无法获取 {code} 的K线数据"}

    engine_result = run_engine(df_raw)
    return build_analysis(code, df_raw, engine_result, category, recent_bars)


def main():
    parser = argparse.ArgumentParser(description="缠论买卖点分析工具")
    parser.add_argument("code", help="6位股票代码，如 000001")
    parser.add_argument("--period", type=int, default=9,
                        help="周期: 9=日线(默认), 7=周线, 6=60分钟, 5=30分钟")
    parser.add_argument("--count", type=int, default=KLINE_COUNT,
                        help=f"K线条数 (默认{KLINE_COUNT})")
    parser.add_argument("--recent", type=int, default=0,
                        help="只返回最近N根K线内的信号，0=全部 (默认0)")

    args = parser.parse_args()

    try:
        result = analyze(args.code, args.period, args.count, args.recent)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
