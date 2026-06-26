#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
CLI = BASE / 'agent_memory_local.py'
WORKSPACE = BASE.parent.parent.parent
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


def run_json(*args: str) -> dict:
    out = subprocess.check_output([*python_cmd(), str(CLI), *args], text=True)
    return json.loads(out)


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    doctor = run_json('doctor')
    assert_true(bool(doctor.get('workspace')), 'doctor missing workspace')
    assert_true('index_status' in doctor, 'doctor missing index_status')

    built = run_json('build-index')
    assert_true(built.get('ok') is True, 'build-index did not return ok=true')
    assert_true(int(built.get('chunks', 0)) > 0, 'index chunks must be > 0')

    query = run_json('query', '记忆检索 主路由', '-k', '3')
    assert_true(query.get('mode') in {'vector', 'fallback'}, 'query mode invalid')
    assert_true(len(query.get('results', [])) >= 1, 'query returned no results')

    smart = run_json('smart-query', '飞书昨天为什么断联了', '-k', '3')
    assert_true(bool(smart.get('used_query')), 'smart-query missing used_query')
    assert_true(len(smart.get('attempted_queries', [])) >= 1, 'smart-query missing attempted queries')
    assert_true(len(smart.get('results', [])) >= 1, 'smart-query returned no results')

    explain_out = subprocess.check_output([
        *python_cmd(), str(CLI), '--workspace', str(WORKSPACE), 'explain', '飞书昨天为什么断联了', '--smart', '-k', '2'
    ], text=True)
    explain_payload = json.loads(explain_out)
    assert_true(len(explain_payload.get('results', [])) >= 1, 'explain returned no results')

    print(json.dumps({
        'ok': True,
        'doctor_status': doctor.get('index_status', {}).get('status'),
        'chunks': built.get('chunks'),
        'query_top_file': (query.get('results') or [{}])[0].get('file'),
        'smart_used_query': smart.get('used_query'),
        'explain_first_file': (explain_payload.get('results') or [{}])[0].get('file'),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except AssertionError as e:
        print(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
