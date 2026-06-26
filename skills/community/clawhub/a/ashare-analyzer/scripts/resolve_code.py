#!/usr/bin/env python3
"""
Resolve user's raw stock input → canonical A-share identifiers.

Accepts: 6-digit code, code.SZ, sz002418, Chinese name (康盛股份), fuzzy partial name.

Output JSON:
  {"code6", "ts_code", "tencent_code", "name", "industry", "total_mv", "list_date"}
  or {"matches": [...]} for ambiguous, or {"error": "..."} for failure.
"""
import json
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")


def _market_suffix(code6: str) -> str:
    if code6.startswith(("60", "68", "90")) or code6[0] == "9":
        return ".SH"
    if code6.startswith(("43", "83", "87", "92", "4", "8")):
        return ".BJ"
    return ".SZ"


def _tencent_prefix(code6: str) -> str:
    if code6.startswith(("60", "68", "90")):
        return "sh"
    if code6.startswith(("43", "83", "87", "92", "4", "8")):
        return "bj"
    return "sz"


def _normalize(raw: str) -> str:
    s = raw.strip()
    m = re.match(r"^(sz|sh|bj)(\d{6})$", s, re.IGNORECASE)
    if m:
        return m.group(2)
    m = re.match(r"^(\d{6})\.(sz|sh|bj)$", s, re.IGNORECASE)
    if m:
        return m.group(1)
    if re.match(r"^\d{6}$", s):
        return s
    return s


def _resolve_by_code(code6: str) -> dict:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sources import eastmoney

    # Try eastmoney snapshot first (fast, no rate limits)
    snap = eastmoney.get_stock_snapshot(code6)
    name, industry, total_mv = "", "", None
    if snap and snap.get("name"):
        name = snap["name"]
        total_mv = snap.get("total_mv")
    else:
        # Fallback: akshare individual info
        try:
            from sources import akshare_src
            info = akshare_src.get_individual_info(code6)
            name = info.get("name", "")
            industry = info.get("industry", "")
            total_mv = info.get("total_mv")
        except Exception:
            pass

    if not name:
        return {"error": f"Code {code6} not found in A-share listings."}

    # Get industry from F10 ssbk (most authoritative)
    try:
        from sources import eastmoney as em
        boards = em.get_boards_of(code6)
        ssbk = boards.get("ssbk", [])
        for item in ssbk:
            n = item.get("board_name", "")
            if re.search(r"[Ⅰ-Ⅶ]$", n):  # 行业板块 end with 罗马数字
                industry = n
                break
    except Exception:
        pass

    return {
        "code6": code6,
        "ts_code": code6 + _market_suffix(code6),
        "tencent_code": _tencent_prefix(code6) + code6,
        "name": name,
        "industry": industry,
        "total_mv": total_mv,
    }


def _resolve_by_name(name: str) -> dict:
    """Use eastmoney's suggest endpoint first (reliable), fall back to akshare."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sources import eastmoney

    try:
        results = eastmoney.search_stocks(name, limit=10)
    except Exception as e:
        results = []

    if len(results) == 0:
        # Fallback to akshare
        try:
            import akshare as ak
            df = ak.stock_info_a_code_name()
            hits = df[df["name"] == name]
            if len(hits) == 0:
                hits = df[df["name"].str.contains(name, na=False, regex=False)]
            results = [{"code6": str(r["code"]).zfill(6), "name": str(r["name"])}
                       for _, r in hits.head(10).iterrows()]
        except Exception:
            pass

    if len(results) == 0:
        return {"error": f"No A-share found matching '{name}'."}

    if len(results) == 1:
        return _resolve_by_code(results[0]["code6"])

    # Multiple matches — check if any is an exact match
    exact = [r for r in results if r["name"] == name]
    if len(exact) == 1:
        return _resolve_by_code(exact[0]["code6"])

    matches = []
    for r in results:
        c = r["code6"]
        matches.append({
            "code6": c,
            "ts_code": c + _market_suffix(c),
            "name": r["name"],
        })
    return {"matches": matches}


def resolve(raw: str) -> dict:
    norm = _normalize(raw)
    if re.match(r"^\d{6}$", norm):
        return _resolve_by_code(norm)
    return _resolve_by_name(norm)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: resolve_code.py <name-or-code>"}, ensure_ascii=False))
        sys.exit(1)
    result = resolve(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if "error" not in result else 2)
