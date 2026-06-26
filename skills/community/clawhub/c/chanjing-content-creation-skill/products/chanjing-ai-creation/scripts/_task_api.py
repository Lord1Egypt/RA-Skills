#!/usr/bin/env python3
"""兼容层：实现已迁至 common/open_ai_creation.py 与 common/open_api_client.py。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from open_ai_creation import (  # noqa: F401
    FAILED_STATUSES,
    RUNNING_STATUSES,
    SUCCESS_STATUSES,
    first_output_url,
    get_ai_creation_task,
    list_ai_creation_tasks,
)
from open_api_client import api_get, api_post

get_task = get_ai_creation_task
list_tasks = list_ai_creation_tasks

__all__ = [
    "api_get",
    "api_post",
    "FAILED_STATUSES",
    "RUNNING_STATUSES",
    "SUCCESS_STATUSES",
    "first_output_url",
    "get_task",
    "list_tasks",
]
