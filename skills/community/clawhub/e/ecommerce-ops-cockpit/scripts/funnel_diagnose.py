#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""funnel_diagnose.py —— 店铺漏斗诊断：流量正常不出单 / 转化率下滑 / ROI 做不上去

口径铁律：
  · 转化率一律用「支付买家数 ÷ 访客数」（无支付买家数时用支付订单数，并在报告中标注口径）
  · ROAS/ROI 只能用同一来源（同一后台、同一归因窗口），禁止混用平台后台与广告后台数字
  · 缺数据 = 输出 DATA_MISSING，禁止用行业均值编造

用法：
  python funnel_diagnose.py --self-test
  python funnel_diagnose.py --data funnel.json [--json]
退出码：0 正常输出诊断；2 关键数据缺失（不允许猜测）。
"""

import argparse
import json
import sys

# 粗基准（CTR/CVR），仅用于定位方向，必须允许被真实店铺历史数据覆盖
BENCH = {
    "generic": {"ctr": 0.025, "cvr": 0.030, "add_cart_rate": 0.080, "order_pay_rate": 0.75},
    "tb": {"ctr": 0.030, "cvr": 0.025, "add_cart_rate": 0.090, "order_pay_rate": 0.75},
    "tmall": {"ctr": 0.030, "cvr": 0.025, "add_cart_rate": 0.090, "order_pay_rate": 0.78},
    "jd": {"ctr": 0.025, "cvr": 0.035, "add_cart_rate": 0.100, "order_pay_rate": 0.80},
    "pdd": {"ctr": 0.035, "cvr": 0.045, "add_cart_rate": 0.110, "order_pay_rate": 0.70},
    "douyin": {"ctr": 0.020, "cvr": 0.020, "add_cart_rate": 0.060, "order_pay_rate": 0.65},
    "xhs": {"ctr": 0.040, "cvr": 0.015, "add_cart_rate": 0.050, "order_pay_rate": 0.60},
    "ks": {"ctr": 0.020, "cvr": 0.018, "add_cart_rate": 0.055, "order_pay_rate": 0.62},
    "wx": {"ctr": 0.025, "cvr": 0.022, "add_cart_rate": 0.060, "order_pay_rate": 0.70},
}

ACTIONS = {
    "曝光": ["检查是否进入推荐池：标题/属性完整度、类目准确性、是否违规降权",
             "提高内容供给量：短视频/笔记条数，稳定上新节奏",
             "核对投放预算与人群包是否过窄"],
    "点击率": ["重做主图：卖点前置、场景化、价格锚点", "标题重写：核心词+属性词+场景词",
               "对比同行 TOP10 主图差异，做 A/B 测试"],
    "加购率": ["详情页面向犹豫人群：补充对比表、尺码表、实物视频",
               "价格带与竞品对齐，检查是否高于同款均价", "增加评价/问大家内容，处理差评"],
    "支付转化率": ["检查是否流量不精准：投放人群包与关键词是否偏移",
                   "检查价格/优惠券/库存/发货时效是否异常", "核对评价区是否有新增差评或质量投诉"],
    "下单支付率": ["排查支付链路：优惠券失效、库存不足、运费过高", "设置下单未支付提醒"],
    "客单价": ["组合装/多件优惠拉升件单价", "关联推荐与详情页加购模块"],
    "ROI": ["按 ROAS = 客单价 × 转化率 ÷ CPC 拆解，定位是 CPC 高还是转化率低",
            "低于保本ROI时先砍亏损计划，再放量盈利计划",
            "检查归因窗口与口径是否混用（禁止平台后台与广告后台数字混算）"],
}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def metrics(d, platform="generic"):
    b = BENCH.get(platform, BENCH["generic"])
    imp, clk, vis = _f(d.get("impressions")), _f(d.get("clicks")), _f(d.get("visits"))
    cart, orders, buyers = _f(d.get("add_cart")), _f(d.get("orders")), _f(d.get("pay_buyers"))
    gmv, ad = _f(d.get("gmv")), _f(d.get("ad_spend"))
    m = {}
    missing = []
    if vis is None and buyers is None:
        missing.append("visits/pay_buyers")
    if vis:
        m["访客数"] = vis
        if buyers is not None:
            m["支付转化率"] = buyers / vis
            m["口径"] = "支付买家数 ÷ 访客数"
        elif orders:
            m["支付转化率"] = orders / vis
            m["口径"] = "支付订单数 ÷ 访客数（无支付买家数，口径已标注）"
        if cart:
            m["加购率"] = cart / vis
        if orders and buyers:
            m["下单支付率"] = buyers / orders
    if imp and clk:
        m["点击率"] = clk / imp
    if clk and ad:
        m["CPC"] = ad / clk
    if gmv and buyers:
        m["客单价"] = gmv / buyers
    elif gmv and orders:
        m["客单价"] = gmv / orders
    if gmv and ad:
        m["ROAS"] = gmv / ad
    if gmv and vis:
        m["UV价值"] = gmv / vis
    m["_bench"] = b
    m["_missing"] = missing
    return m


def diagnose(data: dict) -> dict:
    platform = data.get("platform", "generic")
    cur = metrics(data.get("current") or {}, platform)
    prev = metrics(data.get("prev") or {}, platform) if data.get("prev") else None
    if cur["_missing"]:
        return {"verdict": "DATA_MISSING", "missing": cur["_missing"],
                "note": "关键数据缺失，禁止用行业均值替代，请补齐后再诊断"}

    b = cur["_bench"]
    layers = []
    for name, key in (("点击率", "点击率"), ("加购率", "加购率"), ("支付转化率", "支付转化率"), ("下单支付率", "下单支付率")):
        v = cur.get(key)
        if v is None:
            continue
        bench = b.get(key)
        gap_bench = (v / bench - 1) if bench else None
        mom = None
        if prev and prev.get(key):
            mom = v / prev[key] - 1
        score = 0.0
        if gap_bench is not None:
            score += max(0.0, -gap_bench)
        if mom is not None:
            score += max(0.0, -mom) * 1.5
        layers.append({"layer": name, "value": v, "bench": bench, "gap_vs_bench": gap_bench,
                       "mom": mom, "score": round(score, 4)})
    layers.sort(key=lambda x: -x["score"])
    bottleneck = layers[0]["layer"] if layers else None

    notes, actions = [], []
    roas, be = cur.get("ROAS"), _f(data.get("breakeven_roas"))
    if roas is not None and be:
        if roas < be:
            notes.append("当前 ROAS %.2f < 保本 ROI %.2f，投放净亏损" % (roas, be))
            # 拆解：ROAS = 客单价 × 转化率 ÷ CPC
            aov, cvr, cpc = cur.get("客单价"), cur.get("支付转化率"), cur.get("CPC")
            parts = []
            if aov and cvr and cpc:
                parts.append("拆解：客单价 %.2f × 转化率 %.2f%% ÷ CPC %.2f = ROAS %.2f" % (aov, cvr * 100, cpc, roas))
                if cvr < b.get("cvr", 0):
                    parts.append("转化率低于基准（%.2f%% vs %.2f%%），是拉低 ROI 的主因" % (cvr * 100, b["cvr"] * 100))
                if cpc and aov:
                    parts.append("按当前客单价与转化率，可承受最高 CPC = %.2f 元" % (aov * cvr * (1 / be)))
            notes += parts
            actions += ACTIONS["ROI"]
        else:
            notes.append("当前 ROAS %.2f ≥ 保本 ROI %.2f，投放为正贡献，可放量" % (roas, be))
    if data.get("prev"):
        for L in layers:
            if L["mom"] is not None and L["mom"] < -0.10:
                notes.append("%s 环比下滑 %.1f%%（%.2f%% → %.2f%%）" % (
                    L["layer"], -L["mom"] * 100, L["value"] / (1 + L["mom"]) * 100, L["value"] * 100))
    vis_bench_ok = True
    if data.get("prev") and cur.get("访客数") and prev.get("访客数"):
        chg = cur["访客数"] / prev["访客数"] - 1
        if chg > -0.10 and bottleneck in ("支付转化率", "加购率"):
            notes.append("流量基本正常（访客环比 %+.1f%%）但转化层失守 → 属于「有流量不出单」型问题" % (chg * 100))
    if bottleneck:
        actions += ACTIONS.get(bottleneck, [])
    return {"platform": platform, "current": {k: v for k, v in cur.items() if not k.startswith("_")},
            "prev": ({k: v for k, v in prev.items() if not k.startswith("_")} if prev else None),
            "layers": layers, "bottleneck": bottleneck, "notes": notes, "actions": actions,
            "verdict": "BOTTLENECK:" + bottleneck if bottleneck else "OK"}


def render(res: dict) -> str:
    if res["verdict"] == "DATA_MISSING":
        return "【漏斗诊断】DATA_MISSING：缺少 %s，禁止用行业均值编造，请补齐真实数据后重跑" % ",".join(res["missing"])
    o = ["【漏斗诊断】平台=%s  口径=%s" % (res["platform"], res["current"].get("口径", "-"))]
    o.append("  核心指标：" + " | ".join("%s=%s" % (k, ("%.4f" % v) if isinstance(v, float) else v)
                                    for k, v in res["current"].items() if k != "口径"))
    o.append("  漏斗短板排序：")
    for L in res["layers"]:
        seg = "    %-8s 当前 %.2f%%" % (L["layer"], L["value"] * 100)
        if L["bench"]:
            seg += " 基准 %.2f%% (偏差 %+.1f%%)" % (L["bench"] * 100, (L["gap_vs_bench"] or 0) * 100)
        if L["mom"] is not None:
            seg += " 环比 %+.1f%%" % (L["mom"] * 100)
        o.append(seg)
    o.append("  → 主瓶颈：%s" % res["bottleneck"])
    for n in res["notes"]:
        o.append("  · " + n)
    o.append("  建议动作：")
    for a in res["actions"]:
        o.append("    - " + a)
    return "\n".join(o)


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # 场景：流量正常、转化崩 → 主瓶颈应为支付转化率
    d = {"platform": "tb", "breakeven_roas": 4.0,
         "current": {"impressions": 100000, "clicks": 3000, "visits": 9000, "add_cart": 810,
                     "orders": 200, "pay_buyers": 150, "gmv": 19500, "ad_spend": 6000},
         "prev": {"impressions": 100000, "clicks": 3000, "visits": 9000, "add_cart": 800,
                  "orders": 320, "pay_buyers": 270, "gmv": 35100, "ad_spend": 6000}}
    r = diagnose(d)
    chk("主瓶颈=支付转化率", r["bottleneck"] == "支付转化率")
    chk("识别为有流量不出单", any("有流量不出单" in n for n in r["notes"]))
    chk("ROAS<保本 提示亏损", any("净亏损" in n for n in r["notes"]))
    chk("CVR = 150/9000", abs(r["current"]["支付转化率"] - 150 / 9000) < 1e-9)
    chk("CPC = 6000/3000", abs(r["current"]["CPC"] - 2.0) < 1e-9)
    chk("ROAS = 19500/6000", abs(r["current"]["ROAS"] - 3.25) < 1e-9)

    # 场景：缺数据
    r2 = diagnose({"platform": "tb", "current": {"impressions": 100}})
    chk("缺数据 → DATA_MISSING", r2["verdict"] == "DATA_MISSING")

    # 场景：点击率瓶颈
    d3 = {"platform": "tb", "current": {"impressions": 100000, "clicks": 500, "visits": 500,
                                        "add_cart": 45, "orders": 30, "pay_buyers": 25, "gmv": 2500}}
    r3 = diagnose(d3)
    chk("低CTR场景瓶颈=点击率", r3["bottleneck"] == "点击率")
    print("funnel_diagnose self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="店铺漏斗诊断")
    ap.add_argument("--data", help="漏斗数据 JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.data:
        ap.error("需要 --data 或 --self-test")
    with open(a.data, "r", encoding="utf-8") as f:
        res = diagnose(json.load(f))
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else render(res))
    return 2 if res["verdict"] == "DATA_MISSING" else 0


if __name__ == "__main__":
    sys.exit(main())
