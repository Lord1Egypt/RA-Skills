"""Error types for the Dida365 OpenAPI CLI."""

from __future__ import annotations

from typing import Any, Optional


class UserFacingError(Exception):
    """An error safe to render directly to the CLI user."""

    def __init__(
        self,
        message: str,
        *,
        details: Optional[dict[str, Any]] = None,
        exit_code: int = 2,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.exit_code = exit_code

    def to_error_dict(self) -> dict[str, Any]:
        payload = {
            "type": self.__class__.__name__,
            "message": self.message,
        }
        if self.details:
            payload["details"] = self.details
        return payload


class ApiError(UserFacingError):
    """HTTP error returned by the Dida365 API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        method: str,
        url: str,
        response_body: Any = None,
    ) -> None:
        details = {
            "status_code": status_code,
            "method": method,
            "url": url,
        }
        if response_body not in (None, ""):
            details["response_body"] = response_body
        super().__init__(message, details=details, exit_code=1)
        self.status_code = status_code
        self.method = method
        self.url = url
        self.response_body = response_body

