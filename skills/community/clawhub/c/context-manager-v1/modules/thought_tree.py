#!/usr/bin/env python3
"""
Thought Tree Builder - 思维树构建师
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class ThoughtTreeBuilder:
    """思维树构建师"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
    
    def build(self, topic: str, time_range: str = "3months") -> Dict[str, Any]:
        """构建思维树"""
        # 1. 收集相关上下文
        contexts = self._collect_related(topic, time_range)
        
        # 2. 分类整理
        tree = {
            "topic": topic,
            "time_range": time_range,
            "core_cognitions": self._extract_core_cognitions(contexts),
            "external_info": [c for c in contexts if c.get("type") == "external"],
            "inner_cognitions": [c for c in contexts if c.get("type") == "inner_cognition"],
            "bridges": self._build_bridges(contexts),
            "updates": self._extract_updates(contexts),
            "built_at": datetime.now().isoformat()
        }
        
        # 3. 保存到 trees 目录
        tree_id = f"tree-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        tree_path = self.base_path / "trees" / f"{tree_id}.json"
        tree_path.parent.mkdir(parents=True, exist_ok=True)
        tree_path.write_text(json.dumps(tree, indent=2, ensure_ascii=False))
        
        tree["id"] = tree_id
        tree["path"] = str(tree_path)
        
        return tree
    
    def _collect_related(self, topic: str, time_range: str) -> List[Dict]:
        """收集相关上下文"""
        contexts = []
        contexts_dir = self.base_path / "contexts"
        
        for context_file in contexts_dir.glob("*.json"):
            context = json.loads(context_file.read_text())
            # 简单匹配：检查标题或内容是否包含主题
            if topic in context.get("title", "") or topic in context.get("content", ""):
                contexts.append(context)
        
        return contexts[:20]  # 限制数量
    
    def _extract_core_cognitions(self, contexts: List[Dict]) -> List[str]:
        """提取核心认知"""
        # 简化版：提取高亮内容
        return [c.get("content", "")[:100] for c in contexts if c.get("type") == "inner_cognition"][:5]
    
    def _build_bridges(self, contexts: List[Dict]) -> List[Dict]:
        """构建上下文桥接"""
        bridges = []
        
        for i, ctx1 in enumerate(contexts):
            for ctx2 in contexts[i+1:]:
                if self._should_bridge(ctx1, ctx2):
                    bridges.append({
                        "from": ctx1.get("id"),
                        "to": ctx2.get("id"),
                        "type": self._detect_bridge_type(ctx1, ctx2)
                    })
        
        return bridges[:10]  # 限制数量
    
    def _should_bridge(self, ctx1: Dict, ctx2: Dict) -> bool:
        """判断是否应该桥接"""
        # 简化版：检查是否有共同标签
        tags1 = set(ctx1.get("tags", []))
        tags2 = set(ctx2.get("tags", []))
        return len(tags1 & tags2) > 0
    
    def _detect_bridge_type(self, ctx1: Dict, ctx2: Dict) -> str:
        """检测桥接类型"""
        # 简化版
        return "association"
    
    def _extract_updates(self, contexts: List[Dict]) -> List[Dict]:
        """提取认知更新"""
        # 简化版
        return []
