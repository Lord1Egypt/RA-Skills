"""Shared helpers for readonly/archive semantics on legacy entries."""
from __future__ import annotations

import sqlite3
from typing import Any, Mapping

ARCHIVE_STATUS = 'archived'
ARCHIVE_NOTE_PREFIX = 'Chronos legacy archive:'
ENTRY_ARCHIVE_COLUMNS = {
    'chronos_readonly': "ALTER TABLE entries ADD COLUMN chronos_readonly INTEGER NOT NULL DEFAULT 0",
    'chronos_archived_at': "ALTER TABLE entries ADD COLUMN chronos_archived_at TEXT",
    'chronos_archive_reason': "ALTER TABLE entries ADD COLUMN chronos_archive_reason TEXT",
    'chronos_archived_from_status': "ALTER TABLE entries ADD COLUMN chronos_archived_from_status TEXT",
    'chronos_linked_task_id': "ALTER TABLE entries ADD COLUMN chronos_linked_task_id INTEGER",
}


def get_entry_columns(conn: sqlite3.Connection) -> set[str]:
    return {row[1] for row in conn.execute('PRAGMA table_info(entries)').fetchall()}


def get_allowed_entry_statuses(conn: sqlite3.Connection) -> set[str] | None:
    row = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='entries'").fetchone()
    if not row or not row[0]:
        return None
    sql = str(row[0])
    marker = "CHECK (status IN ("
    start = sql.find(marker)
    if start == -1:
        return None
    end = sql.find('))', start)
    if end == -1:
        return None
    raw_values = sql[start + len(marker):end]
    values = []
    for chunk in raw_values.split(','):
        chunk = chunk.strip()
        if len(chunk) >= 2 and chunk[0] == chunk[-1] == "'":
            values.append(chunk[1:-1])
    return set(values) or None


def resolve_archive_status(conn: sqlite3.Connection, current_status: str) -> str:
    allowed = get_allowed_entry_statuses(conn)
    if not allowed or ARCHIVE_STATUS in allowed:
        return ARCHIVE_STATUS
    return current_status


def ensure_archive_columns(conn: sqlite3.Connection) -> None:
    columns = get_entry_columns(conn)
    for name, statement in ENTRY_ARCHIVE_COLUMNS.items():
        if name not in columns:
            conn.execute(statement)
    conn.commit()


def legacy_archive_select_expressions(columns: set[str], table_alias: str = '') -> dict[str, str]:
    prefix = f'{table_alias}.' if table_alias else ''
    return {
        'chronos_readonly': f"COALESCE({prefix}chronos_readonly, 0)" if 'chronos_readonly' in columns else '0',
        'chronos_archived_at': f"{prefix}chronos_archived_at" if 'chronos_archived_at' in columns else 'NULL',
        'chronos_archived_from_status': f"{prefix}chronos_archived_from_status" if 'chronos_archived_from_status' in columns else 'NULL',
        'chronos_linked_task_id': f"{prefix}chronos_linked_task_id" if 'chronos_linked_task_id' in columns else 'NULL',
        'chronos_archive_reason': f"{prefix}chronos_archive_reason" if 'chronos_archive_reason' in columns else 'NULL',
    }


def build_entry_archive_state(row: Mapping[str, Any] | dict[str, Any]) -> dict[str, Any]:
    state = {
        'status': row.get('status'),
        'chronos_readonly': int(row.get('chronos_readonly') or 0),
        'chronos_archived_at': row.get('chronos_archived_at'),
        'chronos_archived_from_status': row.get('chronos_archived_from_status'),
        'chronos_linked_task_id': row.get('chronos_linked_task_id'),
        'chronos_archive_reason': row.get('chronos_archive_reason'),
    }
    state['is_archived'] = is_archived_entry_state(state)
    return state


def is_archived_entry_state(state: Mapping[str, Any]) -> bool:
    return bool(
        state.get('status') == ARCHIVE_STATUS
        or state.get('chronos_archived_at')
        or state.get('chronos_archive_reason')
        or state.get('chronos_archived_from_status')
    )


def archive_display_label(state: Mapping[str, Any]) -> str:
    return 'Chronos：legacy 归档（只读）' if int(state.get('chronos_readonly') or 0) else 'Chronos：legacy 归档'


def archive_block_message(entry_id: int, state: Mapping[str, Any]) -> str:
    task_hint = f"，请改为操作关联周期任务 {state.get('chronos_linked_task_id')}" if state.get('chronos_linked_task_id') else ''
    archive_hint = '（只读）' if int(state.get('chronos_readonly') or 0) else ''
    return f"❌ ID {entry_id} 是 legacy 归档记录{archive_hint}{task_hint}"
