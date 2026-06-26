"""
tests/ui/_server_runner.py — thin wrapper that starts ui.server via uvicorn
with an isolated temp directory (FRIDAY_BP_APP_DIR) and a pre-seeded test DB.

Called by the conftest server_url fixture as a subprocess so that each
Playwright test session gets a fresh, isolated SQLite database that never
touches ~/.friday-bp/.

Seeded data:
  - User: username='testuser', password='testpass'
  - Ledger: 'Personal' with standard Income + Expense line items
  - 10 sample transactions

Usage (automated — do not call directly):
    FRIDAY_BP_APP_DIR=/tmp/... FRIDAY_BP_UI_PORT=<PORT> python -m tests.ui._server_runner
"""

from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

# ── Set FRIDAY_BP_APP_DIR BEFORE importing any server modules ──────────────
_app_dir_env = os.environ.get("FRIDAY_BP_APP_DIR")
if _app_dir_env:
    _app_dir = Path(_app_dir_env)
    _app_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    (_app_dir / "exports").mkdir(mode=0o700, parents=True, exist_ok=True)

# Now import server.paths — it will pick up FRIDAY_BP_APP_DIR automatically.
import server.paths as _paths  # noqa: E402
from server.db import get_db, init_db  # noqa: E402

# ── Initialise DB ──────────────────────────────────────────────────────────
_db = _paths.DB_PATH
init_db(_db)


# ── Seed test data ─────────────────────────────────────────────────────────


def _seed():
    """Seed testuser + Personal ledger + 10 sample transactions."""
    conn = get_db(_db)
    try:
        # Check if testuser already exists (idempotent)
        existing = conn.execute("SELECT id FROM users WHERE username = 'testuser'").fetchone()
        if existing:
            return

        now = int(time.time())

        # ── User ──────────────────────────────────────────────────────────
        from argon2 import PasswordHasher

        _ph = PasswordHasher()
        password_hash = _ph.hash("testpass")
        user_id = "test-user-001"

        conn.execute(
            "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (user_id, "testuser", password_hash, now),
        )

        # Also update app_config for legacy compat
        try:
            conn.execute("ALTER TABLE app_config ADD COLUMN username TEXT")
        except Exception:
            pass
        try:
            conn.execute("ALTER TABLE app_config ADD COLUMN ui_password_hash TEXT")
        except Exception:
            pass
        conn.execute(
            "INSERT INTO app_config (id, username, ui_password_hash) VALUES (1, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET username=excluded.username, ui_password_hash=excluded.ui_password_hash",
            ("testuser", password_hash),
        )

        # ── Personal ledger ───────────────────────────────────────────────
        ledger_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "Personal", user_id),
        )

        # Standard line items
        income_items = ["Salary", "Freelance", "Other Income"]
        expense_items = [
            "Rent / Mortgage",
            "Groceries",
            "Utilities",
            "Transport",
            "Dining Out",
            "Entertainment",
            "Healthcare",
        ]

        for name in income_items:
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), ledger_id, name, "income"),
            )
        for name in expense_items:
            conn.execute(
                "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), ledger_id, name, "expense"),
            )

        conn.commit()
    finally:
        conn.close()


_seed()


# ── Start uvicorn ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("FRIDAY_BP_UI_PORT", "6789"))
    uvicorn.run("ui.server:app", host="127.0.0.1", port=port, log_level="warning")
