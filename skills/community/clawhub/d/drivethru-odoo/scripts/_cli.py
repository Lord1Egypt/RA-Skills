"""Shared CLI plumbing for the drivethru-odoo skill scripts.

Each command script dispatches on `argv[1]` (the action) and reads an optional
JSON object from stdin. Results are printed as a single JSON object on stdout;
failures print `{"error": {...}}` and exit non-zero.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable

from odoo_client import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    OdooAPIError,
    OdooClient,
    OdooConnectionError,
    client_from_env,
)


def fail(error_type: str, message: str, exit_code: int = 1, **extra: Any) -> None:
    print(json.dumps({"error": {"type": error_type, "message": message, **extra}}))
    sys.exit(exit_code)


def emit(payload: Any) -> None:
    print(json.dumps(payload, default=str))


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("validation_error", f"Invalid JSON on stdin: {exc}")
    if not isinstance(payload, dict):
        fail("validation_error", "Input must be a JSON object.")
    return payload  # type: ignore[return-value]


def get_client() -> OdooClient:
    try:
        return client_from_env()
    except OdooConnectionError as exc:
        fail("config_error", str(exc), exit_code=2)
    raise AssertionError("unreachable")


def run(
    actions: dict[str, Callable[[OdooClient, dict[str, Any]], Any]],
    *,
    usage: str,
    offline_actions: set[str] | None = None,
) -> None:
    """Dispatch `argv[1]` against `actions`, reading args from stdin JSON.

    Actions named in `offline_actions` run without building an Odoo client
    (they receive None) and never require ODOO_URL / ODOO_API_KEY.
    """
    offline_actions = offline_actions or set()
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        fail("usage", usage, exit_code=2, actions=sorted(actions))

    action = sys.argv[1]
    handler = actions.get(action)
    if handler is None:
        fail(
            "unknown_action",
            f"Unknown action {action!r}.",
            exit_code=2,
            actions=sorted(actions),
        )

    args = read_stdin_json()
    client = None if action in offline_actions else get_client()
    try:
        result = handler(client, args)
    except OdooAPIError as exc:
        fail("api_error", str(exc), status=exc.status, body=str(exc.body)[:500])
    except OdooConnectionError as exc:
        fail("connection_error", str(exc))
    except (KeyError, ValueError, TypeError) as exc:
        fail("validation_error", str(exc))
    emit(result)
