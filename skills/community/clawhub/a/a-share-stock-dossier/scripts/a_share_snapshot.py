#!/usr/bin/env python3
"""
A-share market snapshot helper.

Fetch:
1) Real-time quote snapshot from Eastmoney push2 API
2) Recent daily kline from Tencent fqkline API
3) Optional index/breadth baseline

No third-party dependencies (urllib only).
Compatible with Python 3.6+.
"""

import argparse
import datetime as dt
import json
import re
import statistics
import urllib.parse
import urllib.request


EM_QUOTE_API = "https://push2.eastmoney.com/api/qt/ulist.np/get"
TX_KLINE_API = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"


def _http_get_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "ignore"))


def normalize_code(code):
    c = code.strip().upper().replace(" ", "")

    # Accept SH/SZ prefixed forms
    if c.startswith("SH") and len(c) == 8 and c[2:].isdigit():
        c = c[2:]
    elif c.startswith("SZ") and len(c) == 8 and c[2:].isdigit():
        c = c[2:]

    # Accept code.exchange forms
    if "." in c:
        left, right = c.split(".", 1)
        if left.isdigit() and right in {"SH", "SS", "SZ"}:
            c = left

    if not re.fullmatch(r"\d{6}", c):
        raise ValueError("Unsupported code format: {}".format(code))
    return c


def code_to_secid(code6):
    # Eastmoney secid: 1 = SH, 0 = SZ/BJ (basic support for SH/SZ)
    if code6.startswith("6"):
        return "1." + code6
    return "0." + code6


def code_to_tencent_symbol(code6):
    if code6.startswith("6"):
        return "sh" + code6
    return "sz" + code6


def fetch_quotes(codes):
    secids = [code_to_secid(c) for c in codes]
    fields = "f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f15,f16,f17,f18"
    url = EM_QUOTE_API + "?" + urllib.parse.urlencode(
        {
            "fltt": "2",
            "invt": "2",
            "fields": fields,
            "secids": ",".join(secids),
        }
    )
    obj = _http_get_json(url)
    diff = obj.get("data", {}).get("diff", [])

    out = []
    for it in diff:
        out.append(
            {
                "code": str(it.get("f12", "")),
                "name": it.get("f14"),
                "last": it.get("f2"),
                "pct": it.get("f3"),
                "chg": it.get("f4"),
                "open": it.get("f17"),
                "high": it.get("f15"),
                "low": it.get("f16"),
                "prev_close": it.get("f18"),
                "volume": it.get("f5"),
                "amount": it.get("f6"),
                "amplitude": it.get("f7"),
                "turnover": it.get("f8"),
                "pe_ttm": it.get("f9"),
                "volume_ratio": it.get("f10"),
            }
        )

    order = dict((c, i) for i, c in enumerate(codes))
    out.sort(key=lambda x: order.get(x.get("code"), 9999))
    return out


def fetch_index_baseline():
    # SH/SZ/ChiNext + up/down breadth fields where available
    secids = ["1.000001", "0.399001", "0.399006"]
    fields = "f12,f14,f2,f3,f4,f15,f16,f17,f18,f104,f105,f6,f7"
    url = EM_QUOTE_API + "?" + urllib.parse.urlencode(
        {
            "fltt": "2",
            "invt": "2",
            "fields": fields,
            "secids": ",".join(secids),
        }
    )
    obj = _http_get_json(url)
    diff = obj.get("data", {}).get("diff", [])
    out = []
    for it in diff:
        out.append(
            {
                "code": str(it.get("f12", "")),
                "name": it.get("f14"),
                "last": it.get("f2"),
                "pct": it.get("f3"),
                "chg": it.get("f4"),
                "high": it.get("f15"),
                "low": it.get("f16"),
                "open": it.get("f17"),
                "prev_close": it.get("f18"),
                "amount": it.get("f6"),
                "amplitude": it.get("f7"),
                "up_count": it.get("f104"),
                "down_count": it.get("f105"),
            }
        )
    return out


def _ma(vals, n):
    if len(vals) < n:
        return None
    return round(statistics.mean(vals[-n:]), 4)


def _ret(vals, n):
    if len(vals) <= n:
        return None
    base = vals[-(n + 1)]
    if not base:
        return None
    return round((vals[-1] / base - 1) * 100, 4)


def fetch_kline(code6, days=60):
    symbol = code_to_tencent_symbol(code6)
    url = TX_KLINE_API + "?" + urllib.parse.urlencode({"param": "{},day,,,{},qfq".format(symbol, days)})
    obj = _http_get_json(url)
    data = obj.get("data", {}).get(symbol, {})
    rows = data.get("qfqday") or data.get("day") or []

    klines = []
    closes = []
    for r in rows:
        # [date, open, close, high, low, vol]
        try:
            rec = {
                "date": r[0],
                "open": float(r[1]),
                "close": float(r[2]),
                "high": float(r[3]),
                "low": float(r[4]),
                "volume": float(r[5]),
            }
        except Exception:
            continue
        klines.append(rec)
        closes.append(rec["close"])

    metrics = {
        "latest_date": klines[-1]["date"] if klines else None,
        "close": closes[-1] if closes else None,
        "ret_5d_pct": _ret(closes, 5),
        "ret_10d_pct": _ret(closes, 10),
        "ret_20d_pct": _ret(closes, 20),
        "ma5": _ma(closes, 5),
        "ma10": _ma(closes, 10),
        "ma20": _ma(closes, 20),
        "high_10d": max(closes[-10:]) if len(closes) >= 10 else (max(closes) if closes else None),
        "low_10d": min(closes[-10:]) if len(closes) >= 10 else (min(closes) if closes else None),
    }
    return {"metrics": metrics, "klines": klines}


def parse_codes(raw):
    parts = [x for x in re.split(r"[,，\s]+", raw.strip()) if x]
    out = []
    for p in parts:
        c = normalize_code(p)
        if c not in out:
            out.append(c)
    return out


def main():
    parser = argparse.ArgumentParser(description="A-share snapshot helper")
    parser.add_argument("--codes", required=True, help="Comma/space separated 6-digit stock codes")
    parser.add_argument("--with-kline", action="store_true", help="Include daily kline and MA/return metrics")
    parser.add_argument("--kline-days", type=int, default=60, help="Kline lookback days (default: 60)")
    parser.add_argument("--with-indices", action="store_true", help="Include SH/SZ/ChiNext baseline")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    codes = parse_codes(args.codes)

    result = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "codes": codes,
        "quotes": fetch_quotes(codes),
    }

    if args.with_indices:
        result["indices"] = fetch_index_baseline()

    if args.with_kline:
        kline = {}
        for c in codes:
            try:
                kline[c] = fetch_kline(c, days=args.kline_days)
            except Exception as e:
                kline[c] = {"error": str(e)}
        result["kline"] = kline

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
