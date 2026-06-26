"""Local idempotency records for Telegram projection.

The shared source of truth is sshsign history/session state. Delivery records
are local because each bot identity is responsible for projecting only its own
cards. If a process crashes after sshsign records an offer but before Telegram
delivery, the next reconcile sees the missing local delivery key and sends it.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


_DEFAULT_DIR = Path.home() / ".openclaw" / "skill-state" / "negotiate_safe" / "deliveries"


def delivery_dir() -> Path:
    override = os.environ.get("CLAW_NEGOTIATE_DELIVERY_DIR")
    return Path(override) if override else _DEFAULT_DIR


def delivery_path(session_id: str) -> Path:
    d = delivery_dir()
    d.mkdir(parents=True, exist_ok=True)
    safe = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in session_id)
    return d / f"{safe}.json"


def read_deliveries(session_id: str) -> dict:
    p = delivery_path(session_id)
    try:
        payload = json.loads(p.read_text())
    except FileNotFoundError:
        return {"session_id": session_id, "delivered": {}}
    except (OSError, json.JSONDecodeError):
        return {"session_id": session_id, "delivered": {}}
    if not isinstance(payload, dict):
        return {"session_id": session_id, "delivered": {}}
    delivered = payload.get("delivered")
    if not isinstance(delivered, dict):
        payload["delivered"] = {}
    return payload


def has_delivery(session_id: str, key: str) -> bool:
    payload = read_deliveries(session_id)
    return key in payload.get("delivered", {})


def mark_delivery(session_id: str, key: str, target: str, message_id: str | None = None) -> None:
    payload = read_deliveries(session_id)
    delivered = payload.setdefault("delivered", {})
    delivered[key] = {
        "target": str(target),
        "message_id": str(message_id) if message_id is not None else "",
    }
    target_path = delivery_path(session_id)
    fd, tmp = tempfile.mkstemp(
        prefix=f".{target_path.stem}.", suffix=".tmp", dir=str(target_path.parent),
    )
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(payload, fh, sort_keys=True)
        os.replace(tmp, target_path)
    except Exception:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
