from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class FeishuAPIError(Exception):
    """Base exception for Feishu API integration."""


@dataclass(slots=True)
class FeishuRequestError(FeishuAPIError):
    message: str
    code: int | None = None
    request_id: str | None = None
    details: Any = None

    def __str__(self) -> str:
        parts = [self.message]
        if self.code is not None:
            parts.append(f"code={self.code}")
        if self.request_id:
            parts.append(f"request_id={self.request_id}")
        return " | ".join(parts)


@dataclass(slots=True)
class FeishuConfigError(FeishuAPIError):
    message: str

    def __str__(self) -> str:
        return self.message
