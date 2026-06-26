#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path


def archive_one(path_str: str, archive_root: Path):
    if not path_str:
        return None
    src = Path(path_str)
    if not src.exists():
        return {'source': path_str, 'status': 'missing'}
    rel = src.as_posix().split('memory/daily-review/')[-1] if 'memory/daily-review/' in src.as_posix() else src.name
    dst = archive_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {'source': str(src), 'archived_to': str(dst), 'status': 'archived'}


def main() -> int:
    if len(sys.argv) != 4:
        print('usage: archive_daily_layer.py <candidate.json> <month-id> <archive-root>', file=sys.stderr)
        return 2
    candidate = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    month_id = sys.argv[2]
    archive_root = Path(sys.argv[3])
    actions = []
    for item in candidate.get('archive_candidates', []):
        if item.get('month') != month_id:
            continue
        for raw in item.get('raw_files', []) or []:
            act = archive_one(raw, archive_root / month_id)
            if act:
                actions.append(act)
        for key in ('synthesized_file', 'boss_summary_file'):
            act = archive_one(item.get(key), archive_root / month_id)
            if act:
                actions.append(act)
    print(json.dumps({'month_id': month_id, 'actions': actions}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
