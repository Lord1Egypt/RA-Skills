#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""银行授信「一般负面情况」三条红线确定性判定脚本。

判定标准（命中任意一条即构成一般负面情况）:
  C1 连续三年亏损        —— 归母、合计两口径**分别**判定，任一口径最近三个完整
                            会计年度净利润均 < 0 即命中（两口径平权，不设优先回退）
  C2 连续三年资产负债率超标 —— 最近三个年度报表资产负债率均 > 85%（严格大于）
  C3 当期年报净资产为负   —— **最近一个**年度报表净资产 < 0 即命中，不要求连续三年

口径确认记录：上述 C1 双口径平权、C2 严格大于、C3 当期单年三项，
均经业务口径确认于 2026-08-11 生效。修改前须重新确认。

用法:
  python negative_screen.py --input data.json [--format markdown|json]
  cat data.json | python negative_screen.py --format json

输入 JSON 格式:
{
  "company": "某某股份有限公司",
  "entity_type": "企业法人",          // 企业法人 | 事业单位 | 其他
  "unit": "亿元",                      // 金额单位，仅用于展示
  "years": [
    {
      "year": 2023,
      "net_profit_parent": 121.63,     // 归母净利润（C1 口径之一）
      "net_profit_total": null,        // 净利润合计（C1 口径之一，与归母平权）
      "net_profit_deducted": null,     // 扣非归母净利润（实质性连亏辅助判断）
      "asset_liability_ratio": 73.22,  // 资产负债率，百分数值（73.22 表示 73.22%）
      "total_assets": null,            // 资产总计（用于反算资产负债率）
      "total_liabilities": null,       // 负债合计（用于反算资产负债率）
      "net_assets": null,              // 净资产，默认取所有者权益合计
      "net_assets_parent": null,       // 归母净资产（可选，用于母公司资不抵债提示）
      "audit_opinion": "标准无保留",   // 审计意见类型
      "source": "MCP·预警通 2023年报"  // 来源标签，必填
    }
  ]
}

