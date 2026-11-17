#!/usr/bin/env python3
"""Normalize a transparent sprite atlas and build a web-ready package."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from PIL import Image


def versioned_path(path: Path) -> Path:
    if not path.exists():
        return path
    version = 2
    while path.with_name(f"{path.name}-v{version}").exists():
        version += 1
    return path.with_name(f"{path.name}-v{version}")


def save_gif(
    frames: list[Image.Image], path: Path, duration: int | list[int], loop: bool
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0 if loop else 1,
        disposal=2,
        transparency=0,
        optimize=False,
    )


def validate_config(config: dict) -> None:
    actions = config.get("actions", [])
    frame = config.get("frame", {})
    if not actions:
        raise ValueError("config.actions must not be empty")
    if int(frame.get("width", 0)) <= 0 or int(frame.get("height", 0)) <= 0:
        raise ValueError("config.frame width and height must be positive")
    names = [action.get("name") for action in actions]
    if any(not name for name in names) or len(names) != len(set(names)):
        raise ValueError("action names must be present and unique")
    for action in actions:
        if int(action.get("frame_count", 0)) <= 0:
            raise ValueError(f"{action['name']}: frame_count must be positive")
        if int(action.get("frame_duration_ms", 0)) <= 0:
            raise ValueError(f"{action['name']}: frame_duration_ms must be positive")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas", type=Path, help="Transparent RGBA source atlas")
    parser.add_argument("config", type=Path, help="JSON action/grid configuration")
    parser.add_argument("output", type=Path, help="Requested output directory")
    parser.add_argument(
        "--character-master",
        type=Path,
        help="Optional character master image to include",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_config(config)
    output = versioned_path(args.output.resolve())
    output.mkdir(parents=True)

    actions = config["actions"]
    frame_width = int(config["frame"]["width"])
    frame_height = int(config["frame"]["height"])
    columns = max(int(action["frame_count"]) for action in actions)
    rows = len(actions)
    atlas_name = config.get("atlas_name", "sprite-atlas.png")
    atlas_relative = Path("atlas") / atlas_name

    with Image.open(args.atlas) as opened:
        source = opened.convert("RGBA")
    normalized = source.resize(
        (columns * frame_width, rows * frame_height), Image.Resampling.NEAREST
    )
    atlas_path = output / atlas_relative
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    normalized.save(atlas_path)

    manifest_actions = []
    combined_frames: list[Image.Image] = []
    combined_durations: list[int] = []

    for row, action in enumerate(actions):
        name = action["name"]
        count = int(action["frame_count"])
        duration = int(action["frame_duration_ms"])
        loop = bool(action.get("loop", True))
        frames: list[Image.Image] = []
        frame_paths: list[str] = []

        for column in range(count):
            box = (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
            frame = normalized.crop(box)
            if frame.getchannel("A").getbbox() is None:
                raise ValueError(f"{name} frame {column + 1} is empty")
            relative = Path("frames") / name / f"{name}-{column + 1:02d}.png"
            path = output / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            frame.save(path)
            frames.append(frame)
            frame_paths.append(relative.as_posix())

        strip = Image.new("RGBA", (count * frame_width, frame_height), (0, 0, 0, 0))
        for column, frame in enumerate(frames):
            strip.alpha_composite(frame, (column * frame_width, 0))
        strip_relative = Path("strips") / f"{name}-{count}f.png"
        strip_path = output / strip_relative
        strip_path.parent.mkdir(parents=True, exist_ok=True)
        strip.save(strip_path)
        save_gif(frames, output / "preview" / f"{name}.gif", duration, loop)
        combined_frames.extend(frames)
        combined_durations.extend([duration] * count)

        manifest_actions.append(
            {
                "name": name,
                "row": row,
                "frame_count": count,
                "frame_duration_ms": duration,
                "loop": loop,
                "strip": strip_relative.as_posix(),
                "frames": frame_paths,
                "anchor": action.get("anchor", {"x": 0.5, "y": 0.92}),
                "anchor_px": {
                    "x": round(frame_width * float(action.get("anchor", {}).get("x", 0.5))),
                    "y": round(frame_height * float(action.get("anchor", {}).get("y", 0.92))),
                },
            }
        )

    save_gif(
        combined_frames,
        output / "preview" / "all-actions-preview.gif",
        combined_durations,
        True,
    )
    manifest = {
        "character": config.get("character", "pixel-pet"),
        "atlas": atlas_relative.as_posix(),
        "layout": {"rows": rows, "columns": columns, "order": "row-major"},
        "frame": {"width": frame_width, "height": frame_height, "format": "RGBA PNG"},
        "actions": manifest_actions,
    }
    (output / "sprite-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    shutil.copy2(args.config, output / "package-config.json")
    if args.character_master:
        shutil.copy2(args.character_master, output / "character-master.png")

    zip_path = output.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                archive.write(path, Path(output.name) / path.relative_to(output))
    print(json.dumps({"output": str(output), "zip": str(zip_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
