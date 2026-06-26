"""State file paths + load/save/age helpers for the AC skill."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path.home() / ".activecampaign-skill"
STATE_FILE = STATE_DIR / "state.json"
HISTORY_FILE = STATE_DIR / "history.jsonl"
INSIGHTS_FILE = STATE_DIR / "insights.md"


def _ensure_state_dir() -> None:
    """Create the state directory with restricted permissions."""
    if not STATE_DIR.exists():
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(STATE_DIR, 0o700)


def load_state() -> dict | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def state_age_days() -> float | None:
    state = load_state()
    if not state or "last_calibrated" not in state:
        return None
    try:
        cal = datetime.fromisoformat(state["last_calibrated"])
        if cal.tzinfo is None:
            cal = cal.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - cal).total_seconds() / 86400
    except (ValueError, TypeError):
        return None


def ensure_state(max_age_days: int = 30) -> dict:
    state = load_state()
    if state is None:
        sys.stderr.write(
            "ERROR: State file not found.\n"
            "\n"
            "Set AC_API_URL and AC_API_TOKEN, then run calibration:\n"
            "  python3 scripts/calibrate.py --validate   # check creds\n"
            "  python3 scripts/calibrate.py              # build state.json\n"
            "\n"
            "See INSTALL.md for credential setup options.\n"
        )
        sys.exit(1)
    age = state_age_days()
    if age is not None and age > max_age_days:
        sys.stderr.write(
            f"WARNING: State file is {age:.0f} days old "
            f"(calibrated {age:.0f} days ago). "
            "Results may not reflect recent account changes.\n"
            "  Recalibrate: python3 scripts/calibrate.py\n"
        )
    return state


def save_state(state: dict) -> None:
    _ensure_state_dir()
    fd, tmp_path = tempfile.mkstemp(dir=STATE_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(state, f, indent=2)
        os.chmod(tmp_path, 0o600)
        os.replace(tmp_path, STATE_FILE)
    except BaseException:
        os.unlink(tmp_path)
        raise


def env_or_die(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        sys.stderr.write(f"ERROR: {key} environment variable not set.\n")
        sys.exit(1)
    return val
