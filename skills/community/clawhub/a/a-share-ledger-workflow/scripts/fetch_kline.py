#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch validated forward-adjusted daily bars from Eastmoney, then Tencent."""
import json
import sys
import time
import urllib.request

UA = "Mozilla/5.0"
TIMEOUT = 15
RETRY = 3
BACKOFF = 2.0


def secid(code):
    return ("1." if code[0] in "69" else "0.") + code


def txcode(code):
    return ("sh" if code[0] in "69" else "sz") + code


def _get(url, referer):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": referer})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8", "ignore"))


def fetch_eastmoney(code, limit):
    url = ("https://push2his.eastmoney.com/api/qt/stock/kline/get"
           f"?secid={secid(code)}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56"
           f"&klt=101&fqt=1&end=20500101&lmt={limit}")
    data = _get(url, "https://quote.eastmoney.com/")
    rows = ((data or {}).get("data") or {}).get("klines") or []
    bars = []
    for row in rows:
        fields = row.split(",")
        if len(fields) < 6:
            raise ValueError(f"Eastmoney row has fewer than six fields: {row}")
        bars.append({"d": fields[0], "o": float(fields[1]), "c": float(fields[2]),
                     "h": float(fields[3]), "l": float(fields[4]), "v": float(fields[5])})
    return bars


def fetch_tencent(code, limit):
    ticker = txcode(code)
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={ticker},day,,,{limit},qfq"
    data = _get(url, "https://gu.qq.com/")
    node = ((data or {}).get("data") or {}).get(ticker) or {}
    rows = node.get("qfqday") or node.get("day") or []
    bars = []
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) < 6:
            raise ValueError(f"Tencent row format invalid: {row}")
        bars.append({"d": row[0], "o": float(row[1]), "c": float(row[2]),
                     "h": float(row[3]), "l": float(row[4]), "v": float(row[5])})
    return bars


def validate(bars):
    if not bars:
        return False, "empty daily-bar response"
    for bar in bars[-5:]:
        if not (bar["l"] <= min(bar["o"], bar["c"]) <= max(bar["o"], bar["c"]) <= bar["h"]):
            return False, f"OHLC bounds invalid on {bar['d']}"
        if bar["l"] <= 0 or bar["c"] <= 0:
            return False, f"non-positive price on {bar['d']}"
        if bar["v"] > 1e8:
            return False, f"volume out of range on {bar['d']}"
    for prev, curr in zip(bars[-30:], bars[-29:]):
        if prev["c"] > 0 and abs(curr["c"] / prev["c"] - 1) > 0.5:
            return False, f"adjusted close jump over 50%: {prev['d']}→{curr['d']}"
    return True, "ok"


def fetch_one(code, limit):
    errors = []
    for source, fetch in (("eastmoney", fetch_eastmoney), ("tencent", fetch_tencent)):
        for attempt in range(1, RETRY + 1):
            try:
                bars = fetch(code, limit)
                valid, reason = validate(bars)
                if not valid:
                    raise ValueError(reason)
                return source, bars
            except Exception as exc:
                errors.append(f"{source}#{attempt}: {type(exc).__name__}: {exc}")
                if attempt < RETRY:
                    time.sleep(BACKOFF * attempt)
    raise RuntimeError(" | ".join(errors))


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("codes", help="six-digit ticker; comma-separated list accepted")
    parser.add_argument("--limit", type=int, default=130)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, failed = {}, False
    for code in (item.strip() for item in args.codes.split(",") if item.strip()):
        try:
            source, bars = fetch_one(code, args.limit)
            result[code] = {"source": source, "last_date": bars[-1]["d"], "bars": bars}
        except Exception as exc:
            failed = True
            result[code] = {"error": str(exc)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        for code, row in result.items():
            print(code, row.get("source", "FAIL"), row.get("last_date", row.get("error", "")))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