字段缺失一律填 null，不要填 0。
"""

import argparse
import json
import sys

ALR_RED_LINE = 85.0      # 资产负债率红线（%），严格大于才算超标
ALR_WATCH_LINE = 80.0    # 资产负债率临界关注线（%）
REQUIRED_YEARS = 3       # C1/C2 的连续年度数
BLOCKED = ("数据缺口", "数据不足")

# C1 双口径定义：两者平权，任一口径连续三年为负即命中
PROFIT_CALIBERS = (
    ("net_profit_parent", "归母净利润"),
    ("net_profit_total", "净利润合计"),
)


# ---------------------------------------------------------------- 数据准备

def load_payload(path):
    if path:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("错误：未提供输入。使用 --input <file> 或通过管道传入 JSON。")
    return json.loads(raw)


def normalize_years(years):
    """按年度倒序排列，取最近 REQUIRED_YEARS 个完整年度，并补齐派生字段。"""
    cleaned = [y for y in years if y.get("year") is not None]
    cleaned.sort(key=lambda y: int(y["year"]), reverse=True)
    window = cleaned[:REQUIRED_YEARS]
    for y in window:
        # 资产负债率缺失时用 负债合计 / 资产总计 反算
        if y.get("asset_liability_ratio") is None:
            ta, tl = y.get("total_assets"), y.get("total_liabilities")
            if ta not in (None, 0) and tl is not None:
                y["asset_liability_ratio"] = round(tl / ta * 100, 2)
                y["_alr_derived"] = True
        # 净资产缺失时用 资产总计 - 负债合计 反算
        if y.get("net_assets") is None:
            ta, tl = y.get("total_assets"), y.get("total_liabilities")
            if ta is not None and tl is not None:
                y["net_assets"] = round(ta - tl, 4)
                y["_na_derived"] = True
        # 仍缺失时，由资产负债率推定净资产正负（ALR<100% ⇔ 资产>负债 ⇔ 净资产为正）
        if y.get("net_assets") is None and y.get("asset_liability_ratio") is not None:
            alr = y["asset_liability_ratio"]
            if alr < 100:
                y["_na_inferred_sign"] = 1.0
            elif alr > 100:
                y["_na_inferred_sign"] = -1.0
    return window


def net_assets_for_judge(y):
    """C3 判定取值：优先实际净资产，其次由资产负债率推定的正负号。"""
    if y.get("net_assets") is not None:
        return y["net_assets"]
    return y.get("_na_inferred_sign")


def net_assets_display(y):
    if y.get("net_assets") is not None:
        return fmt(y["net_assets"])
    sign = y.get("_na_inferred_sign")
    if sign is None:
        return "—"
    return "正（推定）" if sign > 0 else "负（推定）"


def is_non_standard_opinion(opinion):
    """判断审计意见是否为非标准意见。"标准无保留"不应触发预警。"""
    op = (opinion or "").replace(" ", "")
    if not op:
        return None
    for key in ("否定意见", "否定", "无法表示意见", "无法表示"):
        if key in op:
            return key
    if "持续经营" in op:
        return "含持续经营重大不确定性"
    if "强调事项" in op:
        return "带强调事项段"
    # "保留意见" 命中，但 "无保留" / "标准无保留" 不命中
    if "保留" in op and "无保留" not in op:
        return "保留意见"
    return None


def display_profit(y):
    """仅用于表格展示与趋势提示，不参与红线判定。"""
    if y.get("net_profit_parent") is not None:
        return y["net_profit_parent"]
    return y.get("net_profit_total")


# ---------------------------------------------------------------- 单项判定

def judge_criterion(window, extract, predicate, label):
    """通用连续三年判定器。返回 dict：命中 / 未命中 / 数据缺口 / 数据不足。"""
    values, gaps = [], []
    for y in window:
        val = extract(y)
        if val is None:
            gaps.append(str(y["year"]))
        values.append({"year": y["year"], "value": val})

    if len(window) < REQUIRED_YEARS:
        status = "数据不足"
        detail = "仅取得 %d 个完整会计年度，不满足「连续三年」判定前提" % len(window)
    elif gaps:
        status = "数据缺口"
        detail = "以下年度缺少该指标：%s" % "、".join(gaps)
    elif all(predicate(v["value"]) for v in values):
        status = "命中"
        detail = "最近三个完整会计年度全部满足红线条件"
    else:
        status = "未命中"
        hit_years = [str(v["year"]) for v in values if predicate(v["value"])]
        detail = ("其中 %s 年度满足红线条件，未构成连续三年" % "、".join(hit_years)
                  if hit_years else "三个年度均不满足红线条件")

    return {"criterion": label, "status": status, "detail": detail, "values": values}


def short_caliber(sub):
    """从子判定标签中取出口径名，如 "C1·归母净利润口径" -> "归母净利润口径"。"""
    return sub["criterion"].split("·")[1]


def caliber_names(subs):
    """拼接口径名，用书名号包裹以免中文行文中出现空格。"""
    return "、".join("「%s」" % short_caliber(s) for s in subs)


def judge_c1(window):
    """C1 双口径平权判定：归母、合计分别计算，任一口径连续三年为负即命中。"""
    subs = []
    for key, name in PROFIT_CALIBERS:
        subs.append(judge_criterion(
            window,
            lambda y, k=key: y.get(k),
            lambda v: v < 0,
            "C1·%s口径" % name))

    hits = [s for s in subs if s["status"] == "命中"]
    done = [s for s in subs if s["status"] == "未命中"]
    blocked = [s for s in subs if s["status"] in BLOCKED]

    if hits:
        status = "命中"
        detail = "以下口径构成连续三年亏损：%s（两口径平权，任一命中即构成）" % \
                 caliber_names(hits)
    elif done:
        status = "未命中"
        detail = "%s已完成判定，均未构成连续三年亏损" % caliber_names(done)
        if blocked:
            detail += "；%s因数据缺失未能判定" % caliber_names(blocked)
    else:
        status = "数据不足" if any(s["status"] == "数据不足" for s in subs) else "数据缺口"
        detail = "归母、合计两口径均无法完成判定：%s" % \
                 "；".join("%s（%s）" % (short_caliber(s), s["detail"]) for s in subs)

    return {"criterion": "C1 连续三年亏损（归母/合计双口径分别判定）",
            "status": status, "detail": detail,
            "values": [], "sub": subs}


def judge_c3(window):
    """C3 当期口径判定：最近一个年度报表净资产为负即命中，不要求连续三年。"""
    label = "C3 当期年报净资产为负"
    if not window:
        return {"criterion": label, "status": "数据不足",
                "detail": "未取得任何完整会计年度数据", "values": []}

    latest = window[0]
    val = net_assets_for_judge(latest)
    values = [{"year": latest["year"], "value": val}]

    if val is None:
        status = "数据缺口"
        detail = "%s 年度未取得净资产金额，且无法由资产负债率推定其正负" % latest["year"]
    elif val < 0:
        status = "命中"
        detail = "最近一期年报（%s 年度）净资产为负，按当期口径直接构成" % latest["year"]
    else:
        status = "未命中"
        detail = "最近一期年报（%s 年度）净资产为正" % latest["year"]

    return {"criterion": label, "status": status, "detail": detail, "values": values}


def judge_all(window):
    c1 = judge_c1(window)
    c2 = judge_criterion(window, lambda y: y.get("asset_liability_ratio"),
                         lambda v: v > ALR_RED_LINE,
                         "C2 连续三年资产负债率 > 85%")
    c3 = judge_c3(window)
    return [c1, c2, c3]


# ---------------------------------------------------------------- 附加提示

def build_warnings(window, results):
    warns = []
    c1, c2, c3 = results[0], results[1], results[2]
    full = len(window) == REQUIRED_YEARS

    # 双口径判定结论不一致
    if c1.get("sub"):
        hit_subs = [s for s in c1["sub"] if s["status"] == "命中"]
        miss_subs = [s for s in c1["sub"] if s["status"] == "未命中"]
        if hit_subs and miss_subs:
            warns.append("C1 双口径结论不一致：%s构成连续三年亏损，而%s未构成。"
                         "差额源于少数股东损益，须核查是否存在通过并表结构调节归母利润的情形。"
                         % (caliber_names(hit_subs), caliber_names(miss_subs)))

    # 扣非口径实质性连亏
    ded = [y.get("net_profit_deducted") for y in window]
    if full and all(v is not None for v in ded) and all(v < 0 for v in ded):
        if c1["status"] != "命中":
            warns.append("扣非归母净利润连续三年为负，主业已实质性连亏，"
                         "账面盈利依赖非经常性损益，建议按实质重于形式原则从严认定。")

    # 资产负债率临界
    alr = [y.get("asset_liability_ratio") for y in window]
    if full and all(v is not None for v in alr):
        if c2["status"] != "命中" and all(v > ALR_WATCH_LINE for v in alr):
            warns.append("资产负债率连续三年高于 %.0f%% 但未全部突破 %.0f%% 红线，"
                         "处于临界区间，须列为重点关注并补充最近一期数据复核。"
                         % (ALR_WATCH_LINE, ALR_RED_LINE))
        if any(abs(v - ALR_RED_LINE) < 0.5 for v in alr):
            warns.append("存在年度资产负债率贴近 %.0f%% 红线（差异不足 0.5 个百分点），"
                         "「超过」按严格大于认定，此类临界值须回原始报表复核小数位。"
                         % ALR_RED_LINE)
        if len(alr) >= 2 and alr[0] - alr[1] >= 5:
            warns.append("最近年度资产负债率较上年上升 %.2f 个百分点，杠杆抬升明显。"
                         % (alr[0] - alr[1]))

    # 亏损趋势
    profits = [display_profit(y) for y in window]
    if full and all(v is not None for v in profits):
        neg = [p for p in profits if p < 0]
        if c1["status"] != "命中" and len(neg) == 2:
            warns.append("三个年度中已有两年亏损，距连续三年亏损红线仅一步之遥，"
                         "须关注最近一期经营是否延续亏损。")

    # 净资产：当期未命中但历史曾为负
    if c3["status"] == "未命中" and len(window) > 1:
        hist_neg = [str(y["year"]) for y in window[1:]
                    if (net_assets_for_judge(y) or 0) < 0]
        if hist_neg:
            warns.append("最近一期净资产虽为正，但 %s 年度曾为负，"
                         "须核查转正来源（增资、债转股、资产重估或利润实现）及其可持续性。"
                         % "、".join(hist_neg))

    # 归母净资产为负而合计为正
    for y in window:
        nap, na = y.get("net_assets_parent"), y.get("net_assets")
        if nap is not None and nap < 0 and na is not None and na >= 0:
            warns.append("%s 年度所有者权益合计为正而归母净资产为负，"
                         "母公司层面已资不抵债，须穿透核查少数股东权益构成。" % y["year"])

    # 审计意见
    for y in window:
        opinion = y.get("audit_opinion")
        flag = is_non_standard_opinion(opinion)
        if flag:
            tail = "" if flag == opinion else "（属%s）" % flag
            warns.append("%s 年度审计意见为「%s」%s，属非标准审计意见，财务数据可靠性存疑，"
                         "判定结论须结合审计说明复核。" % (y["year"], opinion, tail))

    # 派生数据提示
    derived = [str(y["year"]) for y in window if y.get("_alr_derived") or y.get("_na_derived")]
    if derived:
        warns.append("%s 年度的资产负债率或净资产为脚本依据资产/负债科目反算所得，"
                     "非直接披露值，须与报表核对。" % "、".join(derived))

    inferred = [str(y["year"]) for y in window if y.get("_na_inferred_sign") is not None]
    if inferred:
        warns.append("%s 年度未取得净资产金额，脚本依据资产负债率是否低于 100%% "
                     "推定其正负以完成 C3 判定；推定仅决定正负、不代表具体金额，"
                     "如需引用净资产绝对值须另行补充。" % "、".join(inferred))

    return warns


def build_gaps(window, results):
    gaps = []
    if len(window) < REQUIRED_YEARS:
        gaps.append("完整会计年度数据不足 3 个（当前 %d 个），"
                    "C1、C2 无法完成「连续三年」判定，需补充历史年度报表；"
                    "C3 按当期口径判定，不受此限。" % len(window))
    for r in results:
        if r["status"] in BLOCKED:
            gaps.append("%s：%s" % (r["criterion"], r["detail"]))
        # C1 双口径平权，任一口径缺数据即属筛查不完整，须单列
        elif r.get("sub"):
            miss = [s for s in r["sub"] if s["status"] in BLOCKED]
            if miss:
                gaps.append("C1 采用归母、合计双口径分别判定，但%s数据缺失，"
                            "本次仅凭已有口径得出结论，须补充该口径年度数据后复筛。"
                            % caliber_names(miss))
    for y in window:
        if not y.get("source"):
            gaps.append("%s 年度数据未标注来源，不符合来源可追溯要求。" % y["year"])
    return gaps


def conclude(results, window):
    hits = [r for r in results if r["status"] == "命中"]
    blocked = [r for r in results if r["status"] in BLOCKED]
    if hits:
        return ("构成一般负面情况",
                "命中 %d 条红线：%s。" % (len(hits), "；".join(r["criterion"] for r in hits)))
    if not window or len(blocked) == len(results):
        return ("无法认定", "有效数据不足，三条红线均无法完成判定，需补充资料后重筛。")
    if blocked:
        return ("暂不构成（存在数据缺口）",
                "已完成判定的红线均未命中，但 %s 因数据缺失未能判定，结论存在不确定性。"
                % "、".join(r["criterion"] for r in blocked))
    return ("不构成一般负面情况", "三条红线均未命中。本结论不代表客户无其他风险。")


# ---------------------------------------------------------------- 输出渲染

def fmt(v, suffix=""):
    if v is None:
        return "—"
    if isinstance(v, float):
        return ("%.2f%s" % (v, suffix))
    return "%s%s" % (v, suffix)


def render_markdown(payload, window, results, warns, gaps, verdict, reason):
    unit = payload.get("unit") or "万元"
    lines = []
    lines.append("## 一、筛查结论")
    lines.append("")
    lines.append("**%s** —— %s" % (verdict, reason))
    lines.append("")
    lines.append("| 项 | 内容 |")
    lines.append("|---|---|")
    lines.append("| 客户名称 | %s |" % (payload.get("company") or "—"))
    lines.append("| 单位性质 | %s |" % (payload.get("entity_type") or "—"))
    lines.append("| 判定年度 | %s |" % ("、".join(str(y["year"]) for y in window) or "—"))
    lines.append("| 判定依据 | 行内「一般负面情况」三条红线（口径确认版 2026-08-11） |")
    lines.append("")

    lines.append("## 二、三条红线判定明细")
    lines.append("")
    lines.append("| 红线 | 判定结果 | 说明 |")
    lines.append("|---|---|---|")
    for r in results:
        lines.append("| %s | **%s** | %s |" % (r["criterion"], r["status"], r["detail"]))
        for s in r.get("sub", []):
            lines.append("| ├ %s | %s | %s |" % (s["criterion"], s["status"], s["detail"]))
    lines.append("")

    lines.append("### 逐年指标表（金额单位：%s）" % unit)
    lines.append("")
    lines.append("| 年度 | 归母净利润 | 净利润合计 | 扣非净利润 | 资产负债率 | 净资产 | 审计意见 | 来源 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for y in window:
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            y["year"],
            fmt(y.get("net_profit_parent")),
            fmt(y.get("net_profit_total")),
            fmt(y.get("net_profit_deducted")),
            fmt(y.get("asset_liability_ratio"), "%"),
            net_assets_display(y),
            y.get("audit_opinion") or "—",
            y.get("source") or "**未标注**",
        ))
    lines.append("")
    lines.append("> 判定口径：C1 归母与合计**分别计算、互不替代**，任一口径连续三年为负即命中；"
                 "C2「超过 85%」取严格大于；C3 仅看最近一期年报，净资产为负即命中。")
    lines.append("")

    lines.append("## 三、临界与风险提示")
    lines.append("")
    if warns:
        for w in warns:
            lines.append("- %s" % w)
    else:
        lines.append("- 未发现临界或异常提示项。")
    lines.append("")

    lines.append("## 四、信息缺口")
    lines.append("")
    if gaps:
        for g in gaps:
            lines.append("- %s" % g)
    else:
        lines.append("- 判定所需数据完整，无重大缺口。")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*本判定结果由「一般负面情况」红线快筛脚本自动生成，"
                 "仅为辅助参考，不替代正式审批决策。*")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="银行授信「一般负面情况」三条红线确定性判定",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    ap.add_argument("--input", "-i", help="输入 JSON 文件路径；省略则从 stdin 读取")
    ap.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown",
                    help="输出格式，默认 markdown")
    ap.add_argument("--output", "-o", help="输出文件路径；省略则打印到 stdout")
    args = ap.parse_args()

    payload = load_payload(args.input)
    years = payload.get("years") or []
    window = normalize_years(years)
    results = judge_all(window)
    warns = build_warnings(window, results)
    gaps = build_gaps(window, results)
    verdict, reason = conclude(results, window)

    if args.format == "json":
        out = json.dumps({
            "company": payload.get("company"),
            "entity_type": payload.get("entity_type"),
            "judged_years": [y["year"] for y in window],
            "verdict": verdict,
            "reason": reason,
            "criteria": results,
            "warnings": warns,
            "gaps": gaps,
        }, ensure_ascii=False, indent=2)
    else:
        out = render_markdown(payload, window, results, warns, gaps, verdict, reason)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print("已写入：%s" % args.output)
    else:
        print(out)


if __name__ == "__main__":
    main()
