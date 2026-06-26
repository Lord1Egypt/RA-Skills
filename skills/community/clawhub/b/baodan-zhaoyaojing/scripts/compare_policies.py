#!/usr/bin/env python3
"""
保单照妖镜 - 保单权益保障PK擂台
意外险保单比较引擎 V1.0.0
作者: WuWenBin-BeiJing-ST

输入：两份保单的结构化JSON（含理赔口碑数据）
输出：比较结果（七维度打分+建议+坑点+理赔口碑评估）
"""

import json
import sys
import argparse
from pathlib import Path


# ═══════════════════════════════════════
# 维度配置 - 七维度
# ═══════════════════════════════════════

DIMENSION_WEIGHTS = {
    "coverage_scope": 25,
    "amount_ratio": 18,
    "deductible_waiting": 12,
    "exclusions": 18,
    "premium_value": 10,
    "claim_conditions": 7,
    "claim_reputation": 10,
}

DIMENSION_LABELS = {
    "coverage_scope": {"icon": "🟢", "question": "保障够不够全？", "pro_name": "保障范围"},
    "amount_ratio": {"icon": "💰", "question": "出事了赔多少？", "pro_name": "保额与赔付比例"},
    "deductible_waiting": {"icon": "🏥", "question": "多少钱以下不赔？等多久生效？", "pro_name": "免赔额与等待期"},
    "exclusions": {"icon": "⚠️", "question": "什么情况不赔？（坑多不多？）", "pro_name": "除外责任"},
    "premium_value": {"icon": "📊", "question": "划不划算？", "pro_name": "保费与性价比"},
    "claim_conditions": {"icon": "📑", "question": "条款写的理赔好不好走？", "pro_name": "理赔条件与流程"},
    "claim_reputation": {"icon": "🔍", "question": "真出事了赔不赔得到？（真实口碑）", "pro_name": "理赔口碑（实时搜索）"},
}


# ═══════════════════════════════════════
# 打分函数（维度1-6）
# ═══════════════════════════════════════

def score_coverage_scope(dim):
    """保障范围打分"""
    s = 0
    if dim.get("accidental_death", {}).get("covered"):
        s += 20
    if dim.get("accidental_disability", {}).get("covered"):
        s += 15
    if dim.get("accidental_medical", {}).get("covered"):
        s += 20
        if dim.get("accidental_medical", {}).get("social_insurance_only"):
            s -= 10
    if dim.get("sudden_death", {}).get("covered"):
        s += 10
    else:
        s -= 5
    traffic = dim.get("traffic_extra", {})
    if any(v.get("covered") for v in traffic.values() if isinstance(v, dict)):
        s += 15
    if dim.get("hospital_daily_allowance", {}).get("covered"):
        s += 10
    if dim.get("ambulance", {}).get("covered"):
        s += 5
    if dim.get("other_coverages"):
        s += 5
    return max(0, min(100, s))


def score_amount_ratio(dim, premium):
    """保额与赔付比例打分"""
    s = 0
    death_amt = dim.get("accidental_death", {}).get("amount") or 0
    if death_amt >= 1000000:
        s += 30
    elif death_amt >= 500000:
        s += 20
    else:
        s += 10

    med = dim.get("accidental_medical", {})
    med_amt = med.get("amount") or 0
    if med_amt >= 50000:
        s += 25
    elif med_amt >= 20000:
        s += 15
    else:
        s += 8

    ratio_str = med.get("reimbursement_ratio", "0%")
    try:
        ratio = int(ratio_str.replace("%", ""))
    except (ValueError, AttributeError):
        ratio = 0
    if ratio >= 100:
        s += 20
    elif ratio >= 80:
        s += 15
    else:
        s += 8

    traffic = dim.get("traffic_extra", {})
    aviation = traffic.get("aviation", {}).get("amount") or 0
    if aviation >= 2000000:
        s += 15
    elif aviation >= 1000000:
        s += 10
    else:
        s += 5

    grading = dim.get("accidental_disability", {}).get("grading", "")
    if "1-10" in grading or "十级" in grading:
        s += 10
    else:
        s += 5

    return max(0, min(100, s))


def score_deductible_waiting(dim):
    """免赔额与等待期打分"""
    s = 0
    ded = dim.get("medical_deductible", 999)
    if ded == 0:
        s += 40
    elif ded < 100:
        s += 30
    elif ded < 200:
        s += 20
    else:
        s += 10

    wait = dim.get("waiting_period_days", 999)
    if wait == 0:
        s += 35
    elif wait <= 7:
        s += 25
    elif wait <= 30:
        s += 15
    else:
        s += 5

    if dim.get("single_claim_limit") is None and dim.get("annual_limit") is None:
        s += 25
    elif dim.get("annual_limit") is None:
        s += 15
    else:
        s += 8

    return max(0, min(100, s))


