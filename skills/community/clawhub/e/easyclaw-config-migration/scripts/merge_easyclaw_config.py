#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

HOME = Path.home()
BRIDGE_CFG = HOME / '.openclaw' / 'easyclaw.json'
OPENCLAW_CFG = HOME / '.openclaw' / 'openclaw.json'

MAPPINGS = [
    ('commands.native', 'commands.native'),
    ('commands.nativeSkills', 'commands.nativeSkills'),
    ('commands.restart', 'commands.restart'),
    ('gateway.mode', 'gateway.mode'),
    ('gateway.auth.mode', 'gateway.auth.mode'),
    ('gateway.auth.token', 'gateway.auth.token'),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def get_path(data: dict[str, Any], path: str) -> Any:
    cur: Any = data
    for part in path.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def set_path(data: dict[str, Any], path: str, value: Any) -> None:
    cur: dict[str, Any] = data
    parts = path.split('.')
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def main() -> int:
    parser = argparse.ArgumentParser(description='Merge supported EasyClaw settings into OpenClaw config.')
    parser.add_argument('--apply', action='store_true', help='Write changes to ~/.openclaw/openclaw.json')
    args = parser.parse_args()

    if not BRIDGE_CFG.exists():
        raise SystemExit(f'Missing source config: {BRIDGE_CFG}')
    if not OPENCLAW_CFG.exists():
        raise SystemExit(f'Missing target config: {OPENCLAW_CFG}')

    source = load_json(BRIDGE_CFG)
    target = load_json(OPENCLAW_CFG)
    updated = deepcopy(target)

    changes: list[tuple[str, Any, Any]] = []
    for src_path, dst_path in MAPPINGS:
        src_value = get_path(source, src_path)
        if src_value is None:
            continue
        old_value = get_path(updated, dst_path)
        if old_value != src_value:
            set_path(updated, dst_path, src_value)
            changes.append((dst_path, old_value, src_value))

    if not changes:
        print('No changes needed.')
        return 0

    print('Planned changes:')
    for path, old, new in changes:
        print(f'- {path}: {old!r} -> {new!r}')

    if not args.apply:
        print('\nDry run only. Re-run with --apply to write changes.')
        return 0

    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = OPENCLAW_CFG.with_name(f'{OPENCLAW_CFG.name}.bak.easyclaw-{ts}')
    backup.write_text(json.dumps(target, indent=2, ensure_ascii=False) + '\n')
    OPENCLAW_CFG.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + '\n')

    print(f'\nBackup written to: {backup}')
    print(f'Updated: {OPENCLAW_CFG}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
