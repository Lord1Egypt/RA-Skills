"""colony-memory-skill — USK v1.0 entry point.

Reads ONE JSON request object from stdin, dispatches to the corresponding
public method on ``colony_memory.ColonyMemory`` (agent memory backup/restore
over the Colony vault), and writes ONE JSON response to stdout. Exit 0 on
success, 1 on error.

Request shape::

    {"action": "backup", "documents": {"MEMORY.md": "..."}, "label": "default"}
    {"action": "restore", "label": "default"}
    {"action": "status"}

Response shape::

    {"status": "ok", "result": {<method return value>}}
    {"status": "error", "error": {"code": "<code>", "message": "<msg>"}}

See SKILL.md for the action catalogue and examples.
"""

from __future__ import annotations

import base64
import inspect
import json
import os
import sys
from typing import Any

from colony_memory import ColonyMemory

#: Public ColonyMemory methods exposed as actions (everything non-underscore).
ACTIONS: frozenset[str] = frozenset(
    name
    for name in dir(ColonyMemory)
    if not name.startswith("_") and callable(inspect.getattr_static(ColonyMemory, name))
)


def _error(code: str, message: str) -> dict[str, Any]:
    return {"status": "error", "error": {"code": code, "message": message}}


def _serialisable(obj: Any) -> Any:
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {k: _serialisable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialisable(v) for v in obj]
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: _serialisable(v) for k, v in vars(obj).items() if not k.startswith("_")}
    return str(obj)


def _build_signer() -> Any | None:
    raw = (os.environ.get("COLONY_MEMORY_SIGNING_SEED") or "").strip()
    if not raw:
        return None
    try:
        seed = bytes.fromhex(raw)
    except ValueError:
        seed = base64.urlsafe_b64decode(raw + "=" * ((4 - len(raw) % 4) % 4))
    from colony_memory import Ed25519Signer

    return Ed25519Signer(seed)


def _build_memory() -> ColonyMemory:
    api_key = os.environ.get("COLONY_MEMORY_API_KEY") or os.environ.get("COLONY_API_KEY")
    if not api_key:
        raise RuntimeError("COLONY_API_KEY (or COLONY_MEMORY_API_KEY) is not set")
    kwargs: dict[str, Any] = {"api_key": api_key}
    base = os.environ.get("COLONY_MEMORY_API_BASE") or os.environ.get("COLONY_API_BASE")
    if base:
        kwargs["base_url"] = base
    signer = _build_signer()
    if signer is not None:
        kwargs["signer"] = signer
    return ColonyMemory(**kwargs)


def _dispatch(request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("action")
    if not isinstance(action, str) or not action:
        return _error("INVALID_REQUEST", "Missing or empty 'action' field.")
    if action not in ACTIONS:
        return _error("UNKNOWN_ACTION", f"Unknown action {action!r}. Valid: {sorted(ACTIONS)}")

    kwargs = {k: v for k, v in request.items() if k != "action"}
    try:
        mem = _build_memory()
    except RuntimeError as e:
        return _error("MISSING_API_KEY", str(e))

    try:
        result = getattr(mem, action)(**kwargs)
        return {"status": "ok", "result": _serialisable(result)}
    except TypeError as e:
        return _error("INVALID_ARGS", str(e))
    except Exception as e:  # surface SDK/library errors with their class name
        return _error(getattr(e, "code", None) or type(e).__name__, str(e))


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        print(json.dumps(_error("EMPTY_INPUT", "No JSON received on stdin.")))
        return 1
    try:
        request = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps(_error("INVALID_JSON", f"Could not parse stdin as JSON: {e}")))
        return 1
    if not isinstance(request, dict):
        print(json.dumps(_error("INVALID_REQUEST", "Top-level JSON must be an object.")))
        return 1

    response = _dispatch(request)
    print(json.dumps(response, default=str))
    return 0 if response.get("status") == "ok" else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
