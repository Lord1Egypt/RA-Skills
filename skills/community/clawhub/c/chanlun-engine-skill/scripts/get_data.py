#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_data.py — 取日K数据, 输出 CSV (date,open,high,low,close,volume,amount 前复权)
数据源两档:
  akshare  免费, 不需要任何账号和 key (默认, 装完技能即可用; pip install akshare)
  hithink  同花顺官方 Financial-API, 更快更稳 (需环境变量 HITHINK_FINANCE_API_KEY,
           申请方法见 references/getting-started.md: 用同花顺账号登录 fuyao.aicubes.cn/admin)
用法:
  python get_data.py --symbol 600519 [--years 3] [--out moutai.csv] [--source auto|akshare|hithink]
  --source auto(默认): 有 key 用 hithink, 没 key 用 akshare
代码格式随意: 600519 / 600519.SH / sh600519 都认(自动归一)。
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def _load_key():
    k = os.environ.get("HITHINK_FINANCE_API_KEY")
    if k:
        return k
    base = os.environ.get("APPDATA") or os.path.expanduser("~/.config")
    p = os.path.join(base, "hithink-finance", "credentials.env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            if line.startswith("HITHINK_FINANCE_API_KEY_DPAPI="):
                return _dpapi_unprotect(line.split("=", 1)[1].strip())
            if line.startswith("HITHINK_FINANCE_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


def _dpapi_unprotect(b64):
    import base64
    import ctypes
    import ctypes.wintypes as wt

    class BLOB(ctypes.Structure):
        _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    raw = base64.b64decode(b64)
    buf = ctypes.create_string_buffer(raw, len(raw))
    bin_ = BLOB(len(raw), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    bout = BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(bin_), None, None, None, None, 0, ctypes.byref(bout)):
        return None
    try:
        return ctypes.string_at(bout.pbData, bout.cbData).decode()
    finally:
        ctypes.windll.kernel32.LocalFree(bout.pbData)


KEY = _load_key()


def norm_code(s):
    """600519 / 600519.SH / sh600519 → (六位码, 带后缀码)"""
    s = s.strip().upper().replace("SH", "").replace("SZ", "").replace("BJ", "")
    digits = re.sub(r"\D", "", s)
    if len(digits) != 6:
        raise SystemExit(json.dumps({"error": f"无法识别股票代码: {s}, 请给6位数字代码"}, ensure_ascii=False))
    if digits.startswith(("60", "68")):
        suffix = "SH"
    elif digits.startswith(("00", "30")):
        suffix = "SZ"
    else:
        suffix = "BJ"
    return digits, f"{digits}.{suffix}"


def resolve_name(query):
    """股票名 → (六位码, 带后缀码, 权威名称)。
    解析顺序: ①打包名录(零网络,首选) ②同花顺搜索(有key,兜新股) ③akshare名录。
    蠢模型保底: 名称→代码这步必须由脚本确定性完成, 严禁模型凭记忆猜代码。"""
    table = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_stock_names.csv")
    if os.path.exists(table):
        exact, part = [], []
        with open(table, encoding="utf-8") as f:
            next(f)
            for line in f:
                code_full, name = line.strip().split(",", 1)
                if name == query:
                    exact.append((code_full, name))
                elif query in name:
                    part.append((code_full, name))
        pick = exact or part
        if len(pick) == 1:
            full, name = pick[0]
            return full.split(".")[0], full, name
        if len(pick) > 1:
            raise SystemExit(json.dumps({"error": f"「{query}」匹配到多只股票, 请让用户确认要哪只",
                "candidates": [f"{c} {n}" for c, n in pick[:5]]}, ensure_ascii=False))
        # 名录没有(可能是新股) → 继续走在线解析
    if KEY:
        q = urllib.parse.urlencode({"q": query})
        req = urllib.request.Request(f"https://fuyao.aicubes.cn/api/meta/tickers/search?{q}",
                                     headers={"X-api-key": KEY})
        try:
            b = json.loads(urllib.request.urlopen(req, timeout=20).read())
            items = (b.get("data") or {}).get("item") or []
            exact = [i for i in items if i.get("name") == query]
            pick = (exact or items)
            if len(pick) > 1 and not exact:
                raise SystemExit(json.dumps({"error": f"「{query}」匹配到多只股票, 请让用户确认",
                    "candidates": [f"{i.get('thscode')} {i.get('name')}" for i in pick[:5]]}, ensure_ascii=False))
            if pick:
                full = pick[0]["thscode"]
                return full.split(".")[0], full, pick[0].get("name", query)
        except SystemExit:
            raise
        except Exception:
            pass  # 搜索失败退回akshare名录
    import akshare as ak
    df = ak.stock_info_a_code_name()
    exact = df[df["name"] == query]
    if exact.empty:
        part = df[df["name"].str.contains(query, na=False)]
        if part.empty:
            raise SystemExit(json.dumps({"error": f"找不到股票「{query}」, 请确认名称或直接给6位代码"},
                                        ensure_ascii=False))
        if len(part) > 1:
            raise SystemExit(json.dumps({"error": f"「{query}」匹配到多只股票, 请让用户确认",
                "candidates": [f"{r['code']} {r['name']}" for _, r in part.head(5).iterrows()]},
                ensure_ascii=False))
        exact = part
    code6 = str(exact.iloc[0]["code"]).zfill(6)
    _, full = norm_code(code6)
    return code6, full, str(exact.iloc[0]["name"])


def fetch_akshare(code6, years):
    """免费源, 双通道: 东财(主) → 新浪(备)。东财对部分网络环境(尤其海外IP)会断连。"""
    import akshare as ak
    start_d = datetime.date.today() - datetime.timedelta(days=int(years * 365))
    last_err = None
    for attempt in range(2):                      # 东财两次
        try:
            df = ak.stock_zh_a_hist(symbol=code6, period="daily",
                                    start_date=start_d.strftime("%Y%m%d"),
                                    end_date=datetime.date.today().strftime("%Y%m%d"),
                                    adjust="qfq")
            if df is not None and not df.empty:
                return [{"date": str(r["日期"])[:10], "open": float(r["开盘"]),
                         "high": float(r["最高"]), "low": float(r["最低"]),
                         "close": float(r["收盘"]), "volume": float(r["成交量"]),
                         "amount": float(r["成交额"])} for _, r in df.iterrows()]
        except Exception as e:
            last_err = e
            time.sleep(2)
    try:                                          # 新浪备用
        prefix = "sh" if code6.startswith(("60", "68")) else ("sz" if code6.startswith(("00", "30")) else "bj")
        df = ak.stock_zh_a_daily(symbol=f"{prefix}{code6}", adjust="qfq",
                                 start_date=start_d.strftime("%Y%m%d"),
                                 end_date=datetime.date.today().strftime("%Y%m%d"))
        if df is not None and not df.empty:
            rows = []
            for _, r in df.iterrows():
                rows.append({"date": str(r["date"])[:10], "open": float(r["open"]),
                             "high": float(r["high"]), "low": float(r["low"]),
                             "close": float(r["close"]), "volume": float(r["volume"]),
                             "amount": float(r["amount"]) if "amount" in df.columns else None})
            return rows
    except Exception as e:
        last_err = e
    raise SystemExit(json.dumps({
        "error": f"免费数据源都连不上({type(last_err).__name__}), 常见于网络环境限制",
        "hint": "稍后重试; 或申请同花顺key走官方源(见references/getting-started.md); 有代理时关掉代理再试"},
        ensure_ascii=False))


def fetch_hithink(code_full, years):
    end = int(time.time() * 1000)
    start = end - 86400_000 * int(years * 365)
    q = urllib.parse.urlencode({"thscode": code_full, "interval": "1d",
                                "adjust": "forward", "start": start, "end": end})
    req = urllib.request.Request(
        f"https://fuyao.aicubes.cn/api/a-share/prices/historical?{q}",
        headers={"X-api-key": KEY})
    b = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if b.get("code") != 0:
        raise SystemExit(json.dumps({"error": f"同花顺接口返回 code={b.get('code')} {b.get('message')}",
                                     "hint": "key 无效或过期时, 重新去 fuyao.aicubes.cn/admin 签发"},
                                    ensure_ascii=False))
    rows = []
    for it in b["data"]["item"]:
        d = datetime.datetime.fromtimestamp(it["date_ms"] / 1000).strftime("%Y-%m-%d")
        rows.append({"date": d, "open": it["open_price"], "high": it["high_price"],
                     "low": it["low_price"], "close": it["close_price"],
                     "volume": it["volume"], "amount": it["turnover"]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--years", type=float, default=3)
    ap.add_argument("--out", help="输出CSV路径, 缺省打到stdout")
    ap.add_argument("--source", choices=["auto", "akshare", "hithink"], default="auto")
    a = ap.parse_args()
    if re.search(r"[^0-9A-Za-z.\s]", a.symbol):        # 含中文等 → 名称解析
        code6, code_full, name = resolve_name(a.symbol.strip())
    else:
        code6, code_full = norm_code(a.symbol)
        name = None

    src = a.source
    if src == "auto":
        src = "hithink" if KEY else "akshare"
    if src == "hithink" and not KEY:
        raise SystemExit(json.dumps({"error": "缺 HITHINK_FINANCE_API_KEY",
                                     "hint": "申请方法见 references/getting-started.md, 或改用 --source akshare"},
                                    ensure_ascii=False))
    rows = fetch_hithink(code_full, a.years) if src == "hithink" else fetch_akshare(code6, a.years)

    f = open(a.out, "w", newline="", encoding="utf-8") if a.out else sys.stdout
    w = csv.writer(f)
    w.writerow(["date", "open", "high", "low", "close", "volume", "amount"])
    for r in rows:
        w.writerow([r["date"], r["open"], r["high"], r["low"], r["close"], r["volume"], r["amount"]])
    if a.out:
        f.close()
        print(json.dumps({"written": a.out, "bars": len(rows), "source": src,
                          "symbol": code_full, "name": name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
