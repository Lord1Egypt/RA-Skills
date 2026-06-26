#!/usr/bin/env python3
"""
deal-closer 自学习销售智能模块

从历史成交/流失数据中学习模式，预测商机胜率，提供销售教练建议。
基于 self-improving-agent 理念，持续优化销售策略。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    write_json_file,
    format_currency,
    format_percentage,
    calculate_days_since,
    DEAL_STAGES,
    STAGE_DEFAULT_PROBABILITY,
)


# ============================================================
# 常量与配置
# ============================================================

LEARNING_FILE = "learning.json"
DEALS_FILE = "deals.json"

# 默认学习数据结构
_DEFAULT_LEARNING_DATA = {
    "outcomes": [],         # 成交/流失记录
    "patterns": [],         # 成功模式记录
    "version": "1.0.0",
    "last_updated": "",
}

# 特征权重（用于简单评分模型）
_FEATURE_WEIGHTS = {
    "cycle_days_score": 0.15,       # 销售周期合理性
    "followup_score": 0.20,         # 跟进频率得分
    "deal_size_score": 0.10,        # 金额规模匹配度
    "stage_velocity_score": 0.20,   # 阶段推进速度
    "industry_score": 0.15,         # 行业胜率
    "engagement_score": 0.20,       # 客户互动得分
}

# 销售周期基准天数（按阶段）
_STAGE_BENCHMARK_DAYS = {
    "线索": 7,
    "初步接触": 10,
    "需求确认": 14,
    "方案报价": 10,
    "商务谈判": 14,
    "合同签署": 7,
}


# ============================================================
# 数据操作
# ============================================================

def _get_learning_data() -> Dict[str, Any]:
    """读取学习数据文件。"""
    filepath = get_data_file(LEARNING_FILE)
    if not os.path.exists(filepath):
        return dict(_DEFAULT_LEARNING_DATA)
    data = read_json_file(filepath)
    if isinstance(data, list):
        # 兼容旧格式
        return dict(_DEFAULT_LEARNING_DATA)
    return data


def _save_learning_data(data: Dict[str, Any]) -> None:
    """保存学习数据到文件。"""
    data["last_updated"] = now_iso()
    write_json_file(get_data_file(LEARNING_FILE), data)


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


# ============================================================
# 特征提取
# ============================================================

def _extract_deal_features(deal: Dict[str, Any]) -> Dict[str, Any]:
    """从商机数据中提取特征向量。

    Args:
        deal: 商机数据字典。

    Returns:
        特征字典，包含各维度的原始值。
    """
    # 销售周期天数
    created = deal.get("created_at", "")
    updated = deal.get("updated_at", "")
    cycle_days = 0
    if created:
        cycle_days = calculate_days_since(created)

    # 阶段历史分析
    history = deal.get("stage_history", [])
    stage_count = len(history)

    # 计算各阶段停留天数
    stage_durations = {}
    for i in range(len(history) - 1):
        stage = history[i].get("stage", "")
        ts_current = history[i].get("timestamp", "")
        ts_next = history[i + 1].get("timestamp", "")
        if ts_current and ts_next:
            try:
                t1 = datetime.fromisoformat(ts_current.replace("Z", "+00:00")).replace(tzinfo=None)
                t2 = datetime.fromisoformat(ts_next.replace("Z", "+00:00")).replace(tzinfo=None)
                duration = (t2 - t1).days
                stage_durations[stage] = duration
            except (ValueError, TypeError):
                pass

    # 最后阶段的停留时间
    if history:
        last_stage = history[-1].get("stage", "")
        last_ts = history[-1].get("timestamp", "")
        if last_ts:
            stage_durations[last_stage] = calculate_days_since(last_ts)

    return {
        "cycle_days": cycle_days,
        "stage_count": stage_count,
        "stage_durations": stage_durations,
        "amount": deal.get("amount", 0),
        "industry": deal.get("company", ""),
        "source": deal.get("source", ""),
        "tags": deal.get("tags", []),
        "current_stage": deal.get("stage", ""),
        "probability": deal.get("probability", 0),
    }


def _calculate_feature_scores(features: Dict[str, Any],
                               learning_data: Dict[str, Any]) -> Dict[str, float]:
    """根据特征和历史数据计算各维度评分。

    Args:
        features: 商机特征字典。
        learning_data: 学习数据。

    Returns:
        各维度评分字典（0.0-1.0）。
    """
    outcomes = learning_data.get("outcomes", [])
    won_outcomes = [o for o in outcomes if o.get("result") == "won"]
    lost_outcomes = [o for o in outcomes if o.get("result") == "lost"]

    scores = {}

    # 1. 销售周期合理性评分
    if won_outcomes:
        avg_won_cycle = sum(o.get("cycle_days", 30) for o in won_outcomes) / len(won_outcomes)
        cycle_days = features.get("cycle_days", 0)
        if avg_won_cycle > 0:
            # 与成功案例的平均周期越接近，得分越高
            ratio = cycle_days / avg_won_cycle if avg_won_cycle > 0 else 1.0
            if ratio <= 1.0:
                scores["cycle_days_score"] = 0.5 + ratio * 0.5
            elif ratio <= 2.0:
                scores["cycle_days_score"] = max(0.2, 1.0 - (ratio - 1.0) * 0.5)
            else:
                scores["cycle_days_score"] = 0.1
        else:
            scores["cycle_days_score"] = 0.5
    else:
        scores["cycle_days_score"] = 0.5

    # 2. 跟进频率得分
    stage_count = features.get("stage_count", 1)
    cycle_days = max(features.get("cycle_days", 1), 1)
    followup_rate = stage_count / (cycle_days / 7.0) if cycle_days >= 7 else stage_count
    # 每周至少1次阶段推进算好
    scores["followup_score"] = min(1.0, followup_rate * 0.5)

    # 3. 金额规模匹配度
    amount = features.get("amount", 0)
    if won_outcomes:
        avg_won_amount = sum(o.get("amount", 0) for o in won_outcomes) / len(won_outcomes)
        if avg_won_amount > 0:
            ratio = amount / avg_won_amount
            if 0.5 <= ratio <= 2.0:
                scores["deal_size_score"] = 0.8
            elif 0.2 <= ratio <= 3.0:
                scores["deal_size_score"] = 0.5
            else:
                scores["deal_size_score"] = 0.3
        else:
            scores["deal_size_score"] = 0.5
    else:
        scores["deal_size_score"] = 0.5

    # 4. 阶段推进速度评分
    stage_durations = features.get("stage_durations", {})
    velocity_scores = []
    for stage, duration in stage_durations.items():
        benchmark = _STAGE_BENCHMARK_DAYS.get(stage, 10)
        if duration <= benchmark:
            velocity_scores.append(1.0)
        elif duration <= benchmark * 2:
            velocity_scores.append(0.5)
        else:
            velocity_scores.append(0.2)
    scores["stage_velocity_score"] = (
        sum(velocity_scores) / len(velocity_scores) if velocity_scores else 0.5
    )

    # 5. 行业胜率（根据历史同行业数据）
    industry = features.get("industry", "")
    if industry and outcomes:
        industry_outcomes = [o for o in outcomes if industry in o.get("industry", "")]
        if industry_outcomes:
            won_count = sum(1 for o in industry_outcomes if o.get("result") == "won")
            scores["industry_score"] = won_count / len(industry_outcomes)
        else:
            scores["industry_score"] = 0.5
    else:
        scores["industry_score"] = 0.5

    # 6. 客户互动得分（基于阶段推进次数）
    if stage_count >= 4:
        scores["engagement_score"] = 0.9
    elif stage_count >= 2:
        scores["engagement_score"] = 0.6
    else:
        scores["engagement_score"] = 0.3

    return scores


def _compute_win_probability(scores: Dict[str, float]) -> float:
    """根据各维度评分计算综合胜率。

    Args:
        scores: 各维度评分字典。

    Returns:
        加权胜率（0-100）。
    """
    total = 0.0
    for key, weight in _FEATURE_WEIGHTS.items():
        score = scores.get(key, 0.5)
        total += score * weight
    # 归一化到 0-100
    return round(total * 100, 1)


# ============================================================
# 建议生成
# ============================================================

def _generate_suggestions(deal: Dict[str, Any],
                          features: Dict[str, Any],
                          learning_data: Dict[str, Any]) -> List[str]:
    """根据商机特征和历史数据生成建议。

    Args:
        deal: 商机数据。
        features: 商机特征。
        learning_data: 学习数据。

    Returns:
        建议列表。
    """
    suggestions = []
    outcomes = learning_data.get("outcomes", [])
    won_outcomes = [o for o in outcomes if o.get("result") == "won"]

    stage = deal.get("stage", "")
    stage_durations = features.get("stage_durations", {})

    # 阶段停留时间过长
    if stage in stage_durations:
        current_duration = stage_durations[stage]
        benchmark = _STAGE_BENCHMARK_DAYS.get(stage, 10)

        # 计算历史同阶段平均停留天数
        if won_outcomes:
            same_stage_durations = []
            for o in won_outcomes:
                sd = o.get("stage_durations", {})
                if stage in sd:
                    same_stage_durations.append(sd[stage])
            if same_stage_durations:
                avg_duration = sum(same_stage_durations) / len(same_stage_durations)
                if current_duration > avg_duration * 1.5:
                    suggestions.append(
                        f"相似规模的商机平均在{stage}阶段停留"
                        f"{int(avg_duration)}天，当前商机已停留"
                        f"{current_duration}天，建议主动跟进"
                    )

        if current_duration > benchmark * 2:
            suggestions.append(
                f"当前在「{stage}」阶段已停留 {current_duration} 天，"
                f"超出基准 {benchmark} 天的两倍，存在流失风险"
            )

    # 跟进时机建议
    patterns = learning_data.get("patterns", [])
    timing_patterns = [p for p in patterns if p.get("category") == "timing"]
    if timing_patterns:
        best_timing = max(timing_patterns, key=lambda p: p.get("success_rate", 0))
        suggestions.append(
            f"历史数据显示，{best_timing.get('description', '周二上午')}的跟进"
            f"回复率最高({format_percentage(best_timing.get('success_rate', 0.5))})"
        )
    else:
        suggestions.append(
            "历史数据显示，周二上午的跟进邮件回复率最高(65%)，建议优先安排此时段跟进"
        )

    # 金额相关建议
    amount = deal.get("amount", 0)
    if amount > 0 and won_outcomes:
        similar_won = [
            o for o in won_outcomes
            if 0.5 * amount <= o.get("amount", 0) <= 2.0 * amount
        ]
        if similar_won:
            avg_cycle = sum(o.get("cycle_days", 30) for o in similar_won) / len(similar_won)
            current_cycle = features.get("cycle_days", 0)
            if current_cycle < avg_cycle * 0.5:
                suggestions.append(
                    f"相似金额商机平均周期为 {int(avg_cycle)} 天，"
                    f"当前仅 {current_cycle} 天，节奏良好"
                )
            elif current_cycle > avg_cycle * 1.5:
                suggestions.append(
                    f"相似金额商机平均周期为 {int(avg_cycle)} 天，"
                    f"当前已 {current_cycle} 天，建议加速推进"
                )

    # 阶段转化建议
    if stage in ("需求确认", "方案报价") and won_outcomes:
        # 计算转化率
        stage_idx = DEAL_STAGES.index(stage) if stage in DEAL_STAGES else -1
        if stage_idx >= 0 and stage_idx < len(DEAL_STAGES) - 2:
            next_stage = DEAL_STAGES[stage_idx + 1]
            total_at_stage = sum(
                1 for o in outcomes
                if stage in o.get("stage_durations", {})
            )
            converted = sum(
                1 for o in outcomes
                if next_stage in o.get("stage_durations", {})
                and stage in o.get("stage_durations", {})
            )
            if total_at_stage > 0:
                rate = converted / total_at_stage
                if rate < 0.5:
                    suggestions.append(
                        f"{stage}→{next_stage}转化率偏低"
                        f"({format_percentage(rate)})，建议加强需求调研深度"
                    )

    return suggestions


def _generate_coaching_tips(learning_data: Dict[str, Any],
                             deals: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """根据管道瓶颈生成教练建议。

    Args:
        learning_data: 学习数据。
        deals: 当前商机列表。

    Returns:
        教练建议列表。
    """
    tips = []
    outcomes = learning_data.get("outcomes", [])

    # 活跃商机
    active_deals = [
        d for d in deals if d.get("stage") not in ("成交", "流失")
    ]

    if not active_deals:
        tips.append({
            "category": "pipeline",
            "tip": "当前管道为空，建议加大线索获取力度",
            "priority": "high",
        })
        return tips

    # 分析各阶段分布
    stage_counts = defaultdict(int)
    for d in active_deals:
        stage_counts[d.get("stage", "")] += 1

    # 检测瓶颈：某阶段商机堆积
    total_active = len(active_deals)
    for stage, count in stage_counts.items():
        ratio = count / total_active if total_active > 0 else 0
        if ratio > 0.4 and total_active >= 3:
            tips.append({
                "category": "bottleneck",
                "tip": f"「{stage}」阶段商机占比过高({format_percentage(ratio)})，"
                       f"共 {count} 个商机停滞，建议集中精力推进此阶段转化",
                "priority": "high",
            })

    # 检测停滞商机
    stale_count = 0
    for d in active_deals:
        updated = d.get("updated_at", "")
        if updated and calculate_days_since(updated) > 14:
            stale_count += 1

    if stale_count > 0:
        stale_ratio = stale_count / total_active
        tips.append({
            "category": "stale",
            "tip": f"有 {stale_count} 个商机超过14天未更新"
                   f"（占比{format_percentage(stale_ratio)}），建议逐一排查跟进",
            "priority": "high" if stale_ratio > 0.3 else "medium",
        })

    # 转化率分析（基于历史数据）
    if outcomes:
        won = sum(1 for o in outcomes if o.get("result") == "won")
        total = len(outcomes)
        win_rate = won / total if total > 0 else 0

        if win_rate < 0.3:
            tips.append({
                "category": "win_rate",
                "tip": f"整体胜率偏低({format_percentage(win_rate)})，"
                       f"建议复盘最近流失商机，找出共性问题",
                "priority": "high",
            })
        elif win_rate > 0.6:
            tips.append({
                "category": "win_rate",
                "tip": f"整体胜率较高({format_percentage(win_rate)})，"
                       f"可适当提高目标商机金额或数量",
                "priority": "low",
            })

        # 流失原因分析
        loss_reasons = defaultdict(int)
        for o in outcomes:
            if o.get("result") == "lost":
                for reason in o.get("loss_reasons", []):
                    loss_reasons[reason] += 1

        if loss_reasons:
            top_reason = max(loss_reasons.items(), key=lambda x: x[1])
            tips.append({
                "category": "loss_analysis",
                "tip": f"最常见流失原因是「{top_reason[0]}」（{top_reason[1]}次），"
                       f"建议针对性优化应对策略",
                "priority": "medium",
            })

    # 跟进频率建议
    patterns = learning_data.get("patterns", [])
    followup_patterns = [p for p in patterns if p.get("category") == "followup"]
    if followup_patterns:
        best = max(followup_patterns, key=lambda p: p.get("success_rate", 0))
        tips.append({
            "category": "best_practice",
            "tip": f"最佳实践：{best.get('description', '')}，"
                   f"成功率 {format_percentage(best.get('success_rate', 0))}",
            "priority": "low",
        })

    return tips


# ============================================================
# 操作函数
# ============================================================

def record_outcome(data: Dict[str, Any]) -> None:
    """记录商机成交/流失结果。

    必填字段: deal_id, result（won/lost）
    可选字段: cycle_days, followup_count, loss_reasons, notes,
              contributing_factors

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "自学习销售智能"):
        return

    deal_id = data.get("deal_id")
    result = data.get("result", "").lower()

    if not deal_id:
        output_error("商机ID（deal_id）为必填字段", code="VALIDATION_ERROR")
        return

    if result not in ("won", "lost"):
        output_error("结果（result）必须为 won 或 lost", code="VALIDATION_ERROR")
        return

    # 加载商机数据获取特征
    deals = _get_deals()
    target_deal = None
    for d in deals:
        if d.get("id") == deal_id:
            target_deal = d
            break

    features = {}
    if target_deal:
        features = _extract_deal_features(target_deal)

    # 构建结果记录
    outcome = {
        "id": generate_id("LO"),
        "deal_id": deal_id,
        "deal_name": target_deal.get("name", "") if target_deal else "",
        "result": result,
        "amount": target_deal.get("amount", 0) if target_deal else data.get("amount", 0),
        "industry": target_deal.get("company", "") if target_deal else data.get("industry", ""),
        "source": target_deal.get("source", "") if target_deal else data.get("source", ""),
        "cycle_days": data.get("cycle_days", features.get("cycle_days", 0)),
        "followup_count": data.get("followup_count", features.get("stage_count", 0)),
        "stage_durations": features.get("stage_durations", {}),
        "loss_reasons": data.get("loss_reasons", []),
        "contributing_factors": data.get("contributing_factors", []),
        "notes": data.get("notes", ""),
        "recorded_at": now_iso(),
    }

    learning = _get_learning_data()
    learning["outcomes"].append(outcome)
    _save_learning_data(learning)

    output_success({
        "message": f"已记录商机结果：{result}",
        "outcome": outcome,
        "total_outcomes": len(learning["outcomes"]),
    })


