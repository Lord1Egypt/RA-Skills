"""
Data cleaner — handle missing values, outliers, type conversion, deduplication.
"""
import sys
import numpy as np
import pandas as pd
from typing import Optional


def clean_data(df: pd.DataFrame,
               fill_strategy: str = 'auto',
               remove_outliers: bool = False,
               drop_cols: list = None) -> pd.DataFrame:
    """
    Clean a DataFrame with configurable strategies.

    Args:
        df: Input DataFrame
        fill_strategy: 'auto' (mode for cat, median for num), 'mean', 'median', 'mode', 'drop'
        remove_outliers: Whether to cap/remove outliers using IQR
        drop_cols: List of columns to drop

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    original_shape = df.shape

    # Drop specified columns
    if drop_cols:
        existing = [c for c in drop_cols if c in df.columns]
        df.drop(columns=existing, inplace=True, errors='ignore')
        if existing:
            print(f"[Cleaner] Dropped columns: {existing}")

    # Drop fully-null columns
    all_null = [c for c in df.columns if df[c].isna().all()]
    if all_null:
        df.drop(columns=all_null, inplace=True)
        print(f"[Cleaner] Dropped all-null columns: {all_null}")

    # Drop fully-null rows
    null_rows = df.isna().all(axis=1).sum()
    if null_rows > 0:
        df.dropna(how='all', inplace=True)
        print(f"[Cleaner] Dropped {null_rows} fully-null rows")

    # Handle missing values
    if fill_strategy != 'drop':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object', 'category']).columns

        for col in df.columns:
            miss = df[col].isna().sum()
            if miss == 0:
                continue

            if fill_strategy == 'auto':
                if col in numeric_cols:
                    fill_val = df[col].median()
                else:
                    fill_val = df[col].mode()[0] if not df[col].mode().empty else 'MISSING'
            elif fill_strategy == 'mean' and col in numeric_cols:
                fill_val = df[col].mean()
            elif fill_strategy == 'median' and col in numeric_cols:
                fill_val = df[col].median()
            elif fill_strategy == 'mode':
                fill_val = df[col].mode()[0] if not df[col].mode().empty else 'MISSING'
            else:
                continue

            df[col] = df[col].fillna(fill_val)

        remaining = df.isna().sum().sum()
        print(f"[Cleaner] Filled missing values, strategy={fill_strategy}, remaining NaN={remaining}")
    else:
        before = len(df)
        df.dropna(inplace=True)
        print(f"[Cleaner] Dropped {before - len(df)} rows with NaN")

    # Remove duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df.drop_duplicates(inplace=True)
        print(f"[Cleaner] Removed {dup_count} duplicate rows")

    # Outlier capping (IQR method)
    if remove_outliers:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        capped = 0
        for col in numeric_cols:
            q1, q3 = df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = (df[col] < lower) | (df[col] > upper)
            capped += outliers.sum()
            df[col] = df[col].clip(lower, upper)
        if capped > 0:
            print(f"[Cleaner] Capped {capped} outlier values")

    # Infer and convert types
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col], errors='raise')
            except Exception:
                try:
                    numeric = pd.to_numeric(df[col], errors='coerce')
                    if numeric.notna().sum() / len(df) > 0.95:
                        df[col] = numeric
                except Exception:
                    pass

    new_shape = df.shape
    print(f"[Cleaner] Done: {original_shape} -> {new_shape}")
    return df


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_cleaner.py <filepath>")
        sys.exit(1)

    from data_loader import load_data
    df = load_data(sys.argv[1])
    df_clean = clean_data(df)
    print(f"\nCleaned data preview:\n{df_clean.head()}")
    print(f"\nMissing after cleaning:\n{df_clean.isna().sum()}")
