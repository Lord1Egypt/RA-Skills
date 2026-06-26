"""
Data profiler for summary statistics and quality metrics.
"""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

class DataProfiler:
    def profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        report = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": {},
            "missing": {},
            "outliers": {},
            "duplicates": df.duplicated().sum(),
        }
        for col in df.columns:
            series = df[col]
            col_report = {
                "dtype": str(series.dtype),
                "non_null": series.notna().sum(),
                "null_count": series.isna().sum(),
                "null_pct": round(series.isna().mean() * 100, 2),
            }
            if pd.api.types.is_numeric_dtype(series):
                col_report.update({
                    "min": series.min(),
                    "max": series.max(),
                    "mean": series.mean(),
                    "median": series.median(),
                    "std": series.std(),
                })
                # IQR outliers
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers = series[(series < lower) | (series > upper)]
                col_report["outlier_count"] = len(outliers)
                report["outliers"][col] = {
                    "count": len(outliers),
                    "lower_bound": lower,
                    "upper_bound": upper,
                }
            else:
                col_report["unique_count"] = series.nunique()
                col_report["top_value"] = series.mode().iloc[0] if not series.mode().empty else None
            report["columns"][col] = col_report
            report["missing"][col] = col_report["null_count"]
        return report

    def compare(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict[str, Any]:
        """Compare two datasets for schema drift."""
        drift = {
            "columns_added": list(set(df2.columns) - set(df1.columns)),
            "columns_removed": list(set(df1.columns) - set(df2.columns)),
            "type_changes": {},
        }
        for col in set(df1.columns) & set(df2.columns):
            if df1[col].dtype != df2[col].dtype:
                drift["type_changes"][col] = {"before": str(df1[col].dtype), "after": str(df2[col].dtype)}
        return drift
