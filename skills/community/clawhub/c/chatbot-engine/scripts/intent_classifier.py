"""
Intent Classifier - 意图分类器
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import json
import os
import re


@dataclass
class Intent:
    """意图"""
    name: str
    confidence: float
    entities: Dict[str, str] = None
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = {}


class IntentClassifier:
    """意图分类器"""
    
    def __init__(self, model: str = 'default'):
        self.model = model
        self.intents: Dict[str, Dict] = {}
        self.patterns: Dict[str, List[str]] = {}
        self.keywords: Dict[str, List[str]] = {}
    
    def add_intent(self, name: str, patterns: List[str],
                   keywords: Optional[List[str]] = None):
        """
        添加意图
        
        Args:
            name: 意图名称
            patterns: 匹配模式 (支持正则)
            keywords: 关键词列表
        """
        self.intents[name] = {
            'patterns': patterns,
            'keywords': keywords or []
        }
        self.patterns[name] = patterns
        self.keywords[name] = keywords or []
    
    def classify(self, text: str) -> Dict:
        """
        分类文本意图
        
        Returns:
            {'intent': str, 'confidence': float, 'entities': dict}
        """
        text = text.lower()
        scores = {}
        
        for intent_name, config in self.intents.items():
            score = 0.0
            entities = {}
            
            # 模式匹配
            for pattern in config['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 0.5
                    # 提取实体 (简化版)
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        entities['match'] = matches[0]
            
            # 关键词匹配
            for keyword in config['keywords']:
                if keyword.lower() in text:
                    score += 0.3
            
            scores[intent_name] = (score, entities)
        
        # 选择最高分的意图
        if scores:
            best_intent = max(scores, key=lambda x: scores[x][0])
            best_score, best_entities = scores[best_intent]
            
            # 归一化置信度
            confidence = min(best_score, 1.0)
            
            return {
                'intent': best_intent,
                'confidence': confidence,
                'entities': best_entities
            }
        
        return {'intent': 'unknown', 'confidence': 0.0, 'entities': {}}
    
    def batch_classify(self, texts: List[str]) -> List[Dict]:
        """批量分类"""
        return [self.classify(text) for text in texts]
    
    def save(self, path: str):
        """保存意图配置"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.intents, f, ensure_ascii=False, indent=2)
        print(f"意图配置已保存: {path}")
    
    def load(self, path: str):
        """加载意图配置"""
        if not os.path.exists(path):
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        
        for name, config in self.intents.items():
            self.patterns[name] = config['patterns']
            self.keywords[name] = config['keywords']
        
        print(f"意图配置已加载: {path}")


# 预设意图
DEFAULT_INTENTS = {
    'greeting': {
        'patterns': [r'你好', r'您好', r'hi', r'hello', r'在吗'],
        'keywords': ['你好', '您好', 'hi', 'hello']
    },
    'farewell': {
        'patterns': [r'再见', r'拜拜', r'bye', r'明天见'],
        'keywords': ['再见', '拜拜', 'bye']
    },
    'book_flight': {
        'patterns': [r'订.*机票', r'飞.*去', r'从.*到.*的机票'],
        'keywords': ['机票', '航班', '飞机']
    },
    'book_hotel': {
        'patterns': [r'订.*酒店', r'住.*宿', r'房间'],
        'keywords': ['酒店', '住宿', '房间', '订房']
    },
    'query_weather': {
        'patterns': [r'.*天气.*', r'.*温度.*', r'.*下雨.*'],
        'keywords': ['天气', '温度', '下雨', '晴天']
    },
    'query_time': {
        'patterns': [r'.*时间.*', r'几点', r'日期'],
        'keywords': ['时间', '几点', '日期', '现在']
    }
}


if __name__ == '__main__':
    classifier = IntentClassifier()
    
    # 加载预设意图
    for name, config in DEFAULT_INTENTS.items():
        classifier.add_intent(name, config['patterns'], config['keywords'])
    
    # 测试
    test_texts = [
        "你好",
        "我想订一张去北京的机票",
        "今天天气怎么样？"
    ]
    
    for text in test_texts:
        result = classifier.classify(text)
        print(f"'{text}' -> {result}")