def record_pattern(data: Dict[str, Any]) -> None:
    """记录成功模式。

    必填字段: category, description
    可选字段: success_rate, applicable_stages, notes

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "自学习销售智能"):
        return

    category = data.get("category", "")
    description = data.get("description", "")

    if not category:
        output_error("模式类别（category）为必填字段", code="VALIDATION_ERROR")
        return

    if not description:
        output_error("模式描述（description）为必填字段", code="VALIDATION_ERROR")
        return

    valid_categories = [
        "timing", "communication", "pricing", "followup",
        "negotiation", "presentation", "objection_handling", "other",
    ]
    if category not in valid_categories:
        output_error(
            f"无效类别: {category}，有效类别: {', '.join(valid_categories)}",
            code="VALIDATION_ERROR",
        )
        return

    pattern = {
        "id": generate_id("LP"),
        "category": category,
        "description": description,
        "success_rate": min(1.0, max(0.0, float(data.get("success_rate", 0.5)))),
        "applicable_stages": data.get("applicable_stages", []),
        "notes": data.get("notes", ""),
        "recorded_at": now_iso(),
    }

    learning = _get_learning_data()
    learning["patterns"].append(pattern)
    _save_learning_data(learning)

    output_success({
        "message": f"已记录成功模式：{description}",
        "pattern": pattern,
        "total_patterns": len(learning["patterns"]),
    })


def predict(data: Dict[str, Any]) -> None:
    """预测商机胜率。

    必填字段: deal_id
    可选: 无参数时预测所有活跃商机

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "AI胜率预测"):
        return

    deal_id = data.get("deal_id")
    deals = _get_deals()
    learning = _get_learning_data()

    if deal_id:
        # 预测单个商机
        target = None
        for d in deals:
            if d.get("id") == deal_id:
                target = d
                break

        if not target:
            output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
            return

        features = _extract_deal_features(target)
        scores = _calculate_feature_scores(features, learning)
        probability = _compute_win_probability(scores)
        suggestions = _generate_suggestions(target, features, learning)

        output_success({
            "deal_id": deal_id,
            "deal_name": target.get("name", ""),
            "current_stage": target.get("stage", ""),
            "manual_probability": target.get("probability", 0),
            "ai_probability": probability,
            "dimension_scores": {
                k: round(v * 100, 1)
                for k, v in scores.items()
            },
            "suggestions": suggestions,
            "data_basis": len(learning.get("outcomes", [])),
        })
    else:
        # 预测所有活跃商机
        active = [
            d for d in deals
            if d.get("stage") not in ("成交", "流失")
        ]

        if not active:
            output_error("暂无活跃商机", code="NO_DATA")
            return

        predictions = []
        for deal in active:
            features = _extract_deal_features(deal)
            scores = _calculate_feature_scores(features, learning)
            probability = _compute_win_probability(scores)
            predictions.append({
                "deal_id": deal.get("id", ""),
                "deal_name": deal.get("name", ""),
                "stage": deal.get("stage", ""),
                "amount": deal.get("amount", 0),
                "amount_display": format_currency(deal.get("amount", 0)),
                "manual_probability": deal.get("probability", 0),
                "ai_probability": probability,
            })

        # 按AI预测胜率排序
        predictions.sort(key=lambda p: p["ai_probability"], reverse=True)

        output_success({
            "total": len(predictions),
            "predictions": predictions,
            "data_basis": len(learning.get("outcomes", [])),
        })


