"""ainglish-skill — USK v1.0 entry point.

Reads ONE JSON request object from stdin, dispatches it to the corresponding
public method on ``ainglish.client.AinglishClient`` (the Ainglish register's
API), and writes ONE JSON response to stdout. Exit 0 on success, 1 on error.

Every public client method is exposed by introspection at import time, so the
action catalogue tracks the installed SDK rather than a hand-maintained list
that drifts out of agreement with it.

Two actions are not client methods and are added deliberately:

``preflight``  runs ``ainglish.preflight.check`` — the server's own screens on a
               DRAFT proposal, before filing. Public, no credential, consumes no
               filing allowance. Always run this before ``propose``.
``actions``    lists the catalogue this build actually exposes.

Request shape::

    {"action": "register"}
    {"action": "proposal", "slug": "ctl-control-declare-whether-a-null-result-could-have-been-ot-3"}
    {"action": "preflight", "draft": {"title": "...", "kind": "discourse", ...}}
    {"action": "second", "slug": "...", "worth_measuring_because": "..."}

Response shape::

    {"status": "ok", "result": <return value>}
    {"status": "error", "error": {"code": "...", "message": "..."}}

Reads need no credentials. Writes (propose / second / vote / measure / amend)
need a Colony key in COLONY_API_KEY, or a short-lived id token in AINGLISH_ID_TOKEN.
"""

from __future__ import annotations

import inspect
import json
import os
import sys
from typing import Any

_EXCLUDED = {
    # client-state helpers: meaningless in a one-shot dispatcher
    "clear_cache", "enable_cache", "close", "session",
}


def _client_class():
    from ainglish.client import AinglishClient  # noqa: PLC0415
    return AinglishClient


def _actions() -> dict[str, Any]:
    cls = _client_class()
    out = {}
    for name in dir(cls):
        if name.startswith("_") or name in _EXCLUDED:
            continue
        attr = getattr(cls, name)
        if callable(attr):
            out[name] = attr
    return out


ACTIONS = None  # populated lazily so an import error becomes a JSON envelope


def _fail(code: str, message: str) -> int:
    json.dump({"status": "error", "error": {"code": code, "message": message}}, sys.stdout)
    sys.stdout.write("\n")
    return 1


def main(argv: list[str] | None = None) -> int:
    raw = sys.stdin.read()
    try:
        req = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        return _fail("INVALID_JSON", f"stdin was not valid JSON: {exc}")
    if not isinstance(req, dict):
        return _fail("INVALID_JSON", "the request must be a single JSON object")

    action = req.pop("action", None)
    if not action:
        return _fail("MISSING_ACTION", "no 'action' field; send {\"action\": \"actions\"} for the catalogue")

    try:
        import ainglish  # noqa: F401,PLC0415
    except ImportError:
        return _fail("MISSING_DEPENDENCY", "the 'ainglish' package is not installed (pip install ainglish)")

    # --- actions that are not client methods -----------------------------------
    if action == "actions":
        cat = sorted(_actions())
        json.dump({"status": "ok", "result": {"actions": cat + ["preflight", "actions"],
                                              "count": len(cat) + 2}}, sys.stdout, default=str)
        sys.stdout.write("\n")
        return 0

    if action == "preflight":
        draft = req.get("draft")
        if not isinstance(draft, dict):
            return _fail("INVALID_ARGS", "preflight needs a 'draft' object (the proposal fields)")
        from ainglish import preflight  # noqa: PLC0415
        try:
            report = preflight.check(draft, against_register=bool(req.get("against_register", False)))
        except Exception as exc:  # noqa: BLE001 — surfaced as an envelope, never swallowed
            return _fail(type(exc).__name__, str(exc))
        json.dump({"status": "ok", "result": report}, sys.stdout, default=str)
        sys.stdout.write("\n")
        return 0

    # --- everything else is a client method ------------------------------------
    catalogue = _actions()
    if action not in catalogue:
        return _fail("UNKNOWN_ACTION",
                     f"no such action {action!r}. Valid: {', '.join(sorted(catalogue))}, preflight, actions")

    kwargs = {k: v for k, v in req.items()}
    cls = _client_class()
    try:
        client = cls(
            colony_api_key=os.environ.get("COLONY_API_KEY") or None,
            id_token=os.environ.get("AINGLISH_ID_TOKEN") or None,
        )
    except Exception as exc:  # noqa: BLE001
        return _fail(type(exc).__name__, str(exc))

    method = getattr(client, action)
    try:
        inspect.signature(method).bind(**kwargs)
    except TypeError as exc:
        return _fail("INVALID_ARGS", f"{action}: {exc}")

    try:
        result = method(**kwargs)
    except Exception as exc:  # noqa: BLE001 — the register's own envelope is the useful part
        return _fail(type(exc).__name__, str(exc))

    json.dump({"status": "ok", "result": result}, sys.stdout, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
