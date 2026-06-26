#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

from paths import favorites_paths

PATHS = favorites_paths()
SNAPSHOT_DIR = PATHS['snapshots_dir']
REPORT_DIR = PATHS['reports_dir']


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def load_snapshots():
    snapshots = sorted(
        [path for path in SNAPSHOT_DIR.glob('*.json') if path.name != 'latest.json'],
        key=lambda p: p.name,
    )
    if not snapshots:
        raise SystemExit('No snapshots found. Run scan_favorites.py first.')
    current = load_json(snapshots[-1])
    previous = load_json(snapshots[-2]) if len(snapshots) >= 2 else {'entries': {}}
    return current, previous, snapshots[-1]


def compute_changes(current, previous):
    current_entries = current.get('entries', {})
    previous_entries = previous.get('entries', {})
    new_ids = sorted(set(current_entries) - set(previous_entries))
    updated_ids = []
    for item_id in sorted(set(current_entries) & set(previous_entries)):
        before = previous_entries[item_id]
        after = current_entries[item_id]
        changed = []
        for key in (
            'update_time', 'summary', 'simple_usage', 'source_url', 'install_path', 'score',
            'merged_from_count', 'content_diff_status', 'variant_source_names'
        ):
            if before.get(key) != after.get(key):
                changed.append(key)
        if changed:
            updated_ids.append((item_id, changed))
    return new_ids, updated_ids


def similar_pairs(entries):
    items = list(entries.values())
    pairs = []
    for i, left in enumerate(items):
        for right in items[i + 1:]:
            if left['item_id'] == right['item_id']:
                continue
            score = similarity_score(left, right)
            if score >= 0.72:
                pairs.append((score, left, right))
    pairs.sort(key=lambda item: item[0], reverse=True)
    return pairs[:12]


def similarity_score(left, right):
    if left.get('canonical_source_url') and left.get('canonical_source_url') == right.get('canonical_source_url'):
        return 1.0
    left_name = normalize(left['name'])
    right_name = normalize(right['name'])
    ratio = SequenceMatcher(None, left_name, right_name).ratio()
    left_tail = Path(left['install_path']).name.lower()
    right_tail = Path(right['install_path']).name.lower()
    if left_tail and left_tail == right_tail:
        ratio = max(ratio, 0.9)
    left_tokens = set(left_name.split('-'))
    right_tokens = set(right_name.split('-'))
    if left_tokens and right_tokens:
        overlap = len(left_tokens & right_tokens) / max(len(left_tokens), len(right_tokens))
        ratio = max(ratio, overlap)
    return ratio


def normalize(value):
    return ''.join(ch.lower() if ch.isalnum() else '-' for ch in value).strip('-')


def notable_items(entries):
    items = sorted(entries.values(), key=lambda item: (-item.get('score', 0), item['name'].lower()))
    result = []
    for item in items:
        reasons = item.get('notable_reason', '')
        if 'content-diff-alert' in reasons or item.get('score', 0) >= 6:
            result.append(item)
    result.sort(key=lambda item: ('content-diff-alert' not in item.get('notable_reason', ''), -item.get('score', 0), item['name'].lower()))
    return result[:12]


def merged_results(entries):
    merged = [item for item in entries.values() if item.get('merged_from_count', 1) > 1]
    merged.sort(key=lambda item: (-item.get('merged_from_count', 1), item['name'].lower()))
    return merged[:20]


def content_diff_alerts(entries):
    alerts = [item for item in entries.values() if 'different' in item.get('content_diff_status', '')]
    alerts.sort(key=lambda item: (-item.get('merged_from_count', 1), -item.get('score', 0), item['name'].lower()))
    return alerts[:20]


def render_report(current, previous, snapshot_path):
    entries = current.get('entries', {})
    new_ids, updated_ids = compute_changes(current, previous)
    pairs = similar_pairs(entries)
    notable = notable_items(entries)
    merged = merged_results(entries)
    diff_alerts = content_diff_alerts(entries)
    generated_at = current.get('generated_at', datetime.now().astimezone().isoformat())
    lines = [
        f'# Favorites Daily Digest - {generated_at[:10]}',
        '',
        f'- snapshot: `{snapshot_path.name}`',
        f'- total entries: {current.get("entry_count", len(entries))}',
        f'- new entries: {len(new_ids)}',
        f'- updated entries: {len(updated_ids)}',
        f'- merged entries: {sum(1 for item in entries.values() if item.get("merged_from_count", 1) > 1)}',
        f'- content diff alerts: {len(diff_alerts)}',
        '',
        '## New Entries',
        '',
    ]
    if new_ids:
        for item_id in new_ids[:50]:
            item = entries[item_id]
            lines.append(f'- `{item["data_type"]}` `{item["name"]}` from `{", ".join(item.get("variant_source_names", []))}`')
    else:
        lines.append('- None')
    lines.extend(['', '## Updated Entries', ''])
    if updated_ids:
        for item_id, changed in updated_ids[:50]:
            item = entries[item_id]
            lines.append(f'- `{item["name"]}` changed: {", ".join(changed)}')
    else:
        lines.append('- None')
    lines.extend(['', '## Merge Results', ''])
    if merged:
        for item in merged:
            lines.append(
                f'- {item["name"]}: merged {item["merged_from_count"]} variants across {", ".join(item.get("variant_source_names", []))}'
            )
    else:
        lines.append('- None')
    lines.extend(['', '## Content Diff Alerts', ''])
    if diff_alerts:
        for item in diff_alerts:
            lines.append(
                f'- {item["name"]}: {item.get("content_diff_status", "")}; review {len(item.get("variants", []))} variants'
            )
    else:
        lines.append('- None')
    lines.extend(['', '## Similar Items To Review', ''])
    if pairs:
        for score, left, right in pairs:
            lines.append(
                f'- {left["name"]} <-> {right["name"]} (score {score:.2f}; {left["data_type"]} vs {right["data_type"]})'
            )
    else:
        lines.append('- None')
    lines.extend(['', '## Notable Items Worth Surfacing', ''])
    if notable:
        for item in notable:
            reason = item.get('notable_reason', 'high-signal')
            lines.append(f'- {item["name"]}: {reason}; {item.get("summary", "")}'.rstrip())
    else:
        lines.append('- None')
    return '\n'.join(lines) + '\n'


def write_report(text, snapshot_path):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = snapshot_path.stem.split('-')[0]
    out = REPORT_DIR / f'digest-{stamp}.md'
    out.write_text(text, encoding='utf-8')
    latest = REPORT_DIR / 'latest-digest.md'
    latest.write_text(text, encoding='utf-8')
    return out


def main():
    parser = argparse.ArgumentParser(description='Generate a daily favorites digest from snapshots.')
    parser.parse_args()
    current, previous, snapshot_path = load_snapshots()
    text = render_report(current, previous, snapshot_path)
    out = write_report(text, snapshot_path)
    print(f'Report: {out}')
    print(text)


if __name__ == '__main__':
    main()
