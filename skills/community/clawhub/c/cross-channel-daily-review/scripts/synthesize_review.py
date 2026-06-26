#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fmt(items, fallback='- 无', limit=4):
    items = (items or [fallback])[:limit]
    cleaned = []
    for x in items:
        s = str(x).strip().replace('\n', ' ')
        if len(s) > 120:
            s = s[:117] + '...'
        cleaned.append(f'- {s}' if not s.startswith('-') else s)
    return '\n'.join(cleaned)


def main() -> int:
    if len(sys.argv) != 4:
        print('usage: synthesize_review.py <normalized.json> <template.md> <output.md>', file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    template = Path(sys.argv[2]).read_text(encoding='utf-8')
    if not data:
        raise SystemExit('no normalized data')
    date = data[0].get('date', '')
    overview = []
    weaknesses = []
    wins = []
    misses = []
    improvements = []
    mistakes = []
    for item in data:
        label = item.get('channel_label') or item['channel']
        status = item.get('status')
        sessions = item.get('session_count', 0)
        overview.append(f"{label}｜{status}｜sessions={sessions}")
        if status != 'active':
            weaknesses.append(f"{label} 未强确认：{item.get('missing_reason') or status}")
            improvements.append(f"补强 {label} 的元数据发现与校验")
        else:
            wins.append(f"{label} 已确认，可纳入高可信输入")
        if item.get('scope_type') == 'unknown':
            misses.append(f"{label} scope 仍未知")
        if sessions > 1:
            wins.append(f"{label} 已支持多 session 聚合")
    if not mistakes:
        mistakes.append('早期版本按 channel 扁平建模，scope / 多 session 约束不够强。')
    text = template
    text = text.replace('{{date}}', date)
    text = text.replace('{{channels_overview}}', fmt(overview))
    text = text.replace('{{mistakes}}', fmt(mistakes))
    text = text.replace('{{weaknesses}}', fmt(weaknesses))
    text = text.replace('{{wins}}', fmt(wins))
    text = text.replace('{{misses}}', fmt(misses))
    text = text.replace('{{improvements}}', fmt(improvements))
    out = Path(sys.argv[3])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    print(json.dumps({'output': str(out), 'date': date, 'channels': len(data)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
