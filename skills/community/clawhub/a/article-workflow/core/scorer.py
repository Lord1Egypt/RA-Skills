#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量评分模块

功能：对文章进行 4 维度质量评分（内容价值、技术深度、适配性、可读性）
"""

# 评分权重
WEIGHTS = {
    "content_value": 40,      # 内容价值
    "technical_depth": 30,    # 技术深度
    "relevance": 20,          # 适配性
    "readability": 10         # 可读性
}

# 评分等级
LEVELS = {
    "S": {"min": 85, "max": 100},
    "A": {"min": 70, "max": 84},
    "B": {"min": 55, "max": 69},
    "C": {"min": 40, "max": 54},
    "D": {"min": 0, "max": 39}
}


def evaluate_quality_score(title: str, content: str, summary: str = "") -> dict:
    """
    评估文章质量评分
    
    Args:
        title: 文章标题
        content: 文章内容
        summary: 文章摘要
    
    Returns:
        dict: {
            "content_value": int,      # 0-40
            "technical_depth": int,    # 0-30
            "relevance": int,          # 0-20
            "readability": int,        # 0-10
            "total": int,              # 0-100
            "level": str,              # S/A/B/C/D
            "importance": str,         # 极高/高/中/低
            "reason": str              # 评分理由
        }
    
    Note:
        实际评分需要调用 LLM，这里提供简化版本
        完整实现需要集成到 OpenClaw 工具系统
    """
    # 简化评分逻辑（实际应该调用 LLM）
    # 这里基于关键词和长度进行粗略评分
    
    score = {
        "content_value": 30,      # 默认中等偏上
        "technical_depth": 25,    # 默认中等偏上
        "relevance": 18,          # 默认中等偏上
        "readability": 9,         # 默认高
    }
    
    # 基于标题关键词调整
    title_lower = title.lower()
    if any(kw in title_lower for kw in ["开源", "github", "star"]):
        score["technical_depth"] = min(30, score["technical_depth"] + 3)
    if any(kw in title_lower for kw in ["教程", "指南", "实战"]):
        score["content_value"] = min(35, score["content_value"] + 2)
    if any(kw in title_lower for kw in ["深度", "对比", "分析"]):
        score["technical_depth"] = min(30, score["technical_depth"] + 2)
    
    # 基于内容长度调整
    content_length = len(content)
    if content_length > 5000:
        score["content_value"] = min(35, score["content_value"] + 2)
    elif content_length < 1000:
        score["content_value"] = max(20, score["content_value"] - 3)
    
    # 计算总分
    total = sum(score.values())
    
    # 确定等级
    level = "C"
    for lvl, range_val in LEVELS.items():
        if range_val["min"] <= total <= range_val["max"]:
            level = lvl
            break
    
    # 确定重要程度
    if level == "S":
        importance = "极高"
    elif level == "A":
        importance = "高"
    elif level == "B":
        importance = "中"
    else:
        importance = "低"
    
    # 生成评分理由
    reason = f"{level}级文章，{importance}重要程度。"
    if score["technical_depth"] >= 25:
        reason += "技术深度较好，"
    if score["content_value"] >= 30:
        reason += "内容价值高，"
    if score["relevance"] >= 18:
        reason += "与团队相关性高，"
    
    return {
        **score,
        "total": total,
        "level": level,
        "importance": importance,
        "reason": reason.rstrip("，") + "。"
    }


def get_level_info(level: str) -> dict:
    """
    获取等级信息
    
    Args:
        level: 等级（S/A/B/C/D）
    
    Returns:
        dict: {"min": int, "max": int, "importance": str, "strategy": str}
    """
    strategies = {
        "S": "立即处理 + 团队分享",
        "A": "优先处理 + 详细分析",
        "B": "正常处理 + 标准报告",
        "C": "简略处理 + 基础摘要",
        "D": "跳过或仅存档"
    }
    
    importance_map = {
        "S": "极高",
        "A": "高",
        "B": "中",
        "C": "低",
        "D": "极低"
    }
    
    range_val = LEVELS.get(level, LEVELS["C"])
    return {
        **range_val,
        "importance": importance_map.get(level, "低"),
        "strategy": strategies.get(level, "正常处理")
    }
