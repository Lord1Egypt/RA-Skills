"""
OpenClaw 平台适配器

实现 OpenClaw 特定的记忆管理逻辑。
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone

from .base import BaseAdapter


class OpenClawAdapter(BaseAdapter):
    """
    OpenClaw 平台适配器
    
    适配 OpenClaw 的记忆目录结构和会话格式。
    
    用法:
        adapter = OpenClawAdapter(workspace=Path("/path/to/workspace"))
        engine = AutoDreamEngine(adapter)
        result = engine.run()
    """
    
    def __init__(self, workspace: Path, memory_dir: Path = None):
        super().__init__(workspace, memory_dir)
        self.sessions_dir = workspace / "sessions"
        self.memory_md = workspace / "MEMORY.md"
    
    def get_memory_files(self) -> List[Path]:
        """
        获取记忆文件列表（MEMORY.md + memory/*.md）
        
        返回:
            按 mtime 降序排序的文件列表
        """
        files = []
        
        # 添加 MEMORY.md
        if self.memory_md.exists():
            files.append(self.memory_md)
        
        # 添加 memory/*.md
        if self.memory_dir.exists():
            for f in self.memory_dir.glob("*.md"):
                files.append(f)
        
        # 按 mtime 降序排序
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        return files
    
    def get_memory_md_lines(self) -> int:
        """获取 MEMORY.md 行数"""
        if not self.memory_md.exists():
            return 0
        
        content = self.memory_md.read_text(encoding="utf-8", errors="ignore")
        return len(content.splitlines())
    
    def update_memory_md(self, content: str, entries: List[Dict]) -> bool:
        """
        更新 MEMORY.md
        
        策略：
        1. 保留 frontmatter（如果有）
        2. 替换条目区域
        3. 保持 ≤ 200 行
        """
        if not self.memory_md.exists():
            # 创建新文件
            self.memory_md.write_text(content, encoding="utf-8")
            return True
        
        # 读取现有内容
        existing = self.memory_md.read_text(encoding="utf-8", errors="ignore")
        
        # 尝试保留 frontmatter
        if existing.startswith("---"):
            try:
                end = existing.index("---", 3)
                frontmatter = existing[:end + 3]
                # 新内容 = frontmatter + 新条目
                new_content = frontmatter + "\n" + content
            except ValueError:
                new_content = content
        else:
            new_content = content
        
        # 写入
        self.memory_md.write_text(new_content, encoding="utf-8")
        
        return True
    
    def count_sessions_since(self, timestamp: float) -> int:
        """
        计算指定时间戳之后的会话数量
        
        通过扫描 sessions 目录中的 JSON 文件。
        """
        if not self.sessions_dir.exists():
            return 0
        
        count = 0
        for f in self.sessions_dir.glob("*.json"):
            try:
                mtime = f.stat().st_mtime
                if mtime > timestamp:
                    count += 1
            except Exception:
                continue
        
        return count
    
    def extract_session_signals(self) -> List[Dict]:
        """
        从会话记录中提取信号
        
        提取策略：
        - 用户明确说"记住这个"
        - 决策性陈述（"我们决定..."）
        - 重要结论
        """
        signals = []
        
        if not self.sessions_dir.exists():
            return signals
        
        # 关键词匹配
        keywords = [
            "记住", "remember", "决定", "decided", "结论", "conclusion",
            "重要", "important", "注意", "note",
        ]
        
        for f in self.sessions_dir.glob("*.json"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                data = json.loads(content)
                
                # 遍历消息
                messages = data.get("messages", [])
                for msg in messages:
                    text = msg.get("content", "")
                    
                    # 检查是否包含关键词
                    if any(kw in text.lower() for kw in keywords):
                        signals.append({
                            "text": text.strip(),
                            "source": f.name,
                            "timestamp": msg.get("timestamp", ""),
                            "metadata": {
                                "type": "session_signal",
                                "confidence": "medium",
                            },
                        })
                        
            except Exception:
                continue
        
        return signals
