#!/usr/bin/env python3
"""
customer-pulse 销售漏斗与转化分析模块

提供销售阶段分析、转化率统计、月度报表生成等功能。
"""

import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    format_currency,
    get_data_file,
    load_input_data,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    today_str,
    STAGES,
)


# ============================================================
# 数据文件
# ============================================================

CUSTOMERS_FILE = "customers.json"
FOLLOWUPS_FILE = "followups.json"


def _get_customers() -> List[Dict[str, Any]]:
    """读取所有客户数据。"""
    return read_json_file(get_data_file(CUSTOMERS_FILE))


def _get_followups() -> List[Dict[str, Any]]:
    """读取所有跟进记录。"""
    return read_json_file(get_data_file(FOLLOWUPS_FILE))


# ============================================================
# 漏斗分析
# ============================================================

def analyze_funnel(data: Optional[Dict[str, Any]] = None) -> None:
    """分析销售漏斗各阶段分布。

    统计各阶段客户数量、预算总额，生成漏斗视图。

    Args:
        data: 可选过滤参数。
    """
    customers = _get_customers()
    if not customers:
        output_error("暂无客户数据", code="NO_DATA")
        return

    # 按阶段统计
    funnel_stages = ["初步接触", "需求确认", "方案报价", "谈判", "成交"]
    stage_data = []

    for stage in funnel_stages:
        stage_customers = [c for c in customers if c.get("stage") == stage]
        total_budget = sum(float(c.get("budget", 0)) for c in stage_customers)
        stage_data.append({
            "stage": stage,
            "count": len(stage_customers),
            "budget_total": total_budget,
            "budget_display": format_currency(total_budget),
        })

    # 流失客户单独统计
    lost_customers = [c for c in customers if c.get("stage") == "流失"]
    lost_budget = sum(float(c.get("budget", 0)) for c in lost_customers)

    # 计算漏斗转化率（相邻阶段）
    conversions = []
    for i in range(len(funnel_stages) - 1):
        from_count = stage_data[i]["count"]
        to_count = stage_data[i + 1]["count"]
        rate = (to_count / from_count * 100) if from_count > 0 else 0
        conversions.append({
            "from_stage": funnel_stages[i],
            "to_stage": funnel_stages[i + 1],
            "from_count": from_count,
            "to_count": to_count,
            "conversion_rate": f"{rate:.1f}%",
        })

    # 总转化率
    total_leads = stage_data[0]["count"] + stage_data[1]["count"] + stage_data[2]["count"] + stage_data[3]["count"]
    total_won = stage_data[4]["count"]
    overall_rate = (total_won / (total_leads + total_won) * 100) if (total_leads + total_won) > 0 else 0

    result = {
        "funnel": stage_data,
        "conversions": conversions,
        "lost": {
            "count": len(lost_customers),
            "budget_total": lost_budget,
            "budget_display": format_currency(lost_budget),
        },
        "overall": {
            "total_customers": len(customers),
            "active_pipeline": total_leads,
            "won": total_won,
            "lost": len(lost_customers),
            "overall_conversion_rate": f"{overall_rate:.1f}%",
        },
    }

    # 付费版：生成 Mermaid 漏斗图
    sub = check_subscription()
    if "mermaid_chart" in sub["features"]:
        mermaid = _generate_funnel_mermaid(stage_data)
        result["mermaid_chart"] = mermaid

    output_success(result)


