#!/usr/bin/env python3
"""
竞价雷达（9:15–9:25 集合竞价专用）

补的缺口：老板 playbook 里的「竞价/早盘异动」形态一直没数据源。
- 腾讯行情在竞价时段：现价(字段3)=虚拟开盘参考价，成交量(6)=竞价累计量，成交额(37，万)
- 高开幅度 = (虚拟开盘 - 昨收)/昨收
- 竞价强度 = 竞价量 / 昨日全天量（正常 1–3%，>5% 为明显异动）
- 撤单检测：两次 snapshot 对比，9:20 前量缩水 = 撤单（9:20 后不可撤）

用法:
  python3 auction.py snapshot 002487 601218      # 抓一次，落 trading/alerts/auction_<日期>.json
  python3 auction.py snapshot 002487            # 同日再抓 → 自动与上次对比，报撤单/加单
数据源：腾讯 qt.gtimg.cn（稳定）；昨日量用腾讯日K ifzq.gtimg.cn。
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_get, tencent_quote_symbol, ws_root  # noqa: E402

ALERT_DIR = os.path.join(ws_root(), "trading", "alerts")
WATCHLIST = os.path.join(ALERT_DIR, "watchlist.txt")   # 每行一个代码，# 注释


def load_watchlist():
    if not os.path.exists(WATCHLIST):
        return []
    out = []
    for ln in open(WATCHLIST, encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if ln:
            out.append(ln.split()[0])
    return out


def tq(codes):
    """腾讯实时：返回 {code: {...}}"""
    out = {}
    ids = ",".join(tencent_quote_symbol(c) for c in codes)
    txt = http_get("https://qt.gtimg.cn/q=" + ids, referer="https://gu.qq.com/", encoding="gbk")
    for line in txt.strip().split(";"):
        if '"' not in line:
            continue
        p = line.split('"')[1].split("~")
        if len(p) < 40:
            continue
        def f(i):
            try:
                return float(p[i])
            except Exception:
                return 0.0
        out[p[2]] = {
            "name": p[1], "price": f(3), "prev": f(4), "open": f(5),
            "vol": f(6), "amount_wan": f(37), "high": f(33), "low": f(34),
            "ts": p[30], "chg_pct": f(32),
        }
    return out


def prev_vol(code):
    """昨日全天成交量（手）；腾讯日K倒数第2行。"""
    try:
        sym = tencent_quote_symbol(code)
        d = json.loads(http_get(
            "https://ifzq.gtimg.cn/appstock/app/fqkline/get?param={},day,,,3,qfq".format(sym),
            referer="https://gu.qq.com/"))
        node = d["data"][sym]
        k = node.get("qfqday") or node.get("day") or []
        if len(k) >= 2:
            # 最后一行为今日（未收盘），倒数第二为昨日
            return float(k[-2][5])
    except Exception:
        pass
    return 0.0


def snap_path():
    return os.path.join(ALERT_DIR, "auction_{}.json".format(dt.date.today().isoformat()))


def cmd_snapshot(a):
    codes = a.codes or load_watchlist()
    if not codes:
        print("无代码，且自选清单 {} 为空。用法: auction.py snapshot <codes...> 或先写 watchlist.txt".format(WATCHLIST))
        return 1
    q = tq(codes)
    if not q:
        print("取价失败（腾讯不可达）")
        return 1
    prev = {}
    if os.path.exists(snap_path()):
        try:
            prev = json.load(open(snap_path(), encoding="utf-8")).get("data", {})
        except Exception:
            prev = {}

    print("==== 竞价雷达 {} ====".format(dt.datetime.now().strftime("%m-%d %H:%M:%S")))
    _now = dt.datetime.now()
    if not (9 * 60 + 15 <= _now.hour * 60 + _now.minute <= 9 * 60 + 25):
        print("⚠️ 非竞价时段（9:15–9:25）。下面为当前快照，竞价强度/高开仅供参考。")
    print("{:<8} {:<8} {:>7} {:>7} {:>8} {:>9} {:>7}".format(
        "代码", "名称", "虚拟开", "高开%", "竞价量(手)", "昨日量(手)", "竞价强度"))
    rows = []
    for c in codes:
        it = q.get(c)
        if not it:
            print("{:<8} 取价失败".format(c)); continue
        gap = (it["price"] / it["prev"] - 1) * 100 if it["prev"] else 0.0
        pv = prev_vol(c)
        intensity = (it["vol"] / pv * 100) if pv else 0.0
        print("{:<8} {:<8} {:>7.2f} {:>+7.2f} {:>8.0f} {:>9.0f} {:>6.2f}%".format(
            c, it["name"][:6], it["price"], gap, it["vol"], pv, intensity))
        rows.append({"code": c, "name": it["name"], "price": it["price"], "gap": round(gap, 2),
                     "vol": it["vol"], "prev_vol": pv, "intensity": round(intensity, 2),
                     "ts": it["ts"]})
    os.makedirs(ALERT_DIR, exist_ok=True)
    json.dump({"date": dt.date.today().isoformat(), "at": dt.datetime.now().isoformat(),
               "data": {r["code"]: r for r in rows}}, open(snap_path(), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 与上次对比 → 撤单
    if prev:
        print("\n与上次快照对比（撤单检测）：")
        any_c = False
        for r in rows:
            p = prev.get(r["code"])
            if not p:
                continue
            dv = r["vol"] - p["vol"]
            if abs(dv) < 1:
                continue
            any_c = True
            tag = "🔻 撤单" if dv < 0 else "🔺 加单"
            print("  {} {} 量 {:.0f}→{:.0f}（{:+.0f}） {}".format(
                r["code"], r["name"][:6], p["vol"], r["vol"], dv, tag))
        if not any_c:
            print("  （无明显增减）")
    print("\n提示：竞价强度>5% 且 高开>2% = 竞价异动候选；9:20 前的量缩水多为撤单诱多。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="竞价雷达")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("snapshot"); ps.add_argument("codes", nargs="*"); ps.set_defaults(func=cmd_snapshot)
    a = ap.parse_args()
    sys.exit(a.func(a) or 0)


if __name__ == "__main__":
    main()
