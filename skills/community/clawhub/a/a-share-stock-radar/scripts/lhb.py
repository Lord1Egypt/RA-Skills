#!/usr/bin/env python3
"""
龙虎榜 / 游资席位 / 资金性质（多源）

⚠️ 龙虎榜是**盘后**数据（交易所 17:30 左右公布）→ 盘中查只能看上一交易日。
   本脚本自动处理：未指定日期且 <17:30 → 自动回退到上一交易日。

用法:
  python3 lhb.py day [YYYY-MM-DD]        # 净买入榜（东财，含游资标签）
  python3 lhb.py api [YYYY-MM-DD]        # 席位明细版（lhb-api：买5卖5营业部）
  python3 lhb.py ngw [YYYY-MM-DD] [--type N]   # 牛股王（--type: 1机构 2游资 3外资 4顶级游资 5一线游资）
  python3 lhb.py stock <code> [date]     # 某股上榜记录（东财）
  python3 lhb.py seat <code>             # 某股历史席位（lhb-api）
数据源：东财 datacenter / lhb-api(fffy520) / 牛股王 stq.niuguwang.com。
"""
import argparse
import datetime as dt
import json
import sys
import urllib.request

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_json  # noqa: E402

BASE = "https://datacenter-web.eastmoney.com/api/data/v1/get"
REF = "https://data.eastmoney.com/"
API = "http://fffy520.gicp.net:8003/api"
NGW = "https://stq.niuguwang.com/taoquant/NewLhb/GetAllStocks?s=_test&version=6.5.1&packtype=1&night=0"


def auto_date(date_arg, now=None):
    now = now or dt.datetime.now()
    if date_arg:
        return date_arg, None
    d = now.date()
    rolled = False
    if now.hour * 60 + now.minute < 17 * 60 + 30:
        d -= dt.timedelta(days=1); rolled = True
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1); rolled = True
    note = ("⚠️ 龙虎榜盘后公布，当前盘中 → 取上一交易日 {}".format(d.isoformat())) if rolled else None
    return d.isoformat(), note


