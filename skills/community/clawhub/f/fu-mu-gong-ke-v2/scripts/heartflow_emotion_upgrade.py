#!/usr/bin/env python3
"""
心虫情绪分析引擎 (HeartFlow Emotion Analysis Engine) v1.0.0

升级版情绪引擎 — 整合心虫三大核心模型：
1) PAD三维情绪检测 (Pleasure/Arousal/Dominance 0-1)
2) MetaEmotionMonitor 六层次分析 (事件/唤醒/感受/解释/倾向/行为)
3) SDT 动机类型识别 (无动机/外部/内摄/认同/整合/内在)
4) 情绪理性三维度评估 (认知理性/战略理性/整体理性)

理论来源:
- Mehrabian & Russell (1974) PAD 三维情绪空间理论
- Scarantino (2016) SEP 情绪构成六成分模型
- Deci & Ryan (2000) 自我决定理论 (SDT)
- Stanford Encyclopedia of Philosophy: 情绪、理性、动机理论
- HeartFlow 自主感情模块 v3.7.0 / MetaEmotionMonitor v4.1.0

设计目标: 替代 fu-mu-gong-ke 原有 EmotionAssessor 的简单修饰词感知，
提供多维度、可量化、可追踪的情绪分析管线。

作者: HeartFlow 团队 / fu-mu-gong-ke 集成
"""

import json
import re
import math
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum


# =============================================================================
# 第一部分: PAD 三维情绪模型
# 基于 Mehrabian & Russell (1974)
# =============================================================================

class PADEmotion:
    """PAD 情绪坐标点"""
    __slots__ = ('p', 'a', 'd', 'label', 'cn_label')

    def __init__(self, p: float, a: float, d: float, label: str = '', cn_label: str = ''):
        self.p = max(-1.0, min(1.0, p))   # Pleasure: -1(痛苦) ~ +1(愉悦)
        self.a = max(-1.0, min(1.0, a))   # Arousal: -1(平静) ~ +1(兴奋)
        self.d = max(-1.0, min(1.0, d))   # Dominance: -1(无助) ~ +1(掌控)
        self.label = label
        self.cn_label = cn_label

    def to_dict(self) -> Dict[str, float]:
        return {'p': self.p, 'a': self.a, 'd': self.d}

    def distance_to(self, other: 'PADEmotion') -> float:
        return math.sqrt(
            (self.p - other.p) ** 2 +
            (self.a - other.a) ** 2 +
            (self.d - other.d) ** 2
        )

    def normalize_to_01(self) -> Dict[str, float]:
        """将 [-1, 1] 映射到 [0, 1]"""
        return {
            'pleasure': round((self.p + 1) / 2, 4),
            'arousal': round((self.a + 1) / 2, 4),
            'dominance': round((self.d + 1) / 2, 4),
        }


# 标准情绪 PAD 坐标（来自心虫 pad-model.js 的 PAD_MODEL 常量表）
PAD_EMOTION_MAP: Dict[str, PADEmotion] = {
    # 积极高唤醒
    'ecstasy':    PADEmotion(0.9,  0.8,  0.7,  'ecstasy', '狂喜'),
    'excitement': PADEmotion(0.8,  0.7,  0.6,  'excitement', '兴奋'),
    'surprise':   PADEmotion(0.4,  0.7,  0.2,  'surprise', '惊讶'),
    'anger':      PADEmotion(-0.7, 0.7,  0.5,  'anger', '愤怒'),
    'fear':       PADEmotion(-0.6, 0.8, -0.5,  'fear', '恐惧'),
    'distress':   PADEmotion(-0.5, 0.6, -0.3,  'distress', '痛苦'),

    # 积极低唤醒
    'serenity':   PADEmotion(0.7, -0.4,  0.3,  'serenity', '宁静'),
    'contentment':PADEmotion(0.6, -0.3,  0.4,  'contentment', '满足'),
    'boredom':    PADEmotion(-0.3,-0.6, -0.2,  'boredom', '无聊'),
    'sadness':    PADEmotion(-0.5,-0.4, -0.4,  'sadness', '悲伤'),
    'depression': PADEmotion(-0.7,-0.7, -0.6,  'depression', '抑郁'),

    # 支配维度突出
    'pride':      PADEmotion(0.6,  0.3,  0.8,  'pride', '自豪'),
    'contempt':   PADEmotion(-0.3, 0.2,  0.7,  'contempt', '轻蔑'),
    'shame':      PADEmotion(-0.4, 0.2, -0.7,  'shame', '羞愧'),
    'humiliation':PADEmotion(-0.6, 0.3, -0.8,  'humiliation', '屈辱'),

    # 中性
    'neutral':    PADEmotion(0.0,  0.0,  0.0,  'neutral', '中性'),
}

