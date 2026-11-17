"""Shared CLI plumbing: dispatch on argv[1], JSON on stdin, one JSON object out.

Exit codes carry meaning:

    0  success
    1  a failure that is safe to retry or fix and re-run
    2  usage / config error (bad action, missing credential)
    3  ESCALATION REQUIRED — an order may exist. Do not retry; see
       `ChamproPartialOrderError`.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from typing import Any, Callable

from errors import (
    ChamproAPIError,
    ChamproConfigError,
    ChamproError,
    ChamproPartialOrderError,
    ChamproTransportError,
    ChamproValidationError,
)

EXIT_ESCALATION = 3


def _default(value: Any) -> Any:
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return dataclasses.asdict(value)
    return str(value)


def emit(payload: Any) -> None:
    print(json.dumps(payload, default=_default))


def fail(error_type: str, message: str, exit_code: int = 1, **extra: Any) -> None:
    print(json.dumps({"error": {"type": error_type, "message": message, **extra}}, default=_default))
    sys.exit(exit_code)


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("validation_error", f"Invalid JSON on stdin: {exc}", exit_code=1)
    if not isinstance(payload, dict):
        fail("validation_error", "Input must be a JSON object.", exit_code=1)
    return payload  # type: ignore[return-value]


def run(actions: dict[str, Callable[..., Any]], *, usage: str) -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        fail("usage", usage, exit_code=2, actions=sorted(actions))

    action = sys.argv[1]
    handler = actions.get(action)
    if handler is None:
        import difflib  # noqa: PLC0415

        fail(
            "unknown_action",
            f"Unknown action {action!r}.",
            exit_code=2,
            actions=sorted(actions),
            did_you_mean=difflib.get_close_matches(action, list(actions), n=3, cutoff=0.4),
        )

    args = read_stdin_json()
    try:
        result = handler(**args)
    except ChamproPartialOrderError as exc:
        # The one case that must never be retried automatically: suborders were
        # created and lines failed in the same response.
        fail(
            "escalation_required",
            str(exc),
            exit_code=EXIT_ESCALATION,
            retryable=False,
            result=exc.result,
        )
    except ChamproConfigError as exc:
        fail("config_error", str(exc), exit_code=2)
    except ChamproValidationError as exc:
        fail("validation_error", str(exc))
    except ChamproTransportError as exc:
        fail("connection_error", str(exc), retryable=True)
    except ChamproAPIError as exc:
        fail(
            "api_error",
            str(exc),
            endpoint=exc.endpoint,
            codes=exc.codes,
            errors=exc.errors,
            retryable=exc.retryable,
            setup_problem=exc.is_setup_problem,
        )
    except ChamproError as exc:
        fail("api_error", str(exc))
    except (KeyError, ValueError, TypeError) as exc:
        fail("validation_error", f"{type(exc).__name__}: {exc}")
    emit(result)
