#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print('usage: mark_archived_records.py <index.json> <candidate.json> <month-id>', file=sys.stderr)
        return 2
    index_path = Path(sys.argv[1])
    candidate = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    month_id = sys.argv[3]
    data = json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else {'records': []}
    dates = {x.get('date') for x in candidate.get('archive_candidates', []) if x.get('month') == month_id}
    changed = 0
    for rec in data.get('records', []):
        if rec.get('date') in dates:
            rec['archived'] = True
            rec['archive_month'] = month_id
            changed += 1
    index_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'month_id': month_id, 'marked_records': changed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
