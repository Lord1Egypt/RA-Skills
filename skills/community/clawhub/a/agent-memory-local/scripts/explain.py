#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
RETRIEVE = BASE / 'retrieve.py'
MEMORY_QUERY = BASE / 'memory_query.py'
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


def run_json(script: Path, query: str, top_k: int) -> dict:
    out = subprocess.check_output([*python_cmd(), str(script), query, str(top_k)], text=True, env=os.environ.copy())
    return json.loads(out)


def summarize(payload: dict) -> dict:
    results = []
    for idx, item in enumerate(payload.get('results') or [], 1):
        explain = item.get('explain') or {}
        results.append({
            'rank': idx,
            'file': item.get('file'),
            'title': item.get('title'),
            'score': item.get('score'),
            'semantic': item.get('semantic'),
            'overlap': item.get('overlap'),
            'why_matched': {
                'overlap_terms': explain.get('overlap_terms') or [],
                'anchor_hits': explain.get('anchor_hits') or [],
                'recency': explain.get('recency'),
                'phrase_boost': explain.get('phrase_boost'),
                'weekday_boost': explain.get('weekday_boost'),
            },
            'snippet': item.get('text'),
        })
    return {
        'query': payload.get('query') or payload.get('used_query'),
        'used_query': payload.get('used_query'),
        'retried': payload.get('retried', False),
        'mode': payload.get('mode'),
        'index_status': payload.get('index_status'),
        'query_profile': payload.get('query_profile'),
        'rerank': payload.get('rerank'),
        'results': results,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: explain.py "query" [k] [--smart]', file=sys.stderr)
        return 2
    args = sys.argv[1:]
    smart = False
    if '--smart' in args:
        args.remove('--smart')
        smart = True
    query = args[0]
    top_k = int(args[1]) if len(args) > 1 else 5
    script = MEMORY_QUERY if smart else RETRIEVE
    payload = run_json(script, query, top_k)
    if smart:
        payload['query'] = query
    print(json.dumps(summarize(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
