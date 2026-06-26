"""AI 创作（ai_creation）Open API 封装。"""
from __future__ import annotations

from typing import Any

from open_api_client import api_get, api_post

RUNNING_STATUSES = {"Queued", "Ready", "Generating"}
SUCCESS_STATUSES = {"Success"}
FAILED_STATUSES = {"Error", "Fail"}


def get_ai_creation_task(token: str, unique_id: str) -> Any:
    return api_get(token, "/open/v1/ai_creation/task", {"unique_id": unique_id}, query_doseq=True)


def list_ai_creation_tasks(
    token: str,
    creation_type: Any,
    page: int = 1,
    page_size: int = 50,
    unique_ids: list | None = None,
    is_success: bool | None = None,
) -> Any:
    payload: dict[str, Any] = {
        "unique_ids": unique_ids or [],
        "type": creation_type,
        "page": page,
        "page_size": page_size,
    }
    if is_success is not None:
        payload["is_success"] = bool(is_success)
    return api_post(token, "/open/v1/ai_creation/task/page", payload)


def first_output_url(data: Any) -> str | None:
    urls = (data or {}).get("output_url") or []
    if isinstance(urls, list) and urls:
        return urls[0]
    return None
