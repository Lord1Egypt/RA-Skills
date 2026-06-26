from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime


class JsonStore:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def append_jsonl(self, relative: str, item: dict):
        path = self.base_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    def read_jsonl(self, relative: str) -> list[dict]:
        path = self.base_dir / relative
        if not path.exists():
            return []
        rows = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def write_report(self, relative: str, content: str) -> Path:
        path = self.base_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path


def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
