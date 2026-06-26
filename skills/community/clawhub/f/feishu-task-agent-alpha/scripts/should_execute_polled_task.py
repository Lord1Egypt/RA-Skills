#!/usr/bin/env python3
"""Decide whether a polled unfinished task should enter execution."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import sys
from typing import Any, Dict, List, Optional


APP_TASK_MIN_AGE_MS = 20 * 60 * 1000


class ResolveError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message


def _normalize_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ResolveError("invalid_string_field", "string field must be a string")
    value = value.strip()
    return value or None


def _normalize_members(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ResolveError("invalid_members", "members must be an array")
    normalized: List[Dict[str, Any]] = []
    for item in value:
        if isinstance(item, dict):
            normalized.append(item)
    return normalized


def _resolve_assignee_type(payload: Dict[str, Any]) -> Optional[str]:
    members = _normalize_members(payload.get("members"))
    for member in members:
        role = _normalize_string(member.get("role"))
        if role != "assignee":
            continue
        return _normalize_string(member.get("type"))
    return None


def _resolve_creator_type(payload: Dict[str, Any]) -> Optional[str]:
    creator = payload.get("creator")
    if not isinstance(creator, dict):
        return None
    return _normalize_string(creator.get("type"))


def _parse_timestamp_ms(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ResolveError("invalid_created_at", "created_at must be a timestamp or ISO8601 string")
    if isinstance(value, (int, float)):
        numeric = float(value)
        if numeric > 1_000_000_000_000:
            return int(numeric)
        if numeric > 1_000_000_000:
            return int(numeric * 1000)
        raise ResolveError("invalid_created_at", "created_at timestamp is too small")
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.isdigit():
            return _parse_timestamp_ms(int(text))
        iso_text = text.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(iso_text)
        except ValueError as exc:
            raise ResolveError("invalid_created_at", "created_at is not a valid timestamp") from exc
        if parsed.tzinfo is None:
            parsed = parsed.astimezone()
        return int(parsed.timestamp() * 1000)
    raise ResolveError("invalid_created_at", "created_at must be a timestamp or ISO8601 string")


def should_execute_polled_task(payload: Dict[str, Any], source: Optional[str] = None, now_ms: Optional[int] = None) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ResolveError("invalid_input", "input must be a JSON object")

    # 1. 判断任务是否带有 repeat_rule (即是否为循环任务)
    repeat_rule = payload.get("repeat_rule")
    is_repeat_task = isinstance(repeat_rule, str) and bool(repeat_rule.strip())

    # 2. 判断是否为子任务 (包含 parent_task_guid 且非空即视为子任务)
    parent_guid = payload.get("parent_task_guid")
    if isinstance(parent_guid, str) and parent_guid.strip():
        return {"ok": True, "should_execute": False, "skip_reason": "is_subtask", "is_repeat_task": is_repeat_task}

    if source == "get-agent-unfinished-tasks":
        # 如果来自 get-agent-unfinished-tasks，则不处理循环任务（除非创建人是用户）
        if is_repeat_task:
            if _resolve_creator_type(payload) != "user":
                return {"ok": True, "should_execute": False, "skip_reason": "non_user_repeat_task", "is_repeat_task": True}
            
            # 对于用户创建的循环任务，需要判断负责人是否是应用
            assignee_type = _resolve_assignee_type(payload)
            if assignee_type != "app":
                return {"ok": True, "should_execute": False, "skip_reason": "non_app_assignee_repeat_task", "is_repeat_task": True}

            # 进一步判断是否满足时间条件
            due = payload.get("due", {})
            if isinstance(due, dict):
                due_timestamp = _parse_timestamp_ms(due.get("timestamp"))
                is_all_day = due.get("is_all_day")
                if due_timestamp is not None:
                    current_ms = now_ms if now_ms is not None else int(datetime.now().astimezone().timestamp() * 1000)
                    if is_all_day:
                        # 全天任务：判断当前时间是否过了12:00 (即当天中午12点)
                        # 将 due_timestamp 转换为当天12:00的时间戳
                        dt = datetime.fromtimestamp(due_timestamp / 1000.0).astimezone()
                        due_noon_dt = dt.replace(hour=12, minute=0, second=0, microsecond=0)
                        if current_ms < due_noon_dt.timestamp() * 1000:
                            return {"ok": True, "should_execute": False, "skip_reason": "all_day_task_before_noon", "is_repeat_task": True}
                    else:
                        # 非全天任务：判断当前时间是否达到或超过截止时间
                        if current_ms < due_timestamp:
                            return {"ok": True, "should_execute": False, "skip_reason": "task_before_due_time", "is_repeat_task": True}

    else:
        # 如果来自其他定时任务（非 get-agent-unfinished-tasks），则强制要求是循环任务
        if not is_repeat_task:
            return {"ok": True, "should_execute": False, "skip_reason": "not_repeat_task", "is_repeat_task": False}

    assignee_type = _resolve_assignee_type(payload)
    if assignee_type is None:
        return {"ok": True, "should_execute": False, "skip_reason": "missing_assignee", "is_repeat_task": is_repeat_task}
    if assignee_type != "app":
        return {"ok": True, "should_execute": False, "skip_reason": "non_app_assignee", "is_repeat_task": is_repeat_task}

    creator_type = _resolve_creator_type(payload)
    if creator_type is None:
        return {"ok": True, "should_execute": False, "skip_reason": "missing_creator_type", "is_repeat_task": is_repeat_task}
    if creator_type == "user":
        return {"ok": True, "should_execute": True, "skip_reason": None, "is_repeat_task": is_repeat_task}
    if creator_type != "app":
        return {"ok": True, "should_execute": False, "skip_reason": "missing_creator_type", "is_repeat_task": is_repeat_task}

    created_at_ms = _parse_timestamp_ms(payload.get("created_at"))
    if created_at_ms is None:
        return {"ok": True, "should_execute": False, "skip_reason": "missing_created_at", "is_repeat_task": is_repeat_task}

    current_ms = now_ms if now_ms is not None else int(datetime.now().astimezone().timestamp() * 1000)
    if current_ms - created_at_ms > APP_TASK_MIN_AGE_MS:
        return {"ok": True, "should_execute": True, "skip_reason": None, "is_repeat_task": is_repeat_task}
    return {"ok": True, "should_execute": False, "skip_reason": "app_task_not_old_enough", "is_repeat_task": is_repeat_task}


def _load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    raw = args.input_json
    if raw is None:
        raw = sys.stdin.read()
    raw = (raw or "").strip()
    if not raw:
        raise ResolveError("empty_input", "input JSON is required via stdin or --input-json")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ResolveError("invalid_json", f"input is not valid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ResolveError("invalid_input", "input must be a JSON object")
    return payload


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Decide whether a polled unfinished task should execute")
    parser.add_argument("--input-json", help="Input JSON object. If omitted, reads from stdin.")
    parser.add_argument("--source", help="The source of the task, e.g. 'get-agent-unfinished-tasks' or 'cronjob'.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    try:
        payload = _load_payload(args)
        output = should_execute_polled_task(payload, source=args.source)
    except ResolveError as exc:
        error = {"ok": False, "error_code": exc.error_code, "message": exc.message}
        json.dump(error, sys.stdout, ensure_ascii=True, indent=2 if args.pretty else None)
        sys.stdout.write("\n")
        return 1

    json.dump(output, sys.stdout, ensure_ascii=True, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
