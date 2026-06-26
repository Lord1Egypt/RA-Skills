#!/usr/bin/env python3
"""Normalize low-risk historical Chronos residues.

This script handles two deterministic cleanup classes only:
1) orphan periodic_occurrences whose task_id no longer exists
2) legacy once tasks with NULL start_date when a canonical date can be inferred safely

Safety rules:
- default is dry-run
- only mutate rows when a single deterministic normalization path exists
- ambiguous rows are surfaced as manual_review and left untouched
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Plan:
    kind: str
    action: str
    reason: str
    row_id: int
    task_id: int | None = None
    task_name: str | None = None
    inferred_start_date: str | None = None
    occurrence_dates: list[str] | None = None
    end_date: str | None = None
    status: str | None = None


@dataclass
class AppliedResult:
    kind: str
    row_id: int
    note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize low-risk historical Chronos residues")
    parser.add_argument("--db", required=True, help="Path to todo.db")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    return parser.parse_args()


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_table_names(conn: sqlite3.Connection) -> set[str]:
    return {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}


def classify_orphan_occurrences(conn: sqlite3.Connection) -> list[Plan]:
    rows = conn.execute(
        """
        SELECT o.id, o.task_id, o.date, o.status
        FROM periodic_occurrences o
        LEFT JOIN periodic_tasks t ON t.id = o.task_id
        WHERE t.id IS NULL
        ORDER BY o.id
        """
    ).fetchall()
    return [
        Plan(
            kind='orphan_occurrence',
            action='delete',
            reason='task_id no longer exists; row cannot affect live scheduling semantics',
            row_id=int(row['id']),
            task_id=int(row['task_id']) if row['task_id'] is not None else None,
            occurrence_dates=[row['date']] if row['date'] else [],
            status=row['status'],
        )
        for row in rows
    ]


def classify_once_null_start(conn: sqlite3.Connection) -> list[Plan]:
    rows = conn.execute(
        """
        SELECT t.id, t.name, t.end_date, t.is_active,
               GROUP_CONCAT(o.date, ',') AS occurrence_dates,
               COUNT(o.id) AS occurrence_count,
               MIN(o.date) AS min_occurrence_date,
               MAX(o.date) AS max_occurrence_date
        FROM periodic_tasks t
        LEFT JOIN periodic_occurrences o ON o.task_id = t.id
        WHERE t.cycle_type = 'once' AND t.start_date IS NULL
        GROUP BY t.id, t.name, t.end_date, t.is_active
        ORDER BY t.id
        """
    ).fetchall()

    plans: list[Plan] = []
    for row in rows:
        occurrence_count = int(row['occurrence_count'] or 0)
        occurrence_dates = [d for d in (row['occurrence_dates'] or '').split(',') if d]
        inferred_start_date = None
        action = 'manual_review'
        reason = 'ambiguous once task residue'

        if occurrence_count == 1 and row['min_occurrence_date'] == row['max_occurrence_date']:
            inferred_start_date = row['min_occurrence_date']
            action = 'set_start_date'
            reason = 'single canonical occurrence date available'
        elif occurrence_count == 0 and row['end_date']:
            inferred_start_date = row['end_date']
            action = 'set_start_date'
            reason = 'legacy once task has no occurrence yet; use existing end_date as scheduled date'
        elif occurrence_count == 0:
            action = 'manual_review'
            reason = 'once task has neither occurrence history nor end_date'
        else:
            action = 'manual_review'
            reason = 'once task has multiple occurrence dates; cannot infer single canonical start_date safely'

        plans.append(
            Plan(
                kind='once_null_start_date',
                action=action,
                reason=reason,
                row_id=int(row['id']),
                task_id=int(row['id']),
                task_name=row['name'],
                inferred_start_date=inferred_start_date,
                occurrence_dates=occurrence_dates,
                end_date=row['end_date'],
                status='active' if int(row['is_active'] or 0) else 'inactive',
            )
        )
    return plans


def apply_plan(conn: sqlite3.Connection, plan: Plan) -> AppliedResult | None:
    if plan.kind == 'orphan_occurrence' and plan.action == 'delete':
        conn.execute("DELETE FROM periodic_occurrences WHERE id = ?", (plan.row_id,))
        return AppliedResult(kind=plan.kind, row_id=plan.row_id, note=f"deleted orphan occurrence {plan.row_id} (task_id={plan.task_id})")
    if plan.kind == 'once_null_start_date' and plan.action == 'set_start_date' and plan.inferred_start_date:
        conn.execute(
            "UPDATE periodic_tasks SET start_date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND start_date IS NULL",
            (plan.inferred_start_date, plan.row_id),
        )
        return AppliedResult(kind=plan.kind, row_id=plan.row_id, note=f"set periodic_tasks.id={plan.row_id} start_date={plan.inferred_start_date}")
    return None


def summarize(plans: list[Plan], applied: list[AppliedResult], apply_mode: bool, db_path: str) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for plan in plans:
        key = f"{plan.kind}:{plan.action}"
        counts[key] = counts.get(key, 0) + 1
    return {
        'mode': 'apply' if apply_mode else 'dry-run',
        'db': db_path,
        'counts': counts,
        'plans': [asdict(plan) for plan in plans],
        'applied': [asdict(item) for item in applied],
    }


def print_human(summary: dict[str, Any]) -> None:
    print(f"Chronos historical residue normalization ({summary['mode']})")
    print(f"db={summary['db']}")
    for key, count in sorted(summary['counts'].items()):
        print(f"- {key}: {count}")
    if summary['plans']:
        print()
    for plan in summary['plans']:
        extra = ''
        if plan.get('inferred_start_date'):
            extra = f" -> {plan['inferred_start_date']}"
        print(f"[{plan['kind']}:{plan['action']}] row {plan['row_id']}{extra} | {plan['reason']}")
    if summary['applied']:
        print()
        print('Applied:')
        for item in summary['applied']:
            print(f"- {item['note']}")


def main() -> int:
    args = parse_args()
    conn = connect(args.db)
    try:
        tables = get_table_names(conn)
        required = {'periodic_tasks', 'periodic_occurrences'}
        missing = sorted(required - tables)
        if missing:
            raise SystemExit(f"Missing tables: {', '.join(missing)}")
        plans = classify_orphan_occurrences(conn) + classify_once_null_start(conn)
        applied: list[AppliedResult] = []
        if args.apply:
            for plan in plans:
                result = apply_plan(conn, plan)
                if result:
                    applied.append(result)
            conn.commit()
        summary = summarize(plans, applied, args.apply, args.db)
    finally:
        conn.close()

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_human(summary)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
