from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from typing import Any
from zoneinfo import ZoneInfo

from .http import FeishuHttpClient


UNSET = object()


def parse_due_input(
    date_value: str | None,
    datetime_value: str | None,
    clear: bool,
    timezone_name: str = "Asia/Shanghai",
) -> dict[str, Any] | None:
    if clear:
        return None
    if date_value and datetime_value:
        raise ValueError("use either date or datetime, not both")
    if not date_value and not datetime_value:
        return None
    if date_value:
        parsed = datetime.strptime(date_value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return {"timestamp": str(int(parsed.timestamp() * 1000)), "is_all_day": True}
    tz = ZoneInfo(timezone_name)
    parsed = datetime.strptime(datetime_value, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    return {"timestamp": str(int(parsed.timestamp() * 1000)), "is_all_day": False}


def parse_member_args(values: list[str] | None) -> list[str]:
    if not values:
        return []
    return [value.strip() for value in values if value and value.strip()]


def build_update_payload(
    summary: str | object = UNSET,
    description: str | object = UNSET,
    start: dict[str, Any] | None | object = UNSET,
    due: dict[str, Any] | None | object = UNSET,
    clear_fields: list[str] | None = None,
) -> dict[str, Any]:
    task: dict[str, Any] = {}
    update_fields: list[str] = []
    if summary is not UNSET and summary is not None:
        task["summary"] = summary
        update_fields.append("summary")
    if description is not UNSET and description is not None:
        task["description"] = description
        update_fields.append("description")
    if start is not UNSET and start is not None:
        task["start"] = start
        update_fields.append("start")
    if due is not UNSET and due is not None:
        task["due"] = due
        update_fields.append("due")
    for field in clear_fields or []:
        task[field] = None
        update_fields.append(field)
    return {"task": task, "update_fields": update_fields}


def build_member_operation_payload(open_ids: list[str], role: str = "assignee") -> dict[str, Any]:
    return {
        "members": [{"id": open_id, "type": "user", "role": role} for open_id in open_ids],
    }


def build_origin(platform_name: str, title: str | None, url: str | None) -> dict[str, Any]:
    payload: dict[str, Any] = {"platform_i18n_name": {"zh_cn": platform_name}}
    if title or url:
        payload["href"] = {}
        if title:
            payload["href"]["title"] = title
        if url:
            payload["href"]["url"] = url
    return payload


def add_default_member_to_created_task(service: Any, created: dict[str, Any], default_member_open_id: str) -> dict[str, Any]:
    if not default_member_open_id:
        return created
    task_guid = created.get("task", {}).get("guid", "")
    if not task_guid:
        return created
    enriched = dict(created)
    try:
        service.add_members(task_guid, [default_member_open_id])
        enriched["default_member"] = {
            "open_id": default_member_open_id,
            "status": "added",
        }
    except Exception as exc:
        warnings = list(enriched.get("warnings", []))
        warnings.append(
            {
                "code": "default_member_add_failed",
                "message": f"task created, but adding default member failed: {exc}",
            }
        )
        enriched["warnings"] = warnings
        enriched["default_member"] = {
            "open_id": default_member_open_id,
            "status": "failed",
        }
    return enriched


@dataclass
class TaskService:
    client: FeishuHttpClient
    platform_name: str = "OpenClaw"

    def get_task(self, task_guid: str) -> dict[str, Any]:
        return self.client.request("GET", f"/task/v2/tasks/{task_guid}")

    def list_tasks(self, page_size: int = 20, page_token: str | None = None) -> dict[str, Any]:
        return self.client.request("GET", "/task/v2/tasks", params={"page_size": page_size, "page_token": page_token})

    def create_task(
        self,
        summary: str,
        description: str | None = None,
        start: dict[str, Any] | None = None,
        due: dict[str, Any] | None = None,
        origin_title: str | None = None,
        origin_url: str | None = None,
        raw_body: str | None = None,
    ) -> dict[str, Any]:
        if raw_body:
            payload = json.loads(raw_body)
        else:
            payload: dict[str, Any] = {"summary": summary}
            if description:
                payload["description"] = description
            if start is not None:
                payload["start"] = start
            if due is not None:
                payload["due"] = due
            if origin_title or origin_url:
                payload["origin"] = build_origin(self.platform_name, origin_title, origin_url)
        return self.client.request("POST", "/task/v2/tasks", body=payload)

    def update_task(
        self,
        task_guid: str,
        summary: str | object = UNSET,
        description: str | object = UNSET,
        start: dict[str, Any] | None | object = UNSET,
        due: dict[str, Any] | None | object = UNSET,
        clear_fields: list[str] | None = None,
        raw_body: str | None = None,
    ) -> dict[str, Any]:
        payload = json.loads(raw_body) if raw_body else build_update_payload(summary, description, start, due, clear_fields=clear_fields)
        return self.client.request("PATCH", f"/task/v2/tasks/{task_guid}", body=payload)

    def delete_task(self, task_guid: str) -> dict[str, Any]:
        return self.client.request("DELETE", f"/task/v2/tasks/{task_guid}")

    def complete_task(self, task_guid: str, timestamp_ms: str | None = None) -> dict[str, Any]:
        timestamp = timestamp_ms or str(int(datetime.now(timezone.utc).timestamp() * 1000))
        payload = {"task": {"completed_at": timestamp}, "update_fields": ["completed_at"]}
        return self.client.request("PATCH", f"/task/v2/tasks/{task_guid}", body=payload)

    def reopen_task(self, task_guid: str) -> dict[str, Any]:
        payload = {"task": {"completed_at": "0"}, "update_fields": ["completed_at"]}
        return self.client.request("PATCH", f"/task/v2/tasks/{task_guid}", body=payload)

    def add_members(self, task_guid: str, open_ids: list[str], raw_body: str | None = None) -> dict[str, Any]:
        payload = json.loads(raw_body) if raw_body else build_member_operation_payload(open_ids)
        return self.client.request(
            "POST",
            f"/task/v2/tasks/{task_guid}/add_members",
            params={"user_id_type": "open_id"},
            body=payload,
        )

    def remove_members(self, task_guid: str, open_ids: list[str], raw_body: str | None = None) -> dict[str, Any]:
        payload = json.loads(raw_body) if raw_body else build_member_operation_payload(open_ids)
        return self.client.request(
            "POST",
            f"/task/v2/tasks/{task_guid}/remove_members",
            params={"user_id_type": "open_id"},
            body=payload,
        )
