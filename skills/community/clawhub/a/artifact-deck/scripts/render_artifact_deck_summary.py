#!/usr/bin/env python3
"""Render a markdown summary for an Artifact Deck build."""

from __future__ import annotations

import argparse
from pathlib import Path

from deck_common import ensure_existing_path, load_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Artifact Deck manifest JSON.")
    parser.add_argument("--check", required=True, help="Validation JSON.")
    parser.add_argument("--build", required=True, help="Build JSON.")
    parser.add_argument("--out", required=True, help="Output markdown path.")
    args = parser.parse_args()

    manifest_path = ensure_existing_path(args.manifest, "--manifest")
    check_path = ensure_existing_path(args.check, "--check")
    build_path = ensure_existing_path(args.build, "--build")
    out_path = Path(args.out).expanduser().resolve()

    manifest = load_json(manifest_path)
    check = load_json(check_path)
    build = load_json(build_path)

    deck_path = str(build.get("deck_path") or "")
    deck_label = Path(deck_path).name if deck_path else "deck.pptx"
    lines = [
        "# Artifact Deck Summary",
        "",
        f"- Validation: **{check.get('status', 'unknown')}**",
        f"- Deck file: **{deck_label}**",
        f"- Slide count: **{build.get('slide_count', 0)}**",
        f"- Image appendix slides: **{build.get('image_slide_count', 0)}**",
        "",
        "## Rebuild",
        "",
        "Run from the `artifact-deck` repo root:",
        "",
        "```bash",
        "python3 skill/artifact-deck/scripts/build_artifact_deck.py \\",
        "  --manifest <manifest.json> \\",
        f"  --deck-out {deck_label} \\",
        "  --out <build.json>",
        "```",
        "",
        "## Slides",
        "",
    ]
    for title in build.get("slide_titles") or [manifest.get("title")]:
        lines.append(f"- {title}")

    if check.get("warnings"):
        lines.extend(["", "## Validation Warnings", ""])
        for warning in check.get("warnings") or []:
            lines.append(f"- {warning.get('message')}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
