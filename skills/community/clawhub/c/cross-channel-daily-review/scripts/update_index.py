#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load_or_init(path: Path):
    if path.exists():
        data = json.loads(path.read_text(encoding='utf-8'))
    else:
        data = {'records': [], 'weekly': [], 'monthly': [], 'archives': [], 'retention': {'daily_keep_current_months': 2, 'weekly_keep_months': 12, 'monthly_keep_forever': True}}
    data.setdefault('records', [])
    data.setdefault('weekly', [])
    data.setdefault('monthly', [])
    data.setdefault('archives', [])
    data.setdefault('retention', {'daily_keep_current_months': 2, 'weekly_keep_months': 12, 'monthly_keep_forever': True})
    return data


def upsert(items, key_name, record):
    items = [r for r in items if r.get(key_name) != record.get(key_name)]
    items.append(record)
    items.sort(key=lambda x: x.get(key_name, ''))
    return items


def main() -> int:
    if len(sys.argv) != 3:
        print('usage: update_index.py <index.json> <record.json>', file=sys.stderr)
        return 2
    index_path = Path(sys.argv[1])
    record = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    data = load_or_init(index_path)
    if 'date' in record:
        data['records'] = upsert(data['records'], 'date', record)
        updated_key = record.get('date')
    elif 'week_id' in record:
        data['weekly'] = upsert(data['weekly'], 'week_id', record)
        updated_key = record.get('week_id')
    elif 'month_id' in record:
        data['monthly'] = upsert(data['monthly'], 'month_id', record)
        updated_key = record.get('month_id')
    elif 'archive_month' in record:
        data['archives'] = upsert(data['archives'], 'archive_month', record)
        updated_key = record.get('archive_month')
    else:
        raise SystemExit('record must contain date or week_id or month_id or archive_month')
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'records': len(data['records']), 'weekly': len(data['weekly']), 'monthly': len(data['monthly']), 'updated_key': updated_key}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
