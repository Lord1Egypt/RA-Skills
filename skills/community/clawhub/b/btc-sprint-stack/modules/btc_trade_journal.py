from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def ensure_data_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_journal(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def append_journal(path: Path, row: dict) -> None:
    ensure_data_dir(path)
    with path.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(row, sort_keys=True) + '\n')
