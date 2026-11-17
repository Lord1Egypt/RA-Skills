"""
Saga 协调器（SagaCoordinator）—— 跨步骤补偿机制。

当管道中任一步骤失败时，按逆序执行所有已完成步骤的补偿函数，
确保不产生脏数据（如 Step3 写入磁盘但 Step4 失败时清理文件）。

设计原则：
- 补偿函数必须幂等：多次调用不会产生额外副作用
- 补偿失败不阻断其他补偿：每个补偿独立 try/except
- 补偿顺序严格逆序：最后完成的最先回滚
"""

import logging
from typing import List, Callable, Optional

logger = logging.getLogger(__name__)


class SagaCoordinator:
    """
    跨步骤 Saga 补偿协调器。

    用法:
        saga = SagaCoordinator()
        saga.register("Step3", lambda: shutil.rmtree(target_dir))
        saga.register("Step4", lambda: cleanup_temp_files())
        # 若 Step5 失败：
        compensated = saga.compensate_all()
        # → 逆序执行：先 cleanup_temp_files()，再 rmtree()
    """

    def __init__(self):
        self._compensations: List[tuple] = []  # [(step_name, compensate_fn), ...]

    def register(self, step_name: str, compensate_fn: Callable[[], None]) -> None:
        """
        注册步骤的补偿函数。

        Args:
            step_name: 步骤名称（用于日志和调试）
            compensate_fn: 补偿函数（应幂等，多次调用无害）
        """
        self._compensations.append((step_name, compensate_fn))

    def compensate_all(self) -> List[str]:
        """
        逆序执行所有已注册的补偿函数。

        Returns:
            成功执行补偿的步骤名列表
        """
        compensated: List[str] = []

        for step_name, fn in reversed(self._compensations):
            try:
                fn()
                compensated.append(step_name)
                logger.info("Saga 补偿: %s 已回滚", step_name)
            except Exception as e:
                # 补偿失败不阻断其他补偿
                logger.warning(
                    "Saga 补偿: %s 回滚失败 (%s)，继续执行后续补偿",
                    step_name, e,
                )

        self._compensations.clear()
        return compensated

    @property
    def registered_steps(self) -> List[str]:
        """已注册补偿的步骤名列表"""
        return [name for name, _ in self._compensations]
