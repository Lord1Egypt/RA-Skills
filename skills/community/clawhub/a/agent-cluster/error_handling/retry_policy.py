"""
Retry Policy - 错误恢复与重试策略

功能：
- 多种重试策略（固定/指数/抖动）
- 条件重试（可配置）
- 熔断器保护
- 重试历史记录
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

from exception_middleware import ExceptionClassifier, ErrorCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

F = TypeVar("F")


# =============================================================================
# 重试策略
# =============================================================================

class RetryStrategy(Enum):
    """重试策略"""
    FIXED = "fixed"          # 固定间隔
    EXPONENTIAL = "exp"      # 指数退避
    FIBONACCI = "fib"        # 斐波那契退避
    JITTER = "jitter"        # 随机抖动（最推荐）

    # 组合策略
    EXP_JITTER = "exp_jitter"  # 指数+抖动（AWS/Jitter公式）


@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3
    strategy: RetryStrategy = RetryStrategy.EXP_JITTER
    base_delay: float = 1.0     # 基础延迟（秒）
    max_delay: float = 60.0     # 最大延迟
    jitter_range: tuple[float, float] = (0.0, 1.0)  # 抖动范围
    retryable_categories: set[ErrorCategory] = field(
        default_factory=lambda: {
            ErrorCategory.NETWORK, ErrorCategory.TIMEOUT, ErrorCategory.EXTERNAL,
        }
    )
    fatal_categories: set[ErrorCategory] = field(
        default_factory=lambda: {
            ErrorCategory.VALIDATION, ErrorCategory.AUTH, ErrorCategory.INTERNAL,
        }
    )


# =============================================================================
# 重试器
# =============================================================================

@dataclass
class RetryAttempt:
    """重试尝试记录"""
    attempt: int
    timestamp: str
    delay_used: float
    error_category: str
    error_message: str
    success: bool = False


@dataclass
class RetryResult:
    """重试结果"""
    success: bool
    result: Any = None
    total_attempts: int = 0
    total_time_ms: float = 0.0
    attempts: list[RetryAttempt] = field(default_factory=list)
    final_error: Optional[str] = None
    final_category: Optional[ErrorCategory] = None


# =============================================================================
# 重试执行器
# =============================================================================

class RetryExecutor:
    """
    可配置的重试执行器

    支持多种重试策略，智能识别可重试的错误
    """

    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()

    def _calculate_delay(self, attempt: int) -> float:
        """根据策略计算延迟"""
        base = self.config.base_delay

        if self.config.strategy == RetryStrategy.FIXED:
            delay = base

        elif self.config.strategy == RetryStrategy.EXPONENTIAL:
            delay = base * (2 ** (attempt - 1))

        elif self.config.strategy == RetryStrategy.FIBONACCI:
            # 斐波那契数列
            fib = [1, 1, 2, 3, 5, 8, 13, 21]
            multiplier = fib[min(attempt - 1, len(fib) - 1)]
            delay = base * multiplier

        elif self.config.strategy == RetryStrategy.EXP_JITTER:
            # AWS推荐公式: min(cap, base * 2^attempt + random)
            cap = self.config.max_delay
            exponential = min(cap, base * (2 ** attempt))
            jitter = random.uniform(*self.config.jitter_range)
            delay = exponential * jitter + random.uniform(0, exponential * 0.5)

        elif self.config.strategy == RetryStrategy.JITTER:
            # 纯抖动
            delay = base * random.uniform(*self.config.jitter_range)

        else:
            delay = base

        return min(delay, self.config.max_delay)

    def _should_retry(self, exc: Exception) -> bool:
        """判断异常是否可重试"""
        category, _ = ExceptionClassifier.classify(exc)

        if category in self.config.fatal_categories:
            return False
        if category in self.config.retryable_categories:
            return True
        return False

    async def execute(
        self,
        func: Callable,
        *args,
        on_retry: Optional[Callable[[int, Exception], None]] = None,
        **kwargs,
    ) -> RetryResult:
        """
        执行带重试的函数

        Args:
            func: 要执行的异步函数
            on_retry: 每次重试前的回调（可选）

        Returns:
            RetryResult: 包含所有尝试的详细信息
        """
        attempts: list[RetryAttempt] = []
        start_time = time.time()
        last_exc: Optional[Exception] = None
        last_category: Optional[ErrorCategory] = None

        for attempt in range(1, self.config.max_attempts + 1):
            attempt_start = time.time()

            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                total_time = (time.time() - start_time) * 1000
                return RetryResult(
                    success=True,
                    result=result,
                    total_attempts=attempt,
                    total_time_ms=total_time,
                    attempts=attempts,
                )

            except Exception as e:
                last_exc = e
                category, severity = ExceptionClassifier.classify(e)
                last_category = category
                attempt_time = (time.time() - attempt_start) * 1000

                attempt_record = RetryAttempt(
                    attempt=attempt,
                    timestamp=datetime.now().isoformat(),
                    delay_used=0.0,
                    error_category=category.value,
                    error_message=str(e)[:100],
                    success=False,
                )
                attempts.append(attempt_record)

                # 判断是否继续重试
                if not self._should_retry(e):
                    logger.warning(
                        f"[重试] 异常 {category.value} 不可重试（{severity.value}），终止重试"
                    )
                    break

                if attempt < self.config.max_attempts:
                    delay = self._calculate_delay(attempt)
                    attempt_record.delay_used = delay
                    logger.info(
                        f"[重试] 第{attempt}次失败，{category.value}，{delay:.1f}s后重试 "
                        f"({attempt}/{self.config.max_attempts})"
                    )
                    if on_retry:
                        on_retry(attempt, e)
                    await asyncio.sleep(delay)
                else:
                    logger.warning(f"[重试] 达到最大重试次数 {self.config.max_attempts}，放弃")

        total_time = (time.time() - start_time) * 1000
        return RetryResult(
            success=False,
            total_attempts=len(attempts),
            total_time_ms=total_time,
            attempts=attempts,
            final_error=str(last_exc)[:200] if last_exc else None,
            final_category=last_category,
        )

    def execute_sync(
        self,
        func: Callable,
        *args,
        **kwargs,
    ) -> RetryResult:
        """同步版本的重试执行"""
        attempts: list[RetryAttempt] = []
        start_time = time.time()
        last_exc: Optional[Exception] = None
        last_category: Optional[ErrorCategory] = None

        for attempt in range(1, self.config.max_attempts + 1):
            attempt_start = time.time()

            try:
                result = func(*args, **kwargs)
                total_time = (time.time() - start_time) * 1000
                return RetryResult(
                    success=True, result=result, total_attempts=attempt,
                    total_time_ms=total_time, attempts=attempts,
                )
            except Exception as e:
                last_exc = e
                category, _ = ExceptionClassifier.classify(e)
                last_category = category
                attempt_time = (time.time() - attempt_start) * 1000

                attempts.append(RetryAttempt(
                    attempt=attempt, timestamp=datetime.now().isoformat(),
                    delay_used=0.0, error_category=category.value,
                    error_message=str(e)[:100], success=False,
                ))

                if not self._should_retry(e):
                    break
                if attempt < self.config.max_attempts:
                    delay = self._calculate_delay(attempt)
                    attempts[-1].delay_used = delay
                    logger.info(f"[重试] 第{attempt}次失败，{delay:.1f}s后重试")
                    time.sleep(delay)

        return RetryResult(
            success=False, total_attempts=len(attempts),
            total_time_ms=(time.time() - start_time) * 1000,
            attempts=attempts, final_error=str(last_exc)[:200] if last_exc else None,
            final_category=last_category,
        )


# =============================================================================
# 装饰器便捷工具
# =============================================================================

def with_retry(
    config: Optional[RetryConfig] = None,
    strategy: RetryStrategy = RetryStrategy.EXP_JITTER,
    max_attempts: int = 3,
    base_delay: float = 1.0,
):
    """
    重试装饰器

    用法：
        @with_retry(max_attempts=5, strategy=RetryStrategy.EXP_JITTER)
        async def call_api():
            ...
    """
    cfg = config or RetryConfig(
        max_attempts=max_attempts,
        strategy=strategy,
        base_delay=base_delay,
    )
    executor = RetryExecutor(cfg)

    def decorator(func: F) -> F:
        async def wrapper(*args, **kwargs):
            result = await executor.execute(func, *args, **kwargs)
            if not result.success:
                raise Exception(f"重试失败（{result.total_attempts}次尝试）: {result.final_error}")
            return result.result

        def sync_wrapper(*args, **kwargs):
            result = executor.execute_sync(func, *args, **kwargs)
            if not result.success:
                raise Exception(f"重试失败（{result.total_attempts}次尝试）: {result.final_error}")
            return result.result

        if asyncio.iscoroutinefunction(func):
            return wrapper
        return sync_wrapper

    return decorator
