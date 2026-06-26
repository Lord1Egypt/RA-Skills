from __future__ import annotations

from typing import Any

from canvas_claw.client import CanvasClawClient
from canvas_claw.errors import CanvasClawError


def login_and_extract_session(
    client: CanvasClawClient,
    *,
    username: str,
    password: str,
) -> dict[str, Any]:
    response = client.login(username=username, password=password)
    if int(response.get("code") or 0) != 1:
        raise CanvasClawError(str(response.get("msg") or "Login failed"))
    data = response.get("data")
    if not isinstance(data, dict):
        raise CanvasClawError("Login response missing session data")
    return data
