"""
阶段 3: Consolidation - 合并整理

合并重复、删除过时、检测矛盾。
"""

from typing import Dict, List, Any
from datetime import datetime, timezone

from ..utils.text import canonical, stable_id, detect_contradiction
from ..utils.dates import is_stale, parse_relative_dates


class ConsolidateStage:
    """
    Consolidation 阶段
    
    职责:
    1. 去重（基于 stable_id）
    2. 检测矛盾
    3. 删除过时条目
    4. 解析相对日期
    """
    
    def __init__(self, adapter: Any, config: Dict):
        self.adapter = adapter
        self.config = config
    
    def execute(self, gather_result: Dict) -> Dict:
        """
        执行 Consolidation 阶段
        
        参数:
            gather_result: Gather 阶段的结果
            
        返回:
            {
                **gather_result,
                "final_entries": [...],
                "original_count": int,
                "final_count": int,
                "pruned_count": int,
                "merged_count": int,
                "updated_count": int,
            }
        """
        entries = gather_result.get("entries", [])
        original_count = len(entries)
        
        # 1. 解析相对日期
        if self.config.get("enable_relative_date_parsing", True):
            entries = self._parse_dates(entries)
        
        # 2. 去重
        entries, merged_count = self._deduplicate(entries)
        
        # 3. 删除过时
        if self.config.get("enable_stale_detection", True):
            entries, pruned_count = self._prune_stale(entries)
        else:
            pruned_count = 0
        
        # 4. 检测矛盾（可选，仅标记不删除）
        if self.config.get("enable_contradiction_detection", True):
            entries = self._detect_contradictions(entries)
        
        return {
            **gather_result,
            "final_entries": entries,
            "original_count": original_count,
            "final_count": len(entries),
            "pruned_count": pruned_count,
            "merged_count": merged_count,
            "updated_count": 0,  # 待扩展
        }
    
    def _parse_dates(self, entries: List[Dict]) -> List[Dict]:
        """解析相对日期"""
        now = datetime.now(timezone.utc)
        for entry in entries:
            text = entry.get("text", "")
            entry["text"] = parse_relative_dates(text, now)
        return entries
    
    def _deduplicate(self, entries: List[Dict]) -> tuple:
        """
        去重
        
        返回:
            (去重后的列表，合并数量)
        """
        seen_ids = set()
        unique_entries = []
        merged_count = 0
        
        for entry in entries:
            entry_id = stable_id(entry.get("text", ""))
            if entry_id in seen_ids:
                merged_count += 1
            else:
                seen_ids.add(entry_id)
                unique_entries.append(entry)
        
        return unique_entries, merged_count
    
    def _prune_stale(self, entries: List[Dict]) -> tuple:
        """
        删除过时条目
        
        返回:
            (修剪后的列表，删除数量)
        """
        workspace = self.adapter.workspace
        pruned_count = 0
        fresh_entries = []
        
        for entry in entries:
            if is_stale(entry, workspace):
                pruned_count += 1
            else:
                fresh_entries.append(entry)
        
        return fresh_entries, pruned_count
    
    def _detect_contradictions(self, entries: List[Dict]) -> List[Dict]:
        """
        检测矛盾条目
        
        仅标记，不删除。
        """
        for i, entry1 in enumerate(entries):
            for j, entry2 in enumerate(entries[i+1:], start=i+1):
                if detect_contradiction(entry1, entry2):
                    # 标记矛盾
                    entry1["metadata"]["contradiction_with"] = stable_id(entry2.get("text", ""))
                    entry2["metadata"]["contradiction_with"] = stable_id(entry1.get("text", ""))
        
        return entries
