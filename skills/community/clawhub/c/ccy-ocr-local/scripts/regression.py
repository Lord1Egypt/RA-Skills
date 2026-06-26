#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'local_ocr.py'
ASSETS = ROOT / 'assets'
OUT_DIR = ROOT / 'tmp' / 'regression'
BASELINES = {
    'sample-eng': {
        'path': ASSETS / 'sample-eng.png',
        'lang': 'eng',
        'mode': 'balanced',
    },
    'sample-mixed': {
        'path': ASSETS / 'sample-mixed.png',
        'lang': 'chi_sim+eng',
        'mode': 'balanced',
    },
}


def run_one(name: str, cfg: dict) -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(cfg['path']),
            '--lang',
            cfg['lang'],
            '--mode',
            cfg['mode'],
        ],
        capture_output=True,
        text=True,
    )
    text = proc.stdout.strip()
    return {
        'name': name,
        'returncode': proc.returncode,
        'stderr': proc.stderr.strip(),
        'text': text,
        'chars': len(text),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []

    for name, cfg in BASELINES.items():
        result = run_one(name, cfg)
        out_txt = OUT_DIR / f'{name}.txt'
        out_txt.write_text(result['text'], encoding='utf-8')
        summary.append({k: v for k, v in result.items() if k != 'text'})

    summary_path = OUT_DIR / 'summary.json'
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'Wrote outputs to: {OUT_DIR}')
    print(f'Summary: {summary_path}')
    for row in summary:
        print(f"{row['name']}\trc={row['returncode']}\tchars={row['chars']}")


if __name__ == '__main__':
    main()
