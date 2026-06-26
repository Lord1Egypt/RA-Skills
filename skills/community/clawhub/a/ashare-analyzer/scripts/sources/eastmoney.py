"""
Eastmoney data source.

Endpoints:
 1. RPT_F10_FN_MAINOP — main-business composition (product/industry/region breakdowns)
 2. PC_HSF10/CoreConception/PageAjax — reverse-lookup: which boards/concepts a stock belongs to
 3. RPT_LICO_FN_CPD — financial indicators (fundamental fallback)
 4. push2delay/api/qt/clist/get — board constituents (replacement for akshare's rate-limited path)

All responses are JSON. Endpoints don't need auth but need a browser-y User-Agent.
"""
from __future__ import annotations
import json
import re
import urllib.parse
import urllib.request
from typing import Optional

import pandas as pd

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120"


import time

def _http_get_json(url: str, timeout: int = 15, retries: int = 3) -> dict:
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": _UA,
                "Referer": "https://emweb.eastmoney.com/",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
            text = raw.decode("utf-8", errors="ignore")
            return json.loads(text)
        except Exception as e:
            last_err = e
            time.sleep(0.4 + attempt * 0.9)
    raise last_err if last_err else RuntimeError("http_get_json failed")


def _secucode(code: str) -> str:
    """Normalize to 'XXXXXX.SZ' / 'XXXXXX.SH' / 'XXXXXX.BJ' format used by Eastmoney."""
    s = code.strip().upper()
    m = re.match(r"^(SZ|SH|BJ)(\d{6})$", s)
    if m:
        return m.group(2) + "." + m.group(1)
    m = re.match(r"^(\d{6})\.(SZ|SH|BJ)$", s)
    if m:
        return s
    m = re.match(r"^\d{6}$", s)
    if m:
        if s.startswith(("60", "68", "90")) or s[0] == "9":
            return s + ".SH"
        if s.startswith(("00", "30", "20")):
            return s + ".SZ"
        if s.startswith(("43", "83", "87", "92", "4", "8")):
            return s + ".BJ"
        return s + ".SZ"
    raise ValueError(f"Cannot parse Eastmoney secucode from: {code}")


def _em_prefix(code: str) -> str:
    """Convert to SZ002418 / SH600519 / BJ430047 format used by PC_HSF10 endpoints."""
    secu = _secucode(code)
    code6, market = secu.split(".")
    return market + code6


# ============ 1. Main-business composition ============

def get_main_business(code: str, limit: int = 50) -> list[dict]:
    """
    Fetch main-business composition via RPT_F10_FN_MAINOP.

    Returns a list of rows, each:
    {
      'report_date': '2025-06-30',
      'report_name': '2025中报',
      'type': 'product'|'industry'|'region',
      'item': '制冷管路及配件',
      'revenue': 1098964917.48,      # 元
      'revenue_ratio': 0.928574,     # 占比 [0, 1]
      'gross_margin': 0.093419,
      'rank': 1,
    }
    """
    secu = _secucode(code)
    url = (
        "https://datacenter-web.eastmoney.com/api/data/v1/get"
        "?sortColumns=REPORT_DATE,MAINOP_TYPE,MBI_RATIO&sortTypes=-1,1,-1"
        f"&pageSize={limit}&pageNumber=1"
        "&reportName=RPT_F10_FN_MAINOP&columns=ALL"
        f"&filter=(SECUCODE=%22{secu}%22)"
    )
    try:
        payload = _http_get_json(url)
    except Exception as e:
        raise RuntimeError(f"Eastmoney main business fetch failed: {e}")

    result = payload.get("result")
    if not result or not result.get("data"):
        return []

    type_map = {"1": "industry", "2": "product", "3": "region"}
    rows = []
    for r in result["data"]:
        rows.append({
            "report_date": (r.get("REPORT_DATE") or "")[:10],
            "report_name": r.get("REPORT_NAME", ""),
            "type": type_map.get(str(r.get("MAINOP_TYPE", "")), "unknown"),
            "item": r.get("ITEM_NAME", ""),
            "revenue": r.get("MAIN_BUSINESS_INCOME"),
            "revenue_ratio": r.get("MBI_RATIO"),
            "gross_margin": r.get("GROSS_RPOFIT_RATIO"),
            "rank": r.get("RANK"),
            "cost": r.get("MAIN_BUSINESS_COST"),
            "profit": r.get("MAIN_BUSINESS_RPOFIT"),
        })
    return rows


