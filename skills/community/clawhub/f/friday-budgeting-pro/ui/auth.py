"""
ui/auth.py — Auth helpers for Friday Budgeting Pro UI.

Implements:
  - argon2id password hashing via argon2-cffi
  - Multi-profile user management (users table)
  - Permanent sessions (persist until explicit logout — no idle expiry)
  - No login rate limiting (single-user local app per d4403c0)
"""

from __future__ import annotations

import secrets
import time
import uuid
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import Request

from server.db import get_db

# ── Session cookie name ────────────────────────────────────────────────────
SESSION_COOKIE = "friday_bp_session"

# ── argon2id hasher (sensible defaults from argon2-cffi) ──────────────────
_ph = PasswordHasher()


# ── Time helper ──────────────────────────────────────────────────────────


def _now() -> int:
    """Return the current Unix timestamp as an integer."""
    return int(time.time())


# ── Password helpers ──────────────────────────────────────────────────────


def hash_password(plaintext: str) -> str:
    """Hash *plaintext* with argon2id and return the encoded hash string."""
    return _ph.hash(plaintext)


def verify_password(plaintext: str, stored_hash: str) -> bool:
    """Return True if *plaintext* matches *stored_hash*."""
    try:
        return _ph.verify(stored_hash, plaintext)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


# ── User helpers ──────────────────────────────────────────────────────────


def create_user(db_path, username: str, password_plaintext: str) -> str:
    """Create a new user and return the new user_id.

    Raises ValueError if the username is already taken.
    """
    user_id = str(uuid.uuid4())
    password_hash = hash_password(password_plaintext)
    now = _now()
    conn = get_db(db_path)
    try:
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            raise ValueError(f"Username {username!r} is already taken")
        conn.execute(
            "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (user_id, username, password_hash, now),
        )
        conn.commit()
    finally:
        conn.close()
    return user_id


def get_user_by_username(db_path, username: str) -> Optional[dict]:
    """Return the user row as a dict, or None if not found."""
    conn = get_db(db_path)
    try:
        row = conn.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(db_path, user_id: str) -> Optional[dict]:
    """Return the user row as a dict, or None if not found."""
    conn = get_db(db_path)
    try:
        row = conn.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_users(db_path) -> list[dict]:
    """Return all users as a list of dicts (no password_hash)."""
    conn = get_db(db_path)
    try:
        rows = conn.execute(
            "SELECT id, username, created_at FROM users ORDER BY created_at"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_user(db_path, user_id: str) -> None:
    """Delete a user and all their associated data.

    Deletes: bank_connections (+ cascade via FK), ledgers, classification_hints,
    sessions for this user.
    """
    conn = get_db(db_path)
    try:
        # Get connection ids for cascade
        conn_ids = [
            r["id"]
            for r in conn.execute(
                "SELECT id FROM bank_connections WHERE user_id = ?", (user_id,)
            ).fetchall()
        ]
        for cid in conn_ids:
            conn.execute("DELETE FROM sync_cursors WHERE connection_id = ?", (cid,))

        # Delete accounts for user's connections
        if conn_ids:
            placeholders = ",".join("?" * len(conn_ids))
            account_ids = [
                r["id"]
                for r in conn.execute(
                    f"SELECT id FROM bank_accounts WHERE connection_id IN ({placeholders})",
                    conn_ids,
                ).fetchall()
            ]
            if account_ids:
                acc_placeholders = ",".join("?" * len(account_ids))
                txn_ids = [
                    r["id"]
                    for r in conn.execute(
                        f"SELECT id FROM transactions WHERE bank_account_id IN ({acc_placeholders})",
                        account_ids,
                    ).fetchall()
                ]
                if txn_ids:
                    txn_placeholders = ",".join("?" * len(txn_ids))
                    conn.execute(
                        f"DELETE FROM transaction_entries WHERE transaction_id IN ({txn_placeholders})",
                        txn_ids,
                    )
                    conn.execute(
                        f"DELETE FROM transactions WHERE id IN ({txn_placeholders})",
                        txn_ids,
                    )
                conn.execute(
                    f"DELETE FROM bank_accounts WHERE connection_id IN ({placeholders})",
                    conn_ids,
                )
            conn.execute(
                f"DELETE FROM bank_connections WHERE id IN ({placeholders})",
                conn_ids,
            )

        # Delete user's ledgers and line items
        ledger_ids = [
            r["id"]
            for r in conn.execute("SELECT id FROM ledgers WHERE user_id = ?", (user_id,)).fetchall()
        ]
        if ledger_ids:
            l_placeholders = ",".join("?" * len(ledger_ids))
            conn.execute(
                f"DELETE FROM line_items WHERE ledger_id IN ({l_placeholders})",
                ledger_ids,
            )
            conn.execute(
                f"DELETE FROM ledgers WHERE id IN ({l_placeholders})",
                ledger_ids,
            )

        # Delete classification hints
        conn.execute("DELETE FROM classification_hints WHERE user_id = ?", (user_id,))

        # Delete sessions
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))

        # Finally delete the user
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))

        conn.commit()
    finally:
        conn.close()


