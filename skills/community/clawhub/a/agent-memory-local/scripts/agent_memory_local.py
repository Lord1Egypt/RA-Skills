#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
PY311 = Path(r'D:/Python311/python.exe')


def python_cmd() -> list[str]:
    if PY311.exists():
        return [str(PY311)]
    py = shutil.which('py')
    if py:
        return [py, '-3.11']
    if sys.executable:
        return [sys.executable]
    return [shutil.which('python') or 'python']


def run(script: str, *args: str, workspace: str = '') -> int:
    cmd = [*python_cmd(), str(BASE / script), *args]
    env = os.environ.copy()
    if workspace:
        env['AGENT_MEMORY_WORKSPACE'] = workspace
    return subprocess.call(cmd, env=env)


def main() -> int:
    p = argparse.ArgumentParser(description='agent-memory-local: local-first memory indexing and retrieval for agent workspaces')
    p.add_argument('--workspace', default='', help='explicit workspace root containing MEMORY.md / memory/*.md')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('build-index', help='build or rebuild the local memory index')

    q = sub.add_parser('query', help='run direct retrieval against the local index')
    q.add_argument('query')
    q.add_argument('-k', '--top-k', type=int, default=8)

    sq = sub.add_parser('smart-query', help='rewrite natural questions and pick the best retrieval query')
    sq.add_argument('query')
    sq.add_argument('-k', '--top-k', type=int, default=8)

    ex = sub.add_parser('explain', help='show a cleaner explanation of why hits matched')
    ex.add_argument('query')
    ex.add_argument('-k', '--top-k', type=int, default=5)
    ex.add_argument('--smart', action='store_true', help='run explain after smart-query rewriting')

    sub.add_parser('doctor', help='show workspace/index health and auto-rebuild status')

    args = p.parse_args()
    if args.cmd == 'build-index':
        return run('build_index.py', workspace=args.workspace)
    if args.cmd == 'query':
        return run('retrieve.py', args.query, str(args.top_k), workspace=args.workspace)
    if args.cmd == 'smart-query':
        return run('memory_query.py', args.query, str(args.top_k), workspace=args.workspace)
    if args.cmd == 'explain':
        extra = ['--smart'] if args.smart else []
        return run('explain.py', args.query, str(args.top_k), *extra, workspace=args.workspace)
    if args.cmd == 'doctor':
        return run('doctor.py', workspace=args.workspace)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
