#!/usr/bin/env python3
"""
Excel2Insights — Statistical Data Analyzer
Compute comprehensive statistics: numeric summaries, categorical frequency,
date range analysis, correlation matrix, outlier detection.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print(json.dumps({"error": "Missing dependencies. Install: pandas, numpy"}))
    sys.exit(1)


def analyze_file(filepath, sheet=None, encoding="utf-8", with_corr=False,
                 with_outliers=False, cat_top=20):
    ext = Path(filepath).suffix.lower()
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
        else:
            df = pd.read_csv(filepath, encoding=encoding)
    except Exception as e:
        return {"error": f"Failed to load: {e}"}

    n_rows, n_cols = df.shape
    results = {
        "rows": n_rows,
        "columns": n_cols,
        "column_analysis": {},
    }

    # Per-column analysis
    for col in df.columns:
        col_data = df[col]
        dtype = str(col_data.dtype)
        missing = int(col_data.isnull().sum())
        missing_pct = round(missing / n_rows * 100, 2) if n_rows else 0

        analysis = {
            "dtype": dtype,
            "missing": missing,
            "missing_pct": missing_pct,
            "unique": int(col_data.nunique()),
        }

        if pd.api.types.is_numeric_dtype(col_data):
            vals = col_data.dropna()
            analysis["type"] = "numeric"
            analysis.update({
                "mean": round(float(vals.mean()), 4),
                "median": round(float(vals.median()), 4),
                "std": round(float(vals.std()), 4),
                "min": round(float(vals.min()), 4),
                "max": round(float(vals.max()), 4),
                "q1": round(float(vals.quantile(0.25)), 4),
                "q3": round(float(vals.quantile(0.75)), 4),
                "skewness": round(float(vals.skew()), 4),
                "zero_count": int((vals == 0).sum()),
                "negative_count": int((vals < 0).sum()),
            })
            # Outlier detection (IQR)
            if with_outliers and len(vals) > 3:
                q1, q3 = vals.quantile(0.25), vals.quantile(0.75)
                iqr = q3 - q1
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                outliers = vals[(vals < lower) | (vals > upper)]
                analysis["outliers"] = {
                    "count": int(len(outliers)),
                    "pct": round(len(outliers) / len(vals) * 100, 2),
                    "lower_bound": round(float(lower), 4),
                    "upper_bound": round(float(upper), 4)
                }

        elif pd.api.types.is_datetime64_any_dtype(col_data):
            vals = col_data.dropna()
            analysis["type"] = "datetime"
            analysis.update({
                "min_date": str(vals.min()),
                "max_date": str(vals.max()),
                "date_range_days": int((vals.max() - vals.min()).days) if len(vals) > 1 else 0
            })

        else:
            vals = col_data.dropna().astype(str)
            analysis["type"] = "categorical"
            top_values = vals.value_counts().head(cat_top)
            analysis["top_values"] = [
                {"value": k, "count": int(v)}
                for k, v in top_values.items()
            ]
            analysis["mode"] = str(vals.mode().iloc[0]) if not vals.mode().empty else None

        results["column_analysis"][col] = analysis

    # Correlation matrix (numeric columns only)
    if with_corr:
        num_cols = df.select_dtypes(include="number")
        if len(num_cols.columns) > 1:
            corr = num_cols.corr().round(4)
            results["correlation_matrix"] = {
                "columns": list(corr.columns),
                "values": corr.values.tolist()
            }
        else:
            results["correlation_matrix"] = None

    # Cross-tabulation for categorical pairs
    cat_cols = df.select_dtypes(include="object").columns[:5]  # limit to 5
    if len(cat_cols) >= 2:
        cross_tabs = {}
        for i in range(len(cat_cols) - 1):
            c1 = cat_cols[i]
            for c2 in cat_cols[i + 1:i + 3]:
                if c2 in df.columns:
                    ct = pd.crosstab(df[c1], df[c2])
                    cross_tabs[f"{c1}_x_{c2}"] = {
                        "index": list(ct.index),
                        "columns": list(ct.columns),
                        "values": ct.values.tolist()
                    }
        if cross_tabs:
            results["cross_tabulation"] = cross_tabs

    # Dataset-level stats
    results["dataset_summary"] = {
        "total_cells": n_rows * n_cols,
        "total_missing": int(df.isnull().sum().sum()),
        "overall_missing_pct": round(df.isnull().sum().sum() / (n_rows * n_cols) * 100, 2) if n_rows * n_cols else 0,
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_column_count": len(df.select_dtypes(include="number").columns),
        "categorical_column_count": len(df.select_dtypes(include="object").columns),
        "datetime_column_count": len([c for c in df.columns if df[c].dtype.kind == "M"]),
    }

    return results


def main():
    parser = argparse.ArgumentParser(description="Excel2Insights — Data Analyzer")
    parser.add_argument("--file", required=True, help="Path to data file")
    parser.add_argument("--sheet", help="Sheet name (XLSX)")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--output", help="Output JSON path")
    parser.add_argument("--correlation", action="store_true", help="Include correlation matrix")
    parser.add_argument("--outliers", action="store_true", help="Detect outliers")
    parser.add_argument("--categorical-top", type=int, default=20, help="Top N categories")
    args = parser.parse_args()

    result = analyze_file(args.file, args.sheet, args.encoding,
                          with_corr=args.correlation,
                          with_outliers=args.outliers,
                          cat_top=args.categorical_top)

    output = json.dumps(result, indent=2, default=str, ensure_ascii=False)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Analysis saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
