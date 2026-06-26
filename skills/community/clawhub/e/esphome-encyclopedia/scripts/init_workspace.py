#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

SEED_FILES = {
    'inventory/access.md': '# ESPHome Access Inventory\n\nStore ESPHome dashboard, host, and access notes here.\n',
    'inventory/topology.md': '# ESPHome Topology\n\nStore environment-specific ESPHome node-role and deployment notes here.\n',
    'inventory/doc-index.md': '# ESPHome Cached Doc Index\n\nTrack especially useful cached ESPHome docs pages here when helpful.\n',
    'notes/devices/.gitkeep': '',
    'notes/components/.gitkeep': '',
    'notes/patterns/.gitkeep': '',
    'docs/esphome.io/.gitkeep': '',
}


def default_root() -> Path:
    return Path.cwd() / '.ESPHome-Encyclopedia'


def main() -> int:
    parser = argparse.ArgumentParser(description='Create/repair the .ESPHome-Encyclopedia workspace layout.')
    parser.add_argument('--root', default=str(default_root()), help='Data root to initialize (default: <cwd>/.ESPHome-Encyclopedia)')
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    for rel, content in SEED_FILES.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding='utf-8')
    print(root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