# 扩展情绪关键词 → PAD 坐标映射（支持中文和英文）
EXTENDED_EMOTION_KEYWORDS: Dict[str, PADEmotion] = {
    # === 英文关键词 ===
    'ecstatic': PADEmotion(0.9, 0.8, 0.7, 'ecstatic', '狂喜'),
    'thrilled': PADEmotion(0.9, 0.8, 0.7, 'thrilled', '狂喜'),
    'elated': PADEmotion(0.85, 0.75, 0.65, 'elated', '兴高采烈'),
    'joyful': PADEmotion(0.8, 0.6, 0.5, 'joyful', '喜悦'),
    'happy': PADEmotion(0.7, 0.5, 0.4, 'happy', '快乐'),
    'delighted': PADEmotion(0.75, 0.65, 0.5, 'delighted', '愉快'),
    'enthusiastic': PADEmotion(0.75, 0.6, 0.5, 'enthusiastic', '热情'),
    'energetic': PADEmotion(0.6, 0.7, 0.5, 'energetic', '精力充沛'),
    'content': PADEmotion(0.6, -0.3, 0.4, 'content', '满足'),
    'calm': PADEmotion(0.5, -0.5, 0.3, 'calm', '平静'),
    'relaxed': PADEmotion(0.5, -0.4, 0.3, 'relaxed', '放松'),
    'peaceful': PADEmotion(0.6, -0.5, 0.2, 'peaceful', '平和'),
    'grateful': PADEmotion(0.7, -0.2, 0.3, 'grateful', '感恩'),
    'hopeful': PADEmotion(0.6, 0.3, 0.2, 'hopeful', '希望'),
    'furious': PADEmotion(-0.8, 0.8, 0.6, 'furious', '暴怒'),
    'irritated': PADEmotion(-0.5, 0.5, 0.3, 'irritated', '烦躁'),
    'annoyed': PADEmotion(-0.4, 0.5, 0.2, 'annoyed', '恼火'),
    'frustrated': PADEmotion(-0.5, 0.5, -0.2, 'frustrated', '沮丧'),
    'anxious': PADEmotion(-0.4, 0.6, -0.4, 'anxious', '焦虑'),
    'worried': PADEmotion(-0.4, 0.5, -0.3, 'worried', '担忧'),
    'nervous': PADEmotion(-0.3, 0.7, -0.4, 'nervous', '紧张'),
    'terrified': PADEmotion(-0.7, 0.9, -0.6, 'terrified', '惊恐'),
    'panicked': PADEmotion(-0.6, 0.8, -0.5, 'panicked', '恐慌'),
    'shocked': PADEmotion(-0.3, 0.8, 0.1, 'shocked', '震惊'),
    'disgusted': PADEmotion(-0.6, 0.4, 0.3, 'disgusted', '厌恶'),
    'jealous': PADEmotion(-0.4, 0.5, -0.1, 'jealous', '嫉妒'),
    'miserable': PADEmotion(-0.7, -0.4, -0.5, 'miserable', '悲惨'),
    'hopeless': PADEmotion(-0.6, -0.6, -0.6, 'hopeless', '绝望'),
    'lonely': PADEmotion(-0.5, -0.4, -0.5, 'lonely', '孤独'),
    'tired': PADEmotion(-0.2, -0.5, -0.2, 'tired', '疲倦'),
    'exhausted': PADEmotion(-0.3, -0.7, -0.4, 'exhausted', '筋疲力尽'),
    'numb': PADEmotion(-0.3, -0.5, -0.4, 'numb', '麻木'),
    'guilty': PADEmotion(-0.4, 0.1, -0.6, 'guilty', '内疚'),
    'regretful': PADEmotion(-0.4, 0.0, -0.5, 'regretful', '后悔'),
    'proud': PADEmotion(0.6, 0.3, 0.8, 'proud', '自豪'),
    'confident': PADEmotion(0.5, 0.3, 0.7, 'confident', '自信'),
    'powerful': PADEmotion(0.4, 0.5, 0.8, 'powerful', '强大'),
    'helpless': PADEmotion(-0.4, -0.3, -0.7, 'helpless', '无助'),
    'vulnerable': PADEmotion(-0.3, 0.1, -0.6, 'vulnerable', '脆弱'),
    'powerless': PADEmotion(-0.3, -0.2, -0.7, 'powerless', '无力'),

    # === 中文关键词 ===
    '狂喜': PADEmotion(0.9, 0.8, 0.7, 'ecstasy', '狂喜'),
    '兴奋': PADEmotion(0.8, 0.7, 0.6, 'excitement', '兴奋'),
    '兴高采烈': PADEmotion(0.85, 0.75, 0.65, 'elated', '兴高采烈'),
    '喜悦': PADEmotion(0.8, 0.6, 0.5, 'joyful', '喜悦'),
    '快乐': PADEmotion(0.7, 0.5, 0.4, 'happy', '快乐'),
    '愉快': PADEmotion(0.75, 0.65, 0.5, 'delighted', '愉快'),
    '开心': PADEmotion(0.7, 0.5, 0.4, 'happy', '开心'),
    '高兴': PADEmotion(0.7, 0.5, 0.4, 'happy', '高兴'),
    '热情': PADEmotion(0.75, 0.6, 0.5, 'enthusiastic', '热情'),
    '满足': PADEmotion(0.6, -0.3, 0.4, 'contentment', '满足'),
    '宁静': PADEmotion(0.7, -0.4, 0.3, 'serenity', '宁静'),
    '平静': PADEmotion(0.5, -0.5, 0.3, 'calm', '平静'),
    '放松': PADEmotion(0.5, -0.4, 0.3, 'relaxed', '放松'),
    '平和': PADEmotion(0.6, -0.5, 0.2, 'peaceful', '平和'),
    '感恩': PADEmotion(0.7, -0.2, 0.3, 'grateful', '感恩'),
    '希望': PADEmotion(0.6, 0.3, 0.2, 'hopeful', '希望'),
    '愤怒': PADEmotion(-0.7, 0.7, 0.5, 'anger', '愤怒'),
    '生气': PADEmotion(-0.6, 0.6, 0.4, 'anger', '生气'),
    '暴怒': PADEmotion(-0.8, 0.8, 0.6, 'furious', '暴怒'),
    '烦躁': PADEmotion(-0.5, 0.5, 0.3, 'irritated', '烦躁'),
    '恼火': PADEmotion(-0.4, 0.5, 0.2, 'annoyed', '恼火'),
    '沮丧': PADEmotion(-0.5, 0.5, -0.2, 'frustrated', '沮丧'),
    '焦虑': PADEmotion(-0.4, 0.6, -0.4, 'anxious', '焦虑'),
    '担心': PADEmotion(-0.4, 0.5, -0.3, 'worried', '担心'),
    '担忧': PADEmotion(-0.4, 0.5, -0.3, 'worried', '担忧'),
    '紧张': PADEmotion(-0.3, 0.7, -0.4, 'nervous', '紧张'),
    '恐惧': PADEmotion(-0.6, 0.8, -0.5, 'fear', '恐惧'),
    '害怕': PADEmotion(-0.5, 0.7, -0.4, 'fear', '害怕'),
    '惊恐': PADEmotion(-0.7, 0.9, -0.6, 'terrified', '惊恐'),
    '恐慌': PADEmotion(-0.6, 0.8, -0.5, 'panicked', '恐慌'),
    '震惊': PADEmotion(-0.3, 0.8, 0.1, 'shocked', '震惊'),
    '厌恶': PADEmotion(-0.6, 0.4, 0.3, 'disgusted', '厌恶'),
    '惊讶': PADEmotion(0.4, 0.7, 0.2, 'surprise', '惊讶'),
    '嫉妒': PADEmotion(-0.4, 0.5, -0.1, 'jealous', '嫉妒'),
    '悲伤': PADEmotion(-0.5, -0.4, -0.4, 'sadness', '悲伤'),
    '难过': PADEmotion(-0.5, -0.3, -0.3, 'sadness', '难过'),
    '伤心': PADEmotion(-0.5, -0.3, -0.3, 'sadness', '伤心'),
    '悲惨': PADEmotion(-0.7, -0.4, -0.5, 'miserable', '悲惨'),
    '抑郁': PADEmotion(-0.7, -0.7, -0.6, 'depression', '抑郁'),
    '绝望': PADEmotion(-0.6, -0.6, -0.6, 'hopeless', '绝望'),
    '孤独': PADEmotion(-0.5, -0.4, -0.5, 'lonely', '孤独'),
    '无聊': PADEmotion(-0.3, -0.6, -0.2, 'boredom', '无聊'),
    '疲倦': PADEmotion(-0.2, -0.5, -0.2, 'tired', '疲倦'),
    '疲惫': PADEmotion(-0.3, -0.6, -0.3, 'tired', '疲惫'),
    '崩溃': PADEmotion(-0.5, 0.4, -0.6, 'distress', '崩溃'),
    '麻木': PADEmotion(-0.3, -0.5, -0.4, 'numb', '麻木'),
    '内疚': PADEmotion(-0.4, 0.1, -0.6, 'guilty', '内疚'),
    '愧疚': PADEmotion(-0.4, 0.1, -0.6, 'guilty', '愧疚'),
    '后悔': PADEmotion(-0.4, 0.0, -0.5, 'regretful', '后悔'),
    '自责': PADEmotion(-0.4, 0.1, -0.6, 'guilty', '自责'),
    '自豪': PADEmotion(0.6, 0.3, 0.8, 'pride', '自豪'),
    '自信': PADEmotion(0.5, 0.3, 0.7, 'confident', '自信'),
    '羞愧': PADEmotion(-0.4, 0.2, -0.7, 'shame', '羞愧'),
    '屈辱': PADEmotion(-0.6, 0.3, -0.8, 'humiliation', '屈辱'),
    '无助': PADEmotion(-0.4, -0.3, -0.7, 'helpless', '无助'),
    '无力': PADEmotion(-0.3, -0.2, -0.7, 'powerless', '无力'),
    '脆弱': PADEmotion(-0.3, 0.1, -0.6, 'vulnerable', '脆弱'),
    '痛苦': PADEmotion(-0.5, 0.6, -0.3, 'distress', '痛苦'),
    '压抑': PADEmotion(-0.5, -0.4, -0.5, 'sadness', '压抑'),
    '委屈': PADEmotion(-0.4, 0.3, -0.5, 'distress', '委屈'),
    '温暖': PADEmotion(0.6, -0.2, 0.3, 'contentment', '温暖'),
    '感动': PADEmotion(0.7, 0.2, 0.3, 'grateful', '感动'),
    '爱': PADEmotion(0.8, 0.3, 0.3, 'love', '爱'),
    '喜欢': PADEmotion(0.7, 0.4, 0.3, 'joy', '喜欢'),
    '欣慰': PADEmotion(0.6, -0.2, 0.4, 'contentment', '欣慰'),
    '心疼': PADEmotion(-0.3, 0.3, -0.4, 'concern', '心疼'),
    '心碎': PADEmotion(-0.6, 0.2, -0.6, 'sadness', '心碎'),
    '气死': PADEmotion(-0.8, 0.8, 0.5, 'furious', '气死'),
    '火大': PADEmotion(-0.7, 0.7, 0.5, 'anger', '火大'),
    '发火': PADEmotion(-0.7, 0.7, 0.5, 'anger', '发火'),
    '吼了': PADEmotion(-0.7, 0.7, 0.5, 'anger', '吼了'),
    '打了': PADEmotion(-0.7, 0.7, 0.5, 'anger', '打了'),
    '骂了': PADEmotion(-0.7, 0.7, 0.5, 'anger', '骂了'),
    '沉重': PADEmotion(-0.5, -0.3, -0.4, 'sadness', '沉重'),
}


