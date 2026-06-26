#!/usr/bin/env python3
"""
deal-closer 销售漏斗与管道报告模块

提供销售漏斗分析、收入预测、周报/月报生成等功能。
支持 Mermaid 图表（付费功能）和风险预警。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from utils import (
    check_subscription,
    get_data_file,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    format_currency,
    format_percentage,
    calculate_days_since,
    DEAL_STAGES,
    STAGE_COLORS,
    STAGE_DEFAULT_PROBABILITY,
)

# 延迟导入学习引擎
_learning_module = None


def _get_learning_module():
    """延迟加载 learning_engine 模块。"""
    global _learning_module
    if _learning_module is None:
        try:
            import learning_engine as _mod
            _learning_module = _mod
        except ImportError:
            _learning_module = False
    return _learning_module if _learning_module is not False else None


def _get_ai_predictions(deals: List[Dict[str, Any]]) -> Dict[str, float]:
    """获取所有活跃商机的AI预测胜率。

    Args:
        deals: 商机列表。

    Returns:
        商机ID到AI预测胜率的映射。
    """
    learning_mod = _get_learning_module()
    if learning_mod is None:
        return {}

    try:
        learning_data = learning_mod._get_learning_data()
        predictions = {}
        for deal in deals:
            if deal.get("stage") in ("成交", "流失"):
                continue
            features = learning_mod._extract_deal_features(deal)
            scores = learning_mod._calculate_feature_scores(features, learning_data)
            probability = learning_mod._compute_win_probability(scores)
            predictions[deal.get("id", "")] = probability
        return predictions
    except Exception:
        return {}


def _get_coaching_tips() -> List[Dict[str, str]]:
    """获取销售教练建议。

    Returns:
        教练建议列表。
    """
    learning_mod = _get_learning_module()
    if learning_mod is None:
        return []

    try:
        deals = read_json_file(get_data_file(DEALS_FILE))
        learning_data = learning_mod._get_learning_data()
        return learning_mod._generate_coaching_tips(learning_data, deals)
    except Exception:
        return []


def _calculate_pipeline_health(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """计算管道健康评分。

    基于商机年龄与历史平均周期的比较。

    Args:
        deals: 商机列表。

    Returns:
        健康评分数据。
    """
    learning_mod = _get_learning_module()

    active_deals = [
        d for d in deals if d.get("stage") not in ("成交", "流失")
    ]

    if not active_deals:
        return {"score": 0, "level": "无数据", "details": []}

    # 基准周期天数（按阶段）
    stage_benchmarks = {
        "线索": 7, "初步接触": 10, "需求确认": 14,
        "方案报价": 10, "商务谈判": 14, "合同签署": 7,
    }

    # 如果有学习数据，用历史数据覆盖基准
    if learning_mod:
        try:
            learning_data = learning_mod._get_learning_data()
            won_outcomes = [
                o for o in learning_data.get("outcomes", [])
                if o.get("result") == "won"
            ]
            if won_outcomes:
                for stage in stage_benchmarks:
                    durations = []
                    for o in won_outcomes:
                        sd = o.get("stage_durations", {})
                        if stage in sd:
                            durations.append(sd[stage])
                    if durations:
                        stage_benchmarks[stage] = int(
                            sum(durations) / len(durations)
                        )
        except Exception:
            pass

    health_scores = []
    details = []

    for deal in active_deals:
        stage = deal.get("stage", "")
        updated = deal.get("updated_at", "")
        days_since = calculate_days_since(updated) if updated else 0
        benchmark = stage_benchmarks.get(stage, 10)

        if days_since <= benchmark:
            score = 100
        elif days_since <= benchmark * 2:
            score = max(50, 100 - (days_since - benchmark) * 5)
        else:
            score = max(10, 50 - (days_since - benchmark * 2) * 3)

        health_scores.append(score)
        if score < 60:
            details.append({
                "deal_name": deal.get("name", ""),
                "stage": stage,
                "days_since_update": days_since,
                "benchmark_days": benchmark,
                "health_score": score,
            })

    avg_score = sum(health_scores) / len(health_scores) if health_scores else 0
    avg_score = round(avg_score, 1)

    if avg_score >= 80:
        level = "健康"
    elif avg_score >= 60:
        level = "一般"
    elif avg_score >= 40:
        level = "需关注"
    else:
        level = "危险"

    return {
        "score": avg_score,
        "level": level,
        "total_deals": len(active_deals),
        "at_risk_count": len(details),
        "at_risk_deals": sorted(details, key=lambda d: d["health_score"])[:5],
    }


# ============================================================
# 数据文件
# ============================================================

DEALS_FILE = "deals.json"
MEETINGS_FILE = "meetings.json"


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


def _get_meetings() -> List[Dict[str, Any]]:
    """读取所有会议记录。"""
    return read_json_file(get_data_file(MEETINGS_FILE))


# ============================================================
# Mermaid 图表生成
# ============================================================

def _generate_pie_chart(title: str, data: List[Dict[str, Any]]) -> str:
    """生成 Mermaid 饼图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。

    Returns:
        Mermaid 饼图代码块字符串。
    """
    lines = ["```mermaid", f"pie title {title}"]
    for item in data:
        label = item.get("label", "未知")
        value = item.get("value", 0)
        if value > 0:
            lines.append(f'    "{label}" : {value}')
    lines.append("```")
    return "\n".join(lines)


def _generate_bar_chart(title: str, data: List[Dict[str, Any]], y_label: str = "金额") -> str:
    """生成 Mermaid 柱状图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。
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