def get_latest_main_business(code: str) -> dict:
    """
    Convenience: return latest-period breakdown grouped by type.

    Returns:
    {
      'report_date': '2025-06-30',
      'report_name': '2025中报',
      'by_product': [{item, revenue, revenue_ratio, gross_margin}, ...],
      'by_industry': [...],
      'by_region': [...],
    }
    """
    all_rows = get_main_business(code, limit=100)
    if not all_rows:
        return {}
    # Filter to latest report_date only
    latest_date = max(r["report_date"] for r in all_rows)
    latest = [r for r in all_rows if r["report_date"] == latest_date]
    out = {
        "report_date": latest_date,
        "report_name": latest[0]["report_name"] if latest else "",
        "by_product": [],
        "by_industry": [],
        "by_region": [],
    }
    for r in latest:
        entry = {
            "item": r["item"],
            "revenue": r["revenue"],
            "revenue_ratio": r["revenue_ratio"],
            "gross_margin": r["gross_margin"],
            "rank": r["rank"],
        }
        if r["type"] == "product":
            out["by_product"].append(entry)
        elif r["type"] == "industry":
            out["by_industry"].append(entry)
        elif r["type"] == "region":
            out["by_region"].append(entry)
    # Sort each section by revenue desc
    for key in ("by_product", "by_industry", "by_region"):
        out[key].sort(key=lambda x: x.get("revenue") or 0, reverse=True)
    return out


# ============ 2. F10 core concepts reverse lookup ============

def get_boards_of(code: str) -> dict:
    """
    Reverse-lookup: return all Eastmoney boards this stock belongs to.

    Returns:
    {
      'ssbk': [{'board_code': '1242', 'board_name': '家电零部件Ⅱ', 'rank': 2}, ...],
      'hxtc': [...]  # core themes text (may be empty)
    }
    """
    prefix = _em_prefix(code)
    url = (
        "https://emweb.securities.eastmoney.com/PC_HSF10/"
        f"CoreConception/PageAjax?code={prefix}"
    )
    try:
        payload = _http_get_json(url)
    except Exception as e:
        raise RuntimeError(f"Eastmoney F10 core concept fetch failed: {e}")

    ssbk = []
    for item in payload.get("ssbk", []) or []:
        ssbk.append({
            "board_code": str(item.get("BOARD_CODE", "")),
            "board_name": item.get("BOARD_NAME", ""),
            "is_precise": item.get("IS_PRECISE"),
            "rank": item.get("BOARD_RANK"),
        })
    hxtc = []
    for item in payload.get("hxtc", []) or []:
        hxtc.append({
            "key": item.get("KEY_CLASSIF", ""),
            "content": item.get("KEYWORD", ""),
        })
    return {"ssbk": ssbk, "hxtc": hxtc}


# ============ 2b. Board members (bypasses akshare rate limits) ============

def get_board_members(board_code: str, limit: int = 30) -> pd.DataFrame:
    """
    Fetch constituents of a board directly from Eastmoney's push2delay API.
    More reliable than akshare (which wraps push2.push2delay but has tighter
    client-side rate limiting).

    Args:
        board_code: BOARD_CODE from ssbk (e.g. "1138"). If not prefixed with BK,
                    we add it.
        limit: max rows to return.

    Returns DataFrame with columns: code, name, price, pct_chg, turnover_rate,
    pe_dynamic, amount (元).
    """
    if not board_code.startswith("BK"):
        bk = "BK" + str(board_code).zfill(4)
    else:
        bk = board_code

    params = {
        "pn": "1",
        "pz": str(limit),
        "po": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": "f8",          # sort by turnover_rate
        "fs": f"b:{bk}",
        "fields": "f2,f3,f6,f8,f9,f12,f14",
    }
    # Field map (Eastmoney standard):
    # f2 = price        f3 = pct_chg      f6 = amount (元)
    # f8 = turnover_rate  f9 = PE-dynamic  f12 = code     f14 = name
    url = "http://push2delay.eastmoney.com/api/qt/clist/get?" + urllib.parse.urlencode(params)
    try:
        payload = _http_get_json(url)
    except Exception:
        return pd.DataFrame()

    data = payload.get("data") or {}
    rows = data.get("diff") or []
    if not rows:
        return pd.DataFrame()

    records = []
    for r in rows:
        records.append({
            "code": str(r.get("f12", "")).zfill(6),
            "name": str(r.get("f14", "")),
            "price": _to_num(r.get("f2")),
            "pct_chg": _to_num(r.get("f3")),
            "amount": _to_num(r.get("f6")),
            "turnover_rate": _to_num(r.get("f8")),
            "pe_dynamic": _to_num(r.get("f9")),
        })
    return pd.DataFrame(records)


def _to_num(v):
    if v is None or v == "-" or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ============ 2c. Name/code search ============

