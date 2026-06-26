#!/usr/bin/env python3
"""Create an Artifact Deck manifest from markdown sections and optional inline slides."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from deck_common import bullets_from_markdown, ensure_existing_path, parse_image_spec, parse_section_spec, parse_slide_spec, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Deck title.")
    parser.add_argument("--subtitle", default="", help="Deck subtitle.")
    parser.add_argument("--section", action="append", default=[], help="Repeatable TITLE=/abs/path/to/notes.md input.")
    parser.add_argument("--slide", action="append", default=[], help="Repeatable TITLE=bullet one|bullet two input.")
    parser.add_argument("--image", action="append", default=[], help="Repeatable TITLE=/abs/path/image.png|Caption input.")
    parser.add_argument("--out", required=True, help="Output manifest path.")
    args = parser.parse_args()

    slides: List[Dict[str, Any]] = []
    for spec in args.section:
        title, raw_path = parse_section_spec(spec)
        source_path = ensure_existing_path(raw_path, "--section path")
        bullets = bullets_from_markdown(source_path)
        slides.append(
            {
                "title": title,
                "bullets": bullets,
                "source": str(source_path),
            }
        )

    for spec in args.slide:
        slides.append(parse_slide_spec(spec))

    images: List[Dict[str, str]] = []
    for spec in args.image:
        item = parse_image_spec(spec)
        source_path = ensure_existing_path(item["path"], "--image path")
        images.append(
            {
                "title": item["title"],
                "path": str(source_path),
                "caption": item["caption"],
            }
        )

    payload = {
        "title": args.title.strip(),
        "subtitle": args.subtitle.strip(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "slides": slides,
        "images": images,
    }
    out_path = Path(args.out).expanduser().resolve()
    write_json(out_path, payload)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
