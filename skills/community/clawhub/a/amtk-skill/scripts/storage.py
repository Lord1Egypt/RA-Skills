from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from fetcher.common import QUANT_DATA_ROOT


@dataclass(frozen=True)
class DatasetWriteResult:
    rows: int
    parquet_path: Path
    csv_path: Path


def dataset_dir(dataset_name: str, root: Path | None = None) -> Path:
    return (root or QUANT_DATA_ROOT) / dataset_name


def dataset_paths(
    dataset_name: str,
    filename: str,
    root: Path | None = None,
) -> tuple[Path, Path]:
    directory = dataset_dir(dataset_name, root)
    return directory / f"{filename}.parquet", directory / f"{filename}.csv"


def read_dataset_file(parquet_path: Path, csv_path: Path) -> pd.DataFrame:
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return pd.DataFrame()


def write_frame(
    df: pd.DataFrame,
    dataset_name: str,
    filename: str,
    keys: list[str],
    root: Path | None = None,
) -> DatasetWriteResult:
    parquet_path, csv_path = dataset_paths(dataset_name, filename, root)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    existing = read_dataset_file(parquet_path, csv_path)
    merged = pd.concat([existing, df], ignore_index=True) if not existing.empty else df.copy()

    if keys:
        merged = merged.drop_duplicates(subset=keys, keep="last")
        merged = merged.sort_values(keys).reset_index(drop=True)

    merged.to_parquet(parquet_path, index=False)
    merged.to_csv(csv_path, index=False, encoding="utf-8-sig")

    return DatasetWriteResult(
        rows=len(merged),
        parquet_path=parquet_path,
        csv_path=csv_path,
    )


def safe_partition_value(value: object) -> str:
    text = str(value).strip()
    if not text:
        raise RuntimeError("Partition value cannot be empty.")

    return "".join(char if char.isalnum() or char in "._-" else "_" for char in text)


def write_symbol_year_partitioned_dataset(
    df: pd.DataFrame,
    dataset_name: str,
    filename_suffix: str,
    keys: list[str],
    root: Path | None = None,
    symbol_column: str = "ts_code",
    date_column: str = "trade_date",
) -> list[DatasetWriteResult]:
    if df.empty:
        return []
    if symbol_column not in df.columns:
        raise RuntimeError(f"Missing required symbol column: {symbol_column}")
    if date_column not in df.columns:
        raise RuntimeError(f"Missing required date column: {date_column}")

    working = df.copy()
    working[date_column] = pd.to_datetime(working[date_column], errors="coerce")
    working = working.dropna(subset=[symbol_column, date_column])

    results = []
    group_keys = [working[symbol_column], working[date_column].dt.year]
    for (symbol, year), group in working.groupby(group_keys):
        symbol_dir = f"{dataset_name}/{safe_partition_value(symbol)}"
        filename = f"{int(year)}_{filename_suffix}"
        results.append(write_frame(group, symbol_dir, filename, keys, root))

    return results


def read_named_dataset(
    dataset_name: str,
    filename: str,
    root: Path | None = None,
) -> pd.DataFrame:
    parquet_path, csv_path = dataset_paths(dataset_name, filename, root)
    return read_dataset_file(parquet_path, csv_path)
