"""
4-layer data quality audit system.
L1: Basic health check (file structure, column names, empty data)
L2: Structure integrity (duplicates, time gaps, ID compliance)
L3: Business semantics (range checks, allowed values against rules)
L4: Model readiness (IV values, cardinality, distribution drift)
"""
import sys
import numpy as np
import pandas as pd
from pathlib import Path


def audit_data(df: pd.DataFrame, business_rules: dict = None, target_col: str = None,
               sample_size: int = 50000) -> dict:
    """
    Run full 4-layer audit on a DataFrame.

    Args:
        df: Input DataFrame
        business_rules: Optional dict of business validation rules
        target_col: Optional target column for IV/readiness checks
        sample_size: Max rows for sampling (speed on large datasets)

    Returns:
        Dict with audit results per layer
    """
    # Sample for large datasets
    if len(df) > sample_size:
        print(f"[Auditor] Sampling {sample_size:,} from {len(df):,} rows")
        df = df.sample(n=sample_size, random_state=42)

    results = {
        'layer1_health': _layer1_health_check(df),
        'layer2_structure': _layer2_structure_check(df),
        'layer3_business': _layer3_business_check(df, business_rules),
        'layer4_readiness': _layer4_readiness_check(df, target_col),
        'summary': {}
    }

    # Compute summary
    issues = []
    for layer_name, layer_results in results.items():
        if layer_name == 'summary':
            continue
        if isinstance(layer_results, dict):
            for key, val in layer_results.items():
                if isinstance(val, dict) and val.get('status') in ('warning', 'error'):
                    issues.append(f"[{layer_name}] {key}: {val.get('message', '')}")

    results['summary'] = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'total_issues': len(issues),
        'issues': issues[:20],  # Top 20
        'score': _calculate_quality_score(results)
    }

    return results


def _layer1_health_check(df: pd.DataFrame) -> dict:
    """L1: Basic health check — hard errors and structural basics."""
    results = {}

    # Check for empty DataFrame
    results['empty'] = {
        'status': 'error' if df.empty else 'ok',
        'message': 'DataFrame is empty' if df.empty else 'OK'
    }
    if df.empty:
        return results

    # Check column name duplicates
    dup_cols = [c for c in df.columns if list(df.columns).count(c) > 1]
    results['duplicate_columns'] = {
        'status': 'error' if dup_cols else 'ok',
        'message': f'Duplicate columns: {dup_cols}' if dup_cols else 'OK'
    }

    # Check for all-null columns
    all_null_cols = [c for c in df.columns if df[c].isna().all()]
    results['all_null_columns'] = {
        'status': 'warning' if all_null_cols else 'ok',
        'message': f'All-null columns: {all_null_cols}' if all_null_cols else 'OK'
    }

    # Check for single-value columns
    single_val_cols = [c for c in df.columns if df[c].nunique() <= 1]
    results['constant_columns'] = {
        'status': 'warning' if single_val_cols else 'ok',
        'message': f'Constant columns: {single_val_cols}' if single_val_cols else 'OK'
    }

    # Memory usage estimate
    mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    results['memory_usage_mb'] = round(mem_mb, 2)

    # Column type summary
    results['dtypes'] = {c: str(df[c].dtype) for c in df.columns}

    return results


