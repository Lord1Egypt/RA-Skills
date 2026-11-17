#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
溢价-风险对价计算器 / Premium-vs-Risk Consideration Engine
避雷选品团 4.0 专用定量内核。

设计目的：把「性价比款 vs 质价比款」从口味偏好变成可计算的数字对价。
回答四个问题：
  1. 选性价比款，我实际省了多少钱？（ΔP 现金口径）
  2. 选性价比款，我承担了什么风险？折成年化多少钱？（EAC 风险口径）
  3. 风险是不是大于收益？（ΔEAC 与临界故障率 p*）
  4. 选质价比款，我多付的钱换来多少可量化收益？值不值？（溢价 ROI 与盈亏平衡溢价）

零依赖，仅用标准库。用法见 --help 或 SKILL.md。

示例：
  python3 premium_decision.py all --input case.json
  python3 premium_decision.py tco --price 1999 --hold-years 5 --prob 0.15 --repair 700
  python3 premium_decision.py critprob --delta-price 800 --repair 700 --years 5
  python3 premium_decision.py score --input case.json
  python3 premium_decision.py selftest
"""

import argparse
import json
import math
import sys

DEFAULT_WEIGHTS = {
    "safety": 0.20,       # 安全合规（认证/召回/事故）
    "performance": 0.25,  # 核心性能（对用户场景有效的指标）
    "durability": 0.20,   # 可靠性 / 寿命 / 故障率
    "service": 0.15,      # 售后（保修年限、网点、响应）
    "noise": 0.05,        # 体验细节（噪音/震动/易用）
    "price": 0.15,        # 价格（按 EAC 归一化打分，越低越高分）
}


# ---------- 基础工具 ----------

def _pv_factor(rate, year):
    """第 year 年现金流折现系数（year 从 1 开始）。"""
    if rate <= 0:
        return 1.0
    return 1.0 / ((1.0 + rate) ** year)


def _f(x, nd=1):
    """安全格式化，None/inf 友好。"""
    if x is None:
        return "n/a"
    if isinstance(x, float) and (math.isinf(x) or math.isnan(x)):
        return "∞" if math.isinf(x) else "n/a"
    return round(x, nd)


# ---------- 核心模型 1：TCO / EAC ----------

def tco(price, hold_years, annual_failure_prob=0.0, repair_cost=0.0,
        warranty_years=0.0, annual_consumable=0.0, resale=0.0,
        discount_rate=0.0, one_off_outlay=0.0):
    """
    持有期总拥有成本与等额年成本。

    - 保修期内故障成本由厂商承担，故故障成本只计入 (hold_years - warranty_years) 年，
      且保修期不足整年时按比例折算（warranty_years 可为小数，如 1.5）。
    - 年故障率 annual_failure_prob 为「每年至少故障一次」的概率估计；
      期望年维修支出 = prob × repair_cost。
    - 年消耗按年折现累加；残值在第 hold_years 年末回收并折现。
    - one_off_outlay：隐含首年支出（安装费、必要配件、延保等），计入首年。
    """
    if hold_years <= 0:
        raise ValueError("hold_years 必须 > 0")
    if price < 0:
        raise ValueError("price 不能为负")

    self_insured_years = max(0.0, hold_years - max(0.0, warranty_years))
    annual_failure_cost = max(0.0, annual_failure_prob) * max(0.0, repair_cost)

    repair_pv = 0.0
    consumable_pv = 0.0
    for y in range(1, int(math.ceil(hold_years)) + 1):
        span = min(1.0, hold_years - (y - 1))          # 末年可能不足一年
        f = _pv_factor(discount_rate, y)
        # 故障成本：保修覆盖之后才开始自担
        exposed = max(0.0, min(span, self_insured_years - (y - 1)))
        repair_pv += annual_failure_cost * exposed * f
        consumable_pv += max(0.0, annual_consumable) * span * f

    resale_pv = max(0.0, resale) * _pv_factor(discount_rate, hold_years)
    total = price + max(0.0, one_off_outlay) + repair_pv + consumable_pv - resale_pv
    eac = total / hold_years

    return {
        "price": round(price, 2),
        "hold_years": hold_years,
        "self_insured_years": round(self_insured_years, 2),
        "expected_annual_failure_cost": round(annual_failure_cost, 2),
        "repair_pv": round(repair_pv, 2),
        "consumable_pv": round(consumable_pv, 2),
        "resale_pv": round(resale_pv, 2),
        "tco_total": round(total, 2),
        "eac": round(eac, 2),
    }


def critical_failure_prob(cheap, premium, repair_cost, self_insured_years):
    """
    临界年故障率 p*：当廉价款的年故障率超过 p* 时，其 EAC 反超质价比款，
    「省下的钱」被维修期望成本完全吃掉 —— 即此时风险大于收益。

    解方程：(Pc + p*·R·Yc + Cc − Rc) = (Pp + Fp + Cp − Rp)
    其中 Yc 为廉价款自担保修年数。
    返回 p*（>1 表示即使 100% 故障也不亏，即溢价无法被故障风险合理化）。
    """
    if repair_cost <= 0 or self_insured_years <= 0:
        return None
    gap = (premium["price"] + premium["repair_pv"] + premium["consumable_pv"]
           - premium["resale_pv"]
           - cheap["price"] - cheap["consumable_pv"] + cheap["resale_pv"])
    p = gap / (repair_cost * self_insured_years)
    return max(0.0, p)


# ---------- 核心模型 2：溢价对价 ----------

def premium_payback(delta_price, gains, hold_years=1.0):
    """
    质价比款的溢价对价。

    gains: [{"name": 收益项, "value": 全额价值(元), "confidence": 0~1 置信度}]
           价值需折算成「与 delta_price 同口径的现值」，例如：
           - 寿命延长 2 年 → value = 替代机价格 × (2 / 替代机总寿命)
           - 年省电 30 元 × 5 年 → value = 150
           - 保修多 2 年 → value = 同期延保市场价
           - 故障规避 → value = (p_premium_fail − p_cheap_fail) × 维修成本 × 年数

    返回：
      roi           = 风险调整后收益现值 / 溢价  （>=1 才算「溢价值」）
      breakeven     = 盈亏平衡溢价上限 = 风险调整后收益现值
      premium_ratio = 实际溢价 / 盈亏平衡溢价 （>1 表示多付了）
    """
    if delta_price <= 0:
        return {"delta_price": delta_price, "gains_pv": 0.0, "roi": None,
                "breakeven_premium": 0.0, "verdict": "无溢价（同价或更便宜），改用 EAC 直接比较"}

    if not gains:
        return {"delta_price": round(delta_price, 2), "hold_years": hold_years,
                "gains_detail": [], "gains_pv": 0.0, "roi": None,
                "breakeven_premium": 0.0, "premium_overpay": round(delta_price, 2),
                "verdict": "未提供可量化收益项，溢价无法对价（需补 premium_gains 或直接改用 EAC 比较）"}

    rows = []
    pv = 0.0
    for g in gains or []:
        v = float(g.get("value", 0) or 0)
        c = float(g.get("confidence", 1.0))
        c = min(1.0, max(0.0, c))
        pv += v * c
        rows.append({"name": g.get("name", "未命名收益"), "value": round(v, 2),
                     "confidence": c, "weighted": round(v * c, 2)})

    roi = pv / delta_price
    if roi >= 1.2:
        verdict = "溢价成立：可量化收益覆盖溢价并有盈余，属「买得值」"
    elif roi >= 1.0:
        verdict = "溢价勉强成立：收益刚好覆盖溢价，容错空间薄"
    elif roi >= 0.7:
        verdict = "溢价存疑：收益覆盖不足，差价中约 {}% 属品牌/情绪溢价".format(
            round((1 - roi) * 100))
    else:
        verdict = "溢价不成立：约 {}% 的差价买不到可量化收益，属纯品牌溢价".format(
            round((1 - roi) * 100))

    return {
        "delta_price": round(delta_price, 2),
        "hold_years": hold_years,
        "gains_detail": rows,
        "gains_pv": round(pv, 2),
        "roi": round(roi, 3),
        "breakeven_premium": round(pv, 2),
        "premium_overpay": round(max(0.0, delta_price - pv), 2),
        "verdict": verdict,
    }


# ---------- 核心模型 3：场景加权评分 ----------

def weighted_score(scores, weights=None):
    """
    场景加权评分（0~100）。
    scores: {"safety":1~5, "performance":1~5, ...}
    weights: 自定义权重（自动归一化）；缺省用 DEFAULT_WEIGHTS。
    """
    w = dict(weights or DEFAULT_WEIGHTS)
    total_w = sum(v for v in w.values() if v > 0)
    if total_w <= 0:
        raise ValueError("权重之和必须 > 0")
    acc = 0.0
    detail = {}
    for k, weight in w.items():
        if weight <= 0:
            continue
        s = float(scores.get(k, 0) or 0)
        s = min(5.0, max(0.0, s))
        contribution = (s / 5.0) * (weight / total_w) * 100.0
        acc += contribution
        detail[k] = {"score": s, "weight": round(weight / total_w, 4),
                     "points": round(contribution, 2)}
    return {"score_100": round(acc, 2), "detail": detail}


def qpr(quality_score_100, eac):
    """质价比指数 QPR = 加权质量分 / 年化总成本(千元)。可跨型号横向比较，越高越划算。"""
    if eac <= 0:
        return None
    return round(quality_score_100 / (eac / 1000.0), 2)


# ---------- 一体化裁决 ----------

SCENARIO_WEIGHTS = {
    "家用日常":      {"safety": 0.18, "performance": 0.24, "durability": 0.18, "service": 0.16, "noise": 0.10, "price": 0.14},
    "办公多机位":    {"safety": 0.12, "performance": 0.28, "durability": 0.26, "service": 0.16, "noise": 0.04, "price": 0.14},
    "移动便携":      {"safety": 0.20, "performance": 0.18, "durability": 0.16, "service": 0.12, "noise": 0.06, "price": 0.28},
    "安全关键":      {"safety": 0.42, "performance": 0.18, "durability": 0.22, "service": 0.10, "noise": 0.02, "price": 0.06},
    "极致省钱":      {"safety": 0.20, "performance": 0.15, "durability": 0.12, "service": 0.08, "noise": 0.03, "price": 0.42},
}


def _pair(cheap, other, gains, hold):
    """性价比款 → 某候选款 的两两对价。"""
    dp = other["price"] - cheap["price"]
    payback = premium_payback(dp, gains, hold)
    p_star = critical_failure_prob(cheap["tco"], other["tco"],
                                   cheap["repair_cost"], cheap["tco"]["self_insured_years"])
    delta_eac = cheap["tco"]["eac"] - other["tco"]["eac"]
    return {
        "vs": other["name"],
        "delta_price": round(dp, 2),
        # 正值 = 该款比性价比款每年更省；负值 = 每年更贵
        "delta_eac": round(delta_eac, 2),
        "eac_payback_years": (round(dp / delta_eac, 2) if delta_eac > 0 and dp > 0 else None),
        "critical_failure_prob": (None if p_star is None else round(p_star, 4)),
        "risk_over_benefit_for_cheap": (None if p_star is None
                                        else bool(cheap["annual_failure_prob"] > p_star)),
        "premium_payback": payback,
        "fair_price_ceiling": round(cheap["price"] + payback.get("gains_pv", 0.0), 2),
        "qpr_delta": (round((other["qpr"] or 0) - (cheap["qpr"] or 0), 2)
                      if other["qpr"] is not None and cheap["qpr"] is not None else None),
    }


def adjudicate(case):
    """输入整份 case JSON，输出裁决所需全部数字。"""
    hold = float(case.get("hold_years", 5))
    rate = float(case.get("discount_rate", 0.0) or 0.0)
    scenario = case.get("scenario")
    weights = case.get("weights") or SCENARIO_WEIGHTS.get(scenario or "家用日常", DEFAULT_WEIGHTS)

    opts = case.get("options") or []
    if len(opts) < 2:
        raise ValueError("至少需要 2 个候选型号才能做对价")

    computed = []
    for o in opts:
        t = tco(
            price=float(o["price"]),
            hold_years=hold,
            annual_failure_prob=float(o.get("annual_failure_prob", 0) or 0),
            repair_cost=float(o.get("repair_cost", 0) or 0),
            warranty_years=float(o.get("warranty_years", 0) or 0),
            annual_consumable=float(o.get("annual_consumable", 0) or 0),
            resale=float(o.get("resale", 0) or 0),
            discount_rate=rate,
            one_off_outlay=float(o.get("one_off_outlay", 0) or 0),
        )
        score = weighted_score(o.get("scores", {}), weights)
        computed.append({
            "name": o.get("name", "?"),
            "price": t["price"],
            "warranty_years": float(o.get("warranty_years", 0) or 0),
            "annual_failure_prob": float(o.get("annual_failure_prob", 0) or 0),
            "repair_cost": float(o.get("repair_cost", 0) or 0),
            "gain_list": o.get("premium_gains"),
            "tco": t,
            "score": score,
            "qpr": qpr(score["score_100"], t["eac"]),
            "blacklisted": bool(o.get("blacklisted", False)),
            "flags": o.get("flags", []),
        })

    valid = [r for r in computed if not r["blacklisted"]]
    if not valid:
        raise ValueError("全部候选命中一票否决，应输出「当前无可靠选项」")
    cheap = min(valid, key=lambda r: r["price"])
    eac_best = min(valid, key=lambda r: r["tco"]["eac"])

    # 主质价比候选：显式指定 > QPR 最高的非廉价款 > 价格次高者
    others = [r for r in valid if r is not cheap]
    named = case.get("premium_option")
    if named:
        primary = next((r for r in others if r["name"] == named), others[0])
    else:
        primary = max(others, key=lambda r: (r["qpr"] or 0, r["price"]))

    comparisons = []
    for r in others:
        gains = r["gain_list"] if r.get("gain_list") is not None else (case.get("premium_gains") or [])
        comparisons.append(_pair(cheap, r, gains, hold))

    prim = next(c for c in comparisons if c["vs"] == primary["name"])

    return {
        "category": case.get("category", ""),
        "hold_years": hold,
        "discount_rate": rate,
        "scenario": scenario or "自定义",
        "weights_used": weights,
        "options": computed,
        "baseline_cheap": cheap["name"],
        "baseline_eac_best": eac_best["name"],
        "premium_option": primary["name"],
        "comparisons": comparisons,
        # 为兼容与便捷，主对比的关键数字同时提升到顶层
        "delta_price": prim["delta_price"],
        "delta_eac": prim["delta_eac"],
        "premium_payback": prim["premium_payback"],
        "critical_failure_prob": prim["critical_failure_prob"],
        "risk_over_benefit_for_cheap": prim["risk_over_benefit_for_cheap"],
        "fair_price_ceiling": prim["fair_price_ceiling"],
        "ranking_by_qpr": [
            {"name": r["name"], "qpr": r["qpr"], "score": r["score"]["score_100"],
             "eac": r["tco"]["eac"]}
            for r in sorted(valid, key=lambda r: (r["qpr"] is None, -(r["qpr"] or 0)))
        ],
        "veto": [r["name"] for r in computed if r["blacklisted"]],
        "excluded_from_baseline": True,
    }


def render_md(res):
    L = []
    L.append("### 定量对价结果（脚本输出，勿手改）\n")
    L.append("| 型号 | 到手价 | 保修 | 年故障率 | 单次维修 | {}年TCO | **EAC(元/年)** | 加权质量分 | **QPR** |".format(
        int(res["hold_years"]) if res["hold_years"] == int(res["hold_years"]) else res["hold_years"]))
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in res["options"]:
        L.append("| {} | ¥{:.0f} | {:.1f}y | {:.0%} | ¥{:.0f} | ¥{:.0f} | **¥{:.0f}** | {:.1f} | **{}** |".format(
            r["name"], r["price"], r["warranty_years"], r["annual_failure_prob"],
            r["repair_cost"], r["tco"]["tco_total"], r["tco"]["eac"],
            r["score"]["score_100"], r["qpr"]))
    L.append("")
    L.append("**逐款对价（基准＝性价比款 {}）**\n".format(res["baseline_cheap"]))
    L.append("| 对比对象 | 溢价ΔP | EAC差(元/年) | 临界故障率 p* | 风险>收益 | 溢价ROI | 公允价格上限 |")
    L.append("|---|---|---|---|---|---|---|")
    for c in res["comparisons"]:
        rob = c["risk_over_benefit_for_cheap"]
        L.append("| {} | ¥{:.0f} | {:.0f} | {} | {} | {} | ¥{:.0f} |".format(
            c["vs"], c["delta_price"], c["delta_eac"],
            "n/a" if c["critical_failure_prob"] is None else "{:.1%}".format(c["critical_failure_prob"]),
            "—" if rob is None else ("是" if rob else "否"),
            c["premium_payback"].get("roi") if c["premium_payback"].get("roi") is not None else "—",
            c["fair_price_ceiling"]))
    L.append("")
    pb = res["premium_payback"]
    L.append("- **主质价比候选**：{}；溢价 ¥{:.0f}，EAC 差 ¥{:.0f}/年".format(
        res["premium_option"], res["delta_price"], res["delta_eac"]))
    L.append("- **临界年故障率 p\\***：{}（性价比款年故障率高于此值，省下的钱被维修吃光）".format(
        "n/a" if res["critical_failure_prob"] is None else "{:.1%}".format(res["critical_failure_prob"])))
    rob = res["risk_over_benefit_for_cheap"]
    if rob is not None:
        L.append("- **风险是否大于收益**：{}".format("是 —— 性价比轨失效" if rob else "否 —— 性价比轨仍成立"))
    L.append("- **溢价对价**：可量化收益现值 ¥{:.0f}，ROI {:.2f}；{}".format(
        pb.get("gains_pv", 0), pb.get("roi") or 0, pb.get("verdict", "")))
    L.append("- **公允价格上限**：¥{:.0f}（超过此价，溢价即无法被可量化收益覆盖）".format(
        res["fair_price_ceiling"]))
    if pb.get("gains_detail"):
        L.append("")
        L.append("| 收益项 | 全额价值 | 置信度 | 折算值 |")
        L.append("|---|---|---|---|")
        for g in pb["gains_detail"]:
            L.append("| {} | ¥{:.0f} | {:.0%} | ¥{:.0f} |".format(
                g["name"], g["value"], g["confidence"], g["weighted"]))
    if res["veto"]:
        L.append("")
        L.append("- ⛔ **一票否决**：{}（命中黑榜，不得进入推荐）".format("、".join(res["veto"])))
    return "\n".join(L)


# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="溢价-风险对价计算器（避雷选品团 4.0）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("tco", help="单型号 TCO / EAC")
    p1.add_argument("--price", type=float, required=True)
    p1.add_argument("--hold-years", type=float, default=5)
    p1.add_argument("--prob", type=float, default=0.0, help="年故障率 0~1")
    p1.add_argument("--repair", type=float, default=0.0)
    p1.add_argument("--warranty", type=float, default=0.0)
    p1.add_argument("--consumable", type=float, default=0.0, help="年耗材/能耗")
    p1.add_argument("--resale", type=float, default=0.0)
    p1.add_argument("--rate", type=float, default=0.0, help="折现率，如 0.03")

    p2 = sub.add_parser("critprob", help="临界故障率 p*")
    p2.add_argument("--delta-price", type=float, required=True)
    p2.add_argument("--repair", type=float, required=True)
    p2.add_argument("--years", type=float, required=True, help="自担保修年数")

    p3 = sub.add_parser("premium", help="溢价对价 ROI")
    p3.add_argument("--delta-price", type=float, required=True)
    p3.add_argument("--gains", type=str, default="[]",
                    help='JSON 数组，如 \'[{"name":"寿命","value":400,"confidence":0.7}]\'')

    p4 = sub.add_parser("score", help="加权评分")
    p4.add_argument("--input", required=True, help="case.json")

    p5 = sub.add_parser("all", help="一体化裁决（推荐入口）")
    p5.add_argument("--input", required=True, help="case.json")
    p5.add_argument("--format", choices=["md", "json", "both"], default="both")

    sub.add_parser("selftest", help="自检")

    a = ap.parse_args()

    if a.cmd == "tco":
        print(json.dumps(tco(a.price, a.hold_years, a.prob, a.repair, a.warranty,
                             a.consumable, a.resale, a.rate), ensure_ascii=False, indent=2))
    elif a.cmd == "critprob":
        p = critical_failure_prob({"price": 0, "repair_pv": 0, "consumable_pv": 0, "resale_pv": 0},
                                  {"price": a.delta_price, "repair_pv": 0,
                                   "consumable_pv": 0, "resale_pv": 0},
                                  a.repair, a.years)
        print("临界年故障率 p* = {:.2%}".format(p) if p is not None else "参数不足，无法求解")
    elif a.cmd == "premium":
        print(json.dumps(premium_payback(a.delta_price, json.loads(a.gains)),
                         ensure_ascii=False, indent=2))
    elif a.cmd == "score":
        case = json.load(open(a.input, encoding="utf-8"))
        w = case.get("weights") or SCENARIO_WEIGHTS.get(case.get("scenario", ""), DEFAULT_WEIGHTS)
        for o in case.get("options", []):
            s = weighted_score(o.get("scores", {}), w)
            print("{}: {:.2f}/100  {}".format(o.get("name"), s["score_100"], s["detail"]))
    elif a.cmd == "all":
        case = json.load(open(a.input, encoding="utf-8"))
        res = adjudicate(case)
        if a.format in ("json", "both"):
            print(json.dumps(res, ensure_ascii=False, indent=2))
        if a.format in ("md", "both"):
            print(render_md(res))
    elif a.cmd == "selftest":
        selftest()


def selftest():
    ok = True
    # 1) 保修期内不产生故障成本
    t = tco(price=1000, hold_years=2, annual_failure_prob=1.0, repair_cost=500, warranty_years=2)
    ok &= (t["repair_pv"] == 0)
    # 2) 保修期外按年计入
    t = tco(price=1000, hold_years=3, annual_failure_prob=1.0, repair_cost=500, warranty_years=0)
    ok &= (t["repair_pv"] == 1500)
    # 3) EAC 一致性
    t = tco(price=1200, hold_years=4, annual_consumable=100, resale=200)
    ok &= abs(t["tco_total"] - 1400) < 1e-6 and abs(t["eac"] - 350) < 1e-6
    # 4) 临界故障率
    p = critical_failure_prob(
        {"price": 2000, "repair_pv": 0, "consumable_pv": 0, "resale_pv": 0},
        {"price": 2800, "repair_pv": 0, "consumable_pv": 0, "resale_pv": 0},
        500, 4)
    ok &= abs(p - 0.4) < 1e-9
    # 5) 溢价 ROI
    pb = premium_payback(800, [{"name": "寿命", "value": 900, "confidence": 1.0}])
    ok &= abs(pb["roi"] - 1.125) < 1e-9
    # 6) 评分归一化满分
    s = weighted_score({k: 5 for k in DEFAULT_WEIGHTS})
    ok &= abs(s["score_100"] - 100.0) < 1e-9
    print("SELFTEST", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
