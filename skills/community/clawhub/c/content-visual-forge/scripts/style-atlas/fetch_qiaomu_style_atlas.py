#!/usr/bin/env python3
"""Fetch and snapshot Qiaomu Artist Style metadata.

This script stores structured style metadata only. It does not download or
vendor generated images.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


DEFAULT_URL = "https://style.qiaomu.ai/"
DEFAULT_OUTPUT = Path("content-visual-forge/assets/style-atlas/qiaomu-style-atlas.snapshot.json")


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "skill-hub-style-atlas-snapshot/1.0"})
    with urlopen(request, timeout=60) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def extract_title(html: str) -> str:
    match = re.search(r"<title>([^<]+)</title>", html)
    return match.group(1).strip() if match else ""


def extract_description(html: str) -> str:
    match = re.search(r'<meta name="description" content="([^"]+)"', html)
    return match.group(1).strip() if match else ""


def extract_prompt_template(unescaped_html: str) -> str:
    match = re.search(r'"promptTemplate":"([^"]+)"', unescaped_html)
    return match.group(1).strip() if match else ""


def extract_entries(html: str) -> list[dict[str, object]]:
    unescaped = html.replace('\\"', '"')
    object_fragments = re.findall(r'\{"id":"[^{}]+?"(?:,"[^{}]+?:[^{}]+?)*?\}', unescaped)

    entries: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    required = {
        "id",
        "name",
        "chineseName",
        "displayName",
        "movement",
        "movementZh",
        "sourceOrder",
        "sourceCategory",
        "sourceCategoryZh",
        "cue",
        "image",
    }

    for fragment in object_fragments:
        try:
            raw = json.loads(fragment)
        except json.JSONDecodeError:
            continue

        if not required.issubset(raw):
            continue
        if raw["id"] in seen_ids:
            continue

        seen_ids.add(raw["id"])
        entries.append(
            {
                "id": raw["id"],
                "name": raw["name"],
                "chinese_name": raw["chineseName"],
                "display_name": raw["displayName"],
                "movement": raw["movement"],
                "movement_zh": raw["movementZh"],
                "source_order": raw["sourceOrder"],
                "source_category": raw["sourceCategory"],
                "source_category_zh": raw["sourceCategoryZh"],
                "cue": raw["cue"],
                "image_path": raw["image"],
            }
        )

    entries.sort(key=lambda item: (str(item["movement_zh"]), int(item["source_order"]), str(item["id"])))
    return entries


def build_families(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for entry in entries:
        grouped[str(entry["movement_zh"])].append(entry)

    families: list[dict[str, object]] = []
    for movement_zh, group in grouped.items():
        cue = Counter(str(item["cue"]) for item in group).most_common(1)[0][0]
        movement = str(group[0]["movement"])
        family_id = re.sub(r"[^a-z0-9]+", "-", movement.lower()).strip("-") or "style-family"
        families.append(
            {
                "family_id": family_id,
                "movement": movement,
                "movement_zh": movement_zh,
                "cue": cue,
                "entry_count": len(group),
                "sample_entry_ids": [str(item["id"]) for item in group[:12]],
            }
        )

    families.sort(key=lambda item: (-int(item["entry_count"]), str(item["movement_zh"])))
    return families


def build_snapshot(html: str, source_url: str, snapshot_date: str | None) -> dict[str, object]:
    unescaped = html.replace('\\"', '"')
    entries = extract_entries(html)
    if not entries:
        raise RuntimeError("No style atlas entries found in fetched HTML.")

    date_value = snapshot_date or datetime.now(timezone.utc).date().isoformat()
    return {
        "schema_version": 1,
        "source": {
            "name": "Qiaomu Artist Style",
            "url": source_url,
            "title": extract_title(html),
            "description": extract_description(html),
            "prompt_template": extract_prompt_template(unescaped),
            "snapshot_date": date_value,
            "image_policy": "metadata_only_no_image_downloads",
        },
        "usage_policy": {
            "runtime_default": "use_local_snapshot",
            "refresh_policy": "manual_maintenance_only",
            "artist_name_policy": "translate_to_style_factors_before_prompting",
            "do_not_copy": [
                "specific artwork composition",
                "atlas image layout",
                "living artist signature style",
                "recognizable IP or brand elements",
            ],
        },
        "families": build_families(entries),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--snapshot-date", help="ISO date to pin in the snapshot metadata.")
    args = parser.parse_args()

    html = fetch_text(args.url)
    snapshot = build_snapshot(html, args.url, args.snapshot_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"Wrote {args.output} with "
        f"{len(snapshot['entries'])} entries and {len(snapshot['families'])} families."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
