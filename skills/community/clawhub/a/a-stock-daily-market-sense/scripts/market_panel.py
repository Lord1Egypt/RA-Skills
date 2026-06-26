#!/usr/bin/env python3
"""
Atomic market evidence pack builder for the a-stock-daily-market-sense skill.

The script fetches Tushare data and computes deterministic numeric features.
It intentionally does not name themes, write research reports, or produce
investment recommendations. The model using the skill performs interpretation.
"""

from __future__ import annotations

import argparse
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
    import requests
except ImportError:  # pragma: no cover - optional runtime dependency
    requests = None


DEFAULT_DAILY_FIELDS = (
    "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
)
DEFAULT_BASIC_FIELDS = (
    "ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv,circ_mv"
)
DEFAULT_STOCK_FIELDS = "ts_code,name,market,list_date"
DEFAULT_INDEX_FIELDS = "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
SKILL_ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = SKILL_ROOT / "data" / "cache"
REFERENCE_ROOT = SKILL_ROOT / "reference"
DEFAULT_MARKET_HISTORY_CSV = REFERENCE_ROOT / "market_data.csv"

MARKET_TREND_INDEXES = {
    "shanghai": {"name": "上证指数", "ts_code": "000001.SH"},
    "chinext": {"name": "创业板指数", "ts_code": "399006.SZ"},
}
MARKET_HISTORY_PRIMARY_SOURCE = "akshare.stock_market_activity_legu"
MARKET_HISTORY_SUPPLEMENT_SOURCE = "tushare.daily"
JRJ_LIMIT_UP_URL = "https://gateway.jrj.com/quot-dc/zdt/v1/record"


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
    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y%m%d")
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {value}. Use YYYYMMDD or YYYY-MM-DD.")


def ymd_to_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%d")


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
    out[column] = out[column].astype(str)
    return out.loc[(out[column] >= start_date) & (out[column] <= end_date)].copy()


def missing_edge_ranges(df: pd.DataFrame, column: str, start_date: str, end_date: str) -> List[Tuple[str, str]]:
    if df is None or df.empty or column not in df.columns:
        return [(start_date, end_date)]

    dates = df[column].astype(str)
    cached_min = dates.min()
    cached_max = dates.max()
    ranges: List[Tuple[str, str]] = []
    if start_date < cached_min:
        ranges.append((start_date, (ymd_to_dt(cached_min) - timedelta(days=1)).strftime("%Y%m%d")))
    if end_date > cached_max:
        ranges.append(((ymd_to_dt(cached_max) + timedelta(days=1)).strftime("%Y%m%d"), end_date))
    return [(start, end) for start, end in ranges if start <= end]


def read_cached_frame(endpoint: str, trade_date: str, fields: str) -> Optional[pd.DataFrame]:
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
    dates = list(trade_dates)
    misses: List[str] = []
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
    return pd.concat(frames, ignore_index=True).drop_duplicates()


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
    # New: 15-day previous-mean ratio for the strict low-position spike rule (3x over the 10-15d baseline).
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
    # New: rolling 10-day coefficient of variation of close, used as the "走平/波动收敛" signal in low-position rule B.
    df["close_cv_10d"] = grouped["close"].transform(
        lambda s: s.rolling(10, min_periods=8).std() / s.rolling(10, min_periods=8).mean()
    )
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


def build_market_temperature(panel: pd.DataFrame, index_summary: Dict[str, Optional[float]]) -> Dict[str, Any]:
    total = int(len(panel))
    up = int((panel["pct_chg"] > 0).sum())
    down = int((panel["pct_chg"] < 0).sum())
    flat = total - up - down
    total_amount = float(panel["amount"].sum(skipna=True))
    up_amount = float(panel.loc[panel["pct_chg"] > 0, "amount"].sum(skipna=True))
    down_amount = float(panel.loc[panel["pct_chg"] < 0, "amount"].sum(skipna=True))
    top50_amount = float(panel.nlargest(min(50, total), "amount")["amount"].sum(skipna=True)) if total else 0.0

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
        "limit_up_approx_count": int((panel["pct_chg"] >= 9.8).sum()),
        "limit_down_approx_count": int((panel["pct_chg"] <= -9.8).sum()),
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


def format_history_date(trade_date: str) -> str:
    return datetime.strptime(str(trade_date), "%Y%m%d").strftime("%Y/%m/%d")


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


