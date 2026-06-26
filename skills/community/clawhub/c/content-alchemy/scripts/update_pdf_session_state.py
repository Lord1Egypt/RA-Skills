#!/usr/bin/env python3
"""Maintain session state for segmented PDF reading."""

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


def normalize_state_path(path_str: str | None, plan: dict[str, Any] | None = None) -> Path:
    if path_str:
        return Path(path_str).expanduser().resolve()
    if plan and plan.get("state_file"):
        return Path(plan["state_file"]).expanduser().resolve()
    raise ValueError("State file path is required.")


def infer_plan_path(state_file: str | None) -> Path | None:
    if not state_file:
        return None
    state_path = Path(state_file).expanduser().resolve()
    candidate = state_path.with_name(f"{state_path.stem}-plan.json")
    return candidate if candidate.exists() else None


def current_segment_payload(state: dict[str, Any]) -> dict[str, Any]:
    segment_index = state["current_segment"]
    segment = state["segments"][segment_index - 1]
    payload = dict(state)
    payload["current_page_start"] = segment["page_start"]
    payload["current_page_end"] = segment["page_end"]
    return payload


def segment_result_path(segment_results_dir: str | None, state_path: Path, segment_index: int) -> str:
    if segment_results_dir:
        base_dir = Path(segment_results_dir).expanduser().resolve()
    else:
        base_dir = state_path.with_name(f"{state_path.stem}-segments")
    return str((base_dir / f"segment-{segment_index:03d}.md").resolve())


def checkpoint_result_path(
    checkpoint_results_dir: str | None,
    state_path: Path,
    checkpoint_index: int,
) -> str:
    if checkpoint_results_dir:
        base_dir = Path(checkpoint_results_dir).expanduser().resolve()
    else:
        base_dir = state_path.with_name(f"{state_path.stem}-checkpoints")
    return str((base_dir / f"checkpoint-{checkpoint_index:03d}.md").resolve())


def normalize_saved_result_paths(
    state: dict[str, Any],
    state_path: Path,
    plan: dict[str, Any],
) -> dict[str, Any]:
    normalized = dict(state)
    segment_results_dir = plan.get("segment_results_dir")
    checkpoint_results_dir = plan.get("checkpoint_results_dir")
    segments_by_index = {
        int(segment["index"]): segment for segment in normalized.get("segments", [])
    }

    completed_segments = sorted(int(value) for value in normalized.get("completed_segments", []))
    raw_segment_metadata = dict(normalized.get("segment_result_metadata", {}))
    segment_result_files: dict[str, str] = {}
    segment_result_metadata: dict[str, Any] = {}
    for segment_index in completed_segments:
        key = str(segment_index)
        file_path = segment_result_path(segment_results_dir, state_path, segment_index)
        segment_result_files[key] = file_path
        metadata = dict(raw_segment_metadata.get(key, {}))
        metadata["file"] = file_path
        if segment_index in segments_by_index:
            metadata.setdefault("page_start", segments_by_index[segment_index]["page_start"])
            metadata.setdefault("page_end", segments_by_index[segment_index]["page_end"])
        segment_result_metadata[key] = metadata

    completed_checkpoints = sorted(
        int(value) for value in normalized.get("completed_checkpoints", [])
    )
    raw_checkpoint_metadata = dict(normalized.get("checkpoint_result_metadata", {}))
    checkpoint_result_files: dict[str, str] = {}
    checkpoint_result_metadata: dict[str, Any] = {}
    checkpoint_every = int(
        normalized.get(
            "summary_checkpoint_every_segments",
            plan["strategy"]["summary_checkpoint_every_segments"],
        )
    )
    for checkpoint_index in completed_checkpoints:
        key = str(checkpoint_index)
        file_path = checkpoint_result_path(checkpoint_results_dir, state_path, checkpoint_index)
        checkpoint_result_files[key] = file_path
        metadata = dict(raw_checkpoint_metadata.get(key, {}))
        metadata["file"] = file_path
        start_segment = metadata.get("start_segment")
        end_segment = metadata.get("end_segment")
        if start_segment is None:
            start_segment = (checkpoint_index - 1) * checkpoint_every + 1
        if end_segment is None:
            end_segment = min(
                int(normalized["total_segments"]),
                checkpoint_index * checkpoint_every,
            )
        metadata["start_segment"] = start_segment
        metadata["end_segment"] = end_segment
        checkpoint_result_metadata[key] = metadata

    normalized["segment_result_files"] = segment_result_files
    normalized["segment_result_metadata"] = segment_result_metadata
    normalized["checkpoint_result_files"] = checkpoint_result_files
    normalized["checkpoint_result_metadata"] = checkpoint_result_metadata

    last_completed_segment = normalized.get("last_completed_segment")
    if isinstance(last_completed_segment, int) and str(last_completed_segment) in segment_result_files:
        normalized["last_segment_result_file"] = segment_result_files[str(last_completed_segment)]

    last_checkpoint_segment = normalized.get("last_checkpoint_segment", 0)
    if last_checkpoint_segment:
        checkpoint_index = (int(last_checkpoint_segment) - 1) // checkpoint_every + 1
        if str(checkpoint_index) in checkpoint_result_files:
            normalized["last_checkpoint_file"] = checkpoint_result_files[str(checkpoint_index)]

    return normalized


