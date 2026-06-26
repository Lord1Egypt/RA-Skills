#!/usr/bin/env python3
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


def scan_file(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    task_id = None
    agent = None
    for line in text.splitlines():
        if line.startswith('task_id:'):
            task_id = line.split(':', 1)[1].strip()
        elif line.startswith('agent:'):
            agent = line.split(':', 1)[1].strip()
    if not task_id:
        m = re.search(r'TASK-\d+', text)
        if m:
            task_id = m.group(0)
    return task_id, agent or path.stem


def main():
    parser = argparse.ArgumentParser(description='Detect multiple claims for the same task.')
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    claims = defaultdict(list)
    for raw in args.paths:
        path = Path(raw)
        task_id, agent = scan_file(path)
        if task_id:
            claims[task_id].append((agent, path))
    conflict = False
    for task_id, items in sorted(claims.items()):
        if len(items) > 1:
            conflict = True
            print(f'CONFLICT {task_id}')
            for agent, path in items:
                print(f'  - {agent}: {path}')
        else:
            agent, path = items[0]
            print(f'OK {task_id}: {agent} ({path})')
    return 1 if conflict else 0


if __name__ == '__main__':
    raise SystemExit(main())