class PADDetector:
    """
    PAD 三维情绪检测器
    将自然语言文本映射到 Pleasure/Arousal/Dominance 三维空间
    输出 [0, 1] 归一化坐标 + 最接近的标准情绪标签
    """

    def __init__(self):
        # 强度修饰词
        self._up_modifiers = ['非常', '特别', '极其', '太', '超级', '无比',
                              '暴', '死', '炸', '疯', '很', '好', '十分',
                              '极度', '格外', '异常', '万分', '相当']
        self._down_modifiers = ['有点', '稍微', '略微', '一点点', '一些',
                                '有些', '不太', '不怎么', '还行', '稍许']
        self._negation_modifiers = ['不', '没', '没有', '别', '不要', '不是']

    def detect(self, text: str) -> Dict[str, Any]:
        """
        从文本检测 PAD 情绪状态

        Args:
            text: 输入文本（中文或英文）

        Returns:
            dict: {
                'pad_01': { 'pleasure': 0-1, 'arousal': 0-1, 'dominance': 0-1 },
                'pad_raw': { 'p': -1~1, 'a': -1~1, 'd': -1~1 },
                'dominant_emotion': str,      # 最接近的标准情绪标签
                'dominant_emotion_cn': str,   # 中文标签
                'confidence': float,          # 置信度 0-1
                'matched_keywords': [str],    # 匹配到的关键词
                'valence': str,               # positive/negative/neutral
                'arousal_level': str,         # high/low/moderate
                'dominance_level': str,       # high/low/moderate
            }
        """
        if not text or not text.strip():
            return self._empty_result()

        lower_text = text.lower()
        matched_emotions = []
        matched_keywords = []

        # 1. 关键词匹配（优先精确匹配）
        for keyword, pad in EXTENDED_EMOTION_KEYWORDS.items():
            if keyword in text or keyword.lower() in lower_text:
                # 检查否定词
                negated = False
                for neg in self._negation_modifiers:
                    if neg + keyword in text or neg + keyword in lower_text:
                        negated = True
                        break

                # 检测强度修饰
                intensity_mod = 1.0
                for up in self._up_modifiers:
                    if up + keyword in text or keyword + up in text:
                        intensity_mod = 1.3
                        break
                for down in self._down_modifiers:
                    if down + keyword in text:
                        intensity_mod = 0.5
                        break

                if negated:
                    # 否定词反转情绪
                    inverted = PADEmotion(
                        -pad.p * 0.5,
                        pad.a * 0.5,
                        -pad.d * 0.3,
                        pad.label,
                        pad.cn_label
                    )
                    matched_emotions.append((inverted, 0.6 * intensity_mod))
                else:
                    matched_emotions.append((pad, intensity_mod))
                matched_keywords.append(keyword)

        # 2. 如果没有匹配，检查情绪词组的连续匹配
        if not matched_emotions:
            cn_phrases = self._detect_phrase_emotions(text)
            for phrase_pad, confidence in cn_phrases:
                matched_emotions.append((phrase_pad, confidence))

        # 3. 计算加权平均 PAD
        if not matched_emotions:
            return self._empty_result()

        total_p = total_a = total_d = 0.0
        total_weight = 0.0

        for pad_em, weight in matched_emotions:
            total_p += pad_em.p * weight
            total_a += pad_em.a * weight
            total_d += pad_em.d * weight
            total_weight += weight

        if total_weight == 0:
            return self._empty_result()

        avg_p = total_p / total_weight
        avg_a = total_a / total_weight
        avg_d = total_d / total_weight

        # 4. 找到最接近的标准情绪
        closest_name = 'neutral'
        min_dist = float('inf')
        for name, std_pad in PAD_EMOTION_MAP.items():
            dist = math.sqrt(
                (avg_p - std_pad.p) ** 2 +
                (avg_a - std_pad.a) ** 2 +
                (avg_d - std_pad.d) ** 2
            )
            if dist < min_dist:
                min_dist = dist
                closest_name = name

        confidence = max(0.0, min(1.0, 1.0 - min_dist / 2.0))
        closest = PAD_EMOTION_MAP[closest_name]

        # 5. 效价、唤醒度、支配度判断
        valence = 'positive' if avg_p > 0.2 else ('negative' if avg_p < -0.2 else 'neutral')
        arousal_lvl = 'high' if avg_a > 0.3 else ('low' if avg_a < -0.3 else 'moderate')
        dom_lvl = 'high' if avg_d > 0.3 else ('low' if avg_d < -0.3 else 'moderate')

        return {
            'pad_01': {
                'pleasure': round((avg_p + 1) / 2, 4),
                'arousal': round((avg_a + 1) / 2, 4),
                'dominance': round((avg_d + 1) / 2, 4),
            },
            'pad_raw': {
                'p': round(avg_p, 4),
                'a': round(avg_a, 4),
                'd': round(avg_d, 4),
            },
            'dominant_emotion': closest_name,
            'dominant_emotion_cn': closest.cn_label,
            'confidence': round(confidence, 4),
            'matched_keywords': matched_keywords[:10],
            'valence': valence,
            'arousal_level': arousal_lvl,
            'dominance_level': dom_lvl,
        }

    def _detect_phrase_emotions(self, text: str) -> List[Tuple[PADEmotion, float]]:
        """检测复合情绪词组"""
        results = []

        # 常见情绪词组的组合检测
        phrase_patterns = [
            # (模式, PAD坐标, 置信度)
            (r'(又[生气愤怒焦虑难过]又[生气愤怒焦虑难过])',
             PADEmotion(-0.6, 0.5, -0.3, 'distress', '情绪冲突'), 0.7),
            (r'([生气愤怒焦虑紧张害怕难过悲伤]+(?:到|得)(?:不行|要死|疯了|崩溃|窒息))',
             PADEmotion(-0.7, 0.7, -0.5, 'distress', '情绪崩溃'), 0.8),
            (r'(既[开心高兴兴奋]又[担心害怕焦虑])',
             PADEmotion(0.2, 0.5, -0.1, 'mixed', '矛盾'), 0.6),
            (r'(说不出(?:的|来)(?:难受|压抑|沉重|痛苦))',
             PADEmotion(-0.5, 0.2, -0.5, 'distress', '隐痛'), 0.7),
            (r'(不知道怎么办|不知道该怎么|没办法了|没辙了|束手无策)',
             PADEmotion(-0.4, 0.1, -0.7, 'helpless', '无助'), 0.8),
            (r'(撑不住了|坚持不住了|受不了了|扛不住了)',
             PADEmotion(-0.5, 0.3, -0.6, 'distress', '撑不住'), 0.8),
            (r'(松了一口气|终于可以|放心了|安心了)',
             PADEmotion(0.5, -0.3, 0.4, 'relief', '释然'), 0.7),
        ]

        for pattern, pad_em, conf in phrase_patterns:
            if re.search(pattern, text):
                results.append((pad_em, conf))

        return results

    def _empty_result(self) -> Dict[str, Any]:
        return {
            'pad_01': {'pleasure': 0.5, 'arousal': 0.5, 'dominance': 0.5},
            'pad_raw': {'p': 0.0, 'a': 0.0, 'd': 0.0},
            'dominant_emotion': 'neutral',
            'dominant_emotion_cn': '中性',
            'confidence': 0.0,
            'matched_keywords': [],
            'valence': 'neutral',
            'arousal_level': 'moderate',
            'dominance_level': 'moderate',
        }