def update_user_password(db_path, user_id: str, new_password: str) -> None:
    """Update the password hash for a user."""
    new_hash = hash_password(new_password)
    conn = get_db(db_path)
    try:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_hash, user_id),
        )
        conn.commit()
    finally:
        conn.close()


def has_any_user(db_path) -> bool:
    """Return True if at least one user exists in the users table."""
    conn = get_db(db_path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        return count > 0
    finally:
        conn.close()


# ── Session helpers ───────────────────────────────────────────────────────


def create_session(db_path, user_agent: Optional[str] = None, user_id: Optional[str] = None) -> str:
    """Insert a new session row and return the session token.

    Sessions are permanent — they persist until explicitly deleted via
    delete_session (logout). No expiry is enforced.
    """
    token = secrets.token_hex(32)
    now = _now()
    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO sessions (id, created_at, last_seen_at, expires_at, user_agent, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (token, now, now, 0, user_agent, user_id),
        )
        conn.commit()
    finally:
        conn.close()
    return token


def delete_session(db_path, token: str) -> None:
    """Remove a session row (logout)."""
    conn = get_db(db_path)
    try:
        conn.execute("DELETE FROM sessions WHERE id = ?", (token,))
        conn.commit()
    finally:
        conn.close()


def check_session(request: Request, db_path) -> bool:
    """Return True if the request carries a valid session cookie.

    Sessions are permanent — no expiry check. Updates last_seen_at as a
    record-keeping touch only.
    """
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return False
    conn = get_db(db_path)
    try:
        row = conn.execute("SELECT id FROM sessions WHERE id = ?", (token,)).fetchone()
        if row is None:
            return False
        now = _now()
        conn.execute(
            "UPDATE sessions SET last_seen_at = ? WHERE id = ?",
            (now, token),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_session_user_id(request: Request, db_path) -> Optional[str]:
    """Return the user_id for the session in *request*, or None."""
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    conn = get_db(db_path)
    try:
        row = conn.execute("SELECT user_id FROM sessions WHERE id = ?", (token,)).fetchone()
        return row["user_id"] if row else None
    except Exception:
        return None
    finally:
        conn.close()


def get_active_user_id(db_path) -> Optional[str]:
    """Return the user_id of the most recently active session, or the first user.

    Used by MCP tools (no HTTP context) to find the current logged-in user.
    Falls back to the first user in the DB if no active session exists.
    """
    conn = get_db(db_path)
    try:
        row = conn.execute(
            "SELECT user_id FROM sessions ORDER BY last_seen_at DESC LIMIT 1"
        ).fetchone()
        if row and row["user_id"]:
            return row["user_id"]
        # Fallback: first user
        row2 = conn.execute("SELECT id FROM users ORDER BY created_at LIMIT 1").fetchone()
        return row2["id"] if row2 else None
    finally:
        conn.close()


# ── Recovery token store (shared with MCP tools) ────────────────────────────
# Maps token -> (user_id, expiry_float).  In-memory; tokens do not survive
# daemon restarts, which is acceptable for a local single-user app.

_recovery_tokens: dict[str, tuple[str, float]] = {}
_RECOVERY_TOKEN_TTL: int = 600  # 10 minutes


def add_recovery_token(token: str, user_id: str) -> None:
    """Register *token* → *user_id* in the in-memory recovery-token store.

    The token expires after ``_RECOVERY_TOKEN_TTL`` seconds.  This helper
    is shared by the UI POST /forgot handler and the MCP
    ``reset_ui_password`` tool so both operate on the same in-memory map.
    """
    import time as _time_mod

    expiry = _time_mod.time() + _RECOVERY_TOKEN_TTL
    _recovery_tokens[token] = (user_id, expiry)


# ── Legacy app_config helpers (kept for backward compat) ─────────────────
# These delegate to the users table when a user exists, otherwise fall back
# to the app_config table.  New code should use the user-centric helpers
# above.


def get_password_hash(db_path) -> Optional[str]:
    """Return the stored UI password hash, or None if not yet set.

    Reads from the users table (first user) or falls back to app_config.
    """
    conn = get_db(db_path)
    try:
        # Prefer users table
        row = conn.execute("SELECT password_hash FROM users ORDER BY created_at LIMIT 1").fetchone()
        if row and row[0]:
            return row[0]
        # Legacy fallback
        try:
            row2 = conn.execute("SELECT ui_password_hash FROM app_config WHERE id = 1").fetchone()
            if row2 and row2[0]:
                return row2[0]
        except Exception:
            pass
        return None
    finally:
        conn.close()


def set_password_hash(db_path, hashed: str) -> None:
    """Upsert the UI password hash.

    Updates the first user's hash if users exist; otherwise writes to
    app_config for legacy compatibility.
    """
    now = _now()
    conn = get_db(db_path)
    try:
        row = conn.execute("SELECT id FROM users ORDER BY created_at LIMIT 1").fetchone()
        if row:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (hashed, row["id"]),
            )
            conn.commit()
        else:
            # Legacy: write to app_config
            conn.execute(
                "INSERT INTO app_config (id, ui_password_hash, ui_password_set_at) "
                "VALUES (1, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET ui_password_hash=excluded.ui_password_hash, "
                "ui_password_set_at=excluded.ui_password_set_at",
                (hashed, now),
            )
            conn.commit()
    finally:
        conn.close()
