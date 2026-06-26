"""
Fundamental data resolver with cascading fallback.

Priority order (per user spec):
  1. tushare pro
  2. akshare
  3. baostock
  4. eastmoney datacenter
  5. (web_search — handled by Claude layer, not this script)

Each layer must return a dict in the harmonized shape or None.
The chain records which source succeeded so the report can show provenance.
"""
from __future__ import annotations
import sys
import os
import traceback
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sources import tushare_src, akshare_src, baostock_src, eastmoney  # noqa: E402


LAYERS = [
    ("tushare", tushare_src.get_fundamental_indicators),
    ("akshare", akshare_src.get_fundamental_indicators),
    ("baostock", baostock_src.get_fundamental_indicators),
    ("eastmoney", eastmoney.get_fundamental_indicators),
]


def resolve_fundamentals(code: str, verbose: bool = False) -> dict:
    """
    Try each data source in priority order. Return merged result:
    {
      "data": { ...harmonized dict... } or None,
      "source_used": "tushare"|"akshare"|"baostock"|"eastmoney"|None,
      "attempts": [ {name, ok, error?} ],
      "needs_websearch": bool,   # True if all 4 layers returned None
    }
    """
    attempts = []
    result = None
    source_used = None

    for name, fn in LAYERS:
        try:
            out = fn(code)
            if out:
                attempts.append({"name": name, "ok": True})
                result = out
                source_used = name
                if verbose:
                    print(f"[fundamentals] success via {name}", file=sys.stderr)
                break
            else:
                attempts.append({"name": name, "ok": False, "error": "no data returned"})
                if verbose:
                    print(f"[fundamentals] {name} returned None", file=sys.stderr)
        except Exception as e:
            attempts.append({
                "name": name,
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            })
            if verbose:
                traceback.print_exc(file=sys.stderr)

    # Merge with eastmoney data even when tushare wins, to fill any gaps
    # (eastmoney gives revenue/profit numbers that tushare pro basic plan might miss)
    if result and source_used != "eastmoney":
        try:
            em = eastmoney.get_fundamental_indicators(code)
            if em:
                for k in ("revenue", "net_profit", "revenue_yoy", "net_profit_yoy",
                          "gross_margin", "roe"):
                    if (result.get(k) is None) and (em.get(k) is not None):
                        result[k] = em[k]
                        result.setdefault("_merged_from", []).append(f"{k}:eastmoney")
        except Exception:
            pass

    return {
        "data": result,
        "source_used": source_used,
        "attempts": attempts,
        "needs_websearch": (result is None),
    }


if __name__ == "__main__":
    import json
    if len(sys.argv) < 2:
        print("usage: fundamental_chain.py <code>")
        sys.exit(1)
    out = resolve_fundamentals(sys.argv[1], verbose=True)
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