# =============================================================================
# 第二部分: MetaEmotionMonitor 六层次分析
# 基于心虫 MetaEmotionMonitor v4.1.0 + Scarantino (2016) 六成分模型
# 层次: 事件 → 唤醒 → 感受 → 解释 → 倾向 → 行为
# =============================================================================

class MetaEmotionLevel(Enum):
    """元情绪层次"""
    NONE = 0        # 无元情绪意识
    AWARE = 1       # 意识到情绪
    REFLECTIVE = 2  # 反思情绪
    EVALUATIVE = 3  # 评估情绪
    REGULATIVE = 4  # 调节情绪
    INTEGRATIVE = 5 # 整合情绪


class EmotionComponent(Enum):
    """情绪六成分（基于 Scarantino 2016）"""
    EVENT = 'event'              # 触发事件
    AROUSAL = 'arousal'          # 生理唤醒
    FEELING = 'feeling'          # 主观感受
    APPRAISAL = 'appraisal'      # 认知解释/评价
    TENDENCY = 'tendency'        # 行动倾向
    BEHAVIOR = 'behavior'        # 实际行为


# 六成分检测模式
COMPONENT_PATTERNS = {
    EmotionComponent.EVENT: {
        'name': '触发事件',
        'indicators': [
            r'(?:因为|由于|当|每次|一[到看听]|今天|昨天|刚才|刚刚)',
            r'(?:孩子|儿子|女儿|老公|老婆|父母|老师|同学).*(?:不|没|又|总)',
            r'(?:考试|成绩|作业|上学|手机|游戏|电视)',
        ]
    },
    EmotionComponent.AROUSAL: {
        'name': '生理唤醒',
        'indicators': [
            r'(?:心跳|呼吸|手心出汗|脸红|手抖|发抖|颤抖|胃|胸闷|喘不过气)',
            r'(?:心跳加速|血压升高|手脚冰凉|浑身发热|肌肉紧张)',
            r'(?:哭|流泪|哽咽|声音发抖|说不出话)',
        ]
    },
    EmotionComponent.FEELING: {
        'name': '主观感受',
        'indicators': [
            r'(?:感觉|觉得|感到|感受到|体验|仿佛|像是|好像)',
            r'(?:难受|不舒服|好痛|痛苦|煎熬|折磨)',
            r'(?:空落落|堵得慌|压得喘不过气|心里不是滋味)',
        ]
    },
    EmotionComponent.APPRAISAL: {
        'name': '认知解释',
        'indicators': [
            r'(?:认为|觉得|以为|理解|明白|意识到|注意到|发现)',
            r'(?:是因为|原因|根源|都怪|都因为|要不是)',
            r'(?:我想|我觉得|在我看来|我认为|我的理解)',
            r'(?:不公平|凭什么|为什么|怎么这样|不应该)',
        ]
    },
    EmotionComponent.TENDENCY: {
        'name': '行动倾向',
        'indicators': [
            r'(?:想|想要|渴望|希望|恨不得|巴不得|真想)',
            r'(?:冲动|忍不住|控制不住|差点|就差|快要)',
            r'(?:想逃避|想躲|想离开|想放弃|想骂人|想打人|想哭)',
            r'(?:不想|不愿|懒得|懒得管|不想面对)',
        ]
    },
    EmotionComponent.BEHAVIOR: {
        'name': '实际行为',
        'indicators': [
            r'(?:做了|做了些什么|已经|然后|结果|最后|于是)',
            r'(?:吼了|骂了|打了|摔了|扔了|推了|走了|关门|离开)',
            r'(?:哭了|沉默了|不说话了|躲起来|逃避|回避)',
            r'(?:道歉|解释|沟通|谈话|坐下来|抱了|安慰)',
        ]
    }
}