def upsert_market_history_row(
    row: Dict[str, Any],
    columns: List[str],
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> None:
    """Write one market-history row while preserving existing non-empty values."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    ordered_columns = list(dict.fromkeys(columns + list(row.keys())))

    if csv_path.exists():
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        if "日期" not in df.columns:
            if len(df.columns) == len(ordered_columns):
                df.columns = ordered_columns
            else:
                fixed = list(df.columns)
                if fixed:
                    fixed[0] = "日期"
                    df.columns = fixed

        for col in ordered_columns:
            if col not in df.columns:
                df[col] = ""

        target_date = row.get("日期")
        existing_dates = df["日期"].apply(history_date_to_trade_date)
        target_key = history_date_to_trade_date(target_date)
        matches = df.index[existing_dates == target_key] if target_key else df.index[df["日期"] == target_date]
        if len(matches) > 0:
            idx = matches[0]
            for col, new_value in row.items():
                if col == "日期":
                    continue
                current_value = df.at[idx, col]
                if col == "成交额":
                    if should_fill_turnover(current_value, new_value):
                        df.at[idx, col] = new_value
                    continue
                if col == "全市场换手率":
                    if should_fill_positive_numeric(current_value, new_value):
                        df.at[idx, col] = new_value
                    continue
                if is_blank_value(current_value) and not is_blank_value(new_value):
                    df.at[idx, col] = new_value
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            return

        final_columns = list(df.columns) + [col for col in ordered_columns if col not in df.columns]
        new_row = pd.DataFrame([row], columns=final_columns)
        df = pd.concat([new_row, df.reindex(columns=final_columns)], ignore_index=True)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        return

    pd.DataFrame([row], columns=ordered_columns).to_csv(csv_path, index=False, encoding="utf-8-sig")


def fetch_tushare_market_snapshot_from_daily(
    daily: pd.DataFrame,
    target_date: str,
) -> Tuple[Optional[float], Optional[int], Optional[int], Optional[int]]:
    if daily is None or daily.empty or "trade_date" not in daily.columns:
        return None, None, None, None

    day = daily.loc[daily["trade_date"].astype(str) == str(target_date)].copy()
    if day.empty:
        return None, None, None, None

    total_amount = None
    if "amount" in day.columns:
        amount_series = pd.to_numeric(day["amount"], errors="coerce")
        amount_sum = amount_series.sum(min_count=1)
        if pd.notna(amount_sum) and float(amount_sum) > 0:
            total_amount = float(amount_sum)

    up_count = None
    down_count = None
    flat_count = None
    if "pct_chg" in day.columns:
        pct_series = pd.to_numeric(day["pct_chg"], errors="coerce")
        up_count = int((pct_series > 0).sum())
        down_count = int((pct_series < 0).sum())
        flat_count = int((pct_series == 0).sum())

    return total_amount, up_count, down_count, flat_count


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


def fetch_akshare_market_history_row(target_date: str) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
    detail: Dict[str, Any] = {
        "primary_source": MARKET_HISTORY_PRIMARY_SOURCE,
        "primary_trade_date": None,
        "primary_available": False,
        "fallback_reason": None,
    }
    if ak is None:
        detail["fallback_reason"] = "akshare is not installed"
        return {}, [], detail

    try:
        market_data = ak.stock_market_activity_legu()
    except Exception as exc:
        detail["fallback_reason"] = f"akshare stock_market_activity_legu failed: {exc}"
        return {}, [], detail

    if market_data is None or market_data.empty or "item" not in market_data.columns or "value" not in market_data.columns:
        detail["fallback_reason"] = "akshare stock_market_activity_legu returned empty or invalid data"
        return {}, [], detail

    stat_date = None
    if "统计日期" in market_data["item"].astype(str).values:
        raw_date = market_data.loc[market_data["item"].astype(str) == "统计日期", "value"].values[0]
        parsed = pd.to_datetime(raw_date, errors="coerce")
        if pd.notna(parsed):
            stat_date = parsed.strftime("%Y/%m/%d")

    if not stat_date:
        detail["fallback_reason"] = "akshare data missing 统计日期"
        return {}, [], detail

    stat_trade_date = history_date_to_trade_date(stat_date)
    detail["primary_trade_date"] = stat_trade_date
    if stat_trade_date != target_date:
        detail["fallback_reason"] = f"akshare stat date {stat_trade_date} does not match target date {target_date}"
        return {}, [], detail

    row: Dict[str, Any] = {"日期": stat_date}
    columns = ["日期"]
    for _, item_row in market_data.iterrows():
        item = str(item_row.get("item", "")).strip()
        if not item or item == "统计日期":
            continue
        row[item] = item_row.get("value")
        columns.append(item)
        if len(columns) >= 12:
            break

    detail["primary_available"] = any(not is_blank_value(value) for key, value in row.items() if key != "日期")
    if not detail["primary_available"]:
        detail["fallback_reason"] = "akshare data contains no market activity fields"
        return {}, [], detail
    return row, columns, detail


def update_market_history(
    target_date: str,
    daily: pd.DataFrame,
    daily_basic: Optional[pd.DataFrame] = None,
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> Dict[str, Any]:
    row, columns, detail = fetch_akshare_market_history_row(target_date)
    total_amount, up_count, down_count, flat_count = fetch_tushare_market_snapshot_from_daily(daily, target_date)
    market_turnover_rate, market_turnover_reason = calculate_market_turnover_rate(
        daily,
        daily_basic if daily_basic is not None else pd.DataFrame(),
        target_date,
    )

    fallback_reason = detail.get("fallback_reason")
    if not row:
        row = {"日期": format_history_date(target_date)}
        columns = ["日期"]

    row["成交额"] = total_amount if total_amount is not None else row.get("成交额", "")
    if ("成交额" not in columns):
        columns.append("成交额")

    if ("上涨" not in row or is_blank_value(row.get("上涨"))) and up_count is not None:
        row["上涨"] = up_count
    if "上涨" not in columns:
        columns.append("上涨")

    if ("下跌" not in row or is_blank_value(row.get("下跌"))) and down_count is not None:
        row["下跌"] = down_count
    if "下跌" not in columns:
        columns.append("下跌")

    if ("平盘" not in row or is_blank_value(row.get("平盘"))) and flat_count is not None:
        row["平盘"] = flat_count
    if "平盘" not in columns:
        columns.append("平盘")

    if market_turnover_rate is not None:
        row["全市场换手率"] = market_turnover_rate
    if "全市场换手率" not in columns:
        columns.append("全市场换手率")

    confirmed_values = {
        key: value for key, value in row.items() if key != "日期" and not is_blank_value(value)
    }
    result: Dict[str, Any] = {
        "updated": False,
        "trade_date": target_date,
        "path": str(csv_path),
        "primary_source": MARKET_HISTORY_PRIMARY_SOURCE,
        "supplement_source": MARKET_HISTORY_SUPPLEMENT_SOURCE,
        "primary_trade_date": detail.get("primary_trade_date"),
        "fallback_reason": fallback_reason,
        "market_turnover_rate": market_turnover_rate,
        "market_turnover_rate_unit": "percent",
        "market_turnover_rate_reason": market_turnover_reason,
        "fields": sorted(confirmed_values.keys()),
    }
    if not confirmed_values:
        result["fallback_reason"] = fallback_reason or "no confirmed market history fields from akshare or tushare.daily"
        return result

    try:
        upsert_market_history_row(row, columns, csv_path=csv_path)
    except Exception as exc:
        result["fallback_reason"] = f"failed to update market history csv: {exc}"
        return result

    result["updated"] = True
    return result


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
        "current": current,
        "previous": previous,
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
        "limit_up_approx_count",
        "limit_down_approx_count",
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

    def ratios_for_date(trade_date: str) -> Dict[str, Any]:
        day = df.loc[df["trade_date"] == trade_date].copy()
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
    for trade_date in sorted(df["trade_date"].unique())[-10:]:
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

    day = df.loc[df["trade_date"] == target_date].copy()
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


def build_index_trend_summary(index_daily: pd.DataFrame, index_name: str, ts_code: str, target_date: str, trend_days: int) -> Dict[str, Any]:
    if index_daily is None or index_daily.empty:
        return {
            "available": False,
            "name": index_name,
            "ts_code": ts_code,
            "reason": "index_daily returned no data",
        }

    df = index_daily.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    numeric_cols = ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]
    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.loc[df["trade_date"] <= target_date].sort_values("trade_date")
    df = df.dropna(subset=["close"])
    if df.empty:
        return {
            "available": False,
            "name": index_name,
            "ts_code": ts_code,
            "reason": "no rows on or before target date",
        }

    df = df.tail(max(int(trend_days), 60))
    for period in (1, 5, 20, 60):
        df[f"ret_{period}d"] = pct_return(df["close"], period)
    for period in (5, 20, 60):
        df[f"ma{period}"] = df["close"].rolling(period, min_periods=max(3, period // 2)).mean()

    liquidity_col = "amount" if "amount" in df.columns and df["amount"].notna().any() else "vol"
    if liquidity_col in df.columns:
        df["liquidity_ma5_prev"] = df[liquidity_col].shift(1).rolling(5, min_periods=3).mean()
        df["liquidity_ma20_prev"] = df[liquidity_col].shift(1).rolling(20, min_periods=5).mean()
        df["liquidity_ratio_5d"] = df[liquidity_col] / df["liquidity_ma5_prev"]
        df["liquidity_ratio_20d"] = df[liquidity_col] / df["liquidity_ma20_prev"]
    else:
        df["liquidity_ratio_5d"] = None
        df["liquidity_ratio_20d"] = None

    df["high_20d"] = df["high"].rolling(20, min_periods=5).max() if "high" in df.columns else None
    df["low_20d"] = df["low"].rolling(20, min_periods=5).min() if "low" in df.columns else None
    df["high_60d"] = df["high"].rolling(60, min_periods=20).max() if "high" in df.columns else None
    df["low_60d"] = df["low"].rolling(60, min_periods=20).min() if "low" in df.columns else None

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
    kline_records = df[kline_cols].tail(int(trend_days)).copy()
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
        "kline_days": int(min(int(trend_days), len(kline_records))),
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
            "liquidity_field": liquidity_col if liquidity_col in df.columns else None,
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
    if not csv_path.exists():
        return {
            "available": False,
            "source": str(csv_path),
            "reason": "reference/market_data.csv not found",
        }

    try:
        raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    except Exception as exc:
        return {
            "available": False,
            "source": str(csv_path),
            "reason": f"failed to read market_data.csv: {exc}",
        }

    if raw is None or raw.empty or "日期" not in raw.columns:
        return {
            "available": False,
            "source": str(csv_path),
            "reason": "market_data.csv is empty or missing 日期 column",
        }

    df = raw.copy()
    df["date"] = pd.to_datetime(df["日期"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["trade_date"] = df["date"].dt.strftime("%Y%m%d")
    df = df.loc[df["trade_date"] <= target_date].sort_values("trade_date")
    if df.empty:
        return {
            "available": False,
            "source": str(csv_path),
            "reason": "no sentiment rows on or before target date",
        }

    expected_columns = ["上涨", "下跌", "平盘", "涨停", "跌停", "活跃度", "成交额", "全市场换手率"]
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
        "source": str(csv_path),
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
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    safe_trend_days = max(20, int(trend_days))
    start_date = trade_dates[0] if trade_dates else target_date
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
        )

    return {
        "metadata": {
            "trend_days_requested": safe_trend_days,
            "index_start_date": start_date,
            "index_end_date": target_date,
            "sentiment_source": str(DEFAULT_MARKET_HISTORY_CSV),
            "included_indices": list(MARKET_TREND_INDEXES.keys()),
        },
        "indices": indices,
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
        "amount_ratio_20d",
        "sustained_volume_days_5",
        "turnover_rate",
        "volume_ratio",
        "total_mv",
        "drawdown_120_high",
        "close_position_120d",
    ]


def clean_candidates(df: pd.DataFrame, limit: int) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    cols = [c for c in candidate_columns() if c in df.columns]
    out = df[cols].head(limit).copy()
    if "amount" in out.columns:
        out["amount_100m_yuan"] = pd.to_numeric(out["amount"], errors="coerce") / 100000
    numeric_cols = [c for c in out.columns if c not in {"ts_code", "name", "market", "trade_date"}]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce").round(4)
    out = out.astype(object).where(pd.notnull(out), None)
    return out.to_dict(orient="records")


def build_candidates(panel: pd.DataFrame, sample_limit: int) -> Dict[str, Any]:
    liquid = panel.loc[panel["amount"].fillna(0) > 0].copy()
    if liquid.empty:
        return {
            "strong_samples": [],
            "weak_samples": [],
            "low_position_volume_samples": [],
            "divergence_samples": {"up_against_index": [], "down_against_index": []},
        }

    numeric_inputs = [
        "pct_chg",
        "ret_3d",
        "ret_5d",
        "ret_10d",
        "amount",
        "amount_ratio_20d",
        "sustained_volume_days_5",
        "rel_ret_5d",
        "drawdown_120_high",
        "close_position_120d",
    ]
    for column in numeric_inputs:
        if column in liquid.columns:
            liquid[column] = pd.to_numeric(liquid[column], errors="coerce")

    liquid["strong_score"] = (
        liquid["pct_chg"].fillna(0)
        + liquid["ret_3d"].fillna(0) * 0.4
        + liquid["ret_5d"].fillna(0) * 0.4
        + liquid["amount_ratio_20d"].fillna(1).clip(upper=5) * 1.5
        + liquid["rel_ret_5d"].fillna(0) * 0.4
    )
    liquid["weak_score"] = (
        liquid["pct_chg"].fillna(0)
        + liquid["ret_3d"].fillna(0) * 0.4
        + liquid["ret_5d"].fillna(0) * 0.4
        + liquid["rel_ret_5d"].fillna(0) * 0.4
    )

    strong = liquid.sort_values(["strong_score", "amount"], ascending=[False, False])
    weak = liquid.sort_values(["weak_score", "amount"], ascending=[True, False])

    low_volume = liquid.loc[
        (liquid["drawdown_120_high"].fillna(0) <= -20)
        & (liquid["close_position_120d"].fillna(1) <= 0.35)
        & (liquid["amount_ratio_20d"].fillna(0) >= 1.8)
        & (liquid["ret_3d"].fillna(-999) > 0)
    ].sort_values(["sustained_volume_days_5", "amount_ratio_20d", "ret_5d"], ascending=[False, False, False])

    up_against = liquid.loc[
        (liquid["ret_5d"].fillna(-999) > 0)
        & (liquid["rel_ret_5d"].fillna(-999) >= 5)
        & (liquid["amount_ratio_20d"].fillna(0) >= 1.0)
    ].sort_values(["rel_ret_5d", "ret_5d", "amount"], ascending=[False, False, False])

    down_against = liquid.loc[
        (liquid["ret_5d"].fillna(999) < 0)
        & (liquid["rel_ret_5d"].fillna(999) <= -5)
    ].sort_values(["rel_ret_5d", "ret_5d", "amount"], ascending=[True, True, False])

    return {
        "strong_samples": clean_candidates(strong, sample_limit),
        "weak_samples": clean_candidates(weak, sample_limit),
        "low_position_volume_samples": clean_candidates(low_volume, sample_limit),
        "divergence_samples": {
            "up_against_index": clean_candidates(up_against, sample_limit),
            "down_against_index": clean_candidates(down_against, sample_limit),
        },
    }


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
            "summary": {"candidate_count": 0},
        }

    # daily.amount unit is thousand yuan: 1亿元 = 100000 千元
    amount_threshold_thousand_yuan = amount_threshold_100m_yuan * 100000

    df = panel.copy()
    for column in ("pct_chg", "amount", "ret_3d", "ret_5d", "rel_ret_5d", "amount_ratio_20d"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    qualified = df.loc[
        (df["pct_chg"].fillna(-999) >= pct_chg_threshold)
        & (df["amount"].fillna(0) >= amount_threshold_thousand_yuan)
    ].copy()

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
                "total_amount_100m_yuan": 0.0,
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
        "total_amount_100m_yuan": round(total_amount_100m, 2),
        "median_pct_chg": round(float(qualified["pct_chg"].median()), 2),
        "max_pct_chg": round(float(qualified["pct_chg"].max()), 2),
        "min_pct_chg": round(float(qualified["pct_chg"].min()), 2),
        "median_ret_3d": _safe_median("ret_3d"),
        "median_ret_5d": _safe_median("ret_5d"),
        "median_rel_ret_5d": _safe_median("rel_ret_5d"),
        "median_amount_ratio_20d": _safe_median("amount_ratio_20d"),
        "limit_up_approx_count": int((qualified["pct_chg"] >= 9.8).sum()),
    }

    return {
        "available": True,
        "filter_criteria": {
            "pct_chg_threshold": pct_chg_threshold,
            "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
            "sample_limit": sample_limit,
            "sort_by": "成交额降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
        },
        "candidates": clean_candidates(qualified, sample_limit),
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
        "limit_down_approx_count": int((qualified["pct_chg"] <= -9.8).sum()),
    }

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


def build_low_position_volume_anomaly_samples(
    features: pd.DataFrame,
    target_date: str,
    drawdown_min_abs: float,
    close_position_max: float,
    cv_max: float,
    spike_volume_ratio_min: float,
    spike_pct_chg_min: float,
    lookback_days: int,
    sustain_volume_ratio_min: float,
    quiet_volume_ratio_max: float,
    sample_limit: int,
) -> Dict[str, Any]:
    """
    Low-position volume anomaly samples — three categorized scenarios.

    "Low position" (either A or B is enough):
      A. Close position in the 120d range <= close_position_max (default 0.20),
         i.e. near the historical bottom of the monthly range.
      B. Drawdown from 120d high <= -drawdown_min_abs (default 35%) AND the most
         recent 10 close prices are flat enough: close_cv_10d <= cv_max (default 3%).

    "Volume spike" trigger day requires:
      - amount_ratio_15d >= spike_volume_ratio_min (default 3.0)
      - pct_chg          >= spike_pct_chg_min       (default 7.0)

    Three scenarios based on where the trigger day falls relative to D and what
    the volume / price did afterwards:

      starter      — trigger day == D (today is the spike day).
      sustain      — trigger day is within [D-lookback_days, D-1] AND every
                     post-trigger day has amount >= trigger amount * sustain_volume_ratio_min
                     AND close at D >= open of trigger day. Interpretation: 换手吃筹.
      quiet        — trigger day is within [D-lookback_days, D-1] AND median amount
                     of the most recent 3 days is <= trigger amount * quiet_volume_ratio_max
                     AND close at D >= 0.95 * close of trigger day. Interpretation: 缩量企稳.

    Stocks may match multiple scenarios; we tag each candidate with its primary
    scenario by priority: starter > sustain > quiet.
    """
    if features is None or features.empty:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    for column in (
        "open", "high", "low", "close", "pct_chg", "amount",
        "amount_ratio_15d", "amount_ratio_20d",
        "drawdown_120_high", "close_position_120d", "close_cv_10d",
        "close_ma5", "prev_high_10d", "close_to_high", "history_days",
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Resolve the trade dates around target.
    all_dates = sorted(df["trade_date"].unique())
    if target_date not in all_dates:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }
    target_idx = all_dates.index(target_date)
    lookback_start_idx = max(0, target_idx - lookback_days)
    window_dates = all_dates[lookback_start_idx : target_idx + 1]
    if not window_dates:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    window_df = df.loc[df["trade_date"].isin(window_dates)].copy()

    # Compute "low position" qualifier on each row inside the window:
    # A: close_position_120d <= close_position_max
    # B: drawdown_120_high <= -drawdown_min_abs AND close_cv_10d <= cv_max
    window_df["is_low_A"] = window_df["close_position_120d"].fillna(1.0) <= close_position_max
    window_df["is_low_B"] = (
        (window_df["drawdown_120_high"].fillna(0) <= -drawdown_min_abs)
        & (window_df["close_cv_10d"].fillna(1.0) <= cv_max)
    )
    window_df["is_low_position"] = window_df["is_low_A"] | window_df["is_low_B"]

    names = window_df["name"].fillna("") if "name" in window_df.columns else pd.Series("", index=window_df.index)
    is_special_or_new = names.str.startswith(("ST", "*ST", "退", "C"))
    is_mature = window_df["history_days"].fillna(0) >= 60
    has_1y_amount = window_df["amount"].fillna(0) >= 100000

    # Observation pool: current broad coverage rule.
    window_df["is_observation_trigger"] = (
        window_df["is_low_position"]
        & (window_df["amount_ratio_15d"].fillna(0) >= spike_volume_ratio_min)
        & (window_df["pct_chg"].fillna(-999) >= spike_pct_chg_min)
    )

    # High-quality pool A: deep drawdown + strong thrust.
    window_df["is_high_quality_A"] = (
        (window_df["drawdown_120_high"].fillna(0) <= -45.0)
        & (window_df["amount_ratio_15d"].fillna(0) >= 2.5)
        & (window_df["pct_chg"].fillna(-999) >= 10.0)
        & has_1y_amount
        & is_mature
        & ~is_special_or_new
    )

    # High-quality pool B: broader low zone + strong momentum quality.
    window_df["is_high_quality_B"] = (
        (window_df["close_position_120d"].fillna(1.0) <= 0.35)
        & (window_df["drawdown_120_high"].fillna(0) <= -20.0)
        & (window_df["amount_ratio_15d"].fillna(0) >= 3.0)
        & (window_df["pct_chg"].fillna(-999) >= 15.0)
        & has_1y_amount
        & is_mature
        & ~is_special_or_new
        & (window_df["close"].fillna(0) >= window_df["prev_high_10d"].fillna(float("inf")))
        & (window_df["close_to_high"].fillna(0) >= 0.95)
    )

    # Trigger day can enter through the observation pool or either high-quality pool.
    window_df["is_spike_trigger"] = (
        window_df["is_observation_trigger"]
        | window_df["is_high_quality_A"]
        | window_df["is_high_quality_B"]
    )

    # Build per-stock series indexed by trade_date.
    candidates: List[Dict[str, Any]] = []
    target_rows = window_df.loc[window_df["trade_date"] == target_date].set_index("ts_code")
    triggered_codes = window_df.loc[window_df["is_spike_trigger"], "ts_code"].dropna().unique()
    if len(triggered_codes) == 0:
        return {
            "available": True,
            "filter_criteria": {
                "low_position_rule": (
                    f"A: close_position_120d <= {close_position_max}; "
                    f"B: drawdown_120_high <= -{drawdown_min_abs}% AND close_cv_10d <= {cv_max}"
                ),
                "spike_trigger": (
                    f"amount_ratio_15d >= {spike_volume_ratio_min} AND pct_chg >= {spike_pct_chg_min}"
                ),
                "post_trigger_display_rule": "days_since_trigger == 0 OR today_close >= today_close_ma5",
                "lookback_days_for_trigger": lookback_days,
                "sustain_post_volume_ratio_min": sustain_volume_ratio_min,
                "quiet_post_volume_ratio_max": quiet_volume_ratio_max,
                "sample_limit": sample_limit,
            },
            "candidates": [],
            "summary": {
                "candidate_count": 0,
                "starter_count": 0,
                "sustain_count": 0,
                "quiet_count": 0,
                "undetermined_count": 0,
                "quality_A_count": 0,
                "quality_B_count": 0,
                "quality_A_plus_B_count": 0,
                "quality_C_count": 0,
                "high_quality_A_count": 0,
                "high_quality_B_count": 0,
            },
        }

    grouped = window_df.loc[window_df["ts_code"].isin(triggered_codes)].groupby("ts_code", group_keys=False)
    for ts_code, sub in grouped:
        sub = sub.sort_values("trade_date").reset_index(drop=True)
        if sub.empty or sub["is_spike_trigger"].sum() == 0:
            continue

        # Find the most recent trigger day inside the window.
        trigger_rows = sub.loc[sub["is_spike_trigger"]]
        if trigger_rows.empty:
            continue
        trigger_row = trigger_rows.iloc[-1]
        trigger_date = str(trigger_row["trade_date"])
        trigger_idx_in_window = sub.index[sub["trade_date"] == trigger_date].tolist()
        if not trigger_idx_in_window:
            continue
        t_idx = trigger_idx_in_window[-1]
        days_since_trigger = (len(sub) - 1) - t_idx  # 0 means trigger == today

        target_row = target_rows.loc[ts_code] if ts_code in target_rows.index else None
        if target_row is None:
            continue

        target_close = float(target_row.get("close") or 0)
        target_close_ma5 = target_row.get("close_ma5")
        if days_since_trigger > 0:
            if pd.isna(target_close_ma5) or target_close < float(target_close_ma5):
                continue

        scenario = None
        sustain_ratio = None
        quiet_ratio = None
        post_trigger_days = sub.iloc[t_idx + 1 :]

        if days_since_trigger == 0:
            scenario = "starter"
        else:
            trigger_amount = float(trigger_row.get("amount") or 0)
            trigger_open = float(trigger_row.get("open") or 0)
            trigger_close = float(trigger_row.get("close") or 0)

            # Sustain check: every post-trigger day's amount >= trigger * sustain_ratio_min,
            #                AND target close >= trigger open (price has not collapsed).
            if not post_trigger_days.empty and trigger_amount > 0:
                post_amounts = pd.to_numeric(post_trigger_days["amount"], errors="coerce").dropna()
                if not post_amounts.empty:
                    min_post_ratio = float(post_amounts.min() / trigger_amount)
                    sustain_ratio = round(min_post_ratio, 4)
                    if (
                        min_post_ratio >= sustain_volume_ratio_min
                        and target_close >= trigger_open
                    ):
                        scenario = "sustain"

            # Quiet check: median of last 3 days' amount <= trigger * quiet_ratio_max,
            #              AND target close >= 0.95 * trigger close (price has not broken down).
            if scenario is None and trigger_amount > 0 and trigger_close > 0:
                tail = pd.to_numeric(post_trigger_days["amount"].tail(3), errors="coerce").dropna()
                if not tail.empty:
                    median_post_ratio = float(tail.median() / trigger_amount)
                    quiet_ratio = round(median_post_ratio, 4)
                    if (
                        median_post_ratio <= quiet_volume_ratio_max
                        and target_close >= 0.95 * trigger_close
                    ):
                        scenario = "quiet"

        if scenario is None:
            # Triggered in window but post-trigger behavior matched neither sustain nor quiet:
            # treat as 分歧型 / undetermined; still surface for completeness.
            scenario = "undetermined"

        matched_models: List[str] = []
        if bool(trigger_row.get("is_high_quality_A")):
            matched_models.append("high_quality_A_deep_drawdown_thrust")
        if bool(trigger_row.get("is_high_quality_B")):
            matched_models.append("high_quality_B_broad_momentum_quality")
        matched_model_labels = [
            {
                "high_quality_A_deep_drawdown_thrust": "高质量A：深回撤强启动",
                "high_quality_B_broad_momentum_quality": "高质量B：宽低位强动量质量",
            }.get(model, model)
            for model in matched_models
        ]
        quality_tier = "+".join(["A" if "high_quality_A_deep_drawdown_thrust" in matched_models else "",
                                 "B" if "high_quality_B_broad_momentum_quality" in matched_models else ""]).strip("+")
        if not quality_tier:
            quality_tier = "C"
        scenario_label = {
            "starter": "启动型",
            "sustain": "持续换手型",
            "quiet": "缩量企稳型",
            "undetermined": "分歧型",
        }.get(scenario, scenario)

        candidates.append({
            "ts_code": ts_code,
            "name": nullable_value(target_row.get("name")),
            "market": nullable_value(target_row.get("market")),
            "scenario": scenario,
            "scenario_label": scenario_label,
            "quality_tier": quality_tier,
            "matched_models": matched_models,
            "matched_model_labels": matched_model_labels,
            "observation_pool": bool(trigger_row.get("is_observation_trigger")),
            "trigger_date": trigger_date,
            "days_since_trigger": int(days_since_trigger),
            "trigger_pct_chg": round(float(trigger_row.get("pct_chg") or 0), 2),
            "trigger_amount_ratio_15d": round(float(trigger_row.get("amount_ratio_15d") or 0), 2),
            "trigger_amount_100m_yuan": round(float(trigger_row.get("amount") or 0) / 100000, 2),
            "trigger_drawdown_120_high": round(float(trigger_row.get("drawdown_120_high") or 0), 2),
            "trigger_close_position_120d": (
                round(float(trigger_row.get("close_position_120d")), 4)
                if pd.notna(trigger_row.get("close_position_120d"))
                else None
            ),
            "trigger_close_to_high": (
                round(float(trigger_row.get("close_to_high")), 4)
                if pd.notna(trigger_row.get("close_to_high"))
                else None
            ),
            "trigger_break_prev_high_10d": bool(
                pd.notna(trigger_row.get("prev_high_10d"))
                and float(trigger_row.get("close") or 0) >= float(trigger_row.get("prev_high_10d"))
            ),
            "history_days": (
                int(trigger_row.get("history_days"))
                if pd.notna(trigger_row.get("history_days"))
                else None
            ),
            "trigger_low_track": "+".join(
                track for track, matched in (
                    ("A", bool(trigger_row.get("is_low_A"))),
                    ("B", bool(trigger_row.get("is_low_B"))),
                )
                if matched
            ) or "HQ",
            "post_trigger_min_volume_ratio": sustain_ratio,
            "post_trigger_recent3_volume_ratio": quiet_ratio,
            "today_close": round(float(target_row.get("close") or 0), 2),
            "today_close_ma5": (
                round(float(target_close_ma5), 2)
                if pd.notna(target_close_ma5)
                else None
            ),
            "today_above_ma5": (
                bool(target_close >= float(target_close_ma5))
                if pd.notna(target_close_ma5)
                else None
            ),
            "today_pct_chg": round(float(target_row.get("pct_chg") or 0), 2),
            "today_amount_100m_yuan": round(float(target_row.get("amount") or 0) / 100000, 2),
            "today_drawdown_120_high": round(float(target_row.get("drawdown_120_high") or 0), 2),
            "today_close_position_120d": (
                round(float(target_row.get("close_position_120d")), 4)
                if pd.notna(target_row.get("close_position_120d"))
                else None
            ),
        })

    # Sort: high-quality pools first, then starter/sustain/quiet/undetermined.
    scenario_priority = {"starter": 0, "sustain": 1, "quiet": 2, "undetermined": 3}
    quality_priority = {"A+B": 0, "A": 0, "B": 1, "C": 2}
    candidates.sort(key=lambda r: (
        quality_priority.get(r["quality_tier"], 99),
        scenario_priority.get(r["scenario"], 99),
        -float(r.get("trigger_amount_ratio_15d") or 0),
        -float(r.get("trigger_pct_chg") or 0),
    ))
    candidates = candidates[:sample_limit]

    counts: Dict[str, int] = {"starter": 0, "sustain": 0, "quiet": 0, "undetermined": 0}
    quality_counts: Dict[str, int] = {"A": 0, "B": 0, "A+B": 0, "C": 0}
    model_counts: Dict[str, int] = {
        "high_quality_A_deep_drawdown_thrust": 0,
        "high_quality_B_broad_momentum_quality": 0,
    }
    for c in candidates:
        counts[c["scenario"]] = counts.get(c["scenario"], 0) + 1
        quality_counts[c["quality_tier"]] = quality_counts.get(c["quality_tier"], 0) + 1
        for model in c.get("matched_models") or []:
            model_counts[model] = model_counts.get(model, 0) + 1

    return {
        "available": True,
        "filter_criteria": {
            "low_position_rule_A": f"120日价格分位 <= {close_position_max}",
            "low_position_rule_B": (
                f"距120日高点回撤 <= -{drawdown_min_abs}% 且 10日收盘价变异系数 <= {cv_max}"
            ),
            "spike_volume_ratio_min": spike_volume_ratio_min,
            "spike_pct_chg_min": spike_pct_chg_min,
            "high_quality_pool_A": (
                "距120日高点回撤 <= -45%，15日放量倍数 >= 2.5，"
                "当日涨幅 >= 10%，成交额 >= 1亿，历史交易天数 >= 60，"
                "且排除 ST/*ST/退/C 新股"
            ),
            "high_quality_pool_B": (
                "120日价格分位 <= 0.35，距120日高点回撤 <= -20%，"
                "15日放量倍数 >= 3.0，当日涨幅 >= 15%，成交额 >= 1亿，"
                "收盘价突破前10日高点，收盘/最高 >= 0.95，"
                "历史交易天数 >= 60，且排除 ST/*ST/退/C 新股"
            ),
            "post_trigger_display_rule": "触发日为今日，或今日收盘价仍站在5日均线上方",
            "lookback_days_for_trigger": lookback_days,
            "sustain_post_volume_ratio_min": sustain_volume_ratio_min,
            "quiet_post_volume_ratio_max": quiet_volume_ratio_max,
            "sample_limit": sample_limit,
            "sort_priority": "质量层级 A/A+B > B > C；同层级内按 启动型 > 持续换手型 > 缩量企稳型 > 分歧型 排序",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "starter_count": counts.get("starter", 0),
            "sustain_count": counts.get("sustain", 0),
            "quiet_count": counts.get("quiet", 0),
            "undetermined_count": counts.get("undetermined", 0),
            "quality_A_count": quality_counts.get("A", 0),
            "quality_B_count": quality_counts.get("B", 0),
            "quality_A_plus_B_count": quality_counts.get("A+B", 0),
            "quality_C_count": quality_counts.get("C", 0),
            "high_quality_A_count": model_counts.get("high_quality_A_deep_drawdown_thrust", 0),
            "high_quality_B_count": model_counts.get("high_quality_B_broad_momentum_quality", 0),
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


def build_star_monthly_breakout_samples(
    features: pd.DataFrame,
    target_date: str,
    sample_limit: int,
) -> Dict[str, Any]:
    if features is None or features.empty:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    for column in (
        "open", "high", "low", "close", "pct_chg", "amount",
        "ret_5d", "ret_20d", "amount_ratio_20d", "history_days",
        "prev_high_120d", "close_position_120d", "drawdown_120_high",
        "close_ma20", "close_ma60",
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    target_rows = df.loc[df["trade_date"] == target_date].copy()
    if target_rows.empty:
        return {
            "available": True,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    market = target_rows["market"].fillna("").astype(str) if "market" in target_rows.columns else pd.Series("", index=target_rows.index)
    ts_codes = target_rows["ts_code"].fillna("").astype(str)
    target_rows = target_rows.loc[market.eq("科创板") | ts_codes.str.startswith(("688", "689"))].copy()

    candidates: List[Dict[str, Any]] = []
    grouped = df.loc[df["ts_code"].isin(target_rows["ts_code"])].groupby("ts_code", group_keys=False)
    current_month = pd.Period(pd.to_datetime(target_date), freq="M")

    for ts_code, sub in grouped:
        sub = sub.sort_values("trade_date").reset_index(drop=True)
        target_match = sub.loc[sub["trade_date"] == target_date]
        if target_match.empty:
            continue
        target_row = target_match.iloc[-1]
        history_days = safe_float(target_row.get("history_days")) or 0
        prev_high_120d = safe_float(target_row.get("prev_high_120d"))
        close = safe_float(target_row.get("close"))
        if history_days < 120 or close is None or prev_high_120d is None or close < prev_high_120d:
            continue

        dated = sub.copy()
        dated["_month"] = pd.to_datetime(dated["trade_date"]).dt.to_period("M")
        current_month_rows = dated.loc[dated["_month"] == current_month]
        previous_month_rows = dated.loc[dated["_month"] < current_month]
        if current_month_rows.empty or previous_month_rows.empty:
            continue
        previous_month_high = safe_float(previous_month_rows["high"].max())
        current_month_high = safe_float(current_month_rows["high"].max())
        if previous_month_high is None or close <= previous_month_high:
            continue

        previous_rows = sub.loc[sub["trade_date"] < target_date]
        prior_row = previous_rows.iloc[-1] if not previous_rows.empty else None
        high_trend_excluded = False
        if prior_row is not None:
            prior_close = safe_float(prior_row.get("close"))
            prior_ma20 = safe_float(prior_row.get("close_ma20"))
            prior_ma60 = safe_float(prior_row.get("close_ma60"))
            prior_position = safe_float(prior_row.get("close_position_120d"))
            prior_ret20 = safe_float(prior_row.get("ret_20d"))
            high_trend_excluded = bool(
                prior_close is not None
                and prior_ma20 is not None
                and prior_ma60 is not None
                and prior_position is not None
                and prior_ret20 is not None
                and prior_close > prior_ma20 > prior_ma60
                and prior_position >= 0.70
                and prior_ret20 > 20.0
            )
        if high_trend_excluded:
            continue

        amount = safe_float(target_row.get("amount"))
        candidates.append({
            "ts_code": ts_code,
            "name": nullable_value(target_row.get("name")),
            "market": nullable_value(target_row.get("market")),
            "pct_chg": round_optional(target_row.get("pct_chg"), 2),
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "close": round_optional(close, 2),
            "prev_high_120d": round_optional(prev_high_120d, 2),
            "close_vs_prev_high_120d_pct": pct_change_optional(close, prev_high_120d),
            "previous_complete_month_high": round_optional(previous_month_high, 2),
            "current_month_high": round_optional(current_month_high, 2),
            "close_vs_previous_month_high_pct": pct_change_optional(close, previous_month_high),
            "ret_5d": round_optional(target_row.get("ret_5d"), 2),
            "ret_20d": round_optional(target_row.get("ret_20d"), 2),
            "amount_ratio_20d": round_optional(target_row.get("amount_ratio_20d"), 2),
            "drawdown_120_high": round_optional(target_row.get("drawdown_120_high"), 2),
            "close_position_120d": round_optional(target_row.get("close_position_120d"), 4),
            "trigger_reason": "科创板；今日收盘突破前120日高点；真实自然月K突破此前完整月份高点；未落入高位趋势排除条件",
        })

    candidates.sort(key=lambda item: (
        -float(item.get("amount_100m_yuan") or 0),
        -float(item.get("close_vs_previous_month_high_pct") or 0),
    ))
    candidates = candidates[:sample_limit]
    return {
        "available": True,
        "filter_criteria": {
            "market": "科创板，或 ts_code 以 688/689 开头",
            "new_high": "今日收盘价突破前 120 个交易日最高价",
            "monthly_breakout": "当前自然月最新收盘价突破此前完整自然月最高价",
            "exclude_high_trend": "剔除前一日已处于 close > MA20 > MA60、120日位置 >= 0.70、近20日涨幅 > 20% 的高位趋势样本",
            "sample_limit": sample_limit,
            "sort_by": "成交额（亿元）降序，其次月线突破幅度降序",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "total_amount_100m_yuan": round(sum(float(item.get("amount_100m_yuan") or 0) for item in candidates), 2),
        },
    }


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

    panel_by_ts = {str(row.get("ts_code")): row for _, row in panel.iterrows()} if panel is not None and not panel.empty else {}
    basic_by_ts = {str(row.get("ts_code")): row for _, row in basic.iterrows()} if basic is not None and not basic.empty else {}

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
        "low_position_anomaly": "低位异动",
        "star_120_high_monthly_breakout": "科创板月线突破",
        "early_limit_up_1030": "10:30前涨停",
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
    low_position_anomaly: Dict[str, Any],
    features: pd.DataFrame,
    panel: pd.DataFrame,
    basic: pd.DataFrame,
    target_date: str,
    sample_limit: int,
) -> Dict[str, Any]:
    low_group = {
        "available": low_position_anomaly.get("available", False),
        "filter_criteria": low_position_anomaly.get("filter_criteria"),
        "summary": low_position_anomaly.get("summary"),
        "candidates": low_position_anomaly.get("candidates", []),
    }
    star_group = build_star_monthly_breakout_samples(features, target_date, sample_limit)
    early_group = build_early_limit_up_1030_samples(target_date, panel, basic, sample_limit)
    groups = {
        "low_position_anomaly": low_group,
        "star_120_high_monthly_breakout": star_group,
        "early_limit_up_1030": early_group,
    }
    overlaps = build_feature_group_overlaps(groups)
    return {
        "available": True,
        "groups": groups,
        "overlap_hits": overlaps,
        "summary": {
            "low_position_anomaly_count": len(low_group.get("candidates") or []),
            "star_120_high_monthly_breakout_count": len(star_group.get("candidates") or []),
            "early_limit_up_1030_count": len(early_group.get("candidates") or []),
            "overlap_hit_count": len(overlaps),
        },
        "model_responsibility": "脚本只提供分组命中和确定性量价证据；交叉命中上涨归因由模型基于证据包撰写，不在脚本中调用 LLM。",
    }


def build_resilient_against_index_samples(
    panel: pd.DataFrame,
    index_summary: Dict[str, Optional[float]],
    index_5d_max: float,
    index_10d_max: float,
    rel_ret_5d_min: float,
    ret_5d_min: float,
    amount_threshold_100m_yuan: float,
    sample_limit: int,
) -> Dict[str, Any]:
    """
    "该弱不弱就是强" — find resilient stocks that hold up while the index is weak.

    Skips entirely when index environment is not weak: produces empty candidates
    with a reason field. The model should not list bearish-divergence stocks.

    Index weakness gate (either is enough):
      - index_ret_5d  <= index_5d_max  (default -2.0)
      - index_ret_10d <= index_10d_max (default -3.0)

    Candidate filters (all must pass):
      - rel_ret_5d >= rel_ret_5d_min  (default 5.0pct relative outperformance)
      - ret_5d     >= ret_5d_min      (default 0.0, absolute return positive)
      - amount     >= amount_threshold (default 1亿, ensures real participation)

    Sort: rel_ret_5d desc, then ret_5d desc.
    """
    index_ret_5d = index_summary.get("index_ret_5d") if index_summary else None
    index_ret_10d = index_summary.get("index_ret_10d") if index_summary else None

    weak_environment = False
    weakness_reasons: List[str] = []
    if index_ret_5d is not None and index_ret_5d <= index_5d_max:
        weak_environment = True
        weakness_reasons.append(f"指数5日涨跌幅={index_ret_5d} <= {index_5d_max}")
    if index_ret_10d is not None and index_ret_10d <= index_10d_max:
        weak_environment = True
        weakness_reasons.append(f"指数10日涨跌幅={index_ret_10d} <= {index_10d_max}")

    base = {
        "filter_criteria": {
            "index_5d_max": index_5d_max,
            "index_10d_max": index_10d_max,
            "rel_ret_5d_min": rel_ret_5d_min,
            "ret_5d_min": ret_5d_min,
            "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
            "sample_limit": sample_limit,
            "philosophy": "该弱不弱就是强：只列弱指数环境中的抗跌/逆势上涨候选，不列逆势下跌。",
        },
        "index_environment": {
            "index_ret_5d": index_ret_5d,
            "index_ret_10d": index_ret_10d,
            "is_weak": weak_environment,
            "weakness_reasons": weakness_reasons,
        },
    }

    if not weak_environment:
        return {
            **base,
            "available": True,
            "candidates": [],
            "summary": {
                "candidate_count": 0,
                "skipped_reason": "指数未达到当前弱势门槛，抗跌股筛选按规则跳过。",
            },
        }

    if panel is None or panel.empty:
        return {
            **base,
            "available": False,
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    amount_threshold_thousand_yuan = amount_threshold_100m_yuan * 100000
    df = panel.copy()
    for column in ("ret_5d", "rel_ret_5d", "amount", "pct_chg", "amount_ratio_20d", "drawdown_120_high"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    qualified = df.loc[
        (df["rel_ret_5d"].fillna(-999) >= rel_ret_5d_min)
        & (df["ret_5d"].fillna(-999) >= ret_5d_min)
        & (df["amount"].fillna(0) >= amount_threshold_thousand_yuan)
    ].copy()

    if qualified.empty:
        return {
            **base,
            "available": True,
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    qualified = qualified.sort_values(
        ["rel_ret_5d", "ret_5d", "amount"], ascending=[False, False, False]
    ).head(sample_limit)

    summary = {
        "candidate_count": int(len(qualified)),
        "median_rel_ret_5d": round(float(qualified["rel_ret_5d"].median()), 2),
        "max_rel_ret_5d": round(float(qualified["rel_ret_5d"].max()), 2),
        "median_ret_5d": round(float(qualified["ret_5d"].median()), 2),
        "median_amount_ratio_20d": (
            round(float(qualified["amount_ratio_20d"].median()), 2)
            if "amount_ratio_20d" in qualified.columns
            else None
        ),
    }

    return {
        **base,
        "available": True,
        "candidates": clean_candidates(qualified, sample_limit),
        "summary": summary,
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
        "latest": index.get("latest"),
        "returns": index.get("returns"),
        "moving_averages": index.get("moving_averages"),
        "volume_price": index.get("volume_price"),
        "levels": index.get("levels"),
    }


def build_report_context(
    evidence: Dict[str, Any],
    money_limit: int = 80,
    decline_limit: int = 20,
    low_limit: int = 20,
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
        "close_position_120d",
        "drawdown_120_high",
    ]
    decline_fields = money_fields + ["decline_intensity"]
    low_fields = [
        "ts_code",
        "name",
        "market",
        "scenario",
        "scenario_label",
        "quality_tier",
        "matched_models",
        "matched_model_labels",
        "trigger_date",
        "days_since_trigger",
        "trigger_pct_chg",
        "trigger_amount_ratio_15d",
        "trigger_amount_100m_yuan",
        "trigger_low_track",
        "trigger_drawdown_120_high",
        "trigger_close_position_120d",
        "trigger_close_to_high",
        "trigger_break_prev_high_10d",
        "post_trigger_min_volume_ratio",
        "post_trigger_recent3_volume_ratio",
        "today_close",
        "today_close_ma5",
        "today_amount_100m_yuan",
    ]
    star_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "close",
        "prev_high_120d",
        "close_vs_prev_high_120d_pct",
        "previous_complete_month_high",
        "current_month_high",
        "close_vs_previous_month_high_pct",
        "ret_5d",
        "ret_20d",
        "amount_ratio_20d",
        "drawdown_120_high",
        "close_position_120d",
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
                "sorting": "按成交额（亿元）降序",
                "model_responsibility": "由模型按业务事实归纳主题；不要使用预设行业标签，也不要把该辅助字段当作机械分类器。",
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
        "low_position_volume_anomaly": {
            "filter_criteria": (evidence.get("low_position_volume_anomaly_samples") or {}).get("filter_criteria"),
            "summary": (evidence.get("low_position_volume_anomaly_samples") or {}).get("summary"),
            "candidates": compact_records(
                (evidence.get("low_position_volume_anomaly_samples") or {}).get("candidates", []),
                low_fields,
                low_limit,
            ),
        },
        "feature_group_analysis": {
            "summary": feature_groups.get("summary"),
            "model_responsibility": feature_groups.get("model_responsibility"),
            "groups": {
                "low_position_anomaly": {
                    "filter_criteria": (feature_group_payload.get("low_position_anomaly") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("low_position_anomaly") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("low_position_anomaly") or {}).get("candidates", []),
                        low_fields,
                        low_limit,
                    ),
                },
                "star_120_high_monthly_breakout": {
                    "filter_criteria": (feature_group_payload.get("star_120_high_monthly_breakout") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("star_120_high_monthly_breakout") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("star_120_high_monthly_breakout") or {}).get("candidates", []),
                        star_fields,
                        low_limit,
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
                        low_limit,
                    ),
                },
            },
            "overlap_hits": compact_records(feature_groups.get("overlap_hits", []), overlap_fields, low_limit),
        },
        "resilient_against_index": {
            "index_environment": (evidence.get("resilient_against_index_samples") or {}).get("index_environment"),
            "summary": (evidence.get("resilient_against_index_samples") or {}).get("summary"),
            "candidates": compact_records(
                (evidence.get("resilient_against_index_samples") or {}).get("candidates", []),
                money_fields,
                decline_limit,
            ),
        },
        "reporting_notes": [
            "本上下文是面向模型的轻量辅助包，不是完整证据归档。",
            "最终主线名称和评级仍由模型依据业务事实与 skill 规则判断。",
            "自动化路径有意省略外部收盘综述校验。",
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
        return {"m2": empty, "m3": empty, "m4": empty, "m5": empty, "m6": empty}

    amount_money = args.money_amount_threshold * 100000
    amount_decline = args.decline_amount_threshold * 100000
    amount_resilient = args.resilient_amount_threshold * 100000

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

    low_window = trade_dates[-(max(0, int(args.low_lookback_days)) + 1):]
    m5_codes = set(
        screening_features.loc[
            (screening_features["trade_date"].astype(str).isin(low_window))
            & (pd.to_numeric(screening_features["pct_chg"], errors="coerce").fillna(-999) >= args.low_spike_pct_chg),
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
    m5_codes = m5_codes | star_codes

    index_ret_5d = index_summary.get("index_ret_5d") if index_summary else None
    index_ret_10d = index_summary.get("index_ret_10d") if index_summary else None
    weak_environment = (
        (index_ret_5d is not None and index_ret_5d <= args.resilient_index_5d_max)
        or (index_ret_10d is not None and index_ret_10d <= args.resilient_index_10d_max)
    )
    if weak_environment:
        m6_codes = set(
            panel.loc[
                (pd.to_numeric(panel["ret_5d"], errors="coerce").fillna(-999) >= args.resilient_abs_ret_min)
                & (pd.to_numeric(panel["rel_ret_5d"], errors="coerce").fillna(-999) >= args.resilient_rel_ret_min)
                & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) >= amount_resilient),
                "ts_code",
            ].dropna().astype(str)
        )
    else:
        m6_codes = set()

    return {
        "m2": m2_codes,
        "m3": m3_codes,
        "m4": m4_codes,
        "m5": m5_codes,
        "m6": m6_codes,
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
                "module1_market_trend": ["module1_market_trend.json", "reference/methodology/module1_trend.md", "reference/template/section1.md", "盘面趋势"],
                "module2_concentration": ["module2_concentration.json", "reference/methodology/module2_concentration.md", "reference/template/section2.md", "成交额集中度"],
                "module3_money_effect": ["module3_money_effect.json", "reference/methodology/module3_money_effect.md", "reference/template/section3.md", "赚钱效应与上涨主线"],
                "module4_decline": ["module4_decline.json", "reference/methodology/module4_decline.md", "reference/template/section4.md", "爆量下跌风险"],
                "module5_feature_groups": ["module5_feature_groups.json", "reference/methodology/module5_feature_groups.md", "reference/template/section5.md", "特征分组分析"],
                "module6_resilient": ["module6_resilient.json", "reference/methodology/module6_resilient.md", "reference/template/section6.md", "抗跌股"],
            },
            "aggregation_inputs": ["assembled_checks.json", "reference/methodology/output_discipline.md"],
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
        "module6_resilient": {
            "metadata": metadata,
            "resilient_against_index": context.get("resilient_against_index"),
        },
        "assembled_checks": build_assembled_checks(evidence),
    }


def build_panel(args: argparse.Namespace) -> Dict[str, Any]:
    pro = get_pro()
    asof = normalize_date(args.asof)
    cache_enabled = not bool(args.no_cache)
    fetch_workers = max(1, int(getattr(args, "fetch_workers", 1) or 1))
    target_date, trade_dates = fetch_trade_dates(
        pro,
        asof,
        args.lookback,
        args.offset,
        args.allow_future,
        cache_enabled=cache_enabled,
        refresh_cache=args.refresh_cache,
    )
    previous_trade_date = trade_dates[-2] if len(trade_dates) >= 2 else None

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

        daily = daily_future.result()
        basic = basic_future.result()
        stock_basic = stock_basic_future.result()
        index_daily = index_daily_future.result()

    if daily.empty:
        raise RuntimeError("daily returned no data for the requested window.")

    market_history_update = update_market_history(target_date, daily, basic)
    market_trend = build_market_trend(
        pro,
        target_date,
        trade_dates,
        args.market_trend_days,
        cache_enabled,
        args.refresh_cache,
    )

    screening_features = add_screening_features(daily)
    panel = screening_features.loc[screening_features["trade_date"] == target_date].copy()
    if panel.empty:
        raise RuntimeError(f"No daily rows for resolved trade date {target_date}.")
    previous_panel = (
        screening_features.loc[screening_features["trade_date"] == previous_trade_date].copy()
        if previous_trade_date
        else pd.DataFrame()
    )

    panel = merge_optional(panel, basic, ["ts_code", "trade_date"])

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
        candidate_panel, _ = add_index_features(candidate_panel, index_daily)

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
    low_position_anomaly = build_low_position_volume_anomaly_samples(
        features,
        target_date=target_date,
        drawdown_min_abs=args.low_drawdown_min,
        close_position_max=args.low_close_position_max,
        cv_max=args.low_cv_max,
        spike_volume_ratio_min=args.low_spike_volume_ratio,
        spike_pct_chg_min=args.low_spike_pct_chg,
        lookback_days=args.low_lookback_days,
        sustain_volume_ratio_min=args.low_sustain_ratio,
        quiet_volume_ratio_max=args.low_quiet_ratio,
        sample_limit=args.low_sample_limit,
    )
    feature_group_analysis = build_feature_group_analysis_samples(
        low_position_anomaly=low_position_anomaly,
        features=features,
        panel=panel,
        basic=basic,
        target_date=target_date,
        sample_limit=args.low_sample_limit,
    )
    resilient = build_resilient_against_index_samples(
        candidate_panel,
        index_summary=index_summary,
        index_5d_max=args.resilient_index_5d_max,
        index_10d_max=args.resilient_index_10d_max,
        rel_ret_5d_min=args.resilient_rel_ret_min,
        ret_5d_min=args.resilient_abs_ret_min,
        amount_threshold_100m_yuan=args.resilient_amount_threshold,
        sample_limit=args.resilient_sample_limit,
    )

    return {
        "metadata": {
            "asof_input": asof,
            "resolved_trade_date": target_date,
            "previous_trade_date": previous_trade_date,
            "offset": args.offset,
            "lookback_trade_days_requested": args.lookback,
            "lookback_trade_days_loaded": len(trade_dates),
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
            "cache_enabled": cache_enabled,
            "cache_root": str(CACHE_ROOT),
            "cached_endpoints": ["daily", "daily_basic", "stock_basic", "trade_cal", "index_daily"] if cache_enabled else [],
            "fetch_workers": fetch_workers,
            "future_data_allowed": bool(args.allow_future),
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
        "low_position_volume_anomaly_samples": low_position_anomaly,
        "feature_group_analysis_samples": feature_group_analysis,
        "resilient_against_index_samples": resilient,
        "notes": [
            "脚本有意不做主题归纳。",
            "不要把市场、行业或概念标签作为预设分组规则；主题应由模型基于证据和业务事实归纳。",
            "Tushare daily 的 amount 单位为千元；total_amount_100m_yuan 已换算为亿元。",
            "limit_up_approx_count 和 limit_down_approx_count 是基于日涨跌幅阈值的近似统计。官方 limit_list_d 默认跳过以避免限流，需要时使用 --with-limit。",
            "market_trend 只作为模块 1 证据：上证指数、创业板指数，以及 reference/market_data.csv 的情绪趋势。",
            "amount_concentration 只衡量成交额集中度，不分配主题或行业。",
            "money_effect_samples 按涨幅和成交额阈值筛选，并按成交额排序，是每日赚钱效应和上涨主线分析的标准候选池。",
            "volume_decline_samples 按涨跌幅、20日放量倍数和成交额阈值筛选，并按爆量下跌强度（20日放量倍数 * 跌幅绝对值）排序。",
            "low_position_volume_anomaly_samples 使用严格规则（3倍放量、涨幅7%以上、深回撤或底部区域），并分类为启动型、持续换手型、缩量企稳型和分歧型。",
            "feature_group_analysis_samples 是模块 5 的新证据包：低位异动、科创板120日新高且真实月K突破、10:30前涨停三组分别输出，并提供 overlap_hits 供模型做交叉命中上涨归因。",
            "resilient_against_index_samples 只在弱指数环境输出（该弱不弱就是强），不输出逆势下跌股票。",
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

    # Low-position volume anomaly (低位放量异动) — module 5 feature-group subgroup.
    panel.add_argument("--low-drawdown-min", type=float, default=35.0,
                       help="Low-position pool rule B: minimum |drawdown_120_high| in percent (default 35.0).")
    panel.add_argument("--low-close-position-max", type=float, default=0.20,
                       help="Low-position pool rule A: maximum close_position_120d (default 0.20).")
    panel.add_argument("--low-cv-max", type=float, default=0.03,
                       help="Low-position pool rule B: maximum 10-day close coefficient of variation, the 走平 signal (default 0.03).")
    panel.add_argument("--low-spike-volume-ratio", type=float, default=3.0,
                       help="Low-position pool: minimum amount_ratio_15d for the spike trigger day (default 3.0).")
    panel.add_argument("--low-spike-pct-chg", type=float, default=7.0,
                       help="Low-position pool: minimum pct_chg in percent on the spike trigger day (default 7.0).")
    panel.add_argument("--low-lookback-days", type=int, default=5,
                       help="Low-position pool: how many trading days to look back for the trigger day (default 5).")
    panel.add_argument("--low-sustain-ratio", type=float, default=0.7,
                       help="Sustain scenario: every post-trigger day's amount must be >= sustain_ratio * trigger amount (default 0.7).")
    panel.add_argument("--low-quiet-ratio", type=float, default=0.5,
                       help="Quiet scenario: median of last 3 post-trigger days' amount must be <= quiet_ratio * trigger amount (default 0.5).")
    panel.add_argument("--low-sample-limit", type=int, default=60,
                       help="Low-position pool: max rows after sorting (default 60).")

    # Resilient-against-index (该弱不弱就是强) — module 6.
    panel.add_argument("--resilient-index-5d-max", type=float, default=-2.0,
                       help="Resilient pool: index 5d return must be <= this to count as weak environment (default -2.0).")
    panel.add_argument("--resilient-index-10d-max", type=float, default=-3.0,
                       help="Resilient pool: index 10d return must be <= this to count as weak environment (default -3.0).")
    panel.add_argument("--resilient-rel-ret-min", type=float, default=5.0,
                       help="Resilient pool: minimum 5d relative outperformance vs index in pct (default 5.0).")
    panel.add_argument("--resilient-abs-ret-min", type=float, default=0.0,
                       help="Resilient pool: minimum 5d absolute return in pct (default 0.0).")
    panel.add_argument("--resilient-amount-threshold", type=float, default=1.0,
                       help="Resilient pool: minimum amount in 100m yuan (default 1.0 == 1亿).")
    panel.add_argument("--resilient-sample-limit", type=int, default=40,
                       help="Resilient pool: max rows after sorting (default 40).")

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
