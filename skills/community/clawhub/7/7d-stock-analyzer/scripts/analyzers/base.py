"""
基础分析器 - 所有分析器的基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseAnalyzer(ABC):
    """分析器基类"""

    def __init__(self, adapters: Dict[str, Any], verbose: bool = False):
        """
        初始化分析器

        Args:
            adapters: 数据源适配器字典
            verbose: 是否显示详细输出
        """
        self.adapters = adapters
        self.verbose = verbose
        self.data = {}

    @property
    @abstractmethod
    def name(self) -> str:
        """分析器名称"""
        pass

    @property
    @abstractmethod
    def dimensions(self) -> List[str]:
        """分析维度列表"""
        pass

    @abstractmethod
    def analyze(self, symbol: str) -> Dict[str, Any]:
        """
        执行分析

        Args:
            symbol: 股票代码

        Returns:
            分析结果字典
        """
        pass

    def get_data(self, source: str, method: str, **kwargs) -> Any:
        """
        从指定数据源获取数据

        Args:
            source: 数据源名称
            method: 方法名
            **kwargs: 方法参数

        Returns:
            数据源返回的数据
        """
        if source not in self.adapters:
            raise ValueError(f"未知数据源: {source}")

        adapter = self.adapters[source]
        if not hasattr(adapter, method):
            raise AttributeError(f"适配器 {source} 没有方法 {method}")

        return getattr(adapter, method)(**kwargs)

    def combine_data(self, source_priority: List[str] = None) -> Dict[str, Any]:
        """
        合并多个数据源的数据

        Args:
            source_priority: 数据源优先级列表

        Returns:
            合并后的数据
        """
        if source_priority is None:
            source_priority = list(self.adapters.keys())

        combined = {}
        for source in source_priority:
            if source in self.data:
                combined.update(self.data[source])

        return combined

    def log(self, message: str):
        """日志输出"""
        if self.verbose:
            print(f"  [{self.name}] {message}")
