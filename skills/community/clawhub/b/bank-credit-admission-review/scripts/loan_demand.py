#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""授信审查：流动资金贷款需求测算 + 刚性负债情况分析（确定性计算）。

两块服务于授信结论：
  ① 流动资金贷款需求测算 —— 依《流动资金贷款管理暂行办法》"营运资金量法"，
     给出"新增流动资金贷款额度"上限，约束授信金额合理性。
  ② 刚性负债情况分析     —— 拆解企业必须按期偿付的硬债务，给出占比 / 短期覆盖 /
     利息保障 / 刚性负债-EBITDA / 刚性负债-净资产 五指标与红旗阈值，约束偿债安全性。

计算由脚本确定性产出，禁止人工心算（与 negative_screen.py 同一纪律）。
缺失字段填 null（不要填 0），除零与缺口自动降级，零数据主体走定性降级。

用法:
  python loan_demand.py --input data.json [--format markdown|json]
  cat data.json | python loan_demand.py --format json

输入 JSON 格式:
{
  "company": "某某股份有限公司",
  "unit": "亿元",
  "annual_report_year": 2025,
  "working_capital": {
    "revenue": 100.0,                 // 上年度营业收入 S
    "net_profit": 5.0,                // 上年度净利润（算销售利润率）
    "growth_rate": 0.05,              // 预计销售收入年增长率 g（小数，缺省 0）
    "inventory": 20.0,                // 存货
    "cogs": 80.0,                     // 营业成本
    "accounts_receivable": 15.0,      // 应收账款
    "accounts_payable": 10.0,         // 应付账款
    "prepayments": 3.0,               // 预付账款
    "advances_received": 2.0,         // 预收账款
    "own_fund_ratio": 0.30,           // 借款人自有资金比例 f（缺省 0.30）
    "existing_short_term_loan": 8.0,  // 现有流动资金贷款 L（近似短期借款）
    "other_operating_funds": 0.0      // 其他渠道营运资金 O（缺省 0）
  },
  "rigid_liabilities": {
    "short_term_borrowing": 8.0,      // 短期借款
    "non_current_liab_due_within_1y": 2.0, // 一年内到期的非流动负债
    "long_term_borrowing": 5.0,       // 长期借款
    "bonds_payable": 0.0,             // 应付债券
    "long_term_payable": 1.0,         // 长期应付款（融资租赁等）
    "notes_payable_financing": 0.0,   // 应付票据（融资性部分，可选）
    "total_liabilities": 30.0,        // 负债合计
    "net_assets": 15.0,               // 所有者权益合计
    "ebit": 8.0,                      // 息税前利润（利润总额+利息费用）
    "ebitda": 10.0,                   // 息税折旧摊销前利润
    "interest_expense": 1.5,          // 利息费用
    "cash_and_equivalents": 4.0       // 货币资金
  }
}