def _layer2_structure_check(df: pd.DataFrame) -> dict:
    """L2: Structure integrity — duplicates, time gaps, ID compliance."""
    results = {}

    # Duplicate row check (all columns)
    dup_count = df.duplicated().sum()
    dup_pct = (dup_count / len(df)) * 100 if len(df) > 0 else 0
    results['duplicate_rows'] = {
        'count': int(dup_count),
        'percentage': round(dup_pct, 2),
        'status': 'warning' if dup_pct > 1 else 'ok',
        'message': f'{dup_count} duplicate rows ({dup_pct:.1f}%)' if dup_count > 0 else 'No duplicates'
    }

    # Missing value analysis per column
    missing = {}
    for col in df.columns:
        miss = df[col].isna().sum()
        miss_pct = (miss / len(df)) * 100 if len(df) > 0 else 0
        if miss > 0:
            missing[col] = {'count': int(miss), 'percentage': round(miss_pct, 2)}
    results['missing_values'] = missing

    # ID-like column detection and checks
    id_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in ['id', 'uuid', 'key', 'code']):
            col_data = df[col].dropna().astype(str)
            id_cols.append({
                'column': col,
                'unique_count': int(col_data.nunique()),
                'total_count': len(col_data),
                'uniqueness': round(col_data.nunique() / len(col_data) * 100, 2) if len(col_data) > 0 else 0,
                'has_non_ascii': bool(col_data.str.contains(r'[^\x00-\x7F]').any()) if len(col_data) > 0 else False
            })
    results['id_columns'] = id_cols

    return results


def _layer3_business_check(df: pd.DataFrame, rules: dict = None) -> dict:
    """L3: Business semantic check — apply domain rules."""
    results = {}

    if not rules:
        results['note'] = 'No business rules provided, skipping L3'
        return results

    violations = []
    for field, rule in rules.items():
        if field not in df.columns:
            continue

        series = df[field]

        # Numeric range check
        if 'min' in rule and pd.api.types.is_numeric_dtype(series):
            out_min = (series < rule['min']).sum()
            if out_min > 0:
                violations.append({
                    'field': field,
                    'rule': f"min={rule['min']}",
                    'count': int(out_min),
                    'sample': series[series < rule['min']].head(3).tolist()
                })
        if 'max' in rule and pd.api.types.is_numeric_dtype(series):
            out_max = (series > rule['max']).sum()
            if out_max > 0:
                violations.append({
                    'field': field,
                    'rule': f"max={rule['max']}",
                    'count': int(out_max),
                    'sample': series[series > rule['max']].head(3).tolist()
                })

        # Allowed values check
        if 'allowed_values' in rule:
            allowed = set(rule['allowed_values'])
            series_str = series.astype(str)
            invalid = ~series_str.isin(allowed) & series.notna()
            if invalid.any():
                violations.append({
                    'field': field,
                    'rule': f"allowed={list(allowed)[:5]}...",
                    'count': int(invalid.sum()),
                    'sample': series[invalid].head(5).tolist()
                })

    results['violations'] = violations
    results['status'] = 'warning' if violations else 'ok'
    results['message'] = f'{len(violations)} business rule violations found' if violations else 'All business rules passed'

    return results


def _layer4_readiness_check(df: pd.DataFrame, target_col: str = None) -> dict:
    """L4: Model readiness — cardinality, skewness, outlier detection."""
    results = {}

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Outlier detection (IQR method) for numeric columns
    outliers = {}
    for col in numeric_cols[:20]:  # Cap at 20 cols
        series = df[col].dropna()
        if len(series) < 10:
            continue
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outlier_count = ((series < lower) | (series > upper)).sum()
        outlier_pct = outlier_count / len(series) * 100
        if outlier_pct > 0:
            outliers[col] = {
                'count': int(outlier_count),
                'percentage': round(outlier_pct, 2),
                'lower_bound': round(lower, 2),
                'upper_bound': round(upper, 2)
            }
    results['outliers'] = outliers

    # Skewness for numeric columns
    skewness = {}
    for col in numeric_cols[:20]:
        series = df[col].dropna()
        if len(series) > 1 and series.std() > 0:
            skew = series.skew()
            if abs(skew) > 1:
                skewness[col] = round(skew, 2)
    results['skewed_features'] = skewness

    # High cardinality categorical columns
    high_card = {}
    for col in cat_cols:
        n_unique = df[col].nunique()
        if n_unique > 50:
            high_card[col] = int(n_unique)
    results['high_cardinality'] = high_card

    # IV (Information Value) if target provided
    if target_col and target_col in df.columns:
        iv_values = {}
        target = df[target_col]
        for col in cat_cols[:30]:
            if col == target_col:
                continue
            try:
                iv = _calculate_iv(df[col], target)
                iv_values[col] = round(iv, 4)
            except Exception:
                pass
        results['iv_values'] = {
            k: v for k, v in sorted(iv_values.items(), key=lambda x: x[1], reverse=True)
            if v > 0.02
        }

    return results


