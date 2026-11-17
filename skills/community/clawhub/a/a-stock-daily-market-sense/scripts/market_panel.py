#!/usr/bin/env python3
"""
Atomic market evidence pack builder for the a-stock-daily-market-sense skill.

The script fetches Tushare data and computes deterministic numeric features.
It intentionally does not name themes, write research reports, or produce
investment recommendations. The model using the skill performs interpretation.
"""

from __future__ import annotations

import argparse
import contextlib
from html.parser import HTMLParser
import io
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - dependency check
    raise RuntimeError("Missing dependency: install pandas before using this script.") from exc

try:
    import tushare as ts
except ImportError as exc:  # pragma: no cover - dependency check
    raise RuntimeError("Missing dependency: install tushare before using this script.") from exc

try:
    import akshare as ak
except ImportError:  # pragma: no cover - optional runtime dependency
    ak = None

try:
    import baostock as bs
except ImportError:  # pragma: no cover - optional runtime dependency
    bs = None

try:
    import requests
except ImportError:  # pragma: no cover - optional runtime dependency
    requests = None

SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = SCRIPT_DIR / "_shared"
_DEV_SHARED = SCRIPT_DIR.parents[2] / "shared" / "data"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))
from db_core import BACKEND, Backend
from db_adapter import (
    read_frame,
    write_frame,
    read_dataset,
    write_dataset,
    read_market_history,
    write_market_history,
)


DEFAULT_DAILY_FIELDS = (
    "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
)
DEFAULT_ADJ_FACTOR_FIELDS = "ts_code,trade_date,adj_factor"
DEFAULT_BASIC_FIELDS = (
    "ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv,circ_mv"
)
DEFAULT_STOCK_FIELDS = "ts_code,name,market,list_date"
DEFAULT_INDEX_FIELDS = "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
SKILL_ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = SKILL_ROOT / "data" / "cache"
REFERENCE_ROOT = SKILL_ROOT / "references"
DEFAULT_MARKET_HISTORY_CSV = REFERENCE_ROOT / "market_data.csv"
DEFAULT_MARKET_HISTORY_JSON = REFERENCE_ROOT / "market_data.json"
MARKET_HISTORY_COLUMNS = [
    "日期",
    "上涨",
    "涨停",
    "下跌",
    "跌停",
    "平盘",
    "活跃度",
    "情绪值",
    "成交额",
    "融资净买入",
    "全市场换手率",
]
MARKET_ACTIVITY_COLUMNS = ["上涨", "涨停", "下跌", "跌停", "平盘", "活跃度", "情绪值", "成交额"]
CORRUPTED_MARKET_TURNOVER_COLUMNS = {"?????", "??????"}
MARKET_HISTORY_DB_COLUMNS = {
    "日期": "date",
    "上涨": "rise",
    "涨停": "limit_up",
    "下跌": "fall",
    "跌停": "limit_down",
    "平盘": "flat",
    "活跃度": "activity",
    "情绪值": "sentiment",
    "成交额": "amount",
    "融资净买入": "margin_net_buy",
    "全市场换手率": "turnover_rate",
}

MARKET_TREND_INDEXES = {
    "shanghai": {"name": "上证指数", "ts_code": "000001.SH"},
    "chinext": {"name": "创业板指数", "ts_code": "399006.SZ"},
    "star50": {"name": "科创50", "ts_code": "000688.SH"},
}
MARKET_STYLE_INDEXES = {
    "mega_cap": {"name": "超大盘", "bs_code": "sh.000043", "style_role": "容量大盘"},
    "csi300": {"name": "沪深300", "bs_code": "sh.000300", "style_role": "容量中枢"},
    "csi500": {"name": "中证500", "bs_code": "sh.000905", "style_role": "中盘代表"},
    "csi1000": {"name": "中证1000", "bs_code": "sh.000852", "style_role": "小盘代表"},
    "guozheng2000": {
        "name": "国证2000",
        "bs_code": "sz.399303",
        "style_role": "微盘代理",
        "proxy_note": "Baostock 指数字典未见直接的微盘指数，默认用国证2000代理小微盘风格。",
    },
    "csi_dividend": {"name": "中证红利", "bs_code": "sh.000922", "style_role": "红利防守"},
    "csi300_growth": {"name": "300成长", "bs_code": "sh.000918", "style_role": "成长"},
    "csi300_value": {"name": "300价值", "bs_code": "sh.000919", "style_role": "价值"},
}
INDEX_REGISTRY = tuple(
    [
        {
            "key": key,
            "name": config.get("name"),
            "source": "tushare",
            "roles": ["trend"],
            "ts_code": config.get("ts_code"),
        }
        for key, config in MARKET_TREND_INDEXES.items()
    ]
    + [
        {
            "key": key,
            "name": config.get("name"),
            "source": "baostock",
            "roles": ["style"],
            "bs_code": config.get("bs_code"),
        }
        for key, config in MARKET_STYLE_INDEXES.items()
    ]
)
BAOSTOCK_STYLE_FIELDS = "date,code,open,high,low,close,preclose,volume,amount,pctChg"
BAOSTOCK_STYLE_SOURCE_URL = "https://www.baostock.com/mainContent?file=dataExplain.md"
DEFAULT_INDEX_KLINE_DAYS = 120
MARKET_HISTORY_PRIMARY_SOURCE = "tushare.daily+sentiment_calc"
MARKET_HISTORY_SUPPLEMENT_SOURCE = "tushare.daily,daily_basic,margin(T-1)"
MARKET_HISTORY_SOHU_SOURCE = "sohu.zdt_history"
SOHU_LIMIT_HISTORY_URL = "https://q.stock.sohu.com/cn/zdt.shtml"
JRJ_LIMIT_UP_URL = "https://gateway.jrj.com/quot-dc/zdt/v1/record"
SOHU_LIMIT_HISTORY_CACHE: Dict[str, Dict[str, Dict[str, Any]]] = {}


class StageTimer:
    """Sequential stage timer for build_panel observability."""

    def __init__(self) -> None:
        self.timings: Dict[str, float] = {}
        self._start = time.perf_counter()
        self._last = self._start

    def mark(self, name: str) -> None:
        now = time.perf_counter()
        self.timings[name] = round(now - self._last, 3)
        self._last = now

    def total(self) -> float:
        return round(time.perf_counter() - self._start, 3)


def get_tushare_token() -> str:
    """Read TUSHARE_TOKEN from the environment or cwd/.env."""
    token = os.environ.get("TUSHARE_TOKEN", "").strip()
    if token:
        return token

    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        return ""

    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            if key.strip() == "TUSHARE_TOKEN":
                return value.strip().strip('"').strip("'")
    return ""


def get_pro():
    token = get_tushare_token()
    if not token:
        raise RuntimeError("Missing TUSHARE_TOKEN. Set it in the environment or cwd/.env.")
    return ts.pro_api(token)


def normalize_date(value: Optional[str]) -> str:
    """Normalize date input to YYYYMMDD."""
    if not value:
        return datetime.now().strftime("%Y%m%d")
    raw = str(value).strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y%m%d")
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {value}. Use YYYYMMDD or YYYY-MM-DD.")


def ymd_to_dt(value: str) -> datetime:
    return datetime.strptime(normalize_date(value), "%Y%m%d")


def dataframe_to_records(df: Optional[pd.DataFrame]) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    cleaned = df.copy()
    cleaned = cleaned.where(pd.notnull(cleaned), None)
    return cleaned.to_dict(orient="records")


def split_fields(fields: str) -> List[str]:
    return [field.strip() for field in fields.split(",") if field.strip()]


def cache_file(endpoint: str, trade_date: str) -> Path:
    return CACHE_ROOT / endpoint / f"{trade_date}.parquet"


def cache_dataset_file(endpoint: str, key: str) -> Path:
    safe_key = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(key))
    return CACHE_ROOT / endpoint / f"{safe_key}.parquet"


def read_cached_dataset(endpoint: str, key: str, fields: Optional[str] = None) -> Optional[pd.DataFrame]:
    if BACKEND == Backend.POSTGRESQL:
        return read_dataset(endpoint, key, fields)

    path = cache_dataset_file(endpoint, key)
    if not path.exists():
        return None
    try:
        df = pd.read_parquet(path)
    except Exception as exc:
        print(f"[warn] failed to read cache {path}: {exc}", file=sys.stderr)
        return None

    if fields:
        missing = [field for field in split_fields(fields) if field not in df.columns]
        if missing:
            print(f"[warn] ignoring stale cache {path}, missing fields: {','.join(missing)}", file=sys.stderr)
            return None
    return df


def write_cached_dataset(endpoint: str, key: str, df: pd.DataFrame) -> None:
    if BACKEND == Backend.POSTGRESQL:
        write_dataset(endpoint, key, df)
        return

    path = cache_dataset_file(endpoint, key)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
    except Exception as exc:
        print(f"[warn] failed to write cache {path}: {exc}", file=sys.stderr)


def date_range_filter(df: pd.DataFrame, column: str, start_date: str, end_date: str) -> pd.DataFrame:
    if df is None or df.empty or column not in df.columns:
        return pd.DataFrame()
    out = df.copy()
    normalized_dates = out[column].apply(lambda value: normalize_date(value) if not pd.isna(value) else "")
    out[column] = normalized_dates
    return out.loc[(normalized_dates >= start_date) & (normalized_dates <= end_date)].copy()


def missing_edge_ranges(df: pd.DataFrame, column: str, start_date: str, end_date: str) -> List[Tuple[str, str]]:
    if df is None or df.empty or column not in df.columns:
        return [(start_date, end_date)]

    dates = df[column].apply(lambda value: normalize_date(value) if not pd.isna(value) else "")
    dates = dates.loc[dates != ""]
    if dates.empty:
        return [(start_date, end_date)]
    cached_min = dates.min()
    cached_max = dates.max()
    ranges: List[Tuple[str, str]] = []
    if start_date < cached_min:
        ranges.append((start_date, (ymd_to_dt(cached_min) - timedelta(days=1)).strftime("%Y%m%d")))
    if end_date > cached_max:
        ranges.append(((ymd_to_dt(cached_max) + timedelta(days=1)).strftime("%Y%m%d"), end_date))
    return [(start, end) for start, end in ranges if start <= end]


def read_cached_frame(endpoint: str, trade_date: str, fields: str) -> Optional[pd.DataFrame]:
    if BACKEND == Backend.POSTGRESQL:
        return read_frame(endpoint, trade_date, fields)

    path = cache_file(endpoint, trade_date)
    if not path.exists():
        return None
    try:
        df = pd.read_parquet(path)
    except Exception as exc:
        print(f"[warn] failed to read cache {path}: {exc}", file=sys.stderr)
        return None

    missing = [field for field in split_fields(fields) if field not in df.columns]
    if missing:
        print(f"[warn] ignoring stale cache {path}, missing fields: {','.join(missing)}", file=sys.stderr)
        return None
    return df


def write_cached_frame(endpoint: str, trade_date: str, df: pd.DataFrame) -> None:
    if BACKEND == Backend.POSTGRESQL:
        write_frame(endpoint, trade_date, df)
        return

    path = cache_file(endpoint, trade_date)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
    except Exception as exc:
        print(f"[warn] failed to write cache {path}: {exc}", file=sys.stderr)


def safe_float(value: Any) -> Optional[float]:
    if value is None or pd.isna(value):
        return None
    return float(value)


