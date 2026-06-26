"""API 客户端异常类型。"""

from __future__ import annotations

from typing import Any, Optional


class EqxiuAigcApiError(Exception):
    """服务端返回 success=false 或非预期响应时抛出。"""

    def __init__(self, message: str, *, status_code: Optional[int] = None, raw: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.raw = raw
