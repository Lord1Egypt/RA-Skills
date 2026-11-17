#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临时辅助：用新浪实时(hq)取今日量价，用新浪日K取前5日均量 -> 量能环比。
用法: python3 _volcheck.py 002436 300285 ...
"""
import sys, json, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0 Safari/537.36",
      "Referer": "https://finance.sina.com.cn/"}


def prefix(code):
    if code.startswith(("6", "5", "9")):
        return "sh" + code
    return "sz" + code


def hq(codes):
    syms = ",".join(prefix(c) for c in codes)
    url = "https://hq.sinajs.cn/list=" + syms
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15).read().decode("gbk", "replace")
    out = {}
    for line in raw.strip().split("\n"):
        if "=" not in line:
            continue
        sym, rest = line.split("=", 1)
        code = sym.split("_")[-1][2:]
        f = rest.strip().strip(';"').split(",")
        if len(f) < 32:
            continue
        out[code] = dict(name=f[0], open=float(f[1]), prev=float(f[2]), price=float(f[3]),
                         high=float(f[4]), low=float(f[5]), vol=float(f[8]), amt=float(f[9]))
    return out


def kline(code, n=10):
    url = ("https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
           f"?symbol={prefix(code)}&scale=240&ma=no&datalen={n}")
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15).read().decode("utf-8", "replace")
    return json.loads(raw)


def main():
    codes = sys.argv[1:]
    q = hq(codes)
    for c in codes:
        try:
            qq = q.get(c)
            k = kline(c, 10)
            vols = [float(x["volume"]) for x in k]
            today_vol = qq["vol"] if qq else None
            # 新浪日K最后一根若是今天，则用其之前的5根做基准
            base = vols[-5:]
            avg5 = sum(base) / len(base) if base else None
            ratio = (today_vol / avg5) if (today_vol and avg5) else None
            pct = (qq["price"] / qq["prev"] - 1) * 100 if qq and qq["prev"] else None
            print(f"{c} {qq['name'] if qq else '?':<6} 现{qq['price'] if qq else 0:>8.2f} "
                  f"涨{pct:+5.2f}% 今开{qq['open'] if qq else 0:>8.2f} 高{qq['high'] if qq else 0:>8.2f} "
                  f"低{qq['low'] if qq else 0:>8.2f} | 今量{ (today_vol or 0)/1e6:>7.2f}M "
                  f"前5均{ (avg5 or 0)/1e6:>7.2f}M 环比{ (ratio or 0):>5.2f}x")
        except Exception as e:
            print(f"{c} 失败 {e}")


if __name__ == "__main__":
    main()
