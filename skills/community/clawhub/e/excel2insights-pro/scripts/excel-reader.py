#!/usr/bin/env python3
"""
Excel2Insights — File Reader
Load structured data files (CSV, XLSX, XLS, TSV) and output file metadata,
column overview, preview rows, and data quality flags as structured JSON.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print(json.dumps({"error": "pandas not installed. Run: pip install pandas openpyxl"}))
    sys.exit(1)


def load_file(filepath, sheet=None, encoding="utf-8", preview_rows=5):
    filepath = Path(filepath)
    if not filepath.exists():
        return {"error": f"File not found: {filepath}"}

    ext = filepath.suffix.lower()
    size_bytes = filepath.stat().st_size

    try:
        if ext in (".xlsx", ".xls"):
            if sheet:
                df = pd.read_excel(filepath, sheet_name=sheet)
            else:
                xls = pd.ExcelFile(filepath)
                sheet = xls.sheet_names[0]
                df = pd.read_excel(filepath, sheet_name=sheet)
        elif ext == ".tsv":
            df = pd.read_csv(filepath, sep="\t", encoding=encoding)
        elif ext == ".csv":
            df = pd.read_csv(filepath, encoding=encoding)
        else:
            return {"error": f"Unsupported format: {ext}. Supported: .csv, .xlsx, .xls, .tsv"}
    except Exception as e:
        return {"error": f"Failed to load file: {e}"}

    n_rows, n_cols = df.shape
    dtypes = {col: str(dt) for col, dt in df.dtypes.items()}
    missing = {col: int(cnt) for col, cnt in df.isnull().sum().items()}
    missing_pct = {col: round(cnt / n_rows * 100, 2) if n_rows > 0 else 0
                   for col, cnt in missing.items()}
    duplicates = int(df.duplicated().sum())

    # Numeric columns summary
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    date_cols = [c for c in df.columns if df[c].dtype.kind == "M"]

    preview = {}
    try:
        preview["head"] = df.head(preview_rows).to_dict(orient="records")
        preview["tail"] = df.tail(preview_rows).to_dict(orient="records")
    except Exception:
        preview["head"] = str(df.head(preview_rows))
        preview["tail"] = str(df.tail(preview_rows))

    # Data quality flags
    quality_flags = []
    high_missing = [col for col, pct in missing_pct.items() if pct > 10]
    if high_missing:
        quality_flags.append(f"High missing ratio in: {', '.join(high_missing)}")
    if duplicates > 0:
        quality_flags.append(f"{duplicates} duplicate row(s) found ({round(duplicates/n_rows*100, 2)}%)")
    low_card_cat = [c for c in cat_cols if c in df.columns and df[c].nunique() < 2]
    if low_card_cat:
        quality_flags.append(f"Constant columns: {', '.join(low_card_cat)}")

    return {
        "file": str(filepath),
        "size_bytes": size_bytes,
        "sheet": sheet if ext in (".xlsx", ".xls") else None,
        "rows": n_rows,
        "columns": n_cols,
        "column_names": list(df.columns),
        "dtypes": dtypes,
        "missing": missing,
        "missing_pct": missing_pct,
        "duplicates": duplicates,
        "preview": preview,
        "column_types": {
            "numeric": num_cols,
            "categorical": cat_cols,
            "datetime": date_cols
        },
        "quality_flags": quality_flags
    }


def main():
    parser = argparse.ArgumentParser(description="Excel2Insights — File Reader")
    parser.add_argument("--file", required=True, help="Path to data file")
    parser.add_argument("--sheet", help="Sheet name (XLSX only)")
    parser.add_argument("--encoding", default="utf-8", help="File encoding")
    parser.add_argument("--preview", type=int, default=5, help="Preview rows")
    args = parser.parse_args()

    result = load_file(args.file, args.sheet, args.encoding, args.preview)
    print(json.dumps(result, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
