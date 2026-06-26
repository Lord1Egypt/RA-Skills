"""Shared constants for ClawShorts."""
from __future__ import annotations

from pathlib import Path

__all__ = [
    "STATE_DIR",
    "CONFIG_DIR",
    "SHORTS_WIDTH_THRESHOLD_STRICT",
    "SHORTS_PIXEL_THRESHOLD",
    "MAX_DELTA_SECONDS",
    "SHORTS_FALLBACK_HEIGHT_RATIO",
    "DEFAULT_SCREEN_WIDTH",
    "DEFAULT_SCREEN_HEIGHT",
    "SHORTS_DELTA_CAP",
]

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

STATE_DIR = Path.home() / ".clawshorts"
CONFIG_DIR = STATE_DIR

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

# Default screen dimensions when we cannot query the device
DEFAULT_SCREEN_WIDTH = 1920
DEFAULT_SCREEN_HEIGHT = 1080

# Shorts detection: element must be narrower than this fraction of screen width
SHORTS_WIDTH_THRESHOLD_STRICT = 0.45  # 45% width cap for Shorts

# Loose pixel threshold (90% of 1920 default width) — used in device_monitor.py
SHORTS_PIXEL_THRESHOLD = int(0.90 * DEFAULT_SCREEN_WIDTH)  # 1728

# Max w/h ratio for Shorts (portrait-ish, distinguishes from 16:9 hover previews)
SHORTS_MAX_ASPECT_RATIO = 1.3

# Fallback: element height must exceed this fraction of screen height
SHORTS_FALLBACK_HEIGHT_RATIO = 0.4

# Max gap (seconds) between consecutive Shorts detections that still counts
# as continuous watch time. Lowered from 30s to 15s so brief pauses
# (replying to a text) don't reset counter.
MAX_DELTA_SECONDS = 15.0

# Max seconds per poll to add (prevents abuse / clock skew)
SHORTS_DELTA_CAP = 300
