#!/usr/bin/env python3
"""兼容层：实现已迁至 common/open_aigc_person.py 与 common/open_api_client.py。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from open_aigc_person import (  # noqa: F401
    LORA_FAILED,
    LORA_RUNNING,
    LORA_SUCCESS,
    MOTION_FAILED,
    MOTION_RUNNING,
    MOTION_SUCCESS,
    PHOTO_FAILED,
    PHOTO_RUNNING,
    PHOTO_SUCCESS,
    first_output_url,
    get_lora_task,
    get_motion_task,
    get_photo_task,
    list_photo_tasks,
)
from open_api_client import api_get, api_post

__all__ = [
    "api_get",
    "api_post",
    "LORA_FAILED",
    "LORA_RUNNING",
    "LORA_SUCCESS",
    "MOTION_FAILED",
    "MOTION_RUNNING",
    "MOTION_SUCCESS",
    "PHOTO_FAILED",
    "PHOTO_RUNNING",
    "PHOTO_SUCCESS",
    "first_output_url",
    "get_lora_task",
    "get_motion_task",
    "get_photo_task",
    "list_photo_tasks",
]
