#!/usr/bin/env python3
"""Persist a generated checkpoint summary and update PDF session state."""

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


def checkpoint_results_dir(state: dict[str, Any], state_path: Path) -> Path:
    configured = state.get("checkpoint_results_dir")
    if configured:
        return Path(str(configured)).expanduser().resolve()
    return state_path.with_name(f"{state_path.stem}-checkpoints")


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


def record_checkpoint(
    state_file: str,
    content_file: str | None,
    checkpoint_index: int | None,
) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)
    window = next_checkpoint_window(state)
    if window is None:
        raise ValueError("There is no pending checkpoint window to record.")
    if checkpoint_index is not None and checkpoint_index != window["checkpoint_index"]:
        raise ValueError("Checkpoint index does not match the next pending checkpoint window.")
    if not window["due"]:
        raise ValueError("Checkpoint is not ready yet because some segments are still missing.")

    content = read_content(content_file)
    if not content:
        raise ValueError("Checkpoint summary content is empty.")

    checkpoint_dir = checkpoint_results_dir(state, state_path)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    output_path = checkpoint_dir / f"checkpoint-{window['checkpoint_index']:03d}.md"
    output_path.write_text(content + "\n", encoding="utf-8")

    completed_checkpoints = sorted(
        {int(value) for value in state.get("completed_checkpoints", [])}
        | {window["checkpoint_index"]}
    )
    checkpoint_files = dict(state.get("checkpoint_result_files", {}))
    checkpoint_files[str(window["checkpoint_index"])] = str(output_path)

    checkpoint_metadata = dict(state.get("checkpoint_result_metadata", {}))
    checkpoint_metadata[str(window["checkpoint_index"])] = {
        "file": str(output_path),
        "start_segment": window["start_segment"],
        "end_segment": window["end_segment"],
        "saved_at": now_iso(),
    }

    state["completed_checkpoints"] = completed_checkpoints
    state["checkpoint_result_files"] = checkpoint_files
    state["checkpoint_result_metadata"] = checkpoint_metadata
    state["last_checkpoint_segment"] = window["end_segment"]
    state["last_checkpoint_file"] = str(output_path)
    state["last_action"] = "record-checkpoint"
    state["updated_at"] = now_iso()
    write_json(state_path, state)

    next_window = next_checkpoint_window(state)
    return {
        "status": "ok",
        "state_file": str(state_path),
        "checkpoint_index": window["checkpoint_index"],
        "start_segment": window["start_segment"],
        "end_segment": window["end_segment"],
        "saved_file": str(output_path),
        "completed_checkpoints": completed_checkpoints,
        "next_checkpoint": next_window,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Save a generated checkpoint summary and update session state."
    )
    parser.add_argument("--state-file", required=True, help="Path to the session state file")
    parser.add_argument("--content-file", help="Path to a markdown file containing the summary")
    parser.add_argument(
        "--checkpoint-index",
        type=int,
        help="Checkpoint index to record. Defaults to the next pending checkpoint.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = record_checkpoint(
            state_file=args.state_file,
            content_file=args.content_file,
            checkpoint_index=args.checkpoint_index,
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