class MetaEmotionMonitor:
    """
    元情绪监控器 — 六层次分析

    将用户输入的文本映射到六成分模型:
    事件(Event) → 唤醒(Arousal) → 感受(Feeling) → 解释(Appraisal) → 倾向(Tendency) → 行为(Behavior)

    同时检测元情绪层次（无意识→觉察→反思→评估→调节→整合）
    """

    def __init__(self):
        self.history: List[Dict] = []

    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        对文本进行六层次分析

        Args:
            text: 用户输入文本
            context: 可选的上下文信息（如之前轮次的分析结果）

        Returns:
            dict: {
                'components': { 六成分检测结果 },
                'meta_level': { 元情绪层次 },
                'component_profile': { 成分概览 },
                'primary_component': str,     # 主导成分
                'component_balance': str,      # 平衡/不平衡
                'gaps': [str],                 # 缺失成分
                'meta_emotion_detected': bool, # 是否检测到元情绪
                'meta_emotion_desc': str,      # 元情绪描述
                'insight': str,                # 综合分析洞见
            }
        """
        if not text or not text.strip():
            return self._empty_analysis()

        # 1. 六成分检测
        components = self._detect_components(text)

        # 2. 元情绪层次检测
        meta_level = self._detect_meta_level(text, components)

        # 3. 元情绪检测（对情绪的情绪）
        meta_emotion = self._detect_meta_emotion(text, components)

        # 4. 成分概览
        profile = self._build_component_profile(components)
        primary = max(profile['scores'], key=profile['scores'].get) if profile['scores'] else 'none'
        gaps = [c.value for c, v in profile['scores'].items() if v < 0.3]

        # 5. 成分平衡性
        scores = list(profile['scores'].values())
        if len(scores) >= 3:
            avg = sum(scores) / len(scores)
            variance = sum((s - avg) ** 2 for s in scores) / len(scores)
            balance = '平衡' if variance < 0.02 else ('较平衡' if variance < 0.06 else '不平衡')
        else:
            balance = '数据不足'

        # 6. 生成洞见
        insight = self._generate_insight(components, profile, meta_level, meta_emotion)

        result = {
            'components': components,
            'meta_level': {
                'level': meta_level['level'],
                'level_name': meta_level['name'],
                'level_description': meta_level['description'],
                'confidence': meta_level['confidence'],
            },
            'component_profile': profile,
            'primary_component': primary,
            'component_balance': balance,
            'gaps': gaps,
            'meta_emotion_detected': meta_emotion['detected'],
            'meta_emotion_desc': meta_emotion['description'],
            'insight': insight,
        }

        # 记录历史
        self.history.append(result)
        if len(self.history) > 100:
            self.history = self.history[-100:]

        return result

    def _detect_components(self, text: str) -> Dict[str, Any]:
        """检测六成分"""
        components = {}
        for component, config in COMPONENT_PATTERNS.items():
            matches = []
            for pattern in config['indicators']:
                found = re.findall(pattern, text)
                matches.extend(found)
            score = min(1.0, len(matches) * 0.25)
            components[component.value] = {
                'name': config['name'],
                'score': round(score, 4),
                'matches': matches[:5],
                'detected': score > 0.2,
            }
        return components

    def _detect_meta_level(self, text: str, components: Dict) -> Dict:
        """检测元情绪层次"""
        # 计算各成分的丰富度
        comp_count = sum(1 for c in components.values() if c['detected'])
        total_matches = sum(len(c['matches']) for c in components.values())

        if total_matches == 0:
            level = MetaEmotionLevel.NONE
            conf = 0.0
        elif comp_count <= 2:
            level = MetaEmotionLevel.AWARE
            conf = 0.5
        elif comp_count <= 3:
            level = MetaEmotionLevel.REFLECTIVE
            conf = 0.6
        elif comp_count <= 4:
            level = MetaEmotionLevel.EVALUATIVE
            conf = 0.7
        elif comp_count <= 5:
            level = MetaEmotionLevel.REGULATIVE
            conf = 0.8
        else:
            level = MetaEmotionLevel.INTEGRATIVE
            conf = 0.9

        level_names = {
            0: '无意识', 1: '觉察', 2: '反思',
            3: '评估', 4: '调节', 5: '整合'
        }
        level_descriptions = {
            0: '未意识到自身情绪状态',
            1: '意识到自己正在经历某种情绪',
            2: '能反思情绪的来源和影响',
            3: '能评估情绪的适当性和价值',
            4: '能主动调节情绪反应',
            5: '能将情绪体验整合到自我认知中',
        }

        # 额外检测元情绪层次的高级信号
        advanced_signals = {
            MetaEmotionLevel.REFLECTIVE: [r'(?:反思|回想|回看|思考.*为什么)'],
            MetaEmotionLevel.EVALUATIVE: [r'(?:适当|应该|不应该|对错|好坏|值得|不值得)'],
            MetaEmotionLevel.REGULATIVE: [r'(?:调节|控制|管理|深呼吸|冷静|暂停|停下来)'],
            MetaEmotionLevel.INTEGRATIVE: [r'(?:成长|学习|改变|模式|觉察到|意识到.*模式|理解.*自己)'],
        }

        for lvl, patterns in advanced_signals.items():
            if any(re.search(p, text) for p in patterns):
                if lvl.value > level.value:
                    level = lvl
                    conf = min(1.0, conf + 0.2)

        return {
            'level': level.value,
            'name': level_names[level.value],
            'description': level_descriptions[level.value],
            'confidence': round(conf, 4),
        }

    def _detect_meta_emotion(self, text: str, components: Dict) -> Dict:
        """检测元情绪（对情绪的情绪）"""
        meta_patterns = [
            # 对愤怒感到内疚
            (r'(?:为.*(?:生气|愤怒|发火).*(?:内疚|愧疚|后悔|自责)|'
             r'(?:内疚|愧疚|后悔|自责).*(?:生气|愤怒|发火))',
             '对愤怒感到内疚'),
            # 对恐惧感到羞耻
            (r'(?:为.*(?:害怕|恐惧|担心).*(?:羞耻|丢人|没出息|软弱)|'
             r'(?:羞耻|丢人|没出息|软弱).*(?:害怕|恐惧|担心))',
             '对恐惧感到羞耻'),
            # 对悲伤感到羞愧
            (r'(?:为.*(?:难过|悲伤|哭).*(?:羞耻|丢人|不应该|不该哭)|'
             r'(?:不该哭|不应该难过).*)',
             '对悲伤感到羞愧'),
            # 对焦虑感到焦虑
            (r'(?:为.*(?:焦虑|担心).*(?:更焦虑|更担心|焦虑.*焦虑))',
             '对焦虑感到焦虑'),
            # 为发火后悔（最常见的元情绪）
            (r'(?:发火.*(?:后悔|不该|内疚)|后悔.*(?:发火|吼|骂))',
             '对愤怒感到后悔'),
            # 对无感感到不安
            (r'(?:麻木|没感觉|没有感觉).*(?:可怕|担心|害怕|不安)',
             '对情感麻木感到不安'),
        ]

        for pattern, description in meta_patterns:
            if re.search(pattern, text):
                return {
                    'detected': True,
                    'description': description,
                    'type': 'secondary_emotion',
                }

        # 检查是否有矛盾情绪（混合情绪）
        mixed = self._detect_mixed_emotions(text)
        if mixed:
            return {
                'detected': True,
                'description': f'混合情绪: {mixed}',
                'type': 'mixed_emotion',
            }

        return {'detected': False, 'description': '', 'type': 'none'}

    def _detect_mixed_emotions(self, text: str) -> Optional[str]:
        """检测混合/矛盾情绪"""
        patterns = [
            (r'(?:又爱又恨|既爱又恨)', '爱恨交织'),
            (r'(?:又开心又难过|既开心又难过)', '悲喜交加'),
            (r'(?:又高兴又担心|既高兴又担心)', '喜悦与担忧并存'),
            (r'(?:又生气又心疼|既生气又心疼)', '愤怒与心疼交织'),
            (r'(?:又放松又焦虑|既放松又焦虑)', '放松与焦虑并存'),
            (r'(?:矛盾|纠结|不知道怎么办好|左右为难)', '矛盾纠结'),
        ]
        for pattern, desc in patterns:
            if re.search(pattern, text):
                return desc
        return None

    def _build_component_profile(self, components: Dict) -> Dict:
        """构建成分概览"""
        scores = {}
        for comp_key, comp_data in components.items():
            scores[comp_key] = comp_data['score']
        return {
            'scores': scores,
            'total_detected': sum(1 for c in components.values() if c['detected']),
            'total_matches': sum(len(c['matches']) for c in components.values()),
        }

    def _generate_insight(self, components: Dict, profile: Dict,
                          meta_level: Dict, meta_emotion: Dict) -> str:
        """生成综合分析洞见"""
        parts = []

        # 成分覆盖度
        detected = profile['total_detected']
        if detected <= 1:
            parts.append('情绪表达较简略，仅提及了基本情绪。')
        elif detected <= 3:
            parts.append(f'涵盖了{detected}个情绪成分，有基本的情绪描述能力。')
        else:
            parts.append(f'情绪表达丰富，涉及{detected}个成分，具有较高的情绪觉察力。')

        # 元情绪层次
        if meta_level['level'] >= 4:
            parts.append('具备较高的元情绪能力，能够主动调节情绪。')
        elif meta_level['level'] >= 2:
            parts.append('具备反思性情绪意识，正在思考情绪背后的意义。')

        # 元情绪
        if meta_emotion['detected']:
            parts.append(f'存在元情绪现象：{meta_emotion["description"]}。')

        # 缺失成分
        if profile['total_detected'] >= 3:
            gaps = []
            scores = profile['scores']
            if scores.get('event', 0) < 0.3:
                gaps.append('事件描述')
            if scores.get('behavior', 0) < 0.3:
                gaps.append('行为描述')
            if gaps:
                parts.append(f'可尝试补充{gaps[0]}以更完整地理解情绪。')

        return ' '.join(parts)

    def _empty_analysis(self) -> Dict[str, Any]:
        return {
            'components': {},
            'meta_level': {
                'level': 0, 'level_name': '无意识',
                'level_description': '未意识到自身情绪状态',
                'confidence': 0.0,
            },
            'component_profile': {'scores': {}, 'total_detected': 0, 'total_matches': 0},
            'primary_component': 'none',
            'component_balance': '数据不足',
            'gaps': [],
            'meta_emotion_detected': False,
            'meta_emotion_desc': '',
            'insight': '暂无足够数据进行分析。',
        }


# =============================================================================
# 第三部分: SDT 动机类型识别
# 基于 Deci & Ryan (2000) 自我决定理论
# 动机内化连续体: 无动机 → 外部 → 内摄 → 认同 → 整合 → 内在
# + 三大基本需求: 自主感/能力感/连接感
# =============================================================================

class SDTMotivationType(Enum):
    """SDT 动机内化连续体"""
    AMOTIVATION = 0      # 无动机
    EXTERNAL = 1         # 外部调节
    INTROJECTED = 2      # 内摄调节
    IDENTIFIED = 3       # 认同调节
    INTEGRATED = 4       # 整合调节
    INTRINSIC = 5        # 内在动机


SDT_MOTIVATION_INFO = {
    SDTMotivationType.AMOTIVATION: {
        'name': '无动机',
        'self_determination': 0.0,
        'description': '缺乏行为意图或动机，看不到行为的意义',
        'typical_phrases': ['不知道为什么要', '无所谓', '随便', '都行',
                            '没意义', '懒得做', '不想做', '没劲'],
    },
    SDTMotivationType.EXTERNAL: {
        'name': '外部调节',
        'self_determination': 0.15,
        'description': '为获得奖励或避免惩罚而行动',
        'typical_phrases': ['不得不', '必须', '被要求', '强迫', '命令',
                            '否则就', '为了不被骂', '为了拿', '不这样做就会'],
    },
    SDTMotivationType.INTROJECTED: {
        'name': '内摄调节',
        'self_determination': 0.35,
        'description': '为避免内疚、羞耻或维护自尊而行动',
        'typical_phrases': ['应该', '必须', '不这样做就是不对', '愧疚',
                            '丢人', '没面子', '别人会怎么看', '好父母应该',
                            '合格的', '负责任的做法', '不能让人失望'],
    },
    SDTMotivationType.IDENTIFIED: {
        'name': '认同调节',
        'self_determination': 0.65,
        'description': '认同行为对个人的价值和意义',
        'typical_phrases': ['很重要', '有价值', '是为了', '有助于',
                            '为了孩子好', '为了将来', '为了健康',
                            '我理解这很重要', '我认为值得'],
    },
    SDTMotivationType.INTEGRATED: {
        'name': '整合调节',
        'self_determination': 0.85,
        'description': '行为与个人价值观和身份认同完全一致',
        'typical_phrases': ['这是我的一部分', '这就是我', '我选择这样做',
                            '这符合我的价值观', '我愿意', '我决定',
                            '经过思考我决定', '这是我想要的'],
    },
    SDTMotivationType.INTRINSIC: {
        'name': '内在动机',
        'self_determination': 1.0,
        'description': '出于兴趣、乐趣和内在满足而行动',
        'typical_phrases': ['喜欢', '享受', '有趣', '好玩', '热爱',
                            '沉浸', '着迷', '有成就感', '满足感',
                            '享受过程', '从中获得快乐'],
    },
}


class SDTBasicNeeds:
    """SDT 三大基本需求评估"""
    def __init__(self):
        self._autonomy_patterns = {
            'high': [r'(?:自己决定|自主|自由|选择权|按照自己的|独立)',
                     r'(?:我决定|我愿意|我选择|我自己来|按我自己的节奏)'],
            'low': [r'(?:被控制|被迫|没有选择|身不由己|不由自己)',
                    r'(?:被逼|被强迫|不让我|不许我|管得太死|窒息)'],
        }
        self._competence_patterns = {
            'high': [r'(?:能力|胜任|擅长|有信心|做得好|有成就感|进步)',
                     r'(?:学会了|掌握了|克服了|成长了|有进步|越来越好了)'],
            'low': [r'(?:无能|无力|做不到|不会|不行|失败|差劲|笨)',
                    r'(?:没能力|不够好|比不上|做不好|没用|废物|什么都不会)'],
        }
        self._relatedness_patterns = {
            'high': [r'(?:被理解|被接纳|被爱|被支持|归属|连接|亲密|温暖)',
                     r'(?:有人懂我|有人陪|在一起|关心|在乎|重视)'],
            'low': [r'(?:孤独|被忽视|被排斥|被冷落|被拒绝|不被理解)',
                    r'(?:没人理解|没人懂|没人在乎|一个人|孤立|陌生)'],
        }

    def assess(self, text: str) -> Dict[str, Any]:
        """评估三大基本需求的满足状态"""
        result = {}
        for need_name, patterns in [
            ('autonomy', self._autonomy_patterns),
            ('competence', self._competence_patterns),
            ('relatedness', self._relatedness_patterns),
        ]:
            high_matches = []
            for p in patterns['high']:
                high_matches.extend(re.findall(p, text))
            low_matches = []
            for p in patterns['low']:
                low_matches.extend(re.findall(p, text))

            # 得分 = high信号 / (high + low + 1)
            high_score = len(high_matches) * 0.25
            low_score = len(low_matches) * 0.25
            net_score = max(-1.0, min(1.0, high_score - low_score))

            # 归一化到 [0, 1]
            satisfaction = (net_score + 1) / 2

            if satisfaction >= 0.6:
                status = '满足'
            elif satisfaction >= 0.4:
                status = '一般'
            else:
                status = '不满足'

            result[need_name] = {
                'satisfaction': round(satisfaction, 4),
                'status': status,
                'high_signals': high_matches[:5],
                'low_signals': low_matches[:5],
                'need_name': {
                    'autonomy': '自主感',
                    'competence': '能力感',
                    'relatedness': '连接感',
                }[need_name],
            }

        return result


class SDTDetector:
    """
    SDT 动机类型识别器
    检测用户在文本中表达的动机类型（动机内化连续体）
    以及三大基本需求的满足状态
    """

    def __init__(self):
        self.needs = SDTBasicNeeds()

    def detect(self, text: str) -> Dict[str, Any]:
        """
        检测文本中的 SDT 动机类型和基本需求状态

        Args:
            text: 用户输入文本

        Returns:
            dict: {
                'motivation': { 动机类型检测 },
                'basic_needs': { 三大基本需求 },
                'intrinsic_motivation_score': 0-1,  # 内在动机综合分
                'self_determination_level': str,     # 自我决定程度
                'need_satisfaction_summary': str,    # 需求满足概览
            }
        """
        if not text or not text.strip():
            return self._empty_result()

        # 1. 检测动机类型
        motivation_scores = {}
        for m_type, info in SDT_MOTIVATION_INFO.items():
            matches = []
            for phrase in info['typical_phrases']:
                if phrase in text:
                    matches.append(phrase)
            score = min(1.0, len(matches) * 0.25)
            motivation_scores[m_type.value] = {
                'type': info['name'],
                'self_determination': info['self_determination'],
                'score': round(score, 4),
                'matches': matches[:5],
                'description': info['description'],
            }

        # 2. 找出主导动机
        valid_motivations = {
            k: v for k, v in motivation_scores.items() if v['score'] > 0
        }
        if not valid_motivations:
            primary_type = SDTMotivationType.AMOTIVATION.value
            primary_info = SDT_MOTIVATION_INFO[SDTMotivationType.AMOTIVATION]
            primary = {
                'type': primary_info['name'],
                'self_determination': primary_info['self_determination'],
                'score': 0.2,
                'matches': [],
                'description': primary_info['description'],
            }
        else:
            primary_type = max(valid_motivations, key=lambda k: valid_motivations[k]['score'])
            primary = valid_motivations[primary_type]

        # 3. 内在动机综合评分（加权平均）
        total_weight = sum(v['score'] * v['self_determination'] for v in valid_motivations.values())
        total_score = sum(v['score'] for v in valid_motivations.values())
        intrinsic_score = total_weight / total_score if total_score > 0 else 0.1

        # 4. 自我决定程度
        if intrinsic_score >= 0.8:
            sd_level = '高自我决定'
        elif intrinsic_score >= 0.5:
            sd_level = '中等自我决定'
        elif intrinsic_score >= 0.2:
            sd_level = '低自我决定'
        else:
            sd_level = '无自我决定'

        # 5. 三大基本需求
        basic_needs = self.needs.assess(text)

        # 6. 需求满足概览
        need_statuses = [v['status'] for v in basic_needs.values()]
        satisfied_count = need_statuses.count('满足')
        unsatisfied_count = need_statuses.count('不满足')
        if satisfied_count >= 2:
            need_summary = '基本需求整体满足'
        elif unsatisfied_count >= 2:
            need_summary = '基本需求整体不满足'
        else:
            need_summary = '基本需求部分满足'

        # 7. 内在动机公式: IntrinsicMotivation ≈ Autonomy × Competence × Relatedness
        auto_sat = basic_needs['autonomy']['satisfaction']
        comp_sat = basic_needs['competence']['satisfaction']
        rel_sat = basic_needs['relatedness']['satisfaction']
        sdt_formula_score = round(auto_sat * comp_sat * rel_sat, 4)

        return {
            'motivation': {
                'primary_type': primary['type'],
                'primary_self_determination': primary['self_determination'],
                'primary_score': primary['score'],
                'primary_matches': primary['matches'],
                'all_types': motivation_scores,
            },
            'basic_needs': basic_needs,
            'intrinsic_motivation_score': round(intrinsic_score, 4),
            'sdt_formula_score': sdt_formula_score,
            'self_determination_level': sd_level,
            'need_satisfaction_summary': need_summary,
        }

    def _empty_result(self) -> Dict[str, Any]:
        return {
            'motivation': {
                'primary_type': '无动机',
                'primary_self_determination': 0.0,
                'primary_score': 0.0,
                'primary_matches': [],
                'all_types': {},
            },
            'basic_needs': {
                'autonomy': {'satisfaction': 0.5, 'status': '一般', 'need_name': '自主感',
                             'high_signals': [], 'low_signals': []},
                'competence': {'satisfaction': 0.5, 'status': '一般', 'need_name': '能力感',
                               'high_signals': [], 'low_signals': []},
                'relatedness': {'satisfaction': 0.5, 'status': '一般', 'need_name': '连接感',
                                'high_signals': [], 'low_signals': []},
            },
            'intrinsic_motivation_score': 0.125,
            'sdt_formula_score': 0.125,
            'self_determination_level': '中等自我决定',
            'need_satisfaction_summary': '数据不足',
        }


# =============================================================================
# 第四部分: 情绪理性三维度评估
# 认知理性(Cognitive Rationality) / 战略理性(Strategic Rationality) / 整体理性(Holistic Rationality)
# 理论基础: 双系统理论(Kahneman)、生态理性(Gigerenzer)、整体理性(心虫哲学引擎)
# =============================================================================

class RationalityDimension(Enum):
    """理性三维度"""
    COGNITIVE = 'cognitive'       # 认知理性 — 逻辑一致性、事实准确性
    STRATEGIC = 'strategic'       # 战略理性 — 目标导向、长期效益
    HOLISTIC = 'holistic'         # 整体理性 — 真善美整合、系统平衡


RATIONALITY_INDICATORS = {
    RationalityDimension.COGNITIVE: {
        'name': '认知理性',
        'description': '逻辑一致性、事实准确性、因果推理能力',
        'high_indicators': [
            r'(?:因为.*所以|如果.*那么|原因|结果|逻辑|事实|证据)',
            r'(?:数据|统计|研究|调查|研究显示|调查表明|科学)',
            r'(?:分析|推理|判断|结论|归纳|演绎|论证)',
            r'(?:冷静|理性|客观|中立|就事论事)',
            r'(?:首先|其次|最后|一方面|另一方面)',
        ],
        'low_indicators': [
            r'(?:不讲道理|说不通|逻辑混乱|前后矛盾)',
            r'(?:瞎说|胡说|乱说|不讲理|不可理喻)',
            r'(?:情绪化|失控|没道理|不讲逻辑)',
        ],
    },
    RationalityDimension.STRATEGIC: {
        'name': '战略理性',
        'description': '目标导向、长远考量、资源优化',
        'high_indicators': [
            r'(?:目标|计划|规划|长远|长期|未来|将来)',
            r'(?:策略|方案|步骤|方法|路径|路线)',
            r'(?:权衡|平衡|取舍|优先级|重点|关键)',
            r'(?:效果|结果|效益|效率|成本|收益)',
            r'(?:为了.*更好|为了.*将来|为.*做准备)',
        ],
        'low_indicators': [
            r'(?:走一步看一步|没想那么远|过一天算一天)',
            r'(?:顾不了那么多|先不管了|先过了这关再说)',
            r'(?:短视|急功近利|只顾眼前|没有计划)',
        ],
    },
    RationalityDimension.HOLISTIC: {
        'name': '整体理性',
        'description': '真善美整合、系统思维、多视角兼顾',
        'high_indicators': [
            r'(?:整体|全局|系统|全面|综合|多方)',
            r'(?:平衡|和谐|兼顾|整合|协调|统一)',
            r'(?:真善美|真|善|美|对大家都好|共同)',
            r'(?:理解.*也理解|站在.*角度|换位思考|共情)',
            r'(?:意义|价值|本质|根源|系统思考)',
        ],
        'low_indicators': [
            r'(?:只看到|只看|片面的|偏激|极端|钻牛角尖)',
            r'(?:非黑即白|全有全无|要么.*要么|不是.*就是)',
            r'(?:只顾自己|自私|不管别人|不考虑)',
        ],
    },
}


class RationalityAssessor:
    """
    情绪理性三维度评估器

    评估用户在情绪表达中的理性水平:
    - 认知理性: 逻辑一致性、事实准确性
    - 战略理性: 目标导向、长期效益
    - 整体理性: 真善美整合、系统平衡
    """

    def assess(self, text: str) -> Dict[str, Any]:
        """
        对文本进行理性三维度评估

        Args:
            text: 用户输入文本

        Returns:
            dict: {
                'dimensions': { 三维度评估 },
                'overall_rationality': 0-1,   # 综合理性得分
                'dominant_dimension': str,     # 主导理性维度
                'profile': str,                # 理性特征描述
                'recommendations': [str],      # 改进建议
            }
        """
        if not text or not text.strip():
            return self._empty_result()

        dimensions = {}
        for dim, config in RATIONALITY_INDICATORS.items():
            high_matches = []
            for p in config['high_indicators']:
                high_matches.extend(re.findall(p, text))
            low_matches = []
            for p in config['low_indicators']:
                low_matches.extend(re.findall(p, text))

            high_score = min(1.0, len(high_matches) * 0.2)
            low_score = min(1.0, len(low_matches) * 0.25)
            net = max(0.0, min(1.0, high_score - low_score + 0.5))

            dimensions[dim.value] = {
                'name': config['name'],
                'description': config['description'],
                'score': round(net, 4),
                'high_signals': high_matches[:5],
                'low_signals': low_matches[:5],
                'level': '高' if net >= 0.7 else ('中' if net >= 0.4 else '低'),
            }

        # 综合理性得分
        overall = sum(d['score'] for d in dimensions.values()) / len(dimensions)

        # 主导维度
        dominant = max(dimensions, key=lambda k: dimensions[k]['score'])
        dominant_info = dimensions[dominant]

        # 理性特征描述
        profile_parts = []
        for d in dimensions.values():
            if d['score'] >= 0.7:
                profile_parts.append(f'{d["name"]}较强（{d["level"]}）')
            elif d['score'] < 0.4:
                profile_parts.append(f'{d["name"]}偏弱（{d["level"]}）')
            else:
                profile_parts.append(f'{d["name"]}中等（{d["level"]}）')
        profile = '，'.join(profile_parts)

        # 改进建议
        recommendations = []
        if dimensions[RationalityDimension.COGNITIVE.value]['score'] < 0.4:
            recommendations.append('可尝试更多基于事实的分析，减少情绪化判断')
        if dimensions[RationalityDimension.STRATEGIC.value]['score'] < 0.4:
            recommendations.append('可尝试从更长远的角度思考，建立明确的目标和计划')
        if dimensions[RationalityDimension.HOLISTIC.value]['score'] < 0.4:
            recommendations.append('可尝试从多视角看待问题，兼顾各方需求和系统影响')
        if all(d['score'] >= 0.7 for d in dimensions.values()):
            recommendations.append('理性水平较高，继续保持多维度的思考方式')

        return {
            'dimensions': dimensions,
            'overall_rationality': round(overall, 4),
            'dominant_dimension': dominant_info['name'],
            'profile': profile,
            'recommendations': recommendations,
        }

    def _empty_result(self) -> Dict[str, Any]:
        return {
            'dimensions': {
                'cognitive': {'name': '认知理性', 'score': 0.5, 'level': '中',
                              'high_signals': [], 'low_signals': []},
                'strategic': {'name': '战略理性', 'score': 0.5, 'level': '中',
                              'high_signals': [], 'low_signals': []},
                'holistic': {'name': '整体理性', 'score': 0.5, 'level': '中',
                             'high_signals': [], 'low_signals': []},
            },
            'overall_rationality': 0.5,
            'dominant_dimension': '认知理性',
            'profile': '数据不足，默认中等水平',
            'recommendations': [],
        }


# =============================================================================
# 第五部分: 心虫情绪分析引擎（统一入口）
# =============================================================================

class HeartFlowEmotionEngine:
    """
    心虫情绪分析引擎 — 统一分析入口

    整合四大模块:
    1. PADDetector — PAD三维情绪检测
    2. MetaEmotionMonitor — 六层次元情绪分析
    3. SDTDetector — 动机类型识别
    4. RationalityAssessor — 理性三维度评估
    """

    def __init__(self):
        self.pad = PADDetector()
        self.meta_emotion = MetaEmotionMonitor()
        self.sdt = SDTDetector()
        self.rationality = RationalityAssessor()

    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        全量情绪分析

        Args:
            text: 用户输入文本
            context: 可选上下文信息

        Returns:
            dict: 综合分析结果（包含所有四个模块的输出）
        """
        if not text or not text.strip():
            return self._empty_result()

        result = {
            'pad_analysis': self.pad.detect(text),
            'meta_emotion_analysis': self.meta_emotion.analyze(text, context),
            'sdt_analysis': self.sdt.detect(text),
            'rationality_analysis': self.rationality.assess(text),
            'summary': self._generate_summary(text),
        }

        return result

    def analyze_pad_only(self, text: str) -> Dict[str, Any]:
        """仅分析 PAD 情绪维度"""
        return self.pad.detect(text)

    def analyze_meta_only(self, text: str) -> Dict[str, Any]:
        """仅分析元情绪六层次"""
        return self.meta_emotion.analyze(text)

    def analyze_sdt_only(self, text: str) -> Dict[str, Any]:
        """仅分析 SDT 动机类型"""
        return self.sdt.detect(text)

    def analyze_rationality_only(self, text: str) -> Dict[str, Any]:
        """仅分析理性三维度"""
        return self.rationality.assess(text)

    def _generate_summary(self, text: str) -> Dict[str, Any]:
        """生成综合摘要"""
        pad_result = self.pad.detect(text)
        meta_result = self.meta_emotion.analyze(text)
        sdt_result = self.sdt.detect(text)
        rat_result = self.rationality.assess(text)

        # 情绪状态摘要
        emotion_cn = pad_result['dominant_emotion_cn']
        pad_01 = pad_result['pad_01']

        # 动机摘要
        motivation_type = sdt_result['motivation']['primary_type']

        # 理性摘要
        overall_rat = rat_result['overall_rationality']

        # 综合情绪强度（PAD arousal + meta emotion 成分覆盖度）
        arousal_score = pad_01['arousal']
        meta_coverage = meta_result['component_profile']['total_detected'] / 6.0
        composite_intensity = round((arousal_score * 0.6 + meta_coverage * 0.4), 4)

        return {
            'primary_emotion_cn': emotion_cn,
            'pad_01': pad_01,
            'composite_emotional_intensity': composite_intensity,
            'meta_emotion_level': meta_result['meta_level']['level_name'],
            'meta_emotion_level_value': meta_result['meta_level']['level'],
            'primary_motivation': motivation_type,
            'intrinsic_motivation': sdt_result['intrinsic_motivation_score'],
            'need_satisfaction': sdt_result['need_satisfaction_summary'],
            'overall_rationality': overall_rat,
            'rationality_profile': rat_result['profile'],
            'dominant_rationality': rat_result['dominant_dimension'],
        }

    def _empty_result(self) -> Dict[str, Any]:
        return {
            'pad_analysis': PADDetector()._empty_result(),
            'meta_emotion_analysis': MetaEmotionMonitor()._empty_analysis(),
            'sdt_analysis': SDTDetector()._empty_result(),
            'rationality_analysis': RationalityAssessor()._empty_result(),
            'summary': {
                'primary_emotion_cn': '中性',
                'pad_01': {'pleasure': 0.5, 'arousal': 0.5, 'dominance': 0.5},
                'composite_emotional_intensity': 0.0,
                'meta_emotion_level': '无意识',
                'meta_emotion_level_value': 0,
                'primary_motivation': '无动机',
                'intrinsic_motivation': 0.0,
                'need_satisfaction': '数据不足',
                'overall_rationality': 0.5,
                'rationality_profile': '数据不足',
                'dominant_rationality': '认知理性',
            },
        }


