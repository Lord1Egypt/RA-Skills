#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-genai>=1.0.0",
#   "pillow>=10.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""Generate presentation slide images from a strict slides_plan.json file."""

from __future__ import annotations

import argparse
import sys
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
    load_or_init_manifest,
    load_plan,
    render_slide_image,
    resolve_output_dir,
    resolve_output_settings,
    sha256_text,
    upsert_manifest_slide,
    utc_now_iso,
    write_json,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate slide images from a strict JSON plan")
    parser.add_argument("--plan", required=True, help="Path to slides_plan.json")
    parser.add_argument("--out", default=None, help="Output directory (optional)")
    parser.add_argument("--resolution", choices=["2K", "4K"], default=None, help="Override resolution")
    parser.add_argument("--format", choices=["webp", "png", "jpg", "jpeg"], default=None, help="Override format")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image generation model")
    parser.add_argument("--retries", type=int, default=3, help="Per-slide retry count for API failures")
    parser.add_argument("--from-slide", type=int, default=None, help="Start slide number for partial rendering")
    parser.add_argument("--to-slide", type=int, default=None, help="End slide number for partial rendering")
    parser.add_argument("--force", action="store_true", help="Regenerate even if output image already exists")
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
    except PlanValidationError as exc:
        print(f"[ERROR] Invalid plan: {exc}")
        return 2
    except Exception as exc:
        print(f"[ERROR] Setup failed: {exc}")
        return 2

    slides = plan["slides"]
    total_slides = len(slides)
    start = args.from_slide if args.from_slide is not None else 1
    end = args.to_slide if args.to_slide is not None else total_slides

    if start < 1 or end < start or end > total_slides:
        print(f"[ERROR] Invalid range: from-slide={start}, to-slide={end}, total={total_slides}")
        return 2

    selected_numbers = set(range(start, end + 1))

    try:
        client = get_genai_client()
    except Exception as exc:
        print(f"[ERROR] API client initialization failed: {exc}")
        return 2

    manifest = load_or_init_manifest(layout["manifest"], plan, resolution, image_format, args.model)

    generated = 0
    skipped = 0
    failed = 0

    if env_path:
        print(f"[INFO] Loaded environment from: {env_path}")
    else:
        print("[INFO] No .env file discovered, using current environment variables")
    print(f"[INFO] Rendering slides {start}..{end} ({len(selected_numbers)} slide(s))")
    print(f"[INFO] Output: {output_dir}")
    print(f"[INFO] Settings: resolution={resolution}, format={image_format}, model={args.model}")

    for slide in slides:
        number = slide["slide_number"]
        if number not in selected_numbers:
            continue

        image_path = layout["images"] / f"slide-{number:02d}.{image_format}"
        prompt_path = layout["prompts"] / f"slide-{number:02d}.prompt.md"
        meta_path = layout["meta"] / f"slide-{number:02d}.meta.json"

        prompt = build_slide_prompt(
            plan=plan,
            slide=slide,
            total_slides=total_slides,
            resolution=resolution,
            image_format=image_format,
        )
        write_text(prompt_path, prompt)

        existing = find_manifest_slide(manifest, number) or {}
        revision_count = int(existing.get("revision_count", 0))

        status = "generated"
        error_message = None

        if image_path.exists() and not args.force:
            status = "skipped_existing"
            skipped += 1
            print(f"[SKIP] slide {number}: existing image found")
        else:
            print(f"[RUN ] slide {number}: generating image")
            try:
                render_slide_image(
                    client=client,
                    prompt=prompt,
                    image_path=image_path,
                    resolution=resolution,
                    model=args.model,
                    retries=max(1, args.retries),
                )
                generated += 1
            except Exception as exc:  # pragma: no cover - depends on remote API behavior
                status = "failed"
                error_message = str(exc)
                failed += 1
                print(f"[FAIL] slide {number}: {exc}")

        meta = {
            "slide_number": number,
            "slide_type": slide["slide_type"],
            "status": status,
            "generated_at": utc_now_iso(),
            "resolution": resolution,
            "format": image_format,
            "model": args.model,
            "revision_count": revision_count,
            "prompt_sha256": sha256_text(prompt),
            "image_path": str(image_path.relative_to(output_dir)),
            "prompt_path": str(prompt_path.relative_to(output_dir)),
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

    print("[DONE] Generation completed")
    print(f"[DONE] generated={generated}, skipped={skipped}, failed={failed}")
    print(f"[DONE] manifest={layout['manifest']}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
