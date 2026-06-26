#!/usr/bin/env python3
"""
语言检测模块
支持自动识别聊天消息的语言
"""

import re
from typing import List, Dict

# 常见语言特征（简化版，生产环境建议使用 langdetect 或 fasttext）
LANGUAGE_PATTERNS = {
    'zh-CN': {
        'name': '简体中文',
        'patterns': [
            r'[\u4e00-\u9fff]',  # 中文字符
        ],
        'exclude': [
            r'[\u3400-\u4dbf]',  # 扩展 A 区（多为繁体）
        ]
    },
    'zh-TW': {
        'name': '繁体中文',
        'patterns': [
            r'[\u4e00-\u9fff]',
            r'[麼麼裡裡後後為為]'  # 常见繁体字
        ]
    },
    'en': {
        'name': 'English',
        'patterns': [
            r'[a-zA-Z]{3,}',  # 英文单词
        ]
    },
    'ja': {
        'name': '日本語',
        'patterns': [
            r'[\u3040-\u309f]',  # 平假名
            r'[\u30a0-\u30ff]',  # 片假名
        ]
    },
    'ko': {
        'name': '한국어',
        'patterns': [
            r'[\uac00-\ud7af]',  # 韩文音节
            r'[\u1100-\u11ff]',  # 韩文字母
        ]
    }
}

def detect_language(text: str) -> str:
    """
    检测文本语言
    返回：ISO 639-1 语言代码
    """
    if not text or len(text.strip()) < 2:
        return 'unknown'
    
    scores = {}
    
    for lang, config in LANGUAGE_PATTERNS.items():
        score = 0
        for pattern in config['patterns']:
            matches = re.findall(pattern, text)
            score += len(matches)
        
        # 排除规则
        if 'exclude' in config:
            for pattern in config['exclude']:
                matches = re.findall(pattern, text)
                score -= len(matches) * 0.5
        
        if score > 0:
            scores[lang] = score
    
    if not scores:
        return 'unknown'
    
    # 返回得分最高的语言
    return max(scores, key=scores.get)

def detect_mixed_languages(messages: List[Dict]) -> Dict[str, float]:
    """
    检测一组消息的语言分布
    返回：{语言代码：占比}
    """
    lang_counts = {}
    total = 0
    
    for msg in messages:
        content = msg.get('content', '')
        if not content:
            continue
        
        lang = detect_language(content)
        if lang != 'unknown':
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
            total += 1
    
    if total == 0:
        return {'unknown': 1.0}
    
    # 转换为占比
    return {lang: count / total for lang, count in lang_counts.items()}

def get_primary_language(messages: List[Dict]) -> str:
    """
    获取主要语言（占比最高）
    """
    distribution = detect_mixed_languages(messages)
    return max(distribution, key=distribution.get)

if __name__ == "__main__":
    # 测试
    test_texts = [
        ("你好，今天天气不错", "zh-CN"),
        ("Hello, how are you?", "en"),
        ("こんにちは", "ja"),
        ("안녕하세요", "ko"),
        ("你好 Hello 混合", "zh-CN"),  # 中英混合，按字符数判定
    ]
    
    print("语言检测测试：")
    for text, expected in test_texts:
        result = detect_language(text)
        status = "✓" if result == expected else "✗"
        print(f"  {status} \"{text}\" -> {result} (预期：{expected})")
