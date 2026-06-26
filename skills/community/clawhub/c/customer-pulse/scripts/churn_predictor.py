#!/usr/bin/env python3
"""
customer-pulse 客户流失预测模块（付费功能）

基于跟进频率衰减趋势预测客户流失风险，帮助提前干预。
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    calculate_days_since,
    check_subscription,
    format_currency,
    get_data_file,
    load_input_data,
    mask_phone,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    today_str,
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
# 流失预测核心逻辑
# ============================================================

def _calculate_churn_risk(customer: Dict, followups: List[Dict]) -> Dict[str, Any]:
    """计算单个客户的流失风险。

    使用简单的统计方法：
    1. 计算历史平均跟进间隔
    2. 计算近期跟进间隔
    3. 比较近期间隔与历史平均的偏差
    4. 综合最后跟进距今天数计算风险分数

    Args:
        customer: 客户数据。
        followups: 该客户的跟进记录列表。

    Returns:
        包含风险评估详情的字典。
    """
    cid = customer["id"]
    customer_followups = sorted(
        [f for f in followups if f.get("customer_id") == cid],
        key=lambda f: f.get("date", ""),
    )

    today = today_str()
    risk_score = 0  # 0-100，越高风险越大
    risk_factors = []

    if not customer_followups:
        # 从未跟进
        days_since_created = calculate_days_since(customer.get("created_at", "")[:10])
        risk_score = min(90, 40 + days_since_created * 3)
        risk_factors.append(f"从未跟进，客户创建已 {days_since_created} 天")
    elif len(customer_followups) == 1:
        # 只跟进过一次
        last_date = customer_followups[0].get("date", "")
        days_since = calculate_days_since(last_date)
        risk_score = min(85, 20 + days_since * 4)
        risk_factors.append(f"仅跟进 1 次，距今 {days_since} 天")
    else:
        # 计算跟进间隔
        intervals = []
        for i in range(1, len(customer_followups)):
            d1 = customer_followups[i - 1].get("date", "")
            d2 = customer_followups[i].get("date", "")
            if d1 and d2:
                try:
                    dt1 = datetime.strptime(d1, "%Y-%m-%d")
                    dt2 = datetime.strptime(d2, "%Y-%m-%d")
                    interval = (dt2 - dt1).days
                    if interval > 0:
                        intervals.append(interval)
                except ValueError:
                    continue

        if intervals:
            avg_interval = sum(intervals) / len(intervals)

            # 近期间隔（最后 3 个）
            recent_intervals = intervals[-3:] if len(intervals) >= 3 else intervals
            recent_avg = sum(recent_intervals) / len(recent_intervals)

            # 频率衰减比
            decay_ratio = recent_avg / avg_interval if avg_interval > 0 else 1

            # 最后跟进距今天数
            last_date = customer_followups[-1].get("date", "")
            days_since_last = calculate_days_since(last_date)

            # 风险评分计算
            # 基础分：基于频率衰减
            if decay_ratio > 2.0:
                risk_score += 40
                risk_factors.append(f"跟进频率显著下降（衰减比 {decay_ratio:.1f}x）")
            elif decay_ratio > 1.5:
                risk_score += 25
                risk_factors.append(f"跟进频率有所下降（衰减比 {decay_ratio:.1f}x）")
            elif decay_ratio > 1.2:
                risk_score += 10
                risk_factors.append(f"跟进频率略有放缓（衰减比 {decay_ratio:.1f}x）")

            # 附加分：基于最后跟进距今天数
            if days_since_last > 30:
                risk_score += 35
                risk_factors.append(f"超过 30 天未跟进（{days_since_last} 天）")
            elif days_since_last > 14:
                risk_score += 25
                risk_factors.append(f"超过 14 天未跟进（{days_since_last} 天）")
            elif days_since_last > 7:
                risk_score += 15
                risk_factors.append(f"超过 7 天未跟进（{days_since_last} 天）")

            # 附加分：跟进次数过少
            if len(customer_followups) <= 2:
                risk_score += 10
                risk_factors.append(f"跟进次数较少（仅 {len(customer_followups)} 次）")
        else:
            last_date = customer_followups[-1].get("date", "")
            days_since_last = calculate_days_since(last_date)
            risk_score = min(80, 30 + days_since_last * 3)
            risk_factors.append(f"距最后跟进已 {days_since_last} 天")

    # 预算因素：高预算客户流失风险需更关注
    budget = float(customer.get("budget", 0))
    impact = "高" if budget >= 100000 else ("中" if budget >= 10000 else "低")

    # 限制风险分在 0-100
    risk_score = max(0, min(100, risk_score))

    # 风险等级
    if risk_score >= 70:
        risk_level = "高风险"
    elif risk_score >= 40:
        risk_level = "中风险"
    else:
        risk_level = "低风险"

    return {
        "customer_id": cid,
        "customer_name": customer["name"],
        "company": customer.get("company", ""),
        "stage": customer.get("stage", ""),
        "phone": mask_phone(customer.get("phone", "")),
        "budget": budget,
        "budget_display": format_currency(budget),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "impact": impact,
        "total_followups": len(customer_followups),
        "last_followup_date": customer_followups[-1].get("date", "") if customer_followups else "无",
        "suggestion": _get_risk_suggestion(risk_level, risk_factors),
    }


def _get_risk_suggestion(risk_level: str, factors: List[str]) -> str:
    """根据风险等级和因素给出建议。"""
    if risk_level == "高风险":
        return "建议立即安排跟进，了解客户最新情况，必要时由主管介入沟通"
    elif risk_level == "中风险":
        return "建议在本周内安排一次跟进，重新建立联系，了解客户需求变化"
    else:
        return "当前状态良好，建议保持正常跟进节奏"


# ============================================================
# 预测操作
# ============================================================

def predict_churn(data: Optional[Dict[str, Any]] = None) -> None:
    """对所有活跃客户进行流失风险预测。

    仅分析处于活跃阶段（非成交、非流失）的客户。

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("churn_prediction", "客户流失预警"):
        return

    customers = _get_customers()
    followups = _get_followups()

    # 只分析活跃客户
    active_customers = [
        c for c in customers
        if c.get("stage") not in ("成交", "流失")
    ]

    if not active_customers:
        output_error("暂无活跃客户可分析", code="NO_DATA")
        return

    predictions = []
    for customer in active_customers:
        risk = _calculate_churn_risk(customer, followups)
        predictions.append(risk)

    # 按风险分数降序排列
    predictions.sort(key=lambda p: p["risk_score"], reverse=True)

    # 统计
    high_risk = sum(1 for p in predictions if p["risk_level"] == "高风险")
    mid_risk = sum(1 for p in predictions if p["risk_level"] == "中风险")
    low_risk = sum(1 for p in predictions if p["risk_level"] == "低风险")

    # 高风险客户的总预算
    at_risk_budget = sum(p["budget"] for p in predictions if p["risk_level"] == "高风险")

    output_success({
        "analysis_date": today_str(),
        "total_analyzed": len(predictions),
        "risk_summary": {
            "high": high_risk,
            "medium": mid_risk,
            "low": low_risk,
        },
        "at_risk_budget": format_currency(at_risk_budget),
        "predictions": predictions,
    })


def risk_list(data: Optional[Dict[str, Any]] = None) -> None:
    """获取高风险客户列表。

    只返回风险等级为「高风险」的客户。

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("churn_prediction", "客户流失预警"):
        return

    customers = _get_customers()
    followups = _get_followups()

    active_customers = [
        c for c in customers
        if c.get("stage") not in ("成交", "流失")
    ]

    high_risk_list = []
    for customer in active_customers:
        risk = _calculate_churn_risk(customer, followups)
        if risk["risk_level"] == "高风险":
            high_risk_list.append(risk)

    high_risk_list.sort(key=lambda p: p["risk_score"], reverse=True)

    total_at_risk_budget = sum(r["budget"] for r in high_risk_list)

    output_success({
        "analysis_date": today_str(),
        "high_risk_count": len(high_risk_list),
        "total_at_risk_budget": format_currency(total_at_risk_budget),
        "high_risk_customers": high_risk_list,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("customer-pulse 客户流失预测")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "predict": lambda: predict_churn(data),
        "risk_list": lambda: risk_list(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
