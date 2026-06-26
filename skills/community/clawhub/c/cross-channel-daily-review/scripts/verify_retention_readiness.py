#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def month_from_date(date_str: str) -> str:
    return date_str[:7]


def main() -> int:
    if len(sys.argv) != 4:
        print('usage: verify_retention_readiness.py <index.json> <candidate.json> <month-id>', file=sys.stderr)
        return 2
    index = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if Path(sys.argv[1]).exists() else {}
    candidate = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    month_id = sys.argv[3]

    monthly_exists = any(x.get('month_id') == month_id for x in index.get('monthly', []))
    weekly_exists = any((x.get('week_id') or '').startswith(month_id[:4]) for x in index.get('weekly', []))
    has_candidates = any(x.get('month') == month_id for x in candidate.get('archive_candidates', []))

    result = {
        'month_id': month_id,
        'monthly_exists': monthly_exists,
        'weekly_exists': weekly_exists,
        'has_candidates': has_candidates,
        'ready': bool(monthly_exists and weekly_exists and has_candidates)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
