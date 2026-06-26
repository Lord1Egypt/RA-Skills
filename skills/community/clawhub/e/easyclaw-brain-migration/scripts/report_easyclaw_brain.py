#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HOME = Path.home()
SRC = HOME / '.easyclaw' / 'workspace'
DST = HOME / '.openclaw' / 'workspace'

FILES = [
    'AGENTS.md',
    'SOUL.md',
    'CORE-PRINCIPLE.md',
    'MEMORY.md',
    'USER.md',
    'IDENTITY.md',
    'HEARTBEAT.md',
    'docs/context-management.md',
]

DIRS = ['memory', '.memos']


def status(path: Path) -> str:
    return 'FOUND' if path.exists() else 'MISSING'


def main() -> int:
    print('# EasyClaw brain migration report')
    print(f'Source workspace: {SRC}')
    print(f'Target workspace: {DST}')

    print('\n## Core files')
    for rel in FILES:
        src = SRC / rel
        dst = DST / rel
        print(f'- {rel}: source={status(src)} target={status(dst)}')

    print('\n## Directories')
    for rel in DIRS:
        src = SRC / rel
        dst = DST / rel
        src_count = len(list(src.glob('**/*'))) if src.exists() else 0
        dst_count = len(list(dst.glob('**/*'))) if dst.exists() else 0
        print(f'- {rel}: source={status(src)} ({src_count} entries) target={status(dst)} ({dst_count} entries)')

    print('\n## Recommended actions')
    print('- Import MEMORY.md and memory/ into the current workspace.')
    print('- Stage AGENTS.md, SOUL.md, CORE-PRINCIPLE.md, HEARTBEAT.md, USER.md, and IDENTITY.md for review.')
    print('- Rebuild launchd/context automation as OpenClaw heartbeat/cron behavior instead of blindly copying plists.')

    launchagents = sorted((HOME / 'Library' / 'LaunchAgents').glob('com.easyclaw*.plist'))
    if launchagents:
        print('\n## Legacy automations detected')
        for p in launchagents:
            print(f'- {p}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
