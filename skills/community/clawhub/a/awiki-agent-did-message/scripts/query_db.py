"""Read-only SQL query CLI against local SQLite database.

Usage:
    python scripts/query_db.py "SELECT * FROM threads LIMIT 10"
    python scripts/query_db.py "SELECT * FROM messages WHERE credential_name='alice' LIMIT 10"
    python scripts/query_db.py "SELECT * FROM groups ORDER BY last_message_at DESC LIMIT 10"
    python scripts/query_db.py "SELECT * FROM group_members WHERE group_id='grp_xxx' LIMIT 20"
    python scripts/query_db.py "SELECT * FROM relationship_events WHERE status='pending' ORDER BY created_at DESC LIMIT 20"

[INPUT]: local_store (SQLite connection + execute_sql), logging_config
[OUTPUT]: JSON query results to stdout, concise validation/SQLite errors to stderr
[POS]: CLI entry point for ad-hoc local database queries

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sqlite3

import local_store
from utils.cli_errors import exit_with_cli_error
from utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def _normalize_sql_input(sql: str) -> str:
    """Normalize shell-style SQL continuations before execution."""
    return re.sub(r"\s*\\\r?\n\s*", " ", sql)


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Query local SQLite database")
    parser.add_argument("sql", type=str, help="SQL statement to execute")
    parser.add_argument(
        "--credential",
        type=str,
        default=None,
        help="Legacy option; prefer explicit owner_did / credential_name filters in SQL",
    )

    args = parser.parse_args()
    normalized_sql = _normalize_sql_input(args.sql)
    logger.info("query_db CLI started sql=%s", normalized_sql)

    conn = local_store.get_connection()
    local_store.ensure_schema(conn)

    try:
        result = local_store.execute_sql(conn, normalized_sql)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        logger.info("query_db completed rows=%d", len(result) if isinstance(result, list) else 1)
    except ValueError as exc:
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="query_db rejected sql",
            exit_code=1,
            log_traceback=False,
        )
    except sqlite3.Error as exc:
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="query_db execution failed",
        )
    except Exception as exc:  # noqa: BLE001
        exit_with_cli_error(
            exc=exc,
            logger=logger,
            context="query_db CLI failed",
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
