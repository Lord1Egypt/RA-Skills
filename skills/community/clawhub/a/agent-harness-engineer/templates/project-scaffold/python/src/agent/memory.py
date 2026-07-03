#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: agent.memory
# 说明: 记忆系统，实现短期和长期记忆
# 修改建议: 如需扩展，继承MemoryManager类
# ============================================
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, storage_path: str = "memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.short_term: List[Dict[str, Any]] = []
    
    def add_short_term(self, content: str, metadata: Dict[str, Any] = None):
        """添加短期记忆"""
        memory = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.short_term.append(memory)
        logger.debug(f"Added short-term memory: {content[:50]}...")
    
    def add_long_term(self, category: str, content: str):
        """添加长期记忆"""
        memory_file = self.storage_path / f"{category}.md"
        
        with open(memory_file, "a") as f:
            f.write(f"\n## {datetime.now().isoformat()}\n\n")
            f.write(f"{content}\n\n")
        
        logger.info(f"Added long-term memory to {category}")
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[str]:
        """获取相关记忆"""
        # 简化实现：返回最近的记忆
        memories = []
        for memory in self.short_term[-limit:]:
            memories.append(memory["content"])
        return memories
    
    def consolidate(self):
        """整合记忆（自动做梦机制）"""
        logger.info("Consolidating memories...")
        
        # 将短期记忆转为长期记忆
        if len(self.short_term) > 10:
            consolidated = "\n".join(m["content"] for m in self.short_term)
            self.add_long_term("consolidated", consolidated)
            self.short_term = []
            logger.info("Consolidated short-term memories")
    
    def load_memory_index(self) -> Dict[str, Any]:
        """加载记忆索引"""
        index_file = self.storage_path / "MEMORY.md"
        if not index_file.exists():
            return {}
        
        # 解析Markdown索引
        with open(index_file, "r") as f:
            content = f.read()
        
        # 简化实现：返回空字典
        return {}
