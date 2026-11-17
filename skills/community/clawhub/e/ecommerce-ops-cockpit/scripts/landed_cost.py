# -*- coding: utf-8 -*-
"""跨境到岸成本核算：到岸成本 / 真实净利 / 保本售价 / 汇率敏感性。

覆盖国内电商没有、但跨境电商必须算的成本项：
  头程物流、关税、目的国 VAT/GST、FBA 或海外仓费用、跨境收款费率、汇率与波动缓冲、
  跨境退货（多数无法二次销售）、出口退税。

口径遵守 Skill 铁律：
  R3  金额一律由脚本计算，禁止心算
  R15 输入数据为 S1/S2；推算结果标注
  R24 给结论时同时给归因/敏感性，不只给一个数

输入 JSON（金额：外币字段用卖出币种，CNY 字段用人民币）：
{
  "platform": "amazon_us", "sell_currency": "USD",
  "fx_rate": 7.15,              // 1 外币 = ? 人民币
  "sell_price": 29.99,          // 售价（外币）
  "unit_cost_cny": 45.0,        // 货品成本（人民币/件）
  "first_leg_cny": 8.0,         // 头程物流（人民币/件）
  "duty_rate": 0.078,           // 关税率（按申报货值）
  "declare_ratio": 0.6,         // 申报比例（按售价的几成申报）
  "vat_rate": 0.0,              // 目的国 VAT/GST（美国 0；德国 0.19；英国 0.20）
  "vat_on_duty": true,          // VAT 计税基础是否含关税（欧盟通常含）
  "fba_fee": 5.5,               // FBA 配送费/件（外币）；自发货填 0
  "overseas_ship": 0.0,         // 自发货运费/件（外币）
  "storage_cny": 1.2,           // 仓储费（人民币/件）
  "commission_rate": 0.15,      // 平台佣金率
  "payment_fee_rate": 0.015,    // 跨境收款/结汇费率
  "ad_rate": 0.12,              // 广告费占售价比
  "return_rate": 0.06,          // 退货率
  "return_loss_cny": 18.0,      // 单件退货净损失（人民币，含无法二次销售）
  "export_rebate_rate": 0.13,   // 出口退税率（0 表示不适用）
  "fx_buffer": 0.02,            // 汇率波动缓冲（默认 2%）
  "target_margin": 0.18
}

用法：
  python landed_cost.py --data cb.json
  python landed_cost.py --data cb.json --json
  python landed_cost.py --demo
  python landed_cost.py --self-test
退出码：0 正常 / 2 输入错误
"""
import argparse
import json
import os
import sys


