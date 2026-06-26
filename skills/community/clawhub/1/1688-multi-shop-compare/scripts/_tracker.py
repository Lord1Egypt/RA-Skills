#!/usr/bin/env python3
"""Skill 埋点上报"""

import logging
import os
from pathlib import Path

logger = logging.getLogger("1688_tracker")

_ROOT_DIR = Path(__file__).parent.parent

def _load_env_file() -> None:
    env_path = _ROOT_DIR / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key and key not in os.environ:
                os.environ[key] = value

_load_env_file()

def _get_skill_env() -> tuple:
    skill_name = os.environ.get("SKILL_NAME", "1688-multi-shop-compare")
    skill_version = os.environ.get("SKILL_VERSION", "1.0.0")
    channel = os.environ.get("SKILL_CHANNEL", "clawhub")
    return skill_name, skill_version, channel

def report_skill_usage() -> None:
    try:
        from _http import api_post
        skill_name, skill_version, channel = _get_skill_env()
        api_post(
            "/api/reportSkillsUsage/1.0.0",
            {
                "apiName": None,
                "skillsName": skill_name,
                "version": skill_version,
                "scene": "CLI",
                "channel": channel,
            },
        )
    except Exception as exc:
        logger.debug("埋点上报失败（已忽略）: %s", exc)
