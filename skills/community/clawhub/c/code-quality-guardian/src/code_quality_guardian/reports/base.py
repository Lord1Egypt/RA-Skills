"""
Base reporter
报告生成器基类
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..models import AnalysisResult


class Reporter(ABC):
    """报告生成器基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__.replace("Reporter", "").lower()
    
    @abstractmethod
    def render(self, result: AnalysisResult, output_path: Optional[str] = None) -> str:
        """
        渲染报告
        
        Args:
            result: 分析结果
            output_path: 输出路径 (可选)
            
        Returns:
            报告内容字符串
        """
        pass
