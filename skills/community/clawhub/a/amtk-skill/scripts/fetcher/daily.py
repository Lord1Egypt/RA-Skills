import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

from fetcher.adj_factor import fetch_adj_factor_with_pro
from fetcher.common import create_tushare_pro, tushare_request
from fetcher.daily_basic import fetch_daily_basic_with_pro
from storage import (
    DatasetWriteResult,
    dataset_paths,
    read_dataset_file,
    safe_partition_value,
    write_symbol_year_partitioned_dataset,
)
from transforms import add_vwap, normalize_trade_date


DAILY_FIELDS = "ts_code,trade_date,open,high,low,close,vol,amount"
DAILY_COLUMNS = ["ts_code", "trade_date", "open", "high", "low", "close", "vol", "amount", "vwap"]


@dataclass(frozen=True)
class DailyBatchConfig:
    token: str | None
    stock_csv: Path
    ts_code_column: str
    start_date: str
    end_date: str
    offset: int
    limit: int | None
    batch_size: int
    sleep_seconds: float
    fail_fast: bool
    allow_failures: bool
    resume: bool
    incremental: bool
    include_daily_basic: bool
    include_adj_factor: bool
    encoding: str


@dataclass(frozen=True)
class DailyBatchResult:
    requested: int
    skipped: int
    succeeded: int
    failed: int
    rows: int
    daily_rows: int
    daily_basic_rows: int
    adj_factor_rows: int
    writes: list[DatasetWriteResult]
    failures: list[tuple[str, str]]


def default_past_year_dates(today: date | None = None) -> tuple[str, str]:
    end = today or date.today()
    start = end - timedelta(days=365)
    return start.strftime("%Y%m%d"), end.strftime("%Y%m%d")


def validate_yyyymmdd(value: str, label: str) -> None:
    try:
        datetime.strptime(value, "%Y%m%d")
    except ValueError as error:
        raise RuntimeError(f"{label} must use YYYYMMDD format.") from error


def load_ts_codes_from_csv(
    stock_csv: Path,
    column: str = "ts_code",
    encoding: str = "utf-8-sig",
) -> list[str]:
    if not stock_csv.exists():
        raise RuntimeError(f"Stock CSV does not exist: {stock_csv}")

    stocks = pd.read_csv(stock_csv, encoding=encoding)
    if column not in stocks.columns:
        raise RuntimeError(f"Missing column `{column}` in {stock_csv}.")

    return stocks[column].dropna().astype(str).str.strip().drop_duplicates().tolist()


def apply_code_window(
    ts_codes: list[str],
    offset: int = 0,
    limit: int | None = None,
) -> list[str]:
    window = ts_codes[offset:]
    return window[:limit] if limit is not None else window


def years_in_range(start_date: str, end_date: str) -> list[int]:
    start = datetime.strptime(start_date, "%Y%m%d").date()
    end = datetime.strptime(end_date, "%Y%m%d").date()
    return list(range(start.year, end.year + 1))


def stored_symbol_data_covers_range(
    dataset_name: str,
    filename_suffix: str,
    ts_code: str,
    start_date: str,
    end_date: str,
    root: Path | None = None,
) -> bool:
    start = pd.Timestamp(datetime.strptime(start_date, "%Y%m%d").date())
    end = pd.Timestamp(datetime.strptime(end_date, "%Y%m%d").date())
    symbol = safe_partition_value(ts_code)

    frames = []
    for year in years_in_range(start_date, end_date):
        parquet_path, csv_path = dataset_paths(
            f"{dataset_name}/{symbol}",
            f"{year}_{filename_suffix}",
            root=root,
        )
        if not parquet_path.exists() and not csv_path.exists():
            return False

        frame = read_dataset_file(parquet_path, csv_path)
        if frame.empty or "trade_date" not in frame.columns:
            return False
        frames.append(frame)

    data = pd.concat(frames, ignore_index=True)
    data = normalize_trade_date(data)
    data = data[data["ts_code"].astype(str) == ts_code]
    data = data.dropna(subset=["trade_date"])
    if data.empty:
        return False

    return data["trade_date"].min() <= start and data["trade_date"].max() >= end


