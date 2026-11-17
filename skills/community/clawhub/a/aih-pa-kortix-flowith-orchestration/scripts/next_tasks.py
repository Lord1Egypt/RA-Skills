"""Offline dependency/budget checker. Never executes tasks or verifies evidence."""
import argparse
import json
import math
from pathlib import Path
import re

STATES = {'pending', 'running', 'needs_review', 'accepted', 'failed', 'uncertain'}


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError('budget amounts must be finite nonnegative numbers')
    return value


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + ' must be nonempty text')
    return value


def inspect(plan):
    tasks = plan['tasks']
    if not isinstance(tasks, list) or not tasks or len(tasks) > 500:
        raise ValueError('tasks must contain 1 to 500 nodes')
    nodes, effects = {}, set()
    for task in tasks:
        tid = text(task.get('id'), 'id')
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', tid) or tid in nodes:
            raise ValueError('invalid or duplicate task id')
        nodes[tid] = task
        deps = task.get('depends_on')
        if not isinstance(deps, list) or not all(isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise ValueError('dependencies must be unique string ids')
        if task.get('status') not in STATES:
            raise ValueError('unknown task status')
        for key in ('deliverable', 'acceptance'):
            text(task.get(key), key)
        number(task.get('reserve_cost'))
        if not isinstance(task.get('external_write'), bool):
            raise ValueError('external_write must be an explicit boolean')
        if task['external_write']:
            effect = text(task.get('effect_key'), 'effect_key')
            if effect in effects:
                raise ValueError('same external business action appears more than once')
            effects.add(effect)
        if task['status'] == 'accepted':
            text(task.get('evidence_ref'), 'evidence_ref')
            if task['external_write']:
                text(task.get('receipt_ref'), 'receipt_ref')
    indegree = {tid: len(t['depends_on']) for tid, t in nodes.items()}
    children = {tid: [] for tid in nodes}
    for tid, task in nodes.items():
        for dep in task['depends_on']:
            if dep not in nodes:
                raise ValueError('unknown dependency: ' + dep)
            children[dep].append(tid)
        if task['status'] == 'accepted' and any(nodes[d]['status'] != 'accepted' for d in task['depends_on']):
            raise ValueError('accepted node has unaccepted dependencies')
    queue = [tid for tid, value in indegree.items() if value == 0]
    visited = []
    while queue:
        tid = queue.pop(0); visited.append(tid)
        for child in children[tid]:
            indegree[child] -= 1
            if indegree[child] == 0: queue.append(child)
    if len(visited) != len(nodes):
        raise ValueError('dependency cycle')
    budget = plan['budget']
    text(budget.get('currency'), 'currency')
    limit, spent, reserved = (number(budget[k]) for k in ('limit', 'spent', 'reserved'))
    if reserved < sum(t['reserve_cost'] for t in tasks if t['status'] == 'running'):
        raise ValueError('running task reservations are not fully accounted for')
    remaining = limit - spent - reserved
    if remaining < 0:
        raise ValueError('spent plus reserved exceeds budget; stop')
    ready, blocked = [], []
    for tid, task in nodes.items():
        status = task['status']
        if status == 'accepted': continue
        reason = None
        if status == 'uncertain': reason = 'reconcile remote result; no retry'
        elif status in ('running', 'needs_review'): reason = 'existing execution or review outstanding'
        elif status == 'failed' and task['external_write']: reason = 'external failure requires separate reconciliation'
        elif status == 'failed' and task.get('retry_decision') != 'approved': reason = 'retry decision required'
        elif any(nodes[d]['status'] != 'accepted' for d in task['depends_on']): reason = 'dependencies not accepted'
        elif task['external_write'] and not (isinstance(task.get('authorization_ref'), str) and task['authorization_ref'].strip()): reason = 'specific user authorization required'
        elif task['reserve_cost'] > remaining: reason = 'insufficient unreserved budget'
        if reason:
            blocked.append({'id': tid, 'reason': reason})
        else:
            remaining -= task['reserve_cost']; ready.append(tid)
    return {'ready': ready, 'blocked': blocked, 'remaining_after_proposed_reservations': remaining,
            'currency': budget['currency'], 'merge_ready': all(t['status'] == 'accepted' for t in tasks),
            'evidence_verified': False, 'execution_performed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        result = inspect(json.loads(args.plan.read_text(encoding='utf-8')))
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False)); return 2
    print(json.dumps({'valid': True, **result}, ensure_ascii=False, indent=2)); return 0


if __name__ == '__main__':
    raise SystemExit(main())
