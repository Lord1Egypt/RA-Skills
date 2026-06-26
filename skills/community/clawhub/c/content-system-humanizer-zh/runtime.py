from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from skill_runtime.writing_core import dump_json, humanize_markdown, markdown_title, read_text, write_text


def slug_from_input(path: Path) -> str:
    stem = path.stem
    for suffix in ("-article", "-humanized", "-writing-pack"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def run_humanizer_zh(input_path: Path, *, workspace_root: Path) -> dict[str, Any]:
    text = read_text(input_path)
    slug = slug_from_input(input_path)
    drafts_dir = workspace_root / "content-production" / "drafts"
    output_path = drafts_dir / f"{slug}-humanized.md"
    report_path = drafts_dir / f"{slug}-humanizer-report.json"

    result = humanize_markdown(text, mode="surgical")
    write_text(output_path, result["text"])
    dump_json(
        report_path,
        {
            "slug": slug,
            "source_path": str(input_path),
            "output_path": str(output_path),
            "title": markdown_title(text) or re.sub(r"[-_]+", " ", slug),
            "mode": result["mode"],
            "changed_line_count": result["changed_line_count"],
            "ai_trace_risk": result["ai_trace_risk"],
            "pattern_hit_count": result["pattern_hit_count"],
            "pattern_hits": result["pattern_hits"],
            "changes": result["changes"],
        },
    )

    return {
        "slug": slug,
        "output_path": output_path,
        "report_path": report_path,
        "ai_trace_risk": result["ai_trace_risk"],
        "changed_line_count": result["changed_line_count"],
    }