def stored_symbol_max_trade_date(
    dataset_name: str,
    filename_suffix: str,
    ts_code: str,
    root: Path | None = None,
) -> pd.Timestamp | None:
    symbol = safe_partition_value(ts_code)
    dataset_dir = dataset_paths(f"{dataset_name}/{symbol}", "placeholder", root=root)[0].parent
    if not dataset_dir.exists():
        return None

    frames = []
    for parquet_path in sorted(dataset_dir.glob(f"*_{filename_suffix}.parquet")):
        frame = read_dataset_file(parquet_path, parquet_path.with_suffix(".csv"))
        if not frame.empty and "trade_date" in frame.columns:
            frames.append(frame)
    if not frames:
        for csv_path in sorted(dataset_dir.glob(f"*_{filename_suffix}.csv")):
            frame = read_dataset_file(csv_path.with_suffix(".parquet"), csv_path)
            if not frame.empty and "trade_date" in frame.columns:
                frames.append(frame)

    if not frames:
        return None

    data = pd.concat(frames, ignore_index=True)
    data = normalize_trade_date(data)
    data = data[data["ts_code"].astype(str) == ts_code]
    data = data.dropna(subset=["trade_date"])
    if data.empty:
        return None

    return data["trade_date"].max()


def incremental_start_date(
    dataset_name: str,
    filename_suffix: str,
    ts_code: str,
    fallback_start_date: str,
    end_date: str,
    root: Path | None = None,
) -> str | None:
    max_trade_date = stored_symbol_max_trade_date(dataset_name, filename_suffix, ts_code, root=root)
    if max_trade_date is None:
        return fallback_start_date

    next_date = max_trade_date + pd.Timedelta(days=1)
    end = pd.Timestamp(datetime.strptime(end_date, "%Y%m%d").date())
    if next_date > end:
        return None

    fallback = pd.Timestamp(datetime.strptime(fallback_start_date, "%Y%m%d").date())
    start = max(next_date, fallback)
    return start.strftime("%Y%m%d")


def stored_daily_data_covers_range(
    ts_code: str,
    start_date: str,
    end_date: str,
    root: Path | None = None,
) -> bool:
    return stored_symbol_data_covers_range(
        "raw/market_daily",
        "daily",
        ts_code,
        start_date,
        end_date,
        root=root,
    )


def selected_datasets_are_complete(
    ts_code: str,
    config: DailyBatchConfig,
    root: Path | None = None,
) -> bool:
    checks = [
        ("raw/market_daily", "daily"),
    ]
    if config.include_daily_basic:
        checks.append(("raw/daily_basic", "daily_basic"))
    if config.include_adj_factor:
        checks.append(("raw/adj_factor", "adj_factor"))

    return all(
        stored_symbol_data_covers_range(
            dataset_name,
            filename_suffix,
            ts_code,
            config.start_date,
            config.end_date,
            root=root,
        )
        for dataset_name, filename_suffix in checks
    )


def fetch_daily_with_pro(pro, config: dict[str, str | None]) -> pd.DataFrame:
    data = tushare_request(
        "daily",
        lambda: pro.daily(
            trade_date=config["trade_date"],
            ts_code=config["ts_code"],
            start_date=config["start_date"],
            end_date=config["end_date"],
            fields=DAILY_FIELDS,
        ),
    )

    data = normalize_trade_date(data)
    data = add_vwap(data)
    return data.reindex(columns=DAILY_COLUMNS)


