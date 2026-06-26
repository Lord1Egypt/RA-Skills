"""
Exception Middleware - 统一异常处理中间件

功能：
- 全局异常捕获与分类
- 结构化错误响应
- 异常日志与告警
- 错误恢复建议
"""

from __future__ import annotations

import asyncio
import logging
import traceback
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional, TypeVar
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

F = TypeVar("F")


# =============================================================================
# 异常分类
# =============================================================================

class ErrorCategory(Enum):
    """错误分类"""
    VALIDATION = "validation"         # 参数校验错误
    NETWORK = "network"               # 网络/连接错误
    TIMEOUT = "timeout"              # 超时错误
    AUTH = "auth"                    # 认证/权限错误
    RESOURCE = "resource"             # 资源不足
    NOT_FOUND = "not_found"          # 资源不存在
    CONFLICT = "conflict"            # 状态冲突
    INTERNAL = "internal"            # 内部错误
    EXTERNAL = "external"            # 外部依赖错误
    UNKNOWN = "unknown"              # 未知错误


class ErrorSeverity(Enum):
    """错误严重级别"""
    LOW = "low"          # 可忽略，替代方案可用
    MEDIUM = "medium"    # 需要关注，但可继续
    HIGH = "high"        # 必须处理
    CRITICAL = "critical"  # 系统级故障


# =============================================================================
# 结构化错误响应
# =============================================================================

@dataclass
class ErrorResponse:
    """结构化错误响应"""
    error_id: str                    # 错误唯一ID（便于追踪）
    category: ErrorCategory
    severity: ErrorSeverity
    message: str                    # 对用户友好的错误信息
    detail: Optional[str] = None    # 技术细节
    suggestion: Optional[str] = None  # 恢复建议
    source: str = ""                # 错误来源（模块/函数）
    caused_by: Optional[str] = None  # 原始异常类型
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    request_id: Optional[str] = None  # 关联的请求ID
    retry_recommended: bool = True  # 是否建议重试

    def to_dict(self) -> dict:
        return {
            "error_id": self.error_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "detail": self.detail,
            "suggestion": self.suggestion,
            "source": self.source,
            "caused_by": self.caused_by,
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "retry_recommended": self.retry_recommended,
        }


# =============================================================================
# 异常分类器
# =============================================================================

class ExceptionClassifier:
    """将异常分类为ErrorCategory和ErrorSeverity"""

    # 网络相关异常
    NETWORK_EXCEPTIONS = (
        ConnectionError, TimeoutError, asyncio.TimeoutError,
        ConnectionRefusedError, ConnectionResetError,
    )

    # 认证相关异常
    AUTH_EXCEPTIONS = (PermissionError,)

    # 超时异常
    TIMEOUT_EXCEPTIONS = (asyncio.TimeoutError,)

    # 资源异常
    RESOURCE_EXCEPTIONS = (MemoryError, OSError)

    @classmethod
    def classify(cls, exc: Exception) -> tuple[ErrorCategory, ErrorSeverity]:
        """分类异常"""
        if isinstance(exc, cls.TIMEOUT_EXCEPTIONS):
            return ErrorCategory.TIMEOUT, ErrorSeverity.MEDIUM

        if isinstance(exc, cls.NETWORK_EXCEPTIONS):
            return ErrorCategory.NETWORK, ErrorSeverity.HIGH

        if isinstance(exc, (ValueError, TypeError, KeyError)):
            return ErrorCategory.VALIDATION, ErrorSeverity.MEDIUM

        if isinstance(exc, PermissionError):
            return ErrorCategory.AUTH, ErrorSeverity.HIGH

        if isinstance(exc, FileNotFoundError, KeyError):
            return ErrorCategory.NOT_FOUND, ErrorSeverity.MEDIUM

        if isinstance(exc, (MemoryError, OSError)):
            return ErrorCategory.RESOURCE, ErrorSeverity.HIGH

        # 检查异常消息中的关键词
        msg = str(exc).lower()
        if "auth" in msg or "permission" in msg:
            return ErrorCategory.AUTH, ErrorSeverity.HIGH
        if "timeout" in msg:
            return ErrorCategory.TIMEOUT, ErrorSeverity.MEDIUM
        if "not found" in msg or "不存在" in msg:
            return ErrorCategory.NOT_FOUND, ErrorSeverity.LOW
        if "conflict" in msg or "冲突" in msg:
            return ErrorCategory.CONFLICT, ErrorSeverity.MEDIUM

        return ErrorCategory.UNKNOWN, ErrorSeverity.MEDIUM

    @classmethod
    def get_suggestion(cls, category: ErrorCategory, severity: ErrorSeverity) -> str:
        """根据错误类别提供恢复建议"""
        suggestions = {
            ErrorCategory.VALIDATION: "请检查输入参数是否正确",
            ErrorCategory.NETWORK: "请检查网络连接，ERP系统是否可达，可尝试重试",
            ErrorCategory.TIMEOUT: "ERP响应超时，建议稍后重试或检查ERP系统状态",
            ErrorCategory.AUTH: "认证失败，请检查API密钥和权限配置",
            ErrorCategory.RESOURCE: "系统资源不足，请检查服务器负载",
            ErrorCategory.NOT_FOUND: "请求的资源不存在，请检查参数",
            ErrorCategory.CONFLICT: "操作冲突，请稍后重试",
            ErrorCategory.INTERNAL: "系统内部错误，请联系技术支持",
            ErrorCategory.EXTERNAL: "外部依赖异常，请稍后重试",
            ErrorCategory.UNKNOWN: "未知错误，请查看详细日志",
        }
        return suggestions.get(category, "请稍后重试")