def analyze_conversion(data: Optional[Dict[str, Any]] = None) -> None:
    """分析各阶段转化率详情。

    付费功能：包含详细的阶段停留时长、转化瓶颈分析。

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("conversion_analysis", "成交率分析"):
        return

    customers = _get_customers()
    followups = _get_followups()

    if not customers:
        output_error("暂无客户数据", code="NO_DATA")
        return

    funnel_stages = ["初步接触", "需求确认", "方案报价", "谈判", "成交"]
    stage_details = []

    for i, stage in enumerate(funnel_stages):
        stage_customers = [c for c in customers if c.get("stage") == stage]

        # 计算平均停留时长
        total_days = 0
        counted = 0
        for c in stage_customers:
            created = c.get("created_at", "")[:10]
            if created:
                from utils import calculate_days_since
                days = calculate_days_since(created)
                total_days += days
                counted += 1

        avg_days = total_days / counted if counted > 0 else 0

        # 平均跟进次数
        stage_customer_ids = {c["id"] for c in stage_customers}
        stage_followups = [f for f in followups if f.get("customer_id") in stage_customer_ids]
        avg_followups = len(stage_followups) / len(stage_customers) if stage_customers else 0

        stage_details.append({
            "stage": stage,
            "count": len(stage_customers),
            "avg_days_in_stage": round(avg_days, 1),
            "avg_followup_count": round(avg_followups, 1),
            "total_budget": format_currency(sum(float(c.get("budget", 0)) for c in stage_customers)),
        })

    # 瓶颈分析
    bottleneck = None
    min_rate = 100
    for i in range(len(funnel_stages) - 1):
        from_count = stage_details[i]["count"]
        to_count = stage_details[i + 1]["count"]
        rate = (to_count / from_count * 100) if from_count > 0 else 100
        if rate < min_rate:
            min_rate = rate
            bottleneck = {
                "from_stage": funnel_stages[i],
                "to_stage": funnel_stages[i + 1],
                "conversion_rate": f"{rate:.1f}%",
                "suggestion": _get_bottleneck_suggestion(funnel_stages[i], funnel_stages[i + 1]),
            }

    output_success({
        "stage_details": stage_details,
        "bottleneck": bottleneck,
    })


def monthly_stats(data: Optional[Dict[str, Any]] = None) -> None:
    """生成月度统计数据。

    统计指定月份的新增客户、成交客户、跟进活动等数据。

    Args:
        data: 可选参数，包含 month（格式 YYYY-MM）。
    """
    customers = _get_customers()
    followups = _get_followups()

    # 确定统计月份
    if data and data.get("month"):
        month_str = data["month"]
    else:
        month_str = today_str()[:7]

    year, month = map(int, month_str.split("-"))

    # 本月新增客户
    new_customers = [
        c for c in customers
        if c.get("created_at", "").startswith(month_str)
    ]

    # 本月成交客户
    won_customers = [
        c for c in customers
        if c.get("stage") == "成交" and c.get("updated_at", "").startswith(month_str)
    ]

    # 本月流失客户
    lost_customers = [
        c for c in customers
        if c.get("stage") == "流失" and c.get("updated_at", "").startswith(month_str)
    ]

    # 本月跟进次数
    month_followups = [
        f for f in followups
        if f.get("date", "").startswith(month_str)
    ]

    # 成交金额
    won_budget = sum(float(c.get("budget", 0)) for c in won_customers)

    # 活跃客户（本月有跟进记录的独立客户数）
    active_customer_ids = {f.get("customer_id") for f in month_followups}

    result = {
        "month": month_str,
        "new_customers": len(new_customers),
        "won_deals": len(won_customers),
        "lost_deals": len(lost_customers),
        "won_revenue": won_budget,
        "won_revenue_display": format_currency(won_budget),
        "total_followups": len(month_followups),
        "active_customers": len(active_customer_ids),
        "total_customers": len(customers),
        "win_rate": f"{len(won_customers) / len(new_customers) * 100:.1f}%" if new_customers else "N/A",
    }

    output_success(result)


def generate_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成综合销售分析报告。

    整合漏斗分析、月度统计、客户分布等信息。

    Args:
        data: 可选参数。
    """
    customers = _get_customers()
    followups = _get_followups()

    if not customers:
        output_error("暂无客户数据，无法生成报告", code="NO_DATA")
        return

    sub = check_subscription()
    today = today_str()
    month_str = today[:7]

    # 基础统计
    stage_counts = Counter(c.get("stage", "未知") for c in customers)
    source_counts = Counter(c.get("source", "未知") for c in customers if c.get("source"))
    total_budget = sum(float(c.get("budget", 0)) for c in customers)
    won_budget = sum(float(c.get("budget", 0)) for c in customers if c.get("stage") == "成交")

    # 本月数据
    month_new = sum(1 for c in customers if c.get("created_at", "").startswith(month_str))
    month_won = sum(1 for c in customers if c.get("stage") == "成交" and c.get("updated_at", "").startswith(month_str))
    month_followups = sum(1 for f in followups if f.get("date", "").startswith(month_str))

    report = {
        "report_date": today,
        "summary": {
            "total_customers": len(customers),
            "total_pipeline_budget": format_currency(total_budget),
            "total_won_revenue": format_currency(won_budget),
            "month_new_customers": month_new,
            "month_won_deals": month_won,
            "month_followup_count": month_followups,
        },
        "stage_distribution": {stage: stage_counts.get(stage, 0) for stage in STAGES},
        "source_distribution": dict(source_counts),
    }

    # 付费版：添加 Mermaid 图表
    if "mermaid_chart" in sub["features"]:
        # 阶段分布饼图
        pie_data = {stage: stage_counts.get(stage, 0) for stage in STAGES if stage_counts.get(stage, 0) > 0}
        report["mermaid_stage_chart"] = _generate_pie_mermaid("客户阶段分布", pie_data)

        # 来源分布饼图
        if source_counts:
            report["mermaid_source_chart"] = _generate_pie_mermaid("客户来源分布", dict(source_counts))

    output_success(report)


