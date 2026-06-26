import pandas as pd


def parse_tushare_date(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.strip()
    parsed = pd.to_datetime(text, format="%Y%m%d", errors="coerce")
    fallback = pd.to_datetime(series, errors="coerce")
    return parsed.fillna(fallback)


def normalize_trade_date(df: pd.DataFrame, column: str = "trade_date") -> pd.DataFrame:
    if df.empty or column not in df.columns:
        return df.copy()

    normalized = df.copy()
    normalized[column] = parse_tushare_date(normalized[column])
    return normalized


def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    if "amount" not in enriched.columns or "vol" not in enriched.columns:
        enriched["vwap"] = pd.NA
        return enriched

    amount = pd.to_numeric(enriched["amount"], errors="coerce")
    vol = pd.to_numeric(enriched["vol"], errors="coerce")
    enriched["vwap"] = (amount * 10).where(vol > 0) / vol.where(vol > 0)
    return enriched
