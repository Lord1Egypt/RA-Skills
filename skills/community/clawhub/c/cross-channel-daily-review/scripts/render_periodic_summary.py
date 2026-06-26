#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fmt(items, fallback='- 无'):
    items = items or [fallback]
    return '\n'.join(f'- {x}' if not str(x).startswith('-') else str(x) for x in items)


def main() -> int:
    if len(sys.argv) != 5:
        print('usage: render_periodic_summary.py <records.json> <template.md> <kind:weekly|monthly> <output.md>', file=sys.stderr)
        return 2
    records = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    template = Path(sys.argv[2]).read_text(encoding='utf-8')
    kind = sys.argv[3]
    out = Path(sys.argv[4])
    dates = [r.get('date') for r in records if r.get('date')]
    dates.sort()
    if not dates:
        raise SystemExit('no dates in records')
    headline = f'{kind} summary generated from {len(records)} daily records'
    patterns = []
    system_issues = []
    next_steps = []
    for r in records:
        ac = r.get('active_channels', [])
        mc = r.get('missing_channels', [])
        patterns.append(f"{r.get('date')}: active={','.join(ac) if ac else 'none'}")
        if mc:
            system_issues.append(f"{r.get('date')}: missing={','.join(mc)}")
    if kind == 'weekly':
        text = template.replace('{{week_id}}', f"{dates[0]}..{dates[-1]}")
        text = text.replace('{{date_range}}', f"{dates[0]} ~ {dates[-1]}")
        text = text.replace('{{headline}}', headline)
        text = text.replace('{{mistakes}}', fmt(system_issues))
        text = text.replace('{{progress}}', fmt(patterns))
        text = text.replace('{{next_steps}}', fmt(['继续压缩 discoverability gap', '继续上卷高价值模式']))
    else:
        month_id = dates[0][:7]
        text = template.replace('{{month_id}}', month_id)
        text = text.replace('{{date_range}}', f"{dates[0]} ~ {dates[-1]}")
        text = text.replace('{{headline}}', headline)
        text = text.replace('{{patterns}}', fmt(patterns))
        text = text.replace('{{system_issues}}', fmt(system_issues))
        text = text.replace('{{next_steps}}', fmt(['保留月报', '清理满足条件的旧日报层']))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    print(json.dumps({'output': str(out), 'kind': kind, 'records': len(records)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