# =============================================================================
# 统一异常处理中间件
# =============================================================================

class ExceptionMiddleware:
    """
    统一异常处理中间件

    功能：
    - 全局异常捕获
    - 异常分类与严重级别评估
    - 结构化错误响应
    - 自动日志记录
    - 告警回调
    """

    def __init__(
        self,
        log_callback: Optional[Callable[[ErrorResponse], None]] = None,
        alert_callback: Optional[Callable[[ErrorResponse], None]] = None,
    ):
        self.log_callback = log_callback
        self.alert_callback = alert_callback
        self._error_count: dict[ErrorCategory, int] = {c: 0 for c in ErrorCategory}

    def handle(self, exc: Exception, source: str = "", request_id: Optional[str] = None) -> ErrorResponse:
        """处理异常，生成结构化错误响应"""
        error_id = str(uuid.uuid4())[:8]
        category, severity = ExceptionClassifier.classify(exc)
        suggestion = ExceptionClassifier.get_suggestion(category, severity)

        self._error_count[category] += 1

        response = ErrorResponse(
            error_id=error_id,
            category=category,
            severity=severity,
            message=self._human_message(exc, category),
            detail=traceback.format_exc(),
            suggestion=suggestion,
            source=source,
            caused_by=type(exc).__name__,
            request_id=request_id,
            retry_recommended=category not in (ErrorCategory.VALIDATION, ErrorCategory.AUTH, ErrorCategory.INTERNAL),
        )

        # 记录日志
        log_func = logger.warning if severity in (ErrorSeverity.MEDIUM, ErrorSeverity.LOW) else logger.error
        log_func(
            f"[异常中间件] [{error_id}] {category.value} | {severity.value} | {source} | "
            f"{type(exc).__name__}: {str(exc)[:100]}"
        )

        if self.log_callback:
            self.log_callback(response)

        # 高严重级别告警
        if severity == ErrorSeverity.CRITICAL and self.alert_callback:
            self.alert_callback(response)
        if severity == ErrorSeverity.HIGH and category == ErrorCategory.NETWORK and self.alert_callback:
            self.alert_callback(response)

        return response

    def _human_message(self, exc: Exception, category: ErrorCategory) -> str:
        """生成对用户友好的错误信息"""
        exc_msg = str(exc)

        human_messages = {
            ErrorCategory.VALIDATION: f"参数错误：{exc_msg[:100]}",
            ErrorCategory.NETWORK: "无法连接到ERP系统，请检查网络连接",
            ErrorCategory.TIMEOUT: f"ERP系统响应超时（{exc_msg[:50]}），请稍后重试",
            ErrorCategory.AUTH: "认证失败，请检查API配置",
            ErrorCategory.NOT_FOUND: f"数据未找到：{exc_msg[:80]}",
            ErrorCategory.CONFLICT: f"操作冲突：{exc_msg[:80]}",
            ErrorCategory.INTERNAL: "系统内部错误，请联系技术支持",
            ErrorCategory.EXTERNAL: f"外部服务异常：{exc_msg[:80]}",
            ErrorCategory.UNKNOWN: f"执行出错：{exc_msg[:100]}",
        }

        return human_messages.get(category, exc_msg[:100])

    def get_error_stats(self) -> dict:
        """获取错误统计"""
        total = sum(self._error_count.values())
        return {
            "total_errors": total,
            "by_category": {c.value: n for c, n in self._error_count.items() if n > 0},
        }


# =============================================================================
# 装饰器便捷工具
# =============================================================================

_global_middleware: Optional[ExceptionMiddleware] = None


def set_middleware(middleware: ExceptionMiddleware):
    global _global_middleware
    _global_middleware = middleware


def get_middleware() -> ExceptionMiddleware:
    global _global_middleware
    if _global_middleware is None:
        _global_middleware = ExceptionMiddleware()
    return _global_middleware


def handle_exceptions(source: str = ""):
    """
    异常处理装饰器

    用法：
        @handle_exceptions("inventory_agent")
        async def query_stock(params):
            ...
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            middleware = get_middleware()
            try:
                return await func(*args, **kwargs)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                response = middleware.handle(e, source=source)
                raise Exception(f"[{response.error_id}] {response.message}") from e

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            middleware = get_middleware()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                response = middleware.handle(e, source=source)
                raise Exception(f"[{response.error_id}] {response.message}") from e

        if asyncio.iscoroutinefunction(func):
            return wrapper
        return sync_wrapper

    return decorator
