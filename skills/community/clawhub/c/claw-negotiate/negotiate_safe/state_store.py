"""Persistent pointer for two-party founder resume.

P7-5: when the founder binds a group but the investor hasn't joined yet,
the founder's ``run_safe.py`` exits cleanly (OpenClaw reaps long-lived
foreground execs). A tiny JSON pointer on disk lets a later ``scan``
invocation — fired by an OpenClaw cron job — re-open the negotiation:

* ``output_dir`` locates mint.json + config.json already written at mint
* ``session_code`` is the lookup key for sshsign
* ``negotiation_id`` is the local file-naming key

Everything else (session status, member list, founder_resumed_at,
founder_streaming_at, group_chat_id, investor handle) lives on sshsign.
This file is a **pointer**, not a cache — sshsign is the source of truth.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

_REQUIRED_FIELDS = ("negotiation_id", "output_dir", "session_code")
_DEFAULT_DIR = Path.home() / ".openclaw" / "skill-state" / "negotiate_safe"


class StateCorruptError(Exception):
    """Raised when a state file is unreadable or fails schema validation."""


def state_dir() -> Path:
    override = os.environ.get("CLAW_NEGOTIATE_STATE_DIR")
    return Path(override) if override else _DEFAULT_DIR


def state_path(negotiation_id: str) -> Path:
    d = state_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{negotiation_id}.json"


def write_state(payload: dict) -> None:
    """Atomically write a state pointer.

    Uses tempfile + os.replace so a crash mid-write leaves the prior
    file (or no file) intact. Validates required fields up front so a
    caller that forgets a field fails loudly at write-time, not
    silently at read-time.
    """
    missing = [k for k in _REQUIRED_FIELDS if k not in payload]
    if missing:
        raise StateCorruptError(
            f"state payload missing required fields: {missing}"
        )
    negotiation_id = payload["negotiation_id"]
    target = state_path(negotiation_id)
    # NamedTemporaryFile in the same dir ensures os.replace stays atomic
    # (it requires src and dst on the same filesystem).
    fd, tmp = tempfile.mkstemp(
        prefix=f".{negotiation_id}.", suffix=".tmp", dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(payload, fh)
        os.replace(tmp, target)
    except Exception:
        # Best-effort cleanup; target is untouched either way.
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


def read_state(negotiation_id: str) -> dict | None:
    """Return the parsed payload, or None when the file is absent.

    Raises StateCorruptError on any other read/parse/validation
    failure. Missing is a normal operational state (no state for this
    id); corruption is not, and silently treating it as missing would
    hide real bugs.
    """
    p = state_path(negotiation_id)
    try:
        raw = p.read_text()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise StateCorruptError(f"unable to read {p}: {exc}") from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise StateCorruptError(f"invalid JSON in {p}: {exc}") from exc
    if not isinstance(payload, dict):
        raise StateCorruptError(f"{p}: expected object, got {type(payload).__name__}")
    missing = [k for k in _REQUIRED_FIELDS if k not in payload]
    if missing:
        raise StateCorruptError(f"{p}: missing required fields {missing}")
    return payload


def list_active() -> list[dict]:
    """Return every readable state pointer under the state dir.

    Corrupt files are skipped (not raised) so a single bad pointer
    doesn't halt the whole scan — the corrupt one surfaces when its
    negotiation_id is looked up directly.
    """
    d = state_dir()
    if not d.exists():
        return []
    out: list[dict] = []
    for entry in sorted(d.iterdir()):
        if not entry.name.endswith(".json") or entry.name.startswith("."):
            continue
        negotiation_id = entry.name[:-5]
        try:
            payload = read_state(negotiation_id)
        except StateCorruptError:
            continue
        if payload is not None:
            out.append(payload)
    return out


def delete_state(negotiation_id: str) -> None:
    """Remove a state pointer. No-op if already absent."""
    p = state_path(negotiation_id)
    try:
        p.unlink()
    except FileNotFoundError:
        pass
