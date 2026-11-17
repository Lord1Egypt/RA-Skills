#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""settlement_audit.py —— 平台结算单对账与异常检测（9 类检查）

覆盖 requirement 中的对账项：
  C1 佣金率区间校验（佣金 ÷ 销售额，默认 0.5%~30%）
  C2 结算金额为负检测（异常冲销）
  C3 退款大于销售额检测
  C4 零销售额却有费用检测（挂错单）
  C5 结算单汇总 vs 订单明细口径不一致
  C6 直播坑位费与佣金重复计 / 等效佣金率超阈值
  C7 促销补贴核销跨期
  C8 广告返点按未达框架量算高阶梯
  C9 退货扣款漏记

用法：
  python settlement_audit.py --self-test
  python settlement_audit.py --data settlement.json [--json] [--out report.md]
退出码：0 无 P0；1 存在 P0 级异常（致命，可直接接 CI）；2 输入数据缺失。
"""

import argparse
import json
import sys

DEFAULT_CFG = {
    "commission_min": 0.005,
    "commission_max": 0.30,
    "tolerance_abs": 1.0,        # 口径差异容差（元）
    "tolerance_rel": 0.005,      # 口径差异容差（相对）
    "live_equiv_commission_max": 0.30,   # 佣金+坑位费 等效佣金率上限
    "month_tolerance_days": 0,           # 补贴核销允许跨期天数
}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def audit(data: dict) -> dict:
    cfg = dict(DEFAULT_CFG)
    cfg.update(data.get("config") or {})
    rows = data.get("rows") or []
    summary = data.get("summary") or {}
    findings = []

    def add(code, level, title, detail, evidence=None):
        findings.append({"code": code, "level": level, "title": title,
                         "detail": detail, "evidence": evidence or {}})

    # C1 佣金率区间
    for r in rows:
        gmv, comm = _f(r.get("gmv")), _f(r.get("commission"))
        if gmv > 0:
            rate = comm / gmv
            if rate > cfg["commission_max"] or rate < 0:
                add("C1", "P0", "佣金率 %.2f%% 超出合理区间" % (rate * 100),
                    "订单 %s：佣金 %.2f / 销售额 %.2f，超出 %.1f%%~%.0f%% 区间，核对类目费率或是否重复计佣"
                    % (r.get("order_id"), comm, gmv, cfg["commission_min"] * 100, cfg["commission_max"] * 100),
                    {"order_id": r.get("order_id"), "rate": rate})
            elif rate < cfg["commission_min"] and comm != 0:
                add("C1", "P1", "佣金率 %.2f%% 低于常规下限" % (rate * 100),
                    "订单 %s：确认是否为 0 佣金类目或平台减免" % r.get("order_id"),
                    {"order_id": r.get("order_id"), "rate": rate})

    # C2 结算金额为负
    for r in rows:
        net = r.get("net_settlement")
        if net is not None and _f(net) < 0:
            lvl = "P1" if r.get("reversal_reason") else "P0"
            add("C2", lvl, "结算金额为负 %.2f" % _f(net),
                "订单 %s：%s" % (r.get("order_id"), "已有冲销说明：" + str(r.get("reversal_reason"))
                                if r.get("reversal_reason") else "无冲销说明，属异常冲销，需平台出具明细"),
                {"order_id": r.get("order_id"), "net": _f(net)})
    if summary.get("net_settlement") is not None and _f(summary["net_settlement"]) < 0:
        add("C2", "P0", "结算单合计为负 %.2f" % _f(summary["net_settlement"]),
            "整单净结算为负，必须逐项核对冲销与罚款明细", {})

    # C3 退款大于销售额
    for r in rows:
        gmv, refund = _f(r.get("gmv")), _f(r.get("refund"))
        if refund > gmv + 1e-9:
            add("C3", "P0", "退款 %.2f > 销售额 %.2f" % (refund, gmv),
                "订单 %s：存在跨订单退款挂账或重复退款" % r.get("order_id"),
                {"order_id": r.get("order_id")})

    # C4 零销售额却有费用
    for r in rows:
        gmv = _f(r.get("gmv"))
        fees = sum(_f(r.get(x)) for x in ("commission", "fee_ad", "fee_other", "koll_fee", "slot_fee"))
        if gmv == 0 and fees != 0:
            add("C4", "P0", "零销售额却有费用 %.2f" % fees,
                "订单 %s：高度疑似挂错单/广告或达人费用挂到错误链接" % r.get("order_id"),
                {"order_id": r.get("order_id"), "fees": fees})

    # C5 口径不一致（汇总 vs 明细）
    def cmp_sum(key_sum, key_row, label):
        s = summary.get(key_sum)
        if s is None or not rows:
            return
        s = _f(s)
        d = sum(_f(r.get(key_row)) for r in rows)
        diff = abs(s - d)
        tol = max(cfg["tolerance_abs"], abs(s) * cfg["tolerance_rel"])
        if diff > tol:
            add("C5", "P0" if diff > max(tol * 5, 100) else "P1",
                "%s 口径不一致：汇总 %.2f vs 明细 %.2f（差 %.2f）" % (label, s, d, s - d),
                "结算单汇总与订单明细不同源，需确认是否含税、是否含未结算订单、是否跨期",
                {"summary": s, "detail": d, "diff": s - d})

    cmp_sum("gmv", "gmv", "销售额")
    cmp_sum("commission", "commission", "佣金")
    cmp_sum("refund", "refund", "退款")
    cmp_sum("fee_ad", "fee_ad", "广告费用")

    # C6 直播坑位费与佣金重复计 / 等效佣金率
    for deal in data.get("live_deals") or []:
        gmv = _f(deal.get("gmv"))
        if gmv <= 0:
            continue
        equiv = (_f(deal.get("commission")) + _f(deal.get("slot_fee"))) / gmv
        if equiv > cfg["live_equiv_commission_max"]:
            add("C6", "P1", "达人等效佣金率 %.2f%% 超阈值" % (equiv * 100),
                "达人 %s（%s）：佣金 %.2f + 坑位费 %.2f / GMV %.2f。核对坑位费是否已含在佣金内，避免重复计"
                % (deal.get("anchor"), deal.get("date"), _f(deal.get("commission")),
                   _f(deal.get("slot_fee")), gmv),
                {"anchor": deal.get("anchor"), "equiv_rate": equiv})

    # C7 促销补贴核销跨期
    for s in data.get("subsidies") or []:
        od, sd = s.get("order_date"), s.get("settle_date")
        if od and sd and od[:7] != sd[:7]:
            add("C7", "P1", "补贴跨期核销：订单 %s / 核销 %s" % (od, sd),
                "补贴 %.2f 归属期与订单期不同月，需按权责发生制拆分，避免利润跨月失真" % _f(s.get("amount")),
                {"order_date": od, "settle_date": sd})

    # C8 广告返点阶梯
    rb = data.get("rebate")
    if rb:
        target, actual = _f(rb.get("framework_target")), _f(rb.get("actual_spend"))
        claimed = _f(rb.get("claimed_rebate_rate"))
        tiers = sorted((rb.get("tiers") or []), key=lambda t: _f(t.get("spend")), reverse=True)
        due = 0.0
        for t in tiers:
            if actual >= _f(t.get("spend")):
                due = _f(t.get("rate"))
                break
        if actual < target and claimed > due + 1e-9:
            add("C8", "P0", "广告返点多计 %.2f%%（应得 %.2f%%）" % (claimed * 100, due * 100),
                "框架量 %.0f 未达成（实际消耗 %.0f），却按高阶梯 %.2f%% 计提。应得返点 %.2f 元，多计 %.2f 元"
                % (target, actual, claimed * 100, actual * due, actual * (claimed - due)),
                {"due_rate": due, "claimed_rate": claimed, "over_amount": actual * (claimed - due)})

    # C9 退货扣款漏记
    for r in rows:
        refund = _f(r.get("refund"))
        if refund > 0 and r.get("return_deduction") is None and r.get("deduction_expected") is True:
            add("C9", "P1", "退货扣款漏记：订单 %s" % r.get("order_id"),
                "退款 %.2f 存在，但结算单无退货扣款记录，核对平台是否漏扣或已并入其他项" % refund,
                {"order_id": r.get("order_id")})

    p0 = [f for f in findings if f["level"] == "P0"]
    p1 = [f for f in findings if f["level"] == "P1"]
    return {
        "config": cfg,
        "counts": {"rows": len(rows), "P0": len(p0), "P1": len(p1), "total": len(findings)},
        "findings": findings,
        "verdict": "PASS" if not p0 else ("FAIL-P0" if p0 else "WARN"),
    }


def render(res: dict) -> str:
    o = ["【平台结算单对账】共 %d 行明细，异常 %d 项（P0 %d / P1 %d） → %s" % (
        res["counts"]["rows"], res["counts"]["total"], res["counts"]["P0"], res["counts"]["P1"], res["verdict"])]
    for f in res["findings"]:
        o.append("  [%s][%s] %s" % (f["level"], f["code"], f["title"]))
        o.append("        %s" % f["detail"])
    if not res["findings"]:
        o.append("  未发现异常项。")
    return "\n".join(o)


def self_test() -> int:
    ok = True
    data = {
        "summary": {"gmv": 10000, "commission": 800, "refund": 500, "net_settlement": 8700},
        "rows": [
            {"order_id": "A1", "gmv": 100, "commission": 5, "refund": 0},
            {"order_id": "A2", "gmv": 0, "commission": 3, "fee_ad": 20},          # C4
            {"order_id": "A3", "gmv": 200, "commission": 100, "refund": 0},        # C1 (50%)
            {"order_id": "A4", "gmv": 300, "commission": 15, "refund": 400},       # C3
            {"order_id": "A5", "gmv": 100, "commission": 5, "net_settlement": -50},  # C2
        ],
        "live_deals": [{"anchor": "达人X", "date": "2026-09-02", "gmv": 10000, "commission": 2000, "slot_fee": 3000}],
        "subsidies": [{"amount": 100, "order_date": "2026-08-30", "settle_date": "2026-09-05"}],
        "rebate": {"framework_target": 100000, "actual_spend": 60000, "claimed_rebate_rate": 0.08,
                   "tiers": [{"spend": 100000, "rate": 0.08}, {"spend": 50000, "rate": 0.04}]},
    }
    res = audit(data)
    codes = set(f["code"] for f in res["findings"])

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    chk("C1 佣金率超区间命中", "C1" in codes)
    chk("C2 结算金额负命中", "C2" in codes)
    chk("C3 退款>销售额命中", "C3" in codes)
    chk("C4 零销售额有费用命中", "C4" in codes)
    chk("C5 口径不一致命中", "C5" in codes)
    chk("C6 等效佣金率超阈值命中", "C6" in codes)
    chk("C7 补贴跨期命中", "C7" in codes)
    chk("C8 返点高阶梯命中", "C8" in codes)
    chk("存在 P0 → verdict=FAIL-P0", res["verdict"] == "FAIL-P0")
    chk("P0 数量 >= 5", res["counts"]["P0"] >= 5)

    clean = audit({"rows": [{"order_id": "B1", "gmv": 100, "commission": 5, "refund": 0, "net_settlement": 95}],
                   "summary": {"gmv": 100, "commission": 5, "refund": 0, "net_settlement": 95}})
    chk("干净数据 PASS", clean["verdict"] == "PASS" and clean["counts"]["total"] == 0)
    # C8 返点计算正确性：应得 4%，多计 = 60000*(0.08-0.04)=2400
    c8 = [f for f in res["findings"] if f["code"] == "C8"][0]
    chk("C8 多计金额 = 2400", abs(c8["evidence"]["over_amount"] - 2400) < 1e-6)
    print("settlement_audit self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def make_spec(res, title=None, subtitle=None):
    """产出可直接喂给 report_pdf.build 的 spec（异常分布可视化）。"""
    import collections
    by_code = collections.Counter(f["code"] for f in res["findings"])
    name = {
        "C1": "佣金率超区间", "C2": "结算金额为负", "C3": "退款大于销售额",
        "C4": "零销售额有费用", "C5": "口径不一致", "C6": "退货扣款漏记",
        "C7": "坑位费与佣金重复计", "C8": "补贴跨期", "C9": "返点阶梯高估",
    }
    c = res["counts"]
    blocks = [
        {"type": "h1", "text": "一、对账结论"},
        {"type": "callout", "tone": "warn" if c["P0"] else "ok",
         "text": "共 %d 行明细，异常 %d 项（P0 %d / P1 %d）→ %s"
                 % (c["rows"], c["total"], c["P0"], c["P1"], res["verdict"])},
        {"type": "kv", "per_row": 4, "items": [
            ["明细行数", str(c["rows"])], ["异常总数", str(c["total"])],
            ["P0", str(c["P0"])], ["P1", str(c["P1"])]]},
        {"type": "h1", "text": "二、异常分布"},
        {"type": "bar", "title": "按异常类型分布（条）",
         "labels": ["%s %s" % (k, name.get(k, "")) for k in sorted(by_code)],
         "values": [by_code[k] for k in sorted(by_code)], "unit": "条"},
        {"type": "h1", "text": "三、异常清单"},
        {"type": "table", "header": ["级别", "代码", "问题", "说明"],
         "rows": [[f["level"], f["code"], f["title"], f["detail"][:90]]
                  for f in res["findings"]] or [["—", "—", "未发现异常", "—"]]},
        {"type": "bullets", "items": [
            "对账口径：佣金率=佣金÷销售额，合理区间 0.5%–30%",
            "每条异常均需给出金额影响（R8）；本表未逐条量化金额时，请在交付前补齐"]},
    ]
    spec = {"blocks": blocks}
    if title:
        spec["title"] = title
    if subtitle:
        spec["subtitle"] = subtitle
    return spec


def main():
    ap = argparse.ArgumentParser(description="平台结算单对账")
    ap.add_argument("--data", help="结算数据 JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="输出 markdown 报告")
    ap.add_argument("--spec-out", help="输出 report_pdf 可用的图表 spec JSON")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.data:
        ap.error("需要 --data 或 --self-test")
    with open(a.data, "r", encoding="utf-8") as f:
        res = audit(json.load(f))
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(render(res))
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else render(res))
    if a.spec_out:
        with open(a.spec_out, "w", encoding="utf-8") as f:
            json.dump(make_spec(res, title="平台结算单对账报告"), f,
                      ensure_ascii=False, indent=2)
        sys.stderr.write("spec 已写入 %s\n" % a.spec_out)
    return 1 if res["counts"]["P0"] else 0


if __name__ == "__main__":
    sys.exit(main())