def init_state(
    plan_file: str | None,
    state_file: str | None,
    force_reset: bool = False,
) -> dict[str, Any]:
    plan_path = None
    if plan_file:
        plan_path = Path(plan_file).expanduser().resolve()
    else:
        plan_path = infer_plan_path(state_file)
    if plan_path is None or not plan_path.exists():
        raise FileNotFoundError("Plan file was not found. Please run plan_pdf_reading.py first.")

    plan = load_json(plan_path)
    if plan.get("status") != "ok":
        raise ValueError("Plan file is not ready for session init.")
    state_path = normalize_state_path(state_file, plan)
    segments = plan["segments"]
    if not segments:
        raise ValueError("Plan contains no segments.")

    if state_path.exists() and not force_reset:
        existing_state = load_json(state_path)
        existing_pdf_path = existing_state.get("pdf_path")
        if existing_pdf_path and existing_pdf_path != plan["pdf_path"]:
            raise ValueError(
                "State file already exists for a different PDF. Use --force-reset to overwrite it."
            )

        existing_state.setdefault("pdf_path", plan["pdf_path"])
        existing_state.setdefault("file_name", plan["file_name"])
        existing_state.setdefault("title", plan.get("title"))
        existing_state.setdefault("author", plan.get("author"))
        existing_state.setdefault("total_pages", plan["total_pages"])
        existing_state.setdefault("planning_window", plan["planning_window"])
        existing_state.setdefault("strategy_mode", plan["strategy"]["mode"])
        existing_state.setdefault("segment_size", plan["strategy"]["recommended_segment_size"])
        existing_state.setdefault("total_segments", plan["strategy"]["total_segments"])
        existing_state.setdefault(
            "summary_checkpoint_every_segments",
            plan["strategy"]["summary_checkpoint_every_segments"],
        )
        existing_state.setdefault("requires_ocr", plan["strategy"]["requires_ocr"])
        existing_state.setdefault("segments", plan["segments"])
        existing_state["state_file"] = str(state_path)
        existing_state["plan_file"] = plan.get("plan_file")
        existing_state["segment_results_dir"] = plan.get("segment_results_dir")
        existing_state["checkpoint_results_dir"] = plan.get("checkpoint_results_dir")
        existing_state = normalize_saved_result_paths(existing_state, state_path, plan)
        existing_state["status"] = "active"
        existing_state["resumed_existing_state"] = True
        existing_state["last_action"] = "resume-existing"
        existing_state["updated_at"] = now_iso()
        existing_state = current_segment_payload(existing_state)
        write_json(state_path, existing_state)
        return existing_state

    first_segment = segments[0]
    state = {
        "status": "active",
        "pdf_path": plan["pdf_path"],
        "file_name": plan["file_name"],
        "title": plan.get("title"),
        "author": plan.get("author"),
        "total_pages": plan["total_pages"],
        "planning_window": plan["planning_window"],
        "strategy_mode": plan["strategy"]["mode"],
        "segment_size": plan["strategy"]["recommended_segment_size"],
        "total_segments": plan["strategy"]["total_segments"],
        "summary_checkpoint_every_segments": plan["strategy"][
            "summary_checkpoint_every_segments"
        ],
        "requires_ocr": plan["strategy"]["requires_ocr"],
        "state_file": str(state_path),
        "plan_file": plan.get("plan_file"),
        "segment_results_dir": plan.get("segment_results_dir"),
        "checkpoint_results_dir": plan.get("checkpoint_results_dir"),
        "segments": segments,
        "current_segment": first_segment["index"],
        "current_page_start": first_segment["page_start"],
        "current_page_end": first_segment["page_end"],
        "visited_segments": [first_segment["index"]],
        "completed_segments": [],
        "segment_result_files": {},
        "segment_result_metadata": {},
        "completed_checkpoints": [],
        "checkpoint_result_files": {},
        "checkpoint_result_metadata": {},
        "last_checkpoint_segment": 0,
        "last_action": "init",
        "updated_at": now_iso(),
    }
    write_json(state_path, state)
    return state


