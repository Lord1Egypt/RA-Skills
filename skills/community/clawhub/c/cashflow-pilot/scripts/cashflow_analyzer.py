#!/usr/bin/env python3
"""
cashflow-pilot 收支分类与汇总分析模块

对账本数据进行多维度汇总分析，生成月度现金流报告、
分类统计、趋势分析等。
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    check_subscription,
    create_parser,
    format_chinese_unit,
    format_currency,
    format_number,
    format_percentage,
    load_input_data,
    load_ledger,
    output_error,
    output_success,
)


# ============================================================
# 数据汇总
# ============================================================

def summarize_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """汇总收支数据。

    Args:
        records: 账本记录列表。

    Returns:
        汇总结果字典。
    """
    total_income = 0.0
    total_expense = 0.0
    income_by_category = defaultdict(float)
    expense_by_category = defaultdict(float)
    income_count = 0
    expense_count = 0

    for r in records:
        amount = float(r.get("amount", 0))
        txn_type = r.get("type", "unknown")
        category = r.get("category", "未分类")

        if txn_type == "income":
            total_income += amount
            income_by_category[category] += amount
            income_count += 1
        elif txn_type == "expense":
            total_expense += amount
            expense_by_category[category] += amount
            expense_count += 1

    net_cashflow = total_income - total_expense

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_cashflow": round(net_cashflow, 2),
        "income_count": income_count,
        "expense_count": expense_count,
        "total_count": len(records),
        "income_by_category": dict(
            sorted(income_by_category.items(), key=lambda x: x[1], reverse=True)
        ),
        "expense_by_category": dict(
            sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)
        ),
        "cashflow_status": "正" if net_cashflow >= 0 else "负",
    }


def filter_records_by_month(
    records: List[Dict[str, Any]], year: int, month: int
) -> List[Dict[str, Any]]:
    """按月份筛选记录。

    Args:
        records: 全部账本记录。
        year: 年份。
        month: 月份。

    Returns:
        筛选后的记录列表。
    """
    result = []
    for r in records:
        date_str = r.get("date", "")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if dt.year == year and dt.month == month:
                result.append(r)
        except (ValueError, TypeError):
            continue
    return result


def filter_records_by_range(
    records: List[Dict[str, Any]], start_date: str, end_date: str
) -> List[Dict[str, Any]]:
    """按日期范围筛选记录。

    Args:
        records: 全部账本记录。
        start_date: 起始日期 (YYYY-MM-DD)。
        end_date: 截止日期 (YYYY-MM-DD)。

    Returns:
        筛选后的记录列表。
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return records

    result = []
    for r in records:
        try:
            dt = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            if start <= dt <= end:
                result.append(r)
        except (ValueError, TypeError):
            continue
    return result


# ============================================================
# 月度报告
# ============================================================

def generate_monthly_report(
    records: List[Dict[str, Any]], year: int, month: int
) -> Dict[str, Any]:
    """生成月度现金流报告。

    Args:
        records: 全部账本记录。
        year: 年份。
        month: 月份。

    Returns:
        月度报告数据字典。
    """
    monthly_records = filter_records_by_month(records, year, month)
    summary = summarize_records(monthly_records)
    sub = check_subscription()

    # 基础报告表格
    report_table = _build_summary_table(summary)

    # 分类明细
    income_detail = _build_category_table(summary["income_by_category"], "收入")
    expense_detail = _build_category_table(summary["expense_by_category"], "支出")

    report = {
        "period": f"{year}年{month}月",
        "year": year,
        "month": month,
        "summary": summary,
        "report_table": report_table,
        "income_detail": income_detail,
        "expense_detail": expense_detail,
        "record_count": len(monthly_records),
    }

    # 付费版附加内容
    if sub["tier"] == "paid":
        report["mermaid_pie_income"] = _build_mermaid_pie(
            summary["income_by_category"], "收入分类占比"
        )
        report["mermaid_pie_expense"] = _build_mermaid_pie(
            summary["expense_by_category"], "支出分类占比"
        )
        report["insights"] = _generate_insights(summary, monthly_records)

        # 异常检测
        anomalies = detect_anomalies(records, year, month)
        if anomalies:
            report["anomalies"] = anomalies

    # 生成 Markdown 报告
    report["markdown"] = _render_monthly_markdown(report, sub["tier"])

    return report


def _build_summary_table(summary: Dict[str, Any]) -> str:
    """生成汇总表格 Markdown。"""
    return (
        "| 指标 | 金额 |\n"
        "|------|-----:|\n"
        f"| 总收入 | {format_currency(summary['total_income'])} |\n"
        f"| 总支出 | {format_currency(summary['total_expense'])} |\n"
        f"| 净现金流 | {format_currency(summary['net_cashflow'])} |\n"
        f"| 收入笔数 | {summary['income_count']} |\n"
        f"| 支出笔数 | {summary['expense_count']} |\n"
    )


