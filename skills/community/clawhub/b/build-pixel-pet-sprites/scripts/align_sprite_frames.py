#!/usr/bin/env python3
"""Align a packaged RGBA sprite set without rescaling or regenerating artwork.

The subject is located from a closed alpha mask and connected components.
The complete RGBA frame (subject plus detached effects) is translated to a
per-action median anchor. Outputs are written to a new directory.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import statistics
import zipfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter


ALPHA_THRESHOLD = 32
MORPH_KERNEL = 5
EDGE_MARGIN = 1


def percentile(values: list[int], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * fraction
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def closed_alpha_mask(image: Image.Image) -> tuple[bytearray, int, int]:
    alpha = image.getchannel("A")
    binary = alpha.point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0)
    # Pillow filters provide a deterministic morphological close: dilation then erosion.
    closed = binary.filter(ImageFilter.MaxFilter(MORPH_KERNEL)).filter(
        ImageFilter.MinFilter(MORPH_KERNEL)
    )
    width, height = image.size
    return bytearray(closed.tobytes()), width, height


def connected_components(mask: bytearray, width: int, height: int) -> list[dict]:
    visited = bytearray(width * height)
    components: list[dict] = []
    for start in range(width * height):
        if not mask[start] or visited[start]:
            continue
        queue = deque([start])
        visited[start] = 1
        pixels: list[tuple[int, int]] = []
        while queue:
            index = queue.popleft()
            y, x = divmod(index, width)
            pixels.append((x, y))
            if x and mask[index - 1] and not visited[index - 1]:
                visited[index - 1] = 1
                queue.append(index - 1)
            if x + 1 < width and mask[index + 1] and not visited[index + 1]:
                visited[index + 1] = 1
                queue.append(index + 1)
            if y and mask[index - width] and not visited[index - width]:
                visited[index - width] = 1
                queue.append(index - width)
            if y + 1 < height and mask[index + width] and not visited[index + width]:
                visited[index + width] = 1
                queue.append(index + width)
        xs = [point[0] for point in pixels]
        ys = [point[1] for point in pixels]
        components.append(
            {
                "pixels": pixels,
                "area": len(pixels),
                "bbox": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
                "centroid": [sum(xs) / len(xs), sum(ys) / len(ys)],
            }
        )
    return components


def choose_subject(components: list[dict], width: int, height: int) -> dict:
    if not components:
        raise ValueError("no alpha component found")
    cx_frame = (width - 1) / 2
    candidates = []
    for component in components:
        x0, y0, x1, y1 = component["bbox"]
        cx, cy = component["centroid"]
        centrality = max(0.18, 1.0 - abs(cx - cx_frame) / (width * 0.62))
        lower_pixels = sum(1 for _, y in component["pixels"] if y >= height * 0.62)
        lower_ratio = lower_pixels / component["area"]
        vertical_span = (y1 - y0) / height
        horizontal_span = (x1 - x0) / width
        # Area dominates; central location, body-like span, and lower-frame presence
        # reject detached panels, nodes, sparkles, and success/error symbols.
        score = component["area"] * centrality
        score *= 1.0 + min(lower_ratio, 0.45) * 1.35
        score *= 0.75 + min(vertical_span + horizontal_span, 1.2) * 0.35
        candidate = dict(component)
        candidate["score"] = score
        candidates.append(candidate)
    return max(candidates, key=lambda item: item["score"])


def subject_anchor(subject: dict) -> tuple[float, float]:
    x0, y0, x1, y1 = subject["bbox"]
    subject_height = max(1, y1 - y0)
    central = [
        (x, y)
        for x, y in subject["pixels"]
        if y0 + subject_height * 0.28 <= y <= y0 + subject_height * 0.78
    ]
    lower = [(x, y) for x, y in subject["pixels"] if y >= y0 + subject_height * 0.72]
    if not central:
        central = subject["pixels"]
    if not lower:
        lower = subject["pixels"]
    body_x = statistics.median(point[0] for point in central)
    support_x = statistics.median(point[0] for point in lower)
    anchor_x = body_x * 0.78 + support_x * 0.22
    anchor_y = percentile([point[1] for point in subject["pixels"]], 0.985)
    return anchor_x, anchor_y


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").point(lambda value: 255 if value >= ALPHA_THRESHOLD else 0).getbbox()
    if bbox is None:
        raise ValueError("empty frame")
    return bbox


def analyze_frame(path: Path) -> dict:
    with Image.open(path) as opened:
        image = opened.convert("RGBA")
    mask, width, height = closed_alpha_mask(image)
    subject = choose_subject(connected_components(mask, width, height), width, height)
    anchor_x, anchor_y = subject_anchor(subject)
    return {
        "path": path,
        "image": image,
        "anchor": [anchor_x, anchor_y],
        "subject_bbox": subject["bbox"],
        "content_bbox": list(alpha_bbox(image)),
        "component_area": subject["area"],
        "component_score": subject["score"],
    }


def clamp_offset(desired: int, low: int, high: int) -> int:
    if low > high:
        return 0
    return max(low, min(high, desired))


def translate(image: Image.Image, dx: int, dy: int) -> Image.Image:
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    output.alpha_composite(image, (dx, dy))
    return output


def metric(points: list[list[float]]) -> dict:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return {
        "x_range": round(max(xs) - min(xs), 4),
        "y_range": round(max(ys) - min(ys), 4),
        "x_stddev": round(statistics.pstdev(xs), 4),
        "y_stddev": round(statistics.pstdev(ys), 4),
    }


def save_gif(frames: list[Image.Image], path: Path, duration: int | list[int], loop: bool) -> None:
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


def next_output_path(requested: Path) -> Path:
    if not requested.exists():
        return requested
    version = 2
    while requested.with_name(f"{requested.name}-v{version}").exists():
        version += 1
    return requested.with_name(f"{requested.name}-v{version}")


def main() -> None:
    global ALPHA_THRESHOLD, MORPH_KERNEL, EDGE_MARGIN
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--alpha-threshold", type=int, default=ALPHA_THRESHOLD)
    parser.add_argument("--morph-kernel", type=int, default=MORPH_KERNEL)
    parser.add_argument("--edge-margin", type=int, default=EDGE_MARGIN)
    args = parser.parse_args()
    if args.morph_kernel < 3 or args.morph_kernel % 2 == 0:
        raise ValueError("--morph-kernel must be an odd integer >= 3")
    ALPHA_THRESHOLD = args.alpha_threshold
    MORPH_KERNEL = args.morph_kernel
    EDGE_MARGIN = args.edge_margin
    source = args.source.resolve()
    output = next_output_path(args.output.resolve())
    output.mkdir(parents=True)

    manifest = json.loads((source / "sprite-manifest.json").read_text(encoding="utf-8"))
    frame_width = manifest["frame"]["width"]
    frame_height = manifest["frame"]["height"]
    all_before: list[list[float]] = []
    all_after: list[list[float]] = []
    all_before_residuals: list[list[float]] = []
    all_after_residuals: list[list[float]] = []
    alignment_actions: dict[str, dict] = {}
    rebuilt_actions = []
    atlas = Image.new(
        "RGBA",
        (frame_width * manifest["layout"]["columns"], frame_height * manifest["layout"]["rows"]),
        (0, 0, 0, 0),
    )
    combined_preview: list[Image.Image] = []
    combined_durations: list[int] = []

    for action in manifest["actions"]:
        name = action["name"]
        analyzed = [analyze_frame(source / relative) for relative in action["frames"]]
        target_x = statistics.median(item["anchor"][0] for item in analyzed)
        target_y = statistics.median(item["anchor"][1] for item in analyzed)
        aligned_frames: list[Image.Image] = []
        frame_reports = []
        before_points = []
        after_points = []

        for index, item in enumerate(analyzed):
            desired_dx = round(target_x - item["anchor"][0])
            desired_dy = round(target_y - item["anchor"][1])
            x0, y0, x1, y1 = item["content_bbox"]
            # Preserve the complete frame and leave a transparent one-pixel border.
            dx = clamp_offset(desired_dx, EDGE_MARGIN - x0, frame_width - EDGE_MARGIN - x1)
            dy = clamp_offset(desired_dy, EDGE_MARGIN - y0, frame_height - EDGE_MARGIN - y1)
            sx0, sy0, sx1, sy1 = item["subject_bbox"]
            if not (
                sx0 + dx >= 0
                and sy0 + dy >= 0
                and sx1 + dx <= frame_width
                and sy1 + dy <= frame_height
            ):
                raise ValueError(f"main subject would clip: {name} frame {index + 1}")
            aligned = translate(item["image"], dx, dy)
            frame_path = output / "frames" / name / f"{name}-{index + 1:02d}.png"
            frame_path.parent.mkdir(parents=True, exist_ok=True)
            aligned.save(frame_path)
            aligned_frames.append(aligned)
            atlas.alpha_composite(aligned, (index * frame_width, action["row"] * frame_height))
            before = item["anchor"]
            after = [before[0] + dx, before[1] + dy]
            before_points.append(before)
            after_points.append(after)
            all_before.append(before)
            all_after.append(after)
            frame_reports.append(
                {
                    "frame": index + 1,
                    "file": str(frame_path.relative_to(output)).replace("\\", "/"),
                    "dx": dx,
                    "dy": dy,
                    "anchor_before": [round(value, 4) for value in before],
                    "anchor_after": [round(value, 4) for value in after],
                    "subject_bbox_before": item["subject_bbox"],
                    "subject_bbox_after": [sx0 + dx, sy0 + dy, sx1 + dx, sy1 + dy],
                    "content_bbox_before": item["content_bbox"],
                }
            )

        frame_count = len(aligned_frames)
        strip = Image.new(
            "RGBA", (frame_width * frame_count, frame_height), (0, 0, 0, 0)
        )
        for index, aligned in enumerate(aligned_frames):
            strip.alpha_composite(aligned, (index * frame_width, 0))
        strip_path = output / "strips" / f"{name}-{frame_count}f.png"
        strip_path.parent.mkdir(parents=True, exist_ok=True)
        strip.save(strip_path)
        save_gif(
            aligned_frames,
            output / "preview" / f"{name}.gif",
            action["frame_duration_ms"],
            action["loop"],
        )
        combined_preview.extend(aligned_frames)
        combined_durations.extend([action["frame_duration_ms"]] * 6)

        updated_action = dict(action)
        updated_action["strip"] = f"strips/{name}-{frame_count}f.png"
        updated_action["frames"] = [
            f"frames/{name}/{name}-{index + 1:02d}.png"
            for index in range(frame_count)
        ]
        updated_action["alignment"] = {
            "target_anchor_px": [round(target_x, 4), round(target_y, 4)],
            "frames": [
                {"frame": report["frame"], "dx": report["dx"], "dy": report["dy"]}
                for report in frame_reports
            ],
        }
        rebuilt_actions.append(updated_action)
        alignment_actions[name] = {
            "target_anchor_px": [round(target_x, 4), round(target_y, 4)],
            "jitter_before": metric(before_points),
            "jitter_after": metric(after_points),
            "frames": frame_reports,
        }
        before_median_x = statistics.median(point[0] for point in before_points)
        before_median_y = statistics.median(point[1] for point in before_points)
        after_median_x = statistics.median(point[0] for point in after_points)
        after_median_y = statistics.median(point[1] for point in after_points)
        all_before_residuals.extend(
            [[point[0] - before_median_x, point[1] - before_median_y] for point in before_points]
        )
        all_after_residuals.extend(
            [[point[0] - after_median_x, point[1] - after_median_y] for point in after_points]
        )

    atlas_relative = Path(manifest["atlas"])
    atlas_path = output / atlas_relative
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(atlas_path)
    save_gif(
        combined_preview,
        output / "preview" / "all-actions-preview.gif",
        combined_durations,
        True,
    )

    manifest["atlas"] = atlas_relative.as_posix()
    manifest["actions"] = rebuilt_actions
    manifest["alignment"] = {
        "mode": "deterministic-alpha-component-translation",
        "target_strategy": "per-action median anchor",
        "alpha_threshold": ALPHA_THRESHOLD,
        "morphological_close_kernel": MORPH_KERNEL,
        "subject_selection": "largest body-like central component weighted by lower-frame presence",
        "anchor": "78% central-body median-x + 22% lower-support median-x; y=98.5th subject percentile",
        "transform": "integer translation only; no scaling, rotation, or filtering",
    }
    (output / "sprite-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    issues = []
    edge_alpha_counts = {}
    for action in manifest["actions"]:
        if action["frame_count"] != len(action["frames"]):
            issues.append(f"{action['name']}: manifest frame count mismatch")
        for relative in action["frames"]:
            path = output / relative
            with Image.open(path) as opened:
                image = opened.convert("RGBA")
            if image.size != (frame_width, frame_height):
                issues.append(f"{relative}: incorrect dimensions")
            if image.getbbox() is None:
                issues.append(f"{relative}: empty frame")
            alpha = image.getchannel("A")
            corners = [alpha.getpixel((0, 0)), alpha.getpixel((frame_width - 1, 0)),
                       alpha.getpixel((0, frame_height - 1)), alpha.getpixel((frame_width - 1, frame_height - 1))]
            if any(corners):
                issues.append(f"{relative}: nontransparent corner")
            border = list(alpha.crop((0, 0, frame_width, 1)).get_flattened_data())
            border += list(alpha.crop((0, frame_height - 1, frame_width, frame_height)).get_flattened_data())
            border += list(alpha.crop((0, 1, 1, frame_height - 1)).get_flattened_data())
            border += list(alpha.crop((frame_width - 1, 1, frame_width, frame_height - 1)).get_flattened_data())
            count = sum(1 for value in border if value >= ALPHA_THRESHOLD)
            edge_alpha_counts[relative] = count
            if count:
                issues.append(f"{relative}: {count} alpha pixels touch outer edge")

    report = {
        "source": str(source),
        "output": str(output),
        "algorithm": manifest["alignment"],
        "actions": alignment_actions,
        "overall_within_action_jitter_before": metric(all_before_residuals),
        "overall_within_action_jitter_after": metric(all_after_residuals),
        "global_anchor_spread_before": metric(all_before),
        "global_anchor_spread_after": metric(all_after),
        "validation": {
            "expected_actions": len(manifest["actions"]),
            "expected_frames_per_action": {
                action["name"]: action["frame_count"]
                for action in manifest["actions"]
            },
            "total_frames": sum(
                action["frame_count"] for action in manifest["actions"]
            ),
            "frame_size": [frame_width, frame_height],
            "mode": "RGBA",
            "edge_alpha_counts": edge_alpha_counts,
            "issues": issues,
        },
    }
    (output / "alignment-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "validation-report.json").write_text(
        json.dumps(report["validation"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for optional_name in (
        "generation-prompts.json",
        "character-master.png",
        "package-config.json",
    ):
        optional_path = source / optional_name
        if optional_path.exists():
            shutil.copy2(optional_path, output / optional_name)

    zip_path = output.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                archive.write(path, Path(output.name) / path.relative_to(output))
    print(json.dumps({"output": str(output), "zip": str(zip_path), "issues": issues,
                      "before": report["overall_within_action_jitter_before"],
                      "after": report["overall_within_action_jitter_after"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
