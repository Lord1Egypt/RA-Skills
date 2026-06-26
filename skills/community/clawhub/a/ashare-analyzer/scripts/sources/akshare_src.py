"""
akshare data source for industry/concept/theme peer discovery.

Exposes:
 - get_industry_of(code) -> str (e.g. "家电零部件Ⅱ") via stock_individual_info_em
 - get_industry_peers(industry_name) -> DataFrame
 - get_concept_peers(concept_name) -> DataFrame
 - get_all_industries() -> DataFrame (name + board_code)
 - get_all_concepts() -> DataFrame
"""
from __future__ import annotations
import warnings
from typing import Optional

import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def _lazy_ak():
    import akshare as ak
    return ak


def get_individual_info(code6: str) -> dict:
    """
    Return a dict with individual info from akshare:
    {'name', 'industry', 'total_mv', 'float_mv', 'total_share', 'list_date'}

    Args: code6 — 6-digit code like '002418'
    """
    ak = _lazy_ak()
    df = ak.stock_individual_info_em(symbol=code6)
    # df has columns 'item' and 'value'
    d = dict(zip(df["item"], df["value"]))
    return {
        "name": str(d.get("股票简称", "")),
        "industry": str(d.get("行业", "")),
        "total_mv": float(d["总市值"]) if d.get("总市值") else None,
        "float_mv": float(d["流通市值"]) if d.get("流通市值") else None,
        "total_share": float(d["总股本"]) if d.get("总股本") else None,
        "float_share": float(d["流通股"]) if d.get("流通股") else None,
        "list_date": str(d.get("上市时间", "")),
        "price": float(d["最新"]) if d.get("最新") else None,
    }


def get_industry_peers(industry_name: str, top_n: int = 20) -> pd.DataFrame:
    """
    Return constituents of an Eastmoney industry board.
    Columns: 代码, 名称, 最新价, 涨跌幅, 换手率, 成交额, 市盈率-动态, 市净率
    """
    ak = _lazy_ak()
    df = ak.stock_board_industry_cons_em(symbol=industry_name)
    return df.head(top_n)


def get_concept_peers(concept_name: str, top_n: int = 30) -> pd.DataFrame:
    """
    Return constituents of an Eastmoney concept board.
    """
    ak = _lazy_ak()
    df = ak.stock_board_concept_cons_em(symbol=concept_name)
    return df.head(top_n)


def get_all_industries() -> pd.DataFrame:
    """List all Eastmoney industry boards."""
    ak = _lazy_ak()
    return ak.stock_board_industry_name_em()


def get_all_concepts() -> pd.DataFrame:
    """List all Eastmoney concept boards."""
    ak = _lazy_ak()
    return ak.stock_board_concept_name_em()


def get_financial_abstract(code6: str) -> Optional[pd.DataFrame]:
    """
    Fetch quarterly financial abstract (财务摘要) from Tonghuashun via akshare.
    Columns vary by indicator; typical: 报告期, 净利润, 净利润同比, 营业收入, 营业收入同比, ...

    Returns None on failure.
    """
    ak = _lazy_ak()
    try:
        df = ak.stock_financial_abstract_ths(symbol=code6, indicator="按报告期")
        return df
    except Exception:
        try:
            df = ak.stock_financial_abstract(symbol=code6)
            return df
        except Exception:
            return None


def get_financial_analysis_indicator(code6: str, start_year: str = "2023") -> Optional[pd.DataFrame]:
    """
    akshare financial analysis indicator (新浪/同花顺口径).
    Contains: 主营业务利润率(%), 总资产利润率(%), 净资产收益率(%), 净利率, 毛利率, ...
    """
    ak = _lazy_ak()
    try:
        df = ak.stock_financial_analysis_indicator(symbol=code6, start_year=start_year)
        return df
    except Exception:
        return None


def get_fundamental_indicators(code: str) -> Optional[dict]:
    """
    akshare fundamental source (layer 2 in fallback chain).
    Uses stock_financial_analysis_indicator (xueqiu/sina backend).
    Returns harmonized dict shape.
    """
    from datetime import datetime
    ak = _lazy_ak()
    code6 = _to_code6(code)

    try:
        df = ak.stock_financial_analysis_indicator(symbol=code6, start_year=str(datetime.now().year - 1))
    except Exception:
        return None
    if df is None or len(df) == 0:
        return None

    df = df.sort_values("日期").reset_index(drop=True)
    latest = df.iloc[-1].to_dict()

    def _f(key, scale: float = 1.0):
        v = latest.get(key)
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return None
        try:
            return float(v) * scale
        except (TypeError, ValueError):
            return None

    end_date = str(latest.get("日期", ""))
    return {
        "end_date": end_date,
        "report_name": f"{end_date[:4]}年{_period_from_date(end_date)}" if len(end_date) >= 7 else "",
        "roe": _f("净资产收益率(%)"),
        "roa": _f("总资产利润率(%)"),
        "gross_margin": _f("销售毛利率(%)"),
        "net_margin": _f("销售净利率(%)"),
        "debt_to_assets": _f("资产负债率(%)"),
        "eps": _f("加权每股收益(元)") or _f("摊薄每股收益(元)"),
        "bps": _f("每股净资产_调整前(元)"),
        "revenue": None,
        "net_profit": None,
        "revenue_yoy": _f("主营业务收入增长率(%)"),
        "net_profit_yoy": _f("净利润增长率(%)"),
        "source": "akshare",
    }


def _to_code6(code: str) -> str:
    import re as _re
    s = code.strip().upper()
    m = _re.match(r"^(SZ|SH|BJ)(\d{6})$", s)
    if m:
        return m.group(2)
    m = _re.match(r"^(\d{6})\.(SZ|SH|BJ)$", s)
    if m:
        return m.group(1)
    m = _re.match(r"^\d{6}$", s)
    if m:
        return s
    return s


def _period_from_date(date_str: str) -> str:
    md = date_str[5:10].replace("-", "")
    return {"0331": "一季报", "0630": "中报", "0930": "三季报", "1231": "年报"}.get(md, "")
