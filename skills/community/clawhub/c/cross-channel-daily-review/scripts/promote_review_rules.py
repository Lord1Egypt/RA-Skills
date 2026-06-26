#!/usr/bin/env python3
import argparse
from pathlib import Path


def extract_rules(text: str):
    rules = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith('- '):
            continue
        body = s[2:].strip()
        if not body:
            continue
        if any(x in body for x in ['补强', '必须', '只保留', '直说', '为准']):
            rules.append(body)
    out = []
    seen = set()
    for r in rules:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('review')
    ap.add_argument('output')
    ap.add_argument('--date', required=True)
    args = ap.parse_args()

    review = Path(args.review).read_text(encoding='utf-8')
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = out.read_text(encoding='utf-8') if out.exists() else '# 复盘沉淀规则\n\n'
    existing_lines = set(x.strip('- ').strip() for x in existing.splitlines() if x.startswith('- '))

    rules = [r for r in extract_rules(review) if r not in existing_lines]
    if not rules:
        print('NO_NEW_RULES')
        return 0

    block = [f'## {args.date}', ''] + [f'- {r}' for r in rules] + ['']
    out.write_text(existing + '\n'.join(block), encoding='utf-8')
    print(f'ADDED {len(rules)} RULES -> {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
