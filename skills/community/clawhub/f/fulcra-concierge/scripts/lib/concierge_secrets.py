"""Shared secret loading for the Fulcra concierge skills.

Resolution order for any key:
  1. Environment variable (e.g. ATTIO_API_KEY) -- wins, good for CI / one-offs.
  2. ~/.fulcra-concierge/secrets.json -- the persistent local store.

Secrets are never printed. Skills read keys through `get_secret`; they should
not open secrets.json themselves. Keeping one loader means one place to harden
(file perms, future keychain support) instead of N copies across skills.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

SECRETS_PATH = Path(os.environ.get("FULCRA_CONCIERGE_HOME", Path.home() / ".fulcra-concierge")) / "secrets.json"


def _load_file() -> dict:
    try:
        with open(SECRETS_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_secret(name: str, *, required: bool = False) -> str | None:
    """Return a secret by name. Env var beats the file. Returns None if absent
    (unless required=True, which raises with a fix-it hint -- never echoing any
    partial value)."""
    val = os.environ.get(name)
    if not val:
        val = _load_file().get(name)
    if val:
        return str(val).strip()
    if required:
        raise SystemExit(
            f"Missing secret {name!r}. Set the {name} environment variable, or add it to "
            f"{SECRETS_PATH} as {{\"{name}\": \"...\"}}."
        )
    return None


def set_secret(name: str, value: str) -> None:
    """Persist a secret into secrets.json (merging with any existing keys) and
    lock the file down to the current user. Used by setup helpers, not skills."""
    SECRETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = _load_file()
    data[name] = value
    # Write atomically-ish and restrict perms before writing the value.
    tmp = SECRETS_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, SECRETS_PATH)


def has_secret(name: str) -> bool:
    return bool(get_secret(name))