def _build_category_table(category_data: Dict[str, float], label: str) -> str:
    """生成分类明细表格 Markdown。"""
    if not category_data:
        return f"暂无{label}记录\n"

    total = sum(category_data.values())
    lines = [f"| {label}分类 | 金额 | 占比 |\n", "|------|-----:|-----:|\n"]

    for cat, amount in category_data.items():
        pct = amount / total if total > 0 else 0
        lines.append(
            f"| {cat} | {format_currency(amount)} | {format_percentage(pct)} |\n"
        )

    lines.append(f"| **合计** | **{format_currency(total)}** | **100.0%** |\n")
    return "".join(lines)


def _build_mermaid_pie(category_data: Dict[str, float], title: str) -> str:
    """生成 Mermaid 饼图代码。"""
    if not category_data:
        return ""

    lines = [f"```mermaid\npie title {title}"]
    for cat, amount in category_data.items():
        lines.append(f'    "{cat}" : {round(amount, 2)}')
    lines.append("```")
    return "\n".join(lines)


def _generate_insights(
    summary: Dict[str, Any], records: List[Dict[str, Any]]
) -> List[str]:
    """生成数据洞察建议（付费版）。"""
    insights = []

    net = summary["net_cashflow"]
    if net < 0:
        insights.append(
            f"本月净现金流为负（{format_currency(net)}），支出超过收入，"
            "建议关注支出控制或加快应收款回收。"
        )
    elif net > 0:
        ratio = net / summary["total_income"] if summary["total_income"] > 0 else 0
        insights.append(
            f"本月净现金流为正（{format_currency(net)}），"
            f"现金留存率 {format_percentage(ratio)}。"
        )

    # 最大支出类别分析
    if summary["expense_by_category"]:
        top_cat = max(summary["expense_by_category"], key=summary["expense_by_category"].get)
        top_amount = summary["expense_by_category"][top_cat]
        total_exp = summary["total_expense"]
        if total_exp > 0:
            pct = top_amount / total_exp
            insights.append(
                f"最大支出类别为「{top_cat}」，占总支出 {format_percentage(pct)}，"
                f"金额 {format_currency(top_amount)}。"
            )

    # 收入集中度
    if summary["income_by_category"]:
        top_inc_cat = max(summary["income_by_category"], key=summary["income_by_category"].get)
        top_inc = summary["income_by_category"][top_inc_cat]
        total_inc = summary["total_income"]
        if total_inc > 0 and top_inc / total_inc > 0.7:
            insights.append(
                f"收入高度集中于「{top_inc_cat}」（占比 {format_percentage(top_inc / total_inc)}），"
                "建议拓展收入来源以降低风险。"
            )

    return insights


def _render_monthly_markdown(report: Dict[str, Any], tier: str) -> str:
    """渲染月度报告为 Markdown 格式。"""
    lines = [
        f"# 现金流月报 — {report['period']}\n",
        f"统计记录数：{report['record_count']} 条\n",
        "## 核心指标\n",
        report["report_table"],
        "\n## 收入明细\n",
        report["income_detail"],
        "\n## 支出明细\n",
        report["expense_detail"],
    ]

    if tier == "paid":
        if report.get("mermaid_pie_income"):
            lines.extend(["\n## 收入分类图\n", report["mermaid_pie_income"], "\n"])
        if report.get("mermaid_pie_expense"):
            lines.extend(["\n## 支出分类图\n", report["mermaid_pie_expense"], "\n"])
        if report.get("insights"):
            lines.append("\n## 洞察与建议\n")
            for i, insight in enumerate(report["insights"], 1):
                lines.append(f"{i}. {insight}\n")
        if report.get("anomalies"):
            lines.append("\n## 异常告警\n")
            for a in report["anomalies"]:
                lines.append(f"- {a['message']}\n")

    lines.append("\n---\n*报告由 cashflow-pilot 自动生成*\n")
    return "".join(lines)


# ============================================================
# 趋势分析
# ============================================================

def analyze_trend(records: List[Dict[str, Any]], months: int = 6) -> Dict[str, Any]:
    """分析最近 N 个月的现金流趋势。

    Args:
        records: 全部账本记录。
        months: 分析月数，默认 6。

    Returns:
        趋势分析结果。
    """
    now = datetime.now()
    monthly_data = []

    for i in range(months - 1, -1, -1):
        year = now.year
        month = now.month - i
        while month <= 0:
            month += 12
            year -= 1

        month_records = filter_records_by_month(records, year, month)
        summary = summarize_records(month_records)
        monthly_data.append({
            "period": f"{year}-{month:02d}",
            "year": year,
            "month": month,
            "income": summary["total_income"],
            "expense": summary["total_expense"],
            "net": summary["net_cashflow"],
            "record_count": len(month_records),
        })

    # 生成趋势 Mermaid 图表（付费版）
    sub = check_subscription()
    mermaid_chart = ""
    if sub["tier"] == "paid" and monthly_data:
        mermaid_chart = _build_trend_chart(monthly_data)

    return {
        "months_analyzed": months,
        "monthly_data": monthly_data,
        "mermaid_chart": mermaid_chart,
        "trend_summary": _summarize_trend(monthly_data),
    }


