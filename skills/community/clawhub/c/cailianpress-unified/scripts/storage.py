from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from models.schemas import ClsItem

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_SNAPSHOT_FILE = DEFAULT_DATA_DIR / "telegraph_snapshots.jsonl"


def ensure_data_dir(path: Path | None = None) -> Path:
    data_dir = path or DEFAULT_DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def append_snapshot(items: Iterable[ClsItem], path: Path | None = None) -> int:
    snapshot_path = path or DEFAULT_SNAPSHOT_FILE
    ensure_data_dir(snapshot_path.parent)
    count = 0
    with snapshot_path.open("a", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")
            count += 1
    return count


def load_snapshots(path: Path | None = None) -> list[dict]:
    snapshot_path = path or DEFAULT_SNAPSHOT_FILE
    if not snapshot_path.exists():
        return []
    rows: list[dict] = []
    with snapshot_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def dedupe_by_id_keep_latest(rows: list[dict]) -> list[dict]:
    latest: dict[int, dict] = {}
    for row in rows:
        row_id = row.get("id")
        if row_id is None:
            continue
        existing = latest.get(row_id)
        if existing is None or int(row.get("ctime") or 0) >= int(existing.get("ctime") or 0):
            latest[row_id] = row
    return sorted(latest.values(), key=lambda x: int(x.get("ctime") or 0), reverse=True)
