"""
Exploratory Data Analysis (EDA) runner.
Generates descriptive statistics, correlation analysis, distribution summaries, and group aggregations.
"""
import sys
import numpy as np
import pandas as pd
from typing import Optional


def run_eda(df: pd.DataFrame, target_col: str = None) -> dict:
    """
    Run comprehensive EDA on a DataFrame.

    Args:
        df: Cleaned DataFrame
        target_col: Optional target column for bivariate analysis

    Returns:
        Dict with EDA results organized by category
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if target_col and target_col in numeric_cols:
        numeric_cols = [c for c in numeric_cols if c != target_col]

    results = {
        'overview': _overview(df, numeric_cols, cat_cols),
        'numeric_summary': _numeric_summary(df, numeric_cols),
        'categorical_summary': _categorical_summary(df, cat_cols),
        'correlation': _correlation_analysis(df, numeric_cols),
        'top_n': _top_n_analysis(df, numeric_cols, cat_cols),
    }

    if target_col and target_col in df.columns:
        results['target_analysis'] = _target_analysis(df, target_col, numeric_cols, cat_cols)

    return results


def _overview(df: pd.DataFrame, numeric_cols: list, cat_cols: list) -> dict:
    """Dataset overview statistics."""
    total_cells = df.shape[0] * df.shape[1]
    total_missing = df.isna().sum().sum()
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'numeric_columns': len(numeric_cols),
        'categorical_columns': len(cat_cols),
        'total_cells': total_cells,
        'missing_cells': int(total_missing),
        'missing_pct': round(total_missing / total_cells * 100, 2) if total_cells > 0 else 0,
        'duplicate_rows': int(df.duplicated().sum()),
        'memory_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
    }


def _numeric_summary(df: pd.DataFrame, numeric_cols: list) -> list:
    """Summary statistics for numeric columns."""
    if not numeric_cols:
        return []
    desc = df[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75]).T
    results = []
    for col in numeric_cols:
        series = df[col].dropna()
        results.append({
            'column': col,
            'count': int(series.count()),
            'missing': int(df[col].isna().sum()),
            'mean': round(series.mean(), 2),
            'std': round(series.std(), 2),
            'min': round(series.min(), 2),
            'q25': round(series.quantile(0.25), 2),
            'median': round(series.median(), 2),
            'q75': round(series.quantile(0.75), 2),
            'max': round(series.max(), 2),
            'skewness': round(series.skew(), 2),
        })
    return results


def _categorical_summary(df: pd.DataFrame, cat_cols: list) -> list:
    """Summary statistics for categorical columns."""
    if not cat_cols:
        return []
    results = []
    for col in cat_cols:
        series = df[col]
        vc = series.value_counts()
        results.append({
            'column': col,
            'count': int(series.count()),
            'unique': int(series.nunique()),
            'missing': int(series.isna().sum()),
            'top_value': str(vc.index[0]) if len(vc) > 0 else None,
            'top_count': int(vc.iloc[0]) if len(vc) > 0 else 0,
            'top_pct': round(vc.iloc[0] / series.count() * 100, 1) if len(vc) > 0 and series.count() > 0 else 0,
        })
    return results


def _correlation_analysis(df: pd.DataFrame, numeric_cols: list) -> dict:
    """Correlation analysis for numeric columns."""
    if len(numeric_cols) < 2:
        return {'matrix': [], 'top_correlations': [], 'notes': 'Need >= 2 numeric columns'}

    corr_matrix = df[numeric_cols].corr()

    # Find top correlations (excluding self-correlation)
    pairs = []
    seen = set()
    for i, col1 in enumerate(numeric_cols):
        for j, col2 in enumerate(numeric_cols):
            if i >= j:
                continue
            pair_key = tuple(sorted([col1, col2]))
            if pair_key in seen:
                continue
            seen.add(pair_key)
            val = corr_matrix.loc[col1, col2]
            if not np.isnan(val) and abs(val) > 0.3:
                pairs.append({
                    'feature1': col1,
                    'feature2': col2,
                    'correlation': round(val, 3),
                    'strength': 'strong' if abs(val) > 0.7 else ('moderate' if abs(val) > 0.5 else 'weak'),
                    'direction': 'positive' if val > 0 else 'negative',
                })

    pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)

    return {
        'matrix': corr_matrix.values.tolist(),
        'columns': numeric_cols,
        'top_correlations': pairs[:15],
    }


def _top_n_analysis(df: pd.DataFrame, numeric_cols: list, cat_cols: list) -> dict:
    """Top-N and bottom-N for key columns."""
    results = {}

    # Top 5 max for numeric columns
    for col in numeric_cols[:5]:
        results[f'{col}_top5'] = df.nlargest(5, col)[[col]].to_dict('records')
        results[f'{col}_bottom5'] = df.nsmallest(5, col)[[col]].to_dict('records')

    # Top 5 frequency for categorical (first 5 columns)
    for col in cat_cols[:5]:
        vc = df[col].value_counts().head(5)
        results[f'{col}_top_categories'] = [{'value': str(k), 'count': int(v)} for k, v in vc.items()]

    return results


def _target_analysis(df: pd.DataFrame, target_col: str,
                     numeric_cols: list, cat_cols: list) -> dict:
    """Bivariate analysis with target variable."""
    results = {}

    # Numeric vs target
    if target_col in numeric_cols:
        # Target itself is numeric — regression-type analysis
        pass
    elif df[target_col].nunique() <= 10:
        # Categorical target — classification
        results['target_distribution'] = df[target_col].value_counts().to_dict()
        results['target_distribution_pct'] = (
            df[target_col].value_counts(normalize=True) * 100
        ).round(1).to_dict()

        # Numeric features by target class
        target_classes = df[target_col].dropna().unique()
        if len(target_classes) <= 5 and numeric_cols:
            numeric_by_target = {}
            for col in numeric_cols[:10]:
                numeric_by_target[col] = {}
                for cls in target_classes:
                    subset = df[df[target_col] == cls][col]
                    numeric_by_target[col][str(cls)] = {
                        'mean': round(subset.mean(), 2),
                        'std': round(subset.std(), 2),
                        'count': len(subset)
                    }
            results['numeric_by_target'] = numeric_by_target

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eda_runner.py <filepath> [target_col]")
        sys.exit(1)

    from data_loader import load_data
    from data_cleaner import clean_data

    df = load_data(sys.argv[1])
    df_clean = clean_data(df)
    target = sys.argv[2] if len(sys.argv) > 2 else None
    results = run_eda(df_clean, target)

    import json
    # Print overview only (non-serializable parts excluded)
    print(json.dumps({k: v for k, v in results.items()
                      if k in ('overview', 'numeric_summary', 'categorical_summary')},
                     indent=2, ensure_ascii=False, default=str))
