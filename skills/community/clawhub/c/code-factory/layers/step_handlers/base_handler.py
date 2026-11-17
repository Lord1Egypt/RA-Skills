"""
步骤处理器基类 —— 统一接口：execute() + compensate()

所有步骤处理器继承此基类，确保接口一致性。
"""

from typing import Dict, Any, Optional, Callable
from abc import ABC, abstractmethod


class BaseStepHandler(ABC):
    """步骤处理器抽象基类"""

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        执行步骤逻辑。

        Returns:
            步骤输出 dict，必须符合该步骤的契约定义
        """
        ...

    def compensate(self) -> Optional[Callable[[], None]]:
        """
        返回补偿函数（用于 Saga 回滚）。

        默认返回 None（无副作用，无需补偿）。
        子类可覆盖此方法返回补偿函数。
        """
        return None
