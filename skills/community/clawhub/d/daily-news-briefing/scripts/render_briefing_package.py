#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_with_placeholders(template_text: str, replacements: dict[str, str]) -> str:
    safe = template_text
    for key, value in replacements.items():
        safe = safe.replace("{{" + key + "}}", value)
    return safe


def build_manifest(args: argparse.Namespace) -> dict[str, object]:
    sections = [
        "Executive Summary",
        "Top Stories",
        "Signals and Watchlist",
        "Closing Take",
    ]
    return {
        "title": args.title,
        "date": args.date,
        "audience": args.audience,
        "scope": args.scope,
        "tone": args.tone,
        "format": args.format,
        "sections": sections,
        "notes": [
            "Replace all placeholders before publishing.",
            "Verify every story with current sources.",
            "Attach source links near the story they support.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a reusable daily briefing package."
    )
    parser.add_argument("--title", required=True, help="Report title")
    parser.add_argument("--date", required=True, help="Exact report date, e.g. 2026-03-18")
    parser.add_argument("--audience", required=True, help="Intended audience")
    parser.add_argument("--scope", required=True, help="Coverage scope")
    parser.add_argument("--tone", default="authoritative", help="Editorial tone")
    parser.add_argument(
        "--format",
        choices=("markdown", "html"),
        default="markdown",
        help="Primary draft format",
    )
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    replacements = {
        "title": args.title,
        "date": args.date,
        "audience": args.audience,
        "scope": args.scope,
        "summary_bullet_1": "[Add the most important development]",
        "summary_bullet_2": "[Add the second most important development]",
        "summary_bullet_3": "[Add the third most important development]",
        "story_1_headline": "[Insert lead headline]",
        "story_1_summary": "[Summarize the lead story in 2 to 4 sentences.]",
        "story_1_why": "[Explain why this matters now.]",
        "story_1_sources": "[Add source links]",
        "story_2_headline": "[Insert second headline]",
        "story_2_summary": "[Summarize the second story.]",
        "story_2_why": "[Explain the implication.]",
        "story_2_sources": "[Add source links]",
        "story_3_headline": "[Insert third headline]",
        "story_3_summary": "[Summarize the third story.]",
        "story_3_why": "[Explain the implication.]",
        "story_3_sources": "[Add source links]",
        "watch_item_1": "[Add watch item]",
        "watch_item_2": "[Add watch item]",
        "watch_item_3": "[Add watch item]",
        "closing_take": "[Write a concise closing synthesis.]",
    }

    manifest = build_manifest(args)
    write_file(
        output_dir / "briefing-manifest.json",
        json.dumps(manifest, ensure_ascii=True, indent=2) + "\n",
    )

    markdown_template = load_template(skill_dir / "assets" / "briefing-template.md")
    html_template = load_template(skill_dir / "assets" / "briefing-template.html")

    write_file(
        output_dir / "briefing.md",
        render_with_placeholders(markdown_template, replacements).rstrip() + "\n",
    )

    if args.format == "html":
        write_file(
            output_dir / "briefing.html",
            render_with_placeholders(html_template, replacements).rstrip() + "\n",
        )


if __name__ == "__main__":
    main()
