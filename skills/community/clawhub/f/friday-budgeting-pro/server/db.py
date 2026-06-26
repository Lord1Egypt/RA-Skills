"""
server/db.py — Thin SQLite connection helper for Friday Budgeting Pro.

No ORM. Plain sqlite3 stdlib only.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path


def get_db(path: str | Path) -> sqlite3.Connection:
    """Return a sqlite3.Connection with sane defaults.

    - row_factory = sqlite3.Row  (column access by name)
    - PRAGMA foreign_keys = ON   (enforce FK constraints)
    """
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: str | Path) -> None:
    """Initialise (or migrate) the database at *path* using db/schema.sql.

    Idempotent — the schema uses IF NOT EXISTS throughout, so calling this
    on an already-initialised database is safe.

    Migrations
    ----------
    After the base schema is applied, any ALTER TABLE migrations needed for
    columns added after the initial schema are run here.  Each migration is
    guarded so it is a no-op if the column already exists.
    """
    import time as _time

    path = Path(path)
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    sql = schema_path.read_text()

    conn = get_db(path)
    try:
        conn.executescript(sql)
        conn.commit()

        # Seed default classification_rules if none exist yet
        default_count = conn.execute(
            "SELECT COUNT(*) FROM classification_rules WHERE is_default = 1"
        ).fetchone()[0]
        if default_count == 0:
            import uuid as _uuid

            now = int(_time.time())
            _DEFAULT_RULES = [
                (
                    1,
                    "Pending skip",
                    "Skip any transaction that is still pending",
                    "skip",
                ),
                (
                    10,
                    "Internal transfer",
                    "If the same amount leaves one account and arrives at another of mine within 3 days, mark both as Transfer",
                    "transfer",
                ),
                (
                    20,
                    "Investment contribution",
                    "Outflows to Wealthsimple, Questrade, or any investment platform are Transfer/Savings, not spending",
                    "transfer",
                ),
                (
                    30,
                    "Credit card payment",
                    "A payment from chequing that matches a credit card balance is a Transfer — the individual charges are already tracked",
                    "transfer",
                ),
                (
                    40,
                    "Salary/payroll",
                    "Transactions tagged as payroll or salary by the bank are Income",
                    "income",
                ),
                (
                    50,
                    "Bank fees",
                    "Monthly account fees and bank charges are Bank Fees",
                    "spending",
                ),
            ]
            for priority, name, description, rule_type in _DEFAULT_RULES:
                conn.execute(
                    "INSERT INTO classification_rules "
                    "(id, name, description, rule_type, line_item_id, priority, is_default, enabled, created_at) "
                    "VALUES (?, ?, ?, ?, NULL, ?, 1, 1, ?)",
                    (str(_uuid.uuid4()), name, description, rule_type, priority, now),
                )
            conn.commit()

        # Migration: bank_accounts.description (added in #127)
        ba_cols = {row[1] for row in conn.execute("PRAGMA table_info(bank_accounts)")}
        if "description" not in ba_cols:
            conn.execute("ALTER TABLE bank_accounts ADD COLUMN description TEXT")
            conn.commit()

        # Migration: user_id columns (#131 — multi-profile support)
        # These are guarded so they are no-ops if the column already exists.
        _add_col_if_missing(conn, "bank_connections", "user_id", "TEXT")

        # Migration: plaid_env (#40 — sandbox vs production env separation)
        _add_col_if_missing(
            conn, "bank_connections", "plaid_env", "TEXT NOT NULL DEFAULT 'sandbox'"
        )

        # Migration: last_alerted_at (#35 — proactive re-auth alerts)
        _add_col_if_missing(conn, "bank_connections", "last_alerted_at", "INTEGER")
        _add_col_if_missing(conn, "ledgers", "user_id", "TEXT")
        _add_col_if_missing(conn, "classification_hints", "user_id", "TEXT")
        _add_col_if_missing(conn, "sessions", "user_id", "TEXT")

        # Migration: ledger types + description (#174)
        _add_col_if_missing(conn, "ledgers", "type", "TEXT NOT NULL DEFAULT 'personal'")
        _add_col_if_missing(conn, "ledgers", "description", "TEXT")

        # Migration: bank_accounts default_ledger_id (#174)
        _add_col_if_missing(conn, "bank_accounts", "default_ledger_id", "TEXT")

        # Migration: line_items item_type (#174)
        _add_col_if_missing(conn, "line_items", "item_type", "TEXT NOT NULL DEFAULT 'expense'")

        # Migration: users.home_currency (#159)
        _add_col_if_missing(conn, "users", "home_currency", "TEXT")
        conn.execute("UPDATE users SET home_currency = 'CAD' WHERE home_currency IS NULL")
        conn.commit()

        # Migration: users.timezone (#161)
        _add_col_if_missing(conn, "users", "timezone", "TEXT")
        conn.execute("UPDATE users SET timezone = 'America/Toronto' WHERE timezone IS NULL")
        conn.commit()

        # Migration: multi-currency (#160)
        _add_col_if_missing(conn, "bank_accounts", "currency", "TEXT")
        conn.execute("UPDATE bank_accounts SET currency = 'CAD' WHERE currency IS NULL")
        _add_col_if_missing(conn, "transactions", "currency", "TEXT")
        conn.execute("UPDATE transactions SET currency = 'CAD' WHERE currency IS NULL")
        conn.commit()

        # Migration: authorized_datetime for time-accurate ordering
        _add_col_if_missing(conn, "transactions", "authorized_datetime", "TEXT")
        conn.commit()

        # Migration: natural-language corrections (#173)
        _add_col_if_missing(conn, "transaction_entries", "source", "TEXT")
        _add_col_if_missing(conn, "transaction_entries", "corrected_from_line_item_id", "TEXT")
        _add_col_if_missing(conn, "transaction_entries", "corrected_at", "INTEGER")
        conn.commit()

        # Migration: plaid_config table — per-user Plaid credentials stored in DB.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plaid_config (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id),
                client_id TEXT NOT NULL,
                secret TEXT NOT NULL,
                plaid_env TEXT NOT NULL DEFAULT 'production',
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
                UNIQUE(user_id)
            )
        """)
        conn.commit()

        # Migration: setup_interview (#206 — guided onboarding answers).
        # Stores answers from the personalisation interview keyed by
        # (user_id, question_key).  Idempotent on (user_id, question_key)
        # so re-answering the same question replaces the previous value.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS setup_interview (
                id           TEXT PRIMARY KEY,
                user_id      TEXT,
                question_key TEXT NOT NULL,
                answer_text  TEXT NOT NULL,
                created_at   INTEGER NOT NULL,
                updated_at   INTEGER NOT NULL,
                UNIQUE(user_id, question_key)
            )
            """)
        conn.commit()

        # Migration: create default user only when there is existing data to migrate
        # (i.e. rows exist that need a user_id) but no users have been created yet.
        # On truly fresh DBs, we leave users empty so the setup wizard can create
        # the first user with a real username and password.
        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count == 0:
            # Check if any existing rows need migration
            existing_data = (
                conn.execute("SELECT COUNT(*) FROM bank_connections").fetchone()[0] > 0
                or conn.execute("SELECT COUNT(*) FROM ledgers").fetchone()[0] > 0
                or conn.execute("SELECT COUNT(*) FROM classification_hints").fetchone()[0] > 0
                or conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] > 0
            )

            # Also check if app_config has a password hash (old single-user DB)
            legacy_hash: str | None = None
            try:
                row = conn.execute(
                    "SELECT ui_password_hash FROM app_config WHERE id = 1"
                ).fetchone()
                if row and row[0]:
                    legacy_hash = row[0]
            except Exception:
                pass

            if existing_data or legacy_hash is not None:
                # This is a legacy single-user DB — create the default user.
                default_user_id = "default-user-id"
                now = int(_time.time())

                if legacy_hash is None:
                    # Has data but no password hash — use a non-verifiable placeholder.
                    import secrets as _secrets

                    from argon2 import PasswordHasher as _PH

                    legacy_hash = _PH().hash(_secrets.token_hex(32))

                conn.execute(
                    "INSERT INTO users (id, username, password_hash, created_at) "
                    "VALUES (?, ?, ?, ?)",
                    (default_user_id, "default", legacy_hash, now),
                )
                conn.commit()

                # Backfill NULL user_id on all existing rows.
                for table in ("bank_connections", "ledgers", "classification_hints", "sessions"):
                    conn.execute(
                        f"UPDATE {table} SET user_id = ? WHERE user_id IS NULL",
                        (default_user_id,),
                    )
                conn.commit()
            # else: fresh DB, no migration needed — setup wizard creates the first user.
        else:
            # Users already exist — backfill any rows that slipped through without a user_id.
            default_user_row = conn.execute(
                "SELECT id FROM users ORDER BY created_at LIMIT 1"
            ).fetchone()
            if default_user_row:
                first_uid = default_user_row["id"]
                for table in ("bank_connections", "ledgers", "classification_hints", "sessions"):
                    conn.execute(
                        f"UPDATE {table} SET user_id = ? WHERE user_id IS NULL",
                        (first_uid,),
                    )
                conn.commit()
    finally:
        conn.close()


def _add_col_if_missing(conn: sqlite3.Connection, table: str, col: str, col_type: str) -> None:
    """ALTER TABLE to add *col* if it is not already present."""
    existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if col not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
        conn.commit()


@contextmanager
def transaction(conn: sqlite3.Connection):
    """Context manager that commits on success and rolls back on any exception.

    Usage::

        with transaction(conn):
            conn.execute("INSERT INTO ...")
    """
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
