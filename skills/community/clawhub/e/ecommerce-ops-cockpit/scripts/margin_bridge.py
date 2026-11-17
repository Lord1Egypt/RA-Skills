#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GMV / 利润变化归因：Price-Volume-Mix 三分量 + 固定成本销量杠杆 + 毛利桥。

借鉴 ClawHive 的 margin-decomposition（CPG 毛利分解）移植到电商口径。
本 Skill 原本只能报「GMV 环比 -2%」，答不出这 -2% 是**价格跌了、销量跌了还是结构变了**——
本脚本补上归因：把收入与利润的变化拆成可归因的若干分量，并指出主因。

口径遵守 Skill 铁律：
  R3  所有金额由脚本计算，不心算
  R4  销量用支付订单数/买家数
  R15 输入数据为 S1/S2；各效应与归因结论为本脚本推算值

输入 JSON：
{
  "period": "2026-W40",
  "fixed_cost": {"cur": 55000, "prev": 52000},      // 可选，算销量杠杆
  "items": [
    {"name": "淘宝",
     "cur":  {"units": 1420, "asp": 188.7, "unit_cost": 62.0, "ad_cost": 41000, "refund": 13500},
     "prev": {"units": 1380, "asp": 181.9, "unit_cost": 60.0, "ad_cost": 38000, "refund": 11800}}
  ]
}

用法：
  python margin_bridge.py --data m.json
  python margin_bridge.py --data m.json --json
  python margin_bridge.py --demo
  python margin_bridge.py --self-test
