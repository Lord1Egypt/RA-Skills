"""文生数字人（aigc photo/motion/lora）Open API 封装。"""
from __future__ import annotations

from typing import Any

from open_api_client import api_get, api_post

PHOTO_RUNNING = {"Ready", "Generating", "Queued"}
PHOTO_SUCCESS = {"Success"}
PHOTO_FAILED = {"Error", "Fail"}

MOTION_RUNNING = {"Ready", "Generating", "Queued"}
MOTION_SUCCESS = {"Success"}
MOTION_FAILED = {"Error", "Fail"}

LORA_RUNNING = {"Queued", "Published", "Generating"}
LORA_SUCCESS = {"Success"}
LORA_FAILED = {"Fail"}


def get_photo_task(token: str, unique_id: str) -> Any:
    return api_get(token, "/open/v1/aigc/photo/task", {"unique_id": unique_id})


def list_photo_tasks(token: str, page: int = 1, page_size: int = 10) -> Any:
    return api_get(token, "/open/v1/aigc/photo/task/page", {"page": page, "page_size": page_size})


def get_motion_task(token: str, unique_id: str) -> Any:
    return api_get(token, "/open/v1/aigc/motion/task", {"unique_id": unique_id})


def get_lora_task(token: str, lora_id: str) -> Any:
    return api_get(token, "/open/v1/aigc/lora/task", {"lora_id": lora_id})


def first_output_url(data: Any) -> str | None:
    urls = (data or {}).get("output_url") or []
    if isinstance(urls, list) and urls:
        return urls[0]
    return None
