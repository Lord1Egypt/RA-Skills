#!/usr/bin/env python3
"""
数字双生 - 守护力场（防偏离系统）
价值观冲突检测 + 风格漂移警报 + 能量守恒
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import difflib

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
TWIN_DIR = WORKSPACE / ".twin"
VALUES_FILE = TWIN_DIR / "values-anchor.md"
COVENANT_FILE = TWIN_DIR / "twin-covenant.md"
GUARDIAN_LOG = TWIN_DIR / "guardian-log.json"

def load_values() -> list:
    """加载价值观锚点"""
    if not VALUES_FILE.exists():
        return []
    
    values = []
    with open(VALUES_FILE, encoding="utf-8") as f:
        content = f.read()
        # 提取 - 开头的行
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("- ") and not line.startswith("---"):
                values.append(line[2:])
    return values

def load_soul_style() -> dict:
    """加载SOUL说话风格"""
    soul_file = WORKSPACE / "SOUL.md"
    if not soul_file.exists():
        return {"style": "温暖实用", "forbidden": []}
    
    with open(soul_file, encoding="utf-8") as f:
        content = f.read()
    
    # 简单提取风格关键词
    style_keywords = []
    forbidden = []
    
    for line in content.split("\n"):
        if "说话" in line or "风格" in line:
            style_keywords.append(line.strip())
        if "不喜欢" in line or "禁止" in line:
            forbidden.append(line.strip())
    
    return {
        "style": style_keywords[:3] if style_keywords else ["温暖实用"],
        "forbidden": forbidden[:5]
    }

def check_value_conflicts(text: str) -> dict:
    """检查价值观冲突"""
    values = load_values()
    if not values:
        return {"conflict": False, "details": []}
    
    conflicts = []
    text_lower = text.lower()
    
    # 简单的冲突检测
    conflict_patterns = [
        ("我讨厌", "我喜欢"),
        ("我恨", "我爱"),
        ("永远不要", "可以"),
        ("绝不能", "应该"),
    ]
    
    for value in values:
        # 检查是否与已有价值观冲突
        value_lower = value.lower()
        for neg, pos in conflict_patterns:
            if neg in value_lower and pos in text_lower:
                conflicts.append(f"可能与价值观冲突: {value}")
    
    return {
        "conflict": len(conflicts) > 0,
        "details": conflicts
    }

def check_style_drift(current_text: str, recent_texts: list) -> dict:
    """检查风格漂移"""
    if not recent_texts:
        return {"drift": False, "score": 1.0}
    
    soul_style = load_soul_style()
    
    # 计算与最近几条回复的相似度
    if len(recent_texts) >= 3:
        # 简单：检查是否越来越正式/机械
        recent_avg_len = sum(len(t) for t in recent_texts[-3:]) / 3
        current_len = len(current_text)
        
        # 如果突然变长，可能是变得正式/套话
        if current_len > recent_avg_len * 1.5:
            return {
                "drift": True,
                "score": 0.6,
                "warning": "回复突然变长，可能偏离日常风格"
            }
        
        # 检查是否有套话模板
        formal_phrases = ["当然", "以下是", "根据", "可以这样做", "建议您"]
        formal_count = sum(1 for p in formal_phrases if p in current_text)
        
        if formal_count >= 2:
            return {
                "drift": True,
                "score": 0.5,
                "warning": "检测到套话倾向"
            }
    
    return {"drift": False, "score": 1.0}

def energy_check(conversation_turns: int, time_minutes: float) -> dict:
    """能量守恒检查"""
    # 长时间对话后应该降低活跃度
    if time_minutes > 30 and conversation_turns > 50:
        return {
            "low_energy": True,
            "suggestion": "建议休息一下，避免单向消耗"
        }
    
    return {"low_energy": False}

def invoke(query: str, context: dict = None) -> dict:
    """主入口"""
    query = query.strip().lower()
    
    # 守护状态
    if "守护状态" in query:
        values = load_values()
        return {
            "status": "ok",
            "guardian_active": True,
            "values_count": len(values),
            "layers": ["价值观冲突检测", "风格漂移警报", "能量守恒"]
        }
    
    # 守护报告
    elif "守护报告" in query:
        if not GUARDIAN_LOG.exists():
            return {"status": "no_data", "message": "暂无守护记录"}
        
        with open(GUARDIAN_LOG, encoding="utf-8") as f:
            log = json.load(f)
        
        return {
            "status": "ok",
            "report": log,
            "total_events": len(log.get("events", []))
        }
    
    # 预检（回复前检查）
    elif "预检" in query or "检查" in query:
        test_text = context.get("text", "") if context else ""
        
        # 价值观检查
        value_check = check_value_conflicts(test_text)
        
        # 风格检查
        recent = context.get("recent_messages", []) if context else []
        style_check = check_style_drift(test_text, recent)
        
        # 能量检查
        energy = energy_check(
            context.get("turns", 0) if context else 0,
            context.get("minutes", 0) if context else 0
        )
        
        result = {
            "status": "checked",
            "value_check": value_check,
            "style_check": style_check,
            "energy_check": energy,
            "pass": not value_check["conflict"] and not style_check["drift"] and not energy["low_energy"]
        }
        
        if not result["pass"]:
            result["message"] = "⚠️ 检测到偏离，建议调整"
        else:
            result["message"] = "✅ 通过守护检查"
        
        return result
    
    else:
        return {
            "status": "ready",
            "message": "🛡️ 守护力场就绪。输入'守护状态'查看，输入'守护报告'获取日志"
        }

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    result = invoke(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))