def run_daily_batch_fetch(config: DailyBatchConfig) -> DailyBatchResult:
    ts_codes = load_ts_codes_from_csv(
        config.stock_csv,
        column=config.ts_code_column,
        encoding=config.encoding,
    )
    ts_codes = apply_code_window(ts_codes, offset=config.offset, limit=config.limit)

    if not ts_codes:
        raise RuntimeError("No stock codes selected from CSV.")

    pro = create_tushare_pro(config.token)
    frames_by_dataset = {
        "daily": [],
        "daily_basic": [],
        "adj_factor": [],
    }
    writes = []
    failures = []
    skipped = 0
    succeeded = 0
    daily_rows = 0
    daily_basic_rows = 0
    adj_factor_rows = 0

    def flush() -> None:
        for dataset_key, frames in frames_by_dataset.items():
            if not frames:
                continue

            data = pd.concat(frames, ignore_index=True)
            if dataset_key == "daily":
                dataset_name = "raw/market_daily"
                filename_suffix = "daily"
            elif dataset_key == "daily_basic":
                dataset_name = "raw/daily_basic"
                filename_suffix = "daily_basic"
            else:
                dataset_name = "raw/adj_factor"
                filename_suffix = "adj_factor"

            writes.extend(
                write_symbol_year_partitioned_dataset(
                    data,
                    dataset_name=dataset_name,
                    filename_suffix=filename_suffix,
                    keys=["ts_code", "trade_date"],
                )
            )
            frames_by_dataset[dataset_key] = []

    def fetch_with_delay(fetcher):
        try:
            return fetcher()
        finally:
            if config.sleep_seconds:
                time.sleep(config.sleep_seconds)

    for index, ts_code in enumerate(ts_codes, start=1):
        if config.resume and selected_datasets_are_complete(ts_code, config):
            skipped += 1
            print(f"[{index}/{len(ts_codes)}] Skipping {ts_code}; stored data already covers range.")
            continue

        print(f"[{index}/{len(ts_codes)}] Fetching {ts_code}...")
        try:
            base_request_config = {
                "token": config.token,
                "trade_date": None,
                "ts_code": ts_code,
                "start_date": config.start_date,
                "end_date": config.end_date,
            }
            dataset_fetches = [
                ("daily", "raw/market_daily", "daily", fetch_daily_with_pro),
            ]
            if config.include_daily_basic:
                dataset_fetches.append(
                    ("daily_basic", "raw/daily_basic", "daily_basic", fetch_daily_basic_with_pro)
                )
            if config.include_adj_factor:
                dataset_fetches.append(
                    ("adj_factor", "raw/adj_factor", "adj_factor", fetch_adj_factor_with_pro)
                )

            fetched_any = False
            for dataset_key, dataset_name, filename_suffix, fetcher in dataset_fetches:
                request_config = dict(base_request_config)
                if config.incremental:
                    start_date = incremental_start_date(
                        dataset_name,
                        filename_suffix,
                        ts_code,
                        config.start_date,
                        config.end_date,
                    )
                    if start_date is None:
                        continue
                    request_config["start_date"] = start_date

                data = fetch_with_delay(lambda fetcher=fetcher, request_config=request_config: fetcher(pro, request_config))
                fetched_any = True
                if dataset_key == "daily":
                    daily_rows += len(data)
                elif dataset_key == "daily_basic":
                    daily_basic_rows += len(data)
                else:
                    adj_factor_rows += len(data)

                if not data.empty:
                    frames_by_dataset[dataset_key].append(data)

            if config.incremental and not fetched_any:
                skipped += 1
                print(f"[{index}/{len(ts_codes)}] Skipping {ts_code}; selected datasets are up to date.")
            else:
                succeeded += 1
        except RuntimeError as error:
            failures.append((ts_code, str(error)))
            print(f"Failed {ts_code}: {error}")
            if config.fail_fast:
                raise

        if sum(len(frames) for frames in frames_by_dataset.values()) >= config.batch_size:
            flush()

    flush()

    return DailyBatchResult(
        requested=len(ts_codes),
        skipped=skipped,
        succeeded=succeeded,
        failed=len(failures),
        rows=daily_rows + daily_basic_rows + adj_factor_rows,
        daily_rows=daily_rows,
        daily_basic_rows=daily_basic_rows,
        adj_factor_rows=adj_factor_rows,
        writes=writes,
        failures=failures,
    )
