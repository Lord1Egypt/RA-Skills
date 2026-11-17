#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""profit_roi.py —— 定价 / 真实利润 / 保本售价 / 保本ROI / 最高可承受出价 / 目标ROI反推

纯标准库、零依赖。所有公式写死在本文件，禁止临场推导。

恒等式（唯一口径，任何报告都必须引用）：
  vc       = 商品成本 + 履约物流 + 其他变动成本 + 退货率 × 单均退货损失
  k        = 平台佣金率 + 支付通道费率（+ 其他按售价比例计的费用率）
  CM       = P × (1 - k) - vc - 单件固定分摊            # 单件贡献毛利（不含广告）
  g        = CM / P                                      # 毛利率（不含广告）
  g_eff    = g - 达人/坑位分摊率 - 目标净利率 m           # 可用于投广告的比例
  保本ROAS = 1 / g_eff
  ROAS     = CVR × P / CPC                               # 恒等式，三变量知二求一
  最高CPC  = P × g_eff × CVR
  最高CPM  = 1000 × 最高CPC × CTR
  保本售价 = (vc + 单件固定分摊) / (1 - k - a - m)        # a=广告占售价比, m=目标净利率

用法：
  python profit_roi.py --self-test
  python profit_roi.py --params params.json [--json]
  python profit_roi.py --price 129 --cost-goods 38 --commission-rate 0.05 --cvr 0.035
