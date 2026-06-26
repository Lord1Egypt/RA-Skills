#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_profile.py - 从对话历史中提取用户画像

Usage:
    python extract_profile.py --conversation "用户对话文本"
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional

# 处理 Windows 控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ============== 画像提取规则 ==============

COMPANION_PATTERNS = {
    "solo": [
        r"一个人", r"独自", r"自己", r"solo", r"alone",
        r"我就一个", r"就我自己"
    ],
    "couple": [
        r"情侣", r"对象", r"男女朋友", r"老公", r"老婆",
        r"男朋友", r"女朋友", r"爱人", r"couple", r"dating"
    ],
    "family": [
        r"带孩子", r"带娃", r"带小孩", r"一家人", r"全家",
        r"带父母", r"带爸妈", r"family", r"with kids", r"with parents"
    ],
    "friends": [
        r"朋友", r"哥们", r"姐妹", r"闺蜜", r"兄弟",
        r"同学", r"同事", r"friends", r"with friends"
    ],
    "elderly": [
        r"带老人", r"陪父母", r"陪长辈", r"老人", r"elderly"
    ]
}

INTEREST_PATTERNS = {
    "photography": [
        r"拍照", r"摄影", r"拍照打卡", r"拍照片", r"出片",
        r"photo", r"photograph", r"picture", r"camera"
    ],
    "history": [
        r"历史", r"文物", r"古代", r"朝代", r"皇帝",
        r"history", r"historical", r"ancient"
    ],
    "culture": [
        r"文化", r"故事", r"典故", r"讲解", r"深度",
        r"culture", r"story", r"deep"
    ],
    "architecture": [
        r"建筑", r"设计", r"结构", r"风格", r"构造",
        r"architecture", r"building", r"design"
    ],
    "nature": [
        r"自然", r"风景", r"山水", r"花园", r"植物",
        r"nature", r"scenery", r"garden"
    ],
    "quick-visit": [
        r"随便逛逛", r"随便看看", r"快速", r"赶时间",
        r"时间紧", r"quick", r"fast", r"brief"
    ]
}

TIME_PATTERNS = {
    "1h": [
        r"1 小时", r"一小时", r"一个小时", r"很快", r"马上走",
        r"1 hour", r"one hour", r"quick"
    ],
    "2-3h": [
        r"2 小时", r"3 小时", r"两三个小时", r"半天不到",
        r"2 hours", r"3 hours", r"half day"
    ],
    "half-day": [
        r"半天", r"大半天", r"上午", r"下午",
        r"half day", r"morning", r"afternoon"
    ],
    "full-day": [
        r"一天", r"一整天", r"慢慢玩", r"不着急",
        r"full day", r"all day", r"whole day"
    ]
}

ENERGY_PATTERNS = {
    "high": [
        r"体力好", r"能走", r"不累", r"多走点", r"high energy"
    ],
    "medium": [
        r"正常", r"还可以", r"一般", r"normal", r"medium"
    ],
    "low": [
        r"累了", r"走不动", r"少走路", r"休息", r"tired", r"low energy"
    ]
}


def extract_companion(text: str) -> str:
    """提取同行人员"""
    text_lower = text.lower()
    for companion, patterns in COMPANION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return companion
    return "any"  # 默认


def extract_interests(text: str) -> List[str]:
    """提取兴趣偏好"""
    interests = []
    text_lower = text.lower()
    for interest, patterns in INTEREST_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if interest not in interests:
                    interests.append(interest)
                break
    return interests if interests else ["quick-visit"]


def extract_time_budget(text: str) -> str:
    """提取时间预算"""
    for time_budget, patterns in TIME_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return time_budget
    return "2-3h"  # 默认


def extract_energy_level(text: str) -> str:
    """提取体力水平"""
    for energy, patterns in ENERGY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return energy
    return "medium"  # 默认


def extract_profile_from_conversation(conversation: str) -> Dict:
    """
    从对话历史中提取用户画像
    
    Args:
        conversation: 对话文本
    
    Returns:
        用户画像字典
    """
    # 提取各维度
    companion = extract_companion(conversation)
    interests = extract_interests(conversation)
    time_budget = extract_time_budget(conversation)
    energy_level = extract_energy_level(conversation)
    
    # 推断画像类型
    profile_type = infer_profile_type(companion, interests, time_budget)
    
    return {
        "companions": companion,
        "interests": interests,
        "time_budget": time_budget,
        "energy_level": energy_level,
        "profile_type": profile_type,
        "confidence": "high" if any([
            companion != "any",
            len(interests) > 0 and interests != ["quick-visit"],
            time_budget != "2-3h"
        ]) else "low"
    }


def infer_profile_type(companion: str, interests: List[str], time_budget: str) -> str:
    """根据提取的信息推断画像类型"""
    # 摄影优先
    if "photography" in interests and companion == "solo":
        return "solo-photographer"
    
    # 情侣浪漫
    if companion == "couple":
        return "couple-romantic"
    
    # 家庭亲子
    if companion == "family":
        return "family-kids"
    
    # 历史深度
    if "history" in interests or "culture" in interests:
        if time_budget in ["half-day", "full-day"]:
            return "history-buff"
    
    # 快速游览
    if time_budget == "1h" or "quick-visit" in interests:
        return "quick-visit"
    
    # 默认
    return "quick-visit"


def generate_questions_if_needed() -> List[str]:
    """生成画像采集问题（当无法从对话提取时）"""
    return [
        "1️⃣ 和谁一起？（一个人/情侣/带娃/朋友/带老人）",
        "2️⃣ 更想看什么？（历史/拍照/文化/建筑/随便逛逛）",
        "3️⃣ 时间大概多久？（1 小时/2-3 小时/半天/一天）"
    ]


def format_output(profile: Dict) -> str:
    """格式化输出画像"""
    output = []
    output.append("👤 用户画像分析")
    output.append("=" * 40)
    output.append(f"同行人员：{profile['companions']}")
    output.append(f"兴趣偏好：{', '.join(profile['interests'])}")
    output.append(f"时间预算：{profile['time_budget']}")
    output.append(f"体力水平：{profile['energy_level']}")
    output.append(f"推荐路线：{profile['profile_type']}")
    output.append(f"置信度：{profile['confidence']}")
    output.append("=" * 40)
    
    if profile['confidence'] == "low":
        output.append("")
        output.append("⚠️ 信息不足，建议询问：")
        for q in generate_questions_if_needed():
            output.append(f"  {q}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="从对话提取用户画像")
    parser.add_argument("--conversation", type=str, required=True, help="对话文本")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    profile = extract_profile_from_conversation(args.conversation)
    
    if args.json:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(format_output(profile))


if __name__ == "__main__":
    main()
