"""Fetch stock_basic list from Tushare API."""

from datetime import datetime
from pathlib import Path

import pandas as pd

from fetcher.common import DATA_ROOT, create_tushare_pro, tushare_request


STOCK_BASIC_FIELDS = (
    "ts_code,symbol,name,area,industry,fullname,enname,"
    "cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"
)

STOCK_BASIC_COLUMNS = [
    "ts_code", "symbol", "name", "area", "industry", "fullname", "enname",
    "cnspell", "market", "exchange", "curr_type", "list_status", "list_date",
    "delist_date", "is_hs",
]


def fetch_stock_basic(
    token: str | None = None,
    list_status: str = "L",
    exchange: str | None = None,
) -> pd.DataFrame:
    """Fetch stock_basic from Tushare and return as DataFrame."""
    pro = create_tushare_pro(token)

    kwargs = {"fields": STOCK_BASIC_FIELDS}
    if list_status:
        kwargs["list_status"] = list_status
    if exchange:
        kwargs["exchange"] = exchange

    data = tushare_request(
        "stock_basic",
        lambda: pro.stock_basic(**kwargs),
    )

    for col in STOCK_BASIC_COLUMNS:
        if col not in data.columns:
            data[col] = None

    return data.reindex(columns=STOCK_BASIC_COLUMNS)


def fetch_and_save_stock_basic(
    token: str | None = None,
    list_status: str = "L",
    exchange: str | None = None,
) -> Path:
    """Fetch stock_basic, save to data/stock_basic_{status}_{timestamp}.csv, return the path."""
    data = fetch_stock_basic(token=token, list_status=list_status, exchange=exchange)

    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stock_basic_{list_status}_{timestamp}.csv"
    csv_path = DATA_ROOT / filename

    data.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved {len(data)} stocks to {csv_path}")

    return csv_path


def find_latest_stock_basic_csv() -> Path:
    """Find the most recent stock_basic_*.csv in data/ directory."""
    if not DATA_ROOT.exists():
        raise RuntimeError(
            f"Data directory does not exist: {DATA_ROOT}. "
            "Use /run-pipeline stock-list or call fetcher.stock_basic.fetch_and_save_stock_basic() first."
        )

    candidates = sorted(DATA_ROOT.glob("stock_basic_*.csv"), reverse=True)
    if not candidates:
        raise RuntimeError(
            f"No stock_basic_*.csv found in {DATA_ROOT}. "
            "Use /run-pipeline stock-list or call fetcher.stock_basic.fetch_and_save_stock_basic() first."
        )

    return candidates[0]
