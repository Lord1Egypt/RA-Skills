#!/usr/bin/env python3
"""Ingest all authorized content into raw_records.jsonl and source_summary.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable, List

from mbti_common import (
    detect_language_mix,
    iso_now,
    load_json,
    load_sqlite_rows,
    read_jsonl,
    resolve_path,
    shorten,
    split_into_segments,
    write_json,
    write_jsonl,
)


def stable_id(parts: Iterable[str]) -> str:
    digest = hashlib.sha1("||".join(parts).encode("utf-8")).hexdigest()
    return digest[:16]


def parse_session_record(line: Dict, source_path: Path) -> List[Dict]:
    records: List[Dict] = []
    if line.get("type") == "message" and isinstance(line.get("message"), dict):
        message = line["message"]
        role = message.get("role", "unknown")
        content_blocks = message.get("content", [])
        texts = []
        if isinstance(content_blocks, list):
            for block in content_blocks:
                if isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text", ""))
                elif isinstance(block, dict) and "text" in block:
                    texts.append(str(block["text"]))
                elif isinstance(block, str):
                    texts.append(block)
        elif isinstance(content_blocks, str):
            texts.append(content_blocks)
        content = "\n".join(part for part in texts if part).strip()
        if content:
            location = f"{source_path.name}:{line.get('id', 'message')}"
            records.append(
                {
                    "record_id": stable_id([str(source_path), location, content[:80]]),
                    "source_type": "openclaw-sessions",
                    "source_path": str(source_path),
                    "location": location,
                    "timestamp": line.get("timestamp") or message.get("created_at"),
                    "speaker": role,
                    "conversation_id": source_path.stem,
                    "content": content,
                }
            )
    return records


def ingest_workspace_long_memory(workspace_root: Path) -> List[Dict]:
    memory_md = workspace_root / "MEMORY.md"
    if not memory_md.exists():
        return []
    content = memory_md.read_text(encoding="utf-8")
    return [
        {
            "record_id": stable_id([str(memory_md), "MEMORY.md"]),
            "source_type": "workspace-long-memory",
            "source_path": str(memory_md),
            "location": "MEMORY.md",
            "timestamp": None,
            "speaker": "user",
            "conversation_id": "workspace-memory",
            "content": content,
        }
    ]


def ingest_workspace_daily_memory(workspace_root: Path) -> List[Dict]:
    records = []
    for path in sorted((workspace_root / "memory").glob("*.md")):
        content = path.read_text(encoding="utf-8")
        records.append(
            {
                "record_id": stable_id([str(path), path.name]),
                "source_type": "workspace-daily-memory",
                "source_path": str(path),
                "location": path.name,
                "timestamp": path.stem[:10] if len(path.stem) >= 10 else None,
                "speaker": "user",
                "conversation_id": path.stem,
                "content": content,
            }
        )
    return records


def ingest_openclaw_sessions(openclaw_home: Path) -> List[Dict]:
    records: List[Dict] = []
    for path in sorted(openclaw_home.glob("agents/*/sessions/*.jsonl")):
        if any(suffix in path.name for suffix in (".bak", ".reset", ".deleted", ".lock")):
            continue
        for row in read_jsonl(path):
            records.extend(parse_session_record(row, path))
    return records


def ingest_openclaw_memory_index(openclaw_home: Path) -> List[Dict]:
    db_path = openclaw_home / "memory" / "main.sqlite"
    if not db_path.exists():
        return []
    rows = load_sqlite_rows(
        db_path,
        """
        select path, start_line, end_line, text, updated_at
        from chunks
        order by path, start_line
        """,
    )
    records: List[Dict] = []
    for row in rows:
        location = f"{row['path']}:{row['start_line']}-{row['end_line']}"
        records.append(
            {
                "record_id": stable_id([str(db_path), location]),
                "source_type": "openclaw-memory-index",
                "source_path": str(db_path),
                "location": location,
                "timestamp": row["updated_at"],
                "speaker": "user",
                "conversation_id": row["path"],
                "content": row["text"],
            }
        )
    return records


def ingest_openclaw_task_runs(openclaw_home: Path) -> List[Dict]:
    db_path = openclaw_home / "tasks" / "runs.sqlite"
    if not db_path.exists():
        return []
    rows = load_sqlite_rows(
        db_path,
        """
        select task_id, runtime, label, task, status, progress_summary, terminal_summary, created_at
        from task_runs
        order by created_at desc
        """,
    )
    records: List[Dict] = []
    for row in rows:
        content = " | ".join(
            part
            for part in [
                row["label"] or "",
                row["task"] or "",
                row["status"] or "",
                row["progress_summary"] or "",
                row["terminal_summary"] or "",
            ]
            if part
        )
        if not content:
            continue
        records.append(
            {
                "record_id": stable_id([str(db_path), row["task_id"]]),
                "source_type": "openclaw-task-runs",
                "source_path": str(db_path),
                "location": row["task_id"],
                "timestamp": row["created_at"],
                "speaker": "system",
                "conversation_id": row["task_id"],
                "content": content,
            }
        )
    return records


def ingest_openclaw_cron_runs(openclaw_home: Path) -> List[Dict]:
    records: List[Dict] = []
    for path in sorted((openclaw_home / "cron" / "runs").glob("*.jsonl")):
        for index, row in enumerate(read_jsonl(path), start=1):
            content = json.dumps(row, ensure_ascii=False, sort_keys=True)
            records.append(
                {
                    "record_id": stable_id([str(path), str(index)]),
                    "source_type": "openclaw-cron-runs",
                    "source_path": str(path),
                    "location": f"{path.name}:{index}",
                    "timestamp": row.get("timestamp") or row.get("created_at"),
                    "speaker": "system",
                    "conversation_id": path.stem,
                    "content": content,
                }
            )
    return records


INGESTORS = {
    "workspace-long-memory": ingest_workspace_long_memory,
    "workspace-daily-memory": ingest_workspace_daily_memory,
    "openclaw-sessions": ingest_openclaw_sessions,
    "openclaw-memory-index": ingest_openclaw_memory_index,
    "openclaw-task-runs": ingest_openclaw_task_runs,
    "openclaw-cron-runs": ingest_openclaw_cron_runs,
}


def build_summary(records: List[Dict], approved_source_types: List[str], workspace_root: Path, openclaw_home: Path) -> Dict:
    by_source: Dict[str, Dict] = {}
    for source_type in approved_source_types:
        matching = [record for record in records if record["source_type"] == source_type]
        by_source[source_type] = {
            "record_count": len(matching),
            "example_locations": [record["location"] for record in matching[:3]],
            "language_mix": detect_language_mix(" ".join(record["content"][:400] for record in matching[:5])),
            "sample_preview": [shorten(record["content"], 120) for record in matching[:2]],
        }
    return {
        "generated_at": iso_now(),
        "workspace_root": str(workspace_root),
        "openclaw_home": str(openclaw_home),
        "approved_source_types": approved_source_types,
        "record_count": len(records),
        "segment_estimate": sum(len(split_into_segments(record["content"])) for record in records),
        "sources": by_source,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest all authorized MBTI content.")
    parser.add_argument("--manifest", required=True, help="Path to source manifest.")
    parser.add_argument("--approved-source-types", required=True, help="Comma-separated source types or 'all'.")
    parser.add_argument("--output-dir", required=True, help="Directory for output files.")
    args = parser.parse_args()

    manifest = load_json(resolve_path(args.manifest))
    workspace_root = resolve_path(manifest["workspace_root"])
    openclaw_home = resolve_path(manifest["openclaw_home"])
    output_dir = resolve_path(args.output_dir)

    discovered = [candidate["source_type"] for candidate in manifest["candidates"] if candidate["available"]]
    approved_source_types = discovered if args.approved_source_types == "all" else [
        item.strip() for item in args.approved_source_types.split(",") if item.strip()
    ]

    records: List[Dict] = []
    for source_type in approved_source_types:
        ingestor = INGESTORS.get(source_type)
        if ingestor is None:
            continue
        target_root = workspace_root if source_type.startswith("workspace") else openclaw_home
        records.extend(ingestor(target_root))

    write_jsonl(output_dir / "raw_records.jsonl", records)
    write_json(output_dir / "source_summary.json", build_summary(records, approved_source_types, workspace_root, openclaw_home))


if __name__ == "__main__":
    main()
