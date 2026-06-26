#!/usr/bin/env python3
"""ClankerHive — shared context store for multi-session agent coordination.

SQLite-backed key/value facts (with TTL), alert queue, and task deduplication.
Designed for OpenClaw agents that run across cron jobs, heartbeats, sub-agents,
and interactive sessions.

Usage:
    clankerhive.py <command> [args] [options]

Environment:
    CLANKERHIVE_DB  Path to SQLite database (default: ~/.openclaw/hive.db)
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from typing import Optional

DB_PATH: str = os.environ.get("CLANKERHIVE_DB", os.path.expanduser("~/.openclaw/hive.db"))


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def _connect() -> sqlite3.Connection:
    """Return a WAL-mode SQLite connection, creating parent dirs as needed."""
    db_dir: str = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    db_exists: bool = os.path.exists(DB_PATH)
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH, timeout=5)
    if not db_exists:
        os.chmod(DB_PATH, 0o600)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def _init_db(conn: sqlite3.Connection) -> None:
    """Create tables if they do not already exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS active_facts (
            key        TEXT PRIMARY KEY,
            value      TEXT,
            expires_at INTEGER,
            created_at INTEGER NOT NULL,
            source     TEXT
        );

        CREATE TABLE IF NOT EXISTS pending_alerts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            topic      TEXT,
            payload    TEXT,
            created_at INTEGER NOT NULL,
            claimed_by TEXT,
            claimed_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS task_state (
            task_id    TEXT PRIMARY KEY,
            status     TEXT NOT NULL DEFAULT 'claimed',
            owner      TEXT,
            started_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL,
            result     TEXT
        );
    """)


def _prune_expired(conn: sqlite3.Connection) -> None:
    """Delete facts whose TTL has passed."""
    now: int = int(time.time())
    conn.execute(
        "DELETE FROM active_facts WHERE expires_at IS NOT NULL AND expires_at <= ?",
        (now,),
    )
    conn.commit()


def _db() -> sqlite3.Connection:
    """Return a ready-to-use connection (tables created, expired facts pruned)."""
    conn: sqlite3.Connection = _connect()
    _init_db(conn)
    _prune_expired(conn)
    return conn


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

def cmd_set(args: argparse.Namespace) -> None:
    """Set a key/value fact with an optional TTL in seconds."""
    conn: sqlite3.Connection = _db()
    now: int = int(time.time())
    expires: Optional[int] = now + args.ttl if args.ttl else None
    source: Optional[str] = args.source or None
    conn.execute(
        "INSERT OR REPLACE INTO active_facts (key, value, expires_at, created_at, source) VALUES (?, ?, ?, ?, ?)",
        (args.key, args.value, expires, now, source),
    )
    conn.commit()
    conn.close()
    print("ok")


def cmd_get(args: argparse.Namespace) -> None:
    """Print a fact's value, or nothing if missing or expired."""
    conn: sqlite3.Connection = _db()
    row = conn.execute(
        "SELECT value FROM active_facts WHERE key = ?", (args.key,)
    ).fetchone()
    conn.close()
    if row:
        print(row["value"])


def cmd_list(args: argparse.Namespace) -> None:
    """List all active (non-expired) facts as a JSON array."""
    conn: sqlite3.Connection = _db()
    if args.prefix:
        rows = conn.execute(
            "SELECT key, value, expires_at, created_at, source FROM active_facts "
            "WHERE key LIKE ? ORDER BY key",
            (args.prefix + "%",),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT key, value, expires_at, created_at, source FROM active_facts ORDER BY key"
        ).fetchall()
    conn.close()
    print(json.dumps([dict(r) for r in rows], indent=2))


def cmd_delete(args: argparse.Namespace) -> None:
    """Delete a fact by key. Prints 'ok' or 'not-found'."""
    conn: sqlite3.Connection = _db()
    cur = conn.execute("DELETE FROM active_facts WHERE key = ?", (args.key,))
    conn.commit()
    conn.close()
    if cur.rowcount:
        print("ok")
    else:
        print("not-found")


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------

