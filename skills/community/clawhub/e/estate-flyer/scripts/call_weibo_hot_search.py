#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def load_runtime(skill_dir: Path):
    runtime_path = skill_dir / 'config' / 'runtime.json'
    if runtime_path.exists():
        try:
            return json.loads(runtime_path.read_text(encoding='utf-8'))
        except Exception:
            pass
    example_path = skill_dir / 'config' / 'runtime.example.json'
    return json.loads(example_path.read_text(encoding='utf-8'))


def build_command(skill_dir: Path, limit: int):
    runtime = load_runtime(skill_dir)
    cfg = runtime.get('weibo_hot_search', {})
    mode = cfg.get('mode', 'bundled')
    if mode == 'external_command' and cfg.get('command'):
        cmd = cfg['command']
    else:
        cmd = f"node {skill_dir / 'vendor' / 'weibo-hot-trend' / 'scripts' / 'weibo.js'} {limit}"
    cmd = cmd.replace('{skill_dir}', str(skill_dir)).replace('{limit}', str(limit))
    timeout = int(cfg.get('timeout_sec', 60))
    return cmd, timeout


def parse_output(text: str):
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    fetched_at = None
    items = []
    current = None
    rank_pat = re.compile(r'^(\d+)\.\s+(.*)$')
    hot_pat = re.compile(r'^🔥\s*热度:\s*(.*)$')
    for line in lines:
        if '更新时间:' in line:
            fetched_at = line.split('更新时间:', 1)[1].strip()
            continue
        m = rank_pat.match(line)
        if m:
            if current:
                items.append(current)
            title = m.group(2).strip()
            current = {'rank': int(m.group(1)), 'title': title, 'hot': '', 'url': ''}
            continue
        if current:
            hm = hot_pat.match(line)
            if hm:
                current['hot'] = hm.group(1).strip()
                continue
            if line.startswith('🔗'):
                current['url'] = line.replace('🔗', '').strip()
                continue
    if current:
        items.append(current)
    return fetched_at, items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    cmd, timeout = build_command(skill_dir, args.limit)
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        print(json.dumps({'ok': False, 'command': cmd, 'stderr': proc.stderr.strip(), 'stdout': proc.stdout.strip()}, ensure_ascii=False, indent=2))
        sys.exit(proc.returncode)

    fetched_at, items = parse_output(proc.stdout)
    if not fetched_at:
        fetched_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = {
        'ok': True,
        'source': 'bundled weibo-hot-trend',
        'command': cmd,
        'fetched_at': fetched_at,
        'count': len(items),
        'items': items[: args.limit],
        'raw_stdout': proc.stdout.strip()
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
