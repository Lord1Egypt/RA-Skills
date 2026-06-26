#!/usr/bin/env python3
"""
biz-data-insight 报告生成器

从结构化数据生成 Markdown + Mermaid 格式的业务分析报告。
支持日报、周报、月报和交互问答四种模板。

用法:
    python3 report_generator.py --template daily --data '{"metrics":[...]}'
    python3 report_generator.py --template weekly --data-file ./query_results.json
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from utils import (
    format_number,
    format_percentage,
    format_chinese_unit,
    output_success,
    output_error,
    check_subscription,
)


# ============================================================
# Mermaid 图表生成
# ============================================================

def generate_pie_chart(title: str, data: List[Dict[str, Any]]) -> str:
    """生成 Mermaid 饼图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。

    Returns:
        Mermaid 饼图代码块字符串。
    """
    lines = [f'```mermaid', f'pie title {title}']
    for item in data:
        label = item.get("label", "未知")
        value = item.get("value", 0)
        lines.append(f'    "{label}" : {value}')
    lines.append("```")
    return "\n".join(lines)


def generate_line_chart(
    title: str,
    data: List[Dict[str, Any]],
    x_label: str = "时间",
    y_label: str = "数值",
) -> str:
    """生成 Mermaid xychart-beta 折线图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。
        x_label: X 轴标签。
        y_label: Y 轴标签。

    Returns:
        Mermaid 折线图代码块字符串。
    """
    labels = [f'"{item.get("label", "")}"' for item in data]
    values = [str(item.get("value", 0)) for item in data]

    lines = [
        "```mermaid",
        "xychart-beta",
        f'    title "{title}"',
        f'    x-axis [{", ".join(labels)}]',
        f'    y-axis "{y_label}"',
        f'    line [{", ".join(values)}]',
        "```",
    ]
    return "\n".join(lines)


def generate_bar_chart(
    title: str,
    data: List[Dict[str, Any]],
    x_label: str = "类别",
    y_label: str = "数值",
) -> str:
    """生成 Mermaid xychart-beta 柱状图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。
        x_label: X 轴标签。
        y_label: Y 轴标签。

    Returns:
        Mermaid 柱状图代码块字符串。
    """
    labels = [f'"{item.get("label", "")}"' for item in data]
    values = [str(item.get("value", 0)) for item in data]

    lines = [
        "```mermaid",
        "xychart-beta",
        f'    title "{title}"',
        f'    x-axis [{", ".join(labels)}]',
        f'    y-axis "{y_label}"',
        f'    bar [{", ".join(values)}]',
        "```",
    ]
    return "\n".join(lines)


# ============================================================
# 指标分析辅助函数
# ============================================================

def _calc_change(current: float, previous: float) -> Optional[float]:
    """计算环比变化率。

    Args:
        current: 当前值。
        previous: 上一期值。

    Returns:
        变化率（小数形式），previous 为 0 时返回 None。
    """
    if previous == 0:
        return None
    return (current - previous) / previous


def _describe_change(current: float, previous: float) -> str:
    """描述指标环比变化。

    Args:
        current: 当前值。
        previous: 上一期值。

    Returns:
        环比变化描述文本，如 "环比增长5.9%" 或 "环比下降3.0%"。
    """
    change = _calc_change(current, previous)
    if change is None:
        return "无可比数据"
    abs_change = abs(change)
    pct_str = format_percentage(abs_change)
    if change > 0:
        return f"环比增长{pct_str}"
    elif change < 0:
        return f"环比下降{pct_str}"
    else:
        return "环比持平"


def _build_metrics_table(metrics: List[Dict[str, Any]]) -> str:
    """生成核心指标 Markdown 表格。

    Args:
        metrics: 指标列表。

    Returns:
        Markdown 表格字符串。
    """
    lines = [
        "| 指标 | 当前值 | 上期值 | 环比变化 |",
        "|------|--------|--------|----------|",
    ]
    for m in metrics:
        name = m.get("name", "未知")
        value = m.get("value", 0)
        previous = m.get("previous")
        unit = m.get("unit", "")

        formatted_value = f"{format_chinese_unit(value)}{unit}"
        if previous is not None:
            formatted_prev = f"{format_chinese_unit(previous)}{unit}"
            change_desc = _describe_change(value, previous)
        else:
            formatted_prev = "-"
            change_desc = "-"

        lines.append(f"| {name} | {formatted_value} | {formatted_prev} | {change_desc} |")

    return "\n".join(lines)


def _build_anomaly_section(anomalies: List[Dict[str, Any]]) -> str:
    """生成异常告警章节。

    Args:
        anomalies: 异常列表。

    Returns:
        Markdown 异常告警内容。
    """
    if not anomalies:
        return ""

    lines = ["## 异常告警\n"]
    for a in anomalies:
        metric = a.get("metric", "未知指标")
        value = a.get("value", 0)
        threshold = a.get("threshold", 0)
        severity = a.get("severity", "info")
        description = a.get("description", "")

        severity_icon = "⚠️" if severity == "warning" else "🔴" if severity == "critical" else "ℹ️"
        lines.append(
            f"- {severity_icon} **{metric}**: 当前值 {value}，阈值 {threshold}。{description}"
        )

    return "\n".join(lines)


def _build_dimension_section(
    dimensions: List[Dict[str, Any]],
    is_paid: bool,
) -> str:
    """生成维度分析章节（含可选图表）。

    Args:
        dimensions: 维度列表。
        is_paid: 是否为付费用户。

    Returns:
        Markdown 维度分析内容（付费用户含 Mermaid 图表）。
    """
    if not dimensions:
        return ""

    charts_parts: List[str] = []

    for dim in dimensions:
        name = dim.get("name", "未知维度")
        dim_type = dim.get("type", "")
        data = dim.get("data", [])

        charts_parts.append(f"### {name}\n")

        # 数据表格
        charts_parts.append("| 项目 | 数值 |")
        charts_parts.append("|------|------|")
        for item in data:
            label = item.get("label", "")
            value = item.get("value", 0)
            charts_parts.append(f"| {label} | {format_chinese_unit(value)} |")
        charts_parts.append("")

        # 付费用户生成图表
        if is_paid and data:
            if dim_type == "distribution":
                charts_parts.append(generate_pie_chart(name, data))
            elif dim_type == "trend":
                charts_parts.append(generate_line_chart(name, data, x_label="时间", y_label="数值"))
            elif dim_type == "ranking":
                charts_parts.append(generate_bar_chart(name, data, x_label="项目", y_label="数值"))
            charts_parts.append("")

    return "\n".join(charts_parts)


# ============================================================
# 报告模板
# ============================================================

def _render_daily(
    data: Dict[str, Any],
    title: Optional[str],
    is_paid: bool,
) -> str:
    """渲染日报模板。

    Args:
        data: 报告数据。
        title: 可选标题覆盖。
        is_paid: 是否为付费用户。

    Returns:
        完整的 Markdown 日报内容。
    """
    period = data.get("period", "未知日期")
    header = title or f"📊 {period} 业务日报"
    metrics = data.get("metrics", [])
    dimensions = data.get("dimensions", [])

    parts: List[str] = [f"# {header}\n"]

    # 核心指标
    parts.append("## 核心指标\n")
    parts.append(_build_metrics_table(metrics))
    parts.append("")

    # 指标洞察
    parts.append("## 指标洞察\n")
    for m in metrics:
        name = m.get("name", "")
        value = m.get("value", 0)
        previous = m.get("previous")
        unit = m.get("unit", "")
        if previous is not None:
            change_desc = _describe_change(value, previous)
            parts.append(f"- **{name}**: {format_chinese_unit(value)}{unit}，{change_desc}")
        else:
            parts.append(f"- **{name}**: {format_chinese_unit(value)}{unit}")
    parts.append("")

    # 维度分析
    if dimensions:
        parts.append("## 维度分析\n")
        parts.append(_build_dimension_section(dimensions, is_paid))

    return "\n".join(parts)


def _render_weekly(
    data: Dict[str, Any],
    title: Optional[str],
    is_paid: bool,
) -> str:
    """渲染周报模板。

    Args:
        data: 报告数据。
        title: 可选标题覆盖。
        is_paid: 是否为付费用户。

    Returns:
        完整的 Markdown 周报内容。
    """
    period = data.get("period", "未知周期")
    header = title or f"📊 {period} 业务周报"
    metrics = data.get("metrics", [])
    dimensions = data.get("dimensions", [])
    anomalies = data.get("anomalies", [])

    parts: List[str] = [f"# {header}\n"]

    # 本周概览
    parts.append("## 本周概览\n")
    parts.append(_build_metrics_table(metrics))
    parts.append("")

    # 指标周环比分析
    parts.append("## 周环比分析\n")
    for m in metrics:
        name = m.get("name", "")
        value = m.get("value", 0)
        previous = m.get("previous")
        unit = m.get("unit", "")
        if previous is not None:
            change_desc = _describe_change(value, previous)
            parts.append(f"- **{name}**: {format_chinese_unit(value)}{unit}，{change_desc}")
        else:
            parts.append(f"- **{name}**: {format_chinese_unit(value)}{unit}")
    parts.append("")

    # 维度明细
    if dimensions:
        parts.append("## 维度明细\n")
        parts.append(_build_dimension_section(dimensions, is_paid))

    # 异常告警（仅付费用户）
    if is_paid and anomalies:
        parts.append(_build_anomaly_section(anomalies))
        parts.append("")

    return "\n".join(parts)


def _render_monthly(
    data: Dict[str, Any],
    title: Optional[str],
    is_paid: bool,
) -> str:
    """渲染月报模板（仅付费用户可用）。

    Args:
        data: 报告数据。
        title: 可选标题覆盖。
        is_paid: 是否为付费用户。

    Returns:
        完整的 Markdown 月报内容。

    Raises:
        PermissionError: 当免费用户尝试生成月报时抛出。
    """
    if not is_paid:
        raise PermissionError("月报功能仅限付费用户使用，请升级订阅。")

    period = data.get("period", "未知月份")
    header = title or f"📊 {period} 业务月报"
    metrics = data.get("metrics", [])
    dimensions = data.get("dimensions", [])
    anomalies = data.get("anomalies", [])

    parts: List[str] = [f"# {header}\n"]

    # 执行摘要
    parts.append("## 执行摘要\n")
    summary_items: List[str] = []
    for m in metrics:
        name = m.get("name", "")
        value = m.get("value", 0)
        previous = m.get("previous")
        unit = m.get("unit", "")
        if previous is not None:
            change_desc = _describe_change(value, previous)
            summary_items.append(f"{name}{format_chinese_unit(value)}{unit}（{change_desc}）")
        else:
            summary_items.append(f"{name}{format_chinese_unit(value)}{unit}")
    parts.append(f"本月关键指标：{'；'.join(summary_items)}。\n")

    # 核心指标趋势
    parts.append("## 核心指标\n")
    parts.append(_build_metrics_table(metrics))
    parts.append("")

    # 为每个指标生成趋势说明
    parts.append("## 指标趋势分析\n")
    for m in metrics:
        name = m.get("name", "")
        value = m.get("value", 0)
        previous = m.get("previous")
        unit = m.get("unit", "")
        if previous is not None:
            change = _calc_change(value, previous)
            change_desc = _describe_change(value, previous)
            if change is not None and change > 0:
                parts.append(f"- **{name}**：本月录得 {format_chinese_unit(value)}{unit}，{change_desc}，呈上升趋势。")
            elif change is not None and change < 0:
                parts.append(f"- **{name}**：本月录得 {format_chinese_unit(value)}{unit}，{change_desc}，需关注下降原因。")
            else:
                parts.append(f"- **{name}**：本月录得 {format_chinese_unit(value)}{unit}，与上期持平。")
        else:
            parts.append(f"- **{name}**：本月录得 {format_chinese_unit(value)}{unit}。")
    parts.append("")

    # 维度深度分析
    if dimensions:
        parts.append("## 维度深度分析\n")
        parts.append(_build_dimension_section(dimensions, is_paid))

    # 异常分析
    if anomalies:
        parts.append("## 异常分析\n")
        for a in anomalies:
            metric = a.get("metric", "未知指标")
            value = a.get("value", 0)
            threshold = a.get("threshold", 0)
            severity = a.get("severity", "info")
            description = a.get("description", "")

            severity_label = "警告" if severity == "warning" else "严重" if severity == "critical" else "提示"
            parts.append(f"### {metric}（{severity_label}）\n")
            parts.append(f"- 当前值：{value}")
            parts.append(f"- 阈值：{threshold}")
            parts.append(f"- 说明：{description}")
            parts.append(f"- 建议：请排查{metric}异常原因，及时采取纠正措施。\n")

    # 建议
    parts.append("## 改进建议\n")
    recommendation_idx = 1
    for m in metrics:
        name = m.get("name", "")
        value = m.get("value", 0)
        previous = m.get("previous")
        if previous is not None:
            change = _calc_change(value, previous)
            if change is not None and change < 0:
                parts.append(f"{recommendation_idx}. **{name}**出现下降，建议分析下降原因并制定改善方案。")
                recommendation_idx += 1
            elif change is not None and change > 0:
                parts.append(f"{recommendation_idx}. **{name}**保持增长，建议总结成功经验并推广。")
                recommendation_idx += 1
    if anomalies:
        for a in anomalies:
            metric = a.get("metric", "")
            parts.append(f"{recommendation_idx}. 重点关注**{metric}**异常，建立预警和快速响应机制。")
            recommendation_idx += 1
    if recommendation_idx == 1:
        parts.append("各项指标表现稳定，建议持续监控。")
    parts.append("")

    return "\n".join(parts)


def _render_interactive(
    data: Dict[str, Any],
    title: Optional[str],
    is_paid: bool,
) -> str:
    """渲染交互问答模板。

    Args:
        data: 报告数据。
        title: 可选标题覆盖。
        is_paid: 是否为付费用户。

    Returns:
        简洁的 Markdown 回答内容。
    """
    header = title or "📊 数据查询结果"
    metrics = data.get("metrics", [])
    dimensions = data.get("dimensions", [])

    parts: List[str] = [f"# {header}\n"]

    # 数据表格
    if metrics:
        parts.append("## 数据概览\n")
        parts.append(_build_metrics_table(metrics))
        parts.append("")

    # 维度数据
    if dimensions:
        for dim in dimensions:
            name = dim.get("name", "")
            dim_type = dim.get("type", "")
            dim_data = dim.get("data", [])

            parts.append(f"## {name}\n")
            parts.append("| 项目 | 数值 |")
            parts.append("|------|------|")
            for item in dim_data:
                label = item.get("label", "")
                value = item.get("value", 0)
                parts.append(f"| {label} | {format_chinese_unit(value)} |")
            parts.append("")

            # 付费用户生成图表
            if is_paid and dim_data:
                if dim_type == "distribution":
                    parts.append(generate_pie_chart(name, dim_data))
                elif dim_type == "trend":
                    parts.append(generate_line_chart(name, dim_data))
                elif dim_type == "ranking":
                    parts.append(generate_bar_chart(name, dim_data))
                parts.append("")

    # 简要洞察
    parts.append("## 简要洞察\n")
    insights: List[str] = []
    for m in metrics:
        name = m.get("name", "")
        value = m.get("value", 0)
        previous = m.get("previous")
        unit = m.get("unit", "")
        if previous is not None:
            change_desc = _describe_change(value, previous)
            insights.append(f"{name}为{format_chinese_unit(value)}{unit}，{change_desc}")
        else:
            insights.append(f"{name}为{format_chinese_unit(value)}{unit}")
    if insights:
        parts.append("；".join(insights) + "。")
    else:
        parts.append("暂无指标数据。")
    parts.append("")

    return "\n".join(parts)


# ============================================================
# 模板路由
# ============================================================

_TEMPLATE_RENDERERS = {
    "daily": _render_daily,
    "weekly": _render_weekly,
    "monthly": _render_monthly,
    "interactive": _render_interactive,
}


def _count_charts(report: str) -> int:
    """统计报告中 Mermaid 图表的数量。

    Args:
        report: Markdown 报告内容。

    Returns:
        图表数量。
    """
    return report.count("```mermaid")


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """CLI 主入口：解析参数、加载数据、生成报告并输出。"""
    parser = argparse.ArgumentParser(
        description="biz-data-insight 报告生成器 — 生成 Markdown + Mermaid 业务报告",
    )
    parser.add_argument(
        "--template",
        required=True,
        choices=["daily", "weekly", "monthly", "interactive"],
        help="报告模板类型：daily（日报）、weekly（周报）、monthly（月报）、interactive（交互问答）",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 字符串格式的报告数据",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="报告数据 JSON 文件路径（与 --data 二选一）",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="可选的报告标题覆盖",
    )
    parser.add_argument(
        "--tier",
        default=None,
        choices=["free", "paid"],
        help="订阅等级覆盖（free 或 paid）",
    )

    args = parser.parse_args()

    # ----------------------------------------------------------
    # 加载数据
    # ----------------------------------------------------------
    if args.data and args.data_file:
        output_error("--data 和 --data-file 不能同时使用，请选择其一。", code="INVALID_ARGS")
        sys.exit(1)

    if not args.data and not args.data_file:
        output_error("请提供 --data 或 --data-file 参数。", code="MISSING_DATA")
        sys.exit(1)

    try:
        if args.data:
            report_data: Dict[str, Any] = json.loads(args.data)
        else:
            with open(args.data_file, "r", encoding="utf-8") as f:
                report_data = json.load(f)
    except json.JSONDecodeError as e:
        output_error(f"JSON 解析失败: {e}", code="JSON_ERROR")
        sys.exit(1)
    except FileNotFoundError:
        output_error(f"数据文件不存在: {args.data_file}", code="FILE_NOT_FOUND")
        sys.exit(1)
    except Exception as e:
        output_error(f"读取数据失败: {e}", code="DATA_ERROR")
        sys.exit(1)

    if not isinstance(report_data, dict):
        output_error("数据格式错误，期望 JSON 对象。", code="INVALID_DATA")
        sys.exit(1)

    # ----------------------------------------------------------
    # 检查订阅
    # ----------------------------------------------------------
    try:
        subscription = check_subscription(args.tier)
    except ValueError as e:
        output_error(str(e), code="SUBSCRIPTION_ERROR")
        sys.exit(1)

    is_paid = subscription["tier"] == "paid"

    # ----------------------------------------------------------
    # 渲染报告
    # ----------------------------------------------------------
    renderer = _TEMPLATE_RENDERERS.get(args.template)
    if renderer is None:
        output_error(f"未知模板类型: {args.template}", code="UNKNOWN_TEMPLATE")
        sys.exit(1)

    try:
        report_md = renderer(report_data, args.title, is_paid)
    except PermissionError as e:
        output_error(str(e), code="PERMISSION_DENIED")
        sys.exit(1)
    except Exception as e:
        output_error(f"报告生成失败: {e}", code="RENDER_ERROR")
        sys.exit(1)

    # ----------------------------------------------------------
    # 输出结果
    # ----------------------------------------------------------
    charts_count = _count_charts(report_md)
    output_success({
        "report": report_md,
        "template": args.template,
        "charts_count": charts_count,
    })


if __name__ == "__main__":
    main()
