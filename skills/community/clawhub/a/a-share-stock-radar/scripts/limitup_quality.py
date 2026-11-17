#!/usr/bin/env python3
"""
涨停板质量（封单强度 + 首封时间 + 连板）

用法:
  python3 .../limitup_quality.py [YYYYMMDD]            # 全部涨停
  python3 .../limitup_quality.py [YYYYMMDD] --early    # 只要早盘板(≤10:00)
数据源：东财 push2ex getTopicZTPool。
判定：封单额/流通市值 = 封单强度（越大越硬）；首封越早越强；连板数=梯队位置。
"""
import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_json  # noqa: E402

UT = "7eea3edcaed734bea9cbfc24409ed989"
URL = ("https://push2ex.eastmoney.com/getTopicZTPool?ut=" + UT +
       "&dpt=wz.ztzt&Pageindex=0&pagesize=300&sort=fbt%3Aasc&date={d}")


def _t(v):
    """92500 -> 09:25:00"""
    s = str(int(v)).zfill(6)
    return "{}:{}:{}".format(s[:2], s[2:4], s[4:6])


def main():
    ap = argparse.ArgumentParser(description="涨停板质量")
    ap.add_argument("date", nargs="?", default="")
    ap.add_argument("--early", action="store_true", help="只看早盘板 ≤10:00")
    a = ap.parse_args()
    d = a.date or ""
    import datetime as dt
    if not d:
        d = dt.date.today().strftime("%Y%m%d")

    obj = http_json(URL.format(d=d), referer="https://quote.eastmoney.com/")
    data = obj.get("data") or {}
    pool = data.get("pool") or []
    if not pool:
        print("（{} 无涨停池数据）".format(d)); return 1

    rows = []
    for x in pool:
        fbt = x.get("fbt", 0)
        rows.append({
            "code": x.get("c"), "name": x.get("n"), "price": (x.get("p") or 0) / 1000.0,
            "lbc": x.get("lbc", 1), "hs": x.get("hs") or 0, "fbt": fbt, "lbt": x.get("lbt", 0),
            "fund": x.get("fund") or 0, "ltsz": x.get("ltsz") or 0, "hybk": x.get("hybk") or "",
            "zbc": x.get("zbc") or 0,
        })
    if a.early:
        rows = [r for r in rows if r["fbt"] <= 100000]

    print("==== 涨停板质量 · {} · 共 {} 只 ====".format(d, len(rows)))
    print("{:<7} {:<9} {:>4} {:>7} {:>11} {:<9} {:<10}".format(
        "代码", "名称", "连板", "换手%", "封单(万)", "首封", "行业"))
    for r in sorted(rows, key=lambda r: (-r["lbc"], -r["fund"])):
        print("{:<7} {:<9} {:>4} {:>7.1f} {:>11.0f} {:<9} {:<10}".format(
            r["code"], r["name"][:8], r["lbc"], r["hs"], r["fund"] / 1e4, _t(r["fbt"]), r["hybk"][:9]))

    early = [r for r in rows if r["fbt"] <= 100000]
    late = [r for r in rows if r["fbt"] >= 140000]
    print("-" * 60)
    print("早盘板(≤10:00) {} 只 ｜ 尾盘板(≥14:00) {} 只 ｜ 最高 {} 板".format(
        len(early), len(late), max([r["lbc"] for r in rows], default=0)))
    print("梯队：" + " ".join("{}板×{}".format(b, sum(1 for r in rows if r["lbc"] == b))
                             for b in sorted({r["lbc"] for r in rows}, reverse=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