def score_exclusions(dim):
    """除外责任打分（坑越少分越高）"""
    s = 100

    occ = dim.get("occupation_limit", "")
    if "1-3" in occ:
        s -= 15
    elif "1-4" in occ:
        s -= 10
    elif "1-5" in occ:
        s -= 5

    if dim.get("high_risk_sports"):
        s -= 15

    if dim.get("pre_existing"):
        s -= 5

    for _ in dim.get("specific_regions", []):
        s -= 5

    for _ in dim.get("other_key_exclusions", []):
        s -= 5

    return max(0, min(100, s))


def score_premium_value(policy):
    """性价比打分"""
    premium = policy.get("premium_annual", 1) or 1
    death_amt = (policy.get("dimensions", {})
                 .get("coverage_scope", {})
                 .get("accidental_death", {})
                 .get("amount") or 1)

    leverage = death_amt / premium

    if leverage >= 1000:
        s = 100
    elif leverage >= 500:
        s = 80
    elif leverage >= 300:
        s = 60
    elif leverage >= 100:
        s = 40
    else:
        s = 20
    return s


def score_claim_conditions(dim):
    """理赔条件打分"""
    s = 0
    if dim.get("online_claim"):
        s += 30

    days = dim.get("claim_processing_days") or 999
    if days <= 3:
        s += 30
    elif days <= 7:
        s += 20
    elif days <= 15:
        s += 10
    else:
        s += 5

    hosp = dim.get("hospital_scope", "")
    if "私立" in hosp:
        s += 25
    elif "公立" in hosp:
        s += 15
    else:
        s += 10

    materials = dim.get("required_materials", [])
    if len(materials) <= 3:
        s += 15
    elif len(materials) <= 5:
        s += 10
    else:
        s += 5

    return max(0, min(100, s))


# ═══════════════════════════════════════
# 打分函数（维度7：理赔口碑）
# ═══════════════════════════════════════

def score_claim_reputation(dim):
    """
    理赔口碑打分（基于搜索数据）

    输入: claim_reputation 维度数据
    输出: (score, has_data)
      - score: 0-100 分数，或 None（无数据）
      - has_data: bool
    """
    if not dim.get("search_conducted") or not dim.get("data_available"):
        return None, False

    s = 0

    # 用户反馈理赔时效（30分）
    avg_days = dim.get("avg_claim_days_reported")
    if avg_days is not None:
        if avg_days <= 7:
            s += 30
        elif avg_days <= 15:
            s += 22
        elif avg_days <= 30:
            s += 14
        else:
            s += 6

    # 投诉量等级（25分）
    complaint_vol = dim.get("complaint_volume", "未知")
    vol_scores = {"低": 25, "中": 15, "高": 5, "未知": 10}
    s += vol_scores.get(complaint_vol, 10)

    # 常见投诉类型扣分（20分基准，有坑扣分）
    s += 20
    common_complaints = dim.get("common_complaints", [])
    for c in common_complaints:
        if "拖赔" in c or "拖延" in c:
            s -= 10
        elif "拒赔" in c:
            s -= 10
        elif "材料" in c and ("反复" in c or "补充" in c):
            s -= 5

    # 正面反馈比例（15分）
    positive = dim.get("positive_feedback", [])
    sources = dim.get("sources", [])
    if sources:
        positive_ratio = sum(1 for src in sources if src.get("sentiment") == "positive") / len(sources)
        if positive_ratio >= 0.7:
            s += 15
        elif positive_ratio >= 0.4:
            s += 10
        else:
            s += 5
    else:
        s += 7

    # 监管披露结案率（10分）
    reg = dim.get("regulatory_data", {})
    if reg.get("has_data"):
        rate_str = reg.get("settlement_rate", "")
        try:
            rate = float(rate_str.replace("%", ""))
        except (ValueError, AttributeError):
            rate = 0
        if rate >= 98:
            s += 10
        elif rate >= 95:
            s += 7
        elif rate > 0:
            s += 3
    else:
        s += 5  # 无监管数据给中间分

    return max(0, min(100, s)), True


# ═══════════════════════════════════════
# 综合评分
# ═══════════════════════════════════════

def grade_letter(score):
    if score >= 95: return "A+"
    if score >= 85: return "A"
    if score >= 80: return "A-"
    if score >= 75: return "B+"
    if score >= 70: return "B"
    if score >= 65: return "B-"
    if score >= 60: return "C+"
    if score >= 55: return "C"
    return "D"


