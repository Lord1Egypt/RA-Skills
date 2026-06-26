"""
错误重试处理器
支持多种重试策略和错误分类
"""

import time
from enum import Enum
from typing import Callable, Optional, Any
from dataclasses import dataclass


class RetryStrategy(Enum):
    """重试策略枚举"""

    EXPONENTIAL_BACKOFF = "exponential_backoff"  # 指数退避
    FIXED_DELAY = "fixed_delay"  # 固定延迟
    IMMEDIATE = "immediate"  # 立即重试


@dataclass
class RetryResult:
    """重试结果"""

    success: bool
    result: Any = None
    error: Optional[Exception] = None
    attempts: int = 0
    total_wait_time: float = 0.0


class RetryHandler:
    """错误重试处理器"""

    # 可重试的错误类型（临时性错误）
    RETRYABLE_ERRORS = (
        TimeoutError,
        ConnectionError,
        IOError,
        OSError,
    )

    def __init__(
        self,
        max_retries: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        fixed_delay: float = 5.0,
    ):
        """
        初始化重试处理器

        Args:
            max_retries: 最大重试次数（不包括首次尝试）
            strategy: 重试策略
            fixed_delay: 固定延迟时间（秒，仅用于 FIXED_DELAY 策略）
        """
        self.max_retries = max_retries
        self.strategy = strategy
        self.fixed_delay = fixed_delay

    def execute_with_retry(
        self, func: Callable, *args, retry_on_error: Optional[tuple] = None, **kwargs
    ) -> RetryResult:
        """
        带重试机制执行函数

        Args:
            func: 要执行的函数
            *args: 函数位置参数
            retry_on_error: 自定义可重试的错误类型元组
            **kwargs: 函数关键字参数

        Returns:
            RetryResult: 包含执行结果、错误信息、尝试次数等

        策略：
        - EXPONENTIAL_BACKOFF: 0s → 5s → 15s
        - FIXED_DELAY: 每次等待固定时间
        - IMMEDIATE: 立即重试
        """
        last_error = None
        total_wait_time = 0.0
        attempts = 0

        # 总尝试次数 = 首次 + 重试次数
        total_attempts = 1 + self.max_retries

        for attempt in range(total_attempts):
            attempts += 1

            try:
                # 执行函数
                result = func(*args, **kwargs)
                return RetryResult(
                    success=True, result=result, attempts=attempts, total_wait_time=total_wait_time
                )

            except Exception as e:
                last_error = e

                # 检查是否应该重试
                if not self._should_retry(e, attempt, retry_on_error):
                    return RetryResult(
                        success=False, error=e, attempts=attempts, total_wait_time=total_wait_time
                    )

                # 计算等待时间
                wait_time = self._calculate_wait_time(attempt - 1)
                total_wait_time += wait_time

                # 记录错误日志
                self._log_error(e, attempt, wait_time)

                # 等待后重试
                if wait_time > 0:
                    time.sleep(wait_time)

        # 所有尝试都失败
        return RetryResult(
            success=False, error=last_error, attempts=attempts, total_wait_time=total_wait_time
        )

    def _should_retry(
        self, error: Exception, attempt: int, retry_on_error: Optional[tuple]
    ) -> bool:
        """
        判断是否应该重试

        Args:
            error: 捕获的异常
            attempt: 当前尝试次数（从1开始）
            retry_on_error: 自定义可重试的错误类型

        Returns:
            bool: 是否应该重试
        """
        # 检查是否还有重试机会
        if attempt >= (1 + self.max_retries):
            return False

        # 如果指定了自定义错误类型，使用自定义判断
        if retry_on_error is not None:
            return isinstance(error, retry_on_error)

        # 使用默认的可重试错误类型
        return isinstance(error, self.RETRYABLE_ERRORS)

    def _calculate_wait_time(self, attempt: int) -> float:
        """
        计算等待时间

        Args:
            attempt: 失败尝试次数（从0开始）

        Returns:
            float: 等待时间（秒）
        """
        if self.strategy == RetryStrategy.IMMEDIATE:
            return 0.0

        elif self.strategy == RetryStrategy.FIXED_DELAY:
            return self.fixed_delay

        elif self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            # 0s → 5s → 15s → 30s
            # 尝试1（attempt=0）: 0秒
            # 尝试2（attempt=1）: 5秒
            # 尝试3（attempt=2）: 15秒
            # 尝试4（attempt=3）: 30秒
            if attempt == 0:
                return 0.0
            elif attempt == 1:
                return 5.0
            elif attempt == 2:
                return 15.0
            else:
                return 30.0

        return 0.0

    def _log_error(self, error: Exception, attempt: int, wait_time: float) -> None:
        """
        记录错误日志

        Args:
            error: 异常对象
            attempt: 当前尝试次数
            wait_time: 等待时间
        """
        error_type = type(error).__name__
        error_msg = str(error)[:100]  # 限制长度

        if wait_time > 0:
            print(
                f"⚠️  尝试 {attempt} 失败 ({error_type}): {error_msg}\n"
                f"   等待 {wait_time:.1f} 秒后重试..."
            )
        else:
            print(f"⚠️  尝试 {attempt} 失败 ({error_type}): {error_msg}，立即重试...")

    def set_strategy(self, strategy: RetryStrategy) -> None:
        """
        设置重试策略

        Args:
            strategy: 新的重试策略
        """
        self.strategy = strategy

    def set_max_retries(self, max_retries: int) -> None:
        """
        设置最大重试次数

        Args:
            max_retries: 最大重试次数
        """
        if max_retries < 0:
            raise ValueError("max_retries 必须大于等于 0")
        self.max_retries = max_retries


