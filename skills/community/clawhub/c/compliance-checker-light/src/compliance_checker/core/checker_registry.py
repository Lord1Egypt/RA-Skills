"""
检查器注册表模块

管理所有检查器的注册和发现。

注意：此类只定义数据结构和方法，不实例化具体检查器。
检查器的实例化和注册应在 Application 层的 bootstrap.py 中完成，
以避免循环依赖问题。
"""

import threading
from typing import Dict, List, Optional, Set

from .checker_base import BaseChecker, UnavailableChecker


class CheckerRegistry:
    """
    检查器注册表 - 单例模式（线程安全）

    管理所有检查器的注册、发现和获取。
    支持标记未实现的功能，实现优雅降级。

    使用双重检查锁定确保线程安全。
    """

    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        """单例模式 - 双重检查锁定"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化注册表"""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._checkers: Dict[str, BaseChecker] = {}
                    self._unavailable: Set[str] = set()
                    self._initialized = True

    def register(self, checker: BaseChecker) -> None:
        """
        注册检查器

        Args:
            checker: 检查器实例
        """
        self._checkers[checker.name] = checker

    def register_unavailable(self, check_type: str) -> None:
        """
        标记某检查类型为未实现（开发占位）

        Args:
            check_type: 检查类型名称
        """
        self._unavailable.add(check_type)

    def get(self, check_type: str) -> BaseChecker:
        """
        获取检查器

        获取逻辑：
        - 已注册且可用 → 返回检查器
        - 已注册但不可用 → 返回 UnavailableChecker
        - 标记为未实现 → 返回 UnavailableChecker
        - 未知类型 → 返回 UnavailableChecker

        Args:
            check_type: 检查类型名称

        Returns:
            BaseChecker: 检查器实例或 UnavailableChecker
        """
        # 检查是否已注册
        if check_type in self._checkers:
            checker = self._checkers[check_type]
            if checker.is_available():
                return checker
            else:
                return UnavailableChecker(check_type)

        # 检查是否标记为不可用
        if check_type in self._unavailable:
            return UnavailableChecker(check_type)

        # 未知类型
        return UnavailableChecker(check_type)

    def list_available(self) -> List[str]:
        """
        列出所有可用检查器

        Returns:
            可用检查器名称列表
        """
        return [name for name, checker in self._checkers.items() if checker.is_available()]

    def list_all(self) -> Dict[str, str]:
        """
        列出所有检查器状态

        Returns:
            检查器名称到状态的映射
            状态值: "available", "unavailable", "not_implemented"
        """
        result: Dict[str, str] = {}

        # 已注册的检查器
        for name, checker in self._checkers.items():
            if checker.is_available():
                result[name] = "available"
            else:
                result[name] = "unavailable"

        # 标记为未实现的
        for check_type in self._unavailable:
            if check_type not in result:
                result[check_type] = "not_implemented"

        return result

    def unregister(self, check_type: str) -> None:
        """
        注销检查器

        Args:
            check_type: 检查类型名称
        """
        self._checkers.pop(check_type, None)
        self._unavailable.discard(check_type)

    def clear(self) -> None:
        """清空所有注册"""
        self._checkers.clear()
        self._unavailable.clear()
