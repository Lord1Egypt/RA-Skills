"""
Tushare pro data source.

Scope:
  - Daily K-line (OHLCV) for individual stocks and indices
  - Fundamental indicators (fina_indicator + income)
  - Daily basic (PE, PB, turnover_rate, market cap)

Top priority in the fallback chain. Requires TUSHARE_TOKEN env var.
"""
from __future__ import annotations
import os
import re
from typing import Optional

import pandas as pd


def _ts_code(code: str) -> str:
    """Normalize to '002418.SZ' format."""
    s = code.strip().upper()
    m = re.match(r"^(SZ|SH|BJ)(\d{6})$", s)
    if m:
        return m.group(2) + "." + m.group(1)
    m = re.match(r"^(\d{6})\.(SZ|SH|BJ)$", s)
    if m:
        return s
    m = re.match(r"^\d{6}$", s)
    if m:
        if s.startswith(("60", "68", "90")):
            return s + ".SH"
        elif s.startswith(("43", "83", "87", "92", "4", "8")):
            return s + ".BJ"
        else:
            return s + ".SZ"
    return s


def _is_index(code: str) -> bool:
    """Check if code is a market index (e.g. 000300.SH, 000001.SH, 399001.SZ)."""
    s = code.strip()
    m = re.match(r"^(?:sz|sh|bj)?(\d{6})", s, re.IGNORECASE)
    if not m:
        m = re.match(r"^(\d{6})", s)
    if not m:
        return False
    digits = m.group(1)
    # SSE indices: 000xxx, CSI indices
    if digits.startswith("000") or digits.startswith("880"):
        return True
    # SZSE indices: 399xxx
    if digits.startswith("399"):
        return True
    return False


def get_daily_kline(code: str, days: int = 420) -> Optional[pd.DataFrame]:
    """
    Fetch daily K-line from tushare pro.

    Returns DataFrame in the SAME format as tencent.get_daily_kline():
        trade_date (YYYYMMDD str), open, high, low, close, vol (手), amount (元),
        turnover_rate (%)
    Returns None on any failure (missing token, rate limit, no data).
    """
    token = os.environ.get("TUSHARE_TOKEN")
    if not token:
        return None

    try:
        import tushare as ts
        pro = ts.pro_api(token)
    except Exception:
        return None

    ts_code = _ts_code(code)
    is_idx = _is_index(code)

    # Calculate date range
    from datetime import datetime, timedelta
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=int(days * 1.6))  # ~1.6x calendar days for trading days
    start_date = start_dt.strftime("%Y%m%d")

    try:
        if is_idx:
            df = pro.index_daily(ts_code=ts_code, start_date=start_date)
        else:
            df = pro.daily(ts_code=ts_code, start_date=start_date)
    except Exception:
        return None

    if df is None or len(df) == 0:
        return None

    # Normalize columns to match tencent format
    df = df.sort_values("trade_date").reset_index(drop=True)
    df = df.tail(days).reset_index(drop=True)

    # Ensure trade_date is string YYYYMMDD
    df["trade_date"] = df["trade_date"].astype(str)

    # Convert amount from 千元 to 元
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce") * 1000
    else:
        df["amount"] = None

    # Get turnover_rate from daily_basic (only for individual stocks)
    if not is_idx:
        try:
            basic = pro.daily_basic(
                ts_code=ts_code,
                start_date=start_date,
                fields="ts_code,trade_date,turnover_rate"
            )
            if basic is not None and len(basic) > 0:
                basic = basic[["trade_date", "turnover_rate"]].copy()
                basic["trade_date"] = basic["trade_date"].astype(str)
                df = df.merge(basic, on="trade_date", how="left")
        except Exception:
            df["turnover_rate"] = None
    else:
        df["turnover_rate"] = None

    # Select and order columns to match tencent format
    cols = ["trade_date", "open", "high", "low", "close", "vol", "amount", "turnover_rate"]
    available = [c for c in cols if c in df.columns]
    result = df[available].copy()

    # Ensure numeric types
    for c in ["open", "high", "low", "close", "vol", "amount"]:
        if c in result.columns:
            result[c] = pd.to_numeric(result[c], errors="coerce")

    return result


def get_fundamental_indicators(code: str) -> Optional[dict]:
    """
    Fetch from tushare pro fina_indicator + daily_basic.
    Returns dict in harmonized shape (same keys across all fundamental sources),
    or None on any failure (missing token, rate limit, no data).
    """
    token = os.environ.get("TUSHARE_TOKEN")
    if not token:
        return None

    try:
        import tushare as ts
        pro = ts.pro_api(token)
    except Exception:
        return None

    ts_code = _ts_code(code)

    try:
        fina = pro.fina_indicator(
            ts_code=ts_code,
            fields="ts_code,end_date,roe,roa,netprofit_margin,grossprofit_margin,"
                   "debt_to_assets,q_profit_yoy,q_sales_yoy,eps,bps"
        )
        if fina is None or len(fina) == 0:
            return None
        fina = fina.sort_values("end_date")
        latest_f = fina.iloc[-1].to_dict()
    except Exception:
        latest_f = {}

    try:
        income = pro.income(
            ts_code=ts_code,
            fields="ts_code,end_date,revenue,n_income_attr_p,basic_eps"
        )
        if income is not None and len(income) > 0:
            income = income.sort_values("end_date")
            latest_i = income.iloc[-1].to_dict()
            # YoY
            rev_yoy, np_yoy = None, None
            if len(income) >= 5:
                latest_end = str(latest_i["end_date"])
                py_key = str(int(latest_end[:4]) - 1) + latest_end[4:]
                prev = income[income["end_date"] == py_key]
                if len(prev):
                    pr = prev.iloc[0]
                    if pr.get("revenue"):
                        rev_yoy = (latest_i["revenue"] / pr["revenue"] - 1) * 100
                    if pr.get("n_income_attr_p"):
                        np_yoy = (latest_i["n_income_attr_p"] / pr["n_income_attr_p"] - 1) * 100
        else:
            latest_i, rev_yoy, np_yoy = {}, None, None
    except Exception:
        latest_i, rev_yoy, np_yoy = {}, None, None

    if not latest_f and not latest_i:
        return None

    end_date_raw = str(latest_f.get("end_date") or latest_i.get("end_date") or "")
    end_date = f"{end_date_raw[:4]}-{end_date_raw[4:6]}-{end_date_raw[6:8]}" if len(end_date_raw) == 8 else end_date_raw

    return {
        "end_date": end_date,
        "report_name": f"{end_date_raw[:4]}年{_period_label(end_date_raw[4:8])}" if len(end_date_raw) == 8 else "",
        "roe": _f(latest_f.get("roe")),
        "roa": _f(latest_f.get("roa")),
        "gross_margin": _f(latest_f.get("grossprofit_margin")),
        "net_margin": _f(latest_f.get("netprofit_margin")),
        "debt_to_assets": _f(latest_f.get("debt_to_assets")),
        "eps": _f(latest_f.get("eps")) or _f(latest_i.get("basic_eps")),
        "bps": _f(latest_f.get("bps")),
        "revenue": _f(latest_i.get("revenue")),
        "net_profit": _f(latest_i.get("n_income_attr_p")),
        "revenue_yoy": rev_yoy if rev_yoy is not None else _f(latest_f.get("q_sales_yoy")),
        "net_profit_yoy": np_yoy if np_yoy is not None else _f(latest_f.get("q_profit_yoy")),
        "source": "tushare",
    }


def _f(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _period_label(md: str) -> str:
    return {"0331": "一季报", "0630": "中报", "0930": "三季报", "1231": "年报"}.get(md, md)
