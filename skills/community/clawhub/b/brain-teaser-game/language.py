#!/usr/bin/env python3
"""
语言检测模块
根据用户输入文本自动检测语言（中文/英文/日语）
"""

import re
from typing import Literal

Language = Literal["zh", "en", "ja"]


def detect_language(text: str) -> Language:
    """
    检测文本语言

    规则：
    - 包含中文字符（排除日文汉字） → zh
    - 包含日文假名 → ja
    - 其他 → en

    Args:
        text: 用户输入的文本

    Returns:
        语言代码："zh", "en", "ja"
    """
    if not text:
        return "zh"  # 默认中文

    # 日文假名检测（平假名和片假名）
    # 平假名: U+3040-U+309F
    # 片假名: U+30A0-U+30FF
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
        return "ja"

    # 中文字符检测（CJK 统一汉字）
    # 注意：日文也使用汉字，所以要放在假名检测之后
    chinese_pattern = r'[\u4E00-\u9FFF]'
    if re.search(chinese_pattern, text):
        return "zh"

    # 默认英文
    return "en"


def get_language_name(lang: Language) -> str:
    """获取语言显示名称"""
    names = {
        "zh": "中文",
        "en": "English",
        "ja": "日本語"
    }
    return names.get(lang, "中文")


def get_response_language(text: str) -> Language:
    """
    根据用户输入确定回复语言
    与 detect_language 相同，但语义更清晰

    Args:
        text: 用户输入

    Returns:
        语言代码
    """
    return detect_language(text)


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("来个脑筋急转弯", "zh"),
        ("Give me a brain teaser", "en"),
        ("なぞなぞをください", "ja"),
        ("脳トレしたい", "ja"),
        ("我想玩个游戏", "zh"),
        ("Hello 你好", "zh"),  # 包含中文
        ("こんにちは世界", "ja"),  # 包含假名
        ("", "zh"),  # 空字符串默认中文
    ]

    for text, expected in test_cases:
        result = detect_language(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> {result} (expected: {expected})")
