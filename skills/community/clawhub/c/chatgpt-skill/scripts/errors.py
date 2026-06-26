"""Error model for chatgpt-skill."""

from __future__ import annotations

from typing import Any, Dict, Optional


class ChatGPTSkillError(RuntimeError):
    def __init__(self, code: str, message: str, *, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    def to_dict(self, **extra: Any) -> Dict[str, Any]:
        payload = {
            "status": "error",
            "error_code": self.code,
            "error": self.message,
        }
        payload.update(self.details)
        payload.update(extra)
        return payload


def ensure(condition: bool, code: str, message: str, **details: Any):
    if not condition:
        raise ChatGPTSkillError(code, message, details=details or None)


def result_from_exception(error: Exception, **extra: Any) -> Dict[str, Any]:
    if isinstance(error, ChatGPTSkillError):
        return error.to_dict(**extra)
    payload = {
        "status": "error",
        "error_code": "unexpected_error",
        "error": str(error),
    }
    payload.update(extra)
    return payload
