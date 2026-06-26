#!/usr/bin/env python3
"""
Public-source sector strategy snapshot via Eastmoney APIs.
No cookie required.

Usage:
  python sector_strategy_public.py 1D
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

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


def _fetch_board(fs: str, limit: int = 30) -> list[dict[str, Any]]:
    params = {
        "pn": "1",
        "pz": str(limit),
        "po": "1",
        "np": "1",
        "ut": UT,
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": fs,
        "fields": "f12,f14,f2,f3,f62,f184",
    }
    url = "https://push2.eastmoney.com/api/qt/clist/get?" + urllib.parse.urlencode(params)
    obj = _get_json(url)
    return (obj.get("data") or {}).get("diff") or []


def _fetch_index_snapshot() -> list[dict[str, Any]]:
    # 上证指数、深证成指、创业板指
    params = {
        "fltt": "2",
        "invt": "2",
        "fields": "f14,f2,f3",
        "secids": "1.000001,0.399001,0.399006",
        "ut": UT,
    }
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get?" + urllib.parse.urlencode(params)
    obj = _get_json(url)
    diff = (obj.get("data") or {}).get("diff") or []
    out = []
    for r in diff:
        out.append({"name": r.get("f14"), "price": _to_float(r.get("f2")), "pct_change": _to_float(r.get("f3"))})
    return out


def _normalize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in rows:
        out.append(
            {
                "code": r.get("f12"),
                "name": r.get("f14"),
                "price": _to_float(r.get("f2")),
                "pct_change": _to_float(r.get("f3")),
                "main_net_inflow": _to_float(r.get("f62")),
                "turnover_rate": _to_float(r.get("f184")),
            }
        )
    return out


def main() -> int:
    try:
        sectors = _normalize(_fetch_board("m:90+t:2", 30))  # 行业板块
        concepts = _normalize(_fetch_board("m:90+t:3", 30))  # 概念板块
        overview = _fetch_index_snapshot()
        payload = {
            "sectors": sectors,
            "concepts": concepts,
            "sector_fund_flow": sectors[:10],
            "market_overview": {"major_indices": overview},
            "north_flow": {"detail": "public API snapshot does not provide stable northbound aggregate here"},
            "news": [],
        }
        print(
            json.dumps(
                {
                    "ok": True,
                    "operation": "sector_strategy_live_context_public",
                    "period_type": "1D",
                    "payload": payload,
                    "sectors_count": len(sectors),
                    "concepts_count": len(concepts),
                    "source": "eastmoney-public",
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as e:
        print(json.dumps({"ok": False, "detail": str(e)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
