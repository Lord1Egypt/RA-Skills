#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARCHIVE = ROOT / 'dist' / 'auto-proteomics.skill'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Check packaged skill for release residue')
    parser.add_argument('--archive', default=str(DEFAULT_ARCHIVE), help='Path to .skill archive')
    return parser.parse_args()


def forbidden_reason(name: str) -> str | None:
    lowered = name.lower()
    if '/examples/' in lowered and '/results/' in lowered:
        return 'demo results must not ship'
    if '/dist/' in lowered:
        return 'nested dist outputs must not ship'
    if '/.git/' in lowered:
        return 'git metadata must not ship'
    if '__pycache__/' in lowered or lowered.endswith('.pyc'):
        return 'python cache artifacts must not ship'
    if 'mock' in lowered:
        return 'mock residue must not ship'
    return None


def main() -> int:
    args = parse_args()
    archive = Path(args.archive).resolve()
    if not archive.exists():
        print(f'Missing archive: {archive}', file=sys.stderr)
        return 1

    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()

    bad: list[tuple[str, str]] = []
    for name in names:
        reason = forbidden_reason(name)
        if reason:
            bad.append((name, reason))

    if bad:
        print('Forbidden packaged entries found:', file=sys.stderr)
        for name, reason in bad:
            print(f'- {name}: {reason}', file=sys.stderr)
        return 1

    print(f'Archive check passed: {len(names)} entries in {archive}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