def _f(d, k, default=0.0):
    v = d.get(k)
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def calc(d):
    fx = _f(d, "fx_rate", 0) or None
    if not fx:
        raise ValueError("缺少 fx_rate（汇率）")
    p = d.get("sell_price")
    if p is None:
        raise ValueError("缺少 sell_price（售价）")
    p = float(p)

    # ── 收入侧（外币 → 人民币）──
    gross_cny = p * fx
    commission = gross_cny * _f(d, "commission_rate")
    payment_fee = gross_cny * _f(d, "payment_fee_rate")
    ad = gross_cny * _f(d, "ad_rate")

    # ── 成本侧 ──
    goods = _f(d, "unit_cost_cny")
    first_leg = _f(d, "first_leg_cny")
    storage = _f(d, "storage_cny")

    # 关税：按申报货值（售价 × 申报比例 × 汇率）
    declare_value = gross_cny * _f(d, "declare_ratio", 1.0)
    duty = declare_value * _f(d, "duty_rate")

    # VAT/GST：欧盟等按（申报货值 + 关税）计；美国为 0
    vat_base = declare_value + (duty if d.get("vat_on_duty", True) else 0.0)
    vat = vat_base * _f(d, "vat_rate")

    # 履约：FBA 或自发货（外币 → 人民币）
    fba = _f(d, "fba_fee") * fx
    ship = _f(d, "overseas_ship") * fx

    # 出口退税（按货品成本计，退的是国内采购环节增值税）
    rebate = goods * _f(d, "export_rebate_rate")

    # 退货净损失（按退货率摊到每件）
    ret_rate = _f(d, "return_rate")
    ret_loss = _f(d, "return_loss_cny") * ret_rate

    landed = goods + first_leg + duty + vat + fba + ship + storage - rebate
    variable = commission + payment_fee + ad
    # 汇率波动缓冲：按售价的一定比例计提，防汇兑吃掉利润
    fx_buf = gross_cny * _f(d, "fx_buffer", 0.02)

    total_cost = landed + variable + ret_loss + fx_buf
    net = gross_cny - total_cost
    margin = (net / gross_cny) if gross_cny else 0.0

    # ── 保本售价（外币）：令净利 = 0 ──
    # 售价相关的比率项：佣金 + 收款 + 广告 + 汇率缓冲 + 关税(按申报比例) + VAT + 退货损失
    # 其中退货损失/头程/货品/FBA 为绝对金额，与售价无关（FBA 按件固定）
    rate_part = (_f(d, "commission_rate") + _f(d, "payment_fee_rate")
                 + _f(d, "ad_rate") + _f(d, "fx_buffer", 0.02))
    dr = _f(d, "declare_ratio", 1.0)
    vr = _f(d, "vat_rate")
    duty_part = dr * _f(d, "duty_rate")
    # VAT 计税基础：欧盟等地「（申报货值 + 关税）」；有的地区仅按申报货值
    if d.get("vat_on_duty", True):
        vat_part = dr * vr * (1 + _f(d, "duty_rate"))
    else:
        vat_part = dr * vr
    fixed_cny = (goods + first_leg + storage + fba + ship
                 + ret_loss - rebate)
    denom = 1.0 - (rate_part + duty_part + vat_part)
    breakeven_cny = (fixed_cny / denom) if denom > 0 else None
    breakeven_fx = (breakeven_cny / fx) if breakeven_cny else None

    # ── 汇率敏感性：±3%、±5% ──
    sens = {}
    for delta in (-0.05, -0.03, 0.03, 0.05):
        fx2 = fx * (1 + delta)
        g2 = p * fx2
        # 与汇率同比例变动的：售价收入；关税/VAT 按申报货值（随汇率变）；FBA/运费是外币固定（随汇率变）
        duty2 = (g2 * dr) * _f(d, "duty_rate")
        vat2 = (g2 * dr + (duty2 if d.get("vat_on_duty", True) else 0)) * vr
        fba2 = _f(d, "fba_fee") * fx2
        ship2 = _f(d, "overseas_ship") * fx2
        cost2 = (goods + first_leg + duty2 + vat2 + fba2 + ship2 + storage - rebate
                 + g2 * (_f(d, "commission_rate") + _f(d, "payment_fee_rate")
                         + _f(d, "ad_rate") + _f(d, "fx_buffer", 0.02)) + ret_loss)
        net2 = g2 - cost2
        sens["%+.0f%%" % (delta * 100)] = {
            "fx": round(fx2, 4), "net_cny": round(net2, 2),
            "margin": round((net2 / g2) if g2 else 0, 4),
            "delta_cny": round(net2 - net, 2)}

    return {
        "platform": d.get("platform", "?"), "sell_currency": d.get("sell_currency", "?"),
        "fx_rate": fx, "sell_price": p, "gross_cny": gross_cny,
        "cost": {
            "货品成本": goods, "头程物流": first_leg, "关税": duty,
            "VAT/GST": vat, "FBA配送": fba, "自发货运费": ship,
            "仓储": storage, "出口退税": -rebate,
            "平台佣金": commission, "跨境收款费": payment_fee, "广告费": ad,
            "退货净损失": ret_loss, "汇率波动缓冲": fx_buf,
        },
        "landed_cost_cny": landed, "total_cost_cny": total_cost,
        "net_profit_cny": net, "net_margin": margin,
        "breakeven_price_cny": breakeven_cny, "breakeven_price_fx": breakeven_fx,
        "fx_sensitivity": sens,
    }