def _post_json(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore"))


# ---------- 东财 ----------
def _em(date, code=None):
    filt = "(TRADE_DATE='{}')".format(date)
    if code:
        filt += "(SECURITY_CODE=\"{}\")".format(code)
    url = ("{}?reportName=RPT_DAILYBILLBOARD_DETAILSNEW&columns=ALL&pageSize=500&pageNumber=1"
           "&filter={}").format(BASE, filt)
    return ((http_json(url, referer=REF).get("result") or {}).get("data")) or []


def _net(r):
    return (r.get("BILLBOARD_BUY_AMT") or 0) - (r.get("BILLBOARD_SELL_AMT") or 0)


def cmd_day(a):
    date, note = auto_date(a.date)
    if note:
        print(note)
    rows = _em(date)
    if not rows:
        print("（{} 无龙虎榜数据）".format(date)); return 1
    rows.sort(key=_net, reverse=True)
    print("==== 龙虎榜 · {} · 共 {} 条 ====".format(date, len(rows)))
    print("{:<7} {:<9} {:>7} {:>8} {:>11} {:>11} {:<22}".format(
        "代码", "名称", "涨幅%", "换手%", "净买入(万)", "成交额(万)", "游资/原因"))
    for r in rows[:30]:
        print("{:<7} {:<9} {:>7.2f} {:>8.2f} {:>11.0f} {:>11.0f} {:<22}".format(
            r.get("SECURITY_CODE", ""), (r.get("SECURITY_NAME_ABBR") or "")[:8],
            r.get("CHANGE_RATE") or 0, r.get("TURNOVERRATE") or 0,
            _net(r) / 1e4, (r.get("BILLBOARD_DEAL_AMT") or 0) / 1e4,
            (r.get("EXPLAIN") or r.get("EXPLANATION") or "")[:21]))
    return 0


def cmd_stock(a):
    date, note = auto_date(a.date)
    if note:
        print(note)
    rows = _em(date, code=a.code)
    if not rows:
        print("{} 近期无龙虎榜记录".format(a.code)); return 1
    for r in rows:
        print("{date} {code} {name} 涨幅{chg:+.2f}% 净买入{net:+.0f}万 | {ex}".format(
            date=r.get("TRADE_DATE", "")[:10], code=r.get("SECURITY_CODE"),
            name=r.get("SECURITY_NAME_ABBR"), chg=r.get("CHANGE_RATE") or 0,
            net=_net(r) / 1e4, ex=(r.get("EXPLAIN") or r.get("EXPLANATION") or "")))
    return 0


# ---------- lhb-api（席位明细） ----------
def cmd_api(a):
    date, note = auto_date(a.date)
    if note:
        print(note)
    try:
        rows = http_json("{}/lhb/daily?date={}".format(API, date)).get("data") or []
    except Exception as e:
        print("lhb-api 失败：{}".format(str(e)[:80])); return 1
    if not rows:
        print("（{} 无数据）".format(date)); return 1
    rows.sort(key=lambda x: x.get("net_buy") or 0, reverse=True)
    print("==== 龙虎榜席位明细 · {} · 共 {} 条 ====".format(date, len(rows)))
    for r in rows[:20]:
        print("{code} {name} {chg:+.2f}% 净买入{net:+.0f}万 | {reason}".format(
            code=r.get("code"), name=r.get("name"), chg=r.get("change") or 0,
            net=r.get("net_buy") or 0, reason=(r.get("reason") or "")[:24]))
        for b in (r.get("brokers", {}) or {}).get("buy", [])[:3]:
            print("     买{} {:<28} 净{:+.0f}万".format(
                b.get("rank"), (b.get("name") or "")[:26], b.get("net") or 0))
    return 0


def cmd_seat(a):
    try:
        rows = http_json("{}/lhb/history?code={}".format(API, a.code)).get("data") or []
    except Exception as e:
        print("lhb-api 失败：{}".format(str(e)[:80])); return 1
    if not rows:
        print("{} 无历史龙虎榜".format(a.code)); return 1
    print("==== {} 历史龙虎榜（{} 条）====".format(a.code, len(rows)))
    for r in rows[-15:]:
        print("{date} {chg:+.2f}% 净买入{net:+.0f}万 | {reason}".format(
            date=r.get("date"), chg=r.get("change") or 0,
            net=r.get("net_buy") or 0, reason=(r.get("reason") or "")[:26]))
    return 0


# ---------- 牛股王（资金性质） ----------
NGW_TYPE = {0: "全部", 1: "机构买入", 2: "游资买入", 3: "外资买入", 4: "顶级游资", 5: "一线游资"}


def cmd_ngw(a):
    date, note = auto_date(a.date)
    if note:
        print(note)
    try:
        d = _post_json(NGW, {"date": date, "searchtype": a.type, "sortname": 2, "sorttype": 2})
    except Exception as e:
        print("牛股王失败：{}".format(str(e)[:80])); return 1
    data = d.get("data") or {}
    stocks = data.get("stocks") or []
    print("==== 牛股王龙虎榜 · {} · 类型[{}] · {} 只 ====".format(
        data.get("date", date), NGW_TYPE.get(a.type, a.type), len(stocks)))
    for s in stocks[:25]:
        print(json.dumps(s, ensure_ascii=False))
    return 0


def main():
    ap = argparse.ArgumentParser(description="龙虎榜/游资/资金性质")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pd = sub.add_parser("day"); pd.add_argument("date", nargs="?", default=""); pd.set_defaults(func=cmd_day)
    ps = sub.add_parser("stock"); ps.add_argument("code"); ps.add_argument("date", nargs="?", default="")
    ps.set_defaults(func=cmd_stock)
    pa = sub.add_parser("api"); pa.add_argument("date", nargs="?", default=""); pa.set_defaults(func=cmd_api)
    pseat = sub.add_parser("seat"); pseat.add_argument("code"); pseat.set_defaults(func=cmd_seat)
    pn = sub.add_parser("ngw"); pn.add_argument("date", nargs="?", default="")
    pn.add_argument("--type", type=int, default=0, help="1机构 2游资 3外资 4顶级游资 5一线游资")
    pn.set_defaults(func=cmd_ngw)
    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
