#!/usr/bin/env python3
"""Conservative migration for legacy scheduled/system rows stored in entries.

This script intentionally migrates only deterministic cases:
- existing canonical tasks that can be linked back to a legacy entry by normalized name
- explicit Meta-Review legacy rows -> daily system task with meta_review_fallback handler
- legacy every-N-hours subagent-memory sync rows -> hourly system task with sync_subagent_memory handler
- simple bracketed recurring rows with deterministic weekly/daily/monthly_n_times schedules

It does NOT auto-migrate ambiguous rows beyond those patterns.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from core.models import PeriodicTask  # noqa: E402
from core.scheduler import TaskScheduler  # noqa: E402

META_REVIEW_PATTERN = re.compile(r'meta[- ]?review|meta_auditor\.py', re.IGNORECASE)
EVERY_N_HOURS_PATTERN = re.compile(r'每\s*(\d+)\s*小时')
BRACKETED_PATTERN = re.compile(r'^\[(?P<label>[^\]]+)\]\s*(?P<name>.+?)\s*\((?P<schedule>.+)\)\s*$')
WEEKDAY_MAP = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6}


@dataclass
class MigrationPlan:
    entry_id: int
    text: str
    status: str
    group_name: str
    action: str
    reason: str
    normalized_name: str | None = None
    task_id: int | None = None
    task_params: dict[str, Any] | None = None
    unsupported_details: str | None = None


@dataclass
class AppliedResult:
    entry_id: int
    action: str
    task_id: int | None
    note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate deterministic legacy scheduled entries into periodic_tasks")
    parser.add_argument("--db", required=True, help="Path to todo.db")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON summary")
    parser.add_argument("--today", help="Override today's date for tests (YYYY-MM-DD)")
    return parser.parse_args()


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def normalize_legacy_name(text: str) -> str:
    text = text.strip()
    match = BRACKETED_PATTERN.match(text)
    if match:
        return match.group('name').strip()
    if META_REVIEW_PATTERN.search(text):
        return 'Meta-Review fallback'
    if EVERY_N_HOURS_PATTERN.search(text) and 'subagent' in text.lower():
        return '同步 subagent 记忆'
    return text


def parse_time(schedule: str) -> str | None:
    match = re.search(r'(\d{1,2})[:：](\d{2})', schedule)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    match = re.search(r'(\d{1,2})点', schedule)
    if match:
        hour = int(match.group(1))
        if 0 <= hour <= 23:
            return f"{hour:02d}:00"
    return None


def parse_weekday(schedule: str) -> int | None:
    for char, value in WEEKDAY_MAP.items():
        if f'周{char}' in schedule or f'星期{char}' in schedule:
            return value
    return None


def find_task_by_legacy_entry_id(conn: sqlite3.Connection, entry_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id, name, source, legacy_entry_id FROM periodic_tasks WHERE legacy_entry_id = ?",
        (entry_id,),
    ).fetchone()


def find_task_by_name(conn: sqlite3.Connection, name: str) -> sqlite3.Row | None:
    rows = conn.execute(
        "SELECT id, name, source, legacy_entry_id FROM periodic_tasks WHERE name = ? ORDER BY id",
        (name,),
    ).fetchall()
    if len(rows) == 1:
        return rows[0]
    return None


def build_meta_review_task(entry: sqlite3.Row) -> dict[str, Any]:
    start_date = None
    created_at = entry['created_at'] if 'created_at' in entry.keys() else None
    if created_at:
        try:
            start_date = str(created_at)[:10]
            date.fromisoformat(start_date)
        except ValueError:
            start_date = None
    payload = {
        'scope_days': 1,
        'fallback_sources': ['PREDICTIONS.md', 'FRICTION.md'],
        'note': 'Migrated from legacy entries row; explicit system handler replaces text-regex semantics.',
    }
    return {
        'name': 'Meta-Review fallback',
        'category': entry['group_name'] or 'System',
        'cycle_type': 'daily',
        'time_of_day': '02:00',
        'task_kind': 'system',
        'source': 'legacy_entries_migrated',
        'legacy_entry_id': entry['id'],
        'special_handler': 'meta_review_fallback',
        'handler_payload': json.dumps(payload, ensure_ascii=False),
        'start_date': start_date,
    }


def build_every_n_hours_task(entry: sqlite3.Row, interval_hours: int, anchor_time: str | None) -> dict[str, Any]:
    start_date = None
    created_at = entry['created_at'] if 'created_at' in entry.keys() else None
    if created_at:
        try:
            start_date = str(created_at)[:10]
            date.fromisoformat(start_date)
        except ValueError:
            start_date = None
    payload = {
        'command': 'memory_manager.py pending-subagents -> sync -> mark-subagent-synced',
        'session_filter': ':subagent:',
        'note': 'Migrated from legacy every-N-hours entry; sync pending recorded subagent sessions into main memory via ledger.',
    }
    return {
        'name': '同步 subagent 记忆',
        'category': entry['group_name'] or 'System',
        'cycle_type': 'hourly',
        'interval_hours': interval_hours,
        'time_of_day': anchor_time or '00:00',
        'task_kind': 'system',
        'source': 'legacy_entries_migrated',
        'legacy_entry_id': entry['id'],
        'special_handler': 'sync_subagent_memory',
        'handler_payload': json.dumps(payload, ensure_ascii=False),
        'start_date': start_date,
    }


def build_simple_schedule_task(entry: sqlite3.Row) -> dict[str, Any] | None:
    text = entry['text'].strip()
    match = BRACKETED_PATTERN.match(text)
    if not match:
        return None

    label = match.group('label').strip()
    name = match.group('name').strip()
    schedule = match.group('schedule').strip()
    time_of_day = parse_time(schedule)
    if not time_of_day:
        return None

    params: dict[str, Any] = {
        'name': name,
        'category': entry['group_name'] or 'Inbox',
        'time_of_day': time_of_day,
        'task_kind': 'scheduled',
        'source': 'legacy_entries_migrated',
        'legacy_entry_id': entry['id'],
    }

    weekday = parse_weekday(schedule)

    if '每日' in schedule or '每天' in schedule:
        if '每月' in label:
            params['cycle_type'] = 'monthly_n_times'
            params['n_per_month'] = 1
        else:
            params['cycle_type'] = 'daily'
        return params

    if '每周' in schedule and weekday is not None:
        params['cycle_type'] = 'weekly'
        params['weekday'] = weekday
        return params

    if ('每月两次' in label or '每月2次' in label or '每月参与一次' in schedule) and weekday is not None:
        params['cycle_type'] = 'monthly_n_times'
        params['weekday'] = weekday
        params['n_per_month'] = 1 if '每月参与一次' in schedule else 2
        return params

    return None


def classify_entry(conn: sqlite3.Connection, entry: sqlite3.Row) -> MigrationPlan:
    linked = find_task_by_legacy_entry_id(conn, entry['id'])
    if linked:
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='already_migrated',
            reason=f"already linked to periodic_tasks.id={linked['id']}",
            normalized_name=linked['name'],
            task_id=linked['id'],
        )

    normalized_name = normalize_legacy_name(entry['text'])
    existing = find_task_by_name(conn, normalized_name)
    if existing and existing['legacy_entry_id'] is None:
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='link_existing',
            reason='deterministic name match to existing canonical task',
            normalized_name=normalized_name,
            task_id=existing['id'],
        )

    if META_REVIEW_PATTERN.search(entry['text']):
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='create_task',
            reason='explicit meta-review system task',
            normalized_name='Meta-Review fallback',
            task_params=build_meta_review_task(entry),
        )

    every_hours = EVERY_N_HOURS_PATTERN.search(entry['text'])
    if every_hours and 'subagent' in entry['text'].lower() and 'memory_manager.py sync' in entry['text']:
        interval_hours = int(every_hours.group(1))
        anchor_time = parse_time(entry['text']) or '00:00'
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='create_task',
            reason='deterministic every-N-hours subagent memory sync system task',
            normalized_name='同步 subagent 记忆',
            task_params=build_every_n_hours_task(entry, interval_hours, anchor_time),
        )

    if every_hours:
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='manual_review',
            reason='unsupported every-N-hours cadence outside known system sync migration',
            normalized_name=normalized_name,
            unsupported_details=f"every {every_hours.group(1)} hours requires explicit handler semantics or manual mapping",
        )

    parsed = build_simple_schedule_task(entry)
    if parsed:
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='create_task',
            reason='deterministic bracketed recurring pattern',
            normalized_name=parsed['name'],
            task_params=parsed,
        )

    recurring_hint = any(token in entry['text'] for token in ('每周', '每月', '每日', '每天', 'meta-review', 'Meta-Review'))
    if recurring_hint:
        return MigrationPlan(
            entry_id=entry['id'],
            text=entry['text'],
            status=entry['status'],
            group_name=entry['group_name'] or 'Inbox',
            action='manual_review',
            reason='looks scheduled but cannot be deterministically mapped',
            normalized_name=normalized_name,
        )

    return MigrationPlan(
        entry_id=entry['id'],
        text=entry['text'],
        status=entry['status'],
        group_name=entry['group_name'] or 'Inbox',
        action='skip_inbox',
        reason='no recurring/system scheduling semantics detected',
        normalized_name=normalized_name,
    )


def insert_task(conn: sqlite3.Connection, params: dict[str, Any]) -> int:
    task_columns = {row[1] for row in conn.execute("PRAGMA table_info(periodic_tasks)").fetchall()}
    column_values = {
        'name': params.get('name'),
        'category': params.get('category', 'Inbox'),
        'cycle_type': params.get('cycle_type', 'once'),
        'weekday': params.get('weekday'),
        'day_of_month': params.get('day_of_month'),
        'range_start': params.get('range_start'),
        'range_end': params.get('range_end'),
        'n_per_month': params.get('n_per_month'),
        'interval_hours': params.get('interval_hours'),
        'time_of_day': params.get('time_of_day', '09:00'),
        'event_time': params.get('time_of_day', '09:00'),
        'end_date': params.get('end_date'),
        'reminder_template': params.get('reminder_template'),
        'dates_list': params.get('dates_list'),
        'task_kind': params.get('task_kind', 'scheduled'),
        'source': params.get('source', 'legacy_entries_migrated'),
        'legacy_entry_id': params.get('legacy_entry_id'),
        'special_handler': params.get('special_handler'),
        'handler_payload': params.get('handler_payload'),
        'start_date': params.get('start_date'),
        'delivery_target': params.get('delivery_target'),
        'delivery_mode': params.get('delivery_mode'),
    }
    ordered_columns = [
        'name', 'category', 'cycle_type', 'weekday', 'day_of_month', 'range_start', 'range_end', 'n_per_month',
        'interval_hours', 'time_of_day', 'event_time', 'end_date', 'reminder_template', 'dates_list', 'task_kind',
        'source', 'legacy_entry_id', 'special_handler', 'handler_payload', 'start_date', 'delivery_target', 'delivery_mode'
    ]
    columns = [column for column in ordered_columns if column in task_columns]
    placeholders = ', '.join('?' for _ in columns)
    sql = (
        f"INSERT INTO periodic_tasks ({', '.join(columns)}, timezone, is_active, count_current_month, created_at, updated_at) "
        f"VALUES ({placeholders}, 'Asia/Shanghai', 1, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    )
    values = tuple(column_values[column] for column in columns)
    cur = conn.execute(sql, values)
    return int(cur.lastrowid)


def maybe_seed_occurrence(conn: sqlite3.Connection, task_id: int, params: dict[str, Any], entry_status: str, today: date) -> bool:
    if entry_status not in ('pending', 'in_progress'):
        return False

    task = PeriodicTask(
        id=task_id,
        name=params['name'],
        category=params.get('category', 'Inbox'),
        cycle_type=params.get('cycle_type', 'once'),
        weekday=params.get('weekday'),
        day_of_month=params.get('day_of_month'),
        range_start=params.get('range_start'),
        range_end=params.get('range_end'),
        n_per_month=params.get('n_per_month'),
        interval_hours=params.get('interval_hours'),
        time_of_day=params.get('time_of_day', '09:00'),
        event_time=params.get('time_of_day', '09:00'),
        dates_list=params.get('dates_list'),
        task_kind=params.get('task_kind', 'scheduled'),
        source=params.get('source', 'legacy_entries_migrated'),
        legacy_entry_id=params.get('legacy_entry_id'),
        special_handler=params.get('special_handler'),
        handler_payload=params.get('handler_payload'),
        start_date=params.get('start_date'),
        end_date=params.get('end_date'),
        delivery_target=params.get('delivery_target'),
        delivery_mode=params.get('delivery_mode'),
    )
    scheduler = TaskScheduler(task, today)
    if not scheduler.should_remind_today():
        return False

    if params.get('cycle_type') == 'hourly':
        seeded_any = False
        occurrence_columns = {row[1] for row in conn.execute("PRAGMA table_info(periodic_occurrences)").fetchall()}
        occurrence_sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='periodic_occurrences'").fetchone()[0]
        unique_by_time = 'UNIQUE(task_id, date, scheduled_time)' in occurrence_sql
        for scheduled_time in scheduler.get_hourly_schedule_for_day(today):
            scheduled_at = f"{today.isoformat()}T{scheduled_time}:00"
            if unique_by_time:
                conn.execute(
                    """
                    INSERT INTO periodic_occurrences (task_id, date, status, scheduled_time, scheduled_at, legacy_entry_id)
                    VALUES (?, ?, 'pending', ?, ?, ?)
                    """,
                    (task_id, today.isoformat(), scheduled_time, scheduled_at, params.get('legacy_entry_id')),
                )
                seeded_any = True
            else:
                if seeded_any:
                    continue
                insert_columns = ['task_id', 'date', 'status']
                insert_values = [task_id, today.isoformat(), 'pending']
                if 'scheduled_time' in occurrence_columns:
                    insert_columns.append('scheduled_time')
                    insert_values.append(scheduled_time)
                if 'scheduled_at' in occurrence_columns:
                    insert_columns.append('scheduled_at')
                    insert_values.append(scheduled_at)
                if 'legacy_entry_id' in occurrence_columns:
                    insert_columns.append('legacy_entry_id')
                    insert_values.append(params.get('legacy_entry_id'))
                placeholders = ', '.join('?' for _ in insert_columns)
                conn.execute(
                    f"INSERT OR IGNORE INTO periodic_occurrences ({', '.join(insert_columns)}) VALUES ({placeholders})",
                    tuple(insert_values),
                )
                seeded_any = True
        return seeded_any

    scheduled_time = params.get('time_of_day')
    scheduled_at = f"{today.isoformat()}T{scheduled_time}:00" if scheduled_time else None
    conn.execute(
        """
        INSERT OR IGNORE INTO periodic_occurrences (task_id, date, status, scheduled_time, scheduled_at, legacy_entry_id)
        VALUES (?, ?, 'pending', ?, ?, ?)
        """,
        (task_id, today.isoformat(), scheduled_time, scheduled_at, params.get('legacy_entry_id')),
    )
    return True


def apply_plan(conn: sqlite3.Connection, plan: MigrationPlan, today: date) -> AppliedResult:
    if plan.action == 'link_existing':
        conn.execute(
            """
            UPDATE periodic_tasks
            SET legacy_entry_id = ?,
                source = CASE
                    WHEN source IS NULL OR source = '' OR source = 'chronos' THEN 'legacy_entries_linked'
                    ELSE source
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND legacy_entry_id IS NULL
            """,
            (plan.entry_id, plan.task_id),
        )
        return AppliedResult(plan.entry_id, plan.action, plan.task_id, f"linked entry {plan.entry_id} -> task {plan.task_id}")

    if plan.action == 'create_task' and plan.task_params:
        task_id = insert_task(conn, plan.task_params)
        seeded = maybe_seed_occurrence(conn, task_id, plan.task_params, plan.status, today)
        note = f"created task {task_id} from entry {plan.entry_id}"
        if seeded:
            note += f"; seeded occurrence for {today.isoformat()}"
        return AppliedResult(plan.entry_id, plan.action, task_id, note)

    return AppliedResult(plan.entry_id, plan.action, plan.task_id, plan.reason)


def load_entries(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT e.id, e.text, e.status, e.created_at, e.updated_at, COALESCE(g.name, 'Inbox') AS group_name
        FROM entries e
        LEFT JOIN groups g ON g.id = e.group_id
        ORDER BY e.id
        """
    ).fetchall()


