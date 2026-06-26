from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .shared import redact_sensitive_text


def cli_error_payload(
    *,
    command: str | None,
    reason_code: str,
    message: Any,
    exit_code: int = 1,
    error_type: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schemaVersion": 1,
        "ok": False,
        "status": "error",
        "reasonCode": reason_code,
        "generatedAt": datetime.now(UTC).isoformat(),
        "command": command,
        "message": redact_sensitive_text(message),
        "error": {
            "type": error_type or "RuntimeError",
            "message": redact_sensitive_text(message),
        },
        "exitCode": exit_code,
    }
    if details:
        payload["details"] = details
    return payload

