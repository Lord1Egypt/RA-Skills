"""
Shared utility functions for the backtest-poller skill.
"""
import fcntl
import json
import os
import logging
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger("backtest_poller")


def parse_equity(raw) -> Optional[float]:
    """Parse equity string like '$12,345.67' -> 12345.67"""
    if raw is None:
        return None
    s = str(raw).strip().replace(',', '').replace('$', '')
    try:
        return float(s)
    except ValueError:
        return None


def parse_pct(raw) -> Optional[float]:
    """Parse percentage string to decimal.

    QC API returns a fixed format like "XX.XX%" (e.g. "40.20%").
    Always strip '%' then divide by 100 to remove ambiguity.

    "40.20%" -> 0.402
    "0.50%"  -> 0.005
    "1.00%"  -> 0.01
    None     -> None
    """
    if raw is None:
        return None
    s = str(raw).strip().rstrip('%').strip()
    try:
        val = float(s)
        return val / 100.0
    except ValueError:
        return None


@contextmanager
def state_file_lock(state_file_path: str):
    """Exclusive file lock context manager for state.json.
    Prevents CLI and poller from writing simultaneously.

    Usage:
        with state_file_lock(STATE_FILE):
            state = load_state_unlocked(STATE_FILE)
            state["backtests"].append(...)
            save_state_unlocked(state, STATE_FILE)
    """
    lock_path = state_file_path + ".lock"
    lock_fd = open(lock_path, 'w')
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()


def load_state_unlocked(state_file_path: str) -> dict:
    """Read state.json (caller must hold lock)."""
    if os.path.exists(state_file_path):
        try:
            with open(state_file_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to parse state.json: {e}")
    return {"backtests": [], "poller_pid": None, "poller_running": False}


def save_state_unlocked(state: dict, state_file_path: str):
    """Atomic write to state.json (caller must hold lock)."""
    tmp = state_file_path + ".tmp"
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False, default=str)
    os.replace(tmp, state_file_path)
