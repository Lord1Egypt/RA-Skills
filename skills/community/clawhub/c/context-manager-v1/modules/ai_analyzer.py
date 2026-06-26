#!/usr/bin/env python3
"""
AI Analyzer - AI 分析增强模块

借鉴 knowledge-workflow 的 evolve.py
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class AIAnalyzer:
    """AI 分析增强模块"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
        
        # AI 模型配置
        self.ai_model = config.get("ai_model", "qwen3.5-plus")
        self.api_key = config.get("api_key", "")
    
    def analyze_meaning_tags(self, content: str) -> List[str]:
        """
        AI 分析意义标签（增强版）
        
        借鉴 knowledge-workflow 的 tag.py
        """
        # 简化版：基于规则 + 关键词
        # TODO: 集成 AI API
        
        meaning_tags = {
            "成长痛点": {
                "keywords": ["痛点", "困难", "挑战", "挣扎", "困惑", "迷茫", "瓶颈"],
                "weight": 1.0
            },
            "关系锚点": {
                "keywords": ["朋友", "争论", "关系", "理解", "家人", "同事", "伴侣", "沟通"],
                "weight": 1.0
            },
            "灵感触发": {
                "keywords": ["洞察", "顿悟", "灵光", "想到", "启发", "灵感", "觉醒"],
                "weight": 1.2  # 灵感更重要
            },
            "认知冲突": {
                "keywords": ["冲突", "矛盾", "困惑", "犹豫", "纠结", "怀疑", "动摇"],
                "weight": 1.1
            },
            "决策背景": {
                "keywords": ["决定", "选择", "决策", "犹豫", "权衡", "取舍", "考虑"],
                "weight": 1.0
            }
        }
        
        tags = []
        for tag, data in meaning_tags.items():
            score = sum(data["weight"] for kw in data["keywords"] if kw in content)
            if score > 0.5:  # 阈值
                tags.append(f"#{tag}#")
        
        return tags
    
    def analyze_emotion(self, content: str) -> Dict[str, Any]:
        """
        AI 情绪分析（增强版）
        """
        emotion_keywords = {
            "positive": ["开心", "高兴", "兴奋", "满意", "感动", "欣慰", "自豪"],
            "negative": ["难过", "生气", "失望", "焦虑", "痛苦", "沮丧", "懊恼"],
            "neutral": ["思考", "分析", "观察", "记录", "总结"]
        }
        
        scores = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }
        
        for emotion, keywords in emotion_keywords.items():
            scores[emotion] = sum(2 for kw in keywords if kw in content)
        
        # 判断主导情绪
        max_emotion = max(scores, key=scores.get)
        
        return {
            "emotion": max_emotion,
            "scores": scores,
            "confidence": scores[max_emotion] / sum(scores.values()) if sum(scores.values()) > 0 else 0
        }
    
    def extract_keywords(self, content: str, top_n: int = 10) -> List[str]:
        """
        AI 提取关键词（增强版）
        
        借鉴 knowledge-workflow 的 store.py
        """
        import re
        
        # 分词（简化版）
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
        
        # 停用词
        stop_words = {"这个", "那个", "什么", "怎么", "如何", "我们", "你们", "他们"}
        words = [w for w in words if w not in stop_words]
        
        # 词频统计
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # 返回高频词
        sorted_words = sorted(word_count.items(), key=lambda x: -x[1])
        return [word for word, count in sorted_words[:top_n]]
    
    def generate_summary(self, items: List[Dict]) -> str:
        """
        AI 生成总结（用于认知日志）
        
        借鉴 knowledge-workflow 的 output.py
        """
        if not items:
            return ""
        
        # 简化版：拼接 + 提炼
        summary_parts = []
        for item in items:
            content = item.get("content", "")
            judgment = item.get("judgment", "")
            summary_parts.append(f"{content} → {judgment}")
        
        return " | ".join(summary_parts)