def cmd_queue_alert(args: argparse.Namespace) -> None:
    """Queue an alert for another session to pick up."""
    conn: sqlite3.Connection = _db()
    now: int = int(time.time())
    conn.execute(
        "INSERT INTO pending_alerts (topic, payload, created_at) VALUES (?, ?, ?)",
        (args.topic, args.payload, now),
    )
    conn.commit()
    conn.close()
    print("ok")


def cmd_pop_alerts(args: argparse.Namespace) -> None:
    """Claim and return pending alerts as a JSON array."""
    conn: sqlite3.Connection = _db()
    claimer: str = args.claimer or f"pid-{os.getpid()}"
    now: int = int(time.time())

    if args.topic:
        rows = conn.execute(
            "SELECT id, topic, payload, created_at FROM pending_alerts "
            "WHERE claimed_by IS NULL AND topic = ? ORDER BY id",
            (args.topic,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, topic, payload, created_at FROM pending_alerts "
            "WHERE claimed_by IS NULL ORDER BY id"
        ).fetchall()

    out = []
    for r in rows:
        conn.execute(
            "UPDATE pending_alerts SET claimed_by = ?, claimed_at = ? WHERE id = ?",
            (claimer, now, r["id"]),
        )
        out.append(dict(r))

    conn.commit()
    conn.close()
    print(json.dumps(out, indent=2))


def cmd_list_alerts(args: argparse.Namespace) -> None:  # noqa: ARG001
    """List unclaimed alerts as a JSON array without claiming them."""
    conn: sqlite3.Connection = _db()
    rows = conn.execute(
        "SELECT id, topic, payload, created_at FROM pending_alerts "
        "WHERE claimed_by IS NULL ORDER BY id"
    ).fetchall()
    conn.close()
    print(json.dumps([dict(r) for r in rows], indent=2))


def cmd_purge_alerts(args: argparse.Namespace) -> None:
    """Remove claimed alerts older than --age seconds (default: 86400)."""
    conn: sqlite3.Connection = _db()
    cutoff: int = int(time.time()) - args.age
    cur = conn.execute(
        "DELETE FROM pending_alerts WHERE claimed_by IS NOT NULL AND claimed_at < ?",
        (cutoff,),
    )
    conn.commit()
    conn.close()
    print(f"purged {cur.rowcount}")


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def cmd_claim_task(args: argparse.Namespace) -> None:
    """Claim a task. Exits 0 with 'ok', or exits 1 if already claimed."""
    conn: sqlite3.Connection = _db()
    now: int = int(time.time())
    owner: str = args.owner or f"pid-{os.getpid()}"
    row = conn.execute(
        "SELECT status, owner FROM task_state WHERE task_id = ?", (args.task_id,)
    ).fetchone()
    if row and row["status"] == "claimed":
        print(f"already-claimed by {row['owner']}")
        conn.close()
        sys.exit(1)
    conn.execute(
        "INSERT OR REPLACE INTO task_state "
        "(task_id, status, owner, started_at, updated_at) VALUES (?, 'claimed', ?, ?, ?)",
        (args.task_id, owner, now, now),
    )
    conn.commit()
    conn.close()
    print("ok")


def cmd_release_task(args: argparse.Namespace) -> None:
    """Mark a claimed task as done. Exits 1 if task not found."""
    conn: sqlite3.Connection = _db()
    now: int = int(time.time())
    result: str = args.result or ""
    cur = conn.execute(
        "UPDATE task_state SET status = 'done', updated_at = ?, result = ? WHERE task_id = ?",
        (now, result, args.task_id),
    )
    conn.commit()
    conn.close()
    if cur.rowcount:
        print("ok")
    else:
        print("not-found")
        sys.exit(1)


def cmd_task_status(args: argparse.Namespace) -> None:
    """Print task status as JSON, or 'not-found' if it does not exist."""
    conn: sqlite3.Connection = _db()
    row = conn.execute(
        "SELECT task_id, status, owner, started_at, updated_at, result "
        "FROM task_state WHERE task_id = ?",
        (args.task_id,),
    ).fetchone()
    conn.close()
    if row:
        print(json.dumps(dict(row), indent=2))
    else:
        print("not-found")


def cmd_stats(args: argparse.Namespace) -> None:  # noqa: ARG001
    """Print summary counts for all three tables as JSON."""
    conn: sqlite3.Connection = _db()
    facts: int = conn.execute("SELECT COUNT(*) as c FROM active_facts").fetchone()["c"]
    alerts_pending: int = conn.execute(
        "SELECT COUNT(*) as c FROM pending_alerts WHERE claimed_by IS NULL"
    ).fetchone()["c"]
    alerts_claimed: int = conn.execute(
        "SELECT COUNT(*) as c FROM pending_alerts WHERE claimed_by IS NOT NULL"
    ).fetchone()["c"]
    tasks_claimed: int = conn.execute(
        "SELECT COUNT(*) as c FROM task_state WHERE status = 'claimed'"
    ).fetchone()["c"]
    tasks_done: int = conn.execute(
        "SELECT COUNT(*) as c FROM task_state WHERE status = 'done'"
    ).fetchone()["c"]
    conn.close()
    print(json.dumps({
        "facts": facts,
        "alerts_pending": alerts_pending,
        "alerts_claimed": alerts_claimed,
        "tasks_claimed": tasks_claimed,
        "tasks_done": tasks_done,
    }, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="clankerhive",
        description="🐝 ClankerHive — shared context store for multi-session agent coordination",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("set", help="Set a fact (key/value with optional TTL)")
    p.add_argument("key")
    p.add_argument("value")
    p.add_argument("--ttl", type=int, default=None, help="Time-to-live in seconds")
    p.add_argument("--source", default=None, help="Tag identifying who set this fact")

    p = sub.add_parser("get", help="Get a fact's value (empty output if missing/expired)")
    p.add_argument("key")

    p = sub.add_parser("list", help="List active facts (JSON array)")
    p.add_argument("--prefix", default=None, help="Filter by key prefix")

    p = sub.add_parser("delete", help="Delete a fact by key")
    p.add_argument("key")

    p = sub.add_parser("queue-alert", help="Queue an alert for another session")
    p.add_argument("topic")
    p.add_argument("payload")

    p = sub.add_parser("pop-alerts", help="Claim and return pending alerts (JSON)")
    p.add_argument("--topic", default=None, help="Filter by topic")
    p.add_argument("--claimer", default=None, help="Claimer identity string")

    sub.add_parser("list-alerts", help="List unclaimed alerts without claiming (JSON)")

    p = sub.add_parser("purge-alerts", help="Remove old claimed alerts")
    p.add_argument("--age", type=int, default=86400, help="Max age in seconds (default: 86400)")

    p = sub.add_parser("claim-task", help="Claim a task (exit 0=ok, exit 1=already-claimed)")
    p.add_argument("task_id")
    p.add_argument("--owner", default=None, help="Owner identity string")

    p = sub.add_parser("release-task", help="Mark a task as done")
    p.add_argument("task_id")
    p.add_argument("--result", default=None, help="Result string to store")

    p = sub.add_parser("task-status", help="Check task status (JSON)")
    p.add_argument("task_id")

    sub.add_parser("stats", help="Summary counts for all tables (JSON)")

    return parser


def main() -> None:
    """Entry point — parse args and dispatch to the appropriate command."""
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "set": cmd_set,
        "get": cmd_get,
        "list": cmd_list,
        "delete": cmd_delete,
        "queue-alert": cmd_queue_alert,
        "pop-alerts": cmd_pop_alerts,
        "list-alerts": cmd_list_alerts,
        "purge-alerts": cmd_purge_alerts,
        "claim-task": cmd_claim_task,
        "release-task": cmd_release_task,
        "task-status": cmd_task_status,
        "stats": cmd_stats,
    }

    try:
        dispatch[args.command](args)
    except (sqlite3.DatabaseError, sqlite3.OperationalError) as exc:
        print(f"database error: {exc}", file=sys.stderr)
        sys.exit(1)
    except (OSError, PermissionError) as exc:
        print(f"filesystem error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyError as exc:
        print(f"unknown command: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
