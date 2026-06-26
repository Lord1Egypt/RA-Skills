#!/usr/bin/env python3
"""
Claude Code Enhancement Skill - 记忆系统模块
参考 Claude Code 的 MEMORY.md 设计
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
from enum import Enum


class MemoryType(Enum):
    """记忆类型"""
    USER = "user"         # 用户偏好
    FEEDBACK = "feedback" # 用户反馈/纠正
    PROJECT = "project"   # 项目上下文
    REFERENCE = "reference"  # 参考资料


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    type: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class MemorySystem:
    """记忆系统 - 参考 Claude Code 的 MEMORY.md"""
    
    def __init__(self, memory_dir: Optional[str] = None):
        # 默认记忆目录
        if memory_dir is None:
            self.memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
        else:
            self.memory_dir = Path(memory_dir)
        
        # 确保目录存在
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 记忆文件
        self.memory_file = self.memory_dir / "MEMORY.md"
        
        # 分类记忆目录
        self.types_dir = {
            "user": self.memory_dir / "user",
            "feedback": self.memory_dir / "feedback",
            "project": self.memory_dir / "project",
            "reference": self.memory_dir / "reference",
        }
        
        # 初始化目录
        for dir_path in self.types_dir.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 内存中的记忆缓存
        self.entries: Dict[str, List[MemoryEntry]] = defaultdict(list)
        
        # 加载现有记忆
        self._load_memory()
    
    def _load_memory(self):
        """加载现有记忆"""
        if not self.memory_file.exists():
            self._init_memory_file()
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析现有记忆
            # 简化版：按类型分组
            current_type = None
            for line in content.split('\n'):
                if line.startswith('## '):
                    current_type = line[3:].strip().lower()
                elif current_type and line.strip():
                    if current_type not in self.entries:
                        self.entries[current_type] = []
                    self.entries[current_type].append(MemoryEntry(
                        id=str(len(self.entries[current_type])),
                        type=current_type,
                        content=line.strip()
                    ))
        except Exception as e:
            print(f"加载记忆失败: {e}")
    
    def _init_memory_file(self):
        """初始化 MEMORY.md 文件"""
        template = """# MEMORY.md - OpenClaw 记忆入口

> 本文件是 OpenClaw 的记忆入口，AI 助手会读取其中的内容来了解上下文。
> 请保持简洁，控制在 200 行以内。

---

## 用户偏好 (user)

- 

---

## 用户反馈 (feedback)

- 

---

## 项目上下文 (project)

- 

---

## 参考资料 (reference)

- 

---

*最后更新: {timestamp}*
"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            f.write(template.format(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
    
    def add(self, memory_type: str, content: str, tags: List[str] = None) -> str:
        """添加记忆"""
        entry = MemoryEntry(
            id=str(datetime.now().timestamp()),
            type=memory_type,
            content=content,
            tags=tags or []
        )
        
        # 添加到缓存
        self.entries[memory_type].append(entry)
        
        # 持久化到文件
        self._save_to_file(memory_type, content)
        
        return f"✅ 已添加记忆: [{memory_type}] {content[:50]}..."
    
    def _save_to_file(self, memory_type: str, content: str):
        """保存到分类文件"""
        type_file = self.types_dir[memory_type] / "default.md"
        
        # 追加内容
        with open(type_file, 'a', encoding='utf-8') as f:
            f.write(f"\n- {content}")
        
        # 更新 MEMORY.md
        self._update_memory_entry(memory_type, content)
    
    def _update_memory_entry(self, memory_type: str, content: str):
        """更新 MEMORY.md 中的条目"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 找到对应类型的位置
            type_header = f"## {self._get_type_name(memory_type)}"
            start_idx = -1
            end_idx = -1
            
            for i, line in enumerate(lines):
                if type_header in line:
                    start_idx = i + 1
                elif start_idx > 0 and line.startswith('## '):
                    end_idx = i
                    break
            
            if start_idx > 0:
                # 插入新条目
                if end_idx < 0:
                    end_idx = len(lines)
                
                # 找到 "-" 开头的行
                insert_idx = start_idx
                for i in range(start_idx, end_idx):
                    if lines[i].strip().startswith('-'):
                        insert_idx = i + 1
                
                lines.insert(insert_idx, f"- {content}\n")
                
                with open(self.memory_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
        except Exception as e:
            print(f"更新记忆失败: {e}")
    
    def _get_type_name(self, memory_type: str) -> str:
        """获取类型的中文名"""
        names = {
            "user": "用户偏好 (user)",
            "feedback": "用户反馈 (feedback)",
            "project": "项目上下文 (project)",
            "reference": "参考资料 (reference)",
        }
        return names.get(memory_type, memory_type)
    
    def search(self, query: str) -> List[MemoryEntry]:
        """搜索记忆"""
        results = []
        query_lower = query.lower()
        
        for entries in self.entries.values():
            for entry in entries:
                if query_lower in entry.content.lower():
                    results.append(entry)
        
        return results
    
    def get_summary(self) -> str:
        """获取记忆摘要"""
        lines = ["📚 **记忆摘要**\n"]
        
        for mem_type, entries in self.entries.items():
            if entries:
                lines.append(f"### {mem_type.upper()}")
                lines.append(f"共 {len(entries)} 条记忆\n")
        
        if not any(self.entries.values()):
            lines.append("暂无记忆")
        
        return "\n".join(lines)
    
    def clear(self, memory_type: Optional[str] = None) -> str:
        """清除记忆"""
        if memory_type:
            # 清除指定类型
            if memory_type in self.entries:
                self.entries[memory_type] = []
                type_file = self.types_dir[memory_type] / "default.md"
                if type_file.exists():
                    type_file.unlink()
            return f"✅ 已清除 {memory_type} 类型记忆"
        else:
            # 清除所有
            for entries in self.entries.values():
                entries.clear()
            
            # 删除所有分类文件
            for dir_path in self.types_dir.values():
                for f in dir_path.glob("*.md"):
                    f.unlink()
            
            # 重新初始化 MEMORY.md
            self._init_memory_file()
            
            return "✅ 已清除所有记忆"


# 需要导入 Enum
from enum import Enum

# 全局记忆系统实例
_memory_system: Optional[MemorySystem] = None


def get_memory_system() -> MemorySystem:
    """获取全局记忆系统实例"""
    global _memory_system
    if _memory_system is None:
        _memory_system = MemorySystem()
    return _memory_system


# CLI 接口
if __name__ == "__main__":
    ms = get_memory_system()
    
    import sys
    
    if len(sys.argv) < 2:
        print("用法: memory.py <命令> [参数]")
        print("命令: add <类型> <内容> | search <关键词> | summary | clear [类型]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) > 3:
        print(ms.add(sys.argv[2], " ".join(sys.argv[3:])))
    elif cmd == "search" and len(sys.argv) > 2:
        results = ms.search(" ".join(sys.argv[2:]))
        print(f"找到 {len(results)} 条结果:")
        for r in results:
            print(f"  [{r.type}] {r.content}")
    elif cmd == "summary":
        print(ms.get_summary())
    elif cmd == "clear":
        mem_type = sys.argv[2] if len(sys.argv) > 2 else None
        print(ms.clear(mem_type))
    else:
        print(f"未知命令: {cmd}")