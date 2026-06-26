#!/usr/bin/env python3
"""Persist a generated segment result and update PDF session state."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_content(content_file: str | None) -> str:
    if content_file:
        return Path(content_file).expanduser().resolve().read_text(encoding="utf-8").strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise ValueError("Provide --content-file or pipe markdown content through stdin.")


def segment_results_dir(state: dict[str, Any], state_path: Path) -> Path:
    configured = state.get("segment_results_dir")
    if configured:
        return Path(str(configured)).expanduser().resolve()
    return state_path.with_name(f"{state_path.stem}-segments")


def normalize_segments(values: list[int]) -> list[int]:
    return sorted({int(value) for value in values})


def next_checkpoint_window(state: dict[str, Any]) -> dict[str, Any] | None:
    checkpoint_every = int(state["summary_checkpoint_every_segments"])
    total_segments = int(state["total_segments"])
    last_checkpoint_segment = int(state.get("last_checkpoint_segment", 0))
    start_segment = last_checkpoint_segment + 1
    if start_segment > total_segments:
        return None
    end_segment = min(total_segments, start_segment + checkpoint_every - 1)
    completed = set(int(value) for value in state.get("completed_segments", []))
    missing = [seg for seg in range(start_segment, end_segment + 1) if seg not in completed]
    return {
        "checkpoint_index": (start_segment - 1) // checkpoint_every + 1,
        "start_segment": start_segment,
        "end_segment": end_segment,
        "due": not missing,
        "missing_segments": missing,
    }


def record_segment(
    state_file: str,
    content_file: str | None,
    segment_index: int | None,
) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)
    target_segment = segment_index or int(state["current_segment"])
    if target_segment < 1 or target_segment > int(state["total_segments"]):
        raise ValueError("Segment index is out of range.")

    content = read_content(content_file)
    if not content:
        raise ValueError("Segment result content is empty.")

    segment = state["segments"][target_segment - 1]
    results_dir = segment_results_dir(state, state_path)
    results_dir.mkdir(parents=True, exist_ok=True)
    result_path = results_dir / f"segment-{target_segment:03d}.md"
    result_path.write_text(content + "\n", encoding="utf-8")

    completed_segments = normalize_segments(
        [*state.get("completed_segments", []), target_segment]
    )
    result_files = dict(state.get("segment_result_files", {}))
    result_files[str(target_segment)] = str(result_path)

    metadata = dict(state.get("segment_result_metadata", {}))
    metadata[str(target_segment)] = {
        "file": str(result_path),
        "page_start": segment["page_start"],
        "page_end": segment["page_end"],
        "saved_at": now_iso(),
    }

    if target_segment not in state["visited_segments"]:
        state["visited_segments"].append(target_segment)

    state["completed_segments"] = completed_segments
    state["segment_result_files"] = result_files
    state["segment_result_metadata"] = metadata
    state["last_completed_segment"] = target_segment
    state["last_segment_result_file"] = str(result_path)
    state["last_action"] = "record-segment"
    state["updated_at"] = now_iso()
    write_json(state_path, state)

    checkpoint = next_checkpoint_window(state)
    return {
        "status": "ok",
        "state_file": str(state_path),
        "segment_index": target_segment,
        "page_start": segment["page_start"],
        "page_end": segment["page_end"],
        "saved_file": str(result_path),
        "completed_segments": completed_segments,
        "checkpoint": checkpoint,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Save a generated segment result and update the PDF session state."
    )
    parser.add_argument("--state-file", required=True, help="Path to the session state file")
    parser.add_argument(
        "--content-file",
        help="Path to a markdown file containing the segment result",
    )
    parser.add_argument(
        "--segment",
        type=int,
        help="Segment index to record. Defaults to the current segment in state.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = record_segment(
            state_file=args.state_file,
            content_file=args.content_file,
            segment_index=args.segment,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
