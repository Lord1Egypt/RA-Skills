#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
ASSETS = ROOT / 'assets'


def run(cmd):
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', required=True)
    ap.add_argument('--sessions-dir', required=True)
    ap.add_argument('--date')
    ap.add_argument('--window-hours', type=int, default=24)
    ap.add_argument('--expected', default='web,telegram,feishu,qq')
    ap.add_argument('--sessions-list-json')
    args = ap.parse_args()

    workspace = Path(args.workspace)
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    yyyy, mm, _ = date.split('-')

    tmp = workspace / 'tmp' / 'daily-review'
    tmp.mkdir(parents=True, exist_ok=True)
    discovered = tmp / f'discovered-{date}.json'
    normalized = tmp / f'normalized-{date}.json'
    record = tmp / f'record-{date}.json'
    manifest = tmp / f'manifest-{date}.json'

    raw_root = workspace / 'memory' / 'daily-review' / 'raw'
    synth_file = workspace / 'memory' / 'daily-review' / 'synthesized' / yyyy / mm / f'{date}.md'
    index_file = workspace / 'memory' / 'daily-review' / 'index.json'

    discover_cmd = [
        sys.executable, str(SCRIPTS / 'discover_channels.py'),
        '--sessions-dir', args.sessions_dir,
        '--date', date,
        '--window-hours', str(args.window_hours),
        '--expected', args.expected,
        '--output', str(discovered),
    ]
    if args.sessions_list_json:
        discover_cmd.extend(['--sessions-list-json', args.sessions_list_json])
    run(discover_cmd)

    run([sys.executable, str(SCRIPTS / 'normalize_channel_data.py'), str(discovered), str(normalized)])
    run([sys.executable, str(SCRIPTS / 'write_raw_reviews.py'), str(normalized), str(ASSETS / 'raw-template.md'), str(raw_root)])
    run([sys.executable, str(SCRIPTS / 'synthesize_review.py'), str(normalized), str(ASSETS / 'synthesized-template.md'), str(synth_file)])

    data = json.loads(normalized.read_text(encoding='utf-8'))
    active = [x['channel'] for x in data if x.get('status') == 'active']
    missing = [x['channel'] for x in data if x.get('status') != 'active']
    raw_files = [str(raw_root / yyyy / mm / f"{x['channel']}_{date}.md") for x in data]
    rec = {
        'date': date,
        'channels_active': active,
        'channels_missing': missing,
        'synthesized_file': f'synthesized/{yyyy}/{mm}/{date}.md',
        'raw_files': [f'raw/{yyyy}/{mm}/{x["channel"]}_{date}.md' for x in data],
        'status': 'completed' if synth_file.exists() and synth_file.stat().st_size > 0 else 'failed',
        'last_updated': datetime.now().isoformat(),
    }
    record.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding='utf-8')
    run([sys.executable, str(SCRIPTS / 'update_index.py'), str(index_file), str(record)])

    manifest.write_text(json.dumps({
        'raw_files': raw_files,
        'synthesized_file': str(synth_file),
        'index_file': str(index_file)
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    run([sys.executable, str(SCRIPTS / 'verify_outputs.py'), str(manifest)])

    rules_file = workspace / 'memory' / 'daily-review' / 'rules.md'
    run([sys.executable, str(SCRIPTS / 'promote_review_rules.py'), str(synth_file), str(rules_file), '--date', date])

    print(json.dumps({
        'date': date,
        'discovered': str(discovered),
        'normalized': str(normalized),
        'synthesized_file': str(synth_file),
        'index_file': str(index_file),
        'raw_files': raw_files,
        'active_channels': active,
        'missing_channels': missing,
        'status': 'ok'
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
