"""erpclaw_action dispatch: JSON args → ``db_query.py --action`` subprocess.

This is the single execution path (ADR-0024 sub-decision 1). It shells the
foundation router as an unchanged subprocess and returns its JSON stdout
**verbatim**. It introduces no new write path — every invariant (Decimal-as-TEXT,
UUID4, 12-step GL, immutable GL, the BEGIN..COMMIT submit transaction) stays
enforced inside the router, not here.

Arg mapping (matches the router's existing arg shapes):
  - ``{"company_id": "x"}``  → ``--company-id x``  (snake_case key → kebab flag)
  - ``{"force": true}``       → ``--force``          (bool true ⇒ flag presence)
  - ``{"force": false}``      → (omitted)            (bool false ⇒ no flag)
  - ``{"items": [ ... ]}``    → ``--items '<json>'`` (list/dict ⇒ JSON string arg)
  - ``{"name": "Acme"}``      → ``--name Acme``       (scalar ⇒ str(value))

Error semantics: a non-zero router exit (or non-JSON stdout) is surfaced as a
structured error object — never swallowed, never narrated.
"""
import json
import os
import subprocess
import sys

from . import confirm, paths

# The foundation router this server is a transport over.
_FOUNDATION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROUTER = os.path.join(_FOUNDATION_DIR, "scripts", "db_query.py")


def _json_arg(value) -> str:
    """Serialize a list/dict arg to the compact JSON string the routers expect."""
    return json.dumps(value, default=str, separators=(",", ":"))


def build_argv(action_name: str, args: dict, user_confirmed: bool) -> list:
    """Translate (action, JSON args) into the router argv. Pure / testable."""
    argv = [sys.executable, _ROUTER, "--action", action_name]
    for key, value in (args or {}).items():
        flag = "--" + str(key).replace("_", "-")
        if isinstance(value, bool):
            if value:
                argv.append(flag)          # bool true ⇒ flag presence only
            # bool false ⇒ omit entirely
        elif isinstance(value, (list, dict)):
            argv.extend([flag, _json_arg(value)])
        elif value is None:
            continue                        # null ⇒ omit (router treats absent as default)
        else:
            argv.extend([flag, str(value)])
    # The router consumes --user-confirmed for its DANGEROUS_ACTIONS gate. We add
    # it ONLY when the client genuinely confirmed (never mechanically).
    if user_confirmed and confirm.is_destructive(action_name):
        argv.append("--user-confirmed")
    return argv


def _resolve_env() -> dict:
    """Child env. ERPCLAW_HOME flows through unchanged so the subprocess router
    resolves the same lib + DB the server resolved (paths.py mirrors it)."""
    env = dict(os.environ)
    # Be explicit so the child cannot diverge from the server's resolution.
    env["ERPCLAW_HOME"] = paths.erpclaw_home()
    return env


def dispatch(action_name: str, args: dict, user_confirmed: bool = False) -> dict:
    """Run erpclaw_action. Returns a JSON-serializable dict (the tool result).

    Order of checks (all BEFORE any subprocess):
      1. Credential carve-out  → structured refusal, no execution.
      2. Destructive + not confirmed → confirmation-request, no execution.
      3. Otherwise dispatch the router and return its JSON stdout verbatim.
    """
    if confirm.is_credential_carved_out(action_name):
        return confirm.credential_refusal(action_name)

    if confirm.confirmation_required(action_name, user_confirmed):
        return confirm.confirmation_request(action_name)

    argv = build_argv(action_name, args or {}, user_confirmed)
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, env=_resolve_env(),
        )
    except OSError as e:
        return {"status": "error", "action": action_name,
                "error": f"Failed to spawn router subprocess: {e}"}

    stdout = (proc.stdout or "").strip()
    # The router emits JSON to stdout for both success and error. Parse it and
    # return verbatim. Reconcile against the exit code so a non-zero exit is
    # never reported as success.
    parsed = None
    if stdout:
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError:
            parsed = None

    if parsed is not None and isinstance(parsed, dict):
        # Surface the router result verbatim. If the router exited non-zero but
        # somehow produced an ok-looking payload, force the error status so the
        # exit code is authoritative (never a silent pass).
        if proc.returncode != 0 and parsed.get("status") != "error":
            parsed.setdefault("status", "error")
            parsed.setdefault("returncode", proc.returncode)
        return parsed

    # No parseable JSON: surface a structured error carrying the raw streams so
    # the failure is debuggable, not swallowed.
    return {
        "status": "error",
        "action": action_name,
        "error": "Router produced no parseable JSON output.",
        "returncode": proc.returncode,
        "stdout": stdout[:2000],
        "stderr": (proc.stderr or "").strip()[:2000],
    }
