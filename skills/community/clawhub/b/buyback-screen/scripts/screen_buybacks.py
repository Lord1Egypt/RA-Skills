#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
screen_buybacks.py — 筛选最近发布回购公告的A股公司，可按市盈率等条件过滤

数据源：东方财富数据中心 (datacenter-web.eastmoney.com)
  1) RPTA_WEB_GETHGLIST_NEW    回购计划/预案列表
  2) RPT_VALUEANALYSIS_DET     个股估值（PE-TTM / PB / 总市值 / 收盘价）

用法示例：
  python screen_buybacks.py                          # 默认近14天的回购公告
  python screen_buybacks.py --days 30                # 近30天
  python screen_buybacks.py --from 2026-08-01        # 指定起始日期
  python screen_buybacks.py --max-pe 15              # 只看市盈率(TTM)<=15（正盈利）
  python screen_buybacks.py --max-pe 15 --purpose 注销减资
  python screen_buybacks.py --progress 001           # 只看新发预案
  python screen_buybacks.py --min-amount-wan 50000 --days 30   # 回购金额>=5亿
  python screen_buybacks.py --out my.tsv             # 自定义输出文件名

输出：stdout 打印 markdown 表格；同时写入 --out 指定的 UTF-8 TSV 文件。
     （Windows 控制台可能无法显示中文，请以输出文件为准 / 用 Read 读取展示。）
