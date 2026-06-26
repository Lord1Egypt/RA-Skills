#!/usr/bin/env python3
"""Scan iOS project for image assets (xcassets imagesets + loose images)."""

from __future__ import annotations
from pathlib import Path

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".pdf", ".svg"}


def scan_imagesets(root: Path) -> list[dict]:
    """Scan *.xcassets for *.imageset directories."""
    images: list[dict] = []
    seen: set[str] = set()
    for iset in root.rglob("*.imageset"):
        if "/Pods/" in str(iset):
            continue
        name = iset.stem
        if name in seen:
            continue
        seen.add(name)
        # Determine type from contents
        contents_json = iset / "Contents.json"
        img_type = "imageset"
        if contents_json.is_file():
            # Check if it contains PDF/SVG (vector)
            for child in iset.iterdir():
                if child.suffix in (".pdf", ".svg"):
                    img_type = "vector"
                    break
        images.append({
            "name": name,
            "type": img_type,
            "source": str(iset),
        })
    return images


def scan_loose_images(root: Path) -> list[dict]:
    """
    Scan for image files outside *.xcassets.

    Looks for .png/.jpg/.pdf/.svg files not inside xcassets or Pods.
    """
    images: list[dict] = []
    seen: set[str] = set()
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in _IMAGE_EXTS:
            continue
        fstr = str(f)
        if "/Pods/" in fstr or ".xcassets/" in fstr:
            continue
        name = f.stem
        key = f"{name}@{f.parent}"
        if key in seen:
            continue
        seen.add(key)
        images.append({
            "name": name,
            "type": f.suffix.lstrip("."),
            "source": fstr,
        })
    return images