def _generate_line_chart(title: str, data: List[Dict[str, Any]], y_label: str = "数值") -> str:
    """生成 Mermaid 折线图。

    Args:
        title: 图表标题。
        data: 数据列表，每项包含 label 和 value。
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


# ============================================================
# 分析函数
# ============================================================

def _calculate_conversion_rates(deals: List[Dict]) -> List[Dict[str, Any]]:
    """计算各阶段转化率。

    Args:
        deals: 商机列表。

    Returns:
        各阶段转化率数据列表。
    """
    stage_counts = {}
    for stage in DEAL_STAGES:
        stage_counts[stage] = sum(1 for d in deals if d.get("stage") == stage)

    conversions = []
    # 排除 "流失" 计算正向转化
    active_stages = [s for s in DEAL_STAGES if s != "流失"]

    for i in range(len(active_stages) - 1):
        current = active_stages[i]
        next_stage = active_stages[i + 1]
        current_count = stage_counts.get(current, 0)
        next_count = stage_counts.get(next_stage, 0)

        # 累计到达该阶段的商机数（当前 + 后续所有阶段）
        total_at_or_past = sum(
            stage_counts.get(s, 0)
            for s in active_stages[active_stages.index(current):]
        )
        total_past = sum(
            stage_counts.get(s, 0)
            for s in active_stages[active_stages.index(next_stage):]
        )

        rate = total_past / total_at_or_past if total_at_or_past > 0 else 0.0

        conversions.append({
            "from_stage": current,
            "to_stage": next_stage,
            "from_count": total_at_or_past,
            "to_count": total_past,
            "conversion_rate": round(rate, 4),
        })

    return conversions


def _detect_risk_deals(deals: List[Dict], stale_days: int = 14) -> List[Dict[str, Any]]:
    """检测风险商机。

    识别长时间未更新和高价值风险商机。

    Args:
        deals: 商机列表。
        stale_days: 停滞天数阈值。

    Returns:
        风险商机列表。
    """
    risks = []
    for deal in deals:
        stage = deal.get("stage", "")
        if stage in ("成交", "流失"):
            continue

        updated_at = deal.get("updated_at", "")
        days_since = calculate_days_since(updated_at) if updated_at else 0

        risk_reasons = []

        # 停滞风险
        if days_since >= stale_days:
            risk_reasons.append(f"已 {days_since} 天未更新")

        # 超期风险
        expected = deal.get("expected_close_date", "")
        if expected:
            try:
                exp_date = datetime.strptime(expected, "%Y-%m-%d")
                if exp_date < datetime.now():
                    overdue_days = (datetime.now() - exp_date).days
                    risk_reasons.append(f"已超出预计成交日期 {overdue_days} 天")
            except ValueError:
                pass

        # 高金额低概率
        amount = deal.get("amount", 0)
        probability = deal.get("probability", 0)
        if amount >= 100000 and probability <= 30:
            risk_reasons.append("高金额低概率")

        if risk_reasons:
            risks.append({
                "deal_id": deal.get("id", ""),
                "deal_name": deal.get("name", ""),
                "stage": stage,
                "amount": amount,
                "amount_display": format_currency(amount),
                "probability": probability,
                "days_since_update": days_since,
                "risk_reasons": risk_reasons,
            })

    # 按金额降序排序
    risks.sort(key=lambda r: r.get("amount", 0), reverse=True)
    return risks


# ============================================================
# 报告操作
# ============================================================

def funnel_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成销售漏斗报告。

    展示各阶段商机数量、金额和转化率。

    Args:
        data: 可选参数。
    """
    deals = _get_deals()
    if not deals:
        output_error("暂无商机数据", code="NO_DATA")
        return

    sub = check_subscription()
    is_paid = sub["tier"] == "paid"

    # 各阶段统计
    stage_data = []
    for stage in DEAL_STAGES:
        stage_deals = [d for d in deals if d.get("stage") == stage]
        total_amount = sum(d.get("amount", 0) for d in stage_deals)
        stage_data.append({
            "stage": stage,
            "count": len(stage_deals),
            "total_amount": total_amount,
            "total_amount_display": format_currency(total_amount),
        })

    # 转化率
    conversions = _calculate_conversion_rates(deals)

    # 风险商机
    risks = _detect_risk_deals(deals)

    result = {
        "total_deals": len(deals),
        "total_amount": sum(d.get("amount", 0) for d in deals),
        "total_amount_display": format_currency(sum(d.get("amount", 0) for d in deals)),
        "stages": stage_data,
        "conversions": conversions,
        "risk_deals": risks[:10],
        "risk_count": len(risks),
    }

    # 付费用户生成 Mermaid 图表
    if is_paid:
        # 饼图：阶段分布
        pie_data = [
            {"label": s["stage"], "value": s["count"]}
            for s in stage_data if s["count"] > 0
        ]
        result["mermaid_pie"] = _generate_pie_chart("商机阶段分布", pie_data)

        # 柱状图：各阶段金额
        bar_data = [
            {"label": s["stage"], "value": int(s["total_amount"] / 10000)}
            for s in stage_data
        ]
        result["mermaid_bar"] = _generate_bar_chart("各阶段金额（万元）", bar_data, y_label="万元")

    output_success(result)


