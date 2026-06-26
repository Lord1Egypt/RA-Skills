#!/usr/bin/env python3
"""
Meaning Tagger - 意义标签体系

标签类型：
- #成长痛点# - 成长过程中的痛点
- #关系锚点# - 重要关系的锚点事件
- #灵感触发# - 灵感触发的瞬间
- #认知冲突# - 认知冲突的时刻
- #决策背景# - 重要决策的背景
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class MeaningTagger:
    """意义标签体系"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
        
        # 意义标签关键词（扩展版）
        self.meaning_tags = {
            "成长痛点": {
                "keywords": ["痛点", "困难", "挑战", "挣扎", "困惑", "迷茫", "瓶颈"],
                "description": "成长过程中的痛点"
            },
            "关系锚点": {
                "keywords": ["朋友", "争论", "关系", "理解", "家人", "同事", "伴侣", "沟通"],
                "description": "重要关系的锚点事件"
            },
            "灵感触发": {
                "keywords": ["洞察", "顿悟", "灵光", "想到", "启发", "灵感", "觉醒"],
                "description": "灵感触发的瞬间"
            },
            "认知冲突": {
                "keywords": ["冲突", "矛盾", "困惑", "犹豫", "纠结", "怀疑", "动摇"],
                "description": "认知冲突的时刻"
            },
            "决策背景": {
                "keywords": ["决定", "选择", "决策", "犹豫", "权衡", "取舍", "考虑"],
                "description": "重要决策的背景"
            }
        }
    
    def tag(self, context_id: str, content: str) -> Dict[str, Any]:
        """
        打标（意义标签体系）
        
        Args:
            context_id: 上下文 ID
            content: 内容
        
        Returns:
            打标结果
        """
        # 提取意义标签
        tags = self.extract_meaning_tags(content)
        
        # 提取关键词
        keywords = self.extract_keywords(content)
        
        # 更新上下文文件
        self._update_context(context_id, tags, keywords)
        
        return {
            "context_id": context_id,
            "tags": tags,
            "keywords": keywords,
            "tagged_at": datetime.now().isoformat(),
            "status": "tagged"
        }
    
    def extract_meaning_tags(self, content: str) -> List[str]:
        """提取意义标签"""
        tags = []
        
        for tag, data in self.meaning_tags.items():
            if any(kw in content for kw in data["keywords"]):
                tags.append(f"#{tag}#")
        
        return tags
    
    def extract_keywords(self, content: str) -> List[str]:
        """提取关键词（简化版）"""
        # 分词（简化版：按标点分割）
        import re
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
        
        # 统计词频
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # 返回高频词
        sorted_words = sorted(word_count.items(), key=lambda x: -x[1])
        return [word for word, count in sorted_words[:10]]
    
    def _update_context(self, context_id: str, tags: List[str], keywords: List[str]):
        """更新上下文文件"""
        context_path = self.base_path / "inbox" / f"{context_id}.json"
        
        if context_path.exists():
            context = json.loads(context_path.read_text())
            context["tags"] = tags
            context["keywords"] = keywords
            
            # 移动到 contexts 目录
            contexts_path = self.base_path / "contexts" / f"{context_id}.json"
            contexts_path.parent.mkdir(parents=True, exist_ok=True)
            contexts_path.write_text(json.dumps(context, indent=2, ensure_ascii=False))
