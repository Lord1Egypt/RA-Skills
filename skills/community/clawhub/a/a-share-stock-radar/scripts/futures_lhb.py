#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货持仓龙虎榜（多空席位）查询 —— 数据源：东方财富 datacenter (RPT_FUTU_DAILYPOSITION)
一次可取某合约前20会员的「多单/空单持仓 + 增减」，算多空合计与净持仓。

用法：
  python3 futures_lhb.py V2701            # 最新有数据交易日
  python3 futures_lhb.py V2701 --date 2026-09-28
  python3 futures_lhb.py V2701 --json     # 机器可读
"""
import sys, json, argparse, datetime
import requests

URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}


def _get(code, date=None):
    f = f'(SECURITY_CODE="{code}")'
    if date:
        f += f"(TRADE_DATE='{date}')"
    # 先按日期倒序取该合约全部，再取最新交易日
    q = {
        "reportName": "RPT_FUTU_DAILYPOSITION",
        "columns": "ALL",
        "filter": f,
        "sortTypes": "-1",
        "sortColumns": "TRADE_DATE",
        "pageNumber": "1",
        "pageSize": "300",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(URL, params=q, headers=HDR, timeout=30)
    r.raise_for_status()
    d = r.json()
    res = d.get("result") or {}
    rows = res.get("data") or []
    if not date and rows:
        rows = [x for x in rows if x["TRADE_DATE"][:10] == rows[0]["TRADE_DATE"][:10]]
    return rows


def run(code, date=None):
    rows = _get(code, date)
    if not rows:
        print(f"[{code}] 无数据（{date or '最新'}）")
        return None
    tr = rows[0]["TRADE_DATE"][:10]
    settle = rows[0].get("SETTLE_PRICE")
    longs = sorted([r for r in rows if (r.get("LP_RANK") or 9999) <= 20],
                   key=lambda r: r.get("LP_RANK") or 9999)
    shorts = sorted([r for r in rows if (r.get("SP_RANK") or 9999) <= 20],
                    key=lambda r: r.get("SP_RANK") or 9999)
    lp = sum((r.get("LONG_POSITION") or 0) for r in longs)
    sp = sum((r.get("SHORT_POSITION") or 0) for r in shorts)
    lpc = sum((r.get("LP_CHANGE") or 0) for r in longs)
    spc = sum((r.get("SP_CHANGE") or 0) for r in shorts)
    out = {
        "contract": code, "date": tr, "settle": settle,
        "long": {"top20": lp, "change": lpc, "n": len(longs)},
        "short": {"top20": sp, "change": spc, "n": len(shorts)},
        "net_long": lp - sp, "net_change": lpc - spc,
        "long_rows": [{"rank": r.get("LP_RANK"), "member": r.get("MEMBER_NAME_ABBR"),
                       "pos": r.get("LONG_POSITION"), "chg": r.get("LP_CHANGE"),
                       "avg": r.get("LP_AVERAGE_PRICE")} for r in longs],
        "short_rows": [{"rank": r.get("SP_RANK"), "member": r.get("MEMBER_NAME_ABBR"),
                        "pos": r.get("SHORT_POSITION"), "chg": r.get("SP_CHANGE"),
                        "avg": r.get("SP_AVERAGE_PRICE")} for r in shorts],
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("contract", nargs="?", default="V2701")
    ap.add_argument("--date", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    o = run(a.contract, a.date)
    if not o:
        sys.exit(1)
    if a.json:
        print(json.dumps(o, ensure_ascii=False))
        return
    print(f"===== {o['contract']} 持仓龙虎榜 · {o['date']}（结算 {o['settle']}）=====")
    print(f"前20多头合计 {o['long']['top20']:,} 手（增减 {o['long']['change']:+,}）")
    print(f"前20空头合计 {o['short']['top20']:,} 手（增减 {o['short']['change']:+,}）")
    print(f"净持仓(多-空) {o['net_long']:+,} 手 ｜ 净增减 {o['net_change']:+,}")
    verdict = "多头占优" if o['net_long'] > 0 else "空头占优"
    print(f"=> {verdict}（前20席位）\n")
    print("多头龙虎榜 TOP10：")
    for r in o["long_rows"][:10]:
        print(f"  {r['rank']:>2} {r['member']:<14} 多单 {r['pos']:>7,}  增减 {r['chg']:>+7,}  均价 {r['avg']}")
    print("空头龙虎榜 TOP10：")
    for r in o["short_rows"][:10]:
        print(f"  {r['rank']:>2} {r['member']:<14} 空单 {r['pos']:>7,}  增减 {r['chg']:>+7,}  均价 {r['avg']}")


if __name__ == "__main__":
    main()
