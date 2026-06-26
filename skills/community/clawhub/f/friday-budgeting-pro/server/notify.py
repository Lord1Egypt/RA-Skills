"""
server/notify.py — Notification dispatcher for Friday Budgeting Pro.

Design (Architecture § Design Constraint #10)
---------------------------------------------
Two notification paths with automatic fallback, priority-ordered by the user's
preferred notification channel stored in app_config.notification_channel.

Supported channels (in fallback order):
  "openclaw_chat"  → OpenClaw local HTTP API → macOS Notification Center → in-UI banner
  "macos"          → macOS Notification Center → in-UI banner
  "in_ui"          → in-UI banner only

Every call persists a row in the ``notifications`` table so the UI can always
display a banner regardless of delivery outcome.

External dependencies: stdlib only (urllib.request, subprocess, uuid, time, sqlite3).
"""

import os
import sqlite3
import subprocess
import time
import uuid
from urllib import request
from urllib.error import URLError

# Default base URL for the OpenClaw local messaging API.
# Override via OPENCLAW_NOTIFY_URL env var.
_DEFAULT_OPENCLAW_NOTIFY_URL = "http://127.0.0.1:7531/v1/messages"

# Path to the SQLite database, same convention as server/db.py.
_DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "friday.db"))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _get_preferred_channel(conn: sqlite3.Connection) -> str:
    """Return the user's preferred notification channel, defaulting to 'in_ui'."""
    row = conn.execute("SELECT notification_channel FROM app_config WHERE id = 1").fetchone()
    if row and row["notification_channel"]:
        return row["notification_channel"]
    return "in_ui"


def _try_openclaw_chat(message: str, urgency: str) -> bool:
    """
    POST {message, urgency} to the OpenClaw local API.
    Returns True on success, False on any error.
    """
    import json

    url = os.environ.get("OPENCLAW_NOTIFY_URL", _DEFAULT_OPENCLAW_NOTIFY_URL)
    payload = json.dumps({"message": message, "urgency": urgency}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=5) as resp:
            return resp.status < 400
    except (URLError, OSError):
        return False


def _try_macos_notification(message: str) -> bool:
    """
    Send a macOS Notification Center alert via osascript.
    Returns True on success, False on any error.
    """
    script = f'display notification {json_escape(message)} with title "Friday Budgeting Pro"'
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def json_escape(s: str) -> str:
    """Minimal JSON string quoting so we can embed text safely in AppleScript."""
    import json

    return json.dumps(s)


def _write_notification_row(
    conn: sqlite3.Connection,
    notification_id: str,
    message: str,
    urgency: str,
    delivered_via: str,
) -> None:
    """Persist the notification to the notifications table."""
    conn.execute(
        """
        INSERT INTO notifications (id, message, urgency, created_at, delivered_via, read)
        VALUES (?, ?, ?, ?, ?, 0)
        """,
        (notification_id, message, urgency, int(time.time()), delivered_via),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def send(message: str, urgency: str = "normal") -> dict:
    """
    Send a notification via the user's preferred channel with automatic fallback.

    Parameters
    ----------
    message : str
        Human-readable notification text.
    urgency : str
        Severity hint: "normal" (default) or "high".

    Returns
    -------
    dict
        {
            "delivered_via": "openclaw_chat" | "macos" | "in_ui",
            "notification_id": str,   # UUID4
        }

    Fallback order by preferred channel
    ------------------------------------
    "openclaw_chat"  → openclaw_chat → macos → in_ui
    "macos"          → macos → in_ui
    "in_ui"          → in_ui (only)
    """
    notification_id = str(uuid.uuid4())
    delivered_via: str = "in_ui"  # safe default — always succeeds

    with _get_db() as conn:
        preferred = _get_preferred_channel(conn)

        if preferred == "openclaw_chat":
            if _try_openclaw_chat(message, urgency):
                delivered_via = "openclaw_chat"
            elif _try_macos_notification(message):
                delivered_via = "macos"
            else:
                delivered_via = "in_ui"

        elif preferred == "macos":
            if _try_macos_notification(message):
                delivered_via = "macos"
            else:
                delivered_via = "in_ui"

        else:  # "in_ui" or unknown preference
            delivered_via = "in_ui"

        # Always persist — the UI banner depends on this row.
        _write_notification_row(conn, notification_id, message, urgency, delivered_via)

    return {
        "delivered_via": delivered_via,
        "notification_id": notification_id,
    }
