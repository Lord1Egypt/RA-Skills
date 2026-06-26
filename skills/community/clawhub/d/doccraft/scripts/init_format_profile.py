#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_PROFILE = {
    "format_authority": "default-profile",
    "needs_confirmation": True,
    "paper": "A4 portrait",
    "margins_cm": {"top": 2.5, "bottom": 2.5, "left": 3.0, "right": 2.5},
    "paragraph": {
        "alignment": "justified",
        "first_line_indent_chars": 2,
        "space_before_pt": 0,
        "space_after_pt": 0,
        "line_spacing": "exact 28 pt",
    },
    "fonts": {
        "body": {"font": "FangSong_GB2312", "size_pt": 16, "bold": False},
        "heading_1": {"font": "SimHei", "size_pt": 16, "bold": True},
        "heading_2": {"font": "KaiTi_GB2312", "size_pt": 16, "bold": True},
        "heading_3": {"font": "FangSong_GB2312", "size_pt": 16, "bold": True},
        "heading_4": {
            "font": "FangSong_GB2312",
            "size_pt": 16,
            "bold": False,
            "line_spacing": "exact 30 pt",
            "space_before_pt": 6,
            "space_after_pt": 3,
        },
    },
    "tables": {
        "caption_font": "SimHei 12 pt bold centered",
        "header_font": "SimHei 12 pt bold centered",
        "body_font": "SimSun 12 pt",
        "style": "three-line table",
        "row_spacing": "exact 18-20 pt",
    },
    "figures": {
        "caption_font": "FangSong_GB2312 12 pt centered",
    },
    "header": "none",
    "footer": {
        "page_number_font": "SimSun 9 pt",
        "alignment": "centered",
        "page_number_style": "- 1 -",
    },
    "exceptions": [],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a first-pass Word format profile for confirmation or record keeping."
    )
    parser.add_argument("--out", help="Optional output file")
    parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format",
    )
    parser.add_argument(
        "--authority",
        default=DEFAULT_PROFILE["format_authority"],
        help="Resolved format authority label",
    )
    parser.add_argument(
        "--needs-confirmation",
        choices=("yes", "no"),
        default="yes",
        help="Whether the format still needs user confirmation",
    )
    return parser.parse_args()


def build_profile(authority: str, needs_confirmation: str) -> dict:
    profile = json.loads(json.dumps(DEFAULT_PROFILE))
    profile["format_authority"] = authority
    profile["needs_confirmation"] = needs_confirmation == "yes"
    return profile


def render_markdown(profile: dict) -> str:
    margins = profile["margins_cm"]
    paragraph = profile["paragraph"]
    fonts = profile["fonts"]
    tables = profile["tables"]
    footer = profile["footer"]
    lines = [
        "# Word Format Profile",
        "",
        f"- Format authority: {profile['format_authority']}",
        f"- Needs confirmation: {'yes' if profile['needs_confirmation'] else 'no'}",
        "",
        "## Page setup",
        "",
        f"- Paper: {profile['paper']}",
        f"- Margins: top {margins['top']} cm, bottom {margins['bottom']} cm, left {margins['left']} cm, right {margins['right']} cm",
        f"- Paragraph alignment: {paragraph['alignment']}",
        f"- First-line indent: {paragraph['first_line_indent_chars']} characters",
        f"- Paragraph spacing: before {paragraph['space_before_pt']} pt, after {paragraph['space_after_pt']} pt",
        f"- Line spacing: {paragraph['line_spacing']}",
        "",
        "## Fonts",
        "",
        f"- Body: {fonts['body']['font']} {fonts['body']['size_pt']} pt",
        f"- Heading 1: {fonts['heading_1']['font']} {fonts['heading_1']['size_pt']} pt bold",
        f"- Heading 2: {fonts['heading_2']['font']} {fonts['heading_2']['size_pt']} pt bold",
        f"- Heading 3: {fonts['heading_3']['font']} {fonts['heading_3']['size_pt']} pt bold",
        f"- Heading 4: {fonts['heading_4']['font']} {fonts['heading_4']['size_pt']} pt regular, {fonts['heading_4']['line_spacing']}",
        "",
        "## Tables and figures",
        "",
        f"- Table caption: {tables['caption_font']}",
        f"- Table header: {tables['header_font']}",
        f"- Table body: {tables['body_font']}",
        f"- Table style: {tables['style']}",
        f"- Table row spacing: {tables['row_spacing']}",
        f"- Figure caption: {profile['figures']['caption_font']}",
        "",
        "## Header and footer",
        "",
        f"- Header: {profile['header']}",
        f"- Footer page number: {footer['page_number_font']}, {footer['alignment']}, style {footer['page_number_style']}",
        "",
        "## Exceptions",
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
    profile = build_profile(args.authority, args.needs_confirmation)
    if args.format == "json":
        text = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_markdown(profile)
    emit(text, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
