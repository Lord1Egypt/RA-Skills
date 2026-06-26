import pandas as pd


def pick_col(df: pd.DataFrame, candidates):
    """Pick the first existing column name from candidates."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def kv_df_to_dict(df: pd.DataFrame, key_col='字段', val_col='值'):
    """Convert AKShare key-value DataFrame to dict, with basic stripping."""
    if df is None or len(df) == 0:
        return {}
    if key_col not in df.columns or val_col not in df.columns:
        # fallback: try first two columns
        key_col, val_col = df.columns[:2]
    out = {}
    for _, row in df.iterrows():
        k = str(row[key_col]).strip()
        v = row[val_col]
        if isinstance(v, str):
            v = v.strip()
        out[k] = v
    return out


def to_float(x):
    try:
        return float(str(x).replace('%', '').strip())
    except Exception:
        return None


def normalize_greeks_kv(kv: dict):
    """Normalize fields from option_sse_greeks_sina into internal keys."""
    m = {
        '期权合约简称': 'name',
        '成交量': 'volume',
        '最新价': 'price_last',
        '行权价': 'strike',
        '隐含波动率': 'iv',
        'Delta': 'delta',
        'Gamma': 'gamma',
        'Theta': 'theta',
        'Vega': 'vega',
        '理论价值': 'theo_value',
        '交易代码': 'trade_code',
    }
    out = {}
    for k, v in kv.items():
        if k in m:
            out[m[k]] = v
    # numeric conversion
    for nk in ['volume', 'price_last', 'strike', 'iv', 'delta', 'gamma', 'theta', 'vega', 'theo_value']:
        if nk in out:
            out[nk] = to_float(out[nk])
    return out