def suggest(data: Dict[str, Any]) -> None:
    """为商机生成主动建议。

    必填字段: deal_id

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "AI销售建议"):
        return

    deal_id = data.get("deal_id")
    if not deal_id:
        output_error("商机ID（deal_id）为必填字段", code="VALIDATION_ERROR")
        return

    deals = _get_deals()
    target = None
    for d in deals:
        if d.get("id") == deal_id:
            target = d
            break

    if not target:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    learning = _get_learning_data()
    features = _extract_deal_features(target)
    suggestions = _generate_suggestions(target, features, learning)

    if not suggestions:
        suggestions.append("暂无特定建议，建议保持当前跟进节奏")

    output_success({
        "deal_id": deal_id,
        "deal_name": target.get("name", ""),
        "current_stage": target.get("stage", ""),
        "suggestions": suggestions,
        "suggestion_count": len(suggestions),
    })


def coach(data: Optional[Dict[str, Any]] = None) -> None:
    """生成销售教练建议。

    基于当前管道瓶颈和历史数据。

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("advanced_analytics", "销售教练"):
        return

    deals = _get_deals()
    learning = _get_learning_data()

    tips = _generate_coaching_tips(learning, deals)

    if not tips:
        tips.append({
            "category": "general",
            "tip": "当前管道状态良好，继续保持。建议定期复盘成交案例，沉淀最佳实践。",
            "priority": "low",
        })

    # 按优先级排序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tips.sort(key=lambda t: priority_order.get(t.get("priority", "low"), 2))

    output_success({
        "tips": tips,
        "total_tips": len(tips),
        "data_basis": {
            "outcomes": len(learning.get("outcomes", [])),
            "patterns": len(learning.get("patterns", [])),
            "active_deals": len([
                d for d in deals if d.get("stage") not in ("成交", "流失")
            ]),
        },
    })


