"""Shared CLI plumbing for the adidas Click skill scripts.

The single entrypoint (``adidas.py``) dispatches on ``argv[1]`` (the action),
reads an optional JSON object from stdin, and accepts a few credential **flags**
after the action. Results are printed as a single JSON object on stdout;
failures print ``{"error": {...}}`` and exit non-zero.

Credentials can be supplied three ways (later wins): the ``ADIDAS_CLICK_*``
environment variables, credential fields in the stdin JSON, or the CLI flags
``--username`` / ``--password`` / ``--base-url``. The flags let you run locally
without exporting env vars and without embedding secrets in the order JSON, e.g.

    echo '{"purchase_order": {...}, "confirm": false}' \\
        | python3 scripts/adidas.py create-purchase-order \\
            --username "$U" --password "$P"

Note: arguments on a command line are visible to other processes (``ps``) and
your shell history; for sensitive automation prefer env vars or the stdin JSON.
"""

from __future__ import annotations

import inspect
import json
import sys
from typing import Any, Callable

# CLI flags (after the action) that map to handler credential kwargs. Values are
# kept as raw strings — safe for usernames/passwords/URLs.
_CRED_FLAGS = {
    "--username": "username",
    "--password": "password",
    "--base-url": "base_url",
}

from adidas_client import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    AdidasAPIError,
    AdidasConfigError,
    AdidasError,
    AdidasTransportError,
)


def emit(payload: Any) -> None:
    print(json.dumps(payload, default=str))


def fail(error_type: str, message: str, exit_code: int = 1, **extra: Any) -> None:
    print(json.dumps({"error": {"type": error_type, "message": message, **extra}}))
    sys.exit(exit_code)


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("validation_error", f"Invalid JSON on stdin: {exc}", exit_code=1)
    if not isinstance(payload, dict):
        fail("validation_error", "Input must be a JSON object.", exit_code=1)
    return payload  # type: ignore[return-value]


def parse_cred_flags(argv: list[str]) -> dict[str, str]:
    """Parse ``--username`` / ``--password`` / ``--base-url`` flags from ``argv``.

    Accepts ``--flag value`` and ``--flag=value``. Any other token is an error
    (all non-credential arguments go in the stdin JSON). Values stay strings.
    """

    out: dict[str, str] = {}
    i = 0
    while i < len(argv):
        token = argv[i]
        if token.startswith("--") and "=" in token:
            flag, value = token.split("=", 1)
            i += 1
        elif token.startswith("--"):
            flag = token
            # A missing value, or a "value" that is itself a flag, means the
            # intended value was empty. On Windows PowerShell an unset/empty
            # variable is dropped from the command line, so `--username $U
            # --password $P` collapses to `--username --password …` — guard it
            # instead of using "--password" as the username.
            if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                got = "nothing" if i + 1 >= len(argv) else repr(argv[i + 1])
                fail(
                    "usage",
                    f"Flag {flag} needs a value (got {got}). If you are on "
                    "PowerShell, check the variable is set and non-empty — empty "
                    "or unset variables are dropped from the command line. Use "
                    f"{flag}=VALUE to pass a value that begins with '--'.",
                    exit_code=2,
                )
            value = argv[i + 1]
            i += 2
        else:
            fail(
                "usage",
                f"Unexpected argument {token!r}. Only credential flags "
                "(--username, --password, --base-url) are accepted; pass all "
                "other arguments as JSON on stdin.",
                exit_code=2,
            )
        key = _CRED_FLAGS.get(flag)
        if key is None:
            fail(
                "usage",
                f"Unknown flag {flag!r}. Supported: "
                + ", ".join(sorted(_CRED_FLAGS)),
                exit_code=2,
            )
        out[key] = value
    return out


def run(actions: dict[str, Callable[..., Any]], *, usage: str) -> None:
    """Dispatch ``argv[1]`` against ``actions``, reading kwargs from stdin JSON.

    Each handler is an ``adidas_*`` tool function. The stdin JSON object is
    splatted in as keyword arguments, so its keys must match the tool's
    parameter names. Credentials (``username``, ``password``, ``base_url``) may
    be supplied in the stdin JSON, via the ``--username`` / ``--password`` /
    ``--base-url`` CLI flags (which override the JSON), or via the
    ``ADIDAS_CLICK_*`` environment variables.
    """

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

    # Credential flags override matching stdin JSON fields. Only apply keys the
    # handler actually accepts, so an unrelated action never gets a bad kwarg.
    cred_flags = parse_cred_flags(sys.argv[2:])
    if cred_flags:
        params = inspect.signature(handler).parameters
        accepts_kwargs = any(
            p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()
        )
        for key, value in cred_flags.items():
            if accepts_kwargs or key in params:
                args[key] = value
            else:
                fail(
                    "usage",
                    f"Action {action!r} does not accept --{key.replace('_', '-')}.",
                    exit_code=2,
                )

    try:
        result = handler(**args)
    except AdidasConfigError as exc:
        fail("config_error", str(exc), exit_code=2)
    except AdidasTransportError as exc:
        fail("connection_error", str(exc), retryable=True)
    except AdidasAPIError as exc:
        fail(
            "api_error",
            str(exc),
            surface=getattr(exc, "surface", "adidas_click"),
            operation=getattr(exc, "operation", ""),
            retryable=getattr(exc, "retryable", False),
        )
    except AdidasError as exc:
        fail("api_error", str(exc))
    except (KeyError, ValueError, TypeError) as exc:
        fail("validation_error", str(exc))
    emit(result)
