#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


def month_key(date_str: str) -> str:
    return date_str[:7]


def main() -> int:
    if len(sys.argv) != 3:
        print('usage: plan_retention.py <index.json> <today-YYYY-MM-DD>', file=sys.stderr)
        return 2
    index = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if Path(sys.argv[1]).exists() else {'records': []}
    today = datetime.fromisoformat(sys.argv[2])
    keep_months = {today.strftime('%Y-%m')}
    prev_month = (today.replace(day=1).month - 1) or 12
    prev_year = today.year if today.month > 1 else today.year - 1
    keep_months.add(f'{prev_year:04d}-{prev_month:02d}')

    archive_candidates = []
    for rec in index.get('records', []):
        d = rec.get('date')
        if not d:
            continue
        mk = month_key(d)
        if mk not in keep_months:
            archive_candidates.append({
                'date': d,
                'month': mk,
                'raw_files': rec.get('raw_files', []),
                'synthesized_file': rec.get('synthesized_file'),
                'boss_summary_file': rec.get('boss_summary_file'),
                'active_channels': rec.get('active_channels', []),
                'missing_channels': rec.get('missing_channels', []),
            })
    print(json.dumps({
        'today': sys.argv[2],
        'keep_months': sorted(keep_months),
        'archive_candidates': archive_candidates
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