退出码：0 正常；2 参数缺失（数据不足，禁止编造，见 R1 真实数据铁律）。
"""

import argparse
import json
import sys

# 佣金率合理区间（与 settlement_audit.py 同一口径）
COMMISSION_MIN, COMMISSION_MAX = 0.005, 0.30

FIELDS = {
    "price": ("售价(到手价/实收单价)", 0.0),
    "cost_goods": ("商品成本(含头程)", 0.0),
    "cost_fulfill": ("履约物流成本", 0.0),
    "other_var_cost": ("其他变动成本(包装/售后等)", 0.0),
    "commission_rate": ("平台佣金率", 0.0),
    "pay_rate": ("支付通道费率", 0.0),
    "return_rate": ("退货率", 0.0),
    "return_cost": ("单均退货损失(往返运费+不可售损失)", 0.0),
    "fixed_unit": ("单件固定成本分摊", 0.0),
    "ad_unit": ("单件广告费(实测)", 0.0),
    "koll_unit": ("单件达人佣金+坑位费分摊", 0.0),
    "subsidy_unit": ("单件商家承担补贴", 0.0),
    "cvr": ("转化率(支付买家数/访客数)", None),
    "ctr": ("点击率(点击/曝光)", None),
    "cpc": ("平均点击花费", None),
    "target_margin": ("目标净利率", 0.0),
    "ad_rate": ("计划广告占售价比", 0.0),
    "fixed_total": ("总固定成本(算保本销量用)", None),
    "target_roas": ("目标ROAS(反推用，知二求一)", None),
}


def build(params: dict) -> dict:
    missing = [k for k in ("price", "cost_goods") if params.get(k) is None]
    if missing:
        raise ValueError("缺少必填真实数据: %s（禁止用假设值代替）" % ",".join(missing))

    p = {k: (params.get(k) if params.get(k) is not None else d) for k, (_, d) in FIELDS.items()}
    P = float(p["price"])
    if P <= 0:
        raise ValueError("售价必须 > 0")

    vc = p["cost_goods"] + p["cost_fulfill"] + p["other_var_cost"] + p["return_rate"] * p["return_cost"]
    k = p["commission_rate"] + p["pay_rate"]
    if not (0 <= k < 1):
        raise ValueError("费率合计 k=%.4f 不合理" % k)

    fixed_unit = p["fixed_unit"]
    cm = P * (1 - k) - vc - fixed_unit          # 不含广告的贡献毛利
    g = cm / P                                   # 不含广告毛利率
    koll_rate = p["koll_unit"] / P
    m = p["target_margin"]
    g_eff = g - koll_rate - m                    # 可投广告比例

    breakeven_price = (vc + fixed_unit) / (1 - k) if (1 - k) > 0 else None
    breakeven_price_full = None
    denom = 1 - k - p["ad_rate"] - m - koll_rate - (p["subsidy_unit"] / P)
    if denom > 0:
        breakeven_price_full = (vc + fixed_unit) / denom

    roas_be = (1 / g_eff) if g_eff > 0 else None          # 保本ROAS（含目标净利）
    roas_be_basic = (1 / g) if g > 0 else None            # 保本ROAS（仅覆盖成本，不含目标净利）

    cvr, ctr, cpc = p["cvr"], p["ctr"], p["cpc"]
    max_cpc = P * g_eff * cvr if (cvr and g_eff > 0) else None
    max_cpm = 1000 * max_cpc * ctr if (max_cpc is not None and ctr) else None
    ad_unit_cap = P * g_eff                                # 单件广告费上限

    roas_actual = None
    if cvr and cpc and cpc > 0:
        roas_actual = cvr * P / cpc
    cpc_at_target = None
    if roas_be and cvr and roas_be > 0:
        cpc_at_target = cvr * P / roas_be
    cvr_need = None
    if roas_be and cpc and cpc > 0:
        cvr_need = roas_be * cpc / P

    # 目标 ROAS 反推（知二求一）：最高可承受 CPC / 所需 CVR / 所需客单价
    troas = p["target_roas"]
    max_cpc_target = None
    cvr_need_target = None
    aov_need_target = None
    if troas and troas > 0:
        if cvr:
            max_cpc_target = P * cvr / troas
        if cpc and cpc > 0:
            cvr_need_target = troas * cpc / P
        if cpc and cpc > 0 and cvr:
            aov_need_target = troas * cpc / cvr

    net_now = cm - p["ad_unit"] - p["koll_unit"] - p["subsidy_unit"]
    net_margin_now = net_now / P

    breakeven_units = None
    if p["fixed_total"] and cm > 0:
        breakeven_units = p["fixed_total"] / cm

    return {
        "input": p,
        "cost": {
            "变动成本小计 vc": round(vc, 4),
            "费率合计 k": round(k, 6),
            "单件贡献毛利 CM(不含广告)": round(cm, 4),
            "毛利率 g(不含广告)": round(g, 6),
            "可投广告比例 g_eff": round(g_eff, 6),
        },
        "profit": {
            "单件净利(含实测广告)": round(net_now, 4),
            "净利率": round(net_margin_now, 6),
            "单件广告费上限": round(ad_unit_cap, 4) if ad_unit_cap else None,
            "保本销量(件)": round(breakeven_units, 1) if breakeven_units else None,
        },
        "price": {
            "保本售价(仅覆盖成本)": round(breakeven_price, 2) if breakeven_price else None,
            "定价下限(含目标净利/广告/补贴)": round(breakeven_price_full, 2) if breakeven_price_full else None,
        },
        "ads": {
            "保本ROAS(含目标净利)": round(roas_be, 4) if roas_be else None,
            "保本ROAS(仅覆盖成本)": round(roas_be_basic, 4) if roas_be_basic else None,
            "实际ROAS": round(roas_actual, 4) if roas_actual else None,
            "最高可承受CPC": round(max_cpc, 4) if max_cpc else None,
            "最高可承受CPM": round(max_cpm, 4) if max_cpm else None,
            "保本ROAS对应的CPC": round(cpc_at_target, 4) if cpc_at_target else None,
            "按当前CPC需要的转化率": round(cvr_need, 6) if cvr_need else None,
            "目标ROAS反推_最高可承受CPC": round(max_cpc_target, 4) if max_cpc_target else None,
            "目标ROAS反推_所需转化率": round(cvr_need_target, 6) if cvr_need_target else None,
            "目标ROAS反推_所需客单价": round(aov_need_target, 4) if aov_need_target else None,
        },
        "flags": _flags(p, g, g_eff),
    }


def _flags(p, g, g_eff):
    f = []
    cr = p["commission_rate"]
    if cr and not (COMMISSION_MIN <= cr <= COMMISSION_MAX):
        f.append("佣金率 %.2f%% 超出合理区间 %.1f%%~%.0f%%，核对类目与结算单" % (cr * 100, COMMISSION_MIN * 100, COMMISSION_MAX * 100))
    if g <= 0:
        f.append("毛利率 ≤ 0：售价无法覆盖变动成本，任何投放都会亏，先改成本结构或提价")
    elif g_eff <= 0:
        f.append("可投广告比例 g_eff ≤ 0：目标净利率+达人分摊已吃光毛利，投放必亏")
    if p["ad_unit"] and p["ad_unit"] > p["price"] * max(g, 0):
        f.append("实测单件广告费 %.2f 超过单件贡献毛利 %.2f，当前投放为负贡献" % (p["ad_unit"], p["price"] * g))
    return f


def render(res: dict) -> str:
    out = []
    i, c, pf, pr, ad = res["input"], res["cost"], res["profit"], res["price"], res["ads"]
    out.append("【定价与真实利润】售价 %.2f 元" % i["price"])
    out.append("  变动成本 vc=%.2f | 费率合计 k=%.2f%% | 单件固定分摊=%.2f" % (c["变动成本小计 vc"], c["费率合计 k"] * 100, i["fixed_unit"]))
    out.append("  单件贡献毛利 CM=%.2f | 毛利率 g=%.2f%% | 可投广告比例 g_eff=%.2f%%" % (
        c["单件贡献毛利 CM(不含广告)"], c["毛利率 g(不含广告)"] * 100, c["可投广告比例 g_eff"] * 100))
    out.append("  单件净利=%.2f | 净利率=%.2f%%" % (pf["单件净利(含实测广告)"], pf["净利率"] * 100))
    out.append("【保本售价】仅覆盖成本 %.2f 元 | 含目标净利/广告/补贴 %s 元" % (
        pr["保本售价(仅覆盖成本)"] or -1,
        ("%.2f" % pr["定价下限(含目标净利/广告/补贴)"]) if pr["定价下限(含目标净利/广告/补贴)"] else "—"))
    out.append("【投放测算】保本ROAS(含目标净利)=%s | 仅覆盖成本=%s | 实际ROAS=%s" % (
        ad["保本ROAS(含目标净利)"], ad["保本ROAS(仅覆盖成本)"], ad["实际ROAS"]))
    out.append("  最高可承受CPC=%s 元 | 最高可承受CPM=%s 元 | 单件广告费上限=%.2f 元" % (
        ad["最高可承受CPC"], ad["最高可承受CPM"], pf["单件广告费上限"] or 0))
    if ad.get("目标ROAS反推_最高可承受CPC") is not None:
        out.append("  【目标ROAS反推】最高可承受CPC=%.2f 元 | 所需转化率=%.2f%% | 所需客单价=%.2f 元" % (
            ad["目标ROAS反推_最高可承受CPC"], (ad["目标ROAS反推_所需转化率"] or 0) * 100,
            ad["目标ROAS反推_所需客单价"] or 0))
    if res["flags"]:
        out.append("【风险提示】")
        out += ["  ! " + s for s in res["flags"]]
    return "\n".join(out)


def self_test() -> int:
    ok = True

    def chk(name, got, want, tol=1e-6):
        nonlocal ok
        good = got is not None and abs(got - want) < tol
        ok = ok and good
        print("  [%s] %-28s got=%s want=%s" % ("PASS" if good else "FAIL", name, got, want))

    # 用例：P=100, vc=40(+退货0), k=0.06, 无固定成本, 无达人, 目标净利0
    r = build({"price": 100, "cost_goods": 40, "commission_rate": 0.05, "pay_rate": 0.01,
               "cvr": 0.03, "ctr": 0.02, "cpc": 1.0})
    chk("CM = 100*0.94-40", r["cost"]["单件贡献毛利 CM(不含广告)"], 54.0)
    chk("毛利率 g", r["cost"]["毛利率 g(不含广告)"], 0.54)
    chk("保本ROAS = 1/g", r["ads"]["保本ROAS(仅覆盖成本)"], 1 / 0.54, 1e-4)
    chk("最高CPC = P*g*CVR", r["ads"]["最高可承受CPC"], 100 * 0.54 * 0.03)
    chk("最高CPM = 1000*CPC*CTR", r["ads"]["最高可承受CPM"], 1000 * 1.62 * 0.02)
    chk("实际ROAS = CVR*P/CPC", r["ads"]["实际ROAS"], 0.03 * 100 / 1.0)
    chk("保本售价 = vc/(1-k)", r["price"]["保本售价(仅覆盖成本)"], 40 / 0.94, 0.01)

    # 用例：目标 ROAS 反推（P=100, cvr=0.03, cpc=1.0, target_roas=3 → 最高CPC=1.0, 所需CVR=3%）
    r3 = build({"price": 100, "cost_goods": 40, "commission_rate": 0.05, "cvr": 0.03, "cpc": 1.0, "target_roas": 3})
    chk("目标ROAS反推_最高CPC = P*CVR/tROAS", r3["ads"]["目标ROAS反推_最高可承受CPC"], 100 * 0.03 / 3)
    chk("目标ROAS反推_所需CVR = tROAS*CPC/P", r3["ads"]["目标ROAS反推_所需转化率"], 3 * 1.0 / 100)

    # 用例：含退货损失与固定分摊
    r2 = build({"price": 100, "cost_goods": 30, "cost_fulfill": 6, "return_rate": 0.1,
                "return_cost": 20, "commission_rate": 0.05, "fixed_unit": 4, "target_margin": 0.1})
    vc2 = 30 + 6 + 0 + 0.1 * 20
    chk("vc 含退货损失", r2["cost"]["变动成本小计 vc"], vc2)
    chk("g_eff 扣目标净利", r2["cost"]["可投广告比例 g_eff"], (100 * 0.95 - vc2 - 4) / 100 - 0.1)

    # 用例：异常退出（缺售价）
    try:
        build({"cost_goods": 10})
        print("  [FAIL] 缺少售价应报错")
        ok = False
    except ValueError:
        print("  [PASS] 缺少真实数据报错")

    print("profit_roi self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="定价/利润/保本ROI/出价测算")
    ap.add_argument("--params", help="参数 JSON 文件（dict 或 list）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--self-test", action="store_true")
    for k in FIELDS:
        ap.add_argument("--" + k.replace("_", "-"), type=float, default=None)
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    if a.params:
        with open(a.params, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {k: getattr(a, k) for k in FIELDS}
        if data.get("price") is None and data.get("cost_goods") is None:
            ap.error("需要 --params 或至少 --price/--cost-goods")

    items = data if isinstance(data, list) else [data]
    results = []
    for it in items:
        try:
            r = build(it)
        except ValueError as e:
            print("ERROR: %s" % e, file=sys.stderr)
            return 2
        results.append(r)
        if not a.json:
            print(render(r))
            print("-" * 60)
    if a.json:
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