def forecast_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成收入预测报告。

    根据管道金额乘以成交概率计算加权预测。

    Args:
        data: 可选参数，支持 period（月/季度）。
    """
    if not require_paid_feature("forecast", "收入预测"):
        return

    deals = _get_deals()
    if not deals:
        output_error("暂无商机数据", code="NO_DATA")
        return

    data = data or {}
    stale_days = data.get("stale_days", 14)

    # 排除已成交和已流失
    active_deals = [
        d for d in deals
        if d.get("stage") not in ("成交", "流失")
    ]

    # 加权预测
    weighted_total = 0.0
    stage_forecast = {}
    forecast_details = []

    for deal in active_deals:
        amount = deal.get("amount", 0)
        probability = deal.get("probability", 0) / 100.0
        weighted = amount * probability

        stage = deal.get("stage", "")
        if stage not in stage_forecast:
            stage_forecast[stage] = {"count": 0, "raw_amount": 0, "weighted_amount": 0}

        stage_forecast[stage]["count"] += 1
        stage_forecast[stage]["raw_amount"] += amount
        stage_forecast[stage]["weighted_amount"] += weighted
        weighted_total += weighted

        forecast_details.append({
            "deal_id": deal.get("id", ""),
            "deal_name": deal.get("name", ""),
            "stage": stage,
            "amount": amount,
            "amount_display": format_currency(amount),
            "probability": deal.get("probability", 0),
            "weighted_amount": round(weighted, 2),
            "weighted_display": format_currency(weighted),
            "expected_close_date": deal.get("expected_close_date", ""),
            "ai_probability": None,  # 占位，稍后填充
        })

    # 填充 AI 预测胜率
    ai_predictions = _get_ai_predictions(active_deals)
    for fd in forecast_details:
        did = fd.get("deal_id", "")
        if did in ai_predictions:
            fd["ai_probability"] = ai_predictions[did]

    # 按加权金额排序
    forecast_details.sort(key=lambda x: x["weighted_amount"], reverse=True)

    # 格式化阶段预测
    stage_forecast_display = []
    for stage in DEAL_STAGES:
        if stage in stage_forecast:
            sf = stage_forecast[stage]
            stage_forecast_display.append({
                "stage": stage,
                "count": sf["count"],
                "raw_amount": sf["raw_amount"],
                "raw_amount_display": format_currency(sf["raw_amount"]),
                "weighted_amount": round(sf["weighted_amount"], 2),
                "weighted_display": format_currency(sf["weighted_amount"]),
            })

    # 已成交金额
    won_deals = [d for d in deals if d.get("stage") == "成交"]
    won_amount = sum(d.get("amount", 0) for d in won_deals)

    # 管道健康评分
    pipeline_health = _calculate_pipeline_health(deals)

    # 教练建议
    coaching_tips = _get_coaching_tips()

    result = {
        "forecast_total": round(weighted_total, 2),
        "forecast_display": format_currency(weighted_total),
        "active_deals": len(active_deals),
        "raw_pipeline": sum(d.get("amount", 0) for d in active_deals),
        "raw_pipeline_display": format_currency(sum(d.get("amount", 0) for d in active_deals)),
        "won_amount": won_amount,
        "won_amount_display": format_currency(won_amount),
        "won_deals": len(won_deals),
        "stage_forecast": stage_forecast_display,
        "top_deals": forecast_details[:10],
        "pipeline_health": pipeline_health,
        "coaching_tips": coaching_tips[:3],
    }

    # Mermaid 图表
    bar_data = [
        {"label": sf["stage"], "value": int(sf["weighted_amount"] / 10000)}
        for sf in stage_forecast_display
    ]
    result["mermaid_forecast"] = _generate_bar_chart(
        "各阶段加权预测（万元）", bar_data, y_label="万元"
    )

    output_success(result)


def monthly_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成月度销售报告。

    Args:
        data: 可选参数，支持 month（YYYY-MM）。
    """
    if not require_paid_feature("advanced_analytics", "月度报告"):
        return

    deals = _get_deals()
    if not deals:
        output_error("暂无商机数据", code="NO_DATA")
        return

    data = data or {}
    target_month = data.get("month", datetime.now().strftime("%Y-%m"))

    # 本月新增
    new_deals = [
        d for d in deals
        if d.get("created_at", "").startswith(target_month)
    ]

    # 本月成交
    won_deals = []
    for d in deals:
        if d.get("stage") != "成交":
            continue
        history = d.get("stage_history", [])
        for h in history:
            if h.get("stage") == "成交" and h.get("timestamp", "").startswith(target_month):
                won_deals.append(d)
                break

    # 本月流失
    lost_deals = []
    for d in deals:
        if d.get("stage") != "流失":
            continue
        history = d.get("stage_history", [])
        for h in history:
            if h.get("stage") == "流失" and h.get("timestamp", "").startswith(target_month):
                lost_deals.append(d)
                break

    # 当前管道
    active_deals = [
        d for d in deals
        if d.get("stage") not in ("成交", "流失")
    ]

    new_amount = sum(d.get("amount", 0) for d in new_deals)
    won_amount = sum(d.get("amount", 0) for d in won_deals)
    lost_amount = sum(d.get("amount", 0) for d in lost_deals)
    pipeline_amount = sum(d.get("amount", 0) for d in active_deals)

    # 会议统计
    meetings = _get_meetings()
    month_meetings = [m for m in meetings if m.get("date", "").startswith(target_month)]

    # 管道健康评分和教练建议
    pipeline_health = _calculate_pipeline_health(deals)
    coaching_tips = _get_coaching_tips()

    result = {
        "month": target_month,
        "summary": {
            "new_deals": len(new_deals),
            "new_amount": new_amount,
            "new_amount_display": format_currency(new_amount),
            "won_deals": len(won_deals),
            "won_amount": won_amount,
            "won_amount_display": format_currency(won_amount),
            "lost_deals": len(lost_deals),
            "lost_amount": lost_amount,
            "lost_amount_display": format_currency(lost_amount),
            "active_pipeline": len(active_deals),
            "pipeline_amount": pipeline_amount,
            "pipeline_amount_display": format_currency(pipeline_amount),
            "meetings": len(month_meetings),
            "win_rate": round(
                len(won_deals) / max(len(won_deals) + len(lost_deals), 1), 4
            ),
        },
        "pipeline_health": pipeline_health,
        "coaching_tips": coaching_tips[:5],
    }

    # Mermaid 图表
    pie_data = [
        {"label": "成交", "value": len(won_deals)},
        {"label": "流失", "value": len(lost_deals)},
        {"label": "进行中", "value": len(active_deals)},
    ]
    result["mermaid_overview"] = _generate_pie_chart(
        f"{target_month} 商机状态分布", pie_data
    )

    bar_data = [
        {"label": "新增", "value": int(new_amount / 10000)},
        {"label": "成交", "value": int(won_amount / 10000)},
        {"label": "流失", "value": int(lost_amount / 10000)},
        {"label": "管道", "value": int(pipeline_amount / 10000)},
    ]
    result["mermaid_amounts"] = _generate_bar_chart(
        f"{target_month} 金额概览（万元）", bar_data, y_label="万元"
    )

    output_success(result)


