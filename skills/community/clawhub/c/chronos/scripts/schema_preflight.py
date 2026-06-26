#!/usr/bin/env python3
"""Preflight checks for Chronos runtime DB schema health."""
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.paths import TODO_DB, WORKSPACE
from core.models import ALLOWED_CYCLE_TYPES

ALLOWED_OCCURRENCE_STATUSES = {"pending", "completed", "skipped", "reminded"}
REQUIRED_TABLES = {"periodic_tasks", "periodic_occurrences"}
REQUIRED_TASK_COLUMNS = {"task_kind", "source", "special_handler", "start_date", "delivery_target", "delivery_mode", "interval_hours"}
REQUIRED_OCCURRENCE_COLUMNS = {"completion_mode", "special_handler_result", "scheduled_time", "scheduled_at"}


def get_table_names(conn: sqlite3.Connection) -> set[str]:
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return {row[0] for row in cur.fetchall()}


def get_table_sql(conn: sqlite3.Connection, table_name: str) -> str:
    cur = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name = ?",
        (table_name,),
    )
    row = cur.fetchone()
    return row[0] or "" if row else ""


def get_table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    cur = conn.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cur.fetchall()}


def count_duplicate_occurrences(conn: sqlite3.Connection) -> int:
    occurrence_columns = get_table_columns(conn, "periodic_occurrences")
    if 'scheduled_time' in occurrence_columns:
        cur = conn.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT task_id, date, COALESCE(scheduled_time, '') AS scheduled_key, COUNT(*) AS n
                FROM periodic_occurrences
                GROUP BY task_id, date, COALESCE(scheduled_time, '')
                HAVING COUNT(*) > 1
            )
            """
        )
    else:
        cur = conn.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT task_id, date, COUNT(*) AS n
                FROM periodic_occurrences
                GROUP BY task_id, date
                HAVING COUNT(*) > 1
            )
            """
        )
    return int(cur.fetchone()[0])


def get_invalid_statuses(conn: sqlite3.Connection) -> list[dict]:
    cur = conn.execute(
        """
        SELECT status, COUNT(*)
        FROM periodic_occurrences
        GROUP BY status
        ORDER BY status
        """
    )
    invalid = []
    for status, count in cur.fetchall():
        if status not in ALLOWED_OCCURRENCE_STATUSES:
            invalid.append({"status": status, "count": count})
    return invalid


def get_invalid_cycle_types(conn: sqlite3.Connection) -> list[dict]:
    cur = conn.execute(
        """
        SELECT cycle_type, COUNT(*)
        FROM periodic_tasks
        GROUP BY cycle_type
        ORDER BY cycle_type
        """
    )
    invalid = []
    for cycle_type, count in cur.fetchall():
        if cycle_type not in ALLOWED_CYCLE_TYPES:
            invalid.append({"cycle_type": cycle_type, "count": count})
    return invalid


def inspect_schema() -> dict:
    info = {
        "workspace": str(WORKSPACE),
        "runtime_db": str(TODO_DB),
        "db_exists": TODO_DB.exists(),
        "status": "ok",
        "errors": [],
        "checks": {},
    }

    if not TODO_DB.exists():
        info["status"] = "error"
        info["errors"].append("Runtime todo.db does not exist")
        return info

    conn = sqlite3.connect(str(TODO_DB))
    try:
        tables = get_table_names(conn)
        missing_tables = sorted(REQUIRED_TABLES - tables)
        if missing_tables:
            info["status"] = "error"
            info["errors"].append(f"Missing required tables: {', '.join(missing_tables)}")
            return info

        occurrences_sql = get_table_sql(conn, "periodic_occurrences")
        tasks_sql = get_table_sql(conn, "periodic_tasks")
        task_columns = get_table_columns(conn, "periodic_tasks")
        occurrence_columns = get_table_columns(conn, "periodic_occurrences")
        duplicate_count = count_duplicate_occurrences(conn)
        invalid_statuses = get_invalid_statuses(conn)
        invalid_cycle_types = get_invalid_cycle_types(conn)

        info["checks"] = {
            "tables_present": sorted(REQUIRED_TABLES),
            "periodic_occurrences_unique_task_date": (
                "UNIQUE(task_id, date, scheduled_time)" in occurrences_sql
                or "UNIQUE(task_id, date)" in occurrences_sql
            ),
            "periodic_occurrences_fk_task_id": "FOREIGN KEY (task_id) REFERENCES periodic_tasks(id) ON DELETE CASCADE" in occurrences_sql,
            "periodic_tasks_name_unique": "name TEXT NOT NULL UNIQUE" in tasks_sql,
            "required_task_columns_present": sorted(REQUIRED_TASK_COLUMNS - task_columns) == [],
            "required_occurrence_columns_present": sorted(REQUIRED_OCCURRENCE_COLUMNS - occurrence_columns) == [],
            "missing_task_columns": sorted(REQUIRED_TASK_COLUMNS - task_columns),
            "missing_occurrence_columns": sorted(REQUIRED_OCCURRENCE_COLUMNS - occurrence_columns),
            "duplicate_occurrence_groups": duplicate_count,
            "invalid_statuses": invalid_statuses,
            "invalid_cycle_types": invalid_cycle_types,
        }

        if not info["checks"]["periodic_occurrences_unique_task_date"]:
            info["status"] = "warn"
            info["errors"].append("Missing UNIQUE(task_id, date) on periodic_occurrences")
        if not info["checks"]["periodic_occurrences_fk_task_id"]:
            info["status"] = "warn"
            info["errors"].append("Missing FK(task_id -> periodic_tasks.id ON DELETE CASCADE)")
        if not info["checks"]["required_task_columns_present"]:
            info["status"] = "warn"
            info["errors"].append(f"Missing periodic_tasks phase-1 columns: {', '.join(info['checks']['missing_task_columns'])}")
        if not info["checks"]["required_occurrence_columns_present"]:
            info["status"] = "warn"
            info["errors"].append(f"Missing periodic_occurrences phase-1 columns: {', '.join(info['checks']['missing_occurrence_columns'])}")
        if duplicate_count > 0:
            info["status"] = "warn"
            info["errors"].append(f"Found {duplicate_count} duplicate occurrence groups")
        if invalid_statuses:
            info["status"] = "warn"
            info["errors"].append("Found invalid periodic_occurrences.status values")
        if invalid_cycle_types:
            info["status"] = "warn"
            info["errors"].append("Found invalid periodic_tasks.cycle_type values")

        return info
    finally:
        conn.close()


def main() -> int:
    info = inspect_schema()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0 if info["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
