#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

NUMBERED_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)[\.\、\)]?\s*(.+?)\s*$")
HEADING_RE = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$")


@dataclass
class SectionBrief:
    section_id: str
    section_title: str
    purpose: str
    must_cover: list[str]
    primary_sources: list[str]
    secondary_sources: list[str]
    allowed_generic_material: str
    exclusions: list[str]
    expected_tables_or_figures: list[str]
    target_length: str
    open_questions: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap section briefs from a plain-text outline."
    )
    parser.add_argument("--outline", required=True, help="Outline text or markdown file")
    parser.add_argument("--out", help="Optional output file")
    parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format",
    )
    return parser.parse_args()


def parse_outline(path: Path) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    heading_counts: dict[int, int] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        numbered = NUMBERED_RE.match(line)
        if numbered:
            sections.append((numbered.group(1), numbered.group(2)))
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            heading_counts[level] = heading_counts.get(level, 0) + 1
            section_id = f"h{level}-{heading_counts[level]}"
            sections.append((section_id, heading.group(2)))
    return sections


def build_briefs(sections: list[tuple[str, str]]) -> list[SectionBrief]:
    briefs: list[SectionBrief] = []
    for section_id, title in sections:
        briefs.append(
            SectionBrief(
                section_id=section_id,
                section_title=title,
                purpose="",
                must_cover=[],
                primary_sources=[],
                secondary_sources=[],
                allowed_generic_material="",
                exclusions=[],
                expected_tables_or_figures=[],
                target_length="",
                open_questions=[],
            )
        )
    return briefs


def render_markdown(briefs: list[SectionBrief]) -> str:
    blocks: list[str] = []
    for brief in briefs:
        blocks.append(
            "\n".join(
                [
                    f"## {brief.section_id} {brief.section_title}",
                    "",
                    "- Purpose:",
                    "- Must cover:",
                    "- Primary sources:",
                    "- Secondary sources:",
                    "- Allowed generic material:",
                    "- Exclusions:",
                    "- Expected tables or figures:",
                    "- Target length:",
                    "- Open questions:",
                    "",
                ]
            )
        )
    return "\n".join(blocks).rstrip() + "\n"


def emit(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main() -> int:
    args = parse_args()
    outline_path = Path(args.outline)
    briefs = build_briefs(parse_outline(outline_path))
    if args.format == "json":
        text = json.dumps([asdict(item) for item in briefs], ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_markdown(briefs)
    emit(text, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
