#!/usr/bin/env python3
"""Validate a sprite package and report alpha-anchor jitter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from align_sprite_frames import ALPHA_THRESHOLD, analyze_frame, metric


def border_alpha_count(alpha: Image.Image) -> int:
    width, height = alpha.size
    values = list(alpha.crop((0, 0, width, 1)).get_flattened_data())
    values += list(alpha.crop((0, height - 1, width, height)).get_flattened_data())
    values += list(alpha.crop((0, 1, 1, height - 1)).get_flattened_data())
    values += list(
        alpha.crop((width - 1, 1, width, height - 1)).get_flattened_data()
    )
    return sum(value >= ALPHA_THRESHOLD for value in values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    package = args.package.resolve()
    manifest = json.loads((package / "sprite-manifest.json").read_text(encoding="utf-8"))
    width = int(manifest["frame"]["width"])
    height = int(manifest["frame"]["height"])
    rows = int(manifest["layout"]["rows"])
    columns = int(manifest["layout"]["columns"])
    issues: list[str] = []
    actions_report = {}

    atlas_path = package / manifest["atlas"]
    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (width * columns, height * rows):
        issues.append(f"atlas size {atlas.size} does not match grid")

    for action in manifest["actions"]:
        name = action["name"]
        count = int(action["frame_count"])
        if len(action["frames"]) != count:
            issues.append(f"{name}: frame_count mismatch")
        strip_path = package / action["strip"]
        with Image.open(strip_path) as opened:
            strip = opened.convert("RGBA")
        if strip.size != (width * count, height):
            issues.append(f"{name}: strip size {strip.size} is incorrect")

        anchors = []
        for relative in action["frames"]:
            path = package / relative
            with Image.open(path) as opened:
                image = opened.convert("RGBA")
            if image.size != (width, height):
                issues.append(f"{relative}: incorrect dimensions {image.size}")
            alpha = image.getchannel("A")
            if alpha.getbbox() is None:
                issues.append(f"{relative}: empty frame")
                continue
            if any(
                alpha.getpixel(point)
                for point in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))
            ):
                issues.append(f"{relative}: nontransparent corner")
            edge_count = border_alpha_count(alpha)
            if edge_count:
                issues.append(f"{relative}: {edge_count} alpha pixels touch outer edge")
            anchors.append(analyze_frame(path)["anchor"])
        actions_report[name] = {
            "frame_count": count,
            "anchor_jitter": metric(anchors) if anchors else None,
        }

    report = {
        "package": str(package),
        "actions": actions_report,
        "total_frames": sum(action["frame_count"] for action in manifest["actions"]),
        "frame_size": [width, height],
        "issues": issues,
    }
    report_path = args.report or package / "validation-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
