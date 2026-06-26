"""
对话管理器 - Dialogue Manager
"""

import re
from typing import Dict, List, Optional


class DialogueManager:
    """对话管理器类"""
    
    def __init__(self):
        self.context = []
        self.intents = {
            'greeting': ['你好', '您好', '嗨', 'hello', 'hi'],
            'farewell': ['再见', '拜拜', 'bye', 'goodbye'],
            'booking': ['预订', '预约', '订', 'book'],
            'query': ['查询', '查', 'search', 'query']
        }
    
    def classify_intent(self, text: str) -> str:
        """意图分类"""
        text_lower = text.lower()
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        return 'unknown'
    
    def extract_entities(self, text: str) -> Dict[str, str]:
        """实体抽取（简化版）"""
        entities = {}
        
        # 时间实体
        time_pattern = r'(今天|明天|后天|(\d{1,2})月(\d{1,2})日?)'
        time_match = re.search(time_pattern, text)
        if time_match:
            entities['time'] = time_match.group(0)
        
        # 地点实体
        location_pattern = r'(北京|上海|广州|深圳|杭州)'
        loc_match = re.search(location_pattern, text)
        if loc_match:
            entities['location'] = loc_match.group(0)
        
        return entities
    
    def process(self, user_input: str) -> str:
        """处理用户输入"""
        self.context.append({'role': 'user', 'content': user_input})
        
        intent = self.classify_intent(user_input)
        entities = self.extract_entities(user_input)
        
        # 基于意图生成回复
        responses = {
            'greeting': '您好！有什么可以帮助您的吗？',
            'farewell': '再见！祝您有愉快的一天！',
            'booking': f"好的，正在为您处理预订请求... (检测到: {entities})",
            'query': f"正在为您查询... (检测到: {entities})",
            'unknown': '抱歉，我不太理解您的意思，可以换个说法吗？'
        }
        
        response = responses.get(intent, responses['unknown'])
        self.context.append({'role': 'assistant', 'content': response})
        
        return response
    
    def get_context(self) -> List[Dict]:
        """获取对话上下文"""
        return self.context
