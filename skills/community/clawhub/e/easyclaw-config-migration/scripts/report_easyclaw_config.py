#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

HOME = Path.home()
DESKTOP_CFG = HOME / 'Library' / 'Application Support' / '@cfmind' / 'easyclaw' / 'easyclaw.json'
BRIDGE_CFG = HOME / '.openclaw' / 'easyclaw.json'
OPENCLAW_CFG = HOME / '.openclaw' / 'openclaw.json'


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if any(s in k.lower() for s in ('token', 'secret', 'key', 'password')):
                if isinstance(v, str) and v:
                    out[k] = f'<redacted:{len(v)} chars>'
                else:
                    out[k] = '<redacted>'
            else:
                out[k] = redact(v)
        return out
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def get_path(data: dict[str, Any] | None, path: str) -> Any:
    cur: Any = data
    for part in path.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def print_json(title: str, value: Any) -> None:
    print(f'\n## {title}')
    print(json.dumps(redact(value), indent=2, ensure_ascii=False))


def main() -> int:
    desktop = load_json(DESKTOP_CFG)
    bridge = load_json(BRIDGE_CFG)
    openclaw = load_json(OPENCLAW_CFG)

    print('# EasyClaw / OpenClaw config report')
    for path in (DESKTOP_CFG, BRIDGE_CFG, OPENCLAW_CFG):
        print(f'- {path}: {'FOUND' if path.exists() else 'MISSING'}')

    if desktop is not None:
        print_json('EasyClaw desktop config (redacted)', desktop)
    if bridge is not None:
        print_json('EasyClaw bridge config (redacted)', bridge)
    if openclaw is not None:
        print_json('OpenClaw config (redacted excerpt)', {
            'commands': openclaw.get('commands'),
            'gateway': openclaw.get('gateway'),
            'channels': openclaw.get('channels'),
            'plugins': openclaw.get('plugins'),
        })

    migratable = [
        'commands.native',
        'commands.nativeSkills',
        'commands.restart',
        'gateway.mode',
        'gateway.auth.mode',
        'gateway.auth.token',
        'gateway.remote.token',
    ]

    print('\n## Migratable / reportable fields from ~/.openclaw/easyclaw.json')
    if bridge is None:
        print('Bridge config missing; nothing to compare.')
    else:
        for key in migratable:
            src = get_path(bridge, key)
            dst = get_path(openclaw or {}, key)
            print(f'- {key}: source={redact(src)!r} target={redact(dst)!r}')

    if desktop is not None:
        print('\n## Desktop-only fields worth noting')
        desktop_only = {
            'app': desktop.get('app'),
            'window': desktop.get('window'),
            'analytics': desktop.get('analytics'),
            'update': desktop.get('update'),
            'gateway': desktop.get('gateway'),
        }
        print(json.dumps(redact(desktop_only), indent=2, ensure_ascii=False))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
