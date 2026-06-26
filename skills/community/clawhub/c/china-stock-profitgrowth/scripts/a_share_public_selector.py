#!/usr/bin/env python3
"""
Public-source A-share selectors (no Wencai cookie, no python-tools).
Data source: Eastmoney public quote API.

Usage:
  python a_share_public_selector.py lowpricebull 10
  python a_share_public_selector.py smallcap 10
  python a_share_public_selector.py profitgrowth 10
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from typing import Any


BASE = "https://push2.eastmoney.com/api/qt/clist/get"
UT = "bd1d9ddb04089700cf9c27f6f7426281"


def _get_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def _to_float(v: Any) -> float | None:
    try:
        if v in (None, "", "-", "--"):
            return None
        return float(v)
    except Exception:
        return None


def _is_st(name: str) -> bool:
    s = (name or "").upper()
    return "ST" in s or "*ST" in s


def _is_excluded_board(code: str) -> bool:
    return code.startswith("300") or code.startswith("688")


def _fetch_a_shares(limit: int = 200) -> list[dict[str, Any]]:
    params = {
        "pn": "1",
        "pz": str(limit),
        "po": "1",
        "np": "1",
        "ut": UT,
        "fltt": "2",
        "invt": "2",
        "fid": "f62",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
        "fields": "f12,f14,f2,f3,f5,f6,f20,f62,f15,f16,f17,f18,f9,f23",
    }
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    obj = _get_json(url)
    return (obj.get("data") or {}).get("diff") or []


def _format_item(rank: int, row: dict[str, Any]) -> dict[str, Any]:
    cap = _to_float(row.get("f20"))
    return {
        "rank": rank,
        "symbol": str(row.get("f12") or ""),
        "name": str(row.get("f14") or ""),
        "price": _to_float(row.get("f2")),
        "pct_change": _to_float(row.get("f3")),
        "turnover": _to_float(row.get("f6")),
        "market_cap": round(cap / 100000000, 2) if cap else None,
        "main_net_inflow": _to_float(row.get("f62")),
        "pe_ttm": _to_float(row.get("f9")),
        "pb": _to_float(row.get("f23")),
        "raw": row,
    }


def select(strategy: str, top_n: int) -> dict[str, Any]:
    rows = _fetch_a_shares(limit=300)
    out: list[dict[str, Any]] = []
    strategy = strategy.lower().strip()

    for r in rows:
        code = str(r.get("f12") or "")
        name = str(r.get("f14") or "")
        price = _to_float(r.get("f2"))
        cap = _to_float(r.get("f20"))
        inflow = _to_float(r.get("f62"))
        pe = _to_float(r.get("f9"))
        pct = _to_float(r.get("f3"))

        if not code or not name or price is None:
            continue
        if _is_st(name) or _is_excluded_board(code):
            continue

        if strategy == "lowpricebull":
            # Public-source approximation of low-price momentum + capital inflow.
            if price < 10 and (pct or 0) > 0 and (inflow or 0) > 0:
                out.append(r)
        elif strategy == "smallcap":
            # Public-source approximation of small-cap + active turnover.
            if cap and cap <= 5_000_000_000 and (pct or 0) >= 0:
                out.append(r)
        elif strategy == "profitgrowth":
            # Public-source approximation using valuation + trend (no Wencai profit YoY field).
            if pe and 0 < pe <= 60 and (pct or 0) > 0 and (inflow or 0) > 0:
                out.append(r)
        else:
            return {"ok": False, "detail": "strategy_type must be lowpricebull|smallcap|profitgrowth"}

    out.sort(key=lambda x: (_to_float(x.get("f62")) or 0), reverse=True)
    selected = out[: max(1, min(10, top_n))]
    stocks = [_format_item(i + 1, row) for i, row in enumerate(selected)]

    return {
        "ok": True,
        "operation": "stock_selector_public",
        "strategy_type": strategy,
        "top_n": len(stocks),
        "message": "Public-source approximation, not equal to Wencai formula",
        "stocks": stocks,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "detail": "usage: a_share_public_selector.py <strategy_type> [top_n]"}, ensure_ascii=False))
        return 2
    strategy = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    try:
        result = select(strategy, top_n)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("ok") else 1
    except Exception as e:
        print(json.dumps({"ok": False, "detail": str(e)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
