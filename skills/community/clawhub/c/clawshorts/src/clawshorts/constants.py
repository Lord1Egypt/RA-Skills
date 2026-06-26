"""Shared constants for ClawShorts."""
from __future__ import annotations

from pathlib import Path

__all__ = [
    "STATE_DIR",
    "CONFIG_DIR",
    "DEFAULT_SCREEN_WIDTH",
    "DEFAULT_SCREEN_HEIGHT",
    "MAX_DELTA_SECONDS",
]

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

STATE_DIR = Path.home() / ".clawshorts"
CONFIG_DIR = STATE_DIR

# ---------------------------------------------------------------------------
# Screen defaults (CLI-only fallback; daemon uses DB-loaded values)
# ---------------------------------------------------------------------------

DEFAULT_SCREEN_WIDTH = 1920
DEFAULT_SCREEN_HEIGHT = 1080

# ---------------------------------------------------------------------------
# Detection (fallback only — primary values come from DB config)
# ---------------------------------------------------------------------------

# Max gap (seconds) between consecutive Shorts detections that still counts
# as continuous watch time.
MAX_DELTA_SECONDS = 15.0