"""

import argparse
import json
import re
import sys
import time
import datetime
import urllib.parse
import urllib.request

API = "https://datacenter-web.eastmoney.com/api/data/v1/get"
REPUR_REPORT = "RPTA_WEB_GETHGLIST_NEW"   # 回购计划
VALUE_REPORT = "RPT_VALUEANALYSIS_DET"    # 估值

PAGE_SIZE = 300
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

PROGRESS_MAP = {
    "001": "预案",
    "002": "审议",
    "003": "股东大会",
    "004": "进展",
    "006": "进展",
    "007": "完成",
}


def fetch(report, params, retries=3):
    params = dict(params)
    params.setdefault("source", "WEB")
    params.setdefault("client", "WEB")
    url = API + "?" + urllib.parse.urlencode(params)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            d = json.load(urllib.request.urlopen(req, timeout=40))
            if d.get("success"):
                return d.get("result") or {}
            last = d.get("message")
        except Exception as e:
            last = repr(e)
        time.sleep(1.0)
    raise RuntimeError("fetch %s failed: %s" % (report, last))


def fetch_repurchases(cutoff):
    """拉取 DIM_DATE >= cutoff 的回购计划，DIM_DATE 按降序分页。"""
    rows, page = [], 1
    while page <= 20:
        res = fetch(REPUR_REPORT, {
            "reportName": REPUR_REPORT, "columns": "ALL",
            "pageNumber": page, "pageSize": PAGE_SIZE,
            "sortColumns": "DIM_DATE", "sortTypes": "-1",
        })
        data = res.get("data") or []
        if not data:
            break
        keep = [r for r in data if (r.get("DIM_DATE") or "")[:10] >= cutoff]
        rows.extend(keep)
        # 已排降序：本页没有任何 >= cutoff 的记录，说明后面更旧，可停止
        if len(keep) == 0:
            break
        if page >= res.get("pages", page):
            break
        page += 1
        time.sleep(0.3)
    return rows


def fetch_valuations(codes):
    """批量拉取估值，按 TRADE_DATE 降序，每只股票取最近一条。"""
    info = {}
    for i in range(0, len(codes), 100):
        chunk = codes[i:i + 100]
        filt = '(SECURITY_CODE in ("' + '","'.join(chunk) + '"))'
        res = fetch(VALUE_REPORT, {
            "reportName": VALUE_REPORT, "columns": "ALL",
            "pageNumber": 1, "pageSize": 1000,
            "sortColumns": "TRADE_DATE", "sortTypes": "-1",
            "filter": filt,
        })
        for r in res.get("data") or []:
            c = r["SECURITY_CODE"]
            if c not in info:  # 已按 TRADE_DATE 降序，第一条即最新
                info[c] = r
        time.sleep(0.3)
    return info


def ann_date(r):
    m = re.search(r"(\d{4})[.\.](\d{1,2})[.\.](\d{1,2})\s*公告", r.get("REMARK") or "")
    if m:
        return "%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3)))
    return (r.get("DIM_DATE") or "")[:10]


def purpose_tag(o):
    o = o or ""
    if "员工持股" in o or "股权激励" in o:
        return "员工持股/股权激励"
    if "可转债" in o or "可转换" in o:
        return "可转债转股"
    if "注销" in o and "注册资本" in o:
        return "注销减资"
    if "维护公司价值" in o or "股东权益" in o or "市值" in o:
        return "市值管理"
    return "其他"


def market_of(r):
    s = r.get("SECUCODE") or ""
    if s.endswith(".BJ"):
        return "北交所"
    if s.endswith(".SZ"):
        return "深"
    return "沪"


def amount_str(r):
    lo, hi = r.get("REPURAMOUNTLOWER"), r.get("REPURAMOUNTLIMIT")
    if lo is None and r.get("REPURAMOUNT"):
        lo = r["REPURAMOUNT"]
    if lo is not None and hi is not None:
        return "%.0f~%.0f" % (lo / 1e4, hi / 1e4)
    if lo is not None:
        return "%.0f" % (lo / 1e4)
    return "-"


def main():
    ap = argparse.ArgumentParser(description="筛选最近发布回购公告的A股公司")
    ap.add_argument("--days", type=int, default=14, help="回溯天数（默认14）")
    ap.add_argument("--from", dest="from_date", default=None,
                    help="起始日期 YYYY-MM-DD（优先于 --days）")
    ap.add_argument("--max-pe", type=float, default=None, help="市盈率(TTM)上限（默认排除亏损）")
    ap.add_argument("--min-pe", type=float, default=None, help="市盈率(TTM)下限")
    ap.add_argument("--include-loss", action="store_true",
                    help="--max-pe 时把亏损股(PE<0)也纳入范围")
    ap.add_argument("--min-amount-wan", type=float, default=None, help="拟回购金额下限(万元)")
    ap.add_argument("--purpose", default=None,
                    help="按用途过滤：员工持股/股权激励|注销减资|市值管理|可转债转股|其他")
    ap.add_argument("--progress", default=None, help="按进度过滤：001预案/004进展/007完成")
    ap.add_argument("--out", default=None, help="输出 TSV 文件名")
    ap.add_argument("--top", type=int, default=None, help="只显示前 N 条（按公告日倒序）")
    args = ap.parse_args()

    if args.from_date:
        cutoff = args.from_date
    else:
        cutoff = (datetime.date.today() - datetime.timedelta(days=args.days)).strftime("%Y-%m-%d")

    # 1) 回购计划
    rows = fetch_repurchases(cutoff)
    # 同一公司可能出现多期计划，按代码去重，保留最新一期
    dedup = {}
    for r in rows:
        c = r["DIM_SCODE"]
        if c not in dedup or r.get("DIM_DATE", "") > dedup[c].get("DIM_DATE", ""):
            dedup[c] = r
    rows = list(dedup.values())
    print("# 最近回购公告 A股公司  (数据截至今日，窗口 >= %s，共 %d 家)" % (cutoff, len(rows)))

    # 2) 估值联表
    vals = fetch_valuations([r["DIM_SCODE"] for r in rows])

    # 3) 组装 + 过滤
    out, excluded_loss = [], []
    for r in sorted(rows, key=lambda x: ann_date(x), reverse=True):
        v = vals.get(r["DIM_SCODE"]) or {}
        pe = v.get("PE_TTM")
        rec = {
            "公告日": ann_date(r),
            "代码": r["DIM_SCODE"],
            "名称": r["SECURITYSHORTNAME"],
            "板块": market_of(r),
            "回购金额(万)": amount_str(r),
            "价格上限": r.get("REPURPRICECAP"),
            "PE(TTM)": pe,
            "PB": v.get("PB_MRQ"),
            "现价": v.get("CLOSE_PRICE"),
            "总市值(亿)": round(v["TOTAL_MARKET_CAP"] / 1e8, 1) if v.get("TOTAL_MARKET_CAP") else None,
            "用途": purpose_tag(r.get("REPUROBJECTIVE")),
            "进度": PROGRESS_MAP.get(r.get("REPURPROGRESS"), r.get("REPURPROGRESS")),
            "状态": "亏损" if (pe is not None and pe < 0) else "盈利",
        }
        # PE 过滤仅在显式给出时生效；否则亏损股照常展示（状态列标"亏损"）
        if args.min_pe is not None and (pe is None or pe < args.min_pe):
            continue
        if args.max_pe is not None:
            if not args.include_loss and pe is not None and pe < 0:
                excluded_loss.append(rec)
                continue
            if pe is None or pe > args.max_pe:
                continue
        if args.min_amount_wan is not None:
            m = re.match(r"(\d+)~", rec["回购金额(万)"])
            if not (m and float(m.group(1)) >= args.min_amount_wan):
                continue
        if args.purpose and rec["用途"] != args.purpose:
            continue
        if args.progress and PROGRESS_MAP.get(rec["进度"]) != args.progress \
                and rec["进度"] != args.progress:
            continue
        out.append(rec)

    out.sort(key=lambda z: z["公告日"], reverse=True)
    if args.top:
        out = out[:args.top]

    cols = ["公告日", "代码", "名称", "板块", "回购金额(万)", "价格上限",
            "PE(TTM)", "PB", "现价", "总市值(亿)", "用途", "进度", "状态"]

    # markdown 表 → stdout
    def fmt(x):
        if x is None:
            return "-"
        if isinstance(x, float):
            return ("%.2f" % x).rstrip("0").rstrip(".")
        return str(x)

    def render(rows_):
        print("| " + " | ".join(cols) + " |")
        print("|" + "|".join("---" for _ in cols) + "|")
        for rec in rows_:
            print("| " + " | ".join(fmt(rec[c]) for c in cols) + " |")

    pos = [r for r in out if r["状态"] == "盈利"]
    neg = [r for r in out if r["状态"] == "亏损"]
    print("\n## 盈利公司（%d 家）" % len(pos))
    render(pos)
    if neg:
        print("\n## 亏损公司 PE<0（%d 家，单独列出）" % len(neg))
        render(neg)
    if args.max_pe is not None and not args.include_loss and excluded_loss:
        print("\n## 因 --max-pe 被排除的亏损股（%d 家）" % len(excluded_loss))
        render(excluded_loss)

    # TSV 落盘（UTF-8），亏损股也包含在内，状态列标注
    fname = args.out or ("buyback_screen_%s.tsv" % datetime.date.today().strftime("%Y%m%d"))
    with open(fname, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(cols) + "\n")
        for rec in out:
            f.write("\t".join(fmt(rec[c]) for c in cols) + "\n")
    print("\n[已保存] %s (%d 行，含亏损股)" % (fname, len(out)))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