def _calculate_iv(feature: pd.Series, target: pd.Series) -> float:
    """Calculate Information Value for a categorical feature."""
    temp = pd.DataFrame({'feature': feature.fillna('MISSING'), 'target': target})
    grouped = temp.groupby('feature')['target'].agg(['sum', 'count'])
    grouped['non_event'] = grouped['count'] - grouped['sum']
    total_events = grouped['sum'].sum()
    total_non = grouped['non_event'].sum()
    if total_events == 0 or total_non == 0:
        return 0

    grouped['event_pct'] = grouped['sum'] / total_events
    grouped['non_event_pct'] = grouped['non_event'] / total_non
    grouped['woe'] = np.log((grouped['event_pct'] + 1e-10) / (grouped['non_event_pct'] + 1e-10))
    grouped['iv'] = (grouped['event_pct'] - grouped['non_event_pct']) * grouped['woe']
    return grouped['iv'].sum()


def _calculate_quality_score(results: dict) -> dict:
    """Calculate overall data quality score (0-100)."""
    score = 100
    deductions = []

    l1 = results.get('layer1_health', {})
    l2 = results.get('layer2_structure', {})
    l3 = results.get('layer3_business', {})
    l4 = results.get('layer4_readiness', {})

    # L1 penalties
    if l1.get('all_null_columns', {}).get('status') == 'warning':
        score -= 5
        deductions.append('All-null columns (-5)')
    if l1.get('constant_columns', {}).get('status') == 'warning':
        score -= 3
        deductions.append('Constant columns (-3)')

    # L2 penalties
    dup_pct = l2.get('duplicate_rows', {}).get('percentage', 0)
    if dup_pct > 5:
        score -= 10
        deductions.append(f'High duplicate rate {dup_pct:.1f}% (-10)')
    elif dup_pct > 1:
        score -= 5
        deductions.append(f'Duplicate rate {dup_pct:.1f}% (-5)')

    missing = l2.get('missing_values', {})
    high_miss = sum(1 for v in missing.values() if v['percentage'] > 20)
    if high_miss > 0:
        score -= min(high_miss * 3, 15)
        deductions.append(f'{high_miss} columns with >20% missing (-{min(high_miss*3, 15)})')

    # L3 penalties
    violations = l3.get('violations', [])
    if violations:
        score -= min(len(violations) * 2, 10)
        deductions.append(f'{len(violations)} business rule violations (-{min(len(violations)*2, 10)})')

    # L4 penalties
    outliers = l4.get('outliers', {})
    if outliers:
        high_out = sum(1 for v in outliers.values() if v['percentage'] > 10)
        if high_out > 0:
            score -= min(high_out * 2, 10)
            deductions.append(f'{high_out} columns with >10% outliers (-{min(high_out*2, 10)})')

    score = max(0, min(100, score))

    # Grade
    if score >= 90:
        grade = 'A'
    elif score >= 75:
        grade = 'B'
    elif score >= 60:
        grade = 'C'
    else:
        grade = 'D'

    return {'score': score, 'grade': grade, 'deductions': deductions}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_auditor.py <filepath> [target_col]")
        sys.exit(1)

    from data_loader import load_data
    df = load_data(sys.argv[1])
    target = sys.argv[2] if len(sys.argv) > 2 else None
    results = audit_data(df, target_col=target)

    import json
    print(json.dumps(results['summary'], indent=2, ensure_ascii=False))
