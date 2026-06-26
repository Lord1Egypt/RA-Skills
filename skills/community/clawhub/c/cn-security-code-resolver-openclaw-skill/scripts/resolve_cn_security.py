#!/usr/bin/env python3
import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List

API = "https://searchapi.eastmoney.com/api/suggest/get"
TOKEN = "D43BF722C8E33BDC906FB84D85E326E8"
TIMEOUT = 15


def infer_exchange_suffix(code: str) -> str | None:
    if not code:
        return None
    if code[0] in {"5", "6", "9"}:
        return "SH"
    if code[0] in {"0", "1", "2", "3"}:
        return "SZ"
    return None


def score_candidate(query: str, row: Dict[str, Any]) -> int:
    name = str(row.get("Name", ""))
    sec_type = str(row.get("SecurityTypeName", ""))
    code = str(row.get("Code", ""))
    score = 0

    if name == query:
        score += 100
    elif query in name:
        score += 40

    if sec_type in {"沪A", "深A"}:
        score += 20
    elif sec_type == "基金":
        score += 15

    if len(code) == 6 and code.isdigit():
        score += 10

    return score


def fetch_candidates(query: str) -> List[Dict[str, Any]]:
    params = {
        "input": query,
        "type": "14",
        "token": TOKEN,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8", "ignore"))
    rows = data.get("QuotationCodeTable", {}).get("Data", []) or []
    ranked = sorted(rows, key=lambda r: score_candidate(query, r), reverse=True)
    out = []
    for row in ranked:
        code = str(row.get("Code", ""))
        suffix = infer_exchange_suffix(code)
        out.append(
            {
                "name": row.get("Name"),
                "code": code,
                "standardCode": f"{code}.{suffix}" if suffix else None,
                "exchangeSuffix": suffix,
                "securityTypeName": row.get("SecurityTypeName"),
                "classify": row.get("Classify"),
                "marketType": row.get("MarketType"),
                "quoteId": row.get("QuoteID"),
                "score": score_candidate(query, row),
                "raw": row,
            }
        )
    return out


def main() -> int:
    queries = sys.argv[1:]
    if not queries:
        print("Usage: resolve_cn_security.py <name> [<name> ...]", file=sys.stderr)
        return 1

    results = []
    for query in queries:
        try:
            candidates = fetch_candidates(query)
            results.append(
                {
                    "query": query,
                    "resolved": candidates[0] if candidates else None,
                    "candidates": candidates[:5],
                    "source": "eastmoney_suggest",
                    "timestamp": int(time.time()),
                }
            )
        except Exception as e:
            results.append(
                {
                    "query": query,
                    "resolved": None,
                    "candidates": [],
                    "source": "eastmoney_suggest",
                    "error": str(e),
                    "timestamp": int(time.time()),
                }
            )

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
