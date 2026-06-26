#!/usr/bin/env python3
"""
Cognitive Map Generator - 认知地图生成器

借鉴 knowledge-workflow 的 belief_updater.py + rule_miner.py
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class CognitiveMapGenerator:
    """认知地图生成器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
        self.contexts_path = self.base_path / "contexts"
    
    def generate(self, period: str = "weekly") -> Dict[str, Any]:
        """
        生成认知地图
        
        借鉴 knowledge-workflow 的 belief_updater.py 信念更新逻辑
        """
        # 1. 收集指定周期的上下文
        contexts = self._collect_by_period(period)
        
        # 2. 分类整理
        categorized = self._categorize(contexts)
        
        # 3. 提取核心认知
        core_cognitions = self._extract_core_cognitions(contexts)
        
        # 4. 识别认知演化
        evolutions = self._identify_evolutions(contexts)
        
        # 5. 生成认知地图
        cognitive_map = {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "total_contexts": len(contexts),
            "categories": categorized,
            "core_cognitions": core_cognitions,
            "evolutions": evolutions,
            "statistics": self._generate_statistics(contexts)
        }
        
        # 6. 保存
        map_path = self.base_path / "maps" / f"map-{period}-{datetime.now().strftime('%Y%m%d')}.json"
        map_path.parent.mkdir(parents=True, exist_ok=True)
        map_path.write_text(json.dumps(cognitive_map, indent=2, ensure_ascii=False))
        
        cognitive_map["id"] = f"map-{period}-{datetime.now().strftime('%Y%m%d')}"
        cognitive_map["path"] = str(map_path)
        
        return cognitive_map
    
    def _collect_by_period(self, period: str) -> List[Dict]:
        """收集指定周期的上下文"""
        contexts = []
        
        # 简化版：读取所有上下文
        for context_file in self.contexts_path.glob("*.json"):
            context = json.loads(context_file.read_text())
            contexts.append(context)
        
        return contexts[:50]  # 限制数量
    
    def _categorize(self, contexts: List[Dict]) -> Dict[str, List]:
        """
        分类整理
        
        借鉴 knowledge-workflow 的 rule_miner.py 分组逻辑
        """
        categories = {
            "成长痛点": [],
            "关系锚点": [],
            "灵感触发": [],
            "认知冲突": [],
            "决策背景": [],
            "其他": []
        }
        
        for ctx in contexts:
            tags = ctx.get("tags", [])
            categorized = False
            
            for tag in tags:
                if tag in categories:
                    categories[tag].append(ctx)
                    categorized = True
                    break
            
            if not categorized:
                categories["其他"].append(ctx)
        
        return categories
    
    def _extract_core_cognitions(self, contexts: List[Dict]) -> List[Dict]:
        """
        提取核心认知
        
        借鉴 knowledge-workflow 的 belief_updater.py 信念提取逻辑
        """
        core_cognitions = []
        
        # 简化版：提取高亮内容
        for ctx in contexts:
            if ctx.get("type") == "inner_cognition":
                core_cognitions.append({
                    "id": ctx["id"],
                    "content": ctx.get("content", "")[:100],
                    "tags": ctx.get("tags", []),
                    "date": ctx.get("created_at", "")[:10]
                })
        
        return core_cognitions[:10]  # 限制数量
    
    def _identify_evolutions(self, contexts: List[Dict]) -> List[Dict]:
        """
        识别认知演化
        
        借鉴 knowledge-workflow 的 belief_updater.py 信念更新逻辑
        """
        evolutions = []
        
        # 简化版：查找相同主题的认知变化
        # TODO: 实现 AI 分析
        
        return evolutions
    
    def _generate_statistics(self, contexts: List[Dict]) -> Dict[str, Any]:
        """生成统计信息"""
        stats = {
            "total": len(contexts),
            "by_type": {},
            "by_tag": {},
            "avg_per_day": len(contexts) / 7  # 假设 weekly
        }
        
        # 按类型统计
        for ctx in contexts:
            ctx_type = ctx.get("type", "unknown")
            stats["by_type"][ctx_type] = stats["by_type"].get(ctx_type, 0) + 1
        
        # 按标签统计
        for ctx in contexts:
            for tag in ctx.get("tags", []):
                stats["by_tag"][tag] = stats["by_tag"].get(tag, 0) + 1
        
        return stats