字段缺失一律填 null。
"""

import argparse
import json
import sys

# ---- 刚性负债红旗阈值（可按行内口径在 rules_library.md 调整） ----
RIGID_SHARE_RED = 0.70        # 刚性负债占比 ≥ 70% 红
SHORT_COVER_RED = 1.0          # 短期刚性/货币资金 < 1.0 红（即期缺口）
INTEREST_COVER_RED = 1.0       # 利息保障倍数 < 1.0 红
RIGID_EBITDA_RED = 6.0         # 刚性负债/EBITDA > 6 红
RIGID_NA_RED = 1.5             # 刚性负债/净资产 ≥ 1.5 红

# ---- 流贷测算保守默认 ----
DEFAULT_GROWTH = 0.0
DEFAULT_OWN_FUND_RATIO = 0.30
DEFAULT_OTHER_FUNDS = 0.0


# ---------------------------------------------------------------- 工具

def safe_div(a, b):
    """除零 / 空值返回 None，不抛异常。"""
    if a is None or b in (None, 0):
        return None
    return a / b


def fmt(v, suffix="", nd=2):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.{nd}f}{suffix}"
    return f"{v}{suffix}"


def fmt_pct(v, nd=2):
    """小数比率（0.05 表示 5%）按百分比显示。"""
    if v is None:
        return "—"
    return f"{v*100:.{nd}f}%"


def level_tag(value, green, red, higher_better=True, nd=2):
    """三档标签：健康/关注/红旗。higher_better 决定红绿方向。"""
    if value is None:
        return "缺口"
    if higher_better:
        if value >= green:
            return "健康"
        if value >= red:
            return "关注"
        return "红旗"
    else:
        if value <= green:
            return "健康"
        if value <= red:
            return "关注"
        return "红旗"


# ---------------------------------------------------------------- 流贷测算

def compute_working_capital(wc):
    """返回 (结果 dict, 假设 list, 缺口 list)。"""
    assumptions, gaps = [], []

    revenue = wc.get("revenue")
    net_profit = wc.get("net_profit")
    cogs = wc.get("cogs")
    inventory = wc.get("inventory")
    ar = wc.get("accounts_receivable")
    ap = wc.get("accounts_payable")
    prepay = wc.get("prepayments")
    advrec = wc.get("advances_received")

    growth = wc.get("growth_rate")
    if growth is None:
        growth = DEFAULT_GROWTH
        assumptions.append("预计销售收入年增长率 g 缺失，保守取 0%")

    own_ratio = wc.get("own_fund_ratio")
    if own_ratio is None:
        own_ratio = DEFAULT_OWN_FUND_RATIO
        assumptions.append("借款人自有资金比例 f 缺失，保守取 30%")

    exist_loan = wc.get("existing_short_term_loan")
    if exist_loan is None:
        gaps.append("现有流动资金贷款 L 缺失，新增额度 A 不可得，须补数后复核")
    other_funds = wc.get("other_operating_funds")
    if other_funds is None:
        other_funds = DEFAULT_OTHER_FUNDS

    profit_margin = safe_div(net_profit, revenue)
    dinv = safe_div(360.0 * inventory if inventory is not None else None, cogs)
    drec = safe_div(360.0 * ar if ar is not None else None, revenue)
    dpay = safe_div(360.0 * ap if ap is not None else None, cogs)
    dpre = safe_div(360.0 * prepay if prepay is not None else None, cogs)
    dadv = safe_div(360.0 * advrec if advrec is not None else None, revenue)

    days = {"存货周转天数": dinv, "应收账款周转天数": drec,
            "应付账款周转天数": dpay, "预付账款周转天数": dpre,
            "预收账款周转天数": dadv}
    for name, val in days.items():
        if val is None:
            gaps.append("%s 因缺营收/成本/科目数据不可得" % name)

    turnover = None
    if None not in (dinv, drec, dpay, dpre, dadv):
        denom = dinv + drec - dpay + dpre - dadv
        turnover = safe_div(360.0, denom)
        if turnover is None:
            gaps.append("营运资金周转次数因周转天数合计为 0 不可得")

    r_operating = None
    if None not in (revenue, profit_margin, turnover):
        r_operating = revenue * (1 - profit_margin) * (1 + growth) / turnover

    own_fund = r_operating * own_ratio if r_operating is not None else None
    new_loan = None
    if None not in (r_operating, own_fund, exist_loan, other_funds):
        new_loan = r_operating - own_fund - exist_loan - other_funds

    return {
        "revenue": revenue, "net_profit": net_profit,
        "profit_margin": profit_margin, "growth_rate": growth,
        "days": days, "turnover": turnover,
        "operating_capital": r_operating,
        "own_fund_ratio": own_ratio, "own_fund": own_fund,
        "existing_loan": exist_loan, "other_funds": other_funds,
        "new_loan_quota": new_loan,
    }, assumptions, gaps


def conclude_wc(res):
    a = res["new_loan_quota"]
    if a is None:
        return ("数据缺口·转补数前提",
                "新增流贷额度不可得，按缺口即风险处理：补经审计财报与周转科目后复核，"
                "介入前不得核定信用流贷额度。")
    if a < 0:
        return ("无需新增流贷",
                "测算新增额度为负（%.2f），自有资金与存量融资已覆盖营运资金需求，"
                "不应新增信用流贷；确有用途须以足额抵质押/强担保覆盖。" % a)
    return ("需求合理·额度上限可见",
            "新增流动资金贷款测算额度为 %.2f，拟授信流贷应 ≤ 该值；"
            "超额须说明真实用途并配套抵质押或强担保。" % a)


# ---------------------------------------------------------------- 刚性负债

def compute_rigid(rl):
    """返回 (结果 dict, 构成 dict, 指标 dict, 红旗 list, 假设 list, 缺口 list)。"""
    assumptions, gaps, reds = [], [], []

    comp = {
        "短期借款": rl.get("short_term_borrowing"),
        "一年内到期非流动负债": rl.get("non_current_liab_due_within_1y"),
        "长期借款": rl.get("long_term_borrowing"),
        "应付债券": rl.get("bonds_payable"),
        "长期应付款": rl.get("long_term_payable"),
        "应付票据(融资性)": rl.get("notes_payable_financing", 0.0),
    }
    missing_comp = [k for k, v in comp.items() if v is None]
    if missing_comp:
        gaps.append("刚性负债构成缺失：%s（按 0 计入总额，可能低估，须补数）"
                    % "、".join(missing_comp))

    rigid_total = sum(v for v in comp.values() if v is not None)
    rigid_short = sum(v for v in (comp["短期借款"],
                                  comp["一年内到期非流动负债"]) if v is not None)

    total_liab = rl.get("total_liabilities")
    net_assets = rl.get("net_assets")
    ebitda = rl.get("ebitda")
    ebit = rl.get("ebit")
    interest = rl.get("interest_expense")
    cash = rl.get("cash_and_equivalents")

    for nm, val in (("总负债", total_liab), ("净资产", net_assets),
                    ("EBITDA", ebitda), ("EBIT", ebit),
                    ("利息费用", interest), ("货币资金", cash)):
        if val is None:
            gaps.append("%s 缺失，相关刚性指标不可得" % nm)

    share = safe_div(rigid_total, total_liab)
    short_cover = safe_div(rigid_short, cash)
    interest_cover = safe_div(ebit, interest)
    rigid_ebitda = safe_div(rigid_total, ebitda)
    rigid_na = safe_div(rigid_total, net_assets)

    metrics = {
        "刚性负债占比": (share, level_tag(share, 0.50, RIGID_SHARE_RED, higher_better=False)),
        "短期刚性/货币资金": (short_cover, level_tag(short_cover, 1.0, SHORT_COVER_RED, higher_better=True)),
        "利息保障倍数": (interest_cover, level_tag(interest_cover, 3.0, INTEREST_COVER_RED, higher_better=True)),
        "刚性负债/EBITDA": (rigid_ebitda, level_tag(rigid_ebitda, 3.0, RIGID_EBITDA_RED, higher_better=False)),
        "刚性负债/净资产": (rigid_na, level_tag(rigid_na, 1.0, RIGID_NA_RED, higher_better=False)),
    }

    red_map = {
        "刚性负债占比": (share, "≥70%"),
        "短期刚性/货币资金": (short_cover, "<1.0"),
        "利息保障倍数": (interest_cover, "<1.0"),
        "刚性负债/EBITDA": (rigid_ebitda, ">6"),
        "刚性负债/净资产": (rigid_na, "≥1.5"),
    }
    for nm, (val, cond) in red_map.items():
        if val is not None:
            if nm == "刚性负债占比" and val >= RIGID_SHARE_RED:
                reds.append("%s 触发红旗（%.2f，%s）" % (nm, val, cond))
            elif nm == "短期刚性/货币资金" and val < SHORT_COVER_RED:
                reds.append("%s 触发红旗（%.2f，%s）" % (nm, val, cond))
            elif nm == "利息保障倍数" and val < INTEREST_COVER_RED:
                reds.append("%s 触发红旗（%.2f，%s）" % (nm, val, cond))
            elif nm == "刚性负债/EBITDA" and val > RIGID_EBITDA_RED:
                reds.append("%s 触发红旗（%.2f，%s）" % (nm, val, cond))
            elif nm == "刚性负债/净资产" and val >= RIGID_NA_RED:
                reds.append("%s 触发红旗（%.2f，%s）" % (nm, val, cond))

    return ({"total": rigid_total, "short": rigid_short,
             "short_share_of_rigid": safe_div(rigid_short, rigid_total)},
            comp, metrics, reds, assumptions, gaps)


def conclude_rigid(res, reds):
    if res["total"] is None or res["total"] == 0:
        return ("数据缺口·转补数前提",
                "刚性负债不可得，按缺口即风险处理：补企业征信与经审计财报后复核，"
                "介入前不得核定信用额度。")
    if not reds:
        return ("无红旗·结构可控",
                "刚性负债占比与短期覆盖、利息保障均在安全区，偿债结构总体可控，"
                "可按常规条件授信并纳入贷后监测。")
    severe = any("利息保障倍数" in r or "短期刚性/货币资金" in r for r in reds)
    if severe:
        return ("重大红旗·强担保前提",
                "存在即期偿付缺口或息前利润不抵利息，综合评级不得高于「中高」，"
                "授信须以足额抵质押或实控人无限连带为硬前提；若叠加第0步红线则不予介入。")
    return ("一般红旗·审慎",
            "存在刚性负债占比偏高/杠杆偏高等红旗，综合评级不得高于「中高」，"
            "须配强担保与期限错配修正，并设贷后预警线。")


# ---------------------------------------------------------------- 零数据降级

def is_desert(wc, rl):
    keys = ["revenue", "net_profit", "inventory", "accounts_receivable",
            "accounts_payable", "cogs"] + \
           ["short_term_borrowing", "total_liabilities", "cash_and_equivalents"]
    vals = [wc.get(k) for k in keys[:6]] + [rl.get(k) for k in keys[6:]]
    return all(v is None for v in vals)


# ---------------------------------------------------------------- 输出

def render_markdown(payload, wc_res, wc_assume, wc_gaps, wc_verdict, wc_reason,
                    rg_res, rg_comp, rg_metrics, rg_reds, rg_assume, rg_gaps,
                    rg_verdict, rg_reason, desert):
    unit = payload.get("unit") or "万元"
    yr = payload.get("annual_report_year") or "—"
    lines = []
    lines.append("# %s 流动资金贷款需求测算 与 刚性负债情况分析" % payload.get("company", "—"))
    lines.append("")
    lines.append("> 本报告为辅助参考，不替代正式授信审批决策。测算年度：%s ｜ 金额单位：%s" % (yr, unit))
    lines.append("")

    if desert:
        lines.append("## 零数据降级提示")
        lines.append("")
        lines.append("- 被查主体关键财务科目（营收/净利/周转/刚性负债/货币资金等）均为空，"
                     "流贷需求测算与刚性负债分析均不可得。按「零数据/非上市主体」降级规则处理："
                     "暂不予信用授信；确需介入须同时满足——提供经审计财报 + 足额强担保/抵质押"
                     "+ 严格 KYC（凭 USCC 排除同名/关联失信主体）+ 现场尽调。")
        lines.append("")
        lines.append("---")
        return "\n".join(lines)

    # 一、流贷测算
    lines.append("## 一、流动资金贷款需求测算")
    lines.append("")
    lines.append("| 参数 | 数值 | 参数 | 数值 |")
    lines.append("|---|---|---|---|")
    lines.append("| 上年度营业收入 | %s | 销售利润率 | %s |" %
                 (fmt(wc_res["revenue"], unit), fmt_pct(wc_res["profit_margin"])))
    lines.append("| 预计增长率 g | %s | 营运资金周转次数 | %s |" %
                 (fmt_pct(wc_res["growth_rate"]), fmt(wc_res["turnover"], "次", 2)))
    lines.append("| 营运资金量 R | %s | 自有资金比例 f | %s |" %
                 (fmt(wc_res["operating_capital"], unit), fmt_pct(wc_res["own_fund_ratio"])))
    lines.append("| 借款人自有资金 F | %s | 现有流贷 L | %s |" %
                 (fmt(wc_res["own_fund"], unit), fmt(wc_res["existing_loan"], unit)))
    lines.append("| 其他渠道 O | %s | **新增流贷额度 A** | **%s** |" %
                 (fmt(wc_res["other_funds"], unit), fmt(wc_res["new_loan_quota"], unit)))
    lines.append("")
    lines.append("**周转天数**：存货 %s ｜ 应收 %s ｜ 应付 %s ｜ 预付 %s ｜ 预收 %s" % (
        fmt(wc_res["days"]["存货周转天数"], "天"),
        fmt(wc_res["days"]["应收账款周转天数"], "天"),
        fmt(wc_res["days"]["应付账款周转天数"], "天"),
        fmt(wc_res["days"]["预付账款周转天数"], "天"),
        fmt(wc_res["days"]["预收账款周转天数"], "天")))
    lines.append("")
    lines.append("**结论**：%s —— %s" % (wc_verdict, wc_reason))
    lines.append("")

    # 二、刚性负债
    lines.append("## 二、刚性负债情况分析")
    lines.append("")
    lines.append("### 2.1 刚性负债构成（金额单位：%s）" % unit)
    lines.append("")
    lines.append("| 科目 | 金额 |")
    lines.append("|---|---|")
    for k, v in rg_comp.items():
        lines.append("| %s | %s |" % (k, fmt(v, unit)))
    lines.append("| **刚性负债合计** | **%s** |" % fmt(rg_res["total"], unit))
    lines.append("| 其中：短期刚性（短期借款+一年内到期） | %s（占刚性 %.1f%%） |" %
                 (fmt(rg_res["short"], unit),
                  100 * (rg_res["short_share_of_rigid"] or 0)))
    lines.append("")
    lines.append("### 2.2 核心指标与红旗")
    lines.append("")
    lines.append("| 指标 | 数值 | 判定 |")
    lines.append("|---|---|---|")
    label_map = {"刚性负债占比": "%", "短期刚性/货币资金": "倍",
                 "利息保障倍数": "倍", "刚性负债/EBITDA": "倍", "刚性负债/净资产": "倍"}
    for nm, (val, tag) in rg_metrics.items():
        disp = fmt_pct(val) if nm == "刚性负债占比" else fmt(val, label_map[nm])
        lines.append("| %s | %s | %s |" % (nm, disp, tag))
    lines.append("")
    if rg_reds:
        lines.append("**红旗汇总**：")
        for r in rg_reds:
            lines.append("- ⚠ %s" % r)
        lines.append("")
    else:
        lines.append("**红旗汇总**：未发现触发项。")
        lines.append("")
    lines.append("**结论**：%s —— %s" % (rg_verdict, rg_reason))
    lines.append("")

    # 三、假设与缺口
    lines.append("## 三、假设与信息缺口")
    lines.append("")
    if wc_assume or rg_assume:
        lines.append("**采用的保守假设**：")
        for a in wc_assume + rg_assume:
            lines.append("- %s" % a)
        lines.append("")
    if wc_gaps or rg_gaps:
        lines.append("**数据缺口**：")
        for g in wc_gaps + rg_gaps:
            lines.append("- %s" % g)
        lines.append("")
    if not (wc_assume or rg_assume or wc_gaps or rg_gaps):
        lines.append("- 输入数据完整，无额外假设与缺口。")
        lines.append("")

    # 四、联动建议
    lines.append("## 四、结论与联动建议")
    lines.append("")
    lines.append("- **流贷需求**：%s" % wc_reason)
    lines.append("- **刚性负债**：%s" % rg_reason)
    lines.append("- **联动处置**：拟授信流贷须 ≤ 测算新增额度 A；刚性负债任一红旗触发时，"
                 "综合评级不得高于「中高」，并以足额抵质押或强担保为硬前提；"
                 "数据缺口项转为介入前补数前提。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*本测算由 `loan_demand.py` 确定性产出，仅为辅助参考，不替代正式审批决策。*")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="流动资金贷款需求测算 与 刚性负债情况分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    ap.add_argument("--input", "-i", help="输入 JSON 文件路径；省略则从 stdin 读取")
    ap.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown",
                    help="输出格式，默认 markdown")
    ap.add_argument("--output", "-o", help="输出文件路径；省略则打印到 stdout")
    args = ap.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            raise SystemExit("错误：未提供输入。使用 --input <file> 或通过管道传入 JSON。")
        payload = json.loads(raw)

    wc = payload.get("working_capital") or {}
    rl = payload.get("rigid_liabilities") or {}
    desert = is_desert(wc, rl)

    wc_res, wc_assume, wc_gaps = compute_working_capital(wc)
    wc_verdict, wc_reason = conclude_wc(wc_res)

    rg_res, rg_comp, rg_metrics, rg_reds, rg_assume, rg_gaps = compute_rigid(rl)
    rg_verdict, rg_reason = conclude_rigid(rg_res, rg_reds)

    if args.format == "json":
        out = json.dumps({
            "company": payload.get("company"),
            "annual_report_year": payload.get("annual_report_year"),
            "desert_mode": desert,
            "working_capital": {
                "params": wc_res, "verdict": wc_verdict, "reason": wc_reason,
                "assumptions": wc_assume, "gaps": wc_gaps,
            },
            "rigid_liabilities": {
                "total": rg_res["total"], "composition": rg_comp,
                "metrics": {k: {"value": v[0], "tag": v[1]} for k, v in rg_metrics.items()},
                "red_flags": rg_reds, "verdict": rg_verdict, "reason": rg_reason,
                "assumptions": rg_assume, "gaps": rg_gaps,
            },
        }, ensure_ascii=False, indent=2)
    else:
        out = render_markdown(
            payload, wc_res, wc_assume, wc_gaps, wc_verdict, wc_reason,
            rg_res, rg_comp, rg_metrics, rg_reds, rg_assume, rg_gaps,
            rg_verdict, rg_reason, desert)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print("已写入：%s" % args.output)
    else:
        print(out)


if __name__ == "__main__":
    main()