# ============================================================
# Mermaid 图表生成
# ============================================================

def _generate_funnel_mermaid(stage_data: List[Dict]) -> str:
    """生成漏斗 Mermaid 图表。"""
    lines = ["```mermaid", "graph LR"]
    for i, s in enumerate(stage_data):
        node_id = f"S{i}"
        label = f"{s['stage']}<br/>{s['count']}个客户<br/>{s['budget_display']}"
        lines.append(f"    {node_id}[\"{label}\"]")
        if i > 0:
            prev_count = stage_data[i - 1]["count"]
            rate = (s["count"] / prev_count * 100) if prev_count > 0 else 0
            lines.append(f"    S{i-1} -->|{rate:.0f}%| {node_id}")
    lines.append("```")
    return "\n".join(lines)


def _generate_pie_mermaid(title: str, data: Dict[str, int]) -> str:
    """生成饼图 Mermaid 图表。"""
    lines = ["```mermaid", f"pie title {title}"]
    for label, value in data.items():
        lines.append(f'    "{label}" : {value}')
    lines.append("```")
    return "\n".join(lines)


# ============================================================
# 瓶颈建议
# ============================================================

def _get_bottleneck_suggestion(from_stage: str, to_stage: str) -> str:
    """根据转化瓶颈位置给出优化建议。"""
    suggestions = {
        ("初步接触", "需求确认"): "建议加强初次接触后的需求挖掘，提前准备行业案例和产品演示材料",
        ("需求确认", "方案报价"): "建议缩短方案制作周期，提供标准化方案模板，加速报价流程",
        ("方案报价", "谈判"): "建议优化报价策略，提供灵活的套餐选择，及时跟进客户反馈",
        ("谈判", "成交"): "建议加强谈判技巧，了解客户决策链，提供限时优惠促进签约",
    }
    return suggestions.get((from_stage, to_stage), "建议增加跟进频率，深入了解客户需求")


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("customer-pulse 销售漏斗分析")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "funnel": lambda: analyze_funnel(data),
        "conversion": lambda: analyze_conversion(data),
        "monthly_stats": lambda: monthly_stats(data),
        "report": lambda: generate_report(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