# =============================================================================
# CLI 入口
# =============================================================================

def main():
    """CLI 入口 — 支持单次分析和诊断模式"""
    import argparse

    parser = argparse.ArgumentParser(
        description='心虫情绪分析引擎 (HeartFlow Emotion Analysis Engine)')
    parser.add_argument('-i', '--input', type=str, help='输入文本')
    parser.add_argument('-m', '--mode', type=str, default='full',
                        choices=['full', 'pad', 'meta', 'sdt', 'rationality', 'diagnostic'],
                        help='分析模式 (默认: full)')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--pretty', action='store_true', help='美化 JSON 输出')

    args = parser.parse_args()

    engine = HeartFlowEmotionEngine()

    if not args.input:
        print("请输入文本 (输入空行结束):")
        lines = []
        while True:
            try:
                line = input()
                if not line:
                    break
                lines.append(line)
            except EOFError:
                break
        args.input = '\n'.join(lines)

    if not args.input:
        print("未输入文本")
        return

    mode_map = {
        'pad': engine.analyze_pad_only,
        'meta': engine.analyze_meta_only,
        'sdt': engine.analyze_sdt_only,
        'rationality': engine.analyze_rationality_only,
        'full': engine.analyze,
        'diagnostic': lambda t: {
            'input': t,
            'pad': engine.analyze_pad_only(t),
            'meta_emotion': engine.analyze_meta_only(t),
            'sdt': engine.analyze_sdt_only(t),
            'rationality': engine.analyze_rationality_only(t),
            'full_summary': engine.analyze(t)['summary'],
        },
    }

    result = mode_map[args.mode](args.input)

    if args.json:
        indent = 2 if args.pretty else None
        print(json.dumps(result, ensure_ascii=False, indent=indent))
    else:
        print(f"\n{'='*60}")
        print(f"心虫情绪分析引擎 — 模式: {args.mode}")
        print(f"{'='*60}")

        if args.mode == 'full' or args.mode == 'diagnostic':
            summary = result if args.mode == 'diagnostic' else result['summary']
            if isinstance(summary, dict) and 'primary_emotion_cn' in summary:
                s = summary
                print(f"\n📊 综合摘要:")
                print(f"  主导情绪: {s['primary_emotion_cn']}")
                print(f"  PAD: 愉悦度={s['pad_01']['pleasure']:.3f} "
                      f"唤醒度={s['pad_01']['arousal']:.3f} "
                      f"支配度={s['pad_01']['dominance']:.3f}")
                print(f"  情绪综合强度: {s['composite_emotional_intensity']:.3f}")
                print(f"  元情绪层次: {s['meta_emotion_level']} (Lv.{s['meta_emotion_level_value']})")
                print(f"  主导动机: {s['primary_motivation']}")
                print(f"  内在动机得分: {s['intrinsic_motivation']:.3f}")
                print(f"  需求满足: {s['need_satisfaction']}")
                print(f"  整体理性: {s['overall_rationality']:.3f}")
                print(f"  理性特征: {s['rationality_profile']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

        print(f"\n{'='*60}")


if __name__ == '__main__':
    main()
