#!/usr/bin/env python3
"""Plan a page-count-aware reading workflow for long PDFs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from extract_pdf_text import build_response, extract_with_pdfinfo
from session_paths import (
    artifact_paths,
    existing_session_summary,
    load_existing_state,
    migrate_legacy_session,
    session_root,
)


TARGET_CHARS_PER_SEGMENT = 12000


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan a segmented reading workflow for a PDF file."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--page-start",
        type=int,
        default=1,
        help="Planning start page (1-based)",
    )
    parser.add_argument(
        "--page-end",
        type=int,
        default=None,
        help="Planning end page (1-based, defaults to the last page)",
    )
    parser.add_argument(
        "--sample-pages",
        type=int,
        default=3,
        help="Number of leading pages to sample for text density",
    )
    parser.add_argument(
        "--output",
        help="Optional JSON output path",
    )
    return parser


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def choose_base_strategy(total_pages: int) -> tuple[str, int, int, str]:
    if total_pages <= 40:
        return (
            "single_pass",
            max(1, total_pages),
            1,
            "页数较少，适合一次性提炼为完整成果。",
        )
    if total_pages <= 150:
        return (
            "segmented_read",
            10,
            3,
            "页数中等，适合按页段连续阅读并定期做阶段总结。",
        )
    if total_pages <= 400:
        return (
            "long_form_read",
            12,
            4,
            "页数较多，适合分段精读，避免一次性塞入过多文本。",
        )
    return (
        "book_mode",
        15,
        5,
        "页数非常多，更适合像读电子书一样做长程分段阅读。",
    )


def adjust_segment_size(base_size: int, chars_per_page: float) -> int:
    if chars_per_page <= 0:
        return base_size
    density_size = int(TARGET_CHARS_PER_SEGMENT / chars_per_page)
    density_size = max(3, min(25, density_size))
    return max(3, min(base_size, density_size))


def build_segments(page_start: int, page_end: int, segment_size: int) -> list[dict[str, int]]:
    segments: list[dict[str, int]] = []
    current = page_start
    index = 1
    while current <= page_end:
        end = min(current + segment_size - 1, page_end)
        segments.append(
            {
                "index": index,
                "page_start": current,
                "page_end": end,
            }
        )
        current = end + 1
        index += 1
    return segments


def build_sample_windows(
    page_start: int,
    page_end: int,
    base_segment_size: int,
    sample_pages: int,
) -> list[tuple[int, int]]:
    planning_pages = page_end - page_start + 1
    window_size = clamp(max(sample_pages, min(base_segment_size, 12)), 3, planning_pages)

    candidate_starts = [page_start]
    if planning_pages > 80:
        midpoint = page_start + max(0, planning_pages // 2 - window_size // 2)
        candidate_starts.append(midpoint)
    if planning_pages > 250:
        later = page_start + max(0, int(planning_pages * 0.8) - window_size // 2)
        candidate_starts.append(later)

    windows: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for start in candidate_starts:
        start = clamp(start, page_start, page_end)
        end = min(start + window_size - 1, page_end)
        window = (start, end)
        if window not in seen:
            windows.append(window)
            seen.add(window)
    return windows


def build_state_path(pdf_path: Path) -> str:
    return str(artifact_paths(pdf_path)["state"])


def build_plan_path(pdf_path: Path) -> str:
    return str(artifact_paths(pdf_path)["plan"])


def build_segment_results_dir(pdf_path: Path) -> str:
    return str(artifact_paths(pdf_path)["segment_results"])


def build_checkpoint_results_dir(pdf_path: Path) -> str:
    return str(artifact_paths(pdf_path)["checkpoint_results"])


def build_commands(
    pdf_path: Path,
    plan_file: str,
    state_file: str,
    segments: list[dict[str, int]],
    existing_session: dict[str, Any] | None,
) -> dict[str, str]:
    script_dir = Path(__file__).resolve().parent
    first_segment = segments[0]
    commands = {
        "init_state": (
            f'python3 "{script_dir / "update_pdf_session_state.py"}" '
            f'init --plan-file "{plan_file}" --state-file "{state_file}"'
        ),
        "force_reset_state": (
            f'python3 "{script_dir / "update_pdf_session_state.py"}" '
            f'init --plan-file "{plan_file}" --state-file "{state_file}" --force-reset'
        ),
        "show_state": (
            f'python3 "{script_dir / "update_pdf_session_state.py"}" '
            f'show --state-file "{state_file}"'
        ),
        "show_progress": (
            f'python3 "{script_dir / "summarize_pdf_session.py"}" '
            f'--state-file "{state_file}"'
        ),
        "read_first_segment": (
            f'python3 "{script_dir / "extract_pdf_text.py"}" "{pdf_path}" '
            f'--page-start {first_segment["page_start"]} --page-end {first_segment["page_end"]}'
        ),
        "next_segment": (
            f'python3 "{script_dir / "update_pdf_session_state.py"}" '
            f'next --state-file "{state_file}"'
        ),
        "previous_segment": (
            f'python3 "{script_dir / "update_pdf_session_state.py"}" '
            f'previous --state-file "{state_file}"'
        ),
        "jump_page_example": (
            f'python3 "{script_dir / "update_pdf_session_state.py"}" '
            f'jump-page --state-file "{state_file}" --page 201'
        ),
        "record_current_segment": (
            f'python3 "{script_dir / "record_pdf_segment_result.py"}" '
            f'--state-file "{state_file}" --content-file "/path/to/segment-result.md"'
        ),
        "build_next_checkpoint": (
            f'python3 "{script_dir / "build_pdf_checkpoint.py"}" '
            f'--state-file "{state_file}"'
        ),
        "record_next_checkpoint": (
            f'python3 "{script_dir / "record_pdf_checkpoint.py"}" '
            f'--state-file "{state_file}" --content-file "/path/to/checkpoint-summary.md"'
        ),
    }
    if existing_session:
        current_page_start = existing_session.get("current_page_start")
        current_page_end = existing_session.get("current_page_end")
        if isinstance(current_page_start, int) and isinstance(current_page_end, int):
            commands["read_current_segment"] = (
                f'python3 "{script_dir / "extract_pdf_text.py"}" "{pdf_path}" '
                f"--page-start {current_page_start} --page-end {current_page_end}"
            )
    return commands


def build_plan(
    pdf_path: Path,
    page_start: int,
    page_end: int | None,
    sample_pages: int,
) -> dict[str, Any]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {pdf_path.name}")
    if page_start < 1:
        raise ValueError("--page-start must be >= 1")
    if sample_pages < 1:
        raise ValueError("--sample-pages must be >= 1")

    migration = migrate_legacy_session(pdf_path)
    persisted_state = load_existing_state(pdf_path)
    metadata, metadata_warnings = extract_with_pdfinfo(pdf_path)
    total_pages_raw = metadata.get("total_pages")
    if not isinstance(total_pages_raw, int):
        raise RuntimeError("Could not determine total pages for this PDF.")

    total_pages = total_pages_raw
    planning_end = page_end or total_pages
    if planning_end < page_start:
        raise ValueError("--page-end must be >= --page-start")
    if planning_end > total_pages:
        planning_end = total_pages

    planning_pages = planning_end - page_start + 1
    strategy_mode, base_segment_size, summary_every, strategy_reason = choose_base_strategy(
        planning_pages
    )

    sample_windows = build_sample_windows(
        page_start=page_start,
        page_end=planning_end,
        base_segment_size=base_segment_size,
        sample_pages=sample_pages,
    )
    sample_results: list[dict[str, Any]] = []
    chars_per_page_candidates: list[float] = []
    aggregated_warnings = list(metadata_warnings)
    all_low_text = True
    primary_sample: dict[str, Any] | None = None

    for index, (sample_start, sample_end) in enumerate(sample_windows, start=1):
        sample = build_response(
            pdf_path=pdf_path,
            page_start=sample_start,
            page_end=sample_end,
            max_chars=16000,
        )
        sampled_pages = sample_end - sample_start + 1
        chars_per_page = sample["char_count"] / sampled_pages if sampled_pages > 0 else 0.0
        if sample["char_count"] > 0:
            chars_per_page_candidates.append(chars_per_page)
        if not sample["low_text_pdf"]:
            all_low_text = False
        aggregated_warnings.extend(sample["warnings"])
        result = {
            "window_index": index,
            "page_start": sample_start,
            "page_end": sample_end,
            "sampled_pages": sampled_pages,
            "char_count": sample["char_count"],
            "word_count": sample["word_count"],
            "chars_per_page": round(chars_per_page, 2),
            "low_text_pdf": sample["low_text_pdf"],
            "warnings": sample["warnings"],
            "extraction_method": sample["extraction_method"],
        }
        sample_results.append(result)
        if primary_sample is None or sample["char_count"] > primary_sample["char_count"]:
            primary_sample = {
                **sample,
                "page_start": sample_start,
                "page_end": sample_end,
                "sampled_pages": sampled_pages,
                "chars_per_page": round(chars_per_page, 2),
            }

    if primary_sample is None:
        raise RuntimeError("Could not build a readable sample for planning.")

    chars_per_page = (
        sum(chars_per_page_candidates) / len(chars_per_page_candidates)
        if chars_per_page_candidates
        else 0.0
    )
    recommended_segment_size = adjust_segment_size(base_segment_size, chars_per_page)
    segments = build_segments(page_start, planning_end, recommended_segment_size)
    total_segments = len(segments)
    requires_ocr = all_low_text
    existing_session = existing_session_summary(pdf_path)

    if persisted_state and persisted_state.get("segments"):
        persisted_segments = persisted_state["segments"]
        if isinstance(persisted_segments, list) and persisted_segments:
            segments = persisted_segments
            total_segments = int(persisted_state.get("total_segments", len(persisted_segments)))
            strategy_mode = str(persisted_state.get("strategy_mode", strategy_mode))
            recommended_segment_size = int(
                persisted_state.get("segment_size", recommended_segment_size)
            )
            summary_every = int(
                persisted_state.get(
                    "summary_checkpoint_every_segments",
                    summary_every,
                )
            )
            strategy_reason = "检测到已保存会话，沿用现有分段方案继续阅读。"
            requires_ocr = bool(persisted_state.get("requires_ocr", requires_ocr))

    if not requires_ocr and any(window["low_text_pdf"] for window in sample_results):
        aggregated_warnings.append(
            "Some sampled windows were sparse, but other windows contained readable text."
        )

    if existing_session and not requires_ocr:
        current_page_start = existing_session.get("current_page_start")
        current_page_end = existing_session.get("current_page_end")
        current_segment = existing_session.get("current_segment")
        completed_count = existing_session.get("completed_segment_count", 0)
        recommended_action = (
            f"发现已保存进度：当前在第 {current_segment} 段"
            f"（第 {current_page_start}-{current_page_end} 页），已完成 {completed_count} 段。"
            "建议先恢复现有会话继续阅读；如需重新开始，再执行 init --force-reset。"
        )
    elif strategy_mode == "single_pass":
        recommended_action = "直接提取全文并炼成完整成果。"
    elif requires_ocr:
        recommended_action = "先确认这份 PDF 是否需要 OCR，再决定是否继续分段阅读。"
    else:
        recommended_action = (
            f"先读取第 1 段（第 {segments[0]['page_start']}-{segments[0]['page_end']} 页），"
            "之后使用会话状态继续下一段。"
        )

    plan = {
        "status": "ok",
        "source_type": "pdf",
        "pdf_path": str(pdf_path),
        "file_name": pdf_path.name,
        "title": metadata.get("title"),
        "author": metadata.get("author"),
        "session_root": str(session_root()),
        "migration": migration,
        "existing_session": existing_session,
        "total_pages": total_pages,
        "planning_window": {
            "start": page_start,
            "end": planning_end,
            "pages": planning_pages,
        },
        "sampling": {
            "page_start": primary_sample["page_start"],
            "page_end": primary_sample["page_end"],
            "sampled_pages": primary_sample["sampled_pages"],
            "char_count": primary_sample["char_count"],
            "word_count": primary_sample["word_count"],
            "chars_per_page": round(chars_per_page, 2),
            "low_text_pdf": requires_ocr,
            "warnings": aggregated_warnings,
            "extraction_method": primary_sample["extraction_method"],
            "windows": sample_results,
        },
        "strategy": {
            "mode": strategy_mode,
            "reason": strategy_reason,
            "recommended_segment_size": recommended_segment_size,
            "total_segments": total_segments,
            "summary_checkpoint_every_segments": summary_every,
            "should_use_session_state": strategy_mode != "single_pass",
            "requires_ocr": requires_ocr,
        },
        "segments": segments,
        "state_file": build_state_path(pdf_path),
        "segment_results_dir": build_segment_results_dir(pdf_path),
        "checkpoint_results_dir": build_checkpoint_results_dir(pdf_path),
        "recommended_next_step": recommended_action,
    }
    return plan


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    pdf_path = Path(args.pdf_path).expanduser().resolve()

    try:
        plan = build_plan(
            pdf_path=pdf_path,
            page_start=args.page_start,
            page_end=args.page_end,
            sample_pages=args.sample_pages,
        )
        canonical_plan_path = Path(build_plan_path(pdf_path)).expanduser().resolve()
        plan["plan_file"] = str(canonical_plan_path)
        plan["commands"] = build_commands(
            pdf_path=pdf_path,
            plan_file=plan["plan_file"],
            state_file=plan["state_file"],
            segments=plan["segments"],
            existing_session=plan.get("existing_session"),
        )

        write_json(canonical_plan_path, plan)
        if args.output:
            requested_output = Path(args.output).expanduser().resolve()
            if requested_output != canonical_plan_path:
                write_json(requested_output, plan)

        output = json.dumps(plan, ensure_ascii=False, indent=2)
        print(output)
        return 0
    except Exception as exc:
        error = {
            "status": "error",
            "source_type": "pdf",
            "pdf_path": str(pdf_path),
            "message": str(exc),
        }
        output = json.dumps(error, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).expanduser().write_text(output + "\n", encoding="utf-8")
        else:
            print(output)
        return 1


if __name__ == "__main__":
    sys.exit(main())
