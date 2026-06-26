"""Shared Shorts detection logic.

Both device_monitor.py (for `shorts status`) and clawshorts-daemon.py
use this module for identical Shorts detection.
"""
from __future__ import annotations

import re
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Width as fraction of screen width below which an element is considered Shorts
SHORTS_WIDTH_THRESHOLD = 0.45  # 45% — portrait-ish

# Max width/height ratio for Shorts (portrait-ish: taller than wide)
SHORTS_MAX_ASPECT_RATIO = 1.3


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

class ElementInfo(NamedTuple):
    """Parsed UI element information."""
    app: str
    width: int | None
    height: int | None
    detail: str


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def is_shorts_element(width: int | None, height: int | None, screen_width: int) -> bool:
    """Return True if the given element dimensions match a Shorts video.

    Shorts videos are portrait-ish (taller than wide, or at least not wide).
    On Fire TV YouTube, Shorts appear as ~38-45% screen width.
    Regular videos are ~100% width.

    Args:
        width: Element width in pixels (can be None if unknown)
        height: Element height in pixels (can be None if unknown)
        screen_width: Screen width in pixels for threshold calculation

    Returns:
        True if element dimensions match Shorts pattern
    """
    if width is None:
        return False

    # Width must be below the threshold to be Shorts
    width_ratio = width / screen_width if screen_width else 0
    if width_ratio >= SHORTS_WIDTH_THRESHOLD:
        return False

    # If height is known, check aspect ratio (portrait-ish)
    if height is not None and height > 0:
        # Shorts are taller than wide (aspect ratio < 1.0 typically,
        # but we use inverse so we check if it exceeds the max ratio)
        # Actually: short videos are wider than tall = w/h > 1.0
        # We want to exclude very wide 16:9 content
        if width / height > SHORTS_MAX_ASPECT_RATIO:
            return False

    return True


def parse_element_from_ui_dump(ui_text: str) -> ElementInfo | None:
    """Parse the focused element from a Fire TV UI dump.

    Extracts app, width, height, and detail from a uiautomator XML dump.

    Args:
        ui_text: Raw output from uiautomator dump

    Returns:
        ElementInfo or None if no focused element found
    """
    if not ui_text or "node" not in ui_text.lower():
        return None

    # Try to extract focused/larger element
    lines = ui_text.strip().split("\n")
    for line in lines:
        if 'bounds="' in line or 'bounds="' in line:
            # Extract bounds: bounds="[left,top][right,bottom]"
            bounds_m = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', line)
            if bounds_m:
                left, top, right, bottom = (
                    int(bounds_m.group(1)),
                    int(bounds_m.group(2)),
                    int(bounds_m.group(3)),
                    int(bounds_m.group(4)),
                )
                width = right - left
                height = bottom - top
            else:
                width, height = None, None

            # Extract package/app
            package_m = re.search(r'package="([^"]+)"', line)
            app = package_m.group(1) if package_m else "unknown"

            # Extract text or content-desc for detail
            text_m = re.search(r'text="([^"]*)"', line)
            content_m = re.search(r'content-desc="([^"]*)"', line)
            detail = text_m.group(1) or content_m.group(1) or ""

            return ElementInfo(app=app, width=width, height=height, detail=detail)

    return None
