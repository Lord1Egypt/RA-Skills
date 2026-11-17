#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临时辅助：新浪个股资金流历史（主力=超大+大 r0_net），近N日趋势判定。
用法: python3 _flowtrend.py 600552 301217 ...
"""
import sys, json, urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://finance.sina.com.cn/"}


def prefix(code):
    return ("sh" if code.startswith(("6", "5", "9")) else "sz") + code


def hist(code, num=8):
    url = ("https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
           f"MoneyFlow.ssl_qsfx_zjlrqs?daima={prefix(code)}&num={num}&sort=opendate&asc=0&rand=0.5")
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15).read().decode("utf-8", "replace")
    return json.loads(raw)


def main():
    for code in sys.argv[1:]:
        try:
            rows = hist(code, 8)
            rows = list(reversed(rows))  # 旧->新
            r0 = [(r["opendate"], float(r["r0_net"]) / 1e8) for r in rows]
            last3 = [v for _, v in r0[-3:]]
            pos = sum(1 for v in last3 if v > 0)
            last5 = r0[-5:]
            s5 = sum(v for _, v in last5)
            tag = "连续流入" if pos == 3 else ("反复/脉冲" if pos in (1, 2) else "连续流出")
            seq = " ".join(f"{d[5:]}={v:+.2f}" for d, v in last5)
            print(f"{code} 近5日主力净额(亿): {seq} | 近3日 {pos}/3 为正 → {tag} | 近5日合计 {s5:+.2f}亿")
        except Exception as e:
            print(f"{code} 失败 {e}")


if __name__ == "__main__":
    main()