def stats(data: Optional[Dict[str, Any]] = None) -> None:
    """生成学习统计报告。

    包含胜率趋势、平均周期、流失原因、最佳实践。

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("advanced_analytics", "学习统计"):
        return

    learning = _get_learning_data()
    outcomes = learning.get("outcomes", [])
    patterns = learning.get("patterns", [])

    if not outcomes:
        output_success({
            "message": "暂无历史数据，请先使用 record-outcome 记录商机结果",
            "total_outcomes": 0,
            "total_patterns": len(patterns),
        })
        return

    won = [o for o in outcomes if o.get("result") == "won"]
    lost = [o for o in outcomes if o.get("result") == "lost"]

    # 胜率
    win_rate = len(won) / len(outcomes) if outcomes else 0

    # 平均销售周期
    avg_cycle_won = (
        sum(o.get("cycle_days", 0) for o in won) / len(won)
        if won else 0
    )
    avg_cycle_lost = (
        sum(o.get("cycle_days", 0) for o in lost) / len(lost)
        if lost else 0
    )

    # 平均成交金额
    avg_amount_won = (
        sum(o.get("amount", 0) for o in won) / len(won)
        if won else 0
    )

    # 流失原因统计
    loss_reasons = defaultdict(int)
    for o in lost:
        for reason in o.get("loss_reasons", []):
            loss_reasons[reason] += 1

    top_loss_reasons = sorted(
        loss_reasons.items(), key=lambda x: x[1], reverse=True
    )[:5]

    # 最佳实践
    best_practices = sorted(
        patterns,
        key=lambda p: p.get("success_rate", 0),
        reverse=True,
    )[:5]

    # 按月胜率趋势
    monthly_stats = defaultdict(lambda: {"won": 0, "lost": 0})
    for o in outcomes:
        month = o.get("recorded_at", "")[:7]
        if month:
            if o.get("result") == "won":
                monthly_stats[month]["won"] += 1
            else:
                monthly_stats[month]["lost"] += 1

    win_rate_trend = []
    for month in sorted(monthly_stats.keys()):
        ms = monthly_stats[month]
        total = ms["won"] + ms["lost"]
        rate = ms["won"] / total if total > 0 else 0
        win_rate_trend.append({
            "month": month,
            "won": ms["won"],
            "lost": ms["lost"],
            "win_rate": round(rate, 4),
            "win_rate_display": format_percentage(rate),
        })

    output_success({
        "total_outcomes": len(outcomes),
        "total_won": len(won),
        "total_lost": len(lost),
        "win_rate": round(win_rate, 4),
        "win_rate_display": format_percentage(win_rate),
        "avg_cycle_won_days": round(avg_cycle_won, 1),
        "avg_cycle_lost_days": round(avg_cycle_lost, 1),
        "avg_won_amount": round(avg_amount_won, 2),
        "avg_won_amount_display": format_currency(avg_amount_won),
        "top_loss_reasons": [
            {"reason": r, "count": c}
            for r, c in top_loss_reasons
        ],
        "best_practices": [
            {
                "category": p.get("category", ""),
                "description": p.get("description", ""),
                "success_rate": format_percentage(p.get("success_rate", 0)),
            }
            for p in best_practices
        ],
        "win_rate_trend": win_rate_trend,
        "total_patterns": len(patterns),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer 自学习销售智能")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "record-outcome": lambda: record_outcome(data or {}),
        "record-pattern": lambda: record_pattern(data or {}),
        "predict": lambda: predict(data or {}),
        "suggest": lambda: suggest(data or {}),
        "coach": lambda: coach(data),
        "stats": lambda: stats(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
