#!/usr/bin/env python3
"""Summarize the current reading progress for a persistent PDF session."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def contiguous_completed_segments(completed_segments: list[int]) -> list[int]:
    contiguous: list[int] = []
    expected = 1
    for segment in completed_segments:
        if segment != expected:
            break
        contiguous.append(segment)
        expected += 1
    return contiguous


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
    completed_in_window = [
        seg for seg in range(start_segment, end_segment + 1) if seg in completed
    ]
    return {
        "checkpoint_index": (start_segment - 1) // checkpoint_every + 1,
        "start_segment": start_segment,
        "end_segment": end_segment,
        "due": not missing,
        "missing_segments": missing,
        "completed_segments": completed_in_window,
        "completed_count": len(completed_in_window),
        "required_count": end_segment - start_segment + 1,
    }


def checkpoint_note(
    checkpoint: dict[str, Any] | None,
    completed_segments: list[int],
    contiguous_segments: list[int],
) -> str | None:
    if checkpoint is None:
        return "所有阶段总结检查点都已经完成。"

    missing = checkpoint["missing_segments"]
    if not missing:
        return (
            f"第 {checkpoint['checkpoint_index']} 个阶段总结检查点"
            f"（第 {checkpoint['start_segment']}-{checkpoint['end_segment']} 段）已满足生成条件。"
        )

    missing_text = "、".join(str(segment) for segment in missing)
    if len(contiguous_segments) < len(completed_segments):
        return (
            f"已累计完成 {len(completed_segments)} 段，但当前最早待补检查点仍是"
            f"第 {checkpoint['start_segment']}-{checkpoint['end_segment']} 段，"
            f"还缺第 {missing_text} 段。"
        )

    return (
        f"当前最近的阶段总结检查点是第 {checkpoint['checkpoint_index']} 个"
        f"（第 {checkpoint['start_segment']}-{checkpoint['end_segment']} 段），"
        f"还缺第 {missing_text} 段。"
    )


def summarize_state(state_file: str) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve()
    state = load_json(state_path)

    completed_segments = sorted(int(value) for value in state.get("completed_segments", []))
    completed_set = set(completed_segments)
    contiguous_segments = contiguous_completed_segments(completed_segments)
    completed_checkpoints = sorted(
        int(value) for value in state.get("completed_checkpoints", [])
    )
    current_segment = int(state["current_segment"])
    total_segments = int(state["total_segments"])
    next_segment = current_segment + 1 if current_segment < total_segments else None
    previous_segment = current_segment - 1 if current_segment > 1 else None
    checkpoint = next_checkpoint_window(state)
    progress_mode = (
        "nonlinear" if len(contiguous_segments) < len(completed_segments) else "sequential"
    )
    missing_before_current = [
        segment
        for segment in range(1, current_segment)
        if segment not in completed_set
    ]
    current_segment_saved = current_segment in completed_set
    overall_progress_percent = round(len(completed_segments) / total_segments * 100, 1)
    contiguous_through_segment = contiguous_segments[-1] if contiguous_segments else 0
    checkpoint_summary = checkpoint_note(
        checkpoint=checkpoint,
        completed_segments=completed_segments,
        contiguous_segments=contiguous_segments,
    )

    summary = {
        "status": "ok",
        "state_file": str(state_path),
        "pdf_path": state["pdf_path"],
        "file_name": state["file_name"],
        "title": state.get("title"),
        "total_pages": state["total_pages"],
        "strategy_mode": state["strategy_mode"],
        "current_segment": current_segment,
        "current_page_start": state["current_page_start"],
        "current_page_end": state["current_page_end"],
        "total_segments": total_segments,
        "completed_segments": completed_segments,
        "completed_segment_count": len(completed_segments),
        "contiguous_completed_segments": contiguous_segments,
        "contiguous_completed_count": len(contiguous_segments),
        "contiguous_completed_through_segment": contiguous_through_segment,
        "progress_mode": progress_mode,
        "overall_progress_percent": overall_progress_percent,
        "missing_segments_before_current": missing_before_current,
        "current_segment_saved": current_segment_saved,
        "completed_checkpoints": completed_checkpoints,
        "completed_checkpoint_count": len(completed_checkpoints),
        "next_segment": next_segment,
        "previous_segment": previous_segment,
        "segment_results_dir": state.get("segment_results_dir"),
        "checkpoint_results_dir": state.get("checkpoint_results_dir"),
        "last_action": state.get("last_action"),
        "updated_at": state.get("updated_at"),
        "next_checkpoint": checkpoint,
        "checkpoint_note": checkpoint_summary,
        "human_summary": (
            f"当前在第 {current_segment}/{total_segments} 段"
            f"（第 {state['current_page_start']}-{state['current_page_end']} 页），"
            f"已累计完成 {len(completed_segments)} 段"
            f"（约 {overall_progress_percent:.1f}%）。"
            + (
                f" 从开头连续完成到第 {contiguous_through_segment} 段。"
                if contiguous_through_segment > 0
                else ""
            )
            + (
                f" 当前段成果已保存。"
                if current_segment_saved
                else " 当前段尚未保存成果。"
            )
            + (
                f" {checkpoint_summary}"
                if checkpoint_summary
                else ""
            )
        ),
    }
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize the progress of a persistent PDF reading session."
    )
    parser.add_argument("--state-file", required=True, help="Path to the session state file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = summarize_state(args.state_file)
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
