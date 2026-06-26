"""
Baostock fundamental source (layer 3 in fallback chain).
No auth needed. Returns quarterly data.
"""
from __future__ import annotations
import re
from typing import Optional


def _bs_code(code: str) -> str:
    """Normalize to 'sz.002418' / 'sh.600519' / 'bj.430047' format baostock uses."""
    s = code.strip().lower()
    m = re.match(r"^(sz|sh|bj)(\d{6})$", s)
    if m:
        return f"{m.group(1)}.{m.group(2)}"
    m = re.match(r"^(\d{6})\.(sz|sh|bj)$", s)
    if m:
        return f"{m.group(2)}.{m.group(1)}"
    m = re.match(r"^\d{6}$", s)
    if m:
        if s.startswith(("60", "68", "90")):
            return "sh." + s
        if s.startswith(("43", "83", "87", "92", "4", "8")):
            return "bj." + s
        return "sz." + s
    return s


def get_fundamental_indicators(code: str) -> Optional[dict]:
    """
    Fetch latest quarterly indicators from baostock.
    Uses: query_profit_data (ROE, netProfitMargin, ...), query_growth_data (YoY growth).
    """
    try:
        import baostock as bs
    except ImportError:
        return None

    bs_code = _bs_code(code)
    from datetime import datetime
    year = datetime.now().year

    login_rs = bs.login()
    if login_rs.error_code != "0":
        return None

    try:
        profit = _latest_quarter(bs, "query_profit_data", bs_code, year)
        growth = _latest_quarter(bs, "query_growth_data", bs_code, year)
        balance = _latest_quarter(bs, "query_balance_data", bs_code, year)

        if not (profit or growth):
            return None

        def _f(d, key):
            if not d:
                return None
            v = d.get(key)
            if v is None or v == "":
                return None
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        period = (profit or growth or {}).get("statDate") or ""
        # baostock's ROE fields are fractions (0.0097) not percentages (0.97); convert to %
        roe_raw = _f(profit, "roeAvg")
        gross_raw = _f(profit, "gpMargin")
        net_raw = _f(profit, "npMargin")

        return {
            "end_date": period,
            "report_name": f"{period[:4]}{_period_label(period[5:7] + period[8:10])}" if len(period) == 10 else "",
            "roe": roe_raw * 100 if roe_raw is not None else None,
            "gross_margin": gross_raw * 100 if gross_raw is not None else None,
            "net_margin": net_raw * 100 if net_raw is not None else None,
            "debt_to_assets": (_f(balance, "liabilityToAsset") or 0) * 100 if balance else None,
            "eps": _f(profit, "epsTTM"),
            "bps": None,
            "revenue": _f(profit, "MBRevenue"),
            "net_profit": _f(profit, "netProfit"),
            "revenue_yoy": (_f(growth, "YOYEquity") or 0) * 100 if growth else None,
            "net_profit_yoy": (_f(growth, "YOYNI") or 0) * 100 if growth else None,
            "source": "baostock",
        }
    finally:
        bs.logout()


def _latest_quarter(bs, method: str, code: str, year: int) -> Optional[dict]:
    """Query a baostock method for current & recent years, return most-recent non-empty quarter."""
    fn = getattr(bs, method)
    for y in (year, year - 1):
        for q in (3, 2, 1, 4):
            try:
                rs = fn(code=code, year=y, quarter=q)
                if rs.error_code != "0":
                    continue
                rows = []
                while rs.next():
                    rows.append(rs.get_row_data())
                if rows:
                    return dict(zip(rs.fields, rows[0]))
            except Exception:
                continue
    return None


def _period_label(md: str) -> str:
    return {"0331": "一季报", "0630": "中报", "0930": "三季报", "1231": "年报"}.get(md, md)
