#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PRESETS = {
    "iphone-status-bar": [("0", "0", "100%", "7%")],
    "android-status-bar": [("0", "0", "100%", "6%")],
    "bottom-nav-bar": [("0", "92%", "100%", "8%")],
    "notification-banner": [("0", "0", "100%", "16%")],
    "subtitle-strip": [("0", "82%", "100%", "18%")],
}


def parse_value(raw: str, total: int) -> int:
    raw = raw.strip()
    if raw.endswith("%"):
        return round(float(raw[:-1]) * total / 100.0)
    return int(raw)


def parse_region(spec: str, width: int, height: int):
    parts = spec.split(":")
    if len(parts) != 4:
        raise ValueError(f"Invalid region '{spec}'. Expected x:y:w:h")
    x = parse_value(parts[0], width)
    y = parse_value(parts[1], height)
    w = parse_value(parts[2], width)
    h = parse_value(parts[3], height)
    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid non-positive region size in '{spec}'")
    x = max(0, min(x, width))
    y = max(0, min(y, height))
    w = max(0, min(w, width - x))
    h = max(0, min(h, height - y))
    if w == 0 or h == 0:
        raise ValueError(f"Region '{spec}' falls outside the frame")
    return {"spec": spec, "x": x, "y": y, "w": w, "h": h}


def write_pgm(path: Path, width: int, height: int, rows):
    with path.open("w", encoding="ascii") as fh:
        fh.write("P2\n")
        fh.write(f"{width} {height}\n")
        fh.write("255\n")
        for row in rows:
            fh.write(" ".join(str(value) for value in row))
            fh.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Generate a grayscale PGM mask for FFmpeg removelogo workflows.")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--region", action="append", default=[])
    parser.add_argument("--preset", action="append", default=[])
    parser.add_argument("--manifest-output")
    args = parser.parse_args()

    width = args.width
    height = args.height
    if width <= 0 or height <= 0:
        raise SystemExit("Width and height must be positive")

    region_specs = list(args.region)
    for preset in args.preset:
        if preset not in PRESETS:
            valid = ", ".join(sorted(PRESETS))
            raise SystemExit(f"Unknown preset '{preset}'. Valid presets: {valid}")
        region_specs.extend(":".join(region) for region in PRESETS[preset])

    if not region_specs:
        raise SystemExit("At least one --region or --preset is required")

    regions = [parse_region(spec, width, height) for spec in region_specs]

    rows = []
    for y in range(height):
        row = [0] * width
        for region in regions:
            if region["y"] <= y < region["y"] + region["h"]:
                start = region["x"]
                end = region["x"] + region["w"]
                row[start:end] = [255] * (end - start)
        rows.append(row)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_pgm(output_path, width, height, rows)

    manifest = {
        "width": width,
        "height": height,
        "regions": regions,
        "presets": args.preset,
        "mask": str(output_path.resolve()),
    }
    if args.manifest_output:
        manifest_path = Path(args.manifest_output)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(str(output_path.resolve()))


if __name__ == "__main__":
    main()
