#!/usr/bin/env python3
"""
广告投手 - 预算优化与素材分析模块
预算分配建议、出价优化、素材疲劳度检测、A/B测试分析
"""

import sys
import json
from collections import defaultdict
from typing import Optional

from data_manager import load_file, get_summary
from performance import group_by_campaign, group_by_date


def budget_allocation(records: list, total_budget: float = None) -> dict:
    """
    预算分配建议（532法则）
    total_budget: 总预算，None则基于历史消耗自动计算
    """
    campaigns = group_by_campaign(records)
    camp_list = list(campaigns.values())

    if not camp_list:
        return {"error": "无计划数据"}

    # 计算综合评分
    max_cost = max(c.get("cost", 0) for c in camp_list) or 1
    max_roas = max(c.get("roas", 0) for c in camp_list) or 1
    min_cpa = min(c.get("cpa", 999999) for c in camp_list)

    for c in camp_list:
        score = 0
        if max_cost > 0:
            score += (c.get("cost", 0) / max_cost) * 30
        if max_roas > 0:
            score += (c.get("roas", 0) / max_roas) * 40
        cpa_val = c.get("cpa", min_cpa)
        if cpa_val > 0 and min_cpa > 0:
            score += (min_cpa / cpa_val) * 30
        c["score"] = round(score, 1)

    # 分级
    camp_list.sort(key=lambda x: x.get("score", 0), reverse=True)

    if total_budget is None:
        total_budget = sum(c.get("cost", 0) for c in camp_list)

    top_n = max(1, len(camp_list) // 3)
    mid_n = top_n
    rest_n = len(camp_list) - top_n - mid_n

    # 532分配
    tier_a = camp_list[:top_n]  # 50%
    tier_b = camp_list[top_n:top_n + mid_n] if mid_n > 0 else []  # 30%
    tier_c = camp_list[top_n + mid_n:] if rest_n > 0 else []  # 20%

    allocation = {
        "total_budget": round(total_budget, 2),
        "strategy": "532分配法",
        "tiers": {
            "A_优质计划": {
                "budget_share": "50%",
                "amount": round(total_budget * 0.5, 2),
                "plans": [{"name": c["name"], "budget": round(total_budget * 0.5 / len(tier_a), 2),
                          "roas": c.get("roas", 0), "cpa": c.get("cpa", 0)} for c in tier_a],
                "rule": "ROAS > 2.5，持续放量，单日预算可+20%"
            },
            "B_潜力计划": {
                "budget_share": "30%",
                "amount": round(total_budget * 0.3, 2),
                "plans": [{"name": c["name"], "budget": round(total_budget * 0.3 / len(tier_b), 2) if tier_b else 0,
                          "roas": c.get("roas", 0), "cpa": c.get("cpa", 0)} for c in tier_b],
                "rule": "ROAS 1.5~2.5，观察趋势再决策"
            },
            "C_测试计划": {
                "budget_share": "20%",
                "amount": round(total_budget * 0.2, 2),
                "plans": [{"name": c["name"], "budget": round(total_budget * 0.2 / len(tier_c), 2) if tier_c else 0,
                          "roas": c.get("roas", 0), "cpa": c.get("cpa", 0)} for c in tier_c],
                "rule": "ROAS < 1.5，建议缩减或关停"
            }
        }
    }
    return allocation


def bid_optimizer(records: list) -> dict:
    """出价优化建议"""
    summary = get_summary(records)
    campaigns = group_by_campaign(records)

    recommendations = []
    for name, c in campaigns.items():
        cpa = c.get("cpa", 0)
        roas = c.get("roas", 0)
        cost = c.get("cost", 0)
        conversions = c.get("conversions", 0)

        if cost < 100 or conversions < 5:
            recommendations.append({
                "plan": name,
                "action": "数据不足",
                "reason": "消耗<100元或转化<5个，数据量不足以做判断",
                "suggestion": "继续观察，至少积累20个转化后再优化"
            })
            continue

        if roas > 3.0 and conversions >= 20:
            recommendations.append({
                "plan": name,
                "action": "建议加量",
                "current_roas": round(roas, 2),
                "current_cpa": round(cpa, 2),
                "reason": "ROAS优秀且转化稳定",
                "suggestion": "预算可加20-30%，出价可适当上调5-10%抢占更多量"
            })
        elif roas >= 1.5:
            recommendations.append({
                "plan": name,
                "action": "维持观察",
                "current_roas": round(roas, 2),
                "current_cpa": round(cpa, 2),
                "reason": "ROAS尚可，需观察趋势",
                "suggestion": "维持当前出价和预算，关注3天趋势"
            })
        elif roas >= 1.0:
            recommendations.append({
                "plan": name,
                "action": "谨慎观望",
                "current_roas": round(roas, 2),
                "current_cpa": round(cpa, 2),
                "reason": "ROAS偏低仅持平",
                "suggestion": "降低出价10-15%或缩减预算，观察2天后无改善则关停"
            })
        else:
            recommendations.append({
                "plan": name,
                "action": "建议关停或大幅调整",
                "current_roas": round(roas, 2),
                "current_cpa": round(cpa, 2),
                "reason": "ROAS < 1，纯亏损",
                "suggestion": "立即关停，重新设计素材和人群策略后再测试"
            })

    return {
        "summary": {
            "avg_cpa": summary.get("avg_cpa", 0),
            "avg_roas": summary.get("roas", 0),
            "total_cost": summary.get("total_cost", 0),
        },
        "recommendations": recommendations,
        "general_advice": _general_bid_advice(summary),
    }


def _general_bid_advice(summary: dict) -> list:
    """通用出价建议"""
    advice = []
    roas = summary.get("roas", 0)
    cpa = summary.get("avg_cpa", 0)
    ctr = summary.get("avg_ctr", 0)
    cvr = summary.get("avg_cvr", 0)

    if roas < 1.0:
        advice.append("当前ROAS<1，首要任务是止损。建议：1.关停低效计划 2.检查落地页转化率 3.重新评估产品定价")

    if ctr < 1.5:
        advice.append(f"CTR仅{ctr}%，素材吸引力不足。建议：更换3-5套不同风格素材同时测试，找到高CTR方向")

    if cvr < 2:
        advice.append(f"CVR仅{cvr}%，转化链路有问题。建议：检查落地页加载速度、优化转化表单、突出核心卖点")

    if cpa > 80:
        advice.append(f"CPA ¥{cpa:.0f}偏高。建议：1.检查出价策略 2.排除已转化人群 3.测试更多人群包")

    if not advice:
        advice.append("当前指标整体健康，保持现有策略，持续监控趋势变化")

    return advice


def creative_analysis(records: list) -> dict:
    """素材分析和疲劳度检测"""
    # 按创意/素材聚合
    creatives = defaultdict(lambda: {"impressions": 0, "clicks": 0, "cost": 0, "conversions": 0, "revenue": 0, "dates": set()})
    for r in records:
        creative = r.get("creative", "未命名")
        creatives[creative]["impressions"] += r.get("impressions", 0) or 0
        creatives[creative]["clicks"] += r.get("clicks", 0) or 0
        creatives[creative]["cost"] += r.get("cost", 0) or 0
        creatives[creative]["conversions"] += r.get("conversions", 0) or 0
        creatives[creative]["revenue"] += r.get("revenue", 0) or 0
        date_str = str(r.get("date", ""))
        if date_str:
            creatives[creative]["dates"].add(date_str)

    creative_list = []
    for name, c in creatives.items():
        info = {"name": name}
        impr = c["impressions"]
        clk = c["clicks"]
        cost = c["cost"]
        conv = c["conversions"]
        rev = c["revenue"]

        info["impressions"] = impr
        info["clicks"] = clk
        info["cost"] = round(cost, 2)
        info["conversions"] = conv
        info["revenue"] = round(rev, 2)
        info["active_days"] = len(c["dates"])
        info["ctr"] = round(clk / impr * 100, 2) if impr > 0 else 0
        info["cvr"] = round(conv / clk * 100, 2) if clk > 0 else 0
        info["cpa"] = round(cost / conv, 2) if conv > 0 else 0
        info["roas"] = round(rev / cost, 2) if cost > 0 else 0

        # 疲劳度评估
        fatigue = _assess_fatigue(info)
        info["fatigue"] = fatigue

        creative_list.append(info)

    # 排序
    creative_list.sort(key=lambda x: x.get("roas", 0), reverse=True)

    # 素材健康度统计
    fresh = sum(1 for c in creative_list if c["fatigue"]["level"] == "健康")
    warning = sum(1 for c in creative_list if c["fatigue"]["level"] == "注意")
    fatigued = sum(1 for c in creative_list if c["fatigue"]["level"] == "疲劳")

    top_creative = creative_list[0] if creative_list else None
    worst_creative = creative_list[-1] if creative_list else None

    return {
        "total_creatives": len(creative_list),
        "health": {"fresh": fresh, "warning": warning, "fatigued": fatigued},
        "top_performer": top_creative,
        "worst_performer": worst_creative,
        "all_creatives": creative_list,
        "recommendations": _creative_recommendations(creative_list),
    }


def _assess_fatigue(creative: dict) -> dict:
    """评估单个素材的疲劳度"""
    ctr = creative.get("ctr", 0)
    days = creative.get("active_days", 0)
    impressions = creative.get("impressions", 0)
    roas = creative.get("roas", 0)

    if impressions < 1000:
        return {"level": "健康", "score": 100, "message": "曝光量低，素材仍新鲜"}

    # 基于CTR和活跃天数综合评估
    fatigue_score = 100

    if ctr < 1.0:
        fatigue_score -= 30
    elif ctr < 1.5:
        fatigue_score -= 15

    if days > 14:
        fatigue_score -= 25
    elif days > 7:
        fatigue_score -= 10

    if roas < 1.0:
        fatigue_score -= 20
    elif roas < 1.5:
        fatigue_score -= 10

    if fatigue_score >= 70:
        level = "健康"
        message = "素材表现良好，可持续投放"
    elif fatigue_score >= 40:
        level = "注意"
        message = "素材有衰减迹象，建议准备备选素材"
    else:
        level = "疲劳"
        message = "素材已疲劳，建议立即更换"

    return {"level": level, "score": max(0, fatigue_score), "message": message}


def _creative_recommendations(creative_list: list) -> list:
    """素材优化建议"""
    recommendations = []

    top3 = creative_list[:3]
    if top3:
        recommendations.append({
            "type": "优胜素材",
            "priority": "P0",
            "message": f"表现最佳: {top3[0]['name']} (ROAS={top3[0].get('roas', 0)}, CTR={top3[0].get('ctr', 0)}%)",
            "action": "分析优胜素材特征（颜色/文案/卖点），复用成功元素"
        })

    fatigued = [c for c in creative_list if c["fatigue"]["level"] == "疲劳"]
    if fatigued:
        recommendations.append({
            "type": "素材替换",
            "priority": "P0",
            "message": f"{len(fatigued)}个素材已疲劳: {', '.join(c['name'] for c in fatigued)}",
            "action": "立即准备替换素材，每套准备3-5个变体"
        })

    warning = [c for c in creative_list if c["fatigue"]["level"] == "注意"]
    if warning:
        recommendations.append({
            "type": "素材预警",
            "priority": "P1",
            "message": f"{len(warning)}个素材有衰减迹象",
            "action": "提前准备备选素材，72小时内轮换"
        })

    if len(creative_list) < 5:
        recommendations.append({
            "type": "素材储备",
            "priority": "P1",
            "message": "素材数量不足5个",
            "action": "建议每周新增3-5套新素材，保持素材池活跃度"
        })

    return recommendations


def ab_test_analysis(records: list, creative_a: str, creative_b: str) -> dict:
    """A/B测试分析"""
    creatives = creative_analysis(records)
    all_creatives = {c["name"]: c for c in creatives.get("all_creatives", [])}

    a = all_creatives.get(creative_a)
    b = all_creatives.get(creative_b)

    if not a or not b:
        return {"error": "指定的素材在数据中未找到"}

    def better(a_val, b_val, metric, lower_is_better=False):
        if a_val == b_val:
            return "平手"
        if lower_is_better:
            return creative_a if a_val < b_val else creative_b
        return creative_a if a_val > b_val else creative_b

    def winner_count(a_name, b_name, results):
        a_wins = sum(1 for v in results.values() if v == a_name)
        b_wins = sum(1 for v in results.values() if v == b_name)
        return a_wins, b_wins

    results = {
        "CTR": better(a.get("ctr", 0), b.get("ctr", 0), "CTR"),
        "CVR": better(a.get("cvr", 0), b.get("cvr", 0), "CVR"),
        "CPA": better(a.get("cpa", 999), b.get("cpa", 999), "CPA", lower_is_better=True),
        "ROAS": better(a.get("roas", 0), b.get("roas", 0), "ROAS"),
    }
    a_wins, b_wins = winner_count(creative_a, creative_b, results)

    if a_wins > b_wins:
        overall_winner = creative_a
    elif b_wins > a_wins:
        overall_winner = creative_b
    else:
        overall_winner = "平手"

    return {
        "creative_a": a,
        "creative_b": b,
        "comparison": {
            "CTR": f"{a.get('ctr', 0)}% vs {b.get('ctr', 0)}% → {results['CTR']}胜出",
            "CVR": f"{a.get('cvr', 0)}% vs {b.get('cvr', 0)}% → {results['CVR']}胜出",
            "CPA": f"¥{a.get('cpa', 0)} vs ¥{b.get('cpa', 0)} → {results['CPA']}胜出",
            "ROAS": f"{a.get('roas', 0)} vs {b.get('roas', 0)} → {results['ROAS']}胜出",
        },
        "overall_winner": overall_winner,
        "recommendation": f"综合评估，{overall_winner}表现更优，建议作为主力素材" if overall_winner != "平手" else "两者表现接近，可同时保留观察"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python optimizer.py <数据文件路径> [--budget] [--bid] [--creative] [--ab A B]")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        records, platform, meta = load_file(file_path)

        if "--budget" in sys.argv:
            result = budget_allocation(records)
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        elif "--bid" in sys.argv:
            result = bid_optimizer(records)
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        elif "--creative" in sys.argv:
            result = creative_analysis(records)
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        elif "--ab" in sys.argv:
            idx = sys.argv.index("--ab")
            if idx + 2 < len(sys.argv):
                result = ab_test_analysis(records, sys.argv[idx + 1], sys.argv[idx + 2])
                print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            # 默认全部
            result = {
                "budget": budget_allocation(records),
                "bid": bid_optimizer(records),
                "creative": creative_analysis(records),
            }
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
