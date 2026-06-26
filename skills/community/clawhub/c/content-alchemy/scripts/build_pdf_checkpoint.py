#!/usr/bin/env python3
"""Build checkpoint inputs from saved segment results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def build_checkpoint(state_file: str) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)
    window = next_checkpoint_window(state)
    if window is None:
        return {
            "status": "ok",
            "state_file": str(state_path),
            "checkpoint_due": False,
            "message": "All checkpoint windows have already been completed.",
        }

    result_files = dict(state.get("segment_result_files", {}))
    checkpoint_dir = checkpoint_results_dir(state, state_path)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    source_files: list[str] = []
    missing_files: list[int] = []
    for segment in range(window["start_segment"], window["end_segment"] + 1):
        result_file = result_files.get(str(segment))
        if result_file and Path(result_file).exists():
            source_files.append(str(Path(result_file).expanduser().resolve()))
        else:
            missing_files.append(segment)

    due = window["due"] and not missing_files
    source_bundle = checkpoint_dir / f"checkpoint-{window['checkpoint_index']:03d}-source.md"
    recommended_output = checkpoint_dir / f"checkpoint-{window['checkpoint_index']:03d}.md"

    if due:
        parts = [
            f"# Checkpoint {window['checkpoint_index']:03d} Source Bundle",
            "",
            (
                f"Segments {window['start_segment']}-{window['end_segment']}"
                f" from {state['file_name']}"
            ),
            "",
        ]
        for segment in range(window["start_segment"], window["end_segment"] + 1):
            result_file = Path(result_files[str(segment)]).expanduser().resolve()
            parts.extend(
                [
                    f"## Segment {segment:03d}",
                    "",
                    result_file.read_text(encoding="utf-8").strip(),
                    "",
                ]
            )
        source_bundle.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")

    return {
        "status": "ok",
        "state_file": str(state_path),
        "checkpoint_due": due,
        "checkpoint_window": window,
        "source_files": source_files,
        "missing_segment_files": missing_files,
        "source_bundle_file": str(source_bundle) if due else None,
        "recommended_output_file": str(recommended_output),
        "recommended_prompt": (
            "Read the saved segment results, produce one checkpoint summary yourself using "
            "the content-alchemy structure, save it to a temporary markdown file, and then "
            "record it with record_pdf_checkpoint.py. Do not invent a process_content_alchemy.py script."
            if due
            else "Checkpoint is not ready yet. Finish and save the missing segment results first."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare the next checkpoint bundle from saved segment results."
    )
    parser.add_argument("--state-file", required=True, help="Path to the session state file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = build_checkpoint(args.state_file)
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
