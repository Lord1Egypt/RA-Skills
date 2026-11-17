"""Setup detection helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core import detect_sibling_skills, load_config, save_config, default_output_dir


def detect_existing_setup(config_path=None) -> Dict[str, Any]:
    cfg = load_config(config_path)
    siblings = detect_sibling_skills()
    return {
        "config_path": cfg.get("_config_path"),
        "output_dir": cfg.get("output_dir") or str(default_output_dir()),
        "owner_aliases": cfg.get("owner_aliases") or [],
        "siblings": siblings,
        "cloud_asr_optional": siblings.get("dashscope_key_present", False),
        "needs_bailian": False,  # core path never requires it
    }
