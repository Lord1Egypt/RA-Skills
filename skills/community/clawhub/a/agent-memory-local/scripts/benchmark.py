#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
CLI = BASE / 'agent_memory_local.py'
CASES = BASE.parent / 'references' / 'regression-cases.json'
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


def run_case(case: dict) -> dict:
    mode = case.get('mode', 'smart-query')
    query = case['query']
    top_k = int(case.get('top_k', 5))
    cmd = [*python_cmd(), str(CLI), '--workspace', str(WORKSPACE), mode, query, '-k', str(top_k)]
    payload = json.loads(subprocess.check_output(cmd, text=True))
    results = payload.get('results') or []
    expect_file = [x.lower() for x in case.get('expect_any_file_contains', [])]
    expect_text = [x.lower() for x in case.get('expect_any_text_contains', [])]

    matched_file = False
    matched_text = False
    for item in results:
        file_text = (item.get('file') or '').lower()
        snippet = f"{item.get('title','')}\n{item.get('text','')}".lower()
        if expect_file and any(x in file_text for x in expect_file):
            matched_file = True
        if expect_text and any(x in snippet for x in expect_text):
            matched_text = True
    passed = (not expect_file or matched_file) and (not expect_text or matched_text) and bool(results)
    return {
        'name': case['name'],
        'mode': mode,
        'query': query,
        'passed': passed,
        'used_query': payload.get('used_query', query),
        'result_count': len(results),
        'matched_file': matched_file,
        'matched_text': matched_text,
        'top_file': (results[0] if results else {}).get('file'),
    }


def main() -> int:
    cases = json.loads(CASES.read_text(encoding='utf-8'))
    results = [run_case(case) for case in cases]
    passed = sum(1 for r in results if r['passed'])
    payload = {
        'ok': passed == len(results),
        'passed': passed,
        'total': len(results),
        'results': results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