def render(r):
    o = []
    o.append("【跨境到岸成本核算】%s ｜ 售价 %.2f %s ｜ 汇率 %.4f"
             % (r["platform"], r["sell_price"], r["sell_currency"], r["fx_rate"]))
    o.append("收入 %.2f 元 ｜ 到岸成本 %.2f 元 ｜ 总费用 %.2f 元"
             % (r["gross_cny"], r["landed_cost_cny"],
                r["total_cost_cny"] - r["landed_cost_cny"]))
    o.append("")
    o.append("【成本明细】(人民币/件)")
    for k, v in r["cost"].items():
        if abs(v) < 1e-9:
            continue
        o.append("  %-12s %10.2f" % (k, v))
    o.append("")
    o.append("【结果】净利 %.2f 元/件 ｜ 净利率 %.2f%%" % (r["net_profit_cny"], r["net_margin"] * 100))
    if r["breakeven_price_fx"]:
        o.append("【保本售价】%.2f %s（约 %.2f 元）"
                 % (r["breakeven_price_fx"], r["sell_currency"], r["breakeven_price_cny"]))
    o.append("")
    o.append("【汇率敏感性】")
    for k, v in r["fx_sensitivity"].items():
        o.append("  汇率%s → %.4f ｜ 净利 %.2f 元（%+.2f）｜ 净利率 %.2f%%"
                 % (k, v["fx"], v["net_cny"], v["delta_cny"], v["margin"] * 100))
    o.append("")
    o.append("注：成本项为输入数据（S1/S2）；保本售价、敏感性为脚本推算值。")
    return "\n".join(o)


def make_spec(r, title=None, subtitle=None):
    """产出可直接喂给 report_pdf.build 的 spec（数值全部来自计算结果）。"""
    cur = r["sell_currency"]
    cost_rows = [[k, "%.2f" % v, "%.1f%%" % (v / r["gross_cny"] * 100) if r["gross_cny"] else "—"]
                 for k, v in r["cost"].items() if abs(v) > 1e-9]
    blocks = [
        {"type": "h1", "text": "一、跨境利润结论"},
        {"type": "callout", "tone": "ok" if r["net_profit_cny"] > 0 else "warn",
         "text": "%s：售价 %.2f %s（汇率 %.4f）→ 净利 %.2f 元/件，净利率 %.2f%%。保本售价 %.2f %s。"
                 % (r["platform"], r["sell_price"], cur, r["fx_rate"],
                    r["net_profit_cny"], r["net_margin"] * 100,
                    r["breakeven_price_fx"] or 0, cur)},
        {"type": "kv", "per_row": 4, "items": [
            ["售价", "%.2f %s" % (r["sell_price"], cur)],
            ["收入", "%.2f 元" % r["gross_cny"]],
            ["净利", "%.2f 元" % r["net_profit_cny"]],
            ["净利率", "%.2f%%" % (r["net_margin"] * 100)]]},
        {"type": "h1", "text": "二、成本结构"},
        {"type": "pie", "title": "到岸成本构成（元/件）",
         "labels": [k for k, v in r["cost"].items() if v > 1e-9],
         "values": [v for k, v in r["cost"].items() if v > 1e-9]},
        {"type": "table", "header": ["成本项", "金额（元）", "占收入比"], "rows": cost_rows},
        {"type": "h1", "text": "三、汇率敏感性"},
        {"type": "bar", "title": "汇率变动下的净利（元/件）",
         "labels": list(r["fx_sensitivity"].keys()),
         "values": [v["net_cny"] for v in r["fx_sensitivity"].values()], "unit": "元"},
        {"type": "table", "header": ["汇率变动", "汇率", "净利（元）", "变化", "净利率"],
         "rows": [[k, "%.4f" % v["fx"], "%.2f" % v["net_cny"], "%+.2f" % v["delta_cny"],
                   "%.2f%%" % (v["margin"] * 100)] for k, v in r["fx_sensitivity"].items()]},
        {"type": "bullets", "items": [
            "口径：收入=售价×汇率；关税按申报货值×税率；VAT 按（申报货值+关税）计（可关）",
            "出口退税冲减成本（需增值税专用发票）；汇率缓冲按收入比例计提",
            "成本项为输入数据（S1/S2）；保本售价与敏感性为脚本推算值（S4）"]},
    ]
    spec = {"blocks": blocks}
    if title:
        spec["title"] = title
    if subtitle:
        spec["subtitle"] = subtitle
    return spec