# 使用示例
if __name__ == "__main__":
    print("=== 重试处理器测试 ===\n")

    # 示例 1：测试指数退避策略
    print("示例 1：指数退避策略")
    print("-" * 40)

    class SimulatedError(Exception):
        """模拟错误"""


    def failing_function(attempt: int) -> str:
        """模拟会失败的函数"""
        print(f"  函数执行中...（第 {attempt} 次调用）")
        if attempt < 3:
            raise SimulatedError("模拟临时性错误")
        return "成功！"

    handler = RetryHandler(max_retries=3, strategy=RetryStrategy.EXPONENTIAL_BACKOFF)

    attempt_count = [0]

    def wrapper():
        attempt_count[0] += 1
        return failing_function(attempt_count[0])

    result = handler.execute_with_retry(wrapper)

    print(f"\n结果: {'成功' if result.success else '失败'}")
    print(f"尝试次数: {result.attempts}")
    print(f"总等待时间: {result.total_wait_time} 秒")
    if result.success:
        print(f"返回值: {result.result}")

    # 示例 2：测试固定延迟策略
    print("\n\n示例 2：固定延迟策略")
    print("-" * 40)

    handler2 = RetryHandler(max_retries=2, strategy=RetryStrategy.FIXED_DELAY, fixed_delay=1.0)

    attempt_count2 = [0]

    def wrapper2():
        attempt_count2[0] += 1
        if attempt_count2[0] < 2:
            raise ConnectionError("模拟网络错误")
        return "重试成功"

    result2 = handler2.execute_with_retry(wrapper2)

    print(f"\n结果: {'成功' if result2.success else '失败'}")
    print(f"尝试次数: {result2.attempts}")
    print(f"总等待时间: {result2.total_wait_time} 秒")

    # 示例 3：测试不可重试错误
    print("\n\n示例 3：不可重试错误")
    print("-" * 40)

    handler3 = RetryHandler(max_retries=3)

    def value_error_function():
        """不可重试的错误"""
        raise ValueError("这是永久性错误，不应重试")

    result3 = handler3.execute_with_retry(value_error_function)

    print(f"\n结果: {'成功' if result3.success else '失败'}")
    print(f"尝试次数: {result3.attempts}")
    if not result3.success:
        print(f"错误类型: {type(result3.error).__name__}")
        print(f"错误信息: {result3.error}")

    # 示例 4：自定义可重试错误
    print("\n\n示例 4：自定义可重试错误")
    print("-" * 40)

    handler4 = RetryHandler(max_retries=2)

    def custom_error_function():
        raise RuntimeError("自定义错误")

    # 指定 RuntimeError 为可重试错误
    result4 = handler4.execute_with_retry(custom_error_function, retry_on_error=(RuntimeError,))

    print(f"\n结果: {'成功' if result4.success else '失败'}")
    print(f"尝试次数: {result4.attempts}")
