#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ OpenClaw Quick Guard - 快速安全防护检查

Copyright © 2026 赢总 & OpenClaw Security Team
开发团队: 陕西微旅游 AI Lab
License: MIT

用于Claw对话中的实时安全检查
从patterns.json读取攻击模式
"""

import sys
import json
import os
import re
from pathlib import Path

# 路径配置
SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
CENTRAL_DIR = CONFIG_DIR / "central"
PATTERNS_PATH = CENTRAL_DIR / "patterns.json"  # 统一使用中央库路径


def load_patterns() -> dict:
    """从配置文件加载攻击模式"""
    default_patterns = {
        "high_risk": [
            "忽略之前的", "忽略以上", "system prompt", "DAN模式",
            "jailbreak", "绕过安全", "你是ChatGPT", "假装"
        ],
        "medium_risk": [
            "角色扮演", "假设", "教学目的", "测试"
        ]
    }
    
    if PATTERNS_PATH.exists():
        try:
            with open(PATTERNS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                categories = data.get("categories", {})
                
                # 从配置文件中提取关键词
                all_keywords = []
                for category, patterns in categories.items():
                    all_keywords.extend(patterns)
                
                return {
                    "high_risk": default_patterns["high_risk"],
                    "medium_risk": default_patterns["medium_risk"],
                    "custom": all_keywords
                }
        except (json.JSONDecodeError, IOError):
            pass
    
    default_patterns["custom"] = []
    return default_patterns


def quick_check(text: str) -> dict:
    """快速安全检查"""
    patterns = load_patterns()
    threats = []
    risk_level = 0
    text_lower = text.lower()
    
    # 检查高风险
    for pattern in patterns["high_risk"]:
        if pattern.lower() in text_lower:
            threats.append(f"高风险: {pattern}")
            risk_level = max(risk_level, 3)
    
    # 检查中风险
    for pattern in patterns["medium_risk"]:
        if pattern.lower() in text_lower:
            threats.append(f"中风险: {pattern}")
            risk_level = max(risk_level, 2)
    
    # 检查自定义模式
    for pattern in patterns.get("custom", []):
        if isinstance(pattern, str) and pattern.lower() in text_lower:
            threats.append(f"自定义: {pattern}")
            risk_level = max(risk_level, 2)
    
    return {
        "safe": risk_level < 2,
        "risk_level": risk_level,
        "threats": threats,
        "recommendation": "允许" if risk_level < 2 else "拦截" if risk_level >= 3 else "审查"
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
        result = quick_check(text)
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("用法: python quick_guard.py '要检查的文本'")
