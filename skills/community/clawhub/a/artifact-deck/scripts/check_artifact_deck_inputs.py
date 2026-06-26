#!/usr/bin/env python3
"""Validate an Artifact Deck manifest before build."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List

from deck_common import MAX_BULLETS, ensure_existing_path, load_json, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Artifact Deck manifest JSON.")
    parser.add_argument("--out", required=True, help="Validation report JSON.")
    args = parser.parse_args()

    manifest_path = ensure_existing_path(args.manifest, "--manifest")
    manifest = load_json(manifest_path)
    out_path = Path(args.out).expanduser().resolve()

    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    title = str(manifest.get("title") or "").strip()
    slides = manifest.get("slides") or []
    images = manifest.get("images") or []

    if not title:
        errors.append({"code": "missing-title", "message": "Manifest title is required."})
    if not slides and not images:
        errors.append({"code": "empty-deck", "message": "Manifest must contain at least one slide or image appendix entry."})

    for index, slide in enumerate(slides, start=1):
        slide_title = str(slide.get("title") or "").strip()
        bullets = slide.get("bullets") or []
        if not slide_title:
            errors.append({"code": "missing-slide-title", "message": f"Slide {index} is missing a title."})
        if not isinstance(bullets, list) or not bullets:
            errors.append({"code": "missing-slide-bullets", "message": f"Slide {slide_title or index} has no bullets."})
            continue
        cleaned = [str(item).strip() for item in bullets if str(item).strip()]
        if not cleaned:
            errors.append({"code": "empty-slide-bullets", "message": f"Slide {slide_title or index} has no usable bullets."})
        if len(cleaned) > MAX_BULLETS:
            warnings.append({"code": "too-many-bullets", "message": f"Slide {slide_title or index} has more than {MAX_BULLETS} bullets."})

    for index, image in enumerate(images, start=1):
        image_title = str(image.get("title") or "").strip()
        image_path = str(image.get("path") or "").strip()
        if not image_title:
            errors.append({"code": "missing-image-title", "message": f"Image entry {index} is missing a title."})
        if not image_path:
            errors.append({"code": "missing-image-path", "message": f"Image entry {image_title or index} is missing a path."})
            continue
        if not Path(image_path).expanduser().resolve().exists():
            errors.append({"code": "missing-image-file", "message": f"Image entry {image_title or index} points to a missing file: {image_path}"})

    payload: Dict[str, Any] = {
        "manifest": str(manifest_path),
        "slide_count": len(slides),
        "image_count": len(images),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "status": "fix-required" if errors else "ok",
        "errors": errors,
        "warnings": warnings,
    }
    write_json(out_path, payload)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