def weekly_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成周度销售报告。

    Args:
        data: 可选参数，支持 week_start（YYYY-MM-DD，默认为本周一）。
    """
    if not require_paid_feature("advanced_analytics", "周度报告"):
        return

    deals = _get_deals()
    if not deals:
        output_error("暂无商机数据", code="NO_DATA")
        return

    data = data or {}
    week_start_str = data.get("week_start")
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
        except ValueError:
            output_error("week_start 格式错误，请使用 YYYY-MM-DD", code="VALIDATION_ERROR")
            return
    else:
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())

    week_end = week_start + timedelta(days=6)
    ws = week_start.strftime("%Y-%m-%d")
    we = week_end.strftime("%Y-%m-%d")

    # 本周新增
    new_deals = [
        d for d in deals
        if ws <= d.get("created_at", "")[:10] <= we
    ]

    # 本周更新
    updated_deals = [
        d for d in deals
        if ws <= d.get("updated_at", "")[:10] <= we
    ]

    # 本周成交
    won_deals = []
    for d in deals:
        if d.get("stage") != "成交":
            continue
        history = d.get("stage_history", [])
        for h in history:
            ts = h.get("timestamp", "")[:10]
            if h.get("stage") == "成交" and ws <= ts <= we:
                won_deals.append(d)
                break

    # 当前管道
    active_deals = [
        d for d in deals
        if d.get("stage") not in ("成交", "流失")
    ]

    # 风险商机
    risks = _detect_risk_deals(deals)

    # 会议统计
    meetings = _get_meetings()
    week_meetings = [
        m for m in meetings
        if ws <= m.get("date", "")[:10] <= we
    ]

    # 管道健康评分和教练建议
    pipeline_health = _calculate_pipeline_health(deals)
    coaching_tips = _get_coaching_tips()

    result = {
        "week": f"{ws} ~ {we}",
        "summary": {
            "new_deals": len(new_deals),
            "new_amount": sum(d.get("amount", 0) for d in new_deals),
            "new_amount_display": format_currency(sum(d.get("amount", 0) for d in new_deals)),
            "updated_deals": len(updated_deals),
            "won_deals": len(won_deals),
            "won_amount": sum(d.get("amount", 0) for d in won_deals),
            "won_amount_display": format_currency(sum(d.get("amount", 0) for d in won_deals)),
            "active_pipeline": len(active_deals),
            "pipeline_amount": sum(d.get("amount", 0) for d in active_deals),
            "pipeline_display": format_currency(sum(d.get("amount", 0) for d in active_deals)),
            "risk_deals": len(risks),
            "meetings": len(week_meetings),
        },
        "risk_deals": risks[:5],
        "pipeline_health": pipeline_health,
        "coaching_tips": coaching_tips[:3],
    }

    # Mermaid 图表
    stage_data = []
    for stage in DEAL_STAGES:
        count = sum(1 for d in active_deals if d.get("stage") == stage)
        if count > 0:
            stage_data.append({"label": stage, "value": count})

    if stage_data:
        result["mermaid_pipeline"] = _generate_pie_chart("本周管道分布", stage_data)

    output_success(result)


def trends_report(data: Optional[Dict[str, Any]] = None) -> None:
    """生成趋势分析报告。

    Args:
        data: 可选参数，支持 months（分析几个月，默认 6）。
    """
    if not require_paid_feature("advanced_analytics", "趋势分析"):
        return

    deals = _get_deals()
    if not deals:
        output_error("暂无商机数据", code="NO_DATA")
        return

    data = data or {}
    months_count = data.get("months", 6)
    try:
        months_count = int(months_count)
    except (TypeError, ValueError):
        months_count = 6

    # 生成月份列表
    now = datetime.now()
    months = []
    for i in range(months_count - 1, -1, -1):
        dt = now - timedelta(days=i * 30)
        months.append(dt.strftime("%Y-%m"))

    # 各月新增商机数和金额
    monthly_new = []
    monthly_won = []

    for month in months:
        new_in_month = [
            d for d in deals
            if d.get("created_at", "").startswith(month)
        ]
        won_in_month = []
        for d in deals:
            if d.get("stage") != "成交":
                continue
            for h in d.get("stage_history", []):
                if h.get("stage") == "成交" and h.get("timestamp", "").startswith(month):
                    won_in_month.append(d)
                    break

        monthly_new.append({
            "month": month,
            "count": len(new_in_month),
            "amount": sum(d.get("amount", 0) for d in new_in_month),
        })
        monthly_won.append({
            "month": month,
            "count": len(won_in_month),
            "amount": sum(d.get("amount", 0) for d in won_in_month),
        })

    result = {
        "period": f"{months[0]} ~ {months[-1]}",
        "monthly_new": monthly_new,
        "monthly_won": monthly_won,
    }

    # Mermaid 图表
    new_chart_data = [
        {"label": m["month"][-5:], "value": m["count"]}
        for m in monthly_new
    ]
    result["mermaid_new_trend"] = _generate_line_chart(
        "月度新增商机趋势", new_chart_data, y_label="数量"
    )

    won_chart_data = [
        {"label": m["month"][-5:], "value": int(m["amount"] / 10000)}
        for m in monthly_won
    ]
    result["mermaid_won_trend"] = _generate_bar_chart(
        "月度成交金额趋势（万元）", won_chart_data, y_label="万元"
    )

    output_success(result)


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer 销售管道报告")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "funnel": lambda: funnel_report(data),
        "forecast": lambda: forecast_report(data),
        "monthly": lambda: monthly_report(data),
        "weekly": lambda: weekly_report(data),
        "trends": lambda: trends_report(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
