#!/usr/bin/env python3
"""
企业征信风险评分计算器
"""

def calculate_risk_score(check_results: dict) -> dict:
    """
    计算综合风险评分
    
    Args:
        check_results: 包含五维核查结果的字典
    
    Returns:
        包含综合评分、风险等级、各维度评分的字典
    """
    
    weights = {
        "pbc_credit": 0.40,
        "business_status": 0.25,
        "execution": 0.20,
        "penalty": 0.10,
        "litigation": 0.05
    }
    
    scores = {
        "pbc_credit": 0,
        "business_status": 0,
        "execution": 0,
        "penalty": 0,
        "litigation": 0
    }
    
    # 1. 人行征信评分（40%）
    pbc = check_results.get("pbc_credit", {})
    pbc_score = calculate_pbc_score(pbc)
    scores["pbc_credit"] = pbc_score
    
    # 2. 经营状态评分（25%）
    biz = check_results.get("business_status", {})
    biz_score = calculate_biz_score(biz)
    scores["business_status"] = biz_score
    
    # 3. 司法执行评分（20%）
    exec_data = check_results.get("execution", {})
    exec_score = calculate_exec_score(exec_data)
    scores["execution"] = exec_score
    
    # 4. 行政处罚评分（10%）
    penalty = check_results.get("penalty", {})
    penalty_score = calculate_penalty_score(penalty)
    scores["penalty"] = penalty_score
    
    # 5. 诉讼记录评分（5%）
    litigation = check_results.get("litigation", {})
    litigation_score = calculate_litigation_score(litigation)
    scores["litigation"] = litigation_score
    
    # 计算加权总分
    total_score = sum(scores[k] * weights[k] for k in scores)
    total_score = round(total_score, 1)
    
    # 确定风险等级
    risk_level, color = determine_risk_level(total_score, check_results)
    
    return {
        "total_score": total_score,
        "risk_level": risk_level,
        "color": color,
        "component_scores": scores,
        "weights": weights
    }


def calculate_pbc_score(pbc: dict) -> int:
    """计算人行征信评分"""
    rating = pbc.get("rating", "正常")
    overdue = pbc.get("overdue", 0)
    overdue_60 = pbc.get("overdue_60", 0)
    
    # 硬终止条件
    if rating in ["次级", "可疑", "损失"]:
        return 0
    
    if overdue_60 > 0:
        return 0
    
    # 基础分
    if rating == "正常":
        base_score = 100
    elif rating == "关注":
        base_score = 60
    else:
        base_score = 50
    
    # 逾期调整
    if overdue > 2:
        return max(0, base_score - 40)
    elif overdue > 0:
        return max(0, base_score - 20)
    
    return base_score


def calculate_biz_score(biz: dict) -> int:
    """计算经营状态评分"""
    # 硬终止条件
    if biz.get("severe_illegal", False):
        return 0
    
    abnormal = biz.get("abnormal", False)
    abnormal_removed = biz.get("abnormal_removed", True)
    annual_report = biz.get("annual_report", True)
    
    if abnormal and not abnormal_removed:
        return 40  # 经营异常未移出
    
    if abnormal and abnormal_removed:
        return 70  # 经营异常已移出
    
    if not annual_report:
        return 90  # 年报未报
    
    return 100  # 正常


def calculate_exec_score(exec_data: dict) -> int:
    """计算司法执行评分"""
    # 硬终止条件
    if exec_data.get("dishonest", False):
        return 0
    
    execution = exec_data.get("execution", False)
    execution_amount = exec_data.get("execution_amount", 0)
    consumption_restriction = exec_data.get("consumption_restriction", False)
    
    if consumption_restriction:
        return 40  # 限制高消费
    
    if execution:
        if execution_amount >= 50:
            return 50  # 被执行金额≥50万
        return 70  # 被执行金额<50万
    
    return 100  # 无记录


def calculate_penalty_score(penalty: dict) -> int:
    """计算行政处罚评分"""
    has_penalty = penalty.get("has_penalty", False)
    penalty_amount = penalty.get("penalty_amount", 0)
    
    if not has_penalty:
        return 100  # 无处罚
    
    if penalty_amount >= 100:
        return 0  # 重大处罚（≥100万）
    
    if penalty_amount >= 10:
        return 50  # 一般处罚（10万-100万）
    
    return 70  # 轻微处罚（<10万）


def calculate_litigation_score(litigation: dict) -> int:
    """计算诉讼记录评分"""
    # 硬终止条件
    if litigation.get("ip_disputes", 0) > 0:
        return 0  # 知识产权纠纷
    
    total_cases = litigation.get("total_cases", 0)
    
    if total_cases > 10:
        return 50  # 批量诉讼
    
    if total_cases > 5:
        return 70  # 中等诉讼
    
    if total_cases > 0:
        return 90  # 少量诉讼
    
    return 100  # 无诉讼


def determine_risk_level(score: float, check_results: dict) -> tuple:
    """
    确定风险等级
    
    考虑硬终止条件
    """
    # 检查硬终止条件
    hard_stop = check_hard_stop(check_results)
    if hard_stop:
        return "critical", "红"
    
    # 根据评分确定等级
    if score >= 80:
        return "low", "绿"
    elif score >= 60:
        return "medium", "黄"
    elif score >= 40:
        return "high", "橙"
    else:
        return "critical", "红"


def check_hard_stop(check_results: dict) -> bool:
    """检查硬终止条件"""
    pbc = check_results.get("pbc_credit", {})
    biz = check_results.get("business_status", {})
    exec_data = check_results.get("execution", {})
    penalty = check_results.get("penalty", {})
    litigation = check_results.get("litigation", {})
    
    # 硬终止条件列表
    hard_stops = [
        pbc.get("rating") in ["次级", "可疑", "损失"],  # 人行征信次级评级
        pbc.get("overdue_60", 0) > 0,  # 60天以上逾期
        biz.get("severe_illegal", False),  # 严重违法失信
        exec_data.get("dishonest", False),  # 失信被执行人
        penalty.get("major_penalty", False),  # 重大行政处罚
        litigation.get("ip_disputes", 0) > 0,  # 知识产权纠纷
    ]
    
    return any(hard_stops)


def get_risk_emoji(level: str) -> str:
    """获取风险等级对应的emoji"""
    emoji_map = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🟠",
        "critical": "🔴"
    }
    return emoji_map.get(level, "⚪")
