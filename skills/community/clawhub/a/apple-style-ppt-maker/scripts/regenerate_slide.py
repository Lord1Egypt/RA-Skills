#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-genai>=1.0.0",
#   "pillow>=10.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""Regenerate a single slide with a revision instruction."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from workflow_core import (  # noqa: E402
    DEFAULT_MODEL,
    PlanValidationError,
    build_slide_prompt,
    ensure_output_layout,
    find_and_load_env,
    find_manifest_slide,
    get_genai_client,
    get_slide_by_number,
    load_or_init_manifest,
    load_plan,
    render_slide_image,
    resolve_output_dir,
    resolve_output_settings,
    sha256_text,
    snapshot_if_exists,
    upsert_manifest_slide,
    utc_now_iso,
    write_json,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Regenerate one slide in an existing output directory")
    parser.add_argument("--plan", required=True, help="Path to slides_plan.json")
    parser.add_argument("--slide", type=int, required=True, help="Slide number to regenerate")
    parser.add_argument("--change", required=True, help="Revision instruction for this slide")
    parser.add_argument("--out", default=None, help="Output directory containing images/prompts/meta")
    parser.add_argument("--resolution", choices=["2K", "4K"], default=None, help="Override resolution")
    parser.add_argument("--format", choices=["webp", "png", "jpg", "jpeg"], default=None, help="Override format")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image generation model")
    parser.add_argument("--retries", type=int, default=3, help="Retry count for API failures")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan).resolve()

    try:
        plan = load_plan(plan_path)
        env_path = find_and_load_env(plan_path)
        resolution, image_format = resolve_output_settings(plan, args.resolution, args.format)
        output_dir = resolve_output_dir(plan, args.out)
        layout = ensure_output_layout(output_dir)
        target_slide = get_slide_by_number(plan["slides"], args.slide)
    except PlanValidationError as exc:
        print(f"[ERROR] Invalid input: {exc}")
        return 2
    except Exception as exc:
        print(f"[ERROR] Setup failed: {exc}")
        return 2

    try:
        client = get_genai_client()
    except Exception as exc:
        print(f"[ERROR] API client initialization failed: {exc}")
        return 2

    if env_path:
        print(f"[INFO] Loaded environment from: {env_path}")
    else:
        print("[INFO] No .env file discovered, using current environment variables")

    total_slides = len(plan["slides"])
    number = target_slide["slide_number"]

    image_path = layout["images"] / f"slide-{number:02d}.{image_format}"
    prompt_path = layout["prompts"] / f"slide-{number:02d}.prompt.md"
    meta_path = layout["meta"] / f"slide-{number:02d}.meta.json"

    manifest = load_or_init_manifest(layout["manifest"], plan, resolution, image_format, args.model)
    existing = find_manifest_slide(manifest, number) or {}
    revision_count = int(existing.get("revision_count", 0)) + 1

    snapshot_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_dir = layout["history"] / f"slide-{number:02d}" / snapshot_stamp
    snapshot_if_exists(image_path, snapshot_dir, "pre")
    snapshot_if_exists(prompt_path, snapshot_dir, "pre")
    snapshot_if_exists(meta_path, snapshot_dir, "pre")

    prompt = build_slide_prompt(
        plan=plan,
        slide=target_slide,
        total_slides=total_slides,
        resolution=resolution,
        image_format=image_format,
        revision_note=args.change,
    )
    write_text(prompt_path, prompt)

    error_message = None
    status = "regenerated"
    print(f"[RUN ] regenerating slide {number}")
    try:
        render_slide_image(
            client=client,
            prompt=prompt,
            image_path=image_path,
            resolution=resolution,
            model=args.model,
            retries=max(1, args.retries),
        )
    except Exception as exc:  # pragma: no cover - depends on remote API behavior
        status = "failed"
        error_message = str(exc)
        print(f"[FAIL] slide {number}: {exc}")

    meta = {
        "slide_number": number,
        "slide_type": target_slide["slide_type"],
        "status": status,
        "generated_at": utc_now_iso(),
        "resolution": resolution,
        "format": image_format,
        "model": args.model,
        "revision_count": revision_count,
        "revision_note": args.change,
        "prompt_sha256": sha256_text(prompt),
        "image_path": str(image_path.relative_to(output_dir)),
        "prompt_path": str(prompt_path.relative_to(output_dir)),
        "history_path": str(snapshot_dir.relative_to(output_dir)),
        "error": error_message,
    }
    write_json(meta_path, meta)

    upsert_manifest_slide(
        manifest,
        {
            "slide_number": number,
            "status": status,
            "revision_count": revision_count,
            "generated_at": meta["generated_at"],
            "image_path": meta["image_path"],
            "meta_path": str(meta_path.relative_to(output_dir)),
            "prompt_path": meta["prompt_path"],
            "error": error_message,
        },
    )
    write_json(layout["manifest"], manifest)

    if status == "failed":
        return 1

    print(f"[DONE] slide {number} regenerated successfully")
    print(f"[DONE] history snapshot: {snapshot_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