def _build_trend_chart(monthly_data: List[Dict[str, Any]]) -> str:
    """生成趋势折线图 Mermaid 代码。"""
    lines = [
        "```mermaid",
        "xychart-beta",
        '    title "现金流趋势"',
        '    x-axis [' + ", ".join(f'"{d["period"]}"' for d in monthly_data) + "]",
        '    y-axis "金额（元）"',
        "    line [" + ", ".join(str(d["income"]) for d in monthly_data) + "]",
        "    line [" + ", ".join(str(d["expense"]) for d in monthly_data) + "]",
        "```",
    ]
    return "\n".join(lines)


def _summarize_trend(monthly_data: List[Dict[str, Any]]) -> str:
    """生成趋势文字摘要。"""
    if len(monthly_data) < 2:
        return "数据不足，无法分析趋势。"

    last = monthly_data[-1]
    prev = monthly_data[-2]

    parts = []

    # 收入趋势
    if prev["income"] > 0:
        inc_change = (last["income"] - prev["income"]) / prev["income"]
        direction = "增长" if inc_change >= 0 else "下降"
        parts.append(f"收入环比{direction} {format_percentage(abs(inc_change))}")
    else:
        parts.append(f"本月收入 {format_currency(last['income'])}")

    # 支出趋势
    if prev["expense"] > 0:
        exp_change = (last["expense"] - prev["expense"]) / prev["expense"]
        direction = "增长" if exp_change >= 0 else "下降"
        parts.append(f"支出环比{direction} {format_percentage(abs(exp_change))}")

    # 净现金流
    parts.append(f"净现金流 {format_currency(last['net'])}")

    return "；".join(parts) + "。"


# ============================================================
# 异常检测（付费版）
# ============================================================

def detect_anomalies(
    records: List[Dict[str, Any]], year: int, month: int
) -> List[Dict[str, Any]]:
    """检测月度支出异常。

    使用简单的均值+标准差方法，当某分类支出超过历史均值的2倍时标记为异常。

    Args:
        records: 全部账本记录。
        year: 目标年份。
        month: 目标月份。

    Returns:
        异常告警列表。
    """
    sub = check_subscription()
    if sub["tier"] != "paid":
        return []

    # 获取过去6个月各分类的支出数据
    category_history = defaultdict(list)
    for i in range(1, 7):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        month_records = filter_records_by_month(records, y, m)
        month_summary = summarize_records(month_records)
        for cat, amount in month_summary["expense_by_category"].items():
            category_history[cat].append(amount)

    # 当前月各分类支出
    current_records = filter_records_by_month(records, year, month)
    current_summary = summarize_records(current_records)

    anomalies = []
    for cat, current_amount in current_summary["expense_by_category"].items():
        history = category_history.get(cat, [])
        if len(history) < 2:
            continue

        avg = sum(history) / len(history)
        if avg > 0 and current_amount > avg * 2:
            anomalies.append({
                "category": cat,
                "current": round(current_amount, 2),
                "average": round(avg, 2),
                "ratio": round(current_amount / avg, 2),
                "message": (
                    f"「{cat}」本月支出 {format_currency(current_amount)}，"
                    f"是过去6月均值（{format_currency(avg)}）的 "
                    f"{current_amount / avg:.1f} 倍，请关注。"
                ),
            })

    return anomalies


# ============================================================
# 主入口
# ============================================================

def main():
    """主入口函数。"""
    parser = create_parser("cashflow-pilot 收支分类与汇总分析工具")
    parser.add_argument("--year", type=int, default=None, help="年份")
    parser.add_argument("--month", type=int, default=None, help="月份")
    parser.add_argument("--months", type=int, default=6, help="趋势分析月数")

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    try:
        # 加载数据
        data = load_input_data(args)
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict) and "records" in data:
            records = data["records"]
        else:
            records = load_ledger()

        if args.action == "summary":
            # 汇总分析
            if args.year and args.month:
                records = filter_records_by_month(records, args.year, args.month)
            summary = summarize_records(records)
            output_success(summary)

        elif args.action == "monthly":
            # 月度报告
            year = args.year or datetime.now().year
            month = args.month or datetime.now().month
            report = generate_monthly_report(records, year, month)
            output_success(report)

        elif args.action == "trend":
            # 趋势分析
            result = analyze_trend(records, args.months)
            output_success(result)

        elif args.action == "anomaly":
            # 异常检测
            year = args.year or datetime.now().year
            month = args.month or datetime.now().month
            anomalies = detect_anomalies(records, year, month)
            output_success({
                "period": f"{year}年{month}月",
                "anomalies": anomalies,
                "count": len(anomalies),
            })

        else:
            output_error(
                f"不支持的操作: {args.action}。支持的操作: summary, monthly, trend, anomaly",
                "INVALID_ACTION",
            )

    except ValueError as e:
        output_error(str(e), "ANALYSIS_ERROR")
    except Exception as e:
        output_error(f"分析执行失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
