#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_BRIEF = {
    "document_title": "",
    "source_authority": "",
    "target_structure": "",
    "document_purpose": "",
    "audience": "",
    "output_mode": "new-docx",
    "delivery_stage": "draft",
    "completeness_scope": "body-only draft",
    "review_mode": "clean-copy",
    "format_authority": "default-profile",
    "file_naming_and_version": "",
    "cleanup_rule": "remove working notes from final body",
    "open_questions": [],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a first-pass delivery brief for a complete Word deliverable."
    )
    parser.add_argument("--out", help="Optional output file")
    parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format",
    )
    parser.add_argument("--output-mode", default=DEFAULT_BRIEF["output_mode"])
    parser.add_argument("--delivery-stage", default=DEFAULT_BRIEF["delivery_stage"])
    parser.add_argument("--review-mode", default=DEFAULT_BRIEF["review_mode"])
    parser.add_argument("--format-authority", default=DEFAULT_BRIEF["format_authority"])
    return parser.parse_args()


def build_brief(args: argparse.Namespace) -> dict:
    brief = json.loads(json.dumps(DEFAULT_BRIEF))
    brief["output_mode"] = args.output_mode
    brief["delivery_stage"] = args.delivery_stage
    brief["review_mode"] = args.review_mode
    brief["format_authority"] = args.format_authority
    return brief


def render_markdown(brief: dict) -> str:
    lines = [
        "# Word Delivery Brief",
        "",
        f"- Document title: {brief['document_title'] or '[to confirm]'}",
        f"- Source authority: {brief['source_authority'] or '[to confirm]'}",
        f"- Target structure: {brief['target_structure'] or '[to confirm]'}",
        f"- Document purpose: {brief['document_purpose'] or '[to confirm]'}",
        f"- Audience: {brief['audience'] or '[to confirm]'}",
        f"- Output mode: {brief['output_mode']}",
        f"- Delivery stage: {brief['delivery_stage']}",
        f"- Completeness scope: {brief['completeness_scope']}",
        f"- Review mode: {brief['review_mode']}",
        f"- Format authority: {brief['format_authority']}",
        f"- File naming and version: {brief['file_naming_and_version'] or '[to confirm]'}",
        f"- Cleanup rule: {brief['cleanup_rule']}",
        "",
        "## Open questions",
        "",
        "- None yet",
        "",
    ]
    return "\n".join(lines)


def emit(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main() -> int:
    args = parse_args()
    brief = build_brief(args)
    if args.format == "json":
        text = json.dumps(brief, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_markdown(brief)
    emit(text, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
