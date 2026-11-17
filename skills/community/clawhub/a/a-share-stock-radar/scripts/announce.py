#!/usr/bin/env python3
"""
公告 / 事件排雷（选股必跑）

补的缺口：个股突发利空（减持/解禁/监管/预亏…）一直是盲区。

用法:
  python3 announce.py 002487 601218 [--days 90] [--all]
    --all  打印全部公告（默认只打印命中的风险条目）
数据源：东财公告 np-anotice-stock + 东财限售解禁 RPT_LIFT_STAGE。
"""
import argparse
import datetime as dt
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import em_json, http_json  # noqa: E402

# 风险关键词 → (等级, 说明)
RISK = [
    ("减持", "🔴", "股东减持"),
    ("解禁", "🔴", "限售解禁"),
    ("质押", "🟠", "股权质押"),
    ("冻结", "🔴", "股份冻结"),
    ("监管", "🔴", "监管函/关注函"),
    ("问询", "🟠", "交易所问询"),
    ("警示", "🟠", "警示函"),
    ("处罚", "🔴", "行政处罚"),
    ("立案", "🔴", "立案调查"),
    ("调查", "🔴", "调查"),
    ("风险提示", "🟠", "风险提示"),
    ("退市", "🔴", "退市风险"),
    ("ST", "🔴", "ST/风险警示"),
    ("商誉", "🟠", "商誉减值"),
    ("预亏", "🔴", "业绩预亏"),
    ("预减", "🟠", "业绩预减"),
    ("下修", "🟠", "业绩下修"),
    ("终止", "🟠", "终止/中止"),
    ("诉讼", "🟠", "诉讼仲裁"),
    ("违规", "🟠", "违规"),
    ("担保", "🟡", "对外担保"),
    ("停牌", "🟠", "停牌"),
    ("澄清", "🟡", "澄清公告"),
    ("重组", "🟡", "重大重组"),
    ("收购", "🟡", "收购/并购"),
]


def fetch_ann(code):
    url = ("https://np-anotice-stock.eastmoney.com/api/security/ann"
           "?sr=-1&page_size=30&page_index=1&ann_type=A&client_source=web&stock_list={}"
           "&f_node=0&s_node=0".format(code))
    try:
        d = http_json(url, referer="https://data.eastmoney.com/")
        return d.get("data", {}).get("list", []) or []
    except Exception as e:
        return [{"_err": str(e)}]


def fetch_lift(code):
    """未来解禁批次。"""
    try:
        d = em_json("https://datacenter-web.eastmoney.com/api/data/v1/get",
                    {"reportName": "RPT_LIFT_STAGE", "columns": "ALL", "pageSize": "20",
                     "sortColumns": "FREE_DATE", "sortTypes": "-1",
                     "filter": '(SECURITY_CODE="{}")'.format(code)},
                    referer="https://data.eastmoney.com/")
        return (d.get("result") or {}).get("data", []) or []
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser(description="公告/事件排雷")
    ap.add_argument("codes", nargs="+")
    ap.add_argument("--days", type=int, default=90, help="解禁前瞻天数")
    ap.add_argument("--all", action="store_true", help="打印全部公告")
    a = ap.parse_args()

    today = dt.date.today()
    for code in a.codes:
        print("=" * 56)
        print("【{}】公告 / 事件排雷".format(code))
        anns = fetch_ann(code)
        if anns and anns[0].get("_err"):
            print("  ⚠️ 公告接口失败：{}".format(anns[0]["_err"])); anns = []
        hits = []
        for it in anns:
            title = (it.get("title") or "").strip()
            date = (it.get("notice_date") or "")[:10]
            for kw, lvl, desc in RISK:
                if kw in title:
                    hits.append((date, lvl, desc, title)); break
        if a.all:
            for it in anns:
                print("  {} {}".format((it.get("notice_date") or "")[:10], (it.get("title") or "").strip()))
        elif hits:
            for date, lvl, desc, title in hits:
                print("  {} {} {} —— {}".format(date, lvl, desc, title))
            print("  → 命中 {} 条风险公告".format(len(hits)))
        else:
            print("  近30条公告无风险关键词 ✅")

        # 解禁
        lifts = fetch_lift(code)
        up = []
        for L in lifts:
            try:
                fd = dt.date.fromisoformat((L.get("FREE_DATE") or "")[:10])
            except Exception:
                continue
            if fd >= today:
                up.append((fd, L))
        up.sort(key=lambda x: x[0])
        if up:
            print("  🔴 未来解禁：")
            for fd, L in up[:5]:
                if (fd - today).days > a.days:
                    continue
                print("     {} 解禁{:.0f}万股 / 市值{:.0f}万 / 占比{:.2f}%（{}）".format(
                    fd.isoformat(), float(L.get("FREE_SHARES") or 0),
                    float(L.get("LIFT_MARKET_CAP") or 0), float(L.get("FREE_RATIO") or 0) * 100,
                    L.get("FREE_SHARES_TYPE", "")))
        else:
            print("  ✅ 无未来解禁记录")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
