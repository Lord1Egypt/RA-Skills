#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运营周报 —— 多平台数据汇总 + 环比 + 异常标记 + 图表 spec。

借鉴 ALITA 插件「周报生成」（把几个平台的数据汇成一张周报）。
本 Skill 原本有运营节奏/大促/备货（ops-calendar.md），但缺「多平台数据汇总周报」，
此脚本补上：一次吃进多个平台的周数据，算环比、标异常、出可直接喂给 report_pdf 的 spec。

口径遵守 Skill 铁律：
  R4  转化率用支付买家数 ÷ 访客数
  R5  ROAS = 支付金额 ÷ 广告花费（同一来源，不混平台后台与广告后台）
  R15 每个数字来自输入（S1/S2）；环比与异常是本脚本推算，标「脚本推算」

输入 JSON：
{
  "period": "2026-W39",
  "cur": [
    {"platform":"tb","label":"淘宝","gmv":120000,"orders":820,"buyers":760,
     "visitors":40000,"ad_cost":18000,"refund":6000}
  ],
  "prev": [ ...同上，上周数据... ]
}

用法：
  python weekly_report.py --data w.json
  python weekly_report.py --data w.json --json
  python weekly_report.py --data w.json --spec-out spec.json   # 产出 report_pdf 可用的 spec
  python weekly_report.py --demo
  python weekly_report.py --self-test
