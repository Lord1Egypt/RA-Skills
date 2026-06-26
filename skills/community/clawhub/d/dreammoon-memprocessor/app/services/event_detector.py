"""事件检测服务"""
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.models import Event, EventType, MemoryItem


class EventDetector:
    """事件检测器 - 分析内容提取重要事件"""
    
    def __init__(self):
        # 关键词模式
        self.patterns = {
            EventType.DECISION: {
                "keywords": ["决定", "确认", "采用", "方案", "选择", "定下来", "就这个", "确定"],
                "weight": 50
            },
            EventType.IMPORTANT: {
                "keywords": ["重要", "关键", "核心", "主要", "必须", "一定", "务必"],
                "weight": 30
            },
            EventType.ERROR: {
                "keywords": ["错误", "失败", "bug", "问题", "报错", "异常", "出错"],
                "weight": 25
            },
            EventType.LESSON: {
                "keywords": ["学到", "明白", "原来", "发现", "意识到", "理解", "懂得"],
                "weight": 20
            },
            EventType.COMPLETION: {
                "keywords": ["完成", "搞定", "结束", "关闭", "解决了", "ok", "好了"],
                "weight": 35
            },
            EventType.QUESTION: {
                "keywords": ["?", "？", "怎么", "什么", "为什么", "如何", "吗"],
                "weight": 10
            },
            EventType.RELATIONSHIP: {
                "keywords": ["关系", "约定", "承诺", "信任", "理解", "陪伴", "情感"],
                "weight": 60
            },
            EventType.SYSTEM: {
                "keywords": ["架构", "部署", "配置", "节点", "备份", "健康检查", "监控"],
                "weight": 40
            }
        }
        
        # 敏感信息模式
        self.sensitive_patterns = [
            re.compile(r'ghp_[a-zA-Z0-9]{36}'),  # GitHub token
            re.compile(r'sk-[a-zA-Z0-9]{48}'),   # OpenAI key
            re.compile(r'[a-zA-Z0-9]{32,}'),     # 长串可能为密钥
            re.compile(r'password[:=]\s*\S+', re.I),
            re.compile(r'token[:=]\s*\S+', re.I),
            re.compile(r'secret[:=]\s*\S+', re.I),
            re.compile(r'api[_-]?key[:=]\s*\S+', re.I),
        ]
    
    def analyze(self, content: str, context: Optional[Dict] = None) -> Tuple[int, List[Event], bool]:
        """
        分析内容
        
        Returns:
            (importance_score, events, is_sensitive)
        """
        context = context or {}
        score = 0
        events = []
        
        # 检测敏感信息
        is_sensitive = self._detect_sensitive(content)
        if is_sensitive:
            score -= 50  # 降低重要性
        
        # 检测各类事件
        for event_type, pattern in self.patterns.items():
            matches = self._find_matches(content, pattern["keywords"])
            if matches:
                weight = pattern["weight"]
                score += weight
                
                events.append(Event(
                    type=event_type,
                    category=event_type.value,
                    content=content[:200],
                    confidence=min(len(matches) / len(pattern["keywords"]), 1.0),
                    matches=matches
                ))
        
        # 上下文增强
        ref_count = context.get("reference_count", 0)
        score += ref_count * 5
        
        if context.get("task_active"):
            score += 15
        
        if context.get("is_user_explicit"):
            score += 20
        
        # 限制范围
        score = max(0, min(100, score))
        
        return score, events, is_sensitive
    
    def analyze_session(self, messages: List[Dict]) -> Dict:
        """分析整个会话"""
        session = {
            "decisions": [],
            "errors": [],
            "lessons": [],
            "important_moments": [],
            "topics": set()
        }
        
        for i, msg in enumerate(messages):
            content = msg.get("content", "")
            role = msg.get("role", "")
            
            context = {
                "reference_count": msg.get("reference_count", 0),
                "task_active": True
            }
            
            score, events, is_sensitive = self.analyze(content, context)
            
            # 收集决策
            if any(e.type == EventType.DECISION for e in events) and score >= 70:
                session["decisions"].append({
                    "index": i,
                    "role": role,
                    "content": content,
                    "score": score
                })
            
            # 收集错误
            if any(e.type == EventType.ERROR for e in events):
                session["errors"].append({
                    "index": i,
                    "role": role,
                    "content": content
                })
            
            # 收集学习内容
            if any(e.type == EventType.LESSON for e in events):
                session["lessons"].append({
                    "index": i,
                    "role": role,
                    "content": content
                })
            
            # 记录重要时刻
            if score >= 60:
                session["important_moments"].append({
                    "index": i,
                    "role": role,
                    "content": content[:100],
                    "score": score
                })
        
        return session
    
    def _detect_sensitive(self, content: str) -> bool:
        """检测敏感信息"""
        for pattern in self.sensitive_patterns:
            if pattern.search(content):
                return True
        return False
    
    def _find_matches(self, content: str, keywords: List[str]) -> List[str]:
        """查找匹配的关键词"""
        content_lower = content.lower()
        matches = []
        for keyword in keywords:
            if keyword.lower() in content_lower:
                matches.append(keyword)
        return matches


# 单例
_detector: Optional[EventDetector] = None


def get_event_detector() -> EventDetector:
    """获取事件检测器单例"""
    global _detector
    if _detector is None:
        _detector = EventDetector()
    return _detector
