"""
Error Handling - 错误处理与状态管理

模块：
- task_state_machine: 任务状态机（pending/running/success/failed/retry）
- exception_middleware: 统一异常处理中间件
- retry_policy: 错误恢复与重试策略
- operation_log: 操作日志与审计追踪
"""

from __future__ import annotations

from .task_state_machine import (
    TaskStateMachine,
    TaskRecord,
    State,
)
from .exception_middleware import (
    ExceptionMiddleware,
    ErrorResponse,
    ErrorCategory,
    ErrorSeverity,
    ExceptionClassifier,
    handle_exceptions,
    set_middleware,
    get_middleware,
)
from .retry_policy import (
    RetryExecutor,
    RetryConfig,
    RetryResult,
    RetryStrategy,
    RetryAttempt,
    with_retry,
)
from .operation_log import (
    OperationLogger,
    OpLogEntry,
    OpLevel,
    OpType,
    PIIRedactor,
)

__all__ = [
    "TaskStateMachine", "TaskRecord", "State",
    "ExceptionMiddleware", "ErrorResponse", "ErrorCategory", "ErrorSeverity",
    "ExceptionClassifier", "handle_exceptions", "set_middleware", "get_middleware",
    "RetryExecutor", "RetryConfig", "RetryResult", "RetryStrategy", "RetryAttempt",
    "with_retry",
    "OperationLogger", "OpLogEntry", "OpLevel", "OpType", "PIIRedactor",
]