def summarize(plans: list[MigrationPlan], applied: list[AppliedResult], apply_mode: bool, today: date) -> dict[str, Any]:
    by_action: dict[str, int] = {}
    for plan in plans:
        by_action[plan.action] = by_action.get(plan.action, 0) + 1

    return {
        'mode': 'apply' if apply_mode else 'dry-run',
        'today': today.isoformat(),
        'counts': by_action,
        'plans': [asdict(plan) for plan in plans],
        'applied': [asdict(item) for item in applied],
    }


def print_human(summary: dict[str, Any]) -> None:
    print(f"Chronos legacy migration ({summary['mode']})")
    print(f"today={summary['today']}")
    for action, count in sorted(summary['counts'].items()):
        print(f"- {action}: {count}")
    print()
    for plan in summary['plans']:
        line = f"[{plan['action']}] entry {plan['entry_id']} | {plan['text']}"
        if plan.get('task_id'):
            line += f" -> task {plan['task_id']}"
        elif plan.get('normalized_name'):
            line += f" -> {plan['normalized_name']}"
        line += f" | {plan['reason']}"
        if plan.get('unsupported_details'):
            line += f" | {plan['unsupported_details']}"
        print(line)
    if summary['applied']:
        print()
        print('Applied:')
        for item in summary['applied']:
            print(f"- {item['note']}")


def main() -> int:
    args = parse_args()
    today = date.fromisoformat(args.today) if args.today else datetime.now().date()

    conn = connect(args.db)
    try:
        plans = [classify_entry(conn, entry) for entry in load_entries(conn)]
        applied: list[AppliedResult] = []
        if args.apply:
            for plan in plans:
                if plan.action in {'link_existing', 'create_task'}:
                    applied.append(apply_plan(conn, plan, today))
            conn.commit()
        summary = summarize(plans, applied, args.apply, today)
    finally:
        conn.close()

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_human(summary)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
