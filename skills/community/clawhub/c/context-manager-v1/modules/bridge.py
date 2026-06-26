#!/usr/bin/env python3
"""
Context Bridge - 上下文桥接增强版

借鉴 knowledge-workflow 的 store.py（交叉引用）
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class ContextBridge:
    """上下文桥接增强版"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
        self.contexts_path = self.base_path / "contexts"
        
        # 桥接类型
        self.bridge_types = {
            "association": "关联",  # 共同标签
            "causation": "因果",    # 因果关系
            "contrast": "对比",     # 对比关系
            "evolution": "演化",    # 认知演化
            "trigger": "触发"       # 触发关系
        }
    
    def build(self, inner_thought: str, external_info: str) -> Dict[str, Any]:
        """构建上下文桥接"""
        bridge = {
            "id": f"bridge-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "inner_thought": inner_thought,
            "external_info": external_info,
            "type": self._detect_bridge_type(inner_thought, external_info),
            "strength": self._calculate_strength(inner_thought, external_info),
            "built_at": datetime.now().isoformat()
        }
        
        # 保存到 bridges 目录
        bridge_path = self.base_path / "bridges" / f"{bridge['id']}.json"
        bridge_path.parent.mkdir(parents=True, exist_ok=True)
        bridge_path.write_text(json.dumps(bridge, indent=2, ensure_ascii=False))
        
        return bridge
    
    def build_auto(self, contexts: List[Dict]) -> List[Dict]:
        """
        自动构建桥接（批量）
        
        借鉴 knowledge-workflow 的 store.py 交叉引用逻辑
        """
        bridges = []
        
        for i, ctx1 in enumerate(contexts):
            for ctx2 in contexts[i+1:]:
                if self._should_bridge(ctx1, ctx2):
                    bridge = {
                        "id": f"bridge-{ctx1['id']}-{ctx2['id']}",
                        "from": ctx1["id"],
                        "to": ctx2["id"],
                        "type": self._detect_bridge_type(ctx1.get("content", ""), ctx2.get("content", "")),
                        "strength": self._calculate_strength(ctx1.get("content", ""), ctx2.get("content", "")),
                        "reason": self._generate_reason(ctx1, ctx2)
                    }
                    bridges.append(bridge)
        
        return bridges
    
    def _should_bridge(self, ctx1: Dict, ctx2: Dict) -> bool:
        """
        判断是否应该桥接
        
        借鉴 knowledge-workflow 的 store.py 匹配策略
        """
        # 1. 检查共同标签
        tags1 = set(ctx1.get("tags", []))
        tags2 = set(ctx2.get("tags", []))
        tag_overlap = len(tags1 & tags2)
        
        if tag_overlap > 0:
            return True
        
        # 2. 检查共同关键词
        keywords1 = set(ctx1.get("keywords", []))
        keywords2 = set(ctx2.get("keywords", []))
        keyword_overlap = len(keywords1 & keywords2)
        
        if keyword_overlap > 1:
            return True
        
        # 3. 检查时间接近度
        # TODO: 实现时间接近度检查
        
        return False
    
    def _detect_bridge_type(self, content1: str, content2: str) -> str:
        """检测桥接类型"""
        # 简化版：基于关键词
        if any(kw in content1 or kw in content2 for kw in ["因为", "所以", "导致", "因此"]):
            return "causation"
        elif any(kw in content1 or kw in content2 for kw in ["但是", "然而", "对比", "相反"]):
            return "contrast"
        elif any(kw in content1 or kw in content2 for kw in ["演化", "发展", "变化", "更新"]):
            return "evolution"
        elif any(kw in content1 or kw in content2 for kw in ["触发", "想起", "联想"]):
            return "trigger"
        else:
            return "association"
    
    def _calculate_strength(self, content1: str, content2: str) -> float:
        """计算桥接强度（0-1）"""
        # 1. 标签重叠
        # 2. 关键词重叠
        # 3. 语义相似度（TODO: AI 计算）
        
        # 简化版
        common_words = len(set(content1) & set(content2))
        strength = min(1.0, common_words / 100)
        
        return strength
    
    def _generate_reason(self, ctx1: Dict, ctx2: Dict) -> str:
        """生成桥接理由"""
        tags1 = set(ctx1.get("tags", []))
        tags2 = set(ctx2.get("tags", []))
        common_tags = tags1 & tags2
        
        if common_tags:
            return f"共同标签：{', '.join(common_tags)}"
        
        keywords1 = set(ctx1.get("keywords", []))
        keywords2 = set(ctx2.get("keywords", []))
        common_keywords = keywords1 & keywords2
        
        if common_keywords:
            return f"共同关键词：{', '.join(common_keywords)}"
        
        return "语义相关"