退出码：0 正常 / 2 输入错误
"""
import argparse
import json
import os
import sys

# 异常阈值（相对环比变化）
TH = {
    "cvr_drop": 0.20,       # 转化率跌 ≥20% -> P0
    "roas_drop": 0.25,      # ROAS 跌 ≥25%   -> P0
    "refund_up": 0.50,      # 退款率升 ≥50%  -> P0
    "gmv_drop": 0.15,       # GMV 跌 ≥15%    -> P1
    "visitors_drop": 0.25,  # 访客跌 ≥25%    -> P1（流量侧问题）
}


def pct(cur, prev):
    """环比变化率；prev 为 0 或缺失时返回 None（不硬算，避免除零伪装成 0%）。"""
    if prev in (None, 0) or cur is None:
        return None
    return (cur - prev) / float(prev)


def metrics(p):
    """单平台指标。缺字段返回 None，不填 0 充数。"""
    gmv = p.get("gmv")
    buyers = p.get("buyers")
    visitors = p.get("visitors")
    orders = p.get("orders")
    ad = p.get("ad_cost")
    refund = p.get("refund")
    return {
        "platform": p.get("platform"),
        "label": p.get("label") or p.get("platform"),
        "gmv": gmv,
        "orders": orders,
        "buyers": buyers,
        "visitors": visitors,
        "ad_cost": ad,
        "refund": refund,
        "aov": (gmv / buyers) if (gmv and buyers) else None,          # 客单价：支付买家数口径
        "cvr": (buyers / float(visitors)) if (buyers and visitors) else None,
        "roas": (gmv / float(ad)) if (gmv and ad) else None,
        "refund_rate": (refund / float(gmv)) if (refund and gmv) else None,
    }


def compare(cur_m, prev_m):
    """逐项环比 + 异常判定。"""
    deltas = {}
    for k in ("gmv", "orders", "buyers", "visitors", "ad_cost", "refund",
              "aov", "cvr", "roas", "refund_rate"):
        deltas[k] = pct(cur_m.get(k), prev_m.get(k) if prev_m else None)

    issues = []
    d = deltas
    if d["cvr"] is not None and d["cvr"] <= -TH["cvr_drop"]:
        issues.append(("P0", "转化率环比跌 %.0f%%" % (-d["cvr"] * 100), "查详情/评价/价格/竞品，见 funnel_diagnose"))
    if d["roas"] is not None and d["roas"] <= -TH["roas_drop"]:
        issues.append(("P0", "ROAS 环比跌 %.0f%%" % (-d["roas"] * 100), "查出价/人群/素材，见 roi-ads.md"))
    if d["refund_rate"] is not None and d["refund_rate"] >= TH["refund_up"]:
        issues.append(("P0", "退款率环比升 %.0f%%" % (d["refund_rate"] * 100), "查品质/描述不符/物流时效"))
    if d["gmv"] is not None and d["gmv"] <= -TH["gmv_drop"]:
        issues.append(("P1", "GMV 环比跌 %.0f%%" % (-d["gmv"] * 100), "结合流量与转化拆解，见 funnel_diagnose"))
    if d["visitors"] is not None and d["visitors"] <= -TH["visitors_drop"]:
        issues.append(("P1", "访客环比跌 %.0f%%" % (-d["visitors"] * 100), "查流量来源/平台机制变化，见 platform-traffic.md"))
    return deltas, issues


def build(data):
    period = data.get("period", "本期")
    cur = data.get("cur") or []
    prev = data.get("prev") or []
    if not cur:
        raise ValueError("缺少 cur（本期数据）")

    prev_map = {p.get("platform"): metrics(p) for p in prev}

    rows = []
    for p in cur:
        m = metrics(p)
        pm = prev_map.get(m["platform"])
        deltas, issues = compare(m, pm)
        rows.append({"metrics": m, "deltas": deltas, "issues": issues,
                     "has_prev": pm is not None})

    # 汇总（缺失项不计入，避免用 0 拉低/拉高）
    def s(key):
        v = [r["metrics"][key] for r in rows if r["metrics"][key] is not None]
        return sum(v) if v else None

    tgmv, tad = s("gmv"), s("ad_cost")
    tbuyers, tvisitors = s("buyers"), s("visitors")
    totals = {
        "gmv": tgmv, "ad_cost": tad, "orders": s("orders"),
        "buyers": tbuyers, "visitors": tvisitors, "refund": s("refund"),
        "roas": (tgmv / float(tad)) if (tgmv and tad) else None,
        "cvr": (tbuyers / float(tvisitors)) if (tbuyers and tvisitors) else None,
        "aov": (tgmv / float(tbuyers)) if (tgmv and tbuyers) else None,
    }
    # 上周汇总（用于整体环比）
    p_all = [prev_map[k] for k in prev_map]
    pg = sum(x["gmv"] for x in p_all if x["gmv"]) or None
    pa = sum(x["ad_cost"] for x in p_all if x["ad_cost"]) or None
    pb = sum(x["buyers"] for x in p_all if x["buyers"]) or None
    pv = sum(x["visitors"] for x in p_all if x["visitors"]) or None
    totals_prev = {
        "gmv": pg, "ad_cost": pa,
        "roas": (pg / float(pa)) if (pg and pa) else None,
        "cvr": (pb / float(pv)) if (pb and pv) else None,
        "aov": (pg / float(pb)) if (pg and pb) else None,
    }
    total_deltas = {k: pct(totals.get(k), totals_prev.get(k))
                    for k in ("gmv", "ad_cost", "roas", "cvr", "aov")}

    all_issues = [(r["metrics"]["label"], lv, msg, act)
                  for r in rows for (lv, msg, act) in r["issues"]]
    p0 = [x for x in all_issues if x[1] == "P0"]
    p1 = [x for x in all_issues if x[1] == "P1"]

    return {"period": period, "rows": rows, "totals": totals,
            "totals_prev": totals_prev, "total_deltas": total_deltas,
            "issues": all_issues, "p0_count": len(p0), "p1_count": len(p1)}


def fmt(v, kind="num"):
    if v is None:
        return "—"
    if kind == "pct":
        return "%.2f%%" % (v * 100)
    if kind == "money":
        return "%.0f" % v
    if kind == "rate":
        return "%.2f" % v
    return "%.0f" % v


def render(r):
    o = []
    t, td = r["totals"], r["total_deltas"]
    o.append("【%s 运营周报】" % r["period"])
    o.append("总 GMV %s 元（环比 %s） | 广告花费 %s 元 | 整体 ROAS %s（环比 %s） | 整体转化率 %s"
             % (fmt(t["gmv"], "money"),
                "—" if td["gmv"] is None else "%+.0f%%" % (td["gmv"] * 100),
                fmt(t["ad_cost"], "money"), fmt(t["roas"], "rate"),
                "—" if td["roas"] is None else "%+.0f%%" % (td["roas"] * 100),
                fmt(t["cvr"], "pct")))
    o.append("异常：P0 %d 条 / P1 %d 条" % (r["p0_count"], r["p1_count"]))
    o.append("")
    o.append("【分平台】")
    for row in r["rows"]:
        m, d = row["metrics"], row["deltas"]
        o.append("  %s：GMV %s（%s） | 客单价 %s | 转化率 %s（%s） | ROAS %s（%s） | 退款率 %s"
                 % (m["label"], fmt(m["gmv"], "money"),
                    "—" if d["gmv"] is None else "%+.0f%%" % (d["gmv"] * 100),
                    fmt(m["aov"]), fmt(m["cvr"], "pct"),
                    "—" if d["cvr"] is None else "%+.0f%%" % (d["cvr"] * 100),
                    fmt(m["roas"], "rate"),
                    "—" if d["roas"] is None else "%+.0f%%" % (d["roas"] * 100),
                    fmt(m["refund_rate"], "pct")))
        for lv, msg, act in row["issues"]:
            o.append("      [%s] %s → 建议：%s" % (lv, msg, act))
    if r["issues"]:
        o.append("")
        o.append("【异常汇总】")
        for label, lv, msg, act in r["issues"]:
            o.append("  %s %s：%s" % (lv, label, msg))
    else:
        o.append("")
        o.append("【异常汇总】本周无触发阈值的异常。")
    o.append("")
    o.append("注：GMV/花费/买家数等为输入数据（S1/S2）；环比与异常判定为本脚本推算值。")
    return "\n".join(o)


def make_spec(r):
    """产出可直接喂给 report_pdf.build 的 spec（数值全部来自计算结果，不手写）。"""
    t = r["totals"]
    labels = [row["metrics"]["label"] for row in r["rows"]]
    gmv = [row["metrics"]["gmv"] or 0 for row in r["rows"]]
    blocks = [
        {"type": "h1", "text": "一、本周结论"},
        {"type": "callout", "tone": "warn" if r["p0_count"] else "ok",
         "text": "%s：总 GMV %.0f 元，整体 ROAS %.2f，整体转化率 %.2f%%。异常 P0 %d 条 / P1 %d 条。%s"
                 % (r["period"], t["gmv"] or 0, t["roas"] or 0, (t["cvr"] or 0) * 100,
                    r["p0_count"], r["p1_count"],
                    "P0 需本周内处理。" if r["p0_count"] else "本周无 P0 异常。")},
        {"type": "kv", "per_row": 4, "items": [
            ["总 GMV", "%.0f 元" % (t["gmv"] or 0)],
            ["广告花费", "%.0f 元" % (t["ad_cost"] or 0)],
            ["整体 ROAS", "%.2f" % (t["roas"] or 0)],
            ["P0 异常", "%d 条" % r["p0_count"]]]},
        {"type": "h1", "text": "二、分平台表现"},
        {"type": "bar", "title": "各平台 GMV（元）", "labels": labels, "values": gmv, "unit": "元"},
        {"type": "table", "header": ["平台", "GMV", "客单价", "转化率", "ROAS", "退款率", "GMV环比"],
         "rows": [[row["metrics"]["label"],
                   "%.0f" % (row["metrics"]["gmv"] or 0),
                   "%.2f" % (row["metrics"]["aov"] or 0),
                   "%.2f%%" % ((row["metrics"]["cvr"] or 0) * 100),
                   "%.2f" % (row["metrics"]["roas"] or 0),
                   "%.2f%%" % ((row["metrics"]["refund_rate"] or 0) * 100),
                   "—" if row["deltas"]["gmv"] is None else "%+.0f%%" % (row["deltas"]["gmv"] * 100)]
                  for row in r["rows"]]},
    ]
    if r["issues"]:
        blocks.append({"type": "h1", "text": "三、异常与建议"})
        blocks.append({"type": "table", "header": ["级别", "平台", "问题", "建议动作"],
                       "rows": [[lv, label, msg, act] for label, lv, msg, act in r["issues"]]})
    blocks.append({"type": "bullets", "items": [
        "口径：转化率 = 支付买家数 ÷ 访客数；ROAS = 支付金额 ÷ 广告花费（同源同窗口）",
        "GMV/花费/买家数为输入数据（S1/S2）；环比与异常判定为脚本推算值",
    ]})
    return {"blocks": blocks}


DEMO = {
    "period": "2026-W39",
    "cur": [
        {"platform": "tb", "label": "淘宝", "gmv": 120000, "orders": 820, "buyers": 760,
         "visitors": 40000, "ad_cost": 18000, "refund": 6000},
        {"platform": "pdd", "label": "拼多多", "gmv": 88000, "orders": 900, "buyers": 880,
         "visitors": 52000, "ad_cost": 15000, "refund": 7200},
        {"platform": "douyin", "label": "抖音", "gmv": 65000, "orders": 400, "buyers": 380,
         "visitors": 30000, "ad_cost": 22000, "refund": 3200},
    ],
    "prev": [
        {"platform": "tb", "label": "淘宝", "gmv": 130000, "orders": 860, "buyers": 800,
         "visitors": 38000, "ad_cost": 17000, "refund": 5200},
        {"platform": "pdd", "label": "拼多多", "gmv": 80000, "orders": 850, "buyers": 830,
         "visitors": 50000, "ad_cost": 14000, "refund": 4000},
        {"platform": "douyin", "label": "抖音", "gmv": 70000, "orders": 430, "buyers": 400,
         "visitors": 29000, "ad_cost": 20000, "refund": 3000},
    ],
}


def main():
    ap = argparse.ArgumentParser(description="多平台运营周报（环比 + 异常 + 图表 spec）")
    ap.add_argument("--data")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--spec-out", help="输出 report_pdf 可用的 spec JSON")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if a.demo:
        data = DEMO
    elif a.data:
        if not os.path.isfile(a.data):
            sys.stderr.write("输入文件不存在: %s\n" % a.data)
            return 2
        with open(a.data, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                sys.stderr.write("JSON 解析失败: %s\n" % e)
                return 2
    else:
        sys.stderr.write("需要 --data / --demo / --self-test 之一\n")
        return 2

    try:
        r = build(data)
    except ValueError as e:
        sys.stderr.write("输入错误: %s\n" % e)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(render(r))

    if a.spec_out:
        with open(a.spec_out, "w", encoding="utf-8") as f:
            json.dump(make_spec(r), f, ensure_ascii=False, indent=2)
        sys.stderr.write("spec 已写入 %s\n" % a.spec_out)
    return 0


def self_test():
    ok = True

    def chk(name, got, exp, tol=1e-6):
        nonlocal ok
        good = (abs(got - exp) < tol) if isinstance(exp, float) else (got == exp)
        print("[%s] %s (got=%s exp=%s)" % ("PASS" if good else "FAIL", name, got, exp))
        if not good:
            ok = False

    # 恒等式：客单价 = GMV / 支付买家数；转化率 = 买家数 / 访客数；ROAS = GMV / 花费
    r = build({"period": "T", "cur": [
        {"platform": "tb", "label": "淘宝", "gmv": 120000, "orders": 820, "buyers": 600,
         "visitors": 30000, "ad_cost": 20000, "refund": 6000}], "prev": []})
    m = r["rows"][0]["metrics"]
    chk("客单价 = gmv/buyers", m["aov"], 200.0, 1e-6)
    chk("转化率 = buyers/visitors", m["cvr"], 0.02, 1e-9)
    chk("ROAS = gmv/ad_cost", m["roas"], 6.0, 1e-9)
    chk("退款率 = refund/gmv", m["refund_rate"], 0.05, 1e-9)
    chk("无上周数据时不硬算环比", r["rows"][0]["deltas"]["gmv"], None)

    # 环比与异常：转化率跌 50%（0.02 -> 0.01）应触发 P0
    r2 = build({"period": "T", "cur": [
        {"platform": "tb", "label": "淘宝", "gmv": 100000, "orders": 500, "buyers": 300,
         "visitors": 30000, "ad_cost": 20000, "refund": 5000}],
        "prev": [{"platform": "tb", "label": "淘宝", "gmv": 100000, "orders": 500,
                  "buyers": 600, "visitors": 30000, "ad_cost": 20000, "refund": 5000}]})
    d = r2["rows"][0]["deltas"]
    chk("转化率环比 = -50%", d["cvr"], -0.5, 1e-9)
    chk("转化率暴跌触发 P0", any(lv == "P0" and "转化率" in msg
                                for lv, msg, _ in r2["rows"][0]["issues"]), True)

    # 无异常场景：完全相同的数据不触发任何异常
    same = {"platform": "tb", "label": "淘宝", "gmv": 100000, "orders": 500,
            "buyers": 600, "visitors": 30000, "ad_cost": 20000, "refund": 5000}
    r3 = build({"period": "T", "cur": [dict(same)], "prev": [dict(same)]})
    chk("数据持平无异常", len(r3["issues"]), 0)
    chk("GMV 环比 = 0", r3["rows"][0]["deltas"]["gmv"], 0.0, 1e-9)

    # 汇总与 spec 可生成
    r4 = build(DEMO)
    chk("汇总 GMV = 三平台之和", r4["totals"]["gmv"], 273000, 1e-6)
    chk("汇总 ROAS = 总GMV/总花费", r4["totals"]["roas"], 273000 / 55000.0, 1e-9)
    spec = make_spec(r4)
    chk("spec 含图表", any(b.get("type") == "bar" for b in spec["blocks"]), True)
    chk("spec 含表格", any(b.get("type") == "table" for b in spec["blocks"]), True)

    # 缺 cur 应报错
    try:
        build({"prev": []})
        chk("缺 cur 应抛错", False, True)
    except ValueError:
        chk("缺 cur 应抛错", True, True)

    print("\n自测：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
