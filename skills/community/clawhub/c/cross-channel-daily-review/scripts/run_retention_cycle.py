#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {'cmd': cmd, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}


def main() -> int:
    if len(sys.argv) != 4:
        print('usage: run_retention_cycle.py <index.json> <today-YYYY-MM-DD> <archive-root>', file=sys.stderr)
        return 2
    index_path = Path(sys.argv[1])
    today = sys.argv[2]
    archive_root = Path(sys.argv[3])
    base = Path(__file__).resolve().parent
    tmp_dir = archive_root.parent / '.retention-tmp'
    tmp_dir.mkdir(parents=True, exist_ok=True)
    candidate_path = tmp_dir / 'retention-candidate.json'

    step1 = subprocess.run([sys.executable, str(base / 'plan_retention.py'), str(index_path), today], capture_output=True, text=True)
    if step1.returncode != 0:
        print(json.dumps({'ok': False, 'step': 'plan_retention', 'stderr': step1.stderr}, ensure_ascii=False, indent=2))
        return 1
    candidate_path.write_text(step1.stdout, encoding='utf-8')
    candidate = json.loads(step1.stdout)

    months = sorted({x['month'] for x in candidate.get('archive_candidates', [])})
    all_steps = []
    for month_id in months:
        ready = run([sys.executable, str(base / 'verify_retention_readiness.py'), str(index_path), str(candidate_path), month_id])
        all_steps.append({'month_id': month_id, 'ready': ready})
        if ready['returncode'] != 0:
            continue
        archive = run([sys.executable, str(base / 'archive_daily_layer.py'), str(candidate_path), month_id, str(archive_root)])
        mark = run([sys.executable, str(base / 'mark_archived_records.py'), str(index_path), str(candidate_path), month_id])
        all_steps[-1]['archive'] = archive
        all_steps[-1]['mark'] = mark
    print(json.dumps({'ok': True, 'today': today, 'months': months, 'steps': all_steps}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
