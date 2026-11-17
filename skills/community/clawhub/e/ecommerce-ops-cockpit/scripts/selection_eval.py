#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selection_eval.py —— 选品评估与竞品分析（E1 强制脚本）

把「这款产品值不值得做」从专家拍脑袋变成可复算的加权评分：
  输入真实/评估数据 → 六维有效分 → 加权综合分 → 做 / 不做 / 有条件做
  可选输入竞品列表 → 输出价格带 / 销量集中度 / 卖点短板对照表

维度（权重合计=1，全部「越高越好」）：
  market_size     0.15  市场容量与天花板
  competition     0.15  竞争友好度（=100 - 竞争强度）
  margin          0.25  毛利率空间
  aftersale       0.15  售后友好度（=100 - 退货风险）
  compliance      0.15  合规友好度（=100 - 合规风险）
  content_fit     0.15  内容带货适配度

决策阈值：综合分 ≥75 可做；60–74 有条件做；<60 不建议做。

用法：
  python selection_eval.py --self-test
  python selection_eval.py --params sku.json [--json]
退出码：0 正常；2 参数缺失（禁止匿名/编造评估）。
"""

import argparse
import json
import sys

WEIGHTS = {
    "market_size": 0.15,
    "competition": 0.15,
    "margin": 0.25,
    "aftersale": 0.15,
    "compliance": 0.15,
    "content_fit": 0.15,
}


def _clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


def effective(p: dict) -> dict:
    """把原始等级/比例转成「越高越好」0-100 有效分"""
    market = _clamp(float(p.get("market_level", 0)))
    comp_intensity = _clamp(float(p.get("competition_level", 0)))
    gm = float(p.get("gross_margin", 0))
    if gm <= 1:
        gm *= 100  # 允许比例或百分制
    gm = _clamp(gm)
    rr = float(p.get("return_rate", 0))
    if rr <= 1:
        rr *= 100
    aftersale = _clamp(100 - rr * 3.0)  # 退货率每 1% 扣 3 分，33%+ 退货≈0 分
    comp_risk = _clamp(float(p.get("compliance_level", 0)))
    compliance = _clamp(100 - comp_risk)
    content = _clamp(float(p.get("content_level", 0)))
    return {
        "market_size": market,
        "competition": 100 - comp_intensity,
        "margin": gm,
        "aftersale": aftersale,
        "compliance": compliance,
        "content_fit": content,
    }


def decide(score):
    if score >= 75:
        return "可做"
    if score >= 60:
        return "有条件做"
    return "不建议做"


def competitor_table(comps):
    if not comps:
        return None
    prices = [float(c.get("price", 0)) for c in comps if c.get("price")]
    sales = [float(c.get("monthly_sales", 0)) for c in comps if c.get("monthly_sales")]
    rows = []
    total_sales = sum(sales) or 1
    for c in comps:
        s = float(c.get("monthly_sales", 0))
        rows.append({
            "name": c.get("name", "?"),
            "price": float(c.get("price", 0)),
            "monthly_sales": s,
            "share": round(s / total_sales, 4),
            "edge": c.get("edge", ""),
            "weak": c.get("weak", ""),
        })
    sp = sorted(prices)
    n = len(sp)
    median = (sp[n // 2] + sp[(n - 1) // 2]) / 2.0 if n else 0
    return {
        "count": len(comps),
        "price_min": min(prices) if prices else 0,
        "price_max": max(prices) if prices else 0,
        "price_median": median,
        "top3_share": round(sum(sorted(sales, reverse=True)[:3]) / total_sales, 4) if sales else 0,
        "rows": rows,
    }


def evaluate(data: dict) -> dict:
    if not data.get("name"):
        raise ValueError("缺少 SKU 名称（name），禁止匿名评估")
    eff = effective(data)
    score = sum(eff[k] * WEIGHTS[k] for k in WEIGHTS)
    score = round(score, 1)
    weak = min(eff, key=lambda k: eff[k])
    ct = competitor_table(data.get("competitors") or [])
    verdict = decide(score)
    conditions = []
    if verdict == "有条件做":
        if eff["competition"] < 50:
            conditions.append("竞争偏激烈，需做出差异化卖点再入场")
        if eff["margin"] < 40:
            conditions.append("毛利偏薄，定价/成本需优化到毛利率≥40%再上")
        if eff["aftersale"] < 50:
            conditions.append("售后/退货风险偏高，详情页须补实物视频与尺码表")
        if eff["compliance"] < 50:
            conditions.append("合规风险偏高，上架前须备齐资质/检测报告")
    return {
        "name": data["name"],
        "effective_scores": {k: round(v, 1) for k, v in eff.items()},
        "weighted_score": score,
        "verdict": verdict,
        "weakest_dimension": weak,
        "conditions": conditions,
        "competitors": ct,
    }


def render(r):
    o = ["【选品评估】%s → 综合分 %.1f / 100 → %s" % (r["name"], r["weighted_score"], r["verdict"])]
    o.append("  六维有效分（越高越好）：")
    for k, v in r["effective_scores"].items():
        o.append("    %-12s %.1f" % (k, v))
    o.append("  最弱维度：%s" % r["weakest_dimension"])
    if r["conditions"]:
        o.append("  「有条件做」的限制条件：")
        o += ["    - " + c for c in r["conditions"]]
    c = r["competitors"]
    if c and c.get("rows"):
        o.append("  竞品对照：%d 个 | 价格带 %.0f~%.0f（中位 %.0f）| TOP3 销量集中度 %.0f%%" % (
            c["count"], c["price_min"], c["price_max"], c["price_median"], c["top3_share"] * 100))
        for row in c["rows"]:
            o.append("    · %s：价 %.0f / 月销 %.0f（占 %.0f%%）| 卖点：%s | 短板：%s" % (
                row["name"], row["price"], row["monthly_sales"], row["share"] * 100, row["edge"], row["weak"]))
    return "\n".join(o)


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # 全维度满分 → 综合 100 → 可做
    d = {"name": "满分SKU", "market_level": 100, "competition_level": 0, "gross_margin": 1.0,
         "return_rate": 0, "compliance_level": 0, "content_level": 100}
    r = evaluate(d)
    chk("综合分=100", abs(r["weighted_score"] - 100) < 1e-6)
    chk("决策=可做", r["verdict"] == "可做")

    # 低分 → 不建议做
    d2 = {"name": "低分SKU", "market_level": 40, "competition_level": 60, "gross_margin": 0.2,
          "return_rate": 0.3, "compliance_level": 60, "content_level": 40}
    r2 = evaluate(d2)
    chk("低分决策=不建议做", r2["verdict"] == "不建议做")

    # 竞品对照
    d3 = {"name": "带竞品", "market_level": 100, "competition_level": 0, "gross_margin": 1.0,
          "return_rate": 0, "compliance_level": 0, "content_level": 100,
          "competitors": [{"name": "A", "price": 99, "monthly_sales": 3000, "edge": "低价", "weak": "退货高"},
                          {"name": "B", "price": 129, "monthly_sales": 1000, "edge": "品质", "weak": "贵"}]}
    r3 = evaluate(d3)
    chk("竞品 TOP3 集中度=100%", abs(r3["competitors"]["top3_share"] - 1.0) < 1e-6)
    chk("价格中位=(99+129)/2=114", abs(r3["competitors"]["price_median"] - 114) < 1e-6)

    # 异常退出
    try:
        evaluate({"market_level": 80})
        print("  [FAIL] 缺少 name 应报错")
        ok = False
    except ValueError:
        print("  [PASS] 缺少 name 报错")

    print("selection_eval self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="选品评估与竞品分析")
    ap.add_argument("--params", help="参数 JSON（含 name 与六维等级）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.params:
        ap.error("需要 --params 或 --self-test")
    with open(a.params, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else [data]
    try:
        res = [evaluate(it) for it in items]
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(res if len(res) > 1 else res[0], ensure_ascii=False, indent=2) if a.json
          else "\n\n".join(render(r) for r in res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
