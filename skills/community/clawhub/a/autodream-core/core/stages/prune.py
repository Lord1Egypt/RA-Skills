"""
阶段 4: Prune and Index - 修剪索引

更新 MEMORY.md，保持简洁。
"""

from typing import Dict, List, Any
from datetime import datetime, timezone


class PruneStage:
    """
    Prune and Index 阶段
    
    职责:
    1. 更新 MEMORY.md 索引
    2. 保持行数 ≤ 配置限制
    3. 添加/删除主题条目
    """
    
    def __init__(self, adapter: Any, config: Dict):
        self.adapter = adapter
        self.config = config
    
    def execute(self, consolidate_result: Dict) -> Dict:
        """
        执行 Prune 阶段
        
        参数:
            consolidate_result: Consolidation 阶段的结果
            
        返回:
            {
                **consolidate_result,
                "memory_md_lines_before": int,
                "memory_md_lines_after": int,
                "topics_added": [...],
                "topics_removed": [...],
            }
        """
        # 获取当前 MEMORY.md 行数
        lines_before = self.adapter.get_memory_md_lines()
        
        # 获取最终条目
        final_entries = consolidate_result.get("final_entries", [])
        
        # 生成索引内容
        index_content = self._generate_index(final_entries)
        
        # 更新 MEMORY.md
        # 注意：具体实现取决于平台适配器
        # 这里调用适配器的更新方法
        try:
            self.adapter.update_memory_md(index_content, final_entries)
        except Exception as e:
            print(f"   ⚠️ 更新 MEMORY.md 失败：{e}")
        
        # 获取更新后行数
        lines_after = self.adapter.get_memory_md_lines()
        
        return {
            **consolidate_result,
            "memory_md_lines_before": lines_before,
            "memory_md_lines_after": lines_after,
            "topics_added": [],  # 待扩展
            "topics_removed": [],  # 待扩展
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    def _generate_index(self, entries: List[Dict]) -> str:
        """
        生成索引内容
        
        参数:
            entries: 条目列表
            
        返回:
            Markdown 格式的索引内容
        """
        lines = ["# MEMORY.md - 长期记忆索引", ""]
        
        # 按文件分组
        by_file = {}
        for entry in entries:
            filename = entry.get("metadata", {}).get("filename", "unknown")
            if filename not in by_file:
                by_file[filename] = []
            by_file[filename].append(entry)
        
        # 生成每个文件的条目
        for filename, file_entries in sorted(by_file.items()):
            lines.append(f"## {filename}")
            lines.append("")
            for entry in file_entries:
                text = entry.get("text", "")
                lines.append(f"- {text}")
            lines.append("")
        
        return "\n".join(lines)
