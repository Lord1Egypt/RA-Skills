#!/usr/bin/env python3
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'local_ocr.py'
ASSETS = ROOT / 'assets'
OUT_DIR = ROOT / 'tmp' / 'benchmark'

CASES = [
    {'name': 'sample-eng', 'path': ASSETS / 'sample-eng.png', 'lang': 'eng'},
    {'name': 'sample-mixed', 'path': ASSETS / 'sample-mixed.png', 'lang': 'chi_sim+eng'},
]

MODES = ['balanced', 'fast', 'accurate']


def run_case(case: dict, mode: str) -> dict:
    started = time.perf_counter()
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(case['path']),
            '--lang',
            case['lang'],
            '--mode',
            mode,
        ],
        capture_output=True,
        text=True,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        'case': case['name'],
        'mode': mode,
        'returncode': proc.returncode,
        'elapsed_ms': elapsed_ms,
        'stdout_chars': len(proc.stdout.strip()),
        'stderr': proc.stderr.strip(),
        'preview': proc.stdout.strip()[:200],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for case in CASES:
        for mode in MODES:
            rows.append(run_case(case, mode))

    out_path = OUT_DIR / 'benchmark.json'
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')

    print('case\tmode\tms\tchars\trc')
    for row in rows:
        print(f"{row['case']}\t{row['mode']}\t{row['elapsed_ms']}\t{row['stdout_chars']}\t{row['returncode']}")
    print(f'\nJSON: {out_path}')


if __name__ == '__main__':
    main()