DEMO = {
    "platform": "amazon_us", "sell_currency": "USD", "fx_rate": 7.15,
    "sell_price": 29.99, "unit_cost_cny": 45.0, "first_leg_cny": 8.0,
    "duty_rate": 0.078, "declare_ratio": 0.6, "vat_rate": 0.0, "vat_on_duty": True,
    "fba_fee": 5.5, "overseas_ship": 0.0, "storage_cny": 1.2,
    "commission_rate": 0.15, "payment_fee_rate": 0.015, "ad_rate": 0.12,
    "return_rate": 0.06, "return_loss_cny": 18.0,
    "export_rebate_rate": 0.13, "fx_buffer": 0.02, "target_margin": 0.18,
}


def main():
    ap = argparse.ArgumentParser(description="跨境到岸成本核算与保本售价")
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
        r = calc(data)
    except ValueError as e:
        sys.stderr.write("输入错误: %s\n" % e)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
    if a.spec_out:
        with open(a.spec_out, "w", encoding="utf-8") as f:
            json.dump(make_spec(r, title="%s 跨境利润核算报告" % r["platform"]), f,
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

    # 简化场景：无税无 FBA，验证恒等式
    d = {"fx_rate": 7.0, "sell_price": 10.0, "unit_cost_cny": 30.0,
         "commission_rate": 0.1, "fx_buffer": 0.0}
    r = calc(d)
    # 收入 70；佣金 7；成本 30 → 净利 33
    chk("收入=70", r["gross_cny"], 70.0, 1e-6)
    chk("净利=33", r["net_profit_cny"], 33.0, 1e-6)
    chk("恒等式 收入-总成本=净利",
        abs(r["gross_cny"] - r["total_cost_cny"] - r["net_profit_cny"]) < 1e-6, True)

    # 关税：申报比例 0.5，税率 10%，收入 70 → 申报 35 → 关税 3.5
    d2 = dict(d, declare_ratio=0.5, duty_rate=0.10)
    r2 = calc(d2)
    chk("关税=3.5", r2["cost"]["关税"], 3.5, 1e-6)

    # VAT 含关税计税：申报 35 + 关税 3.5 = 38.5，VAT 20% → 7.7
    d3 = dict(d2, vat_rate=0.20, vat_on_duty=True)
    r3 = calc(d3)
    chk("VAT=7.7（含关税为基数）", r3["cost"]["VAT/GST"], 7.7, 1e-6)
    d3b = dict(d2, vat_rate=0.20, vat_on_duty=False)
    r3b = calc(d3b)
    chk("VAT=7.0（不含关税为基数）", r3b["cost"]["VAT/GST"], 7.0, 1e-6)

    # 出口退税冲减成本：货品 30，退税率 13% → -3.9
    d4 = dict(d, export_rebate_rate=0.13)
    r4 = calc(d4)
    chk("出口退税=-3.9（冲减）", r4["cost"]["出口退税"], -3.9, 1e-6)

    # FBA 外币转人民币：5.5 USD × 7.0 = 38.5
    d5 = dict(d, fba_fee=5.5)
    r5 = calc(d5)
    chk("FBA=38.5", r5["cost"]["FBA配送"], 38.5, 1e-6)

    # 退货损失：18 × 6% = 1.08
    d6 = dict(d, return_rate=0.06, return_loss_cny=18.0)
    r6 = calc(d6)
    chk("退货净损失=1.08", r6["cost"]["退货净损失"], 1.08, 1e-6)

    # 保本售价：佣金率 10%，固定成本 30 元
    # 净利=0 → 收入×(1−0.1) = 30 → 收入 33.33 元 → 33.33/7 = 4.7619 USD
    chk("保本售价(外币)=4.7619", r["breakeven_price_fx"], (30 / 0.9) / 7.0, 1e-4)
    # 汇率敏感：+5% → 收入 73.5，净利 36.5（成本含佣金随收入变）
    s = r["fx_sensitivity"]["+5%"]
    chk("汇率+5% 净利增加", s["delta_cny"] > 0, True)

    # 缺汇率应报错
    try:
        calc({"sell_price": 10})
        chk("缺 fx_rate 应抛错", False, True)
    except ValueError:
        chk("缺 fx_rate 应抛错", True, True)

    print("\n自测：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
