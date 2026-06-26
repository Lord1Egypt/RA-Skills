"""
平台适配器基础接口

所有平台适配器必须实现这些方法。
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class BaseAdapter(ABC):
    """
    平台适配器基类
    
    为不同 Agent 平台提供统一的接口。
    """
    
    def __init__(self, workspace: Path, memory_dir: Path = None):
        self.workspace = workspace
        self.memory_dir = memory_dir or (workspace / "memory")
    
    @abstractmethod
    def get_memory_files(self) -> List[Path]:
        """
        获取记忆文件列表
        
        返回:
            文件路径列表，按 mtime 降序排序
        """
        pass
    
    @abstractmethod
    def get_memory_md_lines(self) -> int:
        """
        获取 MEMORY.md 行数
        
        返回:
            行数
        """
        pass
    
    @abstractmethod
    def update_memory_md(self, content: str, entries: List[Dict]) -> bool:
        """
        更新 MEMORY.md
        
        参数:
            content: 新内容
            entries: 条目列表
            
        返回:
            是否成功
        """
        pass
    
    @abstractmethod
    def count_sessions_since(self, timestamp: float) -> int:
        """
        计算指定时间戳之后的会话数量
        
        参数:
            timestamp: Unix 时间戳
            
        返回:
            会话数量
        """
        pass
    
    @abstractmethod
    def extract_session_signals(self) -> List[Dict]:
        """
        从会话记录中提取信号
        
        返回:
            信号条目列表
        """
        pass
    
    def read_file(self, path: Path) -> str:
        """
        读取文件内容（通用实现）
        
        参数:
            path: 文件路径
            
        返回:
            文件内容
        """
        return path.read_text(encoding="utf-8", errors="ignore")
    
    def write_file(self, path: Path, content: str) -> None:
        """
        写入文件内容（通用实现）
        
        参数:
            path: 文件路径
            content: 文件内容
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