def step_state(state_file: str, direction: str) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)
    current = state["current_segment"]
    total = state["total_segments"]
    if direction == "next":
        new_segment = min(total, current + 1)
    else:
        new_segment = max(1, current - 1)
    state["current_segment"] = new_segment
    if new_segment not in state["visited_segments"]:
        state["visited_segments"].append(new_segment)
    state["last_action"] = direction
    state["updated_at"] = now_iso()
    state = current_segment_payload(state)
    write_json(state_path, state)
    return state


def jump_segment(state_file: str, segment_index: int) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)
    if segment_index < 1 or segment_index > state["total_segments"]:
        raise ValueError("Segment index is out of range.")
    state["current_segment"] = segment_index
    if segment_index not in state["visited_segments"]:
        state["visited_segments"].append(segment_index)
    state["last_action"] = "jump-segment"
    state["updated_at"] = now_iso()
    state = current_segment_payload(state)
    write_json(state_path, state)
    return state


def jump_page(state_file: str, page_number: int) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)
    for segment in state["segments"]:
        if segment["page_start"] <= page_number <= segment["page_end"]:
            return jump_segment(str(state_path), segment["index"])
    raise ValueError("Page number is outside the planned reading window.")


def show_state(state_file: str) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    return load_json(state_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize and update session state for segmented PDF reading."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize state from a plan file")
    init_parser.add_argument("--plan-file", help="Path to a JSON plan file")
    init_parser.add_argument("--state-file", help="Optional explicit state file path")
    init_parser.add_argument(
        "--force-reset",
        action="store_true",
        help="Discard any existing saved state and start again from the plan",
    )

    show_parser = subparsers.add_parser("show", help="Show the current state")
    show_parser.add_argument("--state-file", required=True, help="State file path")

    next_parser = subparsers.add_parser("next", help="Advance to the next segment")
    next_parser.add_argument("--state-file", required=True, help="State file path")

    previous_parser = subparsers.add_parser(
        "previous", help="Move back to the previous segment"
    )
    previous_parser.add_argument("--state-file", required=True, help="State file path")

    jump_segment_parser = subparsers.add_parser(
        "jump-segment", help="Jump to a specific segment"
    )
    jump_segment_parser.add_argument("--state-file", required=True, help="State file path")
    jump_segment_parser.add_argument(
        "--segment", required=True, type=int, help="Target segment index"
    )

    jump_page_parser = subparsers.add_parser("jump-page", help="Jump to a page number")
    jump_page_parser.add_argument("--state-file", required=True, help="State file path")
    jump_page_parser.add_argument("--page", required=True, type=int, help="Target page number")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "init":
            payload = init_state(args.plan_file, args.state_file, args.force_reset)
        elif args.command == "show":
            payload = show_state(args.state_file)
        elif args.command == "next":
            payload = step_state(args.state_file, "next")
        elif args.command == "previous":
            payload = step_state(args.state_file, "previous")
        elif args.command == "jump-segment":
            payload = jump_segment(args.state_file, args.segment)
        elif args.command == "jump-page":
            payload = jump_page(args.state_file, args.page)
        else:
            raise ValueError(f"Unsupported command: {args.command}")

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
