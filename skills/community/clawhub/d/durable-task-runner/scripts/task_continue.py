#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from task_resume_apply import apply_task
from task_resume_bootstrap import inspect_task, iter_tasks

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / 'state' / 'tasks'
SCRIPTS = ROOT / 'scripts'


def load_task(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text())
    except Exception:
        return None
    return data if isinstance(data, dict) and data.get('task_id') else None


def list_tasks() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(STATE_DIR.glob('*.json')):
        data = load_task(path)
        if data:
            rows.append(data)
    return rows


def score_task(task: dict[str, Any]) -> tuple[int, str]:
    desired = task.get('desired_state')
    updated = task.get('updated_at') or ''
    phase = task.get('phase') or ''
    if desired == 'running':
        return (400, updated)
    if desired == 'paused':
        return (300, updated)
    if desired == 'failed':
        return (200, updated)
    if desired == 'stopped':
        return (100, updated)
    if desired == 'completed' and phase != 'complete':
        return (50, updated)
    return (0, updated)


def select_task(explicit_task_id: str | None) -> dict[str, Any]:
    tasks = list_tasks()
    if explicit_task_id:
        for task in tasks:
            if task.get('task_id') == explicit_task_id:
                return task
        raise SystemExit(f'task not found: {explicit_task_id}')
    candidates = [t for t in tasks if t.get('desired_state') in {'running', 'paused', 'failed', 'stopped'}]
    if not candidates:
        raise SystemExit('no resumable durable tasks found')
    candidates.sort(key=score_task, reverse=True)
    return candidates[0]


def main() -> int:
    p = argparse.ArgumentParser(description='Resume the most relevant durable task after reset/interruption.')
    p.add_argument('--task-id')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--promote-paused', action='store_true', default=True)
    p.add_argument('--no-promote-paused', dest='promote_paused', action='store_false')
    args = p.parse_args()

    task = select_task(args.task_id)
    task_id = task['task_id']

    promoted = False
    previous_state = task.get('desired_state')
    if args.promote_paused and not args.dry_run and previous_state in {'paused', 'stopped'}:
        import subprocess
        subprocess.run([
            'python3', str(SCRIPTS / 'task_ctl.py'), 'control', task_id, 'running',
            '--note', 'explicit continue-this recovery after reset/interruption',
            '--report-kind', 'internal',
        ], check=True, capture_output=True, text=True)
        task = load_task(STATE_DIR / f'{task_id}.json') or task
        promoted = True

    matches = [(path, row) for path, row in iter_tasks() if row.get('task_id') == task_id]
    if not matches:
        raise SystemExit(f'task not found: {task_id}')
    path, current_task = matches[0]
    item = inspect_task(path, current_task, run_reconcile_checks=True, include_plan=True)
    bootstrap = {'tasks': [item]}
    action = item.get('recommendation', {}).get('action')

    applied: dict[str, Any] | None = None
    if not args.dry_run and action in {'resume_active_line', 'resume_main_flow', 'controller_decision_needed', 'user_control_pending'}:
        applied = {'applied': [apply_task(item)]}
        task = load_task(STATE_DIR / f'{task_id}.json') or task

    print(json.dumps({
        'ok': True,
        'selected_task': {
            'task_id': task_id,
            'title': task.get('title', task_id),
            'desired_state': task.get('desired_state'),
            'phase': task.get('phase', ''),
            'next_step': task.get('next_step', ''),
        },
        'promoted_from_state': previous_state if promoted else None,
        'classification': item.get('classification'),
        'reasons': item.get('reasons', []),
        'recommendation': item.get('recommendation', {}),
        'resume_plan': item.get('resume_plan', {}),
        'applied': applied,
    }, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
