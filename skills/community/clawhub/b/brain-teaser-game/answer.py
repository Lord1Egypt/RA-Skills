#!/usr/bin/env python3
"""
答案判断模块
支持多语言的模糊答案匹配
"""

import re
import unicodedata
from typing import Tuple


def normalize_text(text: str) -> str:
    """
    标准化文本：去除空格、标点，统一大小写

    Args:
        text: 原始文本

    Returns:
        标准化后的文本
    """
    if not text:
        return ""

    # 去除首尾空格
    text = text.strip()

    # 全角转半角
    text = fullwidth_to_halfwidth(text)

    # 转小写（对英文有效）
    text = text.lower()

    # 去除常见标点
    text = re.sub(r'[，。！？、；：""''（）【】《》\s,.!?;:\'"()\[\]<>]', '', text)

    return text


def fullwidth_to_halfwidth(text: str) -> str:
    """
    全角字符转半角字符

    Args:
        text: 包含全角字符的文本

    Returns:
        转换后的文本
    """
    result = []
    for char in text:
        code = ord(char)
        # 全角空格
        if code == 0x3000:
            result.append(' ')
        # 全角字符（! 到 ~）
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(char)
    return ''.join(result)


def extract_answer(text: str, language: str) -> str:
    """
    从用户输入中提取答案

    支持格式：
    - 中文："答案是水"、"是水"、"水"
    - 英文："the answer is water"、"water"
    - 日文："答えは水"、"水"

    Args:
        text: 用户输入
        language: 语言代码

    Returns:
        提取的答案
    """
    text = text.strip()

    if language == "zh":
        # 中文格式：答案是X、是X、答案X、我觉得是X
        patterns = [
            r'^答案[是为：:]\s*(.+)$',
            r'^[是为：:]\s*(.+)$',
            r'^答案\s*(.+)$',
            r'^我觉得[是为]\s*(.+)$',
            r'^我猜[是为]\s*(.+)$',
            r'^应该[是为]\s*(.+)$',
        ]
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                return match.group(1).strip()

    elif language == "en":
        # 英文格式：the answer is X、it's X、X
        patterns = [
            r'^the\s+answer\s+is\s+(.+)$',
            r'^answer[:\s]+(.+)$',
            r'^it\'?s?\s+(.+)$',
            r'^i\s+(?:think|guess|say)\s+(?:it\'?s?\s+)?(.+)$',
        ]
        for pattern in patterns:
            match = re.match(pattern, text.lower())
            if match:
                return match.group(1).strip()

    elif language == "ja":
        # 日文格式：答えはX、Xです
        patterns = [
            r'^答え[はが][:：]?\s*(.+?)(?:です|だ)?$',  # 答えはX
            r'^(.+?)です$',  # Xです
            r'^正解[はが][:：]?\s*(.+)$',  # 正解はX
        ]
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                return match.group(1).strip()

    # 直接返回原文
    return text


def check_answer(user_answer: str, correct_answer: str, language: str = "zh") -> Tuple[bool, str]:
    """
    检查用户答案是否正确

    Args:
        user_answer: 用户的答案
        correct_answer: 正确答案
        language: 语言代码

    Returns:
        (是否正确, 反馈消息)
    """
    if not user_answer:
        return False, "请提供答案"

    # 提取实际答案
    extracted = extract_answer(user_answer, language)

    # 标准化比较
    normalized_user = normalize_text(extracted)
    normalized_correct = normalize_text(correct_answer)

    # 完全匹配
    if normalized_user == normalized_correct:
        return True, "正确！"

    # 包含匹配（用户答案包含正确答案或反之）
    if normalized_correct in normalized_user or normalized_user in normalized_correct:
        # 但要避免太短的情况（比如用户输入"一"匹配到"一年"）
        if len(normalized_user) >= 2 or len(normalized_correct) <= 2:
            return True, "正确！"

    # 模糊匹配（允许一些常见变体）
    if fuzzy_match(normalized_user, normalized_correct, language):
        return True, "正确！"

    return False, "不对哦，再想想~"


def fuzzy_match(user: str, correct: str, language: str) -> bool:
    """
    模糊匹配，处理一些常见的变体

    Args:
        user: 用户答案
        correct: 正确答案
        language: 语言代码

    Returns:
        是否匹配
    """
    # 数字变体（一/1/壹）
    number_map = {
        'zh': {
            '零': ['0', '〇', '零'],
            '一': ['1', '一', '壹', '么'],
            '二': ['2', '二', '贰', '两'],
            '三': ['3', '三', '叁'],
            '四': ['4', '四', '肆'],
            '五': ['5', '五', '伍'],
            '六': ['6', '六', '陆'],
            '七': ['7', '七', '柒'],
            '八': ['8', '八', '捌'],
            '九': ['9', '九', '玖'],
            '十': ['10', '十', '拾'],
        },
        'en': {
            'zero': ['0', 'zero', 'none'],
            'one': ['1', 'one'],
            'two': ['2', 'two'],
            'three': ['3', 'three'],
            'four': ['4', 'four'],
            'five': ['5', 'five'],
            'six': ['6', 'six'],
            'seven': ['7', 'seven'],
            'eight': ['8', 'eight'],
            'nine': ['9', 'nine'],
            'ten': ['10', 'ten'],
        }
    }

    # 简单的数字匹配
    if language in number_map:
        for key, variants in number_map[language].items():
            if user in variants and correct in variants:
                return True
            if correct in variants and user in variants:
                return True

    # 编辑距离（允许1个字符差异，仅对短字符串）
    if len(user) <= 3 and len(correct) <= 3:
        if levenshtein_distance(user, correct) <= 1:
            return True

    return False


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串的编辑距离

    Args:
        s1: 字符串1
        s2: 字符串2

    Returns:
        编辑距离
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


if __name__ == "__main__":
    # 测试用例
    print("=== 答案提取测试 ===")
    test_extractions = [
        ("答案是水", "zh", "水"),
        ("是水", "zh", "水"),
        ("水", "zh", "水"),
        ("The answer is water", "en", "water"),
        ("water", "en", "water"),
        ("答えは水", "ja", "水"),
    ]
    for text, lang, expected in test_extractions:
        result = extract_answer(text, lang)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> '{result}' (expected: '{expected}')")

    print("\n=== 答案检查测试 ===")
    test_checks = [
        ("水", "水", "zh", True),
        ("答案是水", "水", "zh", True),
        ("１", "1", "zh", True),  # 全角数字
        ("water", "water", "en", True),
        ("The answer is piano", "piano", "en", True),
        ("錯", "错", "zh", True),  # 繁简体（简化处理）
    ]
    for user, correct, lang, expected in test_checks:
        result, msg = check_answer(user, correct, lang)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{user}' vs '{correct}' -> {result} ({msg})")
