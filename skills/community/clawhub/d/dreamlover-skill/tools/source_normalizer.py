from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_text(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def paragraph_entries(lines: list[str], source_type: str) -> list[dict]:
    entries: list[dict] = []
    buffer: list[str] = []
    start = 1
    kind = {"manual": "note", "wiki": "summary", "plot": "event"}.get(source_type, "note")
    for idx, line in enumerate(lines, start=1):
        if line.strip():
            if not buffer:
                start = idx
            buffer.append(line.rstrip())
            continue
        if buffer:
            entries.append(make_entry(source_type, kind, start, idx - 1, buffer, len(entries) + 1))
            buffer = []
    if buffer:
        entries.append(make_entry(source_type, kind, start, len(lines), buffer, len(entries) + 1))
    return entries


def quote_entries(lines: list[str], source_type: str) -> list[dict]:
    entries: list[dict] = []
    for idx, line in enumerate(lines, start=1):
        text = line.strip()
        if not text:
            continue
        entries.append(make_entry(source_type, "quote", idx, idx, [text], len(entries) + 1))
    return entries


def make_entry(source_type: str, kind: str, line_start: int, line_end: int, content: Iterable[str], index: int) -> dict:
    return {
        "entry_id": f"{source_type}-{index:03d}",
        "source_type": source_type,
        "kind": kind,
        "line_start": line_start,
        "line_end": line_end,
        "text": "\n".join(content).strip(),
    }


def normalize(path: Path, source_type: str) -> dict:
    lines = load_text(path)
    if source_type == "quotes":
        entries = quote_entries(lines, source_type)
    else:
        entries = paragraph_entries(lines, source_type)
    return {
        "schema_version": "0.1",
        "source": {
            "source_type": source_type,
            "input_path": str(path),
            "normalized_at": utc_now(),
        },
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize text source material into JSON entries.")
    parser.add_argument("--input", required=True, help="Path to a UTF-8 text source.")
    parser.add_argument("--type", required=True, choices=["manual", "wiki", "quotes", "plot"], help="Source type.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    payload = normalize(Path(args.input), args.type)
    content = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(content + "\n", encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
