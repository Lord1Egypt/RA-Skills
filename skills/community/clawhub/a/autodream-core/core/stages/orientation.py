"""
阶段 1: Orientation - 建立记忆状态地图

读取记忆目录，收集文件元数据和条目。
"""

from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timezone

from ..utils.frontmatter import extract_frontmatter_and_body
from ..utils.text import extract_entries_from_text


class OrientationStage:
    """
    Orientation 阶段
    
    职责:
    1. 扫描记忆目录
    2. 收集文件元数据（mtime、frontmatter）
    3. 提取所有条目
    4. 建立记忆状态地图
    """
    
    def __init__(self, adapter: Any, config: Dict):
        self.adapter = adapter
        self.config = config
    
    def execute(self) -> Dict:
        """
        执行 Orientation 阶段
        
        返回:
            {
                "memory_files": [...],
                "memory_headers": [...],
                "total_entries": int,
                "entries": [...],
                "memory_md_lines": int,
                "topics": [],
            }
        """
        max_files = self.config.get("max_memory_files", 200)
        
        # 获取记忆文件列表
        memory_files = self.adapter.get_memory_files()
        
        # 限制文件数量
        if len(memory_files) > max_files:
            memory_files = memory_files[:max_files]
        
        # 收集文件头信息
        memory_headers = []
        all_entries = []
        
        for file_path in memory_files:
            path = Path(file_path)
            
            # 读取文件内容
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                print(f"   ⚠️ 无法读取 {path}: {e}")
                continue
            
            # 解析 frontmatter
            frontmatter, body = extract_frontmatter_and_body(content)
            
            # 提取条目
            entries = extract_entries_from_text(body)
            
            # 为每个条目添加文件元数据
            for entry in entries:
                entry["metadata"]["filename"] = path.name
                entry["metadata"]["filepath"] = str(path)
                entry["metadata"]["frontmatter"] = frontmatter
            
            all_entries.extend(entries)
            
            # 收集文件头
            memory_headers.append({
                "filename": path.name,
                "filepath": str(path),
                "mtime_ms": path.stat().st_mtime * 1000,
                "type": frontmatter.get("type", "unknown"),
                "description": frontmatter.get("description", ""),
            })
        
        # 获取 MEMORY.md 行数
        memory_md_lines = self.adapter.get_memory_md_lines()
        
        result = {
            "memory_files": [str(f) for f in memory_files],
            "memory_headers": memory_headers,
            "total_entries": len(all_entries),
            "entries": all_entries,
            "memory_md_lines": memory_md_lines,
            "topics": [],  # 待扩展
        }
        
        print(f"   找到 {len(memory_files)} 个记忆文件，共 {len(all_entries)} 个条目")
        
        return result