def score_policy(policy):
    """对单张保单打分，返回各维度分数和总分"""
    dims = policy.get("dimensions", {})
    scores = {}

    scores["coverage_scope"] = score_coverage_scope(dims.get("coverage_scope", {}))
    scores["amount_ratio"] = score_amount_ratio(dims.get("coverage_scope", {}), policy.get("premium_annual", 0))
    scores["deductible_waiting"] = score_deductible_waiting(dims.get("deductible_and_waiting", {}))
    scores["exclusions"] = score_exclusions(dims.get("exclusions", {}))
    scores["premium_value"] = score_premium_value(policy)
    scores["claim_conditions"] = score_claim_conditions(dims.get("claim_conditions", {}))

    # 维度7：理赔口碑（可能无数据）
    rep_score, has_rep_data = score_claim_reputation(dims.get("claim_reputation", {}))
    scores["claim_reputation"] = rep_score

    # 计算总分：如果理赔口碑无数据，其余六维度归一化
    if has_rep_data and rep_score is not None:
        total = sum(scores[k] * w for k, w in DIMENSION_WEIGHTS.items() if scores[k] is not None) / 100
    else:
        # 归一化：去掉理赔口碑的10%权重
        active_weight_sum = sum(w for k, w in DIMENSION_WEIGHTS.items() if k != "claim_reputation")
        total = sum(scores[k] * (DIMENSION_WEIGHTS[k] / active_weight_sum * 100)
                    for k, w in DIMENSION_WEIGHTS.items() if k != "claim_reputation") / 100

    return scores, round(total, 1), grade_letter(total), has_rep_data


# ═══════════════════════════════════════
# 比较与建议生成
# ═══════════════════════════════════════

