"""High-level pipeline functions for OpenClaw skills."""

from __future__ import annotations

from fetcher.common import load_dotenv_if_needed
from fetcher.daily import DailyBatchConfig, DailyBatchResult, default_past_year_dates
from fetcher.stock_basic import fetch_and_save_stock_basic, find_latest_stock_basic_csv


def _resolve_stock_csv(token: str | None = None):
    """Find existing stock list CSV or fetch a new one."""
    try:
        path = find_latest_stock_basic_csv()
        print(f"Using existing stock list: {path}")
        return path
    except RuntimeError:
        print("No existing stock list found. Fetching from Tushare...")
        return fetch_and_save_stock_basic(token=token)


def init_fetch(
    start_date: str | None = None,
    end_date: str | None = None,
    sleep_seconds: float = 0.5,
    batch_size: int = 100,
    limit: int | None = None,
    token: str | None = None,
) -> DailyBatchResult:
    """Full init: fetch stock list + batch fetch all datasets with --resume.

    Suitable for first-time setup or resuming an interrupted init.
    """
    load_dotenv_if_needed(token)

    stock_csv = _resolve_stock_csv(token)
    default_start, default_end = default_past_year_dates()

    config = DailyBatchConfig(
        token=token,
        stock_csv=stock_csv,
        ts_code_column="ts_code",
        start_date=start_date or default_start,
        end_date=end_date or default_end,
        offset=0,
        limit=limit,
        batch_size=batch_size,
        sleep_seconds=sleep_seconds,
        fail_fast=False,
        allow_failures=True,
        resume=True,
        incremental=False,
        include_daily_basic=True,
        include_adj_factor=True,
        encoding="utf-8-sig",
    )

    from fetcher.daily import run_daily_batch_fetch
    result = run_daily_batch_fetch(config)
    _print_result(result)
    return result


def daily_update(
    end_date: str,
    start_date: str | None = None,
    sleep_seconds: float = 0.5,
    batch_size: int = 100,
    limit: int | None = None,
    token: str | None = None,
) -> DailyBatchResult:
    """Incremental daily update: fetch new data from local max(trade_date)+1.

    Suitable for post-close daily sync.
    """
    load_dotenv_if_needed(token)

    stock_csv = _resolve_stock_csv(token)
    default_start, _ = default_past_year_dates()

    config = DailyBatchConfig(
        token=token,
        stock_csv=stock_csv,
        ts_code_column="ts_code",
        start_date=start_date or default_start,
        end_date=end_date,
        offset=0,
        limit=limit,
        batch_size=batch_size,
        sleep_seconds=sleep_seconds,
        fail_fast=False,
        allow_failures=True,
        resume=False,
        incremental=True,
        include_daily_basic=True,
        include_adj_factor=True,
        encoding="utf-8-sig",
    )

    from fetcher.daily import run_daily_batch_fetch
    result = run_daily_batch_fetch(config)
    _print_result(result)
    return result


def _print_result(result: DailyBatchResult) -> None:
    print(f"\n--- Batch Result ---")
    print(f"Requested: {result.requested}  Skipped: {result.skipped}  "
          f"Succeeded: {result.succeeded}  Failed: {result.failed}")
    print(f"Rows: daily={result.daily_rows}  daily_basic={result.daily_basic_rows}  "
          f"adj_factor={result.adj_factor_rows}")
    if result.failures:
        print("Failures:")
        for ts_code, error in result.failures[:10]:
            print(f"  - {ts_code}: {error}")
        if len(result.failures) > 10:
            print(f"  ... and {len(result.failures) - 10} more")