def search_stocks(query: str, limit: int = 10) -> list[dict]:
    """
    Search for A-shares by name or code using Eastmoney's suggest endpoint.
    Returns list of {code6, name, market_name, secid}.
    """
    url = (
        "http://searchapi.eastmoney.com/api/suggest/get"
        f"?input={urllib.parse.quote(query)}&type=14"
        "&token=D43BF722C8E33BDC906FB84D85E326E8"
    )
    try:
        payload = _http_get_json(url)
    except Exception:
        return []
    data = payload.get("QuotationCodeTable", {}).get("Data", []) or []
    results = []
    for item in data[:limit]:
        classify = item.get("Classify", "")
        if classify != "AStock":
            continue
        code6 = str(item.get("Code", "")).zfill(6)
        results.append({
            "code6": code6,
            "name": item.get("Name", ""),
            "market_name": item.get("SecurityTypeName", ""),
            "secid": item.get("QuoteID", ""),  # e.g. "0.002418"
        })
    return results


def _secid_for(code6: str) -> str:
    """Convert 6-digit code to eastmoney secid (0.xxxxxx for SZ, 1.xxxxxx for SH, 0.xxxxxx for BJ)."""
    if code6.startswith(("60", "68", "90")):
        return f"1.{code6}"
    if code6.startswith(("43", "83", "87", "92", "4", "8")):
        return f"0.{code6}"  # BJ also uses 0 prefix in eastmoney's scheme
    return f"0.{code6}"


def get_stock_snapshot(code6: str) -> Optional[dict]:
    """
    Fetch a quick snapshot of a stock from eastmoney push API.
    Returns {code6, name, total_mv, float_mv, change_pct, price, is_shanghai}.
    """
    secid = _secid_for(code6)
    url = (
        "http://push2delay.eastmoney.com/api/qt/stock/get"
        f"?secid={secid}"
        "&fields=f43,f57,f58,f107,f116,f117,f162,f170"
    )
    try:
        payload = _http_get_json(url)
    except Exception:
        return None
    d = (payload.get("data") or {})
    if not d or not d.get("f58"):
        return None
    # f43=price(raw int, divide by 100), f58=name, f116=total_mv, f117=float_mv,
    # f162=pe_dynamic(raw int, /100), f170=change_pct(raw, /100)
    def _priced(v, div=100):
        if v is None or v == "-":
            return None
        try:
            return float(v) / div
        except (TypeError, ValueError):
            return None

    return {
        "code6": str(d.get("f57", "")).zfill(6),
        "name": d.get("f58", ""),
        "total_mv": _to_num(d.get("f116")),      # 元
        "float_mv": _to_num(d.get("f117")),
        "price": _priced(d.get("f43")),
        "pe_dynamic": _priced(d.get("f162")),
        "change_pct": _priced(d.get("f170")),
        "market_code": d.get("f107"),            # 0=SZ, 1=SH, 2=BJ
    }


# ============ 3. Fundamental indicators (data center) ============

def get_fundamental_indicators(code: str) -> Optional[dict]:
    """
    Fetch latest financial indicators from Eastmoney data center (RPT_LICO_FN_CPD).
    Used as fundamental fallback (layer 4 in the chain).

    Returns a dict with ROE, margins, growth, revenue, profit — or None on failure.
    Fields harmonized with tushare's fina_indicator shape where possible.
    """
    secu = _secucode(code)
    code6 = secu.split(".")[0]
    url = (
        "https://datacenter-web.eastmoney.com/api/data/v1/get"
        "?sortColumns=NOTICE_DATE&sortTypes=-1"
        "&pageSize=4&pageNumber=1"
        "&reportName=RPT_LICO_FN_CPD&columns=ALL"
        f"&filter=(SECURITY_CODE=%22{code6}%22)"
    )
    try:
        payload = _http_get_json(url)
    except Exception:
        return None
    result = payload.get("result") or {}
    rows = result.get("data") or []
    if not rows:
        return None
    latest = rows[0]

    def _num(v):
        if v is None or v == "":
            return None
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    return {
        "end_date": (latest.get("REPORTDATE") or "")[:10],
        "report_name": latest.get("DATATYPE", ""),
        "quarter_label": latest.get("QDATE", ""),
        "roe": _num(latest.get("WEIGHTAVG_ROE")),                # 加权平均 ROE %
        "gross_margin": _num(latest.get("XSMLL")),               # 销售毛利率 %
        "eps": _num(latest.get("BASIC_EPS")),                    # 基本每股收益
        "bps": _num(latest.get("BPS")),                          # 每股净资产
        "revenue": _num(latest.get("TOTAL_OPERATE_INCOME")),     # 营收 元
        "net_profit": _num(latest.get("PARENT_NETPROFIT")),      # 归母净利 元
        "revenue_yoy": _num(latest.get("YSTZ")),                 # 营收同比 %
        "net_profit_yoy": _num(latest.get("SJLTZ")),             # 净利同比 %
        "revenue_qoq": _num(latest.get("YSHZ")),                 # 营收环比 %
        "net_profit_qoq": _num(latest.get("SJLHZ")),             # 净利环比 %
        "industry_board": latest.get("PUBLISHNAME", ""),
        "source": "eastmoney_datacenter",
    }