def nullable_value(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def fetch_trade_cal(
    pro,
    start_date: str,
    end_date: str,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    fields = "cal_date,is_open"
    cache_key = "all"
    cached = None if refresh_cache or not cache_enabled else read_cached_dataset("trade_cal", cache_key, fields)
    fetch_ranges = missing_edge_ranges(cached, "cal_date", start_date, end_date) if cached is not None else [(start_date, end_date)]

    frames: List[pd.DataFrame] = []
    if cached is not None and not cached.empty:
        frames.append(cached)

    for fetch_start, fetch_end in fetch_ranges:
        try:
            df = pro.trade_cal(exchange="", start_date=fetch_start, end_date=fetch_end, fields=fields)
        except Exception as exc:
            print(f"[warn] trade_cal failed for {fetch_start}-{fetch_end}: {exc}", file=sys.stderr)
            continue
        if df is not None and not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame(columns=["cal_date", "is_open"])

    merged = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["cal_date"], keep="last")
    merged["cal_date"] = merged["cal_date"].astype(str)
    merged = merged.sort_values("cal_date")
    if cache_enabled and not merged.empty:
        write_cached_dataset("trade_cal", cache_key, merged)
    return date_range_filter(merged, "cal_date", start_date, end_date)


def fetch_trade_dates(
    pro,
    asof: str,
    lookback: int,
    offset: int,
    allow_future: bool,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Tuple[str, List[str]]:
    """Resolve the analysis trade date and lookback dates using Tushare trade_cal."""
    asof_dt = ymd_to_dt(asof)
    start = (asof_dt - timedelta(days=max(lookback * 3, 260))).strftime("%Y%m%d")
    today = datetime.now().strftime("%Y%m%d")
    end_dt = max(asof_dt, ymd_to_dt(today))
    end = (end_dt + timedelta(days=10)).strftime("%Y%m%d") if allow_future else today

    cal = fetch_trade_cal(
        pro,
        start,
        end,
        cache_enabled=cache_enabled,
        refresh_cache=refresh_cache,
    )
    if cal is None or cal.empty:
        raise RuntimeError("trade_cal returned no data.")

    open_dates = sorted(cal.loc[cal["is_open"] == 1, "cal_date"].astype(str).tolist())
    if not open_dates:
        raise RuntimeError("No open trading days found in trade_cal result.")

    anchor_candidates = [d for d in open_dates if d <= asof]
    if not anchor_candidates:
        raise RuntimeError(f"No trading day found on or before {asof}.")
    anchor = anchor_candidates[-1]
    anchor_index = open_dates.index(anchor)
    target_index = anchor_index + offset

    if offset > 0 and not allow_future:
        raise RuntimeError("Positive offset reads future data. Re-run with --allow-future only for post-hoc verification.")
    if target_index < 0 or target_index >= len(open_dates):
        raise RuntimeError(f"Offset {offset} from {anchor} is outside available trade calendar.")

    target = open_dates[target_index]
    window_start_index = max(0, target_index - lookback + 1)
    window = open_dates[window_start_index : target_index + 1]
    return target, window


def fetch_by_trade_dates(
    pro,
    endpoint: str,
    trade_dates: Iterable[str],
    fields: str,
    sleep_seconds: float,
    cache_enabled: bool = False,
    refresh_cache: bool = False,
    max_workers: int = 1,
) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    api = getattr(pro, endpoint)
    dates = [str(date) for date in trade_dates]
    misses: List[str] = []
    if cache_enabled and not refresh_cache and BACKEND == Backend.POSTGRESQL and dates:
        # One range query instead of one SELECT per trade date.
        cached_dates: Set[str] = set()
        try:
            cached = read_dataset(
                endpoint,
                "",
                fields,
                date_column="trade_date",
                start_date=min(dates),
                end_date=max(dates),
            )
        except Exception as exc:
            print(f"[warn] {endpoint} range read failed: {exc}", file=sys.stderr)
            cached = None
        if cached is not None and not cached.empty:
            cached = cached.loc[cached["trade_date"].astype(str).isin(set(dates))]
            if not cached.empty:
                frames.append(cached)
                cached_dates = set(cached["trade_date"].astype(str).unique())
        misses = [trade_date for trade_date in dates if trade_date not in cached_dates]
    else:
        for trade_date in dates:
            if cache_enabled and not refresh_cache:
                cached = read_cached_frame(endpoint, trade_date, fields)
                if cached is not None:
                    frames.append(cached)
                    continue
            misses.append(trade_date)

    def fetch_one(trade_date: str) -> pd.DataFrame:
        try:
            df = api(trade_date=trade_date, fields=fields)
        except Exception as exc:
            print(f"[warn] {endpoint} failed for {trade_date}: {exc}", file=sys.stderr)
            return pd.DataFrame()
        if df is not None and not df.empty:
            if cache_enabled:
                write_cached_frame(endpoint, trade_date, df)
            result = df
        else:
            result = pd.DataFrame()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
        return result

    worker_count = max(1, int(max_workers or 1))
    if worker_count == 1 or len(misses) <= 1:
        for trade_date in misses:
            df = fetch_one(trade_date)
            if df is not None and not df.empty:
                frames.append(df)
    else:
        with ThreadPoolExecutor(max_workers=min(worker_count, len(misses))) as executor:
            future_map = {executor.submit(fetch_one, trade_date): trade_date for trade_date in misses}
            for future in as_completed(future_map):
                df = future.result()
                if df is not None and not df.empty:
                    frames.append(df)
    if not frames:
        return pd.DataFrame()
    merged = pd.concat(frames, ignore_index=True)
    if {"ts_code", "trade_date"}.issubset(merged.columns):
        return merged.drop_duplicates(subset=["ts_code", "trade_date"], keep="last")
    return merged.drop_duplicates()


def fetch_adj_factors_by_trade_dates(
    pro,
    trade_dates: Iterable[str],
    sleep_seconds: float,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
    max_workers: int = 1,
) -> pd.DataFrame:
    """Fetch Tushare adj_factor rows for qfq adjustment, PG-cached like daily."""
    df = fetch_by_trade_dates(
        pro,
        "adj_factor",
        trade_dates,
        DEFAULT_ADJ_FACTOR_FIELDS,
        sleep_seconds,
        cache_enabled=cache_enabled,
        refresh_cache=refresh_cache,
        max_workers=max_workers,
    )
    if df is None or df.empty:
        return pd.DataFrame(columns=split_fields(DEFAULT_ADJ_FACTOR_FIELDS))
    df = df.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    df["ts_code"] = df["ts_code"].astype(str)
    df["adj_factor"] = pd.to_numeric(df["adj_factor"], errors="coerce")
    return df.drop_duplicates(subset=["ts_code", "trade_date"], keep="last")


def apply_qfq_adjustment(daily: pd.DataFrame, adj_factors: pd.DataFrame, target_date: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Return daily rows with OHLC prices adjusted to target-date qfq basis."""
    metadata: Dict[str, Any] = {
        "price_adjustment": "qfq",
        "method": "Tushare daily OHLC * adj_factor / latest_adj_factor_by_ts_code_on_or_before_target_date",
        "target_date": target_date,
        "adjusted": False,
    }
    if daily is None or daily.empty:
        metadata["reason"] = "daily is empty"
        return daily, metadata
    if adj_factors is None or adj_factors.empty:
        metadata["reason"] = "adj_factor is empty"
        return daily, metadata

    df = daily.copy()
    df["ts_code"] = df["ts_code"].astype(str)
    df["trade_date"] = df["trade_date"].astype(str)
    adj = adj_factors.copy()
    adj["ts_code"] = adj["ts_code"].astype(str)
    adj["trade_date"] = adj["trade_date"].astype(str)
    adj["adj_factor"] = pd.to_numeric(adj["adj_factor"], errors="coerce")
    adj = adj.dropna(subset=["ts_code", "trade_date", "adj_factor"])
    adj = adj.loc[adj["trade_date"] <= target_date].copy()
    if adj.empty:
        metadata["reason"] = "no adj_factor rows on or before target date"
        return daily, metadata

    latest = (
        adj.sort_values(["ts_code", "trade_date"])
        .groupby("ts_code", as_index=False)
        .tail(1)[["ts_code", "adj_factor"]]
        .rename(columns={"adj_factor": "base_adj_factor"})
    )
    merged = df.merge(adj[["ts_code", "trade_date", "adj_factor"]], on=["ts_code", "trade_date"], how="left")
    merged = merged.merge(latest, on="ts_code", how="left")
    merged["qfq_factor"] = merged["adj_factor"] / merged["base_adj_factor"]
    valid_mask = merged["qfq_factor"].notna() & (merged["qfq_factor"] > 0)

    price_columns = [col for col in ("open", "high", "low", "close") if col in merged.columns]
    for column in price_columns:
        merged[column] = pd.to_numeric(merged[column], errors="coerce")
        merged.loc[valid_mask, column] = merged.loc[valid_mask, column] * merged.loc[valid_mask, "qfq_factor"]

    merged = merged.sort_values(["ts_code", "trade_date"]).reset_index(drop=True)
    if "close" in merged.columns:
        grouped_close = merged.groupby("ts_code")["close"]
        merged["pre_close"] = grouped_close.shift(1)
        merged["change"] = merged["close"] - merged["pre_close"]
        merged["pct_chg"] = (merged["close"] / merged["pre_close"] - 1.0) * 100.0

    metadata.update({
        "adjusted": True,
        "daily_rows": int(len(merged)),
        "adj_factor_rows": int(len(adj)),
        "adjusted_rows": int(valid_mask.sum()),
        "unadjusted_rows": int((~valid_mask).sum()),
        "adjusted_code_count": int(merged.loc[valid_mask, "ts_code"].nunique()),
    })
    return merged, metadata


def fetch_stock_basic(
    pro,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    cached = None if refresh_cache or not cache_enabled else read_cached_dataset("stock_basic", "all", DEFAULT_STOCK_FIELDS)
    if cached is not None and not cached.empty:
        return cached

    try:
        df = pro.stock_basic(exchange="", list_status="L", fields=DEFAULT_STOCK_FIELDS)
    except Exception as exc:
        print(f"[warn] stock_basic failed: {exc}", file=sys.stderr)
        if cached is not None and not cached.empty:
            return cached
        return pd.DataFrame(columns=["ts_code", "name", "market", "list_date"])
    if df is not None and not df.empty and cache_enabled:
        write_cached_dataset("stock_basic", "all", df)
    return df if df is not None else pd.DataFrame(columns=["ts_code", "name", "market", "list_date"])


def fetch_index_daily(
    pro,
    index_code: str,
    start_date: str,
    end_date: str,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    cache_key = index_code
    cached = None if refresh_cache or not cache_enabled else read_cached_dataset("index_daily", cache_key, DEFAULT_INDEX_FIELDS)
    fetch_ranges = missing_edge_ranges(cached, "trade_date", start_date, end_date) if cached is not None else [(start_date, end_date)]

    frames: List[pd.DataFrame] = []
    if cached is not None and not cached.empty:
        frames.append(cached)

    for fetch_start, fetch_end in fetch_ranges:
        try:
            df = pro.index_daily(
                ts_code=index_code,
                start_date=fetch_start,
                end_date=fetch_end,
                fields=DEFAULT_INDEX_FIELDS,
            )
        except Exception as exc:
            print(f"[warn] index_daily failed for {index_code} {fetch_start}-{fetch_end}: {exc}", file=sys.stderr)
            continue
        if df is not None and not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    merged = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["ts_code", "trade_date"], keep="last")
    merged["trade_date"] = merged["trade_date"].astype(str)
    merged = merged.sort_values("trade_date")
    if cache_enabled and not merged.empty:
        write_cached_dataset("index_daily", cache_key, merged)
    return date_range_filter(merged, "trade_date", start_date, end_date)


def fetch_limit_list(pro, trade_date: str) -> pd.DataFrame:
    try:
        df = pro.limit_list_d(trade_date=trade_date)
    except Exception as exc:
        print(f"[warn] limit_list_d failed for {trade_date}: {exc}", file=sys.stderr)
        return pd.DataFrame()
    return df if df is not None else pd.DataFrame()


def pct_return(series: pd.Series, periods: int) -> pd.Series:
    return (series / series.shift(periods) - 1.0) * 100.0


def add_numeric_features(daily: pd.DataFrame) -> pd.DataFrame:
    df = daily.copy()
    for column in ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df["trade_date"] = df["trade_date"].astype(str)
    df = df.sort_values(["ts_code", "trade_date"])
    grouped = df.groupby("ts_code", group_keys=False)
    df["history_days"] = grouped.cumcount() + 1

    for period in (1, 3, 5, 10, 20):
        df[f"ret_{period}d"] = grouped["close"].pct_change(period) * 100.0

    df["close_ma5"] = grouped["close"].transform(lambda s: s.rolling(5, min_periods=5).mean())
    df["close_ma20"] = grouped["close"].transform(lambda s: s.rolling(20, min_periods=20).mean())
    df["close_ma60"] = grouped["close"].transform(lambda s: s.rolling(60, min_periods=60).mean())
    df["prev_high_10d"] = grouped["high"].transform(lambda s: s.shift(1).rolling(10, min_periods=5).max())
    df["prev_high_120d"] = grouped["high"].transform(lambda s: s.shift(1).rolling(120, min_periods=60).max())
    df["close_to_high"] = df["close"] / df["high"].replace(0, pd.NA)
    df["amount_ma20_prev"] = grouped["amount"].transform(lambda s: s.shift(1).rolling(20, min_periods=5).mean())
    df["amount_ratio_20d"] = df["amount"] / df["amount_ma20_prev"]
    df["amount_ma15_prev"] = grouped["amount"].transform(lambda s: s.shift(1).rolling(15, min_periods=10).mean())
    df["amount_ratio_15d"] = df["amount"] / df["amount_ma15_prev"]
    df["high_60d"] = grouped["high"].transform(lambda s: s.rolling(60, min_periods=20).max())
    df["high_120d"] = grouped["high"].transform(lambda s: s.rolling(120, min_periods=30).max())
    df["low_120d"] = grouped["low"].transform(lambda s: s.rolling(120, min_periods=30).min())
    df["drawdown_120_high"] = (df["close"] / df["high_120d"] - 1.0) * 100.0
    range_120 = df["high_120d"] - df["low_120d"]
    df["close_position_120d"] = (df["close"] - df["low_120d"]) / range_120.replace(0, pd.NA)
    df["sustained_volume_days_5"] = grouped["amount_ratio_20d"].transform(
        lambda s: s.gt(1.5).rolling(5, min_periods=1).sum()
    )
    df["close_cv_10d"] = grouped["close"].transform(
        lambda s: s.rolling(10, min_periods=8).std() / s.rolling(10, min_periods=8).mean()
    )
    # 折扣启动（discount-relaunch）量能特征：调整期缩量 → 当日重新放量。
    # 前高折扣（前高之后最低价 / 前高收盘价）改由 attach_discount_after_high 按多日序列另算。
    df["amount_ma5_prev"] = grouped["amount"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=3).mean()
    )
    df["pre_volume_contraction_ratio"] = df["amount_ma5_prev"] / df["amount_ma20_prev"]
    df["amount_vs_prev5_ratio"] = df["amount"] / df["amount_ma5_prev"]
    df["pre_ret_5d"] = (grouped["close"].transform(lambda s: s.shift(1) / s.shift(6)) - 1.0) * 100.0
    return df


def add_screening_features(daily: pd.DataFrame) -> pd.DataFrame:
    """Add only full-market features needed for cheap coarse screens."""
    df = daily.copy()
    for column in ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    if df.empty:
        return df
    df["trade_date"] = df["trade_date"].astype(str)
    df = df.sort_values(["ts_code", "trade_date"])
    grouped = df.groupby("ts_code", group_keys=False)
    df["ret_5d"] = grouped["close"].pct_change(5) * 100.0
    df["amount_ma20_prev"] = grouped["amount"].transform(lambda s: s.shift(1).rolling(20, min_periods=5).mean())
    df["amount_ratio_20d"] = df["amount"] / df["amount_ma20_prev"]
    return df


def add_index_features(panel: pd.DataFrame, index_daily: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Optional[float]]]:
    trade_date = str(panel["trade_date"].iloc[0]) if "trade_date" in panel.columns and not panel.empty else ""
    index_summary = summarize_index(index_daily, trade_date)
    if index_daily is None or index_daily.empty:
        panel["rel_ret_5d"] = None
        panel["rel_ret_10d"] = None
        return panel, index_summary

    index_ret_5d = index_summary["index_ret_5d"]
    index_ret_10d = index_summary["index_ret_10d"]
    panel["rel_ret_5d"] = (
        panel["ret_5d"] - index_ret_5d
        if index_ret_5d is not None and "ret_5d" in panel.columns
        else None
    )
    panel["rel_ret_10d"] = (
        panel["ret_10d"] - index_ret_10d
        if index_ret_10d is not None and "ret_10d" in panel.columns
        else None
    )
    return panel, index_summary


def summarize_index(index_daily: pd.DataFrame, trade_date: str) -> Dict[str, Optional[float]]:
    summary: Dict[str, Optional[float]] = {
        "index_ret_1d": None,
        "index_ret_3d": None,
        "index_ret_5d": None,
        "index_ret_10d": None,
    }
    if index_daily is None or index_daily.empty or not trade_date:
        return summary

    idx = index_daily.copy()
    idx["trade_date"] = idx["trade_date"].astype(str)
    idx["close"] = pd.to_numeric(idx["close"], errors="coerce")
    idx = idx.sort_values("trade_date")
    for period in (1, 3, 5, 10):
        idx[f"index_ret_{period}d"] = pct_return(idx["close"], period)

    row = idx.loc[idx["trade_date"] <= trade_date].tail(1)
    if row.empty:
        return summary
    latest = row.iloc[0]
    for period in (1, 3, 5, 10):
        field = f"index_ret_{period}d"
        if pd.notna(latest[field]):
            summary[field] = round(float(latest[field]), 2)
    return summary


def merge_optional(panel: pd.DataFrame, other: pd.DataFrame, on: List[str]) -> pd.DataFrame:
    if other is None or other.empty:
        return panel
    return panel.merge(other, on=on, how="left")


def count_limit_hits(frame: pd.DataFrame) -> Tuple[int, int, str]:
    """Count limit-up/down rows, preferring exact board-rule flags.

    Frames that merged compute_limit_flags carry is_limit_up/is_limit_down;
    without them fall back to the ±9.8% pct_chg approximation.
    """
    if {"is_limit_up", "is_limit_down"}.issubset(frame.columns):
        up = int(frame["is_limit_up"].fillna(False).astype(bool).sum())
        down = int(frame["is_limit_down"].fillna(False).astype(bool).sum())
        return up, down, "board_rule_price_match"
    pct = pd.to_numeric(frame["pct_chg"], errors="coerce") if "pct_chg" in frame.columns else pd.Series(dtype=float)
    return int((pct >= 9.8).sum()), int((pct <= -9.8).sum()), "pct_chg_approx"


def build_market_temperature(panel: pd.DataFrame, index_summary: Dict[str, Optional[float]]) -> Dict[str, Any]:
    total = int(len(panel))
    up = int((panel["pct_chg"] > 0).sum())
    down = int((panel["pct_chg"] < 0).sum())
    flat = total - up - down
    total_amount = float(panel["amount"].sum(skipna=True))
    up_amount = float(panel.loc[panel["pct_chg"] > 0, "amount"].sum(skipna=True))
    down_amount = float(panel.loc[panel["pct_chg"] < 0, "amount"].sum(skipna=True))
    top50_amount = float(panel.nlargest(min(50, total), "amount")["amount"].sum(skipna=True)) if total else 0.0
    limit_up_count, limit_down_count, limit_detection = count_limit_hits(panel)

    return {
        "stock_count": total,
        "up_count": up,
        "down_count": down,
        "flat_count": flat,
        "up_ratio": round(up / total, 4) if total else None,
        "median_pct_chg": round(float(panel["pct_chg"].median(skipna=True)), 2) if total else None,
        "up_gt_3_count": int((panel["pct_chg"] >= 3).sum()),
        "up_gt_5_count": int((panel["pct_chg"] >= 5).sum()),
        "down_lt_minus_3_count": int((panel["pct_chg"] <= -3).sum()),
        "down_lt_minus_5_count": int((panel["pct_chg"] <= -5).sum()),
        "limit_up_count": limit_up_count,
        "limit_down_count": limit_down_count,
        "limit_detection": limit_detection,
        "total_amount": round(total_amount, 2),
        "total_amount_100m_yuan": round(total_amount / 100000, 2),
        "amount_unit": "thousand_yuan",
        "up_amount_ratio": round(up_amount / total_amount, 4) if total_amount else None,
        "down_amount_ratio": round(down_amount / total_amount, 4) if total_amount else None,
        "top50_amount_ratio": round(top50_amount / total_amount, 4) if total_amount else None,
        "index": index_summary,
    }


def calculate_market_turnover_rate(daily: pd.DataFrame, daily_basic: pd.DataFrame, target_date: str) -> Tuple[Optional[float], Optional[str]]:
    """Calculate full-market turnover rate using amount / circulating market value."""
    if daily is None or daily.empty:
        return None, "daily data is empty"
    if daily_basic is None or daily_basic.empty:
        return None, "daily_basic data is empty"

    daily_day = daily.loc[daily["trade_date"].astype(str) == str(target_date)].copy()
    basic_day = daily_basic.loc[daily_basic["trade_date"].astype(str) == str(target_date)].copy()
    if daily_day.empty:
        return None, f"daily data missing target date {target_date}"
    if basic_day.empty:
        return None, f"daily_basic data missing target date {target_date}"
    if "amount" not in daily_day.columns:
        return None, "daily data missing amount column"
    if "circ_mv" not in basic_day.columns:
        return None, "daily_basic data missing circ_mv column"

    amount = pd.to_numeric(daily_day["amount"], errors="coerce")
    circ_mv = pd.to_numeric(basic_day["circ_mv"], errors="coerce")
    total_amount_thousand_yuan = amount[amount > 0].sum(min_count=1)
    total_circ_mv_10k_yuan = circ_mv[circ_mv > 0].sum(min_count=1)

    if pd.isna(total_amount_thousand_yuan) or float(total_amount_thousand_yuan) <= 0:
        return None, "daily amount has no positive values"
    if pd.isna(total_circ_mv_10k_yuan) or float(total_circ_mv_10k_yuan) <= 0:
        return None, "daily_basic circ_mv has no positive values"

    turnover_rate = (float(total_amount_thousand_yuan) * 1000.0) / (float(total_circ_mv_10k_yuan) * 10000.0) * 100.0
    return round(turnover_rate, 4), None


def fetch_margin_net_buy(
    pro,
    target_date: str,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Tuple[Optional[float], Optional[str]]:
    """Return market-wide financing net buy (rzmre - rzche), in yuan."""
    fields = "trade_date,exchange_id,rzmre,rzche"
    if cache_enabled and not refresh_cache:
        cached = read_cached_frame("margin", target_date, fields)
        if cached is not None:
            margin = cached
        else:
            margin = None
    else:
        margin = None

    try:
        if margin is None:
            margin = pro.margin(trade_date=target_date, fields=fields)
            if margin is not None and not margin.empty and cache_enabled:
                write_cached_frame("margin", target_date, margin)
    except Exception as exc:
        return None, f"tushare margin failed for {target_date}: {exc}"

    if margin is None or margin.empty:
        return None, f"tushare margin returned no data for {target_date}"
    if "rzmre" not in margin.columns or "rzche" not in margin.columns:
        return None, "tushare margin missing rzmre/rzche columns"

    buy = pd.to_numeric(margin["rzmre"], errors="coerce")
    repay = pd.to_numeric(margin["rzche"], errors="coerce")
    net_buy = (buy - repay).sum(min_count=1)
    if pd.isna(net_buy):
        return None, "tushare margin rzmre/rzche has no numeric values"
    return round(float(net_buy), 2), None


def format_history_date(trade_date: str) -> str:
    normalized = history_date_to_trade_date(trade_date)
    if not normalized:
        return str(trade_date)
    return datetime.strptime(normalized, "%Y%m%d").strftime("%Y/%m/%d")


def history_date_to_trade_date(value: Any) -> Optional[str]:
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y%m%d")


def is_blank_value(value: object) -> bool:
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return str(value).strip() == ""


def safe_int(value: Any) -> Optional[int]:
    """Safely convert a value to int, returning None on failure."""
    if is_blank_value(value):
        return None
    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        return None


LIMIT_PCT_MAIN = 0.10
LIMIT_PCT_MAIN_ST = 0.05
LIMIT_PCT_GROWTH = 0.20
LIMIT_PCT_BSE = 0.30


def classify_limit_pct(ts_code: Any, name: Any, market: Any) -> float:
    """Return the price-limit percentage for one stock by board rules.

    主板 ±10%（ST/*ST ±5%）；创业板/科创板 ±20%（含 ST）；北交所 ±30%。
    B 股按主板规则处理。新股上市初期的无涨跌幅阶段无需特判：那些交易日的
    收盘价不会落在按本限幅计算出的涨跌停价上，自然不会被计入。
    """
    code = str(ts_code or "")
    market_text = str(market or "")
    if code.endswith(".BJ") or market_text == "北交所":
        return LIMIT_PCT_BSE
    if market_text in ("创业板", "科创板") or code.startswith(("300", "301", "302", "688", "689")):
        return LIMIT_PCT_GROWTH
    if "ST" in str(name or "").upper():
        return LIMIT_PCT_MAIN_ST
    return LIMIT_PCT_MAIN


def exchange_round_to_fen(prices: pd.Series) -> pd.Series:
    """涨跌停价按交易所口径四舍五入到分（half-up；epsilon 抵消二进制浮点误差）。"""
    return (prices * 100 + 0.5 + 1e-7) // 1 / 100


def compute_limit_flags(daily: pd.DataFrame, stock_basic: pd.DataFrame) -> pd.DataFrame:
    """Exact per-(ts_code, trade_date) limit-up/down flags from raw daily bars.

    交易所规则：涨/跌停价 = 前收盘 ×(1±板块限幅) 四舍五入到分，收盘价等于该价
    即收盘封板（不含盘中触板回落）。必须用未复权的 close/pre_close——qfq 重标
    价格后分位比对即失效，所以本函数要在 apply_qfq_adjustment 之前调用。
    """
    columns = ["ts_code", "trade_date", "limit_pct", "is_limit_up", "is_limit_down"]
    if daily is None or daily.empty or not {"close", "pre_close"}.issubset(daily.columns):
        return pd.DataFrame(columns=columns)

    df = daily[["ts_code", "trade_date", "close", "pre_close"]].copy()
    df["ts_code"] = df["ts_code"].astype(str)
    df["trade_date"] = df["trade_date"].astype(str)
    for column in ("close", "pre_close"):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    name_map: Dict[str, str] = {}
    market_map: Dict[str, str] = {}
    if stock_basic is not None and not stock_basic.empty and "ts_code" in stock_basic.columns:
        basics = stock_basic.copy()
        basics["ts_code"] = basics["ts_code"].astype(str)
        if "name" in basics.columns:
            name_map = dict(zip(basics["ts_code"], basics["name"].fillna("")))
        if "market" in basics.columns:
            market_map = dict(zip(basics["ts_code"], basics["market"].fillna("")))

    codes = df["ts_code"]
    names = codes.map(name_map).fillna("").astype(str)
    markets = codes.map(market_map).fillna("").astype(str)

    # 向量化限幅映射，覆写顺序与 classify_limit_pct 的判定优先级一致：
    # 默认主板 10% → ST 5% → 创业/科创 20%（含 ST）→ 北交所 30%。
    limit_pct = pd.Series(LIMIT_PCT_MAIN, index=df.index)
    limit_pct[names.str.upper().str.contains("ST", na=False)] = LIMIT_PCT_MAIN_ST
    growth = markets.isin(["创业板", "科创板"]) | codes.str.startswith(("300", "301", "302", "688", "689"))
    limit_pct[growth] = LIMIT_PCT_GROWTH
    limit_pct[codes.str.endswith(".BJ") | markets.eq("北交所")] = LIMIT_PCT_BSE
    df["limit_pct"] = limit_pct

    up_price = exchange_round_to_fen(df["pre_close"] * (1 + limit_pct))
    down_price = exchange_round_to_fen(df["pre_close"] * (1 - limit_pct))
    valid = df["close"].notna() & df["pre_close"].notna() & (df["pre_close"] > 0)
    df["is_limit_up"] = valid & (df["close"] - up_price).abs().lt(0.001)
    df["is_limit_down"] = valid & (df["close"] - down_price).abs().lt(0.001)

    # 主板 ST 双档判定：退市整理期等特殊阶段的 ST 股执行 10% 而非 5%
    # （实测 20260609 的 *ST阳光/*ST太和 收盘精确封在 10% 档）。受 5% 限制
    # 的股票价格物理上到不了 10% 档价，所以补判 10% 档不会误伤正常 ST。
    st_main = limit_pct.eq(LIMIT_PCT_MAIN_ST)
    if st_main.any():
        alt_up = exchange_round_to_fen(df["pre_close"] * (1 + LIMIT_PCT_MAIN))
        alt_down = exchange_round_to_fen(df["pre_close"] * (1 - LIMIT_PCT_MAIN))
        df["is_limit_up"] = df["is_limit_up"] | (valid & st_main & (df["close"] - alt_up).abs().lt(0.001))
        df["is_limit_down"] = df["is_limit_down"] | (valid & st_main & (df["close"] - alt_down).abs().lt(0.001))
    return df[columns]


def calc_market_sentiment(
    up: int,
    down: int,
    flat: int,
    limit_up: int,
    limit_down: int,
    zt_weight: float = 1.5,
    dt_weight: float = 3.0,
) -> float:
    """Calculate market sentiment value with limit-up/down weighting.

    Based on regression fitting against 88 historical records from
    legulegu.com.  MAE≈0.85, R²≈0.996.

    Logic:
      - Normal up/down have weight 1.0
      - Limit-up gets extra weight (default 1.5x) reflecting strong
        buying attack intent.
      - Limit-down gets even higher weight (default 3.0x) reflecting
        panic contagion (loss aversion in behavioral finance).

    Args:
        up: Number of rising stocks (including limit-up).
        down: Number of falling stocks (including limit-down).
        flat: Number of flat stocks.
        limit_up: Number of limit-up stocks.
        limit_down: Number of limit-down stocks.
        zt_weight: Weight multiplier for limit-up vs normal up.
        dt_weight: Weight multiplier for limit-down vs normal down.

    Returns:
        Sentiment value in range 0~100.
    """
    normal_up = up - limit_up
    normal_down = down - limit_down

    weighted_up = normal_up + limit_up * zt_weight
    weighted_down = normal_down + limit_down * dt_weight

    denom = weighted_up + weighted_down + flat
    if denom == 0:
        return 50.0

    sentiment = weighted_up / denom * 100
    return float(max(0.0, min(100.0, sentiment)))


def compute_market_activity_from_daily(
    daily: pd.DataFrame, target_date: str, limit_flags: Optional[pd.DataFrame] = None
) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
    """Compute market activity from Tushare daily data (no external web scraping).

    Up/down/flat counts come from pct_chg sign; limit-up/down counts use the
    exact board-rule flags when provided, falling back to the ±9.8% pct_chg
    approximation only when flags are unavailable.
    """
    detail: Dict[str, Any] = {
        "source": "tushare.daily",
        "available": False,
        "fallback_reason": None,
    }

    if daily is None or daily.empty:
        detail["fallback_reason"] = "daily data is empty"
        return {}, [], detail

    day_df = daily.loc[daily["trade_date"].astype(str) == str(target_date)].copy()
    if day_df.empty:
        detail["fallback_reason"] = f"daily data missing target date {target_date}"
        return {}, [], detail

    day_df["pct_chg"] = pd.to_numeric(day_df["pct_chg"], errors="coerce")
    day_df["amount"] = pd.to_numeric(day_df["amount"], errors="coerce")

    total = int(len(day_df))
    up = int((day_df["pct_chg"] > 0).sum())
    down = int((day_df["pct_chg"] < 0).sum())
    flat = total - up - down
    flags_day = (
        limit_flags.loc[limit_flags["trade_date"].astype(str) == str(target_date)]
        if limit_flags is not None and not limit_flags.empty
        else None
    )
    if flags_day is not None and not flags_day.empty:
        limit_up = int(flags_day["is_limit_up"].sum())
        limit_down = int(flags_day["is_limit_down"].sum())
        detail["limit_detection"] = "board_rule_price_match"
    else:
        limit_up = int((day_df["pct_chg"] >= 9.8).sum())
        limit_down = int((day_df["pct_chg"] <= -9.8).sum())
        detail["limit_detection"] = "pct_chg_approx"
    total_amount = float(day_df["amount"].sum(skipna=True))

    sentiment = calc_market_sentiment(up, down, flat, limit_up, limit_down)

    row: Dict[str, Any] = {
        "日期": format_history_date(target_date),
        "上涨": up,
        "涨停": limit_up,
        "下跌": down,
        "跌停": limit_down,
        "平盘": flat,
        "活跃度": round(sentiment, 2),
        "情绪值": round(sentiment, 2),
        "成交额": round(total_amount, 3) if total_amount > 0 else "",
    }
    columns = list(row.keys())
    detail["available"] = True
    return row, columns, detail


def should_fill_turnover(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False

    new_amount = pd.to_numeric(pd.Series([new_value]), errors="coerce").iloc[0]
    if pd.isna(new_amount) or float(new_amount) <= 0:
        return False

    if is_blank_value(existing_value):
        return True

    existing_amount = pd.to_numeric(pd.Series([existing_value]), errors="coerce").iloc[0]
    return pd.isna(existing_amount) or float(existing_amount) <= 0


def normalize_market_history_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Repair known historical CSV header issues before upserting rows."""
    if df is None or df.empty:
        return df

    out = df.copy()
    if "日期" not in out.columns:
        fixed = list(out.columns)
        if fixed:
            fixed[0] = "日期"
            out.columns = fixed

    for bad_col in CORRUPTED_MARKET_TURNOVER_COLUMNS:
        if bad_col not in out.columns:
            continue
        if "全市场换手率" not in out.columns:
            out = out.rename(columns={bad_col: "全市场换手率"})
            continue
        out["全市场换手率"] = out["全市场换手率"].where(
            ~out["全市场换手率"].apply(is_blank_value),
            out[bad_col],
        )
        out = out.drop(columns=[bad_col])

    return out


def order_market_history_columns(columns: Iterable[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for col in MARKET_HISTORY_COLUMNS:
        if col in columns and col not in seen:
            ordered.append(col)
            seen.add(col)
    for col in columns:
        if col not in seen and col not in CORRUPTED_MARKET_TURNOVER_COLUMNS:
            ordered.append(col)
            seen.add(col)
    return ordered


def sort_market_history_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "日期" not in df.columns:
        return df
    out = df.copy()
    out["_sort_date"] = out["日期"].apply(history_date_to_trade_date)
    out = out.sort_values("_sort_date", ascending=False, na_position="last").drop(columns=["_sort_date"])
    return out.reset_index(drop=True)


def market_history_json_path(csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> Path:
    if csv_path == DEFAULT_MARKET_HISTORY_CSV:
        return DEFAULT_MARKET_HISTORY_JSON
    return csv_path.with_suffix(".json")


def skill_relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(SKILL_ROOT).as_posix()
    except ValueError:
        return str(path)


def clean_market_history_value(column: str, value: Any) -> Any:
    if column == "日期":
        return "" if is_blank_value(value) else str(value)
    return parse_market_history_number(value)


def write_market_history_json(
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
    json_path: Optional[Path] = None,
) -> Path:
    """Write a clean JSON derivative of references/market_data.csv for HTML charts."""
    if json_path is None:
        json_path = market_history_json_path(csv_path)

    if BACKEND == Backend.POSTGRESQL:
        db_to_skill_columns = {
            "date": "日期",
            "rise": "上涨",
            "limit_up": "涨停",
            "fall": "下跌",
            "limit_down": "跌停",
            "flat": "平盘",
            "activity": "活跃度",
            "sentiment": "情绪值",
            "amount": "成交额",
            "margin_net_buy": "融资净买入",
            "turnover_rate": "全市场换手率",
        }
        raw = read_market_history()
        if raw is not None and not raw.empty:
            raw = raw.rename(columns=db_to_skill_columns)
        elif csv_path.exists():
            raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    elif csv_path.exists():
        raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    else:
        raw = pd.DataFrame()

    raw = normalize_market_history_columns(raw)
    if raw is None or raw.empty or "日期" not in raw.columns:
        payload = {
            "metadata": {
                "source_csv": skill_relative_path(csv_path),
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sort": "trade_date_ascending",
            },
            "columns": [],
            "records": [],
            "series": {},
            "quality": {
                "records_available": 0,
                "has_120_records": False,
                "missing_trade_date_rows": 0,
            },
        }
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return json_path

    df = raw.copy()
    df["_trade_date"] = df["日期"].apply(history_date_to_trade_date)
    df = df.sort_values("_trade_date", ascending=True, na_position="last").reset_index(drop=True)
    columns = [col for col in df.columns if col != "_trade_date"]

    records: List[Dict[str, Any]] = []
    numeric_columns: List[str] = []
    for column in columns:
        if column == "日期":
            continue
        cleaned_values = [clean_market_history_value(column, value) for value in df[column].tolist()]
        if any(value is not None for value in cleaned_values):
            numeric_columns.append(column)

    for _, row in df.iterrows():
        record: Dict[str, Any] = {
            "日期": clean_market_history_value("日期", row.get("日期")),
            "trade_date": row.get("_trade_date") or None,
        }
        for column in columns:
            if column == "日期":
                continue
            record[column] = clean_market_history_value(column, row.get(column))
        records.append(record)

    series: Dict[str, List[Dict[str, Any]]] = {}
    for column in numeric_columns:
        points: List[Dict[str, Any]] = []
        for record in records:
            points.append({
                "trade_date": record.get("trade_date"),
                "date": record.get("日期"),
                "value": record.get(column),
            })
        series[column] = points

    valid_trade_dates = [record.get("trade_date") for record in records if record.get("trade_date")]
    payload = {
        "metadata": {
            "source_csv": skill_relative_path(csv_path),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sort": "trade_date_ascending",
            "window_start": valid_trade_dates[0] if valid_trade_dates else None,
            "window_end": valid_trade_dates[-1] if valid_trade_dates else None,
        },
        "columns": columns,
        "records": records,
        "series": series,
        "quality": {
            "records_available": len(records),
            "has_120_records": len(records) >= 120,
            "missing_trade_date_rows": sum(1 for record in records if not record.get("trade_date")),
            "numeric_columns": numeric_columns,
        },
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return json_path


def read_market_history_trade_dates(csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> Set[str]:
    """Return normalized trade dates already present in market history."""
    raw = load_market_history_df(csv_path)
    if raw is None or raw.empty or "日期" not in raw.columns:
        return set()

    return {
        trade_date
        for trade_date in raw["日期"].apply(history_date_to_trade_date).tolist()
        if trade_date
    }


def load_market_history_df(csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> pd.DataFrame:
    """Load market history in skill-column shape from DB or CSV."""
    if BACKEND == Backend.POSTGRESQL:
        raw = read_market_history()
        if raw is not None and not raw.empty:
            raw = raw.rename(columns={value: key for key, value in MARKET_HISTORY_DB_COLUMNS.items()})
    elif csv_path.exists():
        raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    else:
        raw = pd.DataFrame()

    raw = normalize_market_history_columns(raw)
    if raw is None or raw.empty:
        return pd.DataFrame()

    if "日期" in raw.columns:
        raw["日期"] = raw["日期"].apply(
            lambda value: format_history_date(history_date_to_trade_date(value))
            if history_date_to_trade_date(value)
            else value
        )
    return raw


def should_update_market_history_field(column: str, current_value: object, new_value: object) -> bool:
    if column == "成交额":
        return should_fill_turnover(current_value, new_value)
    if column == "全市场换手率":
        return should_fill_positive_numeric(current_value, new_value)
    if column in {"情绪值", "融资净买入"}:
        return should_update_numeric(current_value, new_value)
    if column in {"涨停", "跌停", "上涨", "下跌", "平盘"}:
        return should_update_count(current_value, new_value)
    return is_blank_value(current_value) and not is_blank_value(new_value)


def merge_market_history_row(df: pd.DataFrame, row: Dict[str, Any], columns: List[str]) -> pd.DataFrame:
    """Merge one market-history row into an already-loaded history frame."""
    ordered_columns = order_market_history_columns(list(dict.fromkeys(columns + list(row.keys()))))
    if df is None or df.empty:
        return sort_market_history_df(pd.DataFrame([row], columns=ordered_columns))

    current_columns = order_market_history_columns(
        list(df.columns) + [col for col in ordered_columns if col in MARKET_HISTORY_COLUMNS]
    )
    row = {key: value for key, value in row.items() if key in current_columns}

    for col in current_columns:
        if col not in df.columns:
            df[col] = ""
    df = df.reindex(columns=current_columns).copy()

    target_date = row.get("日期")
    existing_dates = df["日期"].apply(history_date_to_trade_date)
    target_key = history_date_to_trade_date(target_date)
    matches = df.index[existing_dates == target_key] if target_key else df.index[df["日期"] == target_date]
    if len(matches) > 0:
        idx = matches[0]
        for col, new_value in row.items():
            if col == "日期":
                continue
            if should_update_market_history_field(col, df.at[idx, col], new_value):
                df.at[idx, col] = new_value
        return sort_market_history_df(df)

    final_columns = order_market_history_columns(list(df.columns) + [col for col in ordered_columns if col not in df.columns])
    new_row = pd.DataFrame([row], columns=final_columns)
    return sort_market_history_df(pd.concat([new_row, df.reindex(columns=final_columns)], ignore_index=True))


def verify_market_history_dates_in_frame(df: pd.DataFrame, target_dates: Iterable[Any]) -> None:
    if df is None or df.empty or "日期" not in df.columns:
        raise RuntimeError("market history write verification failed: 日期 column missing")
    existing_dates = set(df["日期"].apply(history_date_to_trade_date).dropna().tolist())
    missing = [
        str(target_date)
        for target_date in target_dates
        if history_date_to_trade_date(target_date) not in existing_dates
    ]
    if missing:
        raise RuntimeError(f"market history write verification failed: missing dates {','.join(missing)}")


def write_market_history_df(df: pd.DataFrame, csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> None:
    """Persist a full market-history frame once, then refresh derived JSON once."""
    final_df = sort_market_history_df(df)
    if BACKEND == Backend.POSTGRESQL:
        db_df = pd.DataFrame()
        for source_column, db_column in MARKET_HISTORY_DB_COLUMNS.items():
            if source_column not in final_df.columns:
                continue
            if source_column == "日期":
                db_df[db_column] = final_df[source_column].apply(
                    lambda value: (
                        datetime.strptime(history_date_to_trade_date(value), "%Y%m%d").strftime("%Y-%m-%d")
                        if history_date_to_trade_date(value)
                        else None
                    )
                )
            else:
                db_df[db_column] = final_df[source_column].apply(lambda value: clean_market_history_value(source_column, value))
        if not db_df.empty and "date" in db_df.columns:
            db_df = db_df.dropna(subset=["date"])
            write_market_history(db_df)
            write_market_history_json(csv_path)
        return

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    write_market_history_json(csv_path)


def upsert_market_history_rows(
    rows: List[Tuple[Dict[str, Any], List[str]]],
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> None:
    """Write multiple market-history rows with one load/save/JSON refresh."""
    if not rows:
        return
    df = load_market_history_df(csv_path)
    target_dates: List[Any] = []
    for row, columns in rows:
        target_dates.append(row.get("日期"))
        df = merge_market_history_row(df, row, columns)
    verify_market_history_dates_in_frame(df, target_dates)
    write_market_history_df(df, csv_path)


def upsert_market_history_row(
    row: Dict[str, Any],
    columns: List[str],
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> None:
    """Write one market-history row while preserving existing non-empty values."""
    upsert_market_history_rows([(row, columns)], csv_path=csv_path)


def should_fill_positive_numeric(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False

    new_numeric = pd.to_numeric(pd.Series([new_value]), errors="coerce").iloc[0]
    if pd.isna(new_numeric) or float(new_numeric) <= 0:
        return False

    if is_blank_value(existing_value):
        return True

    existing_numeric = pd.to_numeric(pd.Series([existing_value]), errors="coerce").iloc[0]
    return pd.isna(existing_numeric) or float(existing_numeric) <= 0


def should_update_count(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False
    new_numeric = pd.to_numeric(pd.Series([new_value]), errors="coerce").iloc[0]
    if pd.isna(new_numeric) or float(new_numeric) < 0:
        return False
    if is_blank_value(existing_value):
        return True
    existing_numeric = pd.to_numeric(pd.Series([existing_value]), errors="coerce").iloc[0]
    return pd.isna(existing_numeric) or int(existing_numeric) != int(new_numeric)


def should_update_numeric(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False
    new_numeric = parse_market_history_number(new_value)
    if new_numeric is None:
        return False
    if is_blank_value(existing_value):
        return True
    existing_numeric = parse_market_history_number(existing_value)
    return existing_numeric is None or float(existing_numeric) != float(new_numeric)


class SimpleTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_parts: List[str] = []
        self.current_row: List[str] = []
        self.rows: List[List[str]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag == "table":
            self.in_table = True
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in {"td", "th"}:
            self.in_cell = True
            self.cell_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self.in_cell:
            self.current_row.append("".join(self.cell_parts).strip())
            self.in_cell = False
            self.cell_parts = []
        elif tag == "tr" and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)
            self.in_row = False
            self.current_row = []
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_parts.append(data)


def parse_market_history_number(value: Any) -> Optional[float]:
    if is_blank_value(value):
        return None
    text = str(value).strip().replace(",", "").replace("%", "")
    if text in {"--", "-", "—"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def fetch_sohu_market_history_rows(year: str) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
    detail: Dict[str, Any] = {
        "source": MARKET_HISTORY_SOHU_SOURCE,
        "url": SOHU_LIMIT_HISTORY_URL,
        "available": False,
        "fallback_reason": None,
    }
    if requests is None:
        detail["fallback_reason"] = "requests is not installed"
        return {}, detail

    try:
        response = requests.get(
            SOHU_LIMIT_HISTORY_URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )
        response.raise_for_status()
    except Exception as exc:
        detail["fallback_reason"] = f"sohu zdt history request failed: {exc}"
        return {}, detail

    text = response.content.decode("utf-8", errors="replace")
    parser = SimpleTableParser()
    parser.feed(text)

    rows: Dict[str, Dict[str, Any]] = {}
    for cells in parser.rows:
        if len(cells) < 14 or "/" not in cells[0]:
            continue

        values = [parse_market_history_number(cell) for cell in cells]
        amount_100m_yuan = values[4]
        up_count = sum(v for v in [values[5], values[8], values[11]] if v is not None)
        flat_count = sum(v for v in [values[6], values[9], values[12]] if v is not None)
        down_count = sum(v for v in [values[7], values[10], values[13]] if v is not None)
        trade_date = history_date_to_trade_date(f"{year}/{cells[0]}")
        if not trade_date:
            continue
        rows[trade_date] = {
            "日期": f"{year}/{cells[0]}",
            "上涨": int(up_count),
            "涨停": int(values[1]) if values[1] is not None else "",
            "下跌": int(down_count),
            "跌停": int(values[2]) if values[2] is not None else "",
            "平盘": int(flat_count),
            "成交额": round(float(amount_100m_yuan) * 100000, 3) if amount_100m_yuan is not None else "",
        }

    if rows:
        detail["available"] = True
        detail["row_count"] = len(rows)
    else:
        detail["fallback_reason"] = "sohu zdt history table has no usable rows"
    return rows, detail


def fetch_sohu_market_history_row(target_date: str) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
    detail: Dict[str, Any] = {
        "source": MARKET_HISTORY_SOHU_SOURCE,
        "url": SOHU_LIMIT_HISTORY_URL,
        "available": False,
        "fallback_reason": None,
    }
    year = str(target_date)[:4]
    if year not in SOHU_LIMIT_HISTORY_CACHE:
        rows, detail = fetch_sohu_market_history_rows(year)
        if not detail.get("available"):
            return {}, [], detail
        SOHU_LIMIT_HISTORY_CACHE[year] = rows

    row = SOHU_LIMIT_HISTORY_CACHE[year].get(target_date, {})
    if not row:
        detail["fallback_reason"] = f"sohu zdt history missing target date {target_date}"
        return {}, [], detail

    detail["available"] = True
    detail["matched_date"] = target_date
    return row, list(row.keys()), detail


def fill_missing_market_activity(
    row: Dict[str, Any],
    columns: List[str],
    fallback_row: Dict[str, Any],
    fallback_columns: List[str],
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    filled: List[str] = []
    if not fallback_row:
        return row, columns, filled

    if not row:
        row = {"日期": fallback_row.get("日期")}
        columns = ["日期"]

    for key in MARKET_ACTIVITY_COLUMNS:
        if key not in fallback_row:
            continue
        if key not in row or is_blank_value(row.get(key)):
            row[key] = fallback_row[key]
            filled.append(key)

    columns = list(dict.fromkeys(columns + [col for col in fallback_columns if col in row]))
    return row, columns, filled


def update_market_history(
    target_date: str,
    daily: pd.DataFrame,
    daily_basic: Optional[pd.DataFrame] = None,
    margin_net_buy: Optional[float] = None,
    margin_net_buy_reason: Optional[str] = None,
    margin_net_buy_trade_date: Optional[str] = None,
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
    defer_write: bool = False,
    limit_flags: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    # Primary: compute from Tushare daily data (no external web scraping)
    row, columns, detail = compute_market_activity_from_daily(daily, target_date, limit_flags=limit_flags)

    # Fallback: sohu zdt history when Tushare daily is unavailable
    needs_sohu = not detail.get("available")
    sohu_row: Dict[str, Any] = {}
    sohu_columns: List[str] = []
    sohu_detail: Dict[str, Any] = {"available": False, "fallback_reason": "not needed"}
    sohu_filled_fields: List[str] = []
    if needs_sohu:
        sohu_row, sohu_columns, sohu_detail = fetch_sohu_market_history_row(target_date)
        row, columns, sohu_filled_fields = fill_missing_market_activity(row, columns, sohu_row, sohu_columns)

    # If sohu has counts but no sentiment, compute it with V4 formula
    if sohu_detail.get("available") and (
        is_blank_value(row.get("情绪值")) or is_blank_value(row.get("活跃度"))
    ):
        up_val = safe_int(row.get("上涨"))
        down_val = safe_int(row.get("下跌"))
        flat_val = safe_int(row.get("平盘"))
        if up_val is not None and down_val is not None and flat_val is not None:
            limit_up_val = safe_int(row.get("涨停")) or 0
            limit_down_val = safe_int(row.get("跌停")) or 0
            sentiment = calc_market_sentiment(up_val, down_val, flat_val, limit_up_val, limit_down_val)
            row["情绪值"] = round(sentiment, 2)
            row["活跃度"] = round(sentiment, 2)
            for key in ("情绪值", "活跃度"):
                if key not in columns:
                    columns.append(key)

    market_turnover_rate, market_turnover_reason = calculate_market_turnover_rate(
        daily,
        daily_basic if daily_basic is not None else pd.DataFrame(),
        target_date,
    )

    fallback_reason = detail.get("fallback_reason")
    if not row:
        row = {"日期": format_history_date(target_date)}
        columns = ["日期"]

    if market_turnover_rate is not None:
        row["全市场换手率"] = market_turnover_rate
    if "全市场换手率" not in columns:
        columns.append("全市场换手率")

    if margin_net_buy is not None:
        row["融资净买入"] = margin_net_buy
    if "融资净买入" not in columns:
        columns.append("融资净买入")

    confirmed_values = {
        key: value for key, value in row.items() if key != "日期" and not is_blank_value(value)
    }
    result: Dict[str, Any] = {
        "updated": False,
        "trade_date": target_date,
        "path": str(csv_path),
        "json_path": str(market_history_json_path(csv_path)),
        "primary_source": MARKET_HISTORY_PRIMARY_SOURCE,
        "sohu_source": MARKET_HISTORY_SOHU_SOURCE,
        "supplement_source": MARKET_HISTORY_SUPPLEMENT_SOURCE,
        "primary_trade_date": target_date,
        "sohu_available": bool(sohu_detail.get("available")),
        "sohu_fallback_reason": sohu_detail.get("fallback_reason"),
        "sohu_filled_fields": sohu_filled_fields,
        "limit_detection": detail.get("limit_detection"),
        "fallback_reason": fallback_reason,
        "market_turnover_rate": market_turnover_rate,
        "market_turnover_rate_unit": "percent",
        "market_turnover_rate_reason": market_turnover_reason,
        "margin_net_buy": margin_net_buy,
        "margin_net_buy_unit": "yuan",
        "margin_net_buy_trade_date": margin_net_buy_trade_date,
        "margin_net_buy_reason": margin_net_buy_reason,
        "fields": sorted(confirmed_values.keys()),
    }
    if not confirmed_values:
        result["fallback_reason"] = fallback_reason or "no confirmed market history fields from tushare.daily or sohu"
        return result

    if defer_write:
        result["updated"] = True
        result["_market_history_row"] = row
        result["_market_history_columns"] = columns
        return result

    try:
        upsert_market_history_row(row, columns, csv_path=csv_path)
    except Exception as exc:
        result["fallback_reason"] = f"failed to update market history csv: {exc}"
        return result

    result["updated"] = True
    return result


def market_history_backfill_dates(
    target_date: str,
    trade_dates: Iterable[str],
    existing_dates: Set[str],
) -> List[str]:
    """Find missing market-history rows between the previous stored date and target."""
    ordered_dates = sorted({str(date) for date in trade_dates if str(date) <= target_date})
    if not ordered_dates:
        return [target_date]

    previous_existing = max((date for date in existing_dates if date < target_date), default=None)
    if previous_existing:
        candidates = [date for date in ordered_dates if previous_existing < date <= target_date]
    else:
        candidates = [target_date]

    dates = [date for date in candidates if date not in existing_dates or date == target_date]
    if target_date not in dates:
        dates.append(target_date)
    return sorted(set(dates))


def update_market_history_window(
    target_date: str,
    trade_dates: Iterable[str],
    daily: pd.DataFrame,
    daily_basic: Optional[pd.DataFrame] = None,
    pro: Any = None,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
    margin_net_buy: Optional[float] = None,
    margin_net_buy_reason: Optional[str] = None,
    margin_net_buy_trade_date: Optional[str] = None,
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
    limit_flags: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """Update target day and fill recent market-history gaps visible in charts."""
    ordered_trade_dates = sorted({str(date) for date in trade_dates if str(date) <= target_date})
    previous_by_date = {
        date: ordered_trade_dates[idx - 1] if idx > 0 else None
        for idx, date in enumerate(ordered_trade_dates)
    }

    try:
        existing_dates = read_market_history_trade_dates(csv_path)
        dates_to_update = market_history_backfill_dates(target_date, ordered_trade_dates, existing_dates)
    except Exception as exc:
        dates_to_update = [target_date]
        backfill_error = f"failed to inspect existing market history: {exc}"
    else:
        backfill_error = None

    target_result: Optional[Dict[str, Any]] = None
    backfill_updates: List[Dict[str, Any]] = []
    pending_rows: List[Tuple[Dict[str, Any], List[str]]] = []
    for trade_date in dates_to_update:
        if trade_date == target_date:
            row_margin = margin_net_buy
            row_margin_reason = margin_net_buy_reason
            row_margin_trade_date = margin_net_buy_trade_date
        else:
            row_margin = None
            row_margin_reason = "not requested for backfill"
            row_margin_trade_date = previous_by_date.get(trade_date)
            if pro is not None and row_margin_trade_date:
                row_margin, row_margin_reason = fetch_margin_net_buy(
                    pro,
                    row_margin_trade_date,
                    cache_enabled=cache_enabled,
                    refresh_cache=refresh_cache,
                )

        result = update_market_history(
            trade_date,
            daily,
            daily_basic,
            margin_net_buy=row_margin,
            margin_net_buy_reason=row_margin_reason,
            margin_net_buy_trade_date=row_margin_trade_date,
            csv_path=csv_path,
            defer_write=True,
            limit_flags=limit_flags,
        )
        pending_row = result.pop("_market_history_row", None)
        pending_columns = result.pop("_market_history_columns", None)
        if pending_row is not None and pending_columns is not None:
            pending_rows.append((pending_row, pending_columns))
        if trade_date == target_date:
            target_result = result
        else:
            backfill_updates.append(result)

    try:
        upsert_market_history_rows(pending_rows, csv_path=csv_path)
    except Exception as exc:
        message = f"failed to update market history csv: {exc}"
        if target_result is not None:
            target_result["updated"] = False
            target_result["fallback_reason"] = message
        for item in backfill_updates:
            if item.get("updated"):
                item["updated"] = False
                item["fallback_reason"] = message

    if target_result is None:
        target_result = {
            "updated": False,
            "trade_date": target_date,
            "path": str(csv_path),
            "json_path": str(market_history_json_path(csv_path)),
            "fallback_reason": "target date was not updated",
        }

    target_result["backfill_trade_dates"] = [item.get("trade_date") for item in backfill_updates]
    target_result["backfill_updates"] = backfill_updates
    if backfill_error:
        target_result["backfill_reason"] = backfill_error
    return target_result


def build_limit_stats(limit_df: pd.DataFrame) -> Dict[str, Any]:
    if limit_df is None or limit_df.empty:
        return {"available": False}
    result: Dict[str, Any] = {"available": True, "row_count": int(len(limit_df))}
    for column in ("limit", "limit_type", "status", "open_times"):
        if column in limit_df.columns:
            counts = limit_df[column].fillna("NA").astype(str).value_counts().head(20)
            result[f"{column}_counts"] = counts.to_dict()
            if column == "limit":
                result["limit_up_count"] = int(counts.get("U", 0))
                result["limit_down_count"] = int(counts.get("D", 0))
                result["limit_open_or_broken_count"] = int(counts.get("Z", 0))
    return result


def compare_scalar(current: Any, previous: Any) -> Dict[str, Any]:
    current_float = safe_float(current)
    previous_float = safe_float(previous)
    change = None
    change_pct = None
    if current_float is not None and previous_float is not None:
        change = round(current_float - previous_float, 4)
        if previous_float != 0:
            change_pct = round(change / previous_float * 100.0, 2)
    return {
        "current": nullable_value(current),
        "previous": nullable_value(previous),
        "change": change,
        "change_pct": change_pct,
    }


def build_temperature_comparison(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    fields = [
        "stock_count",
        "up_count",
        "down_count",
        "up_ratio",
        "median_pct_chg",
        "up_gt_3_count",
        "up_gt_5_count",
        "down_lt_minus_3_count",
        "down_lt_minus_5_count",
        "limit_up_count",
        "limit_down_count",
        "total_amount_100m_yuan",
        "up_amount_ratio",
        "down_amount_ratio",
        "top50_amount_ratio",
    ]
    return {field: compare_scalar(current.get(field), previous.get(field)) for field in fields}


def build_limit_comparison(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    fields = ["row_count", "limit_up_count", "limit_down_count", "limit_open_or_broken_count"]
    return {field: compare_scalar(current.get(field), previous.get(field)) for field in fields}


def build_amount_concentration(
    features: pd.DataFrame,
    target_date: str,
    previous_trade_date: Optional[str],
    sample_features: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """Summarize market-wide amount concentration without assigning themes."""
    if features is None or features.empty:
        return {}

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Slice the full-market frame once per date instead of re-scanning all
    # rows for every ratio request (current + previous + 10-day series).
    frames_by_date: Dict[str, pd.DataFrame] = {str(date): frame for date, frame in df.groupby("trade_date")}

    def ratios_for_date(trade_date: str) -> Dict[str, Any]:
        day = frames_by_date.get(str(trade_date))
        if day is None:
            day = df.iloc[0:0]
        total = float(day["amount"].sum(skipna=True))
        result: Dict[str, Any] = {
            "trade_date": trade_date,
            "total_amount_100m_yuan": round(total / 100000, 2) if total else None,
        }
        for n in (10, 20, 50, 100):
            top_amount = float(day.nlargest(min(n, len(day)), "amount")["amount"].sum(skipna=True)) if total else 0.0
            result[f"top{n}_amount_ratio"] = round(top_amount / total, 4) if total else None
        return result

    current = ratios_for_date(target_date)
    previous = ratios_for_date(previous_trade_date) if previous_trade_date else {}

    series: List[Dict[str, Any]] = []
    for trade_date in sorted(frames_by_date.keys())[-10:]:
        series.append(ratios_for_date(trade_date))

    top50_values = [item.get("top50_amount_ratio") for item in series if item.get("top50_amount_ratio") is not None]
    top50_change_10d = None
    top50_up_days = None
    if len(top50_values) >= 2:
        top50_change_10d = round(top50_values[-1] - top50_values[0], 4)
        top50_up_days = sum(1 for prev, cur in zip(top50_values, top50_values[1:]) if cur > prev)

    trend = {
        "top50_change_over_series": top50_change_10d,
        "top50_up_days_in_series": top50_up_days,
        "series_length": len(series),
    }

    day = frames_by_date.get(str(target_date), df.iloc[0:0]).copy()
    top_amount_samples = day.nlargest(min(20, len(day)), "amount")
    if sample_features is not None and not sample_features.empty and not top_amount_samples.empty:
        enriched = sample_features.copy()
        enriched["trade_date"] = enriched["trade_date"].astype(str)
        enriched = enriched.loc[
            (enriched["trade_date"] == target_date)
            & (enriched["ts_code"].isin(top_amount_samples["ts_code"]))
        ].copy()
        if not enriched.empty:
            order = {code: idx for idx, code in enumerate(top_amount_samples["ts_code"].tolist())}
            enriched["_amount_rank"] = enriched["ts_code"].map(order)
            top_amount_samples = enriched.sort_values("_amount_rank").drop(columns=["_amount_rank"])
    top_cols = [
        "ts_code",
        "name",
        "market",
        "trade_date",
        "close",
        "pct_chg",
        "ret_3d",
        "ret_5d",
        "amount",
        "amount_ratio_20d",
    ]
    top_cols = [col for col in top_cols if col in top_amount_samples.columns]
    for col in top_cols:
        if col not in {"ts_code", "name", "market", "trade_date"}:
            top_amount_samples[col] = pd.to_numeric(top_amount_samples[col], errors="coerce").round(4)

    return {
        "current": current,
        "previous": previous,
        "change": {
            key: compare_scalar(current.get(key), previous.get(key))
            for key in (
                "top10_amount_ratio",
                "top20_amount_ratio",
                "top50_amount_ratio",
                "top100_amount_ratio",
                "total_amount_100m_yuan",
            )
            if previous
        },
        "recent_series": series,
        "trend": trend,
        "top_amount_samples": top_amount_samples[top_cols].astype(object).where(pd.notnull(top_amount_samples[top_cols]), None).to_dict(orient="records"),
    }


def round_optional(value: Any, digits: int = 2) -> Optional[float]:
    numeric = safe_float(value)
    if numeric is None:
        return None
    return round(numeric, digits)


def pct_change_optional(current: Any, base: Any) -> Optional[float]:
    current_float = safe_float(current)
    base_float = safe_float(base)
    if current_float is None or base_float in (None, 0):
        return None
    return round((current_float / base_float - 1.0) * 100.0, 2)


def parse_numeric_text_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce",
    )


def classify_ma_alignment(close: Any, ma5: Any, ma20: Any, ma60: Any) -> Optional[str]:
    values = [safe_float(item) for item in (close, ma5, ma20, ma60)]
    if any(item is None for item in values):
        return None
    close_v, ma5_v, ma20_v, ma60_v = values
    if close_v > ma5_v > ma20_v > ma60_v:
        return "bullish_alignment"
    if close_v < ma5_v < ma20_v < ma60_v:
        return "bearish_alignment"
    if close_v >= ma20_v and ma20_v >= ma60_v:
        return "medium_term_positive"
    if close_v < ma20_v and ma20_v < ma60_v:
        return "medium_term_negative"
    return "mixed_alignment"


def classify_price_volume_state(ret_1d: Any, amount_ratio_20d: Any) -> Optional[str]:
    ret = safe_float(ret_1d)
    amount_ratio = safe_float(amount_ratio_20d)
    if ret is None or amount_ratio is None:
        return None
    if ret > 0 and amount_ratio >= 1.2:
        return "up_volume_expansion"
    if ret > 0 and amount_ratio <= 0.8:
        return "up_volume_contraction"
    if ret < 0 and amount_ratio >= 1.2:
        return "down_volume_expansion"
    if ret < 0 and amount_ratio <= 0.8:
        return "down_volume_contraction"
    return "neutral_volume"


def classify_index_trend_stage(close: Any, ma20: Any, ma60: Any, ret_20d: Any, ret_60d: Any) -> Optional[str]:
    close_v = safe_float(close)
    ma20_v = safe_float(ma20)
    ma60_v = safe_float(ma60)
    ret20_v = safe_float(ret_20d)
    ret60_v = safe_float(ret_60d)
    if any(item is None for item in (close_v, ma20_v, ma60_v, ret20_v, ret60_v)):
        return None
    if close_v > ma20_v > ma60_v and ret20_v > 0 and ret60_v > 0:
        return "uptrend"
    if close_v < ma20_v < ma60_v and ret20_v < 0:
        return "breakdown"
    if close_v >= ma60_v and close_v < ma20_v and ret20_v < 0:
        return "pullback"
    if close_v > ma20_v and ret20_v > 0 and ret60_v <= 0:
        return "breakdown_repair"
    if abs(ret20_v) <= 2.0:
        return "sideways"
    return "mixed"


def build_level(label: str, value: Any) -> Dict[str, Any]:
    return {"label": label, "value": round_optional(value, 2)}


def _unavailable_index_summary(
    name: Any,
    code_field: str,
    code_value: Any,
    reason: str,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    result = {
        "available": False,
        "name": name,
        code_field: code_value,
        "reason": reason,
    }
    if extra:
        result.update(extra)
    return result


def _prepare_index_summary_frames(
    daily: pd.DataFrame,
    target_date: str,
    trend_days: int,
    kline_days: Optional[int] = None,
    with_series: bool = False,
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], str]:
    if daily is None or daily.empty:
        return None, None, "index_daily returned no data"

    df = daily.copy()
    if "trade_date" not in df.columns:
        return None, None, "trade_date column missing"
    df["trade_date"] = df["trade_date"].astype(str)
    numeric_cols = ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]
    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.loc[df["trade_date"] <= target_date].sort_values("trade_date")
    df = df.dropna(subset=["close"])
    if df.empty:
        return None, None, "no rows on or before target date"

    series_df = df[["trade_date", "close"]].copy() if with_series else None
    safe_trend_days = max(20, int(trend_days))
    windows = [safe_trend_days, 60]
    if kline_days is not None:
        windows.append(max(20, int(kline_days)))
    df = df.tail(max(windows)).copy()

    for period in (1, 5, 20, 60):
        df[f"ret_{period}d"] = pct_return(df["close"], period)
    for period in (5, 20, 60):
        df[f"ma{period}"] = df["close"].rolling(period, min_periods=max(3, period // 2)).mean()

    liquidity_col = "amount" if "amount" in df.columns and df["amount"].notna().any() else "vol"
    df.attrs["liquidity_col"] = liquidity_col
    if liquidity_col in df.columns:
        df["liquidity_ma5_prev"] = df[liquidity_col].shift(1).rolling(5, min_periods=3).mean().replace(0, pd.NA)
        df["liquidity_ma20_prev"] = df[liquidity_col].shift(1).rolling(20, min_periods=5).mean().replace(0, pd.NA)
        df["liquidity_ratio_5d"] = df[liquidity_col] / df["liquidity_ma5_prev"]
        df["liquidity_ratio_20d"] = df[liquidity_col] / df["liquidity_ma20_prev"]
    else:
        df["liquidity_ratio_5d"] = None
        df["liquidity_ratio_20d"] = None
    df["amount_ratio_20d"] = df["liquidity_ratio_20d"] if liquidity_col == "amount" else None

    df["high_20d"] = df["high"].rolling(20, min_periods=5).max() if "high" in df.columns else None
    df["low_20d"] = df["low"].rolling(20, min_periods=5).min() if "low" in df.columns else None
    df["high_60d"] = df["high"].rolling(60, min_periods=20).max() if "high" in df.columns else None
    df["low_60d"] = df["low"].rolling(60, min_periods=20).min() if "low" in df.columns else None
    return df, series_df, ""


def _build_close_series(df: pd.DataFrame, days: int = 90) -> Dict[str, Any]:
    records = df[["trade_date", "close"]].copy()
    records["close"] = pd.to_numeric(records["close"], errors="coerce")
    records = records.dropna(subset=["close"]).sort_values("trade_date").tail(max(1, int(days)))
    records["close"] = records["close"].round(2)
    return {
        "days": int(days),
        "records": records.astype(object).where(pd.notnull(records), None).to_dict(orient="records"),
    }


def build_index_trend_summary(
    index_daily: pd.DataFrame,
    index_name: str,
    ts_code: str,
    target_date: str,
    trend_days: int,
    kline_days: int = DEFAULT_INDEX_KLINE_DAYS,
) -> Dict[str, Any]:
    safe_trend_days = max(20, int(trend_days))
    safe_kline_days = max(20, int(kline_days))
    df, _, reason = _prepare_index_summary_frames(index_daily, target_date, safe_trend_days, safe_kline_days)
    if df is None:
        return _unavailable_index_summary(index_name, "ts_code", ts_code, reason)

    latest = df.iloc[-1]
    ma5 = latest.get("ma5")
    ma20 = latest.get("ma20")
    ma60 = latest.get("ma60")
    close = latest.get("close")
    ret_1d = latest.get("pct_chg") if pd.notna(latest.get("pct_chg")) else latest.get("ret_1d")

    kline_cols = [
        col
        for col in ["trade_date", "open", "high", "low", "close", "pct_chg", "vol", "amount"]
        if col in df.columns
    ]
    kline_records = df[kline_cols].tail(safe_kline_days).copy()
    for column in kline_cols:
        if column != "trade_date":
            kline_records[column] = pd.to_numeric(kline_records[column], errors="coerce").round(4)

    return {
        "available": True,
        "name": index_name,
        "ts_code": ts_code,
        "trade_date": str(latest.get("trade_date")),
        "window_start": str(df["trade_date"].iloc[0]),
        "window_end": str(df["trade_date"].iloc[-1]),
        "records_loaded": int(len(df)),
        "trend_days": int(min(safe_trend_days, len(df))),
        "kline_days": int(min(safe_kline_days, len(kline_records))),
        "kline_days_requested": int(safe_kline_days),
        "latest": {
            "close": round_optional(close, 2),
            "pct_chg": round_optional(ret_1d, 2),
            "amount": round_optional(latest.get("amount"), 4) if "amount" in df.columns else None,
            "amount_100m_yuan": round_optional(latest.get("amount") / 100000, 2) if "amount" in df.columns and pd.notna(latest.get("amount")) else None,
            "vol": round_optional(latest.get("vol"), 4) if "vol" in df.columns else None,
        },
        "returns": {
            "ret_1d": round_optional(ret_1d, 2),
            "ret_5d": round_optional(latest.get("ret_5d"), 2),
            "ret_20d": round_optional(latest.get("ret_20d"), 2),
            "ret_60d": round_optional(latest.get("ret_60d"), 2),
        },
        "moving_averages": {
            "ma5": round_optional(ma5, 2),
            "ma20": round_optional(ma20, 2),
            "ma60": round_optional(ma60, 2),
            "close_vs_ma5_pct": pct_change_optional(close, ma5),
            "close_vs_ma20_pct": pct_change_optional(close, ma20),
            "close_vs_ma60_pct": pct_change_optional(close, ma60),
            "ma_alignment_hint": classify_ma_alignment(close, ma5, ma20, ma60),
        },
        "volume_price": {
            "liquidity_field": df.attrs.get("liquidity_col"),
            "liquidity_ratio_5d": round_optional(latest.get("liquidity_ratio_5d"), 2),
            "liquidity_ratio_20d": round_optional(latest.get("liquidity_ratio_20d"), 2),
            "price_volume_state_hint": classify_price_volume_state(ret_1d, latest.get("liquidity_ratio_20d")),
        },
        "trend_stage_hint": classify_index_trend_stage(
            close,
            ma20,
            ma60,
            latest.get("ret_20d"),
            latest.get("ret_60d"),
        ),
        "levels": {
            "high_20d": round_optional(latest.get("high_20d"), 2),
            "low_20d": round_optional(latest.get("low_20d"), 2),
            "high_60d": round_optional(latest.get("high_60d"), 2),
            "low_60d": round_optional(latest.get("low_60d"), 2),
            "support_candidates": [
                build_level("low_20d", latest.get("low_20d")),
                build_level("low_60d", latest.get("low_60d")),
                build_level("ma20", ma20),
                build_level("ma60", ma60),
            ],
            "resistance_candidates": [
                build_level("high_20d", latest.get("high_20d")),
                build_level("high_60d", latest.get("high_60d")),
            ],
        },
        "kline_records": kline_records.astype(object).where(pd.notnull(kline_records), None).to_dict(orient="records"),
    }


def ymd_to_dash_date(value: str) -> str:
    return ymd_to_dt(value).strftime("%Y-%m-%d")


def baostock_result_to_frame(result: Any) -> pd.DataFrame:
    if result is None:
        return pd.DataFrame()
    if hasattr(result, "get_data"):
        try:
            return result.get_data()
        except Exception:
            pass

    fields = [field.strip() for field in BAOSTOCK_STYLE_FIELDS.split(",")]
    rows: List[List[Any]] = []
    try:
        while result.error_code == "0" and result.next():
            rows.append(result.get_row_data())
    except Exception:
        return pd.DataFrame()
    return pd.DataFrame(rows, columns=fields)


def normalize_baostock_trade_date(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    raw = str(value).strip()
    if not raw:
        return ""
    try:
        return normalize_date(raw)
    except ValueError:
        return ""


def standardize_baostock_index_daily(raw: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    if raw is None or raw.empty:
        return pd.DataFrame()

    df = raw.copy()
    df = df.rename(columns={
        "date": "trade_date",
        "code": "bs_code",
        "preclose": "pre_close",
        "volume": "vol",
        "pctChg": "pct_chg",
    })
    if "trade_date" not in df.columns:
        return pd.DataFrame()

    df["trade_date"] = df["trade_date"].apply(normalize_baostock_trade_date)
    df = df.loc[df["trade_date"] != ""].copy()
    df["bs_code"] = config.get("bs_code")
    df["name"] = config.get("name")
    for column in ["open", "high", "low", "close", "pre_close", "pct_chg", "vol", "amount"]:
        if column in df.columns:
            df[column] = parse_numeric_text_series(df[column])
    return df.sort_values("trade_date").reset_index(drop=True)


def build_market_style_index_summary(
    standardized: pd.DataFrame,
    config: Dict[str, Any],
    target_date: str,
    trend_days: int,
) -> Dict[str, Any]:
    """Summarize one style index from a standardized daily frame.

    `standardized` must already carry trade_date (YYYYMMDD strings) plus the
    usual OHLC/pct_chg/amount columns — either fresh from
    standardize_baostock_index_daily or read back from the PG cache.
    """
    extra = {
        "style_role": config.get("style_role"),
        "proxy_note": config.get("proxy_note"),
    }
    safe_trend_days = max(20, int(trend_days))
    df, series_df, reason = _prepare_index_summary_frames(standardized, target_date, safe_trend_days, with_series=True)
    if df is None or series_df is None:
        if standardized is None or standardized.empty:
            reason = "baostock returned no data"
        return _unavailable_index_summary(config.get("name"), "bs_code", config.get("bs_code"), reason, extra)

    latest = df.iloc[-1]
    close = latest.get("close")
    ma20 = latest.get("ma20")
    ma60 = latest.get("ma60")
    pct_chg = latest.get("pct_chg") if pd.notna(latest.get("pct_chg")) else latest.get("ret_1d")
    amount = latest.get("amount") if "amount" in df.columns else None

    return {
        "available": True,
        "name": config.get("name"),
        "bs_code": config.get("bs_code"),
        "style_role": config.get("style_role"),
        "proxy_note": config.get("proxy_note"),
        "trade_date": str(latest.get("trade_date")),
        "window_start": str(df["trade_date"].iloc[0]),
        "window_end": str(df["trade_date"].iloc[-1]),
        "records_loaded": int(len(df)),
        "latest": {
            "close": round_optional(close, 2),
            "pct_chg": round_optional(pct_chg, 2),
            "amount": round_optional(amount, 2),
            "amount_100m_yuan": round_optional(amount / 100000000, 2) if amount is not None and pd.notna(amount) else None,
        },
        "returns": {
            "ret_1d": round_optional(pct_chg, 2),
            "ret_5d": round_optional(latest.get("ret_5d"), 2),
            "ret_20d": round_optional(latest.get("ret_20d"), 2),
            "ret_60d": round_optional(latest.get("ret_60d"), 2),
        },
        "moving_averages": {
            "ma20": round_optional(ma20, 2),
            "ma60": round_optional(ma60, 2),
            "close_vs_ma20_pct": pct_change_optional(close, ma20),
            "close_vs_ma60_pct": pct_change_optional(close, ma60),
        },
        "volume_price": {
            "amount_unit": "yuan",
            "amount_ratio_20d": round_optional(latest.get("amount_ratio_20d"), 2),
            "price_volume_state_hint": classify_price_volume_state(pct_chg, latest.get("amount_ratio_20d")),
        },
        "trend_stage_hint": classify_index_trend_stage(
            close,
            ma20,
            ma60,
            latest.get("ret_20d"),
            latest.get("ret_60d"),
        ),
        "series": _build_close_series(series_df, days=90),
    }


def market_style_return(style: Dict[str, Any], key: str, field: str) -> Optional[float]:
    item = ((style.get("indices") or {}).get(key) or {})
    value = ((item.get("returns") or {}).get(field))
    return safe_float(value)


def build_style_spread(style: Dict[str, Any], label: str, left_key: str, right_key: str) -> Dict[str, Any]:
    indices = style.get("indices") or {}
    left = indices.get(left_key) or {}
    right = indices.get(right_key) or {}
    left_5d = market_style_return(style, left_key, "ret_5d")
    right_5d = market_style_return(style, right_key, "ret_5d")
    left_20d = market_style_return(style, left_key, "ret_20d")
    right_20d = market_style_return(style, right_key, "ret_20d")
    return {
        "label": label,
        "left_key": left_key,
        "left_name": left.get("name"),
        "right_key": right_key,
        "right_name": right.get("name"),
        "ret_5d_diff": round(left_5d - right_5d, 2) if left_5d is not None and right_5d is not None else None,
        "ret_20d_diff": round(left_20d - right_20d, 2) if left_20d is not None and right_20d is not None else None,
    }


def build_market_style_summary(index_summaries: Dict[str, Dict[str, Any]], target_date: str, start_date: str) -> Dict[str, Any]:
    available_count = sum(1 for item in index_summaries.values() if item.get("available"))
    style: Dict[str, Any] = {
        "available": available_count > 0,
        "source": "baostock.query_history_k_data_plus",
        "source_reference": BAOSTOCK_STYLE_SOURCE_URL,
        "trade_date": target_date,
        "window_start": start_date,
        "window_end": target_date,
        "indices": index_summaries,
        "included_indices": list(MARKET_STYLE_INDEXES.keys()),
        "proxy_notes": {
            key: config["proxy_note"]
            for key, config in MARKET_STYLE_INDEXES.items()
            if config.get("proxy_note")
        },
        "missing": [
            {
                "key": key,
                "name": item.get("name"),
                "reason": item.get("reason"),
            }
            for key, item in index_summaries.items()
            if not item.get("available")
        ],
    }
    if not style["available"]:
        style["reason"] = "no Baostock style index data available"
        style["spreads"] = []
        return style

    style["spreads"] = [
        build_style_spread(style, "微盘代理相对沪深300", "guozheng2000", "csi300"),
        build_style_spread(style, "中证1000相对沪深300", "csi1000", "csi300"),
        build_style_spread(style, "中证500相对沪深300", "csi500", "csi300"),
        build_style_spread(style, "中证红利相对300成长", "csi_dividend", "csi300_growth"),
        build_style_spread(style, "300成长相对300价值", "csi300_growth", "csi300_value"),
        build_style_spread(style, "超大盘相对国证2000", "mega_cap", "guozheng2000"),
    ]
    return style


def build_unavailable_market_style(reason: str, target_date: str, start_date: str) -> Dict[str, Any]:
    return {
        "available": False,
        "source": "baostock.query_history_k_data_plus",
        "source_reference": BAOSTOCK_STYLE_SOURCE_URL,
        "trade_date": target_date,
        "window_start": start_date,
        "window_end": target_date,
        "included_indices": list(MARKET_STYLE_INDEXES.keys()),
        "indices": {
            key: {
                "available": False,
                "name": config.get("name"),
                "bs_code": config.get("bs_code"),
                "style_role": config.get("style_role"),
                "proxy_note": config.get("proxy_note"),
                "reason": reason,
            }
            for key, config in MARKET_STYLE_INDEXES.items()
        },
        "spreads": [],
        "reason": reason,
    }


STYLE_INDEX_CACHE_FIELDS = "ts_code,trade_date,open,high,low,close,pre_close,pct_chg,amount"


def read_cached_style_index(bs_code: str) -> Optional[pd.DataFrame]:
    try:
        return read_cached_dataset("index_daily", bs_code, STYLE_INDEX_CACHE_FIELDS)
    except Exception as exc:
        print(f"[warn] style index cache read failed for {bs_code}: {exc}", file=sys.stderr)
        return None


def query_baostock_style_range(config: Dict[str, Any], fetch_start: str, fetch_end: str) -> pd.DataFrame:
    """Fetch and standardize one Baostock style-index range. Caller owns the session."""
    result = bs.query_history_k_data_plus(
        config["bs_code"],
        BAOSTOCK_STYLE_FIELDS,
        start_date=ymd_to_dash_date(fetch_start),
        end_date=ymd_to_dash_date(fetch_end),
        frequency="d",
        adjustflag="3",
    )
    if getattr(result, "error_code", "0") != "0":
        reason = getattr(result, "error_msg", "") or getattr(result, "error_code", "unknown")
        raise RuntimeError(f"baostock query failed: {reason}")
    return standardize_baostock_index_daily(baostock_result_to_frame(result), config)


def fetch_market_style_from_baostock(
    target_date: str,
    start_date: str,
    trend_days: int,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    """Build style-index summaries, serving history from the PG cache.

    Baostock is only dialled for edge ranges the stock_index_daily cache does
    not cover (keyed by bs_code), with a single login session for all indexes.
    When Baostock is unavailable the cached window still yields summaries.
    """
    cache_fields = split_fields(STYLE_INDEX_CACHE_FIELDS)
    frames: Dict[str, pd.DataFrame] = {}
    fetch_plan: Dict[str, List[Tuple[str, str]]] = {}
    for key, config in MARKET_STYLE_INDEXES.items():
        cached = None if refresh_cache or not cache_enabled else read_cached_style_index(config["bs_code"])
        if cached is not None and not cached.empty:
            cached = cached.copy()
            cached["trade_date"] = cached["trade_date"].astype(str)
            frames[key] = cached
            ranges = missing_edge_ranges(cached, "trade_date", start_date, target_date)
        else:
            ranges = [(start_date, target_date)]
        if ranges:
            fetch_plan[key] = ranges

    fetch_errors: Dict[str, str] = {}
    if fetch_plan:
        login_error: Optional[str] = None
        if bs is None:
            login_error = "missing optional dependency: baostock"
        else:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    login = bs.login()
                if getattr(login, "error_code", "0") != "0":
                    login_error = getattr(login, "error_msg", "") or getattr(login, "error_code", "unknown")
                    login_error = f"baostock login failed: {login_error}"
            except Exception as exc:
                login_error = f"baostock login failed: {exc}"

        if login_error:
            fetch_errors = {key: login_error for key in fetch_plan}
        else:
            try:
                for key, ranges in fetch_plan.items():
                    config = MARKET_STYLE_INDEXES[key]
                    fetched: List[pd.DataFrame] = []
                    for fetch_start, fetch_end in ranges:
                        try:
                            frame = query_baostock_style_range(config, fetch_start, fetch_end)
                        except Exception as exc:
                            fetch_errors[key] = str(exc)
                            continue
                        if not frame.empty:
                            fetched.append(frame)
                        time.sleep(0.05)
                    if not fetched:
                        continue
                    addition = pd.concat(fetched, ignore_index=True)
                    addition["ts_code"] = config["bs_code"]
                    keep = [column for column in cache_fields if column in addition.columns]
                    addition = addition[keep]
                    merged = pd.concat([frames[key][keep], addition], ignore_index=True) if key in frames else addition
                    merged = (
                        merged.drop_duplicates(subset=["trade_date"], keep="last")
                        .sort_values("trade_date")
                        .reset_index(drop=True)
                    )
                    frames[key] = merged
                    if cache_enabled:
                        try:
                            write_cached_dataset("index_daily", config["bs_code"], merged)
                        except Exception as exc:
                            print(f"[warn] style index cache write failed for {config['bs_code']}: {exc}", file=sys.stderr)
            finally:
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        bs.logout()
                except Exception:
                    pass

    summaries: Dict[str, Dict[str, Any]] = {}
    for key, config in MARKET_STYLE_INDEXES.items():
        df = frames.get(key)
        if df is None or df.empty:
            summaries[key] = {
                "available": False,
                "name": config.get("name"),
                "bs_code": config.get("bs_code"),
                "style_role": config.get("style_role"),
                "proxy_note": config.get("proxy_note"),
                "reason": fetch_errors.get(key, "baostock returned no data"),
            }
            continue
        summary = build_market_style_index_summary(df, config, target_date, trend_days)
        if key in fetch_errors:
            summary["fetch_warning"] = f"served from cache; latest fetch failed: {fetch_errors[key]}"
        summaries[key] = summary

    style = build_market_style_summary(summaries, target_date, start_date)
    style["source"] = "baostock.query_history_k_data_plus + stock_index_daily cache"
    return style


def collect_stock_kline_targets(*payloads: Dict[str, Any]) -> List[Dict[str, Any]]:
    targets: List[Dict[str, Any]] = []
    by_code: Dict[str, Dict[str, Any]] = {}

    def add_record(record: Dict[str, Any]) -> None:
        ts_code = str(record.get("ts_code") or "").strip()
        if not ts_code:
            return
        name = str(record.get("name") or "").strip()
        if ts_code in by_code:
            if name:
                aliases = by_code[ts_code].setdefault("aliases", [])
                if name not in aliases:
                    aliases.append(name)
            return
        target = {
            "ts_code": ts_code,
            "name": name or None,
            "aliases": [name] if name else [],
        }
        by_code[ts_code] = target
        targets.append(target)

    for payload in payloads:
        if not isinstance(payload, dict):
            continue
        records = payload.get("candidates")
        if isinstance(records, list):
            for record in records:
                if isinstance(record, dict):
                    add_record(record)
        groups = payload.get("groups")
        if isinstance(groups, dict):
            for group in groups.values():
                group_records = group.get("candidates") if isinstance(group, dict) else None
                if isinstance(group_records, list):
                    for record in group_records:
                        if isinstance(record, dict):
                            add_record(record)
    return targets


def build_stock_kline_records(
    daily: pd.DataFrame,
    stock_basic: pd.DataFrame,
    targets: List[Dict[str, Any]],
    target_date: str,
    kline_days: int = DEFAULT_INDEX_KLINE_DAYS,
) -> Dict[str, Any]:
    safe_kline_days = max(20, int(kline_days))
    empty_payload = {
        "metadata": {
            "target_date": target_date,
            "kline_days_requested": safe_kline_days,
            "stock_count": 0,
            "price_adjustment": "qfq",
        },
        "by_ts_code": {},
        "name_to_ts_code": {},
    }
    if daily is None or daily.empty or not targets:
        return empty_payload

    name_lookup: Dict[str, str] = {}
    if stock_basic is not None and not stock_basic.empty and {"ts_code", "name"}.issubset(stock_basic.columns):
        pairs = stock_basic[["ts_code", "name"]].dropna()
        name_lookup = {
            str(ts_code): str(name)
            for ts_code, name in zip(pairs["ts_code"], pairs["name"])
            if str(ts_code or "").strip()
        }

    requested_names: Dict[str, str] = {}
    name_to_ts_code: Dict[str, str] = {}
    selected_codes: List[str] = []
    seen: Set[str] = set()
    for target in targets:
        ts_code = str(target.get("ts_code") or "").strip()
        if not ts_code or ts_code in seen:
            continue
        seen.add(ts_code)
        selected_codes.append(ts_code)
        name = str(target.get("name") or name_lookup.get(ts_code) or "").strip()
        if name:
            requested_names[ts_code] = name
        for alias in target.get("aliases") or []:
            alias_text = str(alias or "").strip()
            if alias_text:
                name_to_ts_code[alias_text] = ts_code
    if not selected_codes:
        return empty_payload

    df = daily.copy()
    df["ts_code"] = df["ts_code"].astype(str)
    df = df.loc[df["ts_code"].isin(selected_codes)]
    if df.empty:
        return empty_payload

    df = df.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    df = df.loc[(df["trade_date"] != "") & (df["trade_date"] <= target_date)].copy()
    numeric_cols = ["open", "high", "low", "close", "pct_chg", "vol", "amount"]
    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").round(4)

    by_ts_code: Dict[str, Any] = {}
    kline_cols = [col for col in ["trade_date", "open", "high", "low", "close", "pct_chg", "vol", "amount"] if col in df.columns]
    frames_by_code: Dict[str, pd.DataFrame] = {str(code): frame for code, frame in df.groupby("ts_code")}
    for ts_code in selected_codes:
        sub = frames_by_code.get(ts_code)
        if sub is None:
            continue
        sub = sub.sort_values("trade_date").dropna(subset=["close"])
        if sub.empty:
            continue
        kline_records = sub[kline_cols].tail(safe_kline_days).copy()
        name = requested_names.get(ts_code) or name_lookup.get(ts_code) or ts_code
        by_ts_code[ts_code] = {
            "available": True,
            "name": name,
            "ts_code": ts_code,
            "trade_date": str(sub["trade_date"].iloc[-1]),
            "price_adjustment": "qfq",
            "kline_days": int(len(kline_records)),
            "kline_days_requested": int(safe_kline_days),
            "records": kline_records.astype(object).where(pd.notnull(kline_records), None).to_dict(orient="records"),
        }
        if name:
            name_to_ts_code[name] = ts_code

    return {
        "metadata": {
            "target_date": target_date,
            "kline_days_requested": safe_kline_days,
            "stock_count": int(len(by_ts_code)),
            "price_adjustment": "qfq",
        },
        "by_ts_code": by_ts_code,
        "name_to_ts_code": name_to_ts_code,
    }


def count_consecutive_moves(series: pd.Series, direction: str) -> int:
    values = [safe_float(value) for value in series.dropna().tolist()]
    values = [value for value in values if value is not None]
    count = 0
    for index in range(len(values) - 1, 0, -1):
        if direction == "up" and values[index] > values[index - 1]:
            count += 1
        elif direction == "down" and values[index] < values[index - 1]:
            count += 1
        else:
            break
    return count


def classify_volume_temperature(amount_ratio_20d: Any) -> Optional[str]:
    ratio = safe_float(amount_ratio_20d)
    if ratio is None:
        return None
    if ratio >= 1.25:
        return "clear_expansion"
    if ratio >= 1.05:
        return "mild_expansion"
    if ratio <= 0.80:
        return "clear_contraction"
    if ratio <= 0.95:
        return "mild_contraction"
    return "stable_volume"


def classify_turnover_acceleration(turnover_series: pd.Series) -> Dict[str, Any]:
    values = [safe_float(value) for value in turnover_series.dropna().tail(5).tolist()]
    values = [value for value in values if value is not None]
    if len(values) < 3:
        return {
            "status": "insufficient_data",
            "window_days": len(values),
            "reason": "fewer than 3 valid turnover observations",
        }

    current = values[-1]
    first = values[0]
    ma5 = sum(values) / len(values)
    change_pct = ((current / first - 1.0) * 100.0) if first else None
    above_ma5_pct = ((current / ma5 - 1.0) * 100.0) if ma5 else None
    recent = pd.Series(values)
    consecutive_up = count_consecutive_moves(recent, "up")
    consecutive_down = count_consecutive_moves(recent, "down")

    if consecutive_down >= 2 or (change_pct is not None and change_pct <= -5.0):
        status = "cooling"
    elif (
        (consecutive_up >= 3 and change_pct is not None and change_pct >= 8.0)
        or (
            change_pct is not None
            and above_ma5_pct is not None
            and change_pct >= 8.0
            and above_ma5_pct >= 5.0
        )
    ):
        status = "accelerating"
    elif (
        (change_pct is not None and change_pct >= 3.0)
        or consecutive_up >= 2
        or (above_ma5_pct is not None and above_ma5_pct >= 3.0)
    ):
        status = "mild_acceleration"
    else:
        status = "stable"

    risk_hint = {
        "accelerating": "turnover_acceleration_watch",
        "mild_acceleration": "mild_turnover_pickup",
        "stable": "stable_turnover",
        "cooling": "turnover_cooling",
    }.get(status)
    return {
        "status": status,
        "risk_hint": risk_hint,
        "window_days": len(values),
        "current": round(current, 4),
        "window_start": round(first, 4),
        "window_change_pct": round(change_pct, 2) if change_pct is not None else None,
        "current_vs_window_avg_pct": round(above_ma5_pct, 2) if above_ma5_pct is not None else None,
        "consecutive_up_days": consecutive_up,
        "consecutive_down_days": consecutive_down,
    }


def classify_sentiment_temperature(activity: Any, limit_up_down_ratio: Any) -> Optional[str]:
    activity_value = safe_float(activity)
    if activity_value is not None:
        if activity_value < 20:
            return "cold"
        if activity_value < 40:
            return "weak"
        if activity_value <= 60:
            return "neutral"
        if activity_value <= 80:
            return "hot"
        return "overheated"

    ratio = safe_float(limit_up_down_ratio)
    if ratio is None:
        return None
    if ratio < 0.5:
        return "cold"
    if ratio < 1.0:
        return "weak"
    if ratio <= 2.0:
        return "neutral"
    if ratio <= 4.0:
        return "hot"
    return "overheated"


def classify_breadth_temperature(up_ratio: Any) -> Optional[str]:
    ratio = safe_float(up_ratio)
    if ratio is None:
        return None
    if ratio >= 0.65:
        return "broad_rise"
    if ratio >= 0.52:
        return "partial_repair"
    if ratio <= 0.35:
        return "broad_decline"
    if ratio <= 0.48:
        return "partial_weakness"
    return "split"


def build_sentiment_trend(target_date: str, trend_days: int) -> Dict[str, Any]:
    csv_path = DEFAULT_MARKET_HISTORY_CSV
    source = "market_history" if BACKEND == Backend.POSTGRESQL else str(csv_path)
    if BACKEND == Backend.POSTGRESQL:
        try:
            raw = read_market_history()
        except Exception as exc:
            return {
                "available": False,
                "source": source,
                "reason": f"failed to read market_history table: {exc}",
            }
        if raw is not None and not raw.empty:
            raw = raw.rename(columns={
                "date": "日期",
                "rise": "上涨",
                "limit_up": "涨停",
                "fall": "下跌",
                "limit_down": "跌停",
                "flat": "平盘",
                "activity": "活跃度",
                "sentiment": "情绪值",
                "amount": "成交额",
                "margin_net_buy": "融资净买入",
                "turnover_rate": "全市场换手率",
            })
    else:
        if not csv_path.exists():
            return {
                "available": False,
                "source": source,
                "reason": "references/market_data.csv not found",
            }

        try:
            raw = pd.read_csv(csv_path, encoding="utf-8-sig")
        except Exception as exc:
            return {
                "available": False,
                "source": source,
                "reason": f"failed to read market_data.csv: {exc}",
            }

    if raw is None or raw.empty or "日期" not in raw.columns:
        return {
            "available": False,
            "source": source,
            "reason": "market_history is empty or missing 日期 column",
        }

    df = raw.copy()
    df["date"] = pd.to_datetime(df["日期"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["trade_date"] = df["date"].dt.strftime("%Y%m%d")
    df = df.loc[df["trade_date"] <= target_date].sort_values("trade_date")
    if df.empty:
        return {
            "available": False,
            "source": source,
            "reason": "no sentiment rows on or before target date",
        }

    expected_columns = ["上涨", "下跌", "平盘", "涨停", "跌停", "活跃度", "情绪值", "成交额", "全市场换手率"]
    for column in expected_columns:
        if column in df.columns:
            df[column] = parse_numeric_text_series(df[column])

    df = df.tail(int(trend_days)).copy()
    flat = df["平盘"].fillna(0) if "平盘" in df.columns else 0
    breadth_total = df["上涨"] + df["下跌"] + flat
    df["up_ratio"] = df["上涨"] / breadth_total.replace(0, pd.NA)
    df["limit_up_down_ratio"] = df["涨停"] / df["跌停"].replace(0, pd.NA)
    if "成交额" in df.columns:
        df["amount_trillion_yuan"] = df["成交额"] / 1e9
        df["amount_ma5"] = df["成交额"].rolling(5, min_periods=3).mean()
        df["amount_ma20"] = df["成交额"].rolling(20, min_periods=5).mean()
        df["amount_ratio_5d"] = df["成交额"] / df["amount_ma5"].replace(0, pd.NA)
        df["amount_ratio_20d"] = df["成交额"] / df["amount_ma20"].replace(0, pd.NA)
    if "全市场换手率" in df.columns:
        df["market_turnover_rate"] = df["全市场换手率"]
        df["market_turnover_rate_ma5"] = df["market_turnover_rate"].rolling(5, min_periods=3).mean()
        df["market_turnover_rate_ma20"] = df["market_turnover_rate"].rolling(20, min_periods=5).mean()
        df["market_turnover_rate_ratio_5d"] = df["market_turnover_rate"] / df["market_turnover_rate_ma5"].replace(0, pd.NA)
        df["market_turnover_rate_ratio_20d"] = df["market_turnover_rate"] / df["market_turnover_rate_ma20"].replace(0, pd.NA)

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) >= 2 else None
    amount_ma5 = latest.get("amount_ma5") if "amount_ma5" in df.columns else None
    amount_ma20 = latest.get("amount_ma20") if "amount_ma20" in df.columns else None
    turnover_ma5 = latest.get("market_turnover_rate_ma5") if "market_turnover_rate_ma5" in df.columns else None
    turnover_ma20 = latest.get("market_turnover_rate_ma20") if "market_turnover_rate_ma20" in df.columns else None
    turnover_valid = df["market_turnover_rate"].dropna() if "market_turnover_rate" in df.columns else pd.Series(dtype=float)
    turnover_5d_base = turnover_valid.iloc[-5] if len(turnover_valid) >= 5 else None

    recent_cols = [
        col
        for col in [
            "trade_date",
            "上涨",
            "下跌",
            "涨停",
            "跌停",
            "活跃度",
            "情绪值",
            "成交额",
            "amount_trillion_yuan",
            "market_turnover_rate",
            "up_ratio",
            "limit_up_down_ratio",
        ]
        if col in df.columns
    ]
    recent = df[recent_cols].tail(min(20, len(df))).copy()
    for column in recent_cols:
        if column != "trade_date":
            recent[column] = pd.to_numeric(recent[column], errors="coerce").round(4)

    return {
        "available": True,
        "source": source,
        "trade_date": str(latest.get("trade_date")),
        "matches_target_date": str(latest.get("trade_date")) == target_date,
        "window_start": str(df["trade_date"].iloc[0]),
        "window_end": str(df["trade_date"].iloc[-1]),
        "records_loaded": int(len(df)),
        "latest": {
            "up_count": round_optional(latest.get("上涨"), 0),
            "down_count": round_optional(latest.get("下跌"), 0),
            "limit_up_count": round_optional(latest.get("涨停"), 0),
            "limit_down_count": round_optional(latest.get("跌停"), 0),
            "activity": round_optional(latest.get("活跃度"), 2),
            "sentiment_value": round_optional(latest.get("情绪值"), 2),
            "amount": round_optional(latest.get("成交额"), 4),
            "amount_trillion_yuan": round_optional(latest.get("amount_trillion_yuan"), 2),
            "market_turnover_rate": round_optional(latest.get("market_turnover_rate"), 4) if "market_turnover_rate" in df.columns else None,
            "market_turnover_rate_ma5": round_optional(turnover_ma5, 4),
            "market_turnover_rate_ma20": round_optional(turnover_ma20, 4),
            "up_ratio": round_optional(latest.get("up_ratio"), 4),
            "limit_up_down_ratio": round_optional(latest.get("limit_up_down_ratio"), 2),
        },
        "rolling": {
            "amount_ma5": round_optional(amount_ma5, 4),
            "amount_ma20": round_optional(amount_ma20, 4),
            "amount_ma5_trillion_yuan": round_optional(amount_ma5 / 1e9, 2) if amount_ma5 is not None and pd.notna(amount_ma5) else None,
            "amount_ma20_trillion_yuan": round_optional(amount_ma20 / 1e9, 2) if amount_ma20 is not None and pd.notna(amount_ma20) else None,
            "amount_ratio_5d": round_optional(latest.get("amount_ratio_5d"), 2) if "amount_ratio_5d" in df.columns else None,
            "amount_ratio_20d": round_optional(latest.get("amount_ratio_20d"), 2) if "amount_ratio_20d" in df.columns else None,
            "market_turnover_rate_ma5": round_optional(turnover_ma5, 4),
            "market_turnover_rate_ma20": round_optional(turnover_ma20, 4),
            "market_turnover_rate_ratio_5d": round_optional(latest.get("market_turnover_rate_ratio_5d"), 2) if "market_turnover_rate_ratio_5d" in df.columns else None,
            "market_turnover_rate_ratio_20d": round_optional(latest.get("market_turnover_rate_ratio_20d"), 2) if "market_turnover_rate_ratio_20d" in df.columns else None,
            "up_ratio_ma5": round_optional(df["up_ratio"].rolling(5, min_periods=3).mean().iloc[-1], 4),
            "activity_ma5": round_optional(df["活跃度"].rolling(5, min_periods=3).mean().iloc[-1], 2) if "活跃度" in df.columns else None,
            "limit_up_down_ratio_ma5": round_optional(df["limit_up_down_ratio"].rolling(5, min_periods=3).mean().iloc[-1], 2),
        },
        "changes": {
            "up_count_vs_previous": compare_scalar(latest.get("上涨"), previous.get("上涨") if previous is not None else None),
            "down_count_vs_previous": compare_scalar(latest.get("下跌"), previous.get("下跌") if previous is not None else None),
            "activity_vs_previous": compare_scalar(latest.get("活跃度"), previous.get("活跃度") if previous is not None else None),
            "amount_vs_previous": compare_scalar(latest.get("成交额"), previous.get("成交额") if previous is not None else None),
            "amount_vs_20d_avg_pct": pct_change_optional(latest.get("成交额"), amount_ma20),
            "market_turnover_rate_vs_previous": compare_scalar(
                latest.get("market_turnover_rate") if "market_turnover_rate" in df.columns else None,
                previous.get("market_turnover_rate") if previous is not None and "market_turnover_rate" in df.columns else None,
            ),
            "market_turnover_rate_5d_change": compare_scalar(
                latest.get("market_turnover_rate") if "market_turnover_rate" in df.columns else None,
                turnover_5d_base,
            ),
            "market_turnover_rate_vs_20d_avg_pct": pct_change_optional(
                latest.get("market_turnover_rate") if "market_turnover_rate" in df.columns else None,
                turnover_ma20,
            ),
            "market_turnover_rate_improving_days": count_consecutive_moves(df["market_turnover_rate"], "up") if "market_turnover_rate" in df.columns else 0,
            "market_turnover_rate_deteriorating_days": count_consecutive_moves(df["market_turnover_rate"], "down") if "market_turnover_rate" in df.columns else 0,
            "up_ratio_improving_days": count_consecutive_moves(df["up_ratio"], "up"),
            "up_ratio_deteriorating_days": count_consecutive_moves(df["up_ratio"], "down"),
        },
        "turnover_acceleration": classify_turnover_acceleration(df["market_turnover_rate"]) if "market_turnover_rate" in df.columns else {
            "status": "unavailable",
            "reason": "market_turnover_rate column missing",
        },
        "temperature_hints": {
            "volume": classify_volume_temperature(latest.get("amount_ratio_20d") if "amount_ratio_20d" in df.columns else None),
            "sentiment": classify_sentiment_temperature(latest.get("活跃度"), latest.get("limit_up_down_ratio")),
            "breadth": classify_breadth_temperature(latest.get("up_ratio")),
        },
        "recent_series": recent.astype(object).where(pd.notnull(recent), None).to_dict(orient="records"),
    }


def build_market_trend(
    pro,
    target_date: str,
    trade_dates: List[str],
    trend_days: int,
    index_kline_days: int = DEFAULT_INDEX_KLINE_DAYS,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    safe_trend_days = max(20, int(trend_days))
    safe_index_kline_days = max(20, int(index_kline_days))
    trend_start_date = trade_dates[0] if trade_dates else target_date
    kline_start_date = (
        ymd_to_dt(target_date) - timedelta(days=max(safe_index_kline_days * 3, 260))
    ).strftime("%Y%m%d")
    start_date = min(trend_start_date, kline_start_date)
    indices: Dict[str, Any] = {}
    for key, config in MARKET_TREND_INDEXES.items():
        index_daily = fetch_index_daily(
            pro,
            config["ts_code"],
            start_date,
            target_date,
            cache_enabled=cache_enabled,
            refresh_cache=refresh_cache,
        )
        indices[key] = build_index_trend_summary(
            index_daily=index_daily,
            index_name=config["name"],
            ts_code=config["ts_code"],
            target_date=target_date,
            trend_days=safe_trend_days,
            kline_days=safe_index_kline_days,
        )

    market_style = fetch_market_style_from_baostock(
        target_date=target_date,
        start_date=start_date,
        trend_days=safe_trend_days,
        cache_enabled=cache_enabled,
        refresh_cache=refresh_cache,
    )

    return {
        "metadata": {
            "trend_days_requested": safe_trend_days,
            "index_kline_days_requested": safe_index_kline_days,
            "index_start_date": start_date,
            "index_end_date": target_date,
            "sentiment_source": str(DEFAULT_MARKET_HISTORY_CSV),
            "included_indices": list(MARKET_TREND_INDEXES.keys()),
            "market_style_source": market_style.get("source"),
        },
        "indices": indices,
        "market_style": market_style,
        "sentiment": build_sentiment_trend(target_date, safe_trend_days),
    }


def candidate_columns() -> List[str]:
    return [
        "ts_code",
        "name",
        "market",
        "trade_date",
        "close",
        "pct_chg",
        "ret_3d",
        "ret_5d",
        "ret_10d",
        "ret_20d",
        "rel_ret_5d",
        "rel_ret_10d",
        "amount",
        "amount_100m_yuan",
        "amount_ratio_20d",
        "sustained_volume_days_5",
        "turnover_rate",
        "volume_ratio",
        "total_mv",
        "total_mv_100m_yuan",
        "circ_mv",
        "circ_mv_100m_yuan",
        "drawdown_120_high",
        "close_position_120d",
        "close_to_high",
        "elasticity_hint_score",
    ]


def clean_candidates(df: pd.DataFrame, limit: int) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    cols = [c for c in candidate_columns() if c in df.columns]
    out = df[cols].head(limit).copy()
    if "amount" in out.columns:
        out["amount_100m_yuan"] = pd.to_numeric(out["amount"], errors="coerce") / 100000
    if "total_mv" in out.columns:
        out["total_mv_100m_yuan"] = pd.to_numeric(out["total_mv"], errors="coerce") / 10000
    if "circ_mv" in out.columns:
        out["circ_mv_100m_yuan"] = pd.to_numeric(out["circ_mv"], errors="coerce") / 10000
    non_numeric_cols = {
        "ts_code",
        "name",
        "market",
        "trade_date",
    }
    numeric_cols = [c for c in out.columns if c not in non_numeric_cols]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce").round(4)
    out = out.astype(object).where(pd.notnull(out), None)
    return out.to_dict(orient="records")


def clamp(value: Optional[float], lower: float, upper: float) -> float:
    if value is None:
        return lower
    return max(lower, min(upper, float(value)))


def calculate_elasticity_hint_score(record: Dict[str, Any]) -> Optional[float]:
    """Deterministic trading-activity hint; the model still decides final roles."""
    amount_ratio = safe_float(record.get("amount_ratio_20d"))
    turnover = safe_float(record.get("turnover_rate"))
    volume_ratio = safe_float(record.get("volume_ratio"))
    ret_5d = safe_float(record.get("ret_5d"))
    rel_ret_5d = safe_float(record.get("rel_ret_5d"))
    total_mv = safe_float(record.get("total_mv_100m_yuan"))
    close_to_high = safe_float(record.get("close_to_high"))

    score = 0.0
    score += clamp(amount_ratio, 0.0, 5.0) * 1.2
    score += clamp(volume_ratio, 0.0, 5.0) * 0.6
    score += clamp(turnover, 0.0, 20.0) * 0.18
    score += clamp(ret_5d, 0.0, 30.0) * 0.10
    score += clamp(rel_ret_5d, 0.0, 30.0) * 0.12
    if close_to_high is not None:
        score += clamp((close_to_high - 0.90) * 20.0, 0.0, 2.0)
    if total_mv is not None:
        if total_mv <= 80:
            score += 2.0
        elif total_mv <= 200:
            score += 1.5
        elif total_mv <= 500:
            score += 1.0
        elif total_mv <= 1000:
            score += 0.4
    return round(score, 2)


def add_elasticity_hint_scores(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    scored = [dict(record) for record in records]
    for record in scored:
        record["elasticity_hint_score"] = calculate_elasticity_hint_score(record)
    return scored


def build_money_effect_samples(
    panel: pd.DataFrame,
    pct_chg_threshold: float,
    amount_threshold_100m_yuan: float,
    sample_limit: int,
) -> Dict[str, Any]:
    """
    Build the money-effect candidate pool for daily theme grouping.

    Hard filters (designed to capture the "today truly made money" cohort):
      - pct_chg >= pct_chg_threshold (default 7.0%)
      - amount    >= amount_threshold_100m_yuan in 100m yuan (default 2.0 == 2亿)

    Sort:
      - amount descending. Per the skill, money-effect leadership is judged
        primarily by trading amount, not by single-day pct_chg ranking.

    Output:
      - candidates: per-stock detailed records (same column set as other
                    candidate pools, so downstream rendering is consistent).
      - summary: aggregate statistics about this candidate pool.

    Theme grouping is intentionally NOT performed here. The model groups
    candidates by business facts at report-writing time.
    """
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": {
                "pct_chg_threshold": pct_chg_threshold,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
                "sort_by": "成交额降序",
            },
            "candidates": [],
            "summary": {
                "candidate_count": 0,
                "qualified_before_limit_count": 0,
                "market_total_amount_100m_yuan": None,
                "candidate_amount_share_of_market_pct": None,
            },
        }

    # daily.amount unit is thousand yuan: 1亿元 = 100000 千元
    amount_threshold_thousand_yuan = amount_threshold_100m_yuan * 100000

    df = panel.copy()
    for column in ("pct_chg", "amount", "ret_3d", "ret_5d", "rel_ret_5d", "amount_ratio_20d"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    market_total_amount_100m = float(df["amount"].fillna(0).clip(lower=0).sum() / 100000)

    qualified = df.loc[
        (df["pct_chg"].fillna(-999) >= pct_chg_threshold)
        & (df["amount"].fillna(0) >= amount_threshold_thousand_yuan)
    ].copy()

    qualified_before_limit_count = int(len(qualified))

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": {
                "pct_chg_threshold": pct_chg_threshold,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
                "sort_by": "成交额降序",
            },
            "candidates": [],
            "summary": {
                "candidate_count": 0,
                "qualified_before_limit_count": 0,
                "total_amount_100m_yuan": 0.0,
                "market_total_amount_100m_yuan": round(market_total_amount_100m, 2),
                "candidate_amount_share_of_market_pct": (
                    0.0 if market_total_amount_100m > 0 else None
                ),
            },
        }

    qualified = qualified.sort_values("amount", ascending=False).head(sample_limit)
    total_amount_100m = float(qualified["amount"].sum() / 100000)

    def _safe_median(col: str) -> Optional[float]:
        if col not in qualified.columns:
            return None
        series = pd.to_numeric(qualified[col], errors="coerce")
        if series.dropna().empty:
            return None
        return round(float(series.median()), 2)

    summary = {
        "candidate_count": int(len(qualified)),
        "qualified_before_limit_count": qualified_before_limit_count,
        "total_amount_100m_yuan": round(total_amount_100m, 2),
        "market_total_amount_100m_yuan": round(market_total_amount_100m, 2),
        "candidate_amount_share_of_market_pct": (
            round(total_amount_100m / market_total_amount_100m * 100, 2)
            if market_total_amount_100m > 0
            else None
        ),
        "median_pct_chg": round(float(qualified["pct_chg"].median()), 2),
        "max_pct_chg": round(float(qualified["pct_chg"].max()), 2),
        "min_pct_chg": round(float(qualified["pct_chg"].min()), 2),
        "median_ret_3d": _safe_median("ret_3d"),
        "median_ret_5d": _safe_median("ret_5d"),
        "median_rel_ret_5d": _safe_median("rel_ret_5d"),
        "median_amount_ratio_20d": _safe_median("amount_ratio_20d"),
    }
    summary["limit_up_count"], _, summary["limit_detection"] = count_limit_hits(qualified)

    return {
        "available": True,
        "filter_criteria": {
            "pct_chg_threshold": pct_chg_threshold,
            "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
            "sample_limit": sample_limit,
            "sort_by": "成交额降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
        },
        "candidates": add_elasticity_hint_scores(clean_candidates(qualified, sample_limit)),
        "summary": summary,
    }


def build_volume_decline_samples(
    panel: pd.DataFrame,
    pct_chg_max: float,
    amount_ratio_min: float,
    amount_threshold_100m_yuan: float,
    sample_limit: int,
) -> Dict[str, Any]:
    """
    Build the volume-spike-decline (爆量下跌) candidate pool.

    Hard filters (the "money is actively fleeing" cohort):
      - pct_chg          <= pct_chg_max (default -3.0%)
      - amount_ratio_20d >= amount_ratio_min (default 2.0x)
      - amount           >= amount_threshold_100m_yuan (default 1.0 == 1亿)

    Sort:
      - decline_intensity = amount_ratio_20d * abs(pct_chg), descending.
        This surfaces stocks that combine large drops with abnormal volume,
        which is the canonical 爆量下跌 signal the skill cares about.
    """
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": {
                "pct_chg_max": pct_chg_max,
                "amount_ratio_min": amount_ratio_min,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    amount_threshold_thousand_yuan = amount_threshold_100m_yuan * 100000

    df = panel.copy()
    for column in ("pct_chg", "amount", "amount_ratio_20d", "ret_3d", "ret_5d", "rel_ret_5d", "drawdown_120_high"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    qualified = df.loc[
        (df["pct_chg"].fillna(999) <= pct_chg_max)
        & (df["amount_ratio_20d"].fillna(0) >= amount_ratio_min)
        & (df["amount"].fillna(0) >= amount_threshold_thousand_yuan)
    ].copy()

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": {
                "pct_chg_max": pct_chg_max,
                "amount_ratio_min": amount_ratio_min,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
                "sort_by": "20日放量倍数 * 跌幅绝对值 降序",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    qualified["decline_intensity"] = (
        qualified["amount_ratio_20d"].fillna(0) * qualified["pct_chg"].fillna(0).abs()
    ).round(4)

    qualified = qualified.sort_values(
        ["decline_intensity", "amount_ratio_20d", "pct_chg"],
        ascending=[False, False, True],
    ).head(sample_limit)

    total_amount_100m = float(qualified["amount"].sum() / 100000)

    def _safe_median(col: str) -> Optional[float]:
        if col not in qualified.columns:
            return None
        series = pd.to_numeric(qualified[col], errors="coerce")
        if series.dropna().empty:
            return None
        return round(float(series.median()), 2)

    summary = {
        "candidate_count": int(len(qualified)),
        "total_amount_100m_yuan": round(total_amount_100m, 2),
        "median_pct_chg": round(float(qualified["pct_chg"].median()), 2),
        "min_pct_chg": round(float(qualified["pct_chg"].min()), 2),
        "median_amount_ratio_20d": round(float(qualified["amount_ratio_20d"].median()), 2),
        "max_amount_ratio_20d": round(float(qualified["amount_ratio_20d"].max()), 2),
        "median_ret_5d": _safe_median("ret_5d"),
        "median_drawdown_120_high": _safe_median("drawdown_120_high"),
    }
    _, summary["limit_down_count"], summary["limit_detection"] = count_limit_hits(qualified)

    # Inject decline_intensity into the candidate dict so downstream rendering can use it.
    base_records = clean_candidates(qualified, sample_limit)
    intensity_lookup = qualified.set_index("ts_code")["decline_intensity"].to_dict()
    for record in base_records:
        record["decline_intensity"] = intensity_lookup.get(record.get("ts_code"))

    return {
        "available": True,
        "filter_criteria": {
            "pct_chg_max": pct_chg_max,
            "amount_ratio_min": amount_ratio_min,
            "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
            "sample_limit": sample_limit,
            "sort_by": "20日放量倍数 * 跌幅绝对值 降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
        },
        "candidates": base_records,
        "summary": summary,
    }


def build_capacity_up_samples(
    panel: pd.DataFrame,
    market_cap_threshold_100m_yuan: float,
    amount_threshold_100m_yuan: float,
    pct_chg_threshold: float,
    sample_limit: int,
) -> Dict[str, Any]:
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    df = panel.copy()
    for column in (
        "pct_chg", "amount", "total_mv", "circ_mv", "close",
        "turnover_rate", "turnover_rate_f", "volume_ratio",
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    names = df["name"].fillna("").astype(str) if "name" in df.columns else pd.Series("", index=df.index)
    markets = df["market"].fillna("").astype(str) if "market" in df.columns else pd.Series("", index=df.index)
    ts_codes = df["ts_code"].fillna("").astype(str)
    total_mv_100m = df["total_mv"] / 10000 if "total_mv" in df.columns else pd.Series(float("nan"), index=df.index)
    amount_100m = df["amount"] / 100000 if "amount" in df.columns else pd.Series(float("nan"), index=df.index)

    qualified = df.loc[
        (total_mv_100m > market_cap_threshold_100m_yuan)
        & (amount_100m > amount_threshold_100m_yuan)
        & (df["pct_chg"].fillna(-999) > pct_chg_threshold)
        & ~markets.eq("北交所")
        & ~ts_codes.str.endswith(".BJ")
        & ~names.str.upper().str.contains("ST", na=False)
    ].copy()

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": {
                "total_mv_100m_yuan_min_exclusive": market_cap_threshold_100m_yuan,
                "amount_100m_yuan_min_exclusive": amount_threshold_100m_yuan,
                "pct_chg_min_exclusive": pct_chg_threshold,
                "exclude": "北交所/.BJ；ST/*ST",
                "sample_limit": sample_limit,
                "sort_by": "涨幅降序，其次成交额降序",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    qualified["amount_100m_yuan"] = qualified["amount"] / 100000
    qualified["total_mv_100m_yuan"] = qualified["total_mv"] / 10000
    if "circ_mv" in qualified.columns:
        qualified["circ_mv_100m_yuan"] = qualified["circ_mv"] / 10000
    else:
        qualified["circ_mv_100m_yuan"] = None

    qualified = qualified.sort_values(["pct_chg", "amount"], ascending=[False, False]).head(sample_limit)

    candidates: List[Dict[str, Any]] = []
    for _, row in qualified.iterrows():
        amount = safe_float(row.get("amount"))
        total_mv = safe_float(row.get("total_mv"))
        circ_mv = safe_float(row.get("circ_mv"))
        candidates.append({
            "ts_code": nullable_value(row.get("ts_code")),
            "name": nullable_value(row.get("name")),
            "market": nullable_value(row.get("market")),
            "pct_chg": round_optional(row.get("pct_chg"), 2),
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "total_mv_100m_yuan": round_optional(total_mv / 10000, 2) if total_mv is not None else None,
            "circ_mv_100m_yuan": round_optional(circ_mv / 10000, 2) if circ_mv is not None else None,
            "close": round_optional(row.get("close"), 2),
            "turnover_rate": round_optional(row.get("turnover_rate"), 2),
            "volume_ratio": round_optional(row.get("volume_ratio"), 2),
            "trigger_reason": "当天总市值 > 70 亿、成交额 > 5 亿、涨幅 > 8%，且排除北交所与 ST",
        })

    return {
        "available": True,
        "filter_criteria": {
            "total_mv_100m_yuan_min_exclusive": market_cap_threshold_100m_yuan,
            "amount_100m_yuan_min_exclusive": amount_threshold_100m_yuan,
            "pct_chg_min_exclusive": pct_chg_threshold,
            "exclude": "北交所/.BJ；ST/*ST",
            "sample_limit": sample_limit,
            "sort_by": "涨幅降序，其次成交额降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
            "market_cap_unit_note": "Tushare daily_basic 的 total_mv 单位为万元，脚本内部已按亿元阈值换算。",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "total_amount_100m_yuan": round(sum(float(item.get("amount_100m_yuan") or 0) for item in candidates), 2),
            "median_pct_chg": round_optional(qualified["pct_chg"].median(), 2),
            "max_pct_chg": round_optional(qualified["pct_chg"].max(), 2),
            "median_total_mv_100m_yuan": round_optional(qualified["total_mv_100m_yuan"].median(), 2),
        },
    }


def attach_discount_after_high(
    features: pd.DataFrame,
    target_date: str,
    lookback: int,
) -> Dict[str, Dict[str, Any]]:
    """为每只候选股算"前高之后的回撤折扣"。

    口径（用户定义）：
      - 前高：最近 lookback 个交易日窗口内（含今日）**收盘价**最高的那一天，
        取其收盘价为基准（前高收盘价）。若收盘最高日就是今日（今日创窗口内收盘新高），
        则没有"前高之后"，该股不计入。
      - 折扣 discount_after_high = 前高之后（前高日次日起至今日）出现的**最低价 low**
        的最小值 / 前高收盘价。也就是从前高算起最深跌到了前高的几成。
      - post_low_date / low_to_target_days：该最低点的日期，以及它距大涨日的交易日数
        （供"最低点须在大涨日前 N 日内"的新鲜度过滤使用）。
      - close_vs_prev_high：今日收盘 / 前高收盘价，仅作参考（反映现价是否仍在折价位）。
      - monthly_ma10 / monthly_above_ma10：月线 10 月均线（月末收盘的 10 月 SMA）及
        当前月收盘是否站上它，用作长期趋势过滤；月数不足 10 个则为 None。

    需要每只股的多日 close/low 序列，故输入 features（候选股多日特征帧），
    每只股返回 target 日对应的一组折扣证据。历史不足 lookback 个交易日者跳过
    （次新股/长期停牌/缓存缺口——不构成完整的 200 日前高，不冒充折扣）。
    """
    result: Dict[str, Dict[str, Any]] = {}
    if features is None or features.empty or "trade_date" not in features.columns:
        return result

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    for col in ("close", "low"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.loc[df["trade_date"] <= str(target_date)]
    if df.empty or "close" not in df.columns or "low" not in df.columns:
        return result

    for ts_code, sub in df.groupby("ts_code"):
        sub = sub.sort_values("trade_date")
        recent = sub.tail(lookback)
        # 必须有完整的 lookback 个交易日，"最近200日前高"才成立；历史不足者（次新股、
        # 长期停牌、缓存/接口缺口）直接跳过，避免用更短窗口冒充 200 日折扣。
        if len(recent) < lookback:
            continue
        closes = recent["close"].dropna()
        if closes.empty:
            continue
        ph_pos = closes.idxmax()
        ph_date = str(recent.loc[ph_pos, "trade_date"])
        ph_close = safe_float(recent.loc[ph_pos, "close"])
        if ph_close is None or ph_close <= 0 or ph_date >= str(target_date):
            continue  # 前高即今日（窗口内收盘新高）→ 无回撤可言，跳过
        post = recent.loc[recent["trade_date"] > ph_date].copy()
        post["low"] = pd.to_numeric(post["low"], errors="coerce")
        post = post.dropna(subset=["low"])
        if post.empty:
            continue
        pl_idx = post["low"].idxmin()
        pl_date = str(post.loc[pl_idx, "trade_date"])
        post_low = safe_float(post.loc[pl_idx, "low"])
        if post_low is None or post_low <= 0:
            continue
        # 回撤最低点距大涨日的交易日数：在该股已加载的交易日序列里按位置相减。
        recent_dates = recent["trade_date"].tolist()
        last_date = recent_dates[-1]  # ≤ target 的最近交易日（活跃股即 target 当日）
        low_to_target_days = recent_dates.index(last_date) - recent_dates.index(pl_date)
        target_rows = sub.loc[sub["trade_date"] == str(target_date)]
        target_close = safe_float(target_rows["close"].iloc[-1]) if not target_rows.empty else None
        # 月线 10 月均线趋势过滤：把日线收盘按自然月取月末收盘，算 10 月 SMA，
        # 看当前月收盘（= target 日收盘，当月最新）是否站在 10 月线之上。用 to_period
        # 分组而非 resample("ME")，跨 pandas 版本稳。月数不足 10 个则判 None（不可评估）。
        monthly_ma10 = None
        monthly_above_ma10 = None
        mser = sub.dropna(subset=["close"]).copy()
        mser["_period"] = pd.to_datetime(mser["trade_date"], format="%Y%m%d", errors="coerce").dt.to_period("M")
        mser = mser.dropna(subset=["_period"])
        if not mser.empty:
            month_close = mser.groupby("_period")["close"].last()
            if len(month_close) >= 10:
                ma10_val = safe_float(month_close.rolling(10).mean().iloc[-1])
                latest_month_close = safe_float(month_close.iloc[-1])
                if ma10_val is not None and ma10_val > 0 and latest_month_close is not None:
                    monthly_ma10 = round(ma10_val, 2)
                    monthly_above_ma10 = bool(latest_month_close >= ma10_val)
        result[str(ts_code)] = {
            "prev_high_close": round(ph_close, 2),
            "prev_high_date": ph_date,
            "post_low": round(post_low, 2),
            "post_low_date": pl_date,
            "low_to_target_days": int(low_to_target_days),
            "discount_after_high": round(post_low / ph_close, 4),
            "close_vs_prev_high": round(target_close / ph_close, 4) if target_close else None,
            "monthly_ma10": monthly_ma10,
            "monthly_above_ma10": monthly_above_ma10,
        }
    return result


def build_discount_relaunch_samples(
    panel: pd.DataFrame,
    market_cap_threshold_100m_yuan: float,
    amount_threshold_100m_yuan: float,
    pct_chg_threshold: float,
    discount_min: float,
    discount_max: float,
    pre_contraction_max: float,
    volume_expansion_min: float,
    high_lookback: int,
    low_recency_days: int,
    sample_limit: int,
) -> Dict[str, Any]:
    """折扣启动：自前高深度回撤过、调整期缩量、当日重新放量的中大盘上涨股。

    硬性过滤（需同时满足）：
      - 总市值 > market_cap_threshold_100m_yuan（默认 80 亿）
      - 成交额 > amount_threshold_100m_yuan（默认 5 亿）
      - 当日涨幅 > pct_chg_threshold（默认 7%）
      - 前高折扣 discount_after_high = 前高之后最低价 / 前高收盘价，落在
        (discount_min, discount_max) 折价带（默认 0.6~0.85，即自前高最深回撤 15%~40%）。
        前高 = 最近 high_lookback 个交易日（默认 200）收盘价最高日，详见
        attach_discount_after_high；折扣与下面的新鲜度列需由调用方预先附到 panel 上。
      - 最低点新鲜度：回撤最低点距大涨日 low_to_target_days 在 1~low_recency_days 个交易日内
        （默认 5）——即"刚砸出近期最低就放量反包"，排除几周/几个月前的旧坑。
      - 调整期缩量：今日前 5 日均额 / 前 20 日均额 <= pre_contraction_max（默认 0.9）
      - 当日重新放量：amount_vs_prev5_ratio >= volume_expansion_min（默认 2.0），
        即当日量相对最近 5 日缩量期的倍数（不用 20 日均量，避免被前期放量潮抬高基准）
      - 长期趋势：monthly_above_ma10 为真——当前月收盘站在月线 10 月均线之上
        （月末收盘的 10 月 SMA），过滤掉长期趋势已破的折价股；月数不足 10 个无法评估者剔除
      - 排除北交所 / .BJ 与 ST/*ST；前高需可计算（历史不足者剔除）

    排序按成交额降序——放量启动背后的资金体量优先。折扣深度、现价相对前高位置
    （close_vs_prev_high）、缩量比、放量倍数一并输出为证据，强弱与"是否真正调整
    充分、现在是否仍折价"由模型判断，脚本不编码排序意见。
    """
    filter_criteria = {
        "total_mv_100m_yuan_min_exclusive": market_cap_threshold_100m_yuan,
        "amount_100m_yuan_min_exclusive": amount_threshold_100m_yuan,
        "pct_chg_min_exclusive": pct_chg_threshold,
        "discount_after_high_band_exclusive": [discount_min, discount_max],
        "low_to_target_days_max_inclusive": low_recency_days,
        "pre_volume_contraction_ratio_max_inclusive": pre_contraction_max,
        "amount_vs_prev5_ratio_min_inclusive": volume_expansion_min,
        "monthly_above_ma10_required": True,
        "discount_def": f"前高之后最低价 / 前高收盘价；前高=最近{high_lookback}个交易日收盘价最高日；最低点须在大涨日前{low_recency_days}个交易日内",
        "volume_def": "放量=当日量 / 前5日均额（amount_vs_prev5_ratio），不用20日均量",
        "trend_def": "当前月收盘 ≥ 月线10月均线（月末收盘的10月SMA）",
        "exclude": "北交所/.BJ；ST/*ST；前高不可计算（历史不足或今日即收盘新高）；月线在10月线之下或月数不足",
        "sample_limit": sample_limit,
        "sort_by": "成交额降序，其次涨幅降序",
        "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
        "market_cap_unit_note": "Tushare daily_basic 的 total_mv 单位为万元，脚本内部已按亿元阈值换算。",
    }
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": filter_criteria,
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    df = panel.copy()
    for column in (
        "pct_chg", "amount", "total_mv", "circ_mv", "close",
        "turnover_rate", "turnover_rate_f", "volume_ratio",
        "prev_high_close", "post_low", "discount_after_high", "close_vs_prev_high",
        "low_to_target_days", "monthly_ma10", "amount_ratio_20d", "pre_volume_contraction_ratio",
        "amount_vs_prev5_ratio", "pre_ret_5d", "ret_5d", "ret_20d",
        "drawdown_120_high", "close_position_120d",
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    names = df["name"].fillna("").astype(str) if "name" in df.columns else pd.Series("", index=df.index)
    markets = df["market"].fillna("").astype(str) if "market" in df.columns else pd.Series("", index=df.index)
    ts_codes = df["ts_code"].fillna("").astype(str)
    total_mv_100m = df["total_mv"] / 10000 if "total_mv" in df.columns else pd.Series(float("nan"), index=df.index)
    amount_100m = df["amount"] / 100000 if "amount" in df.columns else pd.Series(float("nan"), index=df.index)

    discount = (
        df["discount_after_high"] if "discount_after_high" in df.columns
        else pd.Series(float("nan"), index=df.index)
    )
    discount = pd.to_numeric(discount, errors="coerce")
    contraction = (
        df["pre_volume_contraction_ratio"] if "pre_volume_contraction_ratio" in df.columns
        else pd.Series(float("nan"), index=df.index)
    )
    # 放量基准改为相对最近 5 日缩量期（amount_vs_prev5_ratio），不用 20 日均量。
    expansion = (
        df["amount_vs_prev5_ratio"] if "amount_vs_prev5_ratio" in df.columns
        else pd.Series(float("nan"), index=df.index)
    )
    recency = (
        df["low_to_target_days"] if "low_to_target_days" in df.columns
        else pd.Series(float("nan"), index=df.index)
    )
    # 月线在10月线之上：缺失/None（月数不足、无法评估）按 False 处理 → 剔除。
    above_ma10 = (
        df["monthly_above_ma10"].map(lambda v: v is True)
        if "monthly_above_ma10" in df.columns
        else pd.Series(False, index=df.index)
    )

    qualified = df.loc[
        (total_mv_100m > market_cap_threshold_100m_yuan)
        & (amount_100m > amount_threshold_100m_yuan)
        & (df["pct_chg"].fillna(-999) > pct_chg_threshold)
        & (discount > discount_min)
        & (discount < discount_max)
        & (recency.fillna(99999) >= 1)
        & (recency.fillna(99999) <= low_recency_days)
        & (contraction.fillna(999) <= pre_contraction_max)
        & (expansion.fillna(-999) >= volume_expansion_min)
        & above_ma10
        & ~markets.eq("北交所")
        & ~ts_codes.str.endswith(".BJ")
        & ~names.str.upper().str.contains("ST", na=False)
    ].copy()

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": filter_criteria,
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    qualified = qualified.sort_values(["amount", "pct_chg"], ascending=[False, False]).head(sample_limit)

    trigger_reason = (
        f"总市值>{market_cap_threshold_100m_yuan:g}亿、成交额>{amount_threshold_100m_yuan:g}亿、"
        f"涨幅>{pct_chg_threshold:g}%；自前高（最近{high_lookback}日收盘最高）最深回撤后折扣落在"
        f"{discount_min:g}~{discount_max:g}，且该最低点在大涨日前{low_recency_days:g}个交易日内（刚砸坑就反包）；"
        f"前5日均额≤前20日均额×{pre_contraction_max:g}（调整缩量），当日量≥前5日均额×{volume_expansion_min:g}"
        f"（相对缩量期重新放量）；且当前月收盘站上月线10月均线（长期趋势未破）；排除北交所与ST"
    )

    candidates: List[Dict[str, Any]] = []
    for _, row in qualified.iterrows():
        amount = safe_float(row.get("amount"))
        total_mv = safe_float(row.get("total_mv"))
        circ_mv = safe_float(row.get("circ_mv"))
        candidates.append({
            "ts_code": nullable_value(row.get("ts_code")),
            "name": nullable_value(row.get("name")),
            "market": nullable_value(row.get("market")),
            "pct_chg": round_optional(row.get("pct_chg"), 2),
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "total_mv_100m_yuan": round_optional(total_mv / 10000, 2) if total_mv is not None else None,
            "circ_mv_100m_yuan": round_optional(circ_mv / 10000, 2) if circ_mv is not None else None,
            "close": round_optional(row.get("close"), 2),
            "prev_high_close": round_optional(row.get("prev_high_close"), 2),
            "prev_high_date": nullable_value(row.get("prev_high_date")),
            "post_low": round_optional(row.get("post_low"), 2),
            "post_low_date": nullable_value(row.get("post_low_date")),
            "low_to_target_days": (int(row.get("low_to_target_days")) if pd.notna(row.get("low_to_target_days")) else None),
            "discount_after_high": round_optional(row.get("discount_after_high"), 4),
            "close_vs_prev_high": round_optional(row.get("close_vs_prev_high"), 4),
            "monthly_ma10": round_optional(row.get("monthly_ma10"), 2),
            "monthly_above_ma10": (bool(row.get("monthly_above_ma10")) if row.get("monthly_above_ma10") is not None and pd.notna(row.get("monthly_above_ma10")) else None),
            "close_position_120d": round_optional(row.get("close_position_120d"), 4),
            "amount_ratio_20d": round_optional(row.get("amount_ratio_20d"), 2),
            "pre_volume_contraction_ratio": round_optional(row.get("pre_volume_contraction_ratio"), 2),
            "amount_vs_prev5_ratio": round_optional(row.get("amount_vs_prev5_ratio"), 2),
            "pre_ret_5d": round_optional(row.get("pre_ret_5d"), 2),
            "ret_5d": round_optional(row.get("ret_5d"), 2),
            "ret_20d": round_optional(row.get("ret_20d"), 2),
            "turnover_rate": round_optional(row.get("turnover_rate"), 2),
            "volume_ratio": round_optional(row.get("volume_ratio"), 2),
            "trigger_reason": trigger_reason,
        })

    return {
        "available": True,
        "filter_criteria": filter_criteria,
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "total_amount_100m_yuan": round(sum(float(item.get("amount_100m_yuan") or 0) for item in candidates), 2),
            "median_pct_chg": round_optional(qualified["pct_chg"].median(), 2),
            "median_discount_after_high": round_optional(qualified["discount_after_high"].median(), 4),
            "median_total_mv_100m_yuan": (
                round_optional((qualified["total_mv"] / 10000).median(), 2)
                if "total_mv" in qualified.columns else None
            ),
        },
    }


def code_to_ts_code(code: Any) -> Optional[str]:
    code_str = str(code or "").strip()
    if not code_str:
        return None
    if "." in code_str:
        return code_str
    if len(code_str) != 6 or not code_str.isdigit():
        return None
    if code_str.startswith("6"):
        return f"{code_str}.SH"
    if code_str.startswith(("0", "3")):
        return f"{code_str}.SZ"
    if code_str.startswith(("4", "8", "9")):
        return f"{code_str}.BJ"
    return None


def fetch_jrj_limit_up_records(trade_date: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    if requests is None:
        return [], "requests dependency is not installed"

    headers = {
        "authority": "gateway.jrj.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "deviceinfo": json.dumps({
            "productId": "6000021",
            "version": "1.0.0",
            "device": "Mozilla/5.0",
            "sysName": "Chrome",
            "sysVersion": ["chrome/145.0.0.0"],
        }),
        "origin": "https://summary.jrj.com.cn",
        "productid": "6000021",
        "referer": "https://summary.jrj.com.cn/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    records: List[Dict[str, Any]] = []
    page_size = 100
    try:
        for page_num in range(1, 11):
            payload = {
                "td": trade_date,
                "zdtType": "zt",
                "pageNum": page_num,
                "pageSize": page_size,
            }
            response = requests.post(JRJ_LIMIT_UP_URL, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or data.get("code") != 20000:
                response_code = data.get("code") if isinstance(data, dict) else type(data).__name__
                return records, f"unexpected JRJ response code: {response_code}"
            page_records = data.get("data", {}).get("list", [])
            if not page_records:
                break
            records.extend(page_records)
            if len(page_records) < page_size:
                break
    except Exception as exc:
        return records, str(exc)

    records.sort(key=lambda item: item.get("zdttm", 999999))
    return records, None


def fetch_stock_monthly(
    pro,
    ts_codes: List[str],
    start_date: str,
    end_date: str,
    max_workers: int = 8,
) -> Dict[str, pd.DataFrame]:
    """拉取一组个股的前复权月线行情，用于月线平台突破组的多年底部测算。

    本地 PG / 缓存只覆盖约一年日线，看不到多年底部，必须单拉月线。用 ts.pro_bar(adj='qfq',
    freq='M') 取**前复权**月 K——与生产日线统一的前复权口径一致，避免「现价(qfq) 比 多年箱体
    上沿(raw)」的口径错配（含分红/送转的票尤其要紧）。月线一行一月、体量极小，只在预筛幸存集
    （默认 ≤80 只）上拉取，并发受限、单只失败即跳过。返回 {ts_code: 月线 DataFrame}；pro 不可用
    或全部失败时返回空字典，由调用方降级处理。
    """
    out: Dict[str, pd.DataFrame] = {}
    codes = [str(code).strip() for code in ts_codes if str(code).strip()]
    if pro is None or not codes:
        return out

    def _one(code: str):
        try:
            df = ts.pro_bar(
                ts_code=code,
                api=pro,
                asset="E",
                freq="M",
                adj="qfq",
                start_date=start_date,
                end_date=end_date,
            )
            return code, df
        except Exception:
            return code, None

    with ThreadPoolExecutor(max_workers=max(1, min(max_workers, len(codes)))) as executor:
        for code, df in executor.map(_one, codes):
            if df is not None and not getattr(df, "empty", True):
                out[code] = df
    return out


def build_monthly_base_breakout_samples(
    features: pd.DataFrame,
    target_date: str,
    sample_limit: int,
    pro=None,
    monthly_lookback_months: int = 84,
    up_threshold: float = 7.0,
    breakout_tol: float = 0.02,
    min_base_months: int = 3,
    max_survivors: int = 150,
) -> Dict[str, Any]:
    """全市场月线平台突破（替代原科创板月线突破）。

    形态参照雅克科技：多年月线横盘后，当天放量大涨、日线收盘第一次站上多年箱体上沿。要点：

      - 全市场（排除北交所 / .BJ 与 ST/*ST），不再限定科创板；
      - **当天大涨 + 当天突破**：当日涨幅 ≥ up_threshold（默认 7%），且**昨收 ≤ 箱体上沿 < 今收**
        （今天日线收盘第一次站上箱体上沿），当天下跌或早已站上箱体之上的不算；
      - **横盘长优先、短期也要**：箱体上沿 pivot = 完整月线（回看约 monthly_lookback_months 个月）
        最高价，横盘月数 base_length_months（pivot 成形月 → 当月）≥ min_base_months（默认 3，避免
        次新乱入）即可入选，再按横盘月数降序——多年长底排在前、12 个月内的短底也保留。

    两阶段：阶段一在已加载窗口（约一年日线）上做廉价预筛（当日涨幅 ≥ up_threshold、非北交/ST、
    日线历史够长），按当日成交额取前 max_survivors 只；阶段二对幸存集单拉 Tushare 前复权月 K，
    测算多年箱体上沿 pivot 与横盘月数、确认昨收在 pivot 下、今收在 pivot 上。pro 不可用时本组降级
    为 available=false 并给原因。脚本只给确定性量价证据与月线序列，是否落在 2-3 星主线、归因与取舍
    由模型在写作时叠加（见 module5 方法论）。
    """
    filter_criteria = {
        "universe": "全市场，排除北交所 / .BJ 与 ST/*ST",
        "big_up_day": f"当日涨幅 ≥ {up_threshold}%（当天大涨）",
        "breakout_today": f"昨收 < 箱体上沿 pivot 且 今收 ≥ pivot×(1-{breakout_tol})（昨天没站上多年高、今天放量大涨收在上沿一线以上；下沿单边容差 {breakout_tol:.0%}，上沿敞开；当天下跌或早已在 pivot 之上的不算）",
        "monthly_base": f"箱体上沿 pivot = 完整月线最高价（回看约 {monthly_lookback_months} 个月、不含当月）",
        "min_base_months": f"横盘月数 base_length_months（pivot 成形月 → 当月）≥ {min_base_months}（短期突破也保留、按横盘月数降序）",
        "prefilter": f"阶段一窗口预筛：当日涨幅 ≥ {up_threshold}%、日线历史 ≥ 120 日；按当日成交额取前 {max_survivors} 只再拉月线",
        "sort_by": "横盘月数 base_length_months 降序（横盘越长越好），其次当日成交额降序",
        "sample_limit": sample_limit,
        "reference_shape": "雅克科技 002409.SZ：多年月线箱体后，当天放量大涨站上箱体上沿",
        "data_source": "多年箱体来自 Tushare 前复权月 K（ts.pro_bar adj=qfq freq=M，本地仅约一年日线）；昨收/今收取已加载前复权日线，口径统一",
    }

    def _result(available: bool, candidates=None, series=None, monthly_map=None, reason=None) -> Dict[str, Any]:
        candidates = candidates or []
        series = series or {}
        payload = {
            "available": available,
            "filter_criteria": filter_criteria,
            "candidates": candidates,
            "monthly_series_by_ts_code": series,
            "summary": {
                "candidate_count": len(candidates),
                "survivors_fetched": len(monthly_map or {}),
                "total_amount_100m_yuan": round(sum(float(c.get("amount_100m_yuan") or 0) for c in candidates), 2),
                "max_base_length_months": max((int(c.get("base_length_months") or 0) for c in candidates), default=0),
            },
            "model_overlay": "本组只给技术形态命中；可操作性需模型叠加——仅当个股落在当日 ★★/★★★ 主线内才算主线级信号，否则记为「形态命中但暂不在主线」。",
        }
        if reason:
            payload["reason"] = reason
        return payload

    if features is None or features.empty or "trade_date" not in features.columns:
        return _result(False, reason="无候选日线特征帧")

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    for column in ("open", "high", "low", "close", "pct_chg", "amount", "vol", "history_days", "amount_ratio_20d"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.loc[df["trade_date"] <= str(target_date)]
    target_rows = df.loc[df["trade_date"] == str(target_date)].copy()
    if target_rows.empty:
        return _result(True)

    # 阶段一：全市场预筛（排除北交/ST、**当天大涨** ≥ up_threshold、日线历史够长），按当日成交额取前 N 只。
    names = target_rows["name"].fillna("").astype(str) if "name" in target_rows.columns else pd.Series("", index=target_rows.index)
    markets = target_rows["market"].fillna("").astype(str) if "market" in target_rows.columns else pd.Series("", index=target_rows.index)
    codes_ser = target_rows["ts_code"].fillna("").astype(str)
    keep = (
        ~markets.eq("北交所")
        & ~codes_ser.str.endswith(".BJ")
        & ~names.str.upper().str.contains("ST", na=False)
    )
    target_rows = target_rows.loc[keep].copy()
    if target_rows.empty:
        return _result(True)

    prelim: List[Dict[str, Any]] = []
    for _, row in target_rows.iterrows():
        code = str(row.get("ts_code") or "")
        close = safe_float(row.get("close"))
        pct = safe_float(row.get("pct_chg"))
        hist = safe_float(row.get("history_days"))
        amount = safe_float(row.get("amount"))
        if not code or close is None or pct is None:
            continue
        if pct < up_threshold:  # 当天大涨
            continue
        if hist is not None and hist < 120:
            continue
        prelim.append({"ts_code": code, "amount": amount or 0.0, "row": row})
    if not prelim:
        return _result(True)
    prelim.sort(key=lambda item: -float(item["amount"]))
    prelim = prelim[:max_survivors]

    if pro is None:
        return _result(False, reason="缺少 Tushare pro：无法拉取月线确认多年底部，本组跳过")

    start_dt = (ymd_to_dt(str(target_date)) - timedelta(days=(monthly_lookback_months + 2) * 31)).strftime("%Y%m%d")
    monthly_map = fetch_stock_monthly(pro, [item["ts_code"] for item in prelim], start_dt, str(target_date))
    if not monthly_map:
        return _result(False, reason="Tushare 月线拉取失败或为空，本组跳过")

    cur_month = pd.Period(pd.to_datetime(str(target_date)), freq="M")
    candidates: List[Dict[str, Any]] = []
    series_by_code: Dict[str, Dict[str, Any]] = {}

    for item in prelim:
        code = item["ts_code"]
        row = item["row"]
        mdf = monthly_map.get(code)
        if mdf is None or mdf.empty:
            continue
        mdf = mdf.copy()
        mdf["trade_date"] = mdf["trade_date"].astype(str)
        for col in ("open", "high", "low", "close", "vol"):
            if col in mdf.columns:
                mdf[col] = pd.to_numeric(mdf[col], errors="coerce")
        mdf["_month"] = pd.to_datetime(mdf["trade_date"], format="%Y%m%d", errors="coerce").dt.to_period("M")
        mdf = mdf.dropna(subset=["_month", "close", "high"]).sort_values("_month")
        # 接口里的当前月（可能不完整）丢弃，当前月统一用已加载日线合成。
        completed = mdf.loc[mdf["_month"] < cur_month]
        if len(completed) < min_base_months:
            continue

        # 当前月 bar：用已加载日线本自然月（截至 target）合成。
        cur_daily = df.loc[df["ts_code"] == code].copy()
        cur_daily["_month"] = pd.to_datetime(cur_daily["trade_date"], format="%Y%m%d", errors="coerce").dt.to_period("M")
        cur_daily = cur_daily.loc[cur_daily["_month"] == cur_month].sort_values("trade_date")
        cur_close = safe_float(row.get("close"))
        if cur_close is None and not cur_daily.empty:
            cur_close = safe_float(cur_daily["close"].iloc[-1])
        if cur_close is None:
            continue
        cur_high = safe_float(cur_daily["high"].max()) if not cur_daily.empty else cur_close
        cur_low = safe_float(cur_daily["low"].min()) if not cur_daily.empty else cur_close
        cur_open = safe_float(cur_daily["open"].iloc[0]) if not cur_daily.empty else cur_close
        # 当前月成交量用日线本月累加；Tushare 月线(pro_bar freq=M) 的 vol 以「股」计，日线 vol 以
        # 「手」计，差 100 倍，这里换算到「股」与月线 bar 同口径（既为画图，也保证仅当前月突破时
        # vol_expansion 不被低估 100 倍）。
        cur_vol = (
            safe_float(cur_daily["vol"].sum()) * 100
            if ("vol" in cur_daily.columns and not cur_daily.empty)
            else None
        )

        # 多年箱体上沿 pivot = 完整月线（不含当月）最高价；pivot_month = 该高点所在月。
        pivot = safe_float(completed["high"].max())
        if pivot is None or pivot <= 0:
            continue
        pivot_month = completed.loc[completed["high"].idxmax(), "_month"]

        # 当天突破：昨收还在多年箱体上沿之下（昨天没站上多年高），今天放量大涨、收在上沿一线以上
        # （今收 ≥ 上沿×(1-breakout_tol)）。容差是单边的、只管下沿：雅克这类长底突破常是「大涨日收在
        # 前高一线、次日才收上去」，0 容差会因毫厘漏掉；上沿保持敞开——果断收上箱体的强突破照收，而
        # 「早已冲到箱体上方/已翻倍」的票由「昨收 < 上沿」这条天然挡掉，不需要上限。
        prev_rows = df.loc[(df["ts_code"] == code) & (df["trade_date"] < str(target_date))]
        prev_close = (
            safe_float(prev_rows.sort_values("trade_date")["close"].iloc[-1])
            if not prev_rows.empty else None
        )
        if prev_close is None:
            continue
        if not (prev_close < pivot and cur_close >= pivot * (1.0 - breakout_tol)):
            continue

        # 横盘月数：pivot 成形月 → 当月；短期也保留（≥ min_base_months），长底靠排序排前面。
        base_length_months = (cur_month - pivot_month).n
        if base_length_months < min_base_months:
            continue

        amount = safe_float(row.get("amount"))
        amount_ratio_20d = round_optional(row.get("amount_ratio_20d"), 2)
        # 今收可能略低于上沿（在 breakout_tol 容差内）；措辞要分清「站上」与「收在一线（仍略低）」，
        # 不能一律说成「站上」。close_vs_pivot_pct 已能反映正负，trigger_reason 也据实描述。
        stand_label = "站上" if cur_close >= pivot else f"收在一线（容差 {breakout_tol:.0%} 内、仍略低于上沿）"
        candidates.append({
            "ts_code": code,
            "name": nullable_value(row.get("name")),
            "market": nullable_value(row.get("market")),
            "pct_chg": round_optional(row.get("pct_chg"), 2),
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "close": round_optional(cur_close, 2),
            "prev_close": round_optional(prev_close, 2),
            "base_top_pivot": round_optional(pivot, 2),
            "base_length_months": int(base_length_months),
            "base_start_month": str(pivot_month),
            "breakout_month": str(cur_month),
            "close_vs_pivot_pct": pct_change_optional(cur_close, pivot),
            "amount_ratio_20d": amount_ratio_20d,
            "monthly_history_count": int(len(completed) + 1),
            "trigger_reason": (
                f"全市场；当天涨 {round_optional(row.get('pct_chg'), 2)}%"
                + (f"、放量 {amount_ratio_20d}×20日均量" if amount_ratio_20d is not None else "")
                + f"；今收 {round(cur_close, 2)} 当天第一次{stand_label}多年箱体上沿 {round(pivot, 2)}"
                f"（昨收 {round(prev_close, 2)} 仍在上沿之下），横盘约 {int(base_length_months)} 个月"
            ),
        })

        # 月线序列（供 HTML 月线图：底部箱体阴影 + pivot 线 + 突破月）。
        chart_rows: List[Dict[str, Any]] = []
        for _, mrow in completed.iterrows():
            chart_rows.append({
                "trade_date": str(mrow.get("trade_date")),
                "open": round_optional(mrow.get("open"), 2),
                "high": round_optional(mrow.get("high"), 2),
                "low": round_optional(mrow.get("low"), 2),
                "close": round_optional(mrow.get("close"), 2),
                "vol": round_optional(mrow.get("vol"), 2),
            })
        chart_rows.append({
            "trade_date": str(target_date),
            "open": round_optional(cur_open, 2),
            "high": round_optional(cur_high, 2),
            "low": round_optional(cur_low, 2),
            "close": round_optional(cur_close, 2),
            "vol": round_optional(cur_vol, 2),
        })
        series_by_code[code] = {
            "name": nullable_value(row.get("name")),
            "ts_code": code,
            "base_top_pivot": round_optional(pivot, 2),
            "base_start_month": str(pivot_month),
            "breakout_month": str(cur_month),
            "records": chart_rows[-monthly_lookback_months:],
        }

    candidates.sort(key=lambda it: (
        -int(it.get("base_length_months") or 0),
        -float(it.get("amount_100m_yuan") or 0),
    ))
    candidates = candidates[:sample_limit]
    kept_codes = {c["ts_code"] for c in candidates}
    series_by_code = {k: v for k, v in series_by_code.items() if k in kept_codes}
    return _result(True, candidates=candidates, series=series_by_code, monthly_map=monthly_map)


def build_early_limit_up_1030_samples(
    target_date: str,
    panel: pd.DataFrame,
    basic: pd.DataFrame,
    sample_limit: int,
) -> Dict[str, Any]:
    records, error = fetch_jrj_limit_up_records(target_date)
    if not records and error:
        return {
            "available": False,
            "source": "JRJ zdt record",
            "error": error,
            "filter_criteria": {
                "first_limit_time": "zdttm <= 103000",
                "total_mv_100m_yuan_min": 50,
                "exclude": "ST/*ST",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    def frame_by_ts_code(df: Optional[pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
        if df is None or df.empty or "ts_code" not in df.columns:
            return {}
        indexed = df.copy()
        indexed["ts_code"] = indexed["ts_code"].astype(str)
        return indexed.set_index("ts_code", drop=False).to_dict(orient="index")

    panel_by_ts = frame_by_ts_code(panel)
    basic_by_ts = frame_by_ts_code(basic)

    candidates: List[Dict[str, Any]] = []
    for record in records:
        name = str(record.get("name") or "").strip()
        if "ST" in name.upper():
            continue
        try:
            first_time = int(record.get("zdttm") or 0)
        except Exception:
            first_time = 0
        if first_time <= 0 or first_time > 103000:
            continue

        code = str(record.get("code") or "").strip()
        ts_code = code_to_ts_code(code)
        if not ts_code:
            continue
        panel_row = panel_by_ts.get(ts_code)
        basic_row = basic_by_ts.get(ts_code)

        total_mv_100m = None
        if basic_row is not None:
            total_mv = safe_float(basic_row.get("total_mv"))
            if total_mv is not None:
                total_mv_100m = total_mv / 10000
        if total_mv_100m is None:
            total_mv_100m = safe_float(record.get("total_mv"))
        if total_mv_100m is None or total_mv_100m < 50:
            continue

        amount = safe_float(panel_row.get("amount")) if panel_row is not None else None
        time_str = str(first_time).zfill(6)
        candidates.append({
            "ts_code": ts_code,
            "code": code,
            "name": name or (nullable_value(panel_row.get("name")) if panel_row is not None else None),
            "market": nullable_value(panel_row.get("market")) if panel_row is not None else None,
            "first_limit_time": time_str,
            "first_limit_time_label": f"{time_str[:2]}:{time_str[2:4]}",
            "total_mv_100m_yuan": round(total_mv_100m, 2),
            "pct_chg": round_optional(panel_row.get("pct_chg"), 2) if panel_row is not None else None,
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "close": round_optional(panel_row.get("close"), 2) if panel_row is not None else None,
            "open_times": nullable_value(record.get("open_times")),
            "trigger_reason": "JRJ 涨停池；首次封板时间不晚于 10:30；总市值 >= 50 亿；已过滤 ST",
        })

    candidates.sort(key=lambda item: (
        str(item.get("first_limit_time") or "999999"),
        -float(item.get("total_mv_100m_yuan") or 0),
    ))
    candidates = candidates[:sample_limit]
    return {
        "available": True,
        "source": "JRJ zdt record",
        "error": error,
        "filter_criteria": {
            "first_limit_time": "zdttm <= 103000",
            "total_mv_100m_yuan_min": 50,
            "exclude": "ST/*ST",
            "sample_limit": sample_limit,
            "sort_by": "首次封板时间升序，其次总市值降序",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "source_record_count": len(records),
        },
    }


def build_feature_group_overlaps(groups: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = {
        "capacity_up": "容量上涨",
        "monthly_base_breakout": "全市场月线平台突破",
        "early_limit_up_1030": "10:30前涨停",
        "discount_relaunch": "折扣启动",
    }
    by_code: Dict[str, Dict[str, Any]] = {}
    for group_key, payload in groups.items():
        for candidate in (payload or {}).get("candidates", []) or []:
            ts_code = candidate.get("ts_code")
            if not ts_code:
                continue
            item = by_code.setdefault(ts_code, {
                "ts_code": ts_code,
                "name": candidate.get("name"),
                "matched_groups": [],
                "matched_group_keys": [],
                "group_reasons": {},
                "evidence_by_group": {},
            })
            if not item.get("name") and candidate.get("name"):
                item["name"] = candidate.get("name")
            item["matched_groups"].append(labels.get(group_key, group_key))
            item["matched_group_keys"].append(group_key)
            item["group_reasons"][group_key] = candidate.get("trigger_reason")
            item["evidence_by_group"][group_key] = candidate

    overlaps = [
        {
            **item,
            "matched_group_count": len(item.get("matched_group_keys") or []),
        }
        for item in by_code.values()
        if len(item.get("matched_group_keys") or []) >= 2
    ]
    overlaps.sort(key=lambda item: (-int(item.get("matched_group_count") or 0), str(item.get("ts_code") or "")))
    return overlaps


def build_feature_group_analysis_samples(
    features: pd.DataFrame,
    panel: pd.DataFrame,
    basic: pd.DataFrame,
    candidate_panel: pd.DataFrame,
    target_date: str,
    sample_limit: int,
    capacity_market_cap_threshold_100m_yuan: float,
    capacity_amount_threshold_100m_yuan: float,
    capacity_pct_chg_threshold: float,
    discount_market_cap_threshold_100m_yuan: float,
    discount_amount_threshold_100m_yuan: float,
    discount_pct_chg_threshold: float,
    discount_min: float,
    discount_max: float,
    discount_pre_contraction_max: float,
    discount_volume_expansion_min: float,
    discount_high_lookback: int,
    discount_low_recency_days: int,
    pro=None,
    full_market_features: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    capacity_group = build_capacity_up_samples(
        panel,
        market_cap_threshold_100m_yuan=capacity_market_cap_threshold_100m_yuan,
        amount_threshold_100m_yuan=capacity_amount_threshold_100m_yuan,
        pct_chg_threshold=capacity_pct_chg_threshold,
        sample_limit=sample_limit,
    )
    # 月线平台突破要真·全市场：用全市场多日帧 screening_features 做「当天大涨」预筛，而不是
    # 候选池 features（后者偏向容量/折扣/科创口径，会漏掉低换手的非科创长底突破）。其余组仍用
    # 候选池。无全市场帧时回退到 features。
    monthly_group = build_monthly_base_breakout_samples(
        full_market_features if full_market_features is not None and not full_market_features.empty else features,
        target_date, sample_limit, pro=pro,
    )
    early_group = build_early_limit_up_1030_samples(target_date, panel, basic, sample_limit)
    # 折扣启动需要 candidate_panel（候选池目标日切片，带 daily_basic 市值与量能特征），
    # 折扣本身（前高之后最低价 / 前高收盘价）按多日序列在 features 上另算后附到该切片。
    discount_panel = candidate_panel
    if candidate_panel is not None and not candidate_panel.empty:
        disc_map = attach_discount_after_high(features, target_date, discount_high_lookback)
        discount_panel = candidate_panel.copy()
        keys = discount_panel["ts_code"].astype(str)
        for field in ("prev_high_close", "prev_high_date", "post_low", "post_low_date",
                      "low_to_target_days", "discount_after_high", "close_vs_prev_high",
                      "monthly_ma10", "monthly_above_ma10"):
            discount_panel[field] = keys.map(lambda code, f=field: (disc_map.get(code) or {}).get(f))
    discount_group = build_discount_relaunch_samples(
        discount_panel,
        market_cap_threshold_100m_yuan=discount_market_cap_threshold_100m_yuan,
        amount_threshold_100m_yuan=discount_amount_threshold_100m_yuan,
        pct_chg_threshold=discount_pct_chg_threshold,
        discount_min=discount_min,
        discount_max=discount_max,
        pre_contraction_max=discount_pre_contraction_max,
        volume_expansion_min=discount_volume_expansion_min,
        high_lookback=discount_high_lookback,
        low_recency_days=discount_low_recency_days,
        sample_limit=sample_limit,
    )
    groups = {
        "capacity_up": capacity_group,
        "monthly_base_breakout": monthly_group,
        "early_limit_up_1030": early_group,
        "discount_relaunch": discount_group,
    }
    overlaps = build_feature_group_overlaps(groups)
    return {
        "available": True,
        "groups": groups,
        "overlap_hits": overlaps,
        "summary": {
            "capacity_up_count": len(capacity_group.get("candidates") or []),
            "monthly_base_breakout_count": len(monthly_group.get("candidates") or []),
            "early_limit_up_1030_count": len(early_group.get("candidates") or []),
            "discount_relaunch_count": len(discount_group.get("candidates") or []),
            "overlap_hit_count": len(overlaps),
        },
        "model_responsibility": "脚本只提供分组命中和确定性量价证据；交叉命中上涨归因由模型基于证据包撰写，不在脚本中调用 LLM。",
    }




def compact_record(record: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    source = dict(record)
    if source.get("amount_100m_yuan") is None and source.get("amount") is not None:
        amount = safe_float(source.get("amount"))
        if amount is not None:
            source["amount_100m_yuan"] = round(amount / 100000, 2)
    for field in fields:
        if field in source:
            out[field] = source.get(field)
    return out


def compact_records(records: List[Dict[str, Any]], fields: List[str], limit: int) -> List[Dict[str, Any]]:
    return [compact_record(record, fields) for record in (records or [])[:limit]]


def compact_index_trend(index: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": index.get("name"),
        "ts_code": index.get("ts_code"),
        "latest": index.get("latest"),
        "returns": index.get("returns"),
        "moving_averages": index.get("moving_averages"),
        "volume_price": index.get("volume_price"),
        "levels": index.get("levels"),
        "trend_stage_hint": index.get("trend_stage_hint"),
    }


def compact_market_style_index(index: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "available": index.get("available"),
        "name": index.get("name"),
        "bs_code": index.get("bs_code"),
        "style_role": index.get("style_role"),
        "proxy_note": index.get("proxy_note"),
        "latest": index.get("latest"),
        "returns": index.get("returns"),
        "moving_averages": index.get("moving_averages"),
        "volume_price": index.get("volume_price"),
        "trend_stage_hint": index.get("trend_stage_hint"),
        "reason": index.get("reason"),
    }


def compact_market_style(style: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(style, dict):
        return {}
    return {
        "available": style.get("available"),
        "source": style.get("source"),
        "source_reference": style.get("source_reference"),
        "trade_date": style.get("trade_date"),
        "proxy_notes": style.get("proxy_notes"),
        "indices": {
            key: compact_market_style_index(value)
            for key, value in (style.get("indices") or {}).items()
        },
        "spreads": style.get("spreads"),
        "missing": style.get("missing"),
        "reason": style.get("reason"),
    }


def build_report_context(
    evidence: Dict[str, Any],
    money_limit: int = 80,
    decline_limit: int = 20,
    feature_limit: int = 20,
    amount_limit: int = 20,
) -> Dict[str, Any]:
    money_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "ret_3d",
        "ret_5d",
        "rel_ret_5d",
        "amount_ratio_20d",
        "sustained_volume_days_5",
        "turnover_rate",
        "volume_ratio",
        "close_position_120d",
        "drawdown_120_high",
        "close_to_high",
        "total_mv_100m_yuan",
        "circ_mv_100m_yuan",
        "elasticity_hint_score",
    ]
    decline_fields = money_fields + ["decline_intensity"]
    capacity_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "total_mv_100m_yuan",
        "circ_mv_100m_yuan",
        "close",
        "turnover_rate",
        "volume_ratio",
        "trigger_reason",
    ]
    monthly_base_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "close",
        "prev_close",
        "base_top_pivot",
        "base_length_months",
        "base_start_month",
        "breakout_month",
        "close_vs_pivot_pct",
        "amount_ratio_20d",
        "monthly_history_count",
        "trigger_reason",
    ]
    early_limit_fields = [
        "ts_code",
        "code",
        "name",
        "market",
        "first_limit_time",
        "first_limit_time_label",
        "total_mv_100m_yuan",
        "pct_chg",
        "amount_100m_yuan",
        "close",
        "open_times",
        "trigger_reason",
    ]
    discount_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "total_mv_100m_yuan",
        "circ_mv_100m_yuan",
        "close",
        "prev_high_close",
        "prev_high_date",
        "post_low",
        "post_low_date",
        "low_to_target_days",
        "discount_after_high",
        "close_vs_prev_high",
        "monthly_ma10",
        "monthly_above_ma10",
        "close_position_120d",
        "amount_ratio_20d",
        "pre_volume_contraction_ratio",
        "amount_vs_prev5_ratio",
        "pre_ret_5d",
        "ret_5d",
        "ret_20d",
        "turnover_rate",
        "volume_ratio",
        "trigger_reason",
    ]
    overlap_fields = [
        "ts_code",
        "name",
        "matched_groups",
        "matched_group_count",
        "group_reasons",
    ]
    amount_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "ret_3d",
        "ret_5d",
        "amount_ratio_20d",
    ]

    market_trend = evidence.get("market_trend", {})
    sentiment = dict(market_trend.get("sentiment") or {})
    sentiment.pop("recent_series", None)
    feature_groups = evidence.get("feature_group_analysis_samples") or {}
    feature_group_payload = feature_groups.get("groups") or {}

    return {
        "metadata": {
            **(evidence.get("metadata") or {}),
            "context_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "market_panel.build_report_context",
        },
        "market": {
            "temperature": evidence.get("market_temperature"),
            "temperature_previous": evidence.get("market_temperature_previous"),
            "temperature_change": evidence.get("market_temperature_change"),
            "trend": {
                "sentiment": sentiment,
                "indices": {
                    key: compact_index_trend(value)
                    for key, value in (market_trend.get("indices") or {}).items()
                },
                "market_style": compact_market_style(market_trend.get("market_style") or {}),
            },
        },
        "amount_concentration": {
            "current": (evidence.get("amount_concentration") or {}).get("current"),
            "previous": (evidence.get("amount_concentration") or {}).get("previous"),
            "change": (evidence.get("amount_concentration") or {}).get("change"),
            "trend": (evidence.get("amount_concentration") or {}).get("trend"),
            "top_amount_samples": compact_records(
                (evidence.get("amount_concentration") or {}).get("top_amount_samples", []),
                amount_fields,
                amount_limit,
            ),
        },
        "money_effect": {
            "filter_criteria": (evidence.get("money_effect_samples") or {}).get("filter_criteria"),
            "summary": (evidence.get("money_effect_samples") or {}).get("summary"),
            "theme_grouping_aid": {
                "records": compact_records(
                    (evidence.get("money_effect_samples") or {}).get("candidates", []),
                    money_fields,
                    money_limit,
                ),
                "sorting": "按成交额（亿元）降序；elasticity_hint_score 只辅助识别主线内弹性股，不改写候选池排序。",
                "model_responsibility": "由模型按业务事实归纳主题作为内部判定步骤，报告不输出单独主题分组陈列表；只在 ★★/★★★ 主线内区分领导股与弹性股。不要使用预设行业标签，也不要把弹性提示分当作机械分类器。",
            },
        },
        "volume_decline": {
            "filter_criteria": (evidence.get("volume_decline_samples") or {}).get("filter_criteria"),
            "summary": (evidence.get("volume_decline_samples") or {}).get("summary"),
            "top_candidates": compact_records(
                (evidence.get("volume_decline_samples") or {}).get("candidates", []),
                decline_fields,
                decline_limit,
            ),
        },
        "feature_group_analysis": {
            "summary": feature_groups.get("summary"),
            "model_responsibility": feature_groups.get("model_responsibility"),
            "groups": {
                "capacity_up": {
                    "filter_criteria": (feature_group_payload.get("capacity_up") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("capacity_up") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("capacity_up") or {}).get("candidates", []),
                        capacity_fields,
                        feature_limit,
                    ),
                },
                "monthly_base_breakout": {
                    "available": (feature_group_payload.get("monthly_base_breakout") or {}).get("available"),
                    "reason": (feature_group_payload.get("monthly_base_breakout") or {}).get("reason"),
                    "model_overlay": (feature_group_payload.get("monthly_base_breakout") or {}).get("model_overlay"),
                    "filter_criteria": (feature_group_payload.get("monthly_base_breakout") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("monthly_base_breakout") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("monthly_base_breakout") or {}).get("candidates", []),
                        monthly_base_fields,
                        feature_limit,
                    ),
                },
                "early_limit_up_1030": {
                    "available": (feature_group_payload.get("early_limit_up_1030") or {}).get("available"),
                    "source": (feature_group_payload.get("early_limit_up_1030") or {}).get("source"),
                    "error": (feature_group_payload.get("early_limit_up_1030") or {}).get("error"),
                    "filter_criteria": (feature_group_payload.get("early_limit_up_1030") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("early_limit_up_1030") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("early_limit_up_1030") or {}).get("candidates", []),
                        early_limit_fields,
                        feature_limit,
                    ),
                },
                "discount_relaunch": {
                    "filter_criteria": (feature_group_payload.get("discount_relaunch") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("discount_relaunch") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("discount_relaunch") or {}).get("candidates", []),
                        discount_fields,
                        feature_limit,
                    ),
                },
            },
            "overlap_hits": compact_records(feature_groups.get("overlap_hits", []), overlap_fields, feature_limit),
        },
        "reporting_notes": [
            "本上下文是面向模型的轻量辅助包，不是完整证据归档。",
            "最终主线名称和评级仍由模型依据业务事实与 skill 规则判断。",
            "自动化路径有意省略外部收盘综述校验；模块 3 先完成临时成员映射和确定性统计，由模型锁星后才单独执行催化搜索。",
        ],
    }


def collect_candidate_codes(
    screening_features: pd.DataFrame,
    panel: pd.DataFrame,
    trade_dates: List[str],
    args: argparse.Namespace,
    index_summary: Dict[str, Optional[float]],
) -> Dict[str, Set[str]]:
    """Collect the full-market coarse-screen universe before expensive features."""
    if panel is None or panel.empty:
        empty: Set[str] = set()
        return {"m2": empty, "m3": empty, "m4": empty, "m5": empty}

    amount_money = args.money_amount_threshold * 100000
    amount_decline = args.decline_amount_threshold * 100000
    amount_capacity = args.capacity_amount_threshold * 100000
    market_cap_capacity = args.capacity_market_cap_threshold * 10000

    m2_codes = set(panel.nlargest(min(20, len(panel)), "amount")["ts_code"].dropna().astype(str))
    m3_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(-999) >= args.money_pct_threshold)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) >= amount_money),
            "ts_code",
        ].dropna().astype(str)
    )
    m4_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(999) <= args.decline_pct_max)
            & (pd.to_numeric(panel["amount_ratio_20d"], errors="coerce").fillna(0) >= args.decline_volume_ratio)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) >= amount_decline),
            "ts_code",
        ].dropna().astype(str)
    )

    panel_market = panel["market"].fillna("").astype(str) if "market" in panel.columns else pd.Series("", index=panel.index)
    panel_names = panel["name"].fillna("").astype(str) if "name" in panel.columns else pd.Series("", index=panel.index)
    panel_ts_codes = panel["ts_code"].fillna("").astype(str)
    panel_total_mv = panel["total_mv"] if "total_mv" in panel.columns else pd.Series(0, index=panel.index)
    capacity_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(-999) > args.capacity_pct_threshold)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) > amount_capacity)
            & (pd.to_numeric(panel_total_mv, errors="coerce").fillna(0) > market_cap_capacity)
            & ~panel_market.eq("北交所")
            & ~panel_ts_codes.str.endswith(".BJ")
            & ~panel_names.str.upper().str.contains("ST", na=False),
            "ts_code",
        ].dropna().astype(str)
    )
    # 折扣启动的粗筛只用 panel 现成的硬阈值（涨幅/成交额/市值），把候选股的完整历史
    # 拉进 features；前高折扣与缩量→放量等多日条件在 build_discount_relaunch_samples 精筛。
    amount_discount = args.discount_amount_threshold * 100000
    market_cap_discount = args.discount_market_cap_threshold * 10000
    discount_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(-999) > args.discount_pct_threshold)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) > amount_discount)
            & (pd.to_numeric(panel_total_mv, errors="coerce").fillna(0) > market_cap_discount)
            & ~panel_market.eq("北交所")
            & ~panel_ts_codes.str.endswith(".BJ")
            & ~panel_names.str.upper().str.contains("ST", na=False),
            "ts_code",
        ].dropna().astype(str)
    )
    market = (
        screening_features["market"].fillna("").astype(str)
        if "market" in screening_features.columns
        else pd.Series("", index=screening_features.index)
    )
    ts_codes = screening_features["ts_code"].fillna("").astype(str)
    star_codes = set(
        screening_features.loc[
            market.eq("科创板") | ts_codes.str.startswith(("688", "689")),
            "ts_code",
        ].dropna().astype(str)
    )
    m5_codes = capacity_codes | star_codes | discount_codes

    return {
        "m2": m2_codes,
        "m3": m3_codes,
        "m4": m4_codes,
        "m5": m5_codes,
    }


def build_assembled_checks(evidence: Dict[str, Any]) -> Dict[str, Any]:
    money_records = (evidence.get("money_effect_samples") or {}).get("candidates", [])
    decline_records = (evidence.get("volume_decline_samples") or {}).get("candidates", [])
    decline_by_code = {item.get("ts_code"): item for item in decline_records if item.get("ts_code")}
    overlaps: List[Dict[str, Any]] = []
    for item in money_records:
        ts_code = item.get("ts_code")
        if ts_code in decline_by_code:
            decline = decline_by_code[ts_code]
            overlaps.append({
                "ts_code": ts_code,
                "name": item.get("name") or decline.get("name"),
                "money_amount_100m_yuan": item.get("amount_100m_yuan"),
                "money_pct_chg": item.get("pct_chg"),
                "decline_pct_chg": decline.get("pct_chg"),
                "decline_intensity": decline.get("decline_intensity"),
                "decline_amount_ratio_20d": decline.get("amount_ratio_20d"),
            })

    return {
        "metadata": {
            "resolved_trade_date": (evidence.get("metadata") or {}).get("resolved_trade_date"),
            "source": "market_panel.build_assembled_checks",
        },
        "m3_m4_overlap": {
            "description": "赚钱效应候选池与爆量下跌候选池的交集。只有 M3 ★★★ 主线代表股出现在这里时，最终聚合智能体才应升级为主线见顶预警。",
            "count": len(overlaps),
            "records": overlaps,
        },
    }


def build_module_contexts(evidence: Dict[str, Any]) -> Dict[str, Any]:
    context = build_report_context(evidence)
    metadata = context.get("metadata", {})
    return {
        "meta": {
            "metadata": metadata,
            "subagent_contract": {
                "module1_market_trend": ["module1_market_trend.json", "references/methodology/module1_trend.md", "references/template/section1.md", "盘面趋势"],
                "module2_concentration": ["module2_concentration.json", "references/methodology/module2_concentration.md", "references/template/section2.md", "成交额集中度"],
                "module3_money_effect": ["module3_money_effect.json", "references/methodology/module3_money_effect.md", "module3_theme_map.json", "首轮只做临时主题与成员映射，stars 写 null，不写最终正文"],
                "module3_money_effect_second_stage": [["module3_theme_map.json", "module3_theme_stats.json", "module3_enrichment_pack.json"], "references/methodology/catalyst_subline_mining.md", "references/template/section3.md", "统计后由模型锁星；星级锁定后补催化与细分线路，再写最终模块 3"],
                "module4_decline": ["module4_decline.json", "references/methodology/module4_decline.md", "references/template/section4.md", "爆量下跌风险"],
                "module5_feature_groups": ["module5_feature_groups.json", "references/methodology/module5_feature_groups.md", "references/template/section5.md", "特征分组分析"],
            },
            "aggregation_inputs": ["assembled_checks.json", "references/methodology/output_discipline.md"],
        },
        "module1_market_trend": {
            "metadata": metadata,
            "market": context.get("market"),
            "limit_stats": evidence.get("limit_stats"),
            "limit_stats_change": evidence.get("limit_stats_change"),
        },
        "module2_concentration": {
            "metadata": metadata,
            "amount_concentration": context.get("amount_concentration"),
        },
        "module3_money_effect": {
            "metadata": metadata,
            "money_effect": context.get("money_effect"),
        },
        "module4_decline": {
            "metadata": metadata,
            "volume_decline": context.get("volume_decline"),
        },
        "module5_feature_groups": {
            "metadata": metadata,
            "feature_group_analysis": context.get("feature_group_analysis"),
        },
        "assembled_checks": build_assembled_checks(evidence),
    }


def build_panel(args: argparse.Namespace) -> Dict[str, Any]:
    timer = StageTimer()
    pro = get_pro()
    asof = normalize_date(args.asof)
    cache_enabled = not bool(args.no_cache)
    fetch_workers = max(1, int(getattr(args, "fetch_workers", 1) or 1))
    # 折扣启动的"前高"需要回看 discount_high_lookback 个交易日，月线10月均线还需 ~11 个
    # 自然月（≈230 交易日）的历史，所以实际加载窗口取二者上界并留余量（+50）。其他模块只用
    # 近端数据，多出的历史不改变其结果，仅让候选股的多日特征帧更长。
    effective_lookback = max(args.lookback, int(getattr(args, "discount_high_lookback", 0) or 0) + 50)
    target_date, trade_dates = fetch_trade_dates(
        pro,
        asof,
        effective_lookback,
        args.offset,
        args.allow_future,
        cache_enabled=cache_enabled,
        refresh_cache=args.refresh_cache,
    )
    previous_trade_date = trade_dates[-2] if len(trade_dates) >= 2 else None
    margin_trade_date = previous_trade_date or target_date
    timer.mark("trade_calendar")

    with ThreadPoolExecutor(max_workers=min(fetch_workers, 5)) as executor:
        daily_future = executor.submit(
            fetch_by_trade_dates,
            pro,
            "daily",
            trade_dates,
            DEFAULT_DAILY_FIELDS,
            args.sleep,
            cache_enabled,
            args.refresh_cache,
            fetch_workers,
        )
        adj_factor_future = executor.submit(
            fetch_adj_factors_by_trade_dates,
            pro,
            trade_dates,
            args.sleep,
            cache_enabled,
            args.refresh_cache,
            min(fetch_workers, 3),
        )
        basic_future = executor.submit(
            fetch_by_trade_dates,
            pro,
            "daily_basic",
            [target_date],
            DEFAULT_BASIC_FIELDS,
            args.sleep,
            cache_enabled,
            args.refresh_cache,
            1,
        )
        stock_basic_future = executor.submit(
            fetch_stock_basic,
            pro,
            cache_enabled=cache_enabled,
            refresh_cache=args.refresh_cache,
        )
        index_daily_future = executor.submit(
            fetch_index_daily,
            pro,
            args.index,
            trade_dates[0],
            target_date,
            cache_enabled=cache_enabled,
            refresh_cache=args.refresh_cache,
        )
        margin_future = executor.submit(
            fetch_margin_net_buy,
            pro,
            margin_trade_date,
            cache_enabled,
            args.refresh_cache,
        )

        daily = daily_future.result()
        adj_factors = adj_factor_future.result()
        basic = basic_future.result()
        stock_basic = stock_basic_future.result()
        index_daily = index_daily_future.result()
        margin_net_buy, margin_net_buy_reason = margin_future.result()
    timer.mark("fetch_parallel")

    if daily.empty:
        raise RuntimeError("daily returned no data for the requested window.")

    requested_dates = set(trade_dates)
    loaded_daily_dates = set(daily["trade_date"].astype(str).unique())
    loaded_adj_dates = (
        set(adj_factors["trade_date"].astype(str).unique()) if adj_factors is not None and not adj_factors.empty else set()
    )
    fetch_gaps = {
        "daily": sorted(requested_dates - loaded_daily_dates),
        "adj_factor": sorted(requested_dates - loaded_adj_dates),
        "daily_basic": [] if basic is not None and not basic.empty else [target_date],
        "index_daily": [] if index_daily is not None and not index_daily.empty else [target_date],
    }

    # 板制涨跌停判定必须在 qfq 之前用未复权价格做分位比对。
    limit_flags = compute_limit_flags(daily, stock_basic)
    daily, price_adjustment = apply_qfq_adjustment(daily, adj_factors, target_date)
    timer.mark("qfq_adjustment")

    market_history_update = update_market_history_window(
        target_date,
        trade_dates,
        daily,
        basic,
        pro=pro,
        cache_enabled=cache_enabled,
        refresh_cache=args.refresh_cache,
        margin_net_buy=margin_net_buy,
        margin_net_buy_reason=margin_net_buy_reason,
        margin_net_buy_trade_date=margin_trade_date,
        limit_flags=limit_flags,
    )
    timer.mark("market_history_update")

    # market_trend is network-bound (Tushare index klines + Baostock styles) and
    # independent of the pandas stages below, so it runs concurrently. It must
    # start after update_market_history_window: its sentiment block reads the
    # market_history rows written there.
    market_trend_executor = ThreadPoolExecutor(max_workers=1)
    market_trend_started = time.perf_counter()
    market_trend_future = market_trend_executor.submit(
        build_market_trend,
        pro,
        target_date,
        trade_dates,
        args.market_trend_days,
        args.index_kline_days,
        cache_enabled,
        args.refresh_cache,
    )

    screening_features = add_screening_features(daily)
    timer.mark("screening_features")
    panel = screening_features.loc[screening_features["trade_date"] == target_date].copy()
    if panel.empty:
        raise RuntimeError(f"No daily rows for resolved trade date {target_date}.")
    previous_panel = (
        screening_features.loc[screening_features["trade_date"] == previous_trade_date].copy()
        if previous_trade_date
        else pd.DataFrame()
    )

    panel = merge_optional(panel, basic, ["ts_code", "trade_date"])
    limit_flag_columns = limit_flags[["ts_code", "trade_date", "is_limit_up", "is_limit_down"]] if not limit_flags.empty else pd.DataFrame()
    panel = merge_optional(panel, limit_flag_columns, ["ts_code", "trade_date"])
    if not previous_panel.empty:
        previous_panel = merge_optional(previous_panel, limit_flag_columns, ["ts_code", "trade_date"])

    if not stock_basic.empty:
        panel = panel.merge(stock_basic, on="ts_code", how="left")
        screening_features = screening_features.merge(stock_basic, on="ts_code", how="left")
        if not previous_panel.empty:
            previous_panel = previous_panel.merge(stock_basic, on="ts_code", how="left")
    else:
        panel["name"] = None
        panel["market"] = None
        screening_features["name"] = None
        screening_features["market"] = None
        if not previous_panel.empty:
            previous_panel["name"] = None
            previous_panel["market"] = None

    panel, index_summary = add_index_features(panel, index_daily)
    previous_index_summary = summarize_index(index_daily, previous_trade_date or "")

    candidate_code_groups = collect_candidate_codes(
        screening_features=screening_features,
        panel=panel,
        trade_dates=trade_dates,
        args=args,
        index_summary=index_summary,
    )
    candidate_codes: Set[str] = set().union(*candidate_code_groups.values()) if candidate_code_groups else set()
    candidate_daily = daily.loc[daily["ts_code"].astype(str).isin(candidate_codes)].copy()
    features = add_numeric_features(candidate_daily) if not candidate_daily.empty else pd.DataFrame(columns=daily.columns)
    if not stock_basic.empty and not features.empty:
        features = features.merge(stock_basic, on="ts_code", how="left")
    elif not features.empty:
        features["name"] = None
        features["market"] = None

    candidate_panel = (
        features.loc[features["trade_date"] == target_date].copy()
        if not features.empty and "trade_date" in features.columns
        else pd.DataFrame()
    )
    candidate_panel = merge_optional(candidate_panel, basic, ["ts_code", "trade_date"])
    if not candidate_panel.empty:
        candidate_panel = merge_optional(candidate_panel, limit_flag_columns, ["ts_code", "trade_date"])
        candidate_panel, _ = add_index_features(candidate_panel, index_daily)
    timer.mark("candidate_features")

    limit_df = pd.DataFrame()
    previous_limit_df = pd.DataFrame()
    if args.with_limit and not args.skip_limit:
        limit_df = fetch_limit_list(pro, target_date)
        if previous_trade_date:
            previous_limit_df = fetch_limit_list(pro, previous_trade_date)

    market_temperature = build_market_temperature(panel, index_summary)
    previous_market_temperature = (
        build_market_temperature(previous_panel, previous_index_summary)
        if previous_panel is not None and not previous_panel.empty
        else {}
    )
    limit_stats = build_limit_stats(limit_df)
    previous_limit_stats = build_limit_stats(previous_limit_df)

    money_effect = build_money_effect_samples(
        candidate_panel,
        pct_chg_threshold=args.money_pct_threshold,
        amount_threshold_100m_yuan=args.money_amount_threshold,
        sample_limit=args.money_sample_limit,
    )
    volume_decline = build_volume_decline_samples(
        candidate_panel,
        pct_chg_max=args.decline_pct_max,
        amount_ratio_min=args.decline_volume_ratio,
        amount_threshold_100m_yuan=args.decline_amount_threshold,
        sample_limit=args.decline_sample_limit,
    )
    feature_group_analysis = build_feature_group_analysis_samples(
        features=features,
        panel=panel,
        basic=basic,
        candidate_panel=candidate_panel,
        target_date=target_date,
        sample_limit=args.feature_sample_limit,
        capacity_market_cap_threshold_100m_yuan=args.capacity_market_cap_threshold,
        capacity_amount_threshold_100m_yuan=args.capacity_amount_threshold,
        capacity_pct_chg_threshold=args.capacity_pct_threshold,
        discount_market_cap_threshold_100m_yuan=args.discount_market_cap_threshold,
        discount_amount_threshold_100m_yuan=args.discount_amount_threshold,
        discount_pct_chg_threshold=args.discount_pct_threshold,
        discount_min=args.discount_min,
        discount_max=args.discount_max,
        discount_pre_contraction_max=args.discount_pre_contraction_max,
        discount_volume_expansion_min=args.discount_volume_expansion_min,
        discount_high_lookback=args.discount_high_lookback,
        discount_low_recency_days=args.discount_low_recency_days,
        pro=pro,
        full_market_features=screening_features,
    )
    timer.mark("modules")
    stock_kline_records = build_stock_kline_records(
        daily=daily,
        stock_basic=stock_basic,
        targets=collect_stock_kline_targets(money_effect, feature_group_analysis),
        target_date=target_date,
        kline_days=args.index_kline_days,
    )
    # 月线平台突破组：把月线序列（多年箱体 + pivot + 突破月）注入 kline 展示层供 HTML 月线图，
    # 同时从证据里弹出，避免几十行月线大数组污染模型读取的 evidence 主体。
    monthly_breakout_group = (feature_group_analysis.get("groups") or {}).get("monthly_base_breakout") or {}
    monthly_series = (
        monthly_breakout_group.pop("monthly_series_by_ts_code", {})
        if isinstance(monthly_breakout_group, dict) else {}
    )
    if monthly_series:
        stock_kline_records["monthly"] = {
            "by_ts_code": monthly_series,
            "name_to_ts_code": {
                (item.get("name") or code): code
                for code, item in monthly_series.items()
                if isinstance(item, dict)
            },
        }
    timer.mark("stock_klines")

    try:
        market_trend = market_trend_future.result()
    finally:
        market_trend_executor.shutdown(wait=False)
    timer.mark("market_trend_join_wait")
    timer.timings["market_trend_concurrent"] = round(time.perf_counter() - market_trend_started, 3)
    timer.timings["total"] = timer.total()
    return {
        "metadata": {
            "asof_input": asof,
            "resolved_trade_date": target_date,
            "previous_trade_date": previous_trade_date,
            "offset": args.offset,
            "lookback_trade_days_requested": args.lookback,
            "lookback_trade_days_loaded": len(trade_dates),
            "index_kline_days": int(args.index_kline_days),
            "window_start": trade_dates[0] if trade_dates else None,
            "window_end": target_date,
            "index": args.index,
            "daily_rows": int(len(daily)),
            "panel_rows": int(len(panel)),
            "candidate_feature_rows": int(len(features)),
            "candidate_code_count": int(len(candidate_codes)),
            "candidate_code_counts_by_module": {
                key: int(len(value)) for key, value in candidate_code_groups.items()
            },
            "price_adjustment": price_adjustment,
            "cache_enabled": cache_enabled,
            "cache_root": str(CACHE_ROOT),
            "cached_endpoints": ["daily", "daily_basic", "margin", "stock_basic", "trade_cal", "index_daily", "adj_factor"] if cache_enabled else [],
            "fetch_workers": fetch_workers,
            "future_data_allowed": bool(args.allow_future),
            "stage_timings_seconds": timer.timings,
            "fetch_gaps": fetch_gaps,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "market_temperature": market_temperature,
        "market_temperature_previous": previous_market_temperature,
        "market_temperature_change": (
            build_temperature_comparison(market_temperature, previous_market_temperature)
            if previous_market_temperature
            else {}
        ),
        "market_trend": market_trend,
        "market_history_update": market_history_update,
        "amount_concentration": build_amount_concentration(
            screening_features,
            target_date,
            previous_trade_date,
            sample_features=features,
        ),
        "limit_stats": limit_stats,
        "limit_stats_previous": previous_limit_stats,
        "limit_stats_change": (
            build_limit_comparison(limit_stats, previous_limit_stats)
            if limit_stats.get("available") and previous_limit_stats.get("available")
            else {}
        ),
        "money_effect_samples": money_effect,
        "volume_decline_samples": volume_decline,
        "feature_group_analysis_samples": feature_group_analysis,
        "stock_kline_records": stock_kline_records,
        "notes": [
            "脚本有意不做主题归纳。",
            "不要把市场、行业或概念标签作为预设分组规则；主题应由模型基于证据和业务事实归纳。",
            "Tushare daily 的 amount 单位为千元；total_amount_100m_yuan 已换算为亿元。",
            "limit_up_count / limit_down_count 默认按板制规则精确判定：未复权前收盘 ×(1±板块限幅) 四舍五入到分后与收盘价比对（主板10%、ST 5%、创业/科创20%、北交所30%），limit_detection=board_rule_price_match；flags 不可用时退回 ±9.8% 近似（pct_chg_approx）。判定口径为收盘封板，不含盘中触板回落；官方 limit_list_d 仍可用 --with-limit 拉取对照。",
            "market_trend 只作为模块 1 证据：上证指数、创业板指数、科创50、Baostock 风格代理指数，以及 references/market_data.csv 的情绪趋势。",
            "amount_concentration 只衡量成交额集中度，不分配主题或行业。",
            "个股价格序列统一使用前复权口径：Tushare daily OHLC * adj_factor / 目标日前最新 adj_factor；成交额和成交量仍为原始口径。",
            "指数 K 线来自 Tushare index_daily，不涉及个股复权口径。",
            "市场风格代理指数来自 Baostock query_history_k_data_plus；amount 原始单位为元，amount_100m_yuan 已换算为亿元。Baostock 指数字典未见直接微盘指数，默认用国证2000代理小微盘风格。",
            "money_effect_samples 按涨幅和成交额阈值筛选，并按成交额排序，是每日赚钱效应和上涨主线分析的标准候选池。",
            "volume_decline_samples 按涨跌幅、20日放量倍数和成交额阈值筛选，并按爆量下跌强度（20日放量倍数 * 跌幅绝对值）排序。",
            "feature_group_analysis_samples 是模块 5 的证据包：容量上涨、科创板120日新高且真实月K突破、10:30前涨停、折扣启动四组分别输出，并提供 overlap_hits 供模型做交叉命中上涨归因。折扣启动=市值>80亿、成交额>5亿、涨幅>7%、自前高（最近200日收盘最高）回撤折扣（前高之后最低价/前高收盘）落在0.6~0.85、且该最低点在大涨日前5个交易日内、调整缩量后当日相对前5日均额重新放量(≥2倍)、且当前月收盘站上月线10月均线。",
        ],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Tushare A-share daily market evidence pack.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    panel = subparsers.add_parser("panel", help="Fetch daily-based market evidence pack.")
    panel.add_argument("--asof", default=None, help="Analysis date, YYYYMMDD or YYYY-MM-DD. Defaults to today.")
    panel.add_argument("--offset", type=int, default=0, help="Trading-day offset from asof. Positive offsets require --allow-future.")
    panel.add_argument("--allow-future", action="store_true", help="Allow positive trading-day offsets for post-hoc verification.")
    panel.add_argument("--lookback", type=int, default=120, help="Number of trading days to load.")
    panel.add_argument("--index", default="000300.SH", help="Benchmark index ts_code, default CSI 300.")
    panel.add_argument("--sample-limit", type=int, default=40, help="Max rows in each candidate sample.")
    panel.add_argument("--market-trend-days", type=int, default=90,
                       help="Module 1 market-trend window in trading/history rows (default 90).")
    panel.add_argument("--index-kline-days", type=int, default=DEFAULT_INDEX_KLINE_DAYS,
                       help="Trading-day window for Shanghai/ChiNext HTML candlestick data (default 120).")
    panel.add_argument("--sleep", type=float, default=0.12, help="Sleep seconds between API calls.")
    panel.add_argument("--fetch-workers", type=int, default=6,
                       help="Max worker threads for cache/API fetching. Use 1 for serial debugging.")
    panel.add_argument("--no-cache", action="store_true", help="Disable local daily parquet cache.")
    panel.add_argument("--refresh-cache", action="store_true", help="Force refetch daily data and overwrite local cache.")
    panel.add_argument("--with-limit", action="store_true", help="Fetch official limit_list_d stats. Disabled by default because the endpoint is rate limited.")
    panel.add_argument("--skip-limit", action="store_true", help=argparse.SUPPRESS)

    # Money-effect candidate pool: pct_chg + amount hard thresholds, sorted by amount.
    panel.add_argument("--money-pct-threshold", type=float, default=7.0,
                       help="Money-effect pool: minimum pct_chg in percent (default 7.0).")
    panel.add_argument("--money-amount-threshold", type=float, default=2.0,
                       help="Money-effect pool: minimum amount in 100m yuan (default 2.0 == 2亿).")
    panel.add_argument("--money-sample-limit", type=int, default=80,
                       help="Money-effect pool: max rows after sorting by amount desc (default 80).")

    # Volume-decline (爆量下跌) candidate pool.
    panel.add_argument("--decline-pct-max", type=float, default=-3.0,
                       help="Volume-decline pool: maximum pct_chg in percent, more negative is stricter (default -3.0).")
    panel.add_argument("--decline-volume-ratio", type=float, default=2.0,
                       help="Volume-decline pool: minimum amount_ratio_20d (default 2.0).")
    panel.add_argument("--decline-amount-threshold", type=float, default=1.0,
                       help="Volume-decline pool: minimum amount in 100m yuan (default 1.0 == 1亿).")
    panel.add_argument("--decline-sample-limit", type=int, default=60,
                       help="Volume-decline pool: max rows after sorting (default 60).")

    # Capacity-up (容量上涨) — module 5 feature-group subgroup.
    panel.add_argument("--capacity-market-cap-threshold", type=float, default=70.0,
                       help="Capacity-up pool: minimum total market cap in 100m yuan, exclusive (default 70.0 == 70亿).")
    panel.add_argument("--capacity-amount-threshold", type=float, default=5.0,
                       help="Capacity-up pool: minimum amount in 100m yuan, exclusive (default 5.0 == 5亿).")
    panel.add_argument("--capacity-pct-threshold", type=float, default=8.0,
                       help="Capacity-up pool: minimum pct_chg in percent, exclusive (default 8.0).")
    panel.add_argument("--feature-sample-limit", type=int, default=60,
                       help="Module 5 feature-group max rows per subgroup (default 60).")

    # Discount-relaunch (折扣启动) — module 5 feature-group subgroup.
    panel.add_argument("--discount-market-cap-threshold", type=float, default=80.0,
                       help="Discount-relaunch pool: minimum total market cap in 100m yuan, exclusive (default 80.0 == 80亿).")
    panel.add_argument("--discount-amount-threshold", type=float, default=5.0,
                       help="Discount-relaunch pool: minimum amount in 100m yuan, exclusive (default 5.0 == 5亿).")
    panel.add_argument("--discount-pct-threshold", type=float, default=7.0,
                       help="Discount-relaunch pool: minimum pct_chg in percent, exclusive (default 7.0).")
    panel.add_argument("--discount-min", type=float, default=0.6,
                       help="Discount-relaunch pool: lower bound of close/prev-120d-high discount band, exclusive (default 0.6).")
    panel.add_argument("--discount-max", type=float, default=0.85,
                       help="Discount-relaunch pool: upper bound of close/prev-120d-high discount band, exclusive (default 0.85).")
    panel.add_argument("--discount-pre-contraction-max", type=float, default=0.9,
                       help="Discount-relaunch pool: max prior-5d/prior-20d amount ratio for the adjustment-phase volume contraction (default 0.9).")
    panel.add_argument("--discount-volume-expansion-min", type=float, default=2.0,
                       help="Discount-relaunch pool: min amount_vs_prev5_ratio (today's amount vs the prior-5-day contraction-period average) for the relaunch-day volume expansion (default 2.0).")
    panel.add_argument("--discount-high-lookback", type=int, default=200,
                       help="Discount-relaunch pool: trading-day window for the prior high (close-based) used by the discount = post-high-low / prior-high-close (default 200).")
    panel.add_argument("--discount-low-recency-days", type=int, default=5,
                       help="Discount-relaunch pool: the post-high low must occur within this many trading days before the big-up day (default 5).")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.command == "panel":
        result = build_panel(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
