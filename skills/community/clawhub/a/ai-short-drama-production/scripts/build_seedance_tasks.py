#!/usr/bin/env python3
"""Build Seedance task JSONL from a shot manifest and project profile."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def load_profile(path: Path | None) -> dict:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value, default=False):
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_reference(value: str) -> bool:
    value = value.strip()
    return value.startswith("data:") or value.startswith("http://") or value.startswith("https://") or value.startswith("asset://")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shot-manifest", required=True, help="CSV shot manifest")
    parser.add_argument("--project-profile", help="project_profile.json")
    parser.add_argument("--output", required=True, help="Output JSONL path")
    parser.add_argument("--model", help="Override model ID")
    parser.add_argument("--resolution", help="Override resolution")
    parser.add_argument("--ratio", help="Override aspect ratio")
    parser.add_argument("--strict", action="store_true", help="Fail on missing prompt/duration/reference")
    args = parser.parse_args()

    profile = load_profile(Path(args.project_profile)) if args.project_profile else {}
    generation = profile.get("generation", {})
    models = profile.get("models", {})
    video_model = args.model or models.get("video", {}).get("model_id") or "doubao-seedance-2-5-260628"
    default_ratio = args.ratio or generation.get("ratios", ["9:16"])[0]
    default_resolution = args.resolution or generation.get("resolutions", ["720p"])[0]
    default_audio = generation.get("generate_audio", False)
    default_watermark = generation.get("watermark", False)
    max_duration = float(generation.get("max_task_duration_sec", 30))

    manifest_path = Path(args.shot_manifest)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    warnings: list[str] = []
    tasks: list[dict] = []
    with manifest_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    for idx, row in enumerate(rows, start=2):
        prompt = (row.get("prompt") or row.get("seedance_prompt") or "").strip()
        shot_id = (row.get("shot_id") or f"row-{idx}").strip()
        if not prompt:
            msg = f"row {idx} ({shot_id}): missing prompt"
            warnings.append(msg)
            if args.strict:
                raise SystemExit(msg)
            continue
        try:
            duration = float(row.get("duration_sec") or row.get("duration") or 0)
        except ValueError:
            duration = 0
        if duration < 4 or duration > max_duration:
            msg = f"row {idx} ({shot_id}): duration {duration} outside 4-{max_duration:g}s"
            warnings.append(msg)
            if args.strict:
                raise SystemExit(msg)
            continue

        content = [{"type": "text", "text": prompt}]
        local_refs = []
        refs = (row.get("reference_urls") or row.get("reference_image_urls") or row.get("reference_ids") or "").strip()
        if refs:
            for ref in [x.strip() for x in refs.replace("\n", "|").split("|") if x.strip()]:
                if not is_reference(ref):
                    if Path(ref).exists():
                        local_refs.append(ref)
                        warnings.append(f"row {idx} ({shot_id}): local reference kept in meta.reference_paths; use --embed-local-refs at submit")
                        continue
                    msg = f"row {idx} ({shot_id}): reference is not URL/data URI/asset ID or existing local file: {ref[:80]}"
                    warnings.append(msg)
                    if args.strict:
                        raise SystemExit(msg)
                    continue
                content.append({"type": "image_url", "image_url": {"url": ref}, "role": "reference_image"})
        else:
            warnings.append(f"row {idx} ({shot_id}): no reference_urls; task will be text-only")

        project_id = (row.get("project_id") or profile.get("project", {}).get("project_id") or "project").strip()
        series = (row.get("series") or profile.get("series", [{}])[0].get("series_id") or "main").strip()
        episode = (row.get("episode") or "E01").strip()
        custom_id = f"{project_id}-{series}-{episode}-{shot_id}".replace(" ", "_")
        task = {
            "custom_id": custom_id,
            "model": video_model,
            "content": content,
            "ratio": (row.get("ratio") or default_ratio).strip(),
            "resolution": (row.get("resolution") or default_resolution).strip(),
            "duration": int(duration) if duration.is_integer() else duration,
            "generate_audio": parse_bool(row.get("generate_audio"), default_audio),
            "watermark": parse_bool(row.get("watermark"), default_watermark),
            "return_last_frame": True,
            "meta": {
                "series": series,
                "episode": episode,
                "shot_id": shot_id,
                "scene_id": row.get("scene_id", ""),
                "story_function": row.get("story_function", ""),
                "coverage_role": row.get("coverage_role", ""),
                "camera_intention": row.get("camera_intention", ""),
                "transition": row.get("transition", ""),
                "vfx_level": row.get("vfx_level", ""),
                "reference_paths": local_refs,
            },
        }
        tasks.append(task)

    with output_path.open("w", encoding="utf-8") as f:
        for task in tasks:
            f.write(json.dumps(task, ensure_ascii=False) + "\n")

    summary = {
        "shot_manifest": str(manifest_path),
        "project_profile": args.project_profile,
        "output": str(output_path),
        "rows_read": len(rows),
        "tasks_written": len(tasks),
        "model": video_model,
        "default_ratio": default_ratio,
        "default_resolution": default_resolution,
        "warnings": warnings,
    }
    summary_path = output_path.with_suffix(output_path.suffix + ".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not tasks:
        sys.exit(1)


if __name__ == "__main__":
    main()
