#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stocking_plan.py —— 备货计划（安全库存 / 补货点 / 建议备货量 + 现金流红线）

输入真实销量与库存数据 → 输出补货建议，并校验压货是否超过近 60 天现金流入的 50%。
公式：
  安全库存  = 日均销量 × 补货周期 × 安全系数
  补货点    = 日均销量 × 补货周期 + 安全库存
  建议备货量 = 目标天数销量 + 安全库存 − 现有库存 − 在途库存
  大促备货  = 建议备货量 × 1.3（含 10% 应急）
  红线      = 备货金额 ÷ 近 60 天现金流入 > 50% → 告警（压货压死现金流是中小企业头号死因）

用法：
  python stocking_plan.py --self-test
  python stocking_plan.py --params stock.json [--json]
退出码：0 正常；2 缺数据。
"""

import argparse
import json
import sys


def plan(d: dict) -> dict:
    req = ("avg_daily_sales", "lead_time_days", "unit_cost")
    missing = [k for k in req if d.get(k) is None]
    if missing:
        raise ValueError("缺少必填真实数据: %s（禁止用假设值代替）" % ",".join(missing))
    avg = float(d["avg_daily_sales"])
    lt = float(d["lead_time_days"])
    uc = float(d["unit_cost"])
    sf = float(d.get("safety_factor", 1.5))
    exist = float(d.get("existing_stock", 0))
    transit = float(d.get("in_transit_stock", 0))
    target_days = float(d.get("target_days", 30))
    cash = float(d.get("cash_inflow_60d", 0))
    promo = bool(d.get("is_promo", False))

    safety = avg * lt * sf
    reorder = avg * lt + safety
    planned_qty = max(0.0, avg * target_days + safety - exist - transit)
    stock_value = planned_qty * uc
    if promo:
        promo_qty = planned_qty * 1.3 * 1.1
        promo_value = promo_qty * uc
    else:
        promo_qty = None
        promo_value = None
    redline = None
    if cash > 0:
        ratio = stock_value / cash
        redline = {"stock_value": round(stock_value, 2), "cash_inflow_60d": cash,
                   "ratio": round(ratio, 4), "breach": ratio > 0.5}
    return {
        "avg_daily_sales": avg, "lead_time_days": lt, "safety_factor": sf,
        "safety_stock": round(safety, 1), "reorder_point": round(reorder, 1),
        "planned_qty": round(planned_qty, 1), "stock_value": round(stock_value, 2),
        "promo_planned_qty": (round(promo_qty, 1) if promo_qty else None),
        "promo_stock_value": (round(promo_value, 2) if promo_value else None),
        "redline": redline,
    }


def render(r):
    o = ["【备货计划】日均销量 %.1f × 补货周期 %.0f 天（安全系数 %.2f）" % (
        r["avg_daily_sales"], r["lead_time_days"], r["safety_factor"])]
    o.append("  安全库存 = %.1f 件 | 补货点 = %.1f 件" % (r["safety_stock"], r["reorder_point"]))
    o.append("  建议备货量 = %.1f 件（金额 %.2f 元）" % (r["planned_qty"], r["stock_value"]))
    if r["promo_planned_qty"]:
        o.append("  大促备货量 = %.1f 件（×1.3 含 10%% 应急，金额 %.2f 元）" % (
            r["promo_planned_qty"], r["promo_stock_value"]))
    if r["redline"]:
        rl = r["redline"]
        if rl["breach"]:
            o.append("  ⚠ 压货红线告警：备货金额 %.2f ÷ 近60天现金流入 %.2f = %.0f%% > 50%%，存在压死现金流风险" % (
                rl["stock_value"], rl["cash_inflow_60d"], rl["ratio"] * 100))
        else:
            o.append("  现金流红线：备货占比 %.0f%%（安全，≤50%%）" % (rl["ratio"] * 100))
    return "\n".join(o)


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    d = {"avg_daily_sales": 100, "lead_time_days": 7, "unit_cost": 20, "safety_factor": 1.5,
         "existing_stock": 200, "in_transit_stock": 100, "target_days": 30, "cash_inflow_60d": 200000}
    r = plan(d)
    chk("安全库存=100*7*1.5=1050", abs(r["safety_stock"] - 1050) < 1e-6)
    chk("补货点=700+1050=1750", abs(r["reorder_point"] - 1750) < 1e-6)
    chk("建议量=3000+1050-300=3750", abs(r["planned_qty"] - 3750) < 1e-6)
    chk("金额=3750*20=75000", abs(r["stock_value"] - 75000) < 1e-6)
    chk("红线占比=37.5% 未超", (not r["redline"]["breach"]) and abs(r["redline"]["ratio"] - 0.375) < 1e-6)

    d2 = dict(d)
    d2["cash_inflow_60d"] = 100000
    r2 = plan(d2)
    chk("红线超标告警", r2["redline"]["breach"] and abs(r2["redline"]["ratio"] - 0.75) < 1e-6)

    d3 = dict(d)
    d3["is_promo"] = True
    r3 = plan(d3)
    chk("大促量=3750*1.43=5362.5", abs(r3["promo_planned_qty"] - 5362.5) < 1e-6)

    try:
        plan({"avg_daily_sales": 10})
        print("  [FAIL] 缺数据应报错")
        ok = False
    except ValueError:
        print("  [PASS] 缺数据报错")

    print("stocking_plan self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="备货计划")
    ap.add_argument("--params", help="备货参数 JSON")
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
        res = [plan(it) for it in items]
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(res if len(res) > 1 else res[0], ensure_ascii=False, indent=2) if a.json
          else "\n\n".join(render(r) for r in res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
