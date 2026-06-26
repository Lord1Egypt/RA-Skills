"""Centralized storage paths for pipeline outputs."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")


def _default_output_dir() -> Path:
    """Platform-aware fallback when OUTPUT_BASE_DIR is not provided."""
    home = Path(os.getenv("USERPROFILE", Path.home())) if sys.platform.startswith("win") else Path.home()
    return home / "DouyinContentTracker"


def get_output_base_dir() -> Path:
    env_path = (
        os.getenv("OUTPUT_BASE_DIR")
        or os.getenv("OUTPUT_DIR")
        or os.getenv("TRACKER_OUTPUT_DIR")
    )
    if env_path:
        return Path(env_path).expanduser()
    return _default_output_dir()


OUTPUT_BASE_DIR = get_output_base_dir()
DATA_DIR = OUTPUT_BASE_DIR / "data"
AUDIO_DIR = OUTPUT_BASE_DIR / "audio"
SUBTITLE_DIR = OUTPUT_BASE_DIR / "subtitles"
MODEL_DIR = OUTPUT_BASE_DIR / "models"

DATA_DIR.mkdir(parents=True, exist_ok=True)

