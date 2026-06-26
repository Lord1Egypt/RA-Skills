"""
Base tool runner
工具运行器基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..models import Issue


class ToolRunner(ABC):
    """工具运行器基类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化工具运行器
        
        Args:
            config: 工具特定配置
        """
        self.config = config or {}
        self.name = self.__class__.__name__.replace("Runner", "").lower()
    
    @abstractmethod
    def run(self, path: str, files: Optional[List[Path]] = None) -> List[Issue]:
        """
        运行工具
        
        Args:
            path: 要分析的路径
            files: 文件列表 (可选)
            
        Returns:
            发现的问题列表
        """
        pass
    
    def is_available(self) -> bool:
        """
        检查工具是否可用
        
        Returns:
            是否可用
        """
        import shutil
        return shutil.which(self.name) is not None