def compare(policy_a, policy_b):
    """比较两份保单，返回完整比较结果"""
    scores_a, total_a, grade_a, has_rep_a = score_policy(policy_a)
    scores_b, total_b, grade_b, has_rep_b = score_policy(policy_b)

    # 逐维度判定
    dim_verdicts = {}
    for dim_key in DIMENSION_WEIGHTS:
        sa, sb = scores_a.get(dim_key), scores_b.get(dim_key)
        if sa is None or sb is None:
            dim_verdicts[dim_key] = "no_data"
        elif sa > sb + 10:
            dim_verdicts[dim_key] = "a_better"
        elif sb > sa + 10:
            dim_verdicts[dim_key] = "b_better"
        else:
            dim_verdicts[dim_key] = "similar"

    # 生成坑点
    pitfalls = []
    for label, policy, prefix in [("A", policy_a, "保单A"), ("B", policy_b, "保单B")]:
        dims = policy.get("dimensions", {})
        cs = dims.get("coverage_scope", {})
        if not cs.get("sudden_death", {}).get("covered"):
            pitfalls.append(f"{prefix} **不含猝死**！经常加班的打工人要特别注意")
        dw = dims.get("deductible_and_waiting", {})
        if dw.get("medical_deductible", 0) > 0:
            pitfalls.append(f"{prefix} 有 **{dw['medical_deductible']}元免赔额**，低于此金额不报销")
        if dw.get("waiting_period_days", 0) > 0:
            pitfalls.append(f"{prefix} 有 **{dw['waiting_period_days']}天等待期**，期间出险不赔")
        if cs.get("accidental_medical", {}).get("social_insurance_only"):
            pitfalls.append(f"{prefix} **限社保内用药**，自费药、进口药不报")
        ex = dims.get("exclusions", {})
        if "1-3" in ex.get("occupation_limit", ""):
            pitfalls.append(f"{prefix} 限 **1-3类职业**，4类以上不保")
        if ex.get("high_risk_sports"):
            pitfalls.append(f"{prefix} **不保高风险运动**（攀岩、跳伞等）")

    # 理赔口碑坑点
    for label, policy, prefix in [("A", policy_a, "保单A"), ("B", policy_b, "保单B")]:
        rep = policy.get("dimensions", {}).get("claim_reputation", {})
        if not rep.get("data_available"):
            pitfalls.append(f"{prefix} ⚠️ **理赔口碑数据不足**，建议付费咨询专业保险顾问")
        else:
            for c in rep.get("common_complaints", []):
                if "拖赔" in c or "拖延" in c:
                    pitfalls.append(f"{prefix} 🔴 有用户反馈 **理赔拖延**，到账慢")
                elif "拒赔" in c:
                    pitfalls.append(f"{prefix} 🔴 有投诉 **以各种理由拒赔**")

    # 生成场景建议
    recommendations = []

    ded_a = policy_a.get("dimensions", {}).get("deductible_and_waiting", {}).get("medical_deductible", 999)
    ded_b = policy_b.get("dimensions", {}).get("deductible_and_waiting", {}).get("medical_deductible", 999)
    if ded_a == 0 and ded_b > 0:
        recommendations.append(("👨‍💻", "如果你是 **办公室上班族** → 选保单A，0免赔，日常小意外最实用"))
    elif ded_b == 0 and ded_a > 0:
        recommendations.append(("👨‍💻", "如果你是 **办公室上班族** → 选保单B，0免赔，日常小意外最实用"))

    traffic_a = policy_a.get("dimensions", {}).get("coverage_scope", {}).get("traffic_extra", {})
    traffic_b = policy_b.get("dimensions", {}).get("coverage_scope", {}).get("traffic_extra", {})
    a_traffic_max = max((v.get("amount") or 0 for v in traffic_a.values() if isinstance(v, dict)), default=0)
    b_traffic_max = max((v.get("amount") or 0 for v in traffic_b.values() if isinstance(v, dict)), default=0)
    if a_traffic_max > b_traffic_max:
        recommendations.append(("✈️", "如果你 **经常出差/自驾** → 选保单A，交通额外赔付更高"))
    elif b_traffic_max > a_traffic_max:
        recommendations.append(("✈️", "如果你 **经常出差/自驾** → 选保单B，交通额外赔付更高"))

    if scores_b.get("premium_value", 0) > scores_a.get("premium_value", 0) + 10:
        recommendations.append(("💰", "如果你 **关注性价比** → 选保单B，保障杠杆更高"))
    elif scores_a.get("premium_value", 0) > scores_b.get("premium_value", 0) + 10:
        recommendations.append(("💰", "如果你 **关注性价比** → 选保单A，保障杠杆更高"))

    occ_a = policy_a.get("dimensions", {}).get("exclusions", {}).get("occupation_limit", "1-6类")
    occ_b = policy_b.get("dimensions", {}).get("exclusions", {}).get("occupation_limit", "1-6类")
    if "1-3" in occ_a and "1-6" in occ_b:
        recommendations.append(("💪", "如果你是 **高风险职业** → 只能选保单B，A不保4类以上"))
    elif "1-3" in occ_b and "1-6" in occ_a:
        recommendations.append(("💪", "如果你是 **高风险职业** → 只能选保单A，B不保4类以上"))

    sport_a = policy_a.get("dimensions", {}).get("exclusions", {}).get("high_risk_sports", False)
    sport_b = policy_b.get("dimensions", {}).get("exclusions", {}).get("high_risk_sports", False)
    if sport_a and sport_b:
        recommendations.append(("🧗", "如果你 **喜欢户外运动** → 两个都不太合适，建议找含高风险运动的专项意外险"))

    # 理赔口碑建议
    if has_rep_a and has_rep_b:
        rep_score_a = scores_a.get("claim_reputation") or 0
        rep_score_b = scores_b.get("claim_reputation") or 0
        if rep_score_a > rep_score_b + 15:
            recommendations.append(("🔍", "如果你 **担心理赔扯皮** → 选保单A，真实理赔口碑更好"))
        elif rep_score_b > rep_score_a + 15:
            recommendations.append(("🔍", "如果你 **担心理赔扯皮** → 选保单B，真实理赔口碑更好"))

    return {
        "policy_a": {"name": policy_a.get("policy_name", "保单A"),
                     "insurer": policy_a.get("insurer", ""),
                     "premium": policy_a.get("premium_annual", 0),
                     "scores": scores_a, "total": total_a, "grade": grade_a,
                     "has_reputation_data": has_rep_a},
        "policy_b": {"name": policy_b.get("policy_name", "保单B"),
                     "insurer": policy_b.get("insurer", ""),
                     "premium": policy_b.get("premium_annual", 0),
                     "scores": scores_b, "total": total_b, "grade": grade_b,
                     "has_reputation_data": has_rep_b},
        "dim_verdicts": dim_verdicts,
        "pitfalls": pitfalls,
        "recommendations": recommendations,
    }


# ═══════════════════════════════════════
# 主入口
# ═══════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="保单照妖镜 - 保单权益保障PK擂台 V1.0.0")
    parser.add_argument("--policy-a", required=True, help="保单A JSON文件路径")
    parser.add_argument("--policy-b", required=True, help="保单B JSON文件路径")
    parser.add_argument("--output", default=None, help="输出结果JSON路径")
    args = parser.parse_args()

    with open(args.policy_a) as f:
        policy_a = json.load(f)
    with open(args.policy_b) as f:
        policy_b = json.load(f)

    result = compare(policy_a, policy_b)
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✅ 比较结果已保存到 {args.output}")
    else:
        print(output)
