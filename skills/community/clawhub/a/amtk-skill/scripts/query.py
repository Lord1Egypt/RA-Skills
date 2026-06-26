"""Local Parquet/CSV query engine for AMtkSkill data."""

from pathlib import Path

import pandas as pd

from fetcher.common import QUANT_DATA_ROOT, DATA_ROOT
from storage import read_dataset_file


# Dataset layout constants
DATASETS = {
    "market_daily": {
        "dir": "raw/market_daily",
        "suffix": "daily",
    },
    "daily_basic": {
        "dir": "raw/daily_basic",
        "suffix": "daily_basic",
    },
    "adj_factor": {
        "dir": "raw/adj_factor",
        "suffix": "adj_factor",
    },
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _find_latest_stock_basic_csv() -> Path:
    """Find the most recent stock_basic_*.csv in data/."""
    candidates = sorted(DATA_ROOT.glob("stock_basic_*.csv"), reverse=True)
    if not candidates:
        raise RuntimeError(
            f"No stock_basic_*.csv found in {DATA_ROOT}. "
            "Use /run-pipeline stock-list or call fetcher.stock_basic.fetch_and_save_stock_basic() first."
        )
    return candidates[0]


def _parse_yyyymmdd(value: str | None) -> pd.Timestamp | None:
    if value is None:
        return None
    return pd.Timestamp(value)


def _load_partitioned_dataset(
    dataset_name: str,
    ts_code: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    root: Path | None = None,
) -> pd.DataFrame:
    """Scan partition directories, read Parquet files, filter and concatenate."""
    info = DATASETS[dataset_name]
    base_dir = (root or QUANT_DATA_ROOT) / info["dir"]
    suffix = info["suffix"]

    if not base_dir.exists():
        return pd.DataFrame()

    # Determine which symbol directories to scan
    if ts_code:
        from storage import safe_partition_value
        symbol_dirs = [base_dir / safe_partition_value(ts_code)]
    else:
        symbol_dirs = [d for d in sorted(base_dir.iterdir()) if d.is_dir()]

    # Determine which years to look for (optimization)
    start_ts = _parse_yyyymmdd(start_date)
    end_ts = _parse_yyyymmdd(end_date)
    year_filter = None
    if start_ts is not None and end_ts is not None:
        year_filter = set(range(start_ts.year, end_ts.year + 1))

    frames = []
    for symbol_dir in symbol_dirs:
        if not symbol_dir.exists():
            continue

        for parquet_path in sorted(symbol_dir.glob(f"*_{suffix}.parquet")):
            # Extract year from filename like "2026_daily.parquet"
            try:
                year = int(parquet_path.stem.split("_")[0])
            except (ValueError, IndexError):
                continue

            if year_filter and year not in year_filter:
                continue

            csv_path = parquet_path.with_suffix(".csv")
            frame = read_dataset_file(parquet_path, csv_path)
            if not frame.empty:
                frames.append(frame)

        # Fallback to CSV-only files if no parquet found for this symbol
        if not any(symbol_dir.glob(f"*_{suffix}.parquet")):
            for csv_path in sorted(symbol_dir.glob(f"*_{suffix}.csv")):
                try:
                    year = int(csv_path.stem.split("_")[0])
                except (ValueError, IndexError):
                    continue
                if year_filter and year not in year_filter:
                    continue

                frame = read_dataset_file(csv_path.with_suffix(".parquet"), csv_path)
                if not frame.empty:
                    frames.append(frame)

    if not frames:
        return pd.DataFrame()

    data = pd.concat(frames, ignore_index=True)

    # Normalize trade_date
    if "trade_date" in data.columns:
        data["trade_date"] = pd.to_datetime(data["trade_date"], errors="coerce")

        if start_ts is not None:
            data = data[data["trade_date"] >= start_ts]
        if end_ts is not None:
            data = data[data["trade_date"] <= end_ts]

        data = data.sort_values("trade_date").reset_index(drop=True)

    return data


# ---------------------------------------------------------------------------
# Public data loading functions
# ---------------------------------------------------------------------------

def load_stock_basic(list_status: str | None = "L") -> pd.DataFrame:
    """Load the latest stock_basic CSV from data/."""
    csv_path = _find_latest_stock_basic_csv()
    data = pd.read_csv(csv_path, encoding="utf-8-sig")
    if list_status and "list_status" in data.columns:
        data = data[data["list_status"] == list_status]
    return data.reset_index(drop=True)


def load_market_daily(
    ts_code: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Load market_daily Parquet files. Filter by stock code and/or date range."""
    return _load_partitioned_dataset("market_daily", ts_code, start_date, end_date)


def load_daily_basic(
    ts_code: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Load daily_basic Parquet files. Filter by stock code and/or date range."""
    return _load_partitioned_dataset("daily_basic", ts_code, start_date, end_date)


def load_adj_factor(
    ts_code: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Load adj_factor Parquet files. Filter by stock code and/or date range."""
    return _load_partitioned_dataset("adj_factor", ts_code, start_date, end_date)


def load_full_daily(
    ts_code: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Load and merge market_daily + daily_basic + adj_factor for one stock."""
    daily = load_market_daily(ts_code, start_date, end_date)
    if daily.empty:
        return daily

    basic = load_daily_basic(ts_code, start_date, end_date)
    adj = load_adj_factor(ts_code, start_date, end_date)

    result = daily
    if not basic.empty:
        merge_cols = [c for c in basic.columns if c not in ("ts_code", "trade_date")]
        result = result.merge(
            basic[["ts_code", "trade_date"] + merge_cols],
            on=["ts_code", "trade_date"],
            how="left",
        )
    if not adj.empty:
        merge_cols = [c for c in adj.columns if c not in ("ts_code", "trade_date")]
        result = result.merge(
            adj[["ts_code", "trade_date"] + merge_cols],
            on=["ts_code", "trade_date"],
            how="left",
        )

    return result


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def data_overview() -> pd.DataFrame:
    """Return row counts, date ranges, and stock counts per dataset."""
    rows = []
    for name in DATASETS:
        data = _load_partitioned_dataset(name)
        if data.empty:
            rows.append({"dataset": name, "rows": 0, "stocks": 0, "min_date": None, "max_date": None})
        else:
            rows.append({
                "dataset": name,
                "rows": len(data),
                "stocks": data["ts_code"].nunique() if "ts_code" in data.columns else 0,
                "min_date": data["trade_date"].min() if "trade_date" in data.columns else None,
                "max_date": data["trade_date"].max() if "trade_date" in data.columns else None,
            })

    # Add stock_basic
    try:
        sb = load_stock_basic(list_status=None)
        rows.append({
            "dataset": "stock_basic",
            "rows": len(sb),
            "stocks": len(sb),
            "min_date": None,
            "max_date": None,
        })
    except RuntimeError:
        rows.append({"dataset": "stock_basic", "rows": 0, "stocks": 0, "min_date": None, "max_date": None})

    return pd.DataFrame(rows)


def search_stocks(
    keyword: str | None = None,
    industry: str | None = None,
    exchange: str | None = None,
) -> pd.DataFrame:
    """Search stock_basic by name/keyword, industry, or exchange."""
    data = load_stock_basic(list_status=None)

    if keyword:
        mask = (
            data["name"].astype(str).str.contains(keyword, na=False)
            | data["ts_code"].astype(str).str.contains(keyword, na=False)
            | data["cnspell"].astype(str).str.contains(keyword, na=False, case=False)
        )
        data = data[mask]

    if industry:
        data = data[data["industry"].astype(str).str.contains(industry, na=False)]

    if exchange:
        data = data[data["exchange"] == exchange]

    return data.reset_index(drop=True)


def latest_trading_date() -> str | None:
    """Return the most recent trade_date found in market_daily data (YYYYMMDD)."""
    base_dir = QUANT_DATA_ROOT / "raw" / "market_daily"
    if not base_dir.exists():
        return None

    max_date = None
    # Sample a few symbol directories for performance
    symbol_dirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])
    sample = symbol_dirs[:10] if len(symbol_dirs) > 10 else symbol_dirs

    for symbol_dir in sample:
        parquet_files = sorted(symbol_dir.glob("*_daily.parquet"), reverse=True)
        if not parquet_files:
            continue
        # Read the most recent year file only
        frame = read_dataset_file(parquet_files[0], parquet_files[0].with_suffix(".csv"))
        if not frame.empty and "trade_date" in frame.columns:
            frame["trade_date"] = pd.to_datetime(frame["trade_date"], errors="coerce")
            local_max = frame["trade_date"].max()
            if max_date is None or local_max > max_date:
                max_date = local_max

    if max_date is None:
        return None
    return max_date.strftime("%Y%m%d")


def cross_section(
    trade_date: str,
    sort_by: str = "amount",
    ascending: bool = False,
    limit: int = 20,
) -> pd.DataFrame:
    """Get all stocks for a given date, joined with stock_basic for names."""
    daily = _load_partitioned_dataset("market_daily", start_date=trade_date, end_date=trade_date)
    if daily.empty:
        return daily

    ts = pd.Timestamp(trade_date)
    daily = daily[daily["trade_date"] == ts]
    if daily.empty:
        return daily

    try:
        sb = load_stock_basic(list_status=None)
        daily = daily.merge(sb[["ts_code", "name", "industry"]], on="ts_code", how="left")
    except RuntimeError:
        pass

    if sort_by in daily.columns:
        daily = daily.sort_values(sort_by, ascending=ascending)

    return daily.head(limit).reset_index(drop=True)


def top_movers(
    trade_date: str,
    direction: str = "up",
    limit: int = 10,
) -> pd.DataFrame:
    """Calculate change_pct based on close prices, return top movers for a given date."""
    ts = pd.Timestamp(trade_date)

    # Load a window around the target date to get previous trading day
    start_dt = ts - pd.Timedelta(days=10)
    daily = _load_partitioned_dataset(
        "market_daily",
        start_date=start_dt.strftime("%Y%m%d"),
        end_date=trade_date,
    )
    if daily.empty:
        return daily

    # Get all trading dates and find the previous one
    all_dates = sorted(daily["trade_date"].unique())
    if ts not in all_dates:
        return pd.DataFrame()

    ts_idx = list(all_dates).index(ts)
    if ts_idx == 0:
        return pd.DataFrame()

    prev_date = all_dates[ts_idx - 1]

    today = daily[daily["trade_date"] == ts][["ts_code", "close"]].rename(columns={"close": "close_today"})
    prev = daily[daily["trade_date"] == prev_date][["ts_code", "close"]].rename(columns={"close": "close_prev"})

    merged = today.merge(prev, on="ts_code", how="inner")
    merged["change_pct"] = ((merged["close_today"] - merged["close_prev"]) / merged["close_prev"] * 100).round(2)

    ascending = direction != "up"
    merged = merged.sort_values("change_pct", ascending=ascending)

    try:
        sb = load_stock_basic(list_status=None)
        merged = merged.merge(sb[["ts_code", "name", "industry"]], on="ts_code", how="left")
    except RuntimeError:
        pass

    return merged.head(limit).reset_index(drop=True)
