#!/usr/bin/env python3
"""
Public-source main-force candidate pool (no Wencai cookie).
Data source: Eastmoney public quote API (real-time main net inflow).

Usage:
  python a_share_main_force_public.py 3m 100 50 5000 30 10
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from typing import Any

BASE = "https://push2.eastmoney.com/api/qt/clist/get"
UT = "bd1d9ddb04089700cf9c27f6f7426281"
PERIOD_PRESETS = {
    "3m": {"reference_final_n": 4, "max_range_change": 30.0},
    "6m": {"reference_final_n": 7, "max_range_change": 45.0},
    "1y": {"reference_final_n": 10, "max_range_change": 70.0},
}


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


def _fetch(limit: int = 500) -> list[dict[str, Any]]:
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
        "fields": "f12,f14,f2,f3,f6,f20,f62,f9,f23,f15,f16,f17,f18",
    }
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    obj = _get_json(url)
    return (obj.get("data") or {}).get("diff") or []


def main() -> int:
    pt = (sys.argv[1] if len(sys.argv) > 1 else "3m").lower()
    if pt not in PERIOD_PRESETS:
        print(json.dumps({"ok": False, "detail": "period_type must be 3m|6m|1y"}, ensure_ascii=False))
        return 2
    max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    min_cap = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0
    max_cap = float(sys.argv[4]) if len(sys.argv) > 4 else 5000.0
    max_change = float(sys.argv[5]) if len(sys.argv) > 5 else float(PERIOD_PRESETS[pt]["max_range_change"])
    top_n = int(sys.argv[6]) if len(sys.argv) > 6 else 0

    try:
        rows = _fetch(500)
        out: list[dict[str, Any]] = []
        for r in rows:
            code = str(r.get("f12") or "")
            name = str(r.get("f14") or "")
            if not code or not name or "ST" in name.upper() or code.startswith("300") or code.startswith("688"):
                continue
            cap = _to_float(r.get("f20"))
            cap_yi = (cap / 100000000) if cap else None
            pct = _to_float(r.get("f3"))
            inflow = _to_float(r.get("f62"))
            if cap_yi is None or pct is None or inflow is None:
                continue
            if not (min_cap <= cap_yi <= max_cap):
                continue
            if pct >= max_change:
                continue
            out.append(
                {
                    "symbol": code,
                    "name": name,
                    "price": _to_float(r.get("f2")),
                    "pct_change": pct,
                    "main_net_inflow": inflow,
                    "market_cap": round(cap_yi, 2),
                    "turnover": _to_float(r.get("f6")),
                    "pe_ttm": _to_float(r.get("f9")),
                    "pb": _to_float(r.get("f23")),
                }
            )

        out.sort(key=lambda x: x.get("main_net_inflow") or 0, reverse=True)
        if top_n > 0:
            out = out[:top_n]
        out = out[:max_rows]

        print(
            json.dumps(
                {
                    "ok": True,
                    "operation": "main_force_candidate_pool_public",
                    "period_type": pt,
                    "reference_final_n": PERIOD_PRESETS[pt]["reference_final_n"],
                    "params": {
                        "min_market_cap": min_cap,
                        "max_market_cap": max_cap,
                        "max_range_change": max_change,
                        "top_n": top_n or None,
                        "max_rows": max_rows,
                    },
                    "row_count": len(out),
                    "columns": list(out[0].keys()) if out else [],
                    "rows": out,
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
