"""
Error Classifier - 四类错误分类与处理引擎

将错误自动分类为 TRANSIENT / PERMANENT / VALIDATION / CONTEXT，
并提供对应的处理策略（重试 / 报告用户 / 回传修复 / 触发压缩）。

集成点：coding-framework Step 5.5（异常处理）
"""

import re
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Callable, Any

from patterns import (
    TRANSIENT_PATTERNS,
    PERMANENT_PATTERNS,
    VALIDATION_PATTERNS,
    CONTEXT_PATTERNS,
)

logger = logging.getLogger(__name__)


# ============================================================
# 枚举与数据结构
# ============================================================

class ErrorType(Enum):
    """四类错误枚举"""
    TRANSIENT = "transient"      # 临时错误 → 自动重试
    PERMANENT = "permanent"      # 永久错误 → 报告用户
    VALIDATION = "validation"    # 验证错误 → 回传模型修复
    CONTEXT = "context"          # 上下文错误 → 触发压缩


@dataclass
class ErrorAction:
    """错误处理动作"""
    action: str          # retry / report_user / fix / compress / abort
    message: str
    retry_delay: int = 0
    retry_count: int = 0
    metadata: dict = field(default_factory=dict)


# ============================================================
# 错误分类器
# ============================================================

class ErrorClassifier:
    """
    四类错误分类与处理引擎

    用法：
        classifier = ErrorClassifier()
        error_type = classifier.classify(exception)
        action = classifier.handle(exception, context={"retry_count": 0})
    """

    MAX_RETRIES = 3
    BASE_DELAY = 1  # 秒

    # 分类优先级：CONTEXT > VALIDATION > PERMANENT > TRANSIENT
    # 原因：上下文错误最紧急（需要压缩），验证错误需要修复逻辑，
    # 永久错误不可恢复，其余默认为临时错误。

    def classify(self, error: Exception) -> ErrorType:
        """
        错误分类

        Args:
            error: 异常对象或包含错误信息的字符串

        Returns:
            ErrorType 枚举值
        """
        error_msg = str(error).lower()

        # 按优先级检查
        if self._matches(error_msg, CONTEXT_PATTERNS):
            return ErrorType.CONTEXT
        if self._matches(error_msg, VALIDATION_PATTERNS):
            return ErrorType.VALIDATION
        if self._matches(error_msg, PERMANENT_PATTERNS):
            return ErrorType.PERMANENT
        return ErrorType.TRANSIENT

    def handle(self, error: Exception, context: dict = None) -> ErrorAction:
        """
        错误处理 - 根据分类返回对应处理动作

        Args:
            error: 异常对象
            context: 上下文信息，可包含 retry_count, error_type 等

        Returns:
            ErrorAction 处理动作
        """
        context = context or {}
        error_type = self.classify(error)
        retry_count = context.get("retry_count", 0)

        if error_type == ErrorType.TRANSIENT:
            if retry_count < self.MAX_RETRIES:
                delay = self.get_retry_delay(retry_count)
                return ErrorAction(
                    action="retry",
                    message=f"临时错误，{delay}秒后重试（第{retry_count + 1}次）",
                    retry_delay=delay,
                    retry_count=retry_count + 1,
                    metadata={"error_type": error_type.value},
                )
            else:
                return ErrorAction(
                    action="report_user",
                    message=f"重试{self.MAX_RETRIES}次后仍失败: {error}",
                    metadata={
                        "error_type": error_type.value,
                        "retries_exhausted": True,
                    },
                )

        elif error_type == ErrorType.PERMANENT:
            return ErrorAction(
                action="report_user",
                message=f"不可恢复的错误: {error}",
                metadata={"error_type": error_type.value},
            )

        elif error_type == ErrorType.VALIDATION:
            return ErrorAction(
                action="fix",
                message=f"验证错误，回传模型修复: {error}",
                metadata={"error_type": error_type.value},
            )

        elif error_type == ErrorType.CONTEXT:
            return ErrorAction(
                action="compress",
                message=f"上下文超限，触发压缩: {error}",
                metadata={"error_type": error_type.value},
            )

        # 兜底（理论上不会到达）
        return ErrorAction(
            action="abort",
            message=f"未知错误类型: {error}",
            metadata={"error_type": "unknown"},
        )

    def get_retry_delay(self, attempt: int) -> int:
        """
        指数退避计算

        第0次重试: 1s (BASE_DELAY * 2^0)
        第1次重试: 2s (BASE_DELAY * 2^1)
        第2次重试: 4s (BASE_DELAY * 2^2)

        Args:
            attempt: 当前重试次数（从0开始）

        Returns:
            等待秒数
        """
        return self.BASE_DELAY * (2 ** attempt)

    def execute_with_retry(
        self,
        func: Callable,
        *args,
        on_retry: Optional[Callable[[int, int, Exception], None]] = None,
        **kwargs,
    ) -> Any:
        """
        带指数退避的重试执行器

        Args:
            func: 要执行的函数
            on_retry: 重试回调 (attempt, delay, error)
            *args, **kwargs: 传给 func 的参数

        Returns:
            func 的返回值

        Raises:
            最后一次重试的异常（如果全部失败）
        """
        last_error = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                error_type = self.classify(e)

                # 非临时错误直接抛出
                if error_type != ErrorType.TRANSIENT:
                    raise

                # 已达最大重试次数
                if attempt >= self.MAX_RETRIES:
                    raise

                delay = self.get_retry_delay(attempt)
                logger.warning(
                    f"临时错误（第{attempt + 1}次），{delay}秒后重试: {e}"
                )

                if on_retry:
                    on_retry(attempt, delay, e)

                time.sleep(delay)

        raise last_error  # 兜底

    def _matches(self, text: str, patterns: list) -> bool:
        """检查文本是否匹配任一模式"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False


# ============================================================
# 便捷函数
# ============================================================

_default_classifier = ErrorClassifier()


def classify_error(error: Exception) -> ErrorType:
    """便捷函数：分类错误"""
    return _default_classifier.classify(error)


def handle_error(error: Exception, context: dict = None) -> ErrorAction:
    """便捷函数：处理错误"""
    return _default_classifier.handle(error, context)


def get_retry_delay(attempt: int) -> int:
    """便捷函数：获取重试延迟"""
    return _default_classifier.get_retry_delay(attempt)
