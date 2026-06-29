"""
Multi-format data loader for the data-analyst skill.

Supports: CSV, Excel (.xlsx/.xls), JSON, SQLite
"""
import os
import sys
import pandas as pd
from pathlib import Path


def detect_format(filepath: str) -> str:
    """Detect file format from extension."""
    ext = Path(filepath).suffix.lower()
    fmt_map = {
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.json': 'json',
        '.db': 'sqlite',
        '.sqlite': 'sqlite',
        '.sqlite3': 'sqlite',
    }
    return fmt_map.get(ext, 'unknown')


def load_data(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Auto-detect format and load data into a pandas DataFrame.

    Args:
        filepath: Path to the data file
        **kwargs: Additional arguments passed to pandas reader

    Returns:
        pandas DataFrame
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    fmt = detect_format(filepath)
    if fmt == 'unknown':
        raise ValueError(f"Unsupported file format: {Path(filepath).suffix}")

    print(f"[DataLoader] Detected format: {fmt}, loading from: {filepath}")

    if fmt == 'csv':
        df = pd.read_csv(filepath, encoding=kwargs.pop('encoding', 'utf-8'), **kwargs)
    elif fmt == 'tsv':
        df = pd.read_csv(filepath, sep='\t', encoding=kwargs.pop('encoding', 'utf-8'), **kwargs)
    elif fmt == 'excel':
        df = pd.read_excel(filepath, **kwargs)
    elif fmt == 'json':
        df = pd.read_json(filepath, **kwargs)
    elif fmt == 'sqlite':
        import sqlite3
        conn = sqlite3.connect(filepath)
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table'", conn
        )
        if tables.empty:
            raise ValueError("SQLite database contains no tables")
        table_name = kwargs.pop('table', tables.iloc[0]['name'])
        query = kwargs.pop('query', f"SELECT * FROM {table_name}")
        df = pd.read_sql_query(query, conn, **kwargs)
        conn.close()
    else:
        raise ValueError(f"Unknown format: {fmt}")

    print(f"[DataLoader] Loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_loader.py <filepath>")
        sys.exit(1)
    df = load_data(sys.argv[1])
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nPreview:\n{df.head(3)}")
    print(f"\nInfo:")
    df.info()
