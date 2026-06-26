#!/usr/bin/env python3
import argparse
import json

from paths import favorites_paths

PATHS = favorites_paths()
SNAPSHOT_DIR = PATHS['snapshots_dir']
REPORT_DIR = PATHS['reports_dir']


def load_latest_snapshot():
    path = SNAPSHOT_DIR / 'latest.json'
    if not path.exists():
        raise SystemExit('Missing latest snapshot. Run scan_favorites.py first.')
    return json.loads(path.read_text(encoding='utf-8'))


def load_latest_report_names():
    report = REPORT_DIR / 'latest-digest.md'
    if not report.exists():
        return set()
    names = set()
    for line in report.read_text(encoding='utf-8').splitlines():
        if line.startswith('- ') and ': ' in line:
            names.add(line[2:].split(':', 1)[0].strip('`'))
    return names


def choose_items(snapshot, top):
    report_names = load_latest_report_names()
    items = list(snapshot.get('entries', {}).values())
    items.sort(
        key=lambda item: (
            'content-diff-alert' not in item.get('notable_reason', ''),
            -item.get('score', 0),
            -item.get('merged_from_count', 1),
            item['name'].lower(),
        )
    )
    chosen = []
    seen_names = set()
    for item in items:
        normalized_name = item['name'].strip().lower()
        if normalized_name in seen_names:
            continue
        if item['name'] in report_names or item.get('score', 0) >= 6 or 'content-diff-alert' in item.get('notable_reason', ''):
            chosen.append(item)
            seen_names.add(normalized_name)
        if len(chosen) >= top:
            break
    return chosen


def render_message(item):
    summary = item.get('summary', '').strip() or 'Useful local item.'
    reason = item.get('notable_reason', 'high-signal')
    usage = item.get('simple_usage', '').strip()
    variants = item.get('merged_from_count', 1)
    line = f'[favorites] {item["name"]} ({item["data_type"]}) is worth surfacing: {summary}'
    if variants > 1:
        line += f' | merged: {variants} variants'
    if 'different' in item.get('content_diff_status', ''):
        line += f' | alert: {item.get("content_diff_status")}'
    if usage:
        line += f' | try: {usage}'
    if reason:
        line += f' | why: {reason}'
    return line


def main():
    parser = argparse.ArgumentParser(description='Emit short notification copy for notable favorites.')
    parser.add_argument('--top', type=int, default=5)
    args = parser.parse_args()
    snapshot = load_latest_snapshot()
    items = choose_items(snapshot, args.top)
    if not items:
        print('No notable items found.')
        return
    for item in items:
        print(render_message(item))


if __name__ == '__main__':
    main()