退出码：0 正常 / 2 输入错误
"""
import argparse
import json
import os
import sys


def _safe(d, key, default=0.0):
    v = d.get(key)
    return float(v) if v is not None else default


def analyze_item(it):
    """单个对象（平台/SKU）的三分量分解。"""
    name = it.get("name") or it.get("platform") or "?"
    c, p = it.get("cur") or {}, it.get("prev") or {}

    uc, up = _safe(c, "units"), _safe(p, "units")
    ac, ap = _safe(c, "asp"), _safe(p, "asp")
    cc, cp = _safe(c, "unit_cost"), _safe(p, "unit_cost")

    rev_c, rev_p = uc * ac, up * ap
    # 逐品价格效应：本期销量 × 价差（汇总即总收入价格效应）
    price = (ac - ap) * uc
    # 逐品销量效应：上期价 × 量差（仅作明细参考；汇总层用整体均价法，见 analyze）
    volume = (uc - up) * ap

    cogs_c, cogs_p = uc * cc, up * cp
    return {
        "name": name,
        "rev_cur": rev_c, "rev_prev": rev_p, "rev_delta": rev_c - rev_p,
        "price_effect": price, "volume_effect": volume,
        "units_cur": uc, "units_prev": up, "asp_cur": ac, "asp_prev": ap,
        "cogs_cur": cogs_c, "cogs_prev": cogs_p, "cogs_delta": cogs_c - cogs_p,
        "ad_cur": _safe(c, "ad_cost"), "ad_prev": _safe(p, "ad_cost"),
        "refund_cur": _safe(c, "refund"), "refund_prev": _safe(p, "refund"),
    }


def analyze(data):
    items = data.get("items") or []
    if not items:
        raise ValueError("缺少 items（至少一个对象）")
    period = data.get("period", "本期")
    rows = [analyze_item(it) for it in items]

    def s(k):
        return sum(r[k] for r in rows)

    rev_c, rev_p = s("rev_cur"), s("rev_prev")
    uc, up = s("units_cur"), s("units_prev")
    rev_delta = rev_c - rev_p

    # ── 正确的 PVM 三分量（整体均价法）────────────────────────────
    # Price ：逐品「本期量 × 价差」求和
    price = s("price_effect")
    # Volume：上期整体加权均价 × 总销量变化
    p_avg_prev = (rev_p / up) if up else 0.0
    volume = p_avg_prev * (uc - up)
    # Mix   ：各品销量变化 × 该品价格相对整体均价的偏离
    #         （结构转向高价款 → 正；转向低价款 → 负）
    mix = sum((r["asp_prev"] - p_avg_prev) * (r["units_cur"] - r["units_prev"])
              for r in rows)
    # 恒等式：Price + Volume + Mix = ΔRevenue
    identity_ok = abs((price + volume + mix) - rev_delta) < 1e-6

    fc = data.get("fixed_cost") or {}
    fixed_c, fixed_p = _safe(fc, "cur"), _safe(fc, "prev")

    # 固定成本销量杠杆：单位固定成本因销量变化而摊薄/抬升
    unit_f_c = (fixed_c / uc) if uc else None
    unit_f_p = (fixed_p / up) if up else None
    # 正 = 有利（单位固定成本下降，省了钱）
    leverage = ((unit_f_p - unit_f_c) * uc) if (unit_f_c is not None and unit_f_p is not None) else None

    ad_c, ad_p = s("ad_cur"), s("ad_prev")
    rf_c, rf_p = s("refund_cur"), s("refund_prev")
    cogs_delta = s("cogs_delta")

    # 毛利桥：上期经营利润 + 各效应 = 本期经营利润
    profit_p = rev_p - s("cogs_prev") - ad_p - rf_p - fixed_p
    profit_c = rev_c - s("cogs_cur") - ad_c - rf_c - fixed_c
    bridge = [
        ("上期经营利润", profit_p, None),
        ("价格效应", price, "favorable" if price > 0 else "unfavorable"),
        ("销量效应", volume, "favorable" if volume > 0 else "unfavorable"),
        ("结构效应", mix, "favorable" if mix > 0 else "unfavorable"),
        ("成本变化", -cogs_delta, "favorable" if cogs_delta < 0 else "unfavorable"),
        ("退款变化", -(rf_c - rf_p), "favorable" if (rf_c - rf_p) < 0 else "unfavorable"),
        ("推广费变化", -(ad_c - ad_p), "favorable" if (ad_c - ad_p) < 0 else "unfavorable"),
        ("固定成本变化", -(fixed_c - fixed_p), "favorable" if (fixed_c - fixed_p) < 0 else "unfavorable"),
        ("本期经营利润", profit_c, None),
    ]
    bridge_ok = abs(sum(x[1] for x in bridge[1:-1]) + profit_p - profit_c) < 1e-6

    # 主因：绝对值最大的效应
    candidates = {"价格": price, "销量": volume, "结构": mix}
    if rev_delta == 0:
        driver, driver_note = "无变化", "收入与上期持平"
    else:
        driver = max(candidates, key=lambda k: abs(candidates[k]))
        dv = candidates[driver]
        share = (abs(dv) / abs(rev_delta) * 100) if rev_delta else 0
        # 效应为正 = 拉动（正面贡献）；为负 = 拖累（负面贡献）
        direction = "拉动" if dv > 0 else "拖累"
        extra = "（含其他分量对冲）" if share > 100 else ""
        driver_note = "%s效应 %+.0f 元（占收入变化 %.0f%%%s），为%s主因" % (
            driver, dv, share, extra, direction)

    return {"period": period, "rows": rows,
            "rev_cur": rev_c, "rev_prev": rev_p, "rev_delta": rev_delta,
            "rev_delta_pct": (rev_delta / rev_p) if rev_p else None,
            "price_effect": price, "volume_effect": volume, "mix_effect": mix,
            "identity_ok": identity_ok,
            "units_cur": uc, "units_prev": up,
            "unit_fixed_cur": unit_f_c, "unit_fixed_prev": unit_f_p,
            "leverage_effect": leverage,
            "profit_cur": profit_c, "profit_prev": profit_p,
            "bridge": bridge, "bridge_ok": bridge_ok,
            "driver": driver, "driver_note": driver_note}


def render(r):
    o = []
    o.append("【%s 变化归因】" % r["period"])
    o.append("收入 %.0f → %.0f 元（%+.0f 元，%s）"
             % (r["rev_prev"], r["rev_cur"], r["rev_delta"],
                "—" if r["rev_delta_pct"] is None else "%+.1f%%" % (r["rev_delta_pct"] * 100)))
    o.append("")
    o.append("【三分量分解】(Price + Volume + Mix = Δ收入)")
    for label, key in (("价格效应", "price_effect"), ("销量效应", "volume_effect"),
                       ("结构效应", "mix_effect")):
        v = r[key]
        share = (v / r["rev_delta"] * 100) if r["rev_delta"] else 0
        o.append("  %-6s %+12.0f 元   （占变化 %+.0f%%）" % (label, v, share))
    o.append("  恒等式校验：%s" % ("PASS" if r["identity_ok"] else "FAIL"))
    o.append("")
    o.append("【主因】%s" % r["driver_note"])
    if r["leverage_effect"] is not None:
        tag = "有利（销量摊薄固定成本）" if r["leverage_effect"] > 0 else "不利（销量下滑抬升单位固定成本）"
        o.append("【固定成本销量杠杆】%+.0f 元 → %s" % (r["leverage_effect"], tag))
        o.append("  单位固定成本 %.2f → %.2f 元/单"
                 % (r["unit_fixed_prev"] or 0, r["unit_fixed_cur"] or 0))
    o.append("")
    o.append("【经营利润桥】")
    for label, val, tone in r["bridge"]:
        mark = "" if tone is None else ("  ←有利" if tone == "favorable" else "  ←不利")
        o.append("  %-12s %+14.0f 元%s" % (label, val, mark))
    o.append("  桥式校验：%s" % ("PASS" if r["bridge_ok"] else "FAIL"))
    o.append("")
    o.append("注：units/asp/成本为输入数据（S1/S2）；三分量分解、杠杆与桥为本脚本推算值。")
    return "\n".join(o)


def make_spec(r, title=None, subtitle=None):
    """产出可直接喂给 report_pdf.build 的 spec（数值全部来自计算结果，不手写）。"""
    d = r["rev_delta"]
    blocks = [
        {"type": "h1", "text": "一、归因结论"},
        {"type": "callout", "tone": "ok" if d >= 0 else "warn",
         "text": "%s：收入 %.0f → %.0f 元（%+.0f 元，%s）。%s"
                 % (r["period"], r["rev_prev"], r["rev_cur"], d,
                    "—" if r["rev_delta_pct"] is None else "%+.1f%%" % (r["rev_delta_pct"] * 100),
                    r["driver_note"])},
        {"type": "kv", "per_row": 4, "items": [
            ["上期收入", "%.0f" % r["rev_prev"]],
            ["本期收入", "%.0f" % r["rev_cur"]],
            ["收入变化", "%+.0f" % d],
            ["主因", r["driver"]]]},
        {"type": "h1", "text": "二、三分量分解"},
        {"type": "bar", "title": "收入变化三分量（元）",
         "labels": ["价格效应", "销量效应", "结构效应"],
         "values": [r["price_effect"], r["volume_effect"], r["mix_effect"]], "unit": "元"},
        {"type": "table", "header": ["对象", "上期收入", "本期收入", "价格效应", "销量效应", "结构效应"],
         "rows": [[x["name"], "%.0f" % x["rev_prev"], "%.0f" % x["rev_cur"],
                   "%+.0f" % x["price_effect"], "%+.0f" % x["volume_effect"],
                   "%+.0f" % (x["rev_delta"] - x["price_effect"] - x["volume_effect"])]
                  for x in r["rows"]]},
        {"type": "h1", "text": "三、经营利润桥"},
        {"type": "table", "header": ["环节", "金额（元）", "方向"],
         "rows": [[lb, "%.0f" % v, "" if t is None else ("有利" if t == "favorable" else "不利")]
                  for lb, v, t in r["bridge"]]},
    ]
    if r["leverage_effect"] is not None:
        blocks.append({"type": "bullets", "items": [
            "固定成本销量杠杆 %+.0f 元（单位固定成本 %.2f → %.2f 元/单）"
            % (r["leverage_effect"], r["unit_fixed_prev"] or 0, r["unit_fixed_cur"] or 0),
            "口径：转化率=支付买家数÷访客数；收入=销量×客单价",
            "输入数据为 S1/S2；三分量分解、杠杆与利润桥为本脚本推算值（S4）"]})
    spec = {"blocks": blocks}
    if title:
        spec["title"] = title
    if subtitle:
        spec["subtitle"] = subtitle
    return spec


DEMO = {
    "period": "2026-W40",
    "fixed_cost": {"cur": 55000, "prev": 52000},
    "items": [
        {"name": "淘宝",
         "cur": {"units": 1420, "asp": 188.7, "unit_cost": 62.0, "ad_cost": 41000, "refund": 13500},
         "prev": {"units": 1380, "asp": 181.9, "unit_cost": 60.0, "ad_cost": 38000, "refund": 11800}},
        {"name": "京东",
         "cur": {"units": 780, "asp": 197.4, "unit_cost": 71.0, "ad_cost": 23000, "refund": 6200},
         "prev": {"units": 810, "asp": 200.0, "unit_cost": 69.0, "ad_cost": 22500, "refund": 5900}},
        {"name": "拼多多",
         "cur": {"units": 1190, "asp": 80.7, "unit_cost": 44.0, "ad_cost": 14000, "refund": 9800},
         "prev": {"units": 1250, "asp": 80.8, "unit_cost": 42.0, "ad_cost": 13500, "refund": 5100}},
        {"name": "抖音",
         "cur": {"units": 400, "asp": 180.0, "unit_cost": 78.0, "ad_cost": 26000, "refund": 3600},
         "prev": {"units": 490, "asp": 179.6, "unit_cost": 75.0, "ad_cost": 24000, "refund": 3300}},
    ],
}


def main():
    ap = argparse.ArgumentParser(description="GMV/利润变化归因（Price-Volume-Mix + 毛利桥）")
    ap.add_argument("--data")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--spec-out", help="输出 report_pdf 可用的图表 spec JSON")
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
        r = analyze(data)
    except ValueError as e:
        sys.stderr.write("输入错误: %s\n" % e)
        return 2

    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
    if a.spec_out:
        with open(a.spec_out, "w", encoding="utf-8") as f:
            json.dump(make_spec(r, title="%s 变化归因报告" % r["period"]), f,
                      ensure_ascii=False, indent=2)
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

    # 单品：价 10→12，量 100→120
    one = {"items": [{"name": "A",
                      "cur": {"units": 120, "asp": 12, "unit_cost": 5},
                      "prev": {"units": 100, "asp": 10, "unit_cost": 5}}]}
    r = analyze(one)
    chk("收入 1000→1440", r["rev_delta"], 440.0, 1e-6)
    # 价格效应 = (12-10)*120 = 240；销量效应 = (120-100)*10 = 200；Mix = 440-240-200 = 0
    chk("价格效应=240", r["price_effect"], 240.0, 1e-6)
    chk("销量效应=200", r["volume_effect"], 200.0, 1e-6)
    chk("单品结构效应=0", r["mix_effect"], 0.0, 1e-6)
    chk("恒等式成立", r["identity_ok"], True)
    chk("利润桥成立", r["bridge_ok"], True)

    # 多品结构变化：高价款占比上升应产生正 Mix
    two = {"items": [
        {"name": "高价品", "cur": {"units": 200, "asp": 100, "unit_cost": 40},
         "prev": {"units": 100, "asp": 100, "unit_cost": 40}},
        {"name": "低价品", "cur": {"units": 100, "asp": 20, "unit_cost": 8},
         "prev": {"units": 200, "asp": 20, "unit_cost": 8}},
    ]}
    r2 = analyze(two)
    # 收入 100*100+200*20=14000 → 200*100+100*20=22000，Δ=8000
    chk("多品收入变化=8000", r2["rev_delta"], 8000.0, 1e-6)
    chk("多品价格效应=0（价未变）", r2["price_effect"], 0.0, 1e-6)
    # 总销量 300→300 未变 → 销量效应应为 0；全部变化来自结构
    chk("总销量未变→销量效应=0", r2["volume_effect"], 0.0, 1e-6)
    chk("多品恒等式成立", r2["identity_ok"], True)
    # 结构转向高价款 → Mix 为正且等于全部变化 8000
    chk("结构效应=8000", r2["mix_effect"], 8000.0, 1e-6)
    chk("结构效应为正（转向高价款）", r2["mix_effect"] > 0, True)

    # 固定成本销量杠杆：销量涨 → 单位固定成本降 → 有利（正）
    lev = {"fixed_cost": {"cur": 10000, "prev": 10000},
           "items": [{"name": "A", "cur": {"units": 200, "asp": 50, "unit_cost": 20},
                      "prev": {"units": 100, "asp": 50, "unit_cost": 20}}]}
    r3 = analyze(lev)
    # 单位固定成本 100 → 50，杠杆 = (100-50)*200 = 10000（有利，正）
    chk("销量杠杆=+10000（有利）", r3["leverage_effect"], 10000.0, 1e-6)
    chk("单位固定成本 100→50", (r3["unit_fixed_prev"], r3["unit_fixed_cur"]), (100.0, 50.0))

    # 缺 items 应报错
    try:
        analyze({})
        chk("缺 items 应抛错", False, True)
    except ValueError:
        chk("缺 items 应抛错", True, True)

    print("\n自测：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
