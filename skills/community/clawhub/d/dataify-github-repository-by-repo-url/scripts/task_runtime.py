"""Shared completion runtime for Dataify Builder submission scripts."""

import json
import os
import re

from wait_for_task import DEFAULT_MAX_INTERVAL, wait_for_task


def extract_task_id(payload):
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except ValueError:
            candidate = payload.strip()
            if re.fullmatch(r"[A-Za-z0-9_-]{8,128}", candidate):
                return candidate
            return None
    if isinstance(payload, dict):
        for key in ("task_id", "taskId"):
            value = payload.get(key)
            if value:
                return str(value)
        data = payload.get("data")
        if data is not payload:
            value = extract_task_id(data)
            if value:
                return value
    return None


def complete_task(task_id, api_key, wait_timeout=600, request_timeout=60):
    task_id = str(task_id or "").strip()
    if not task_id:
        raise RuntimeError("Builder response did not contain a task_id; cannot wait for a final result.")
    api_key = str(api_key or "").strip()
    if api_key.lower().startswith("bearer "):
        api_key = api_key[7:].strip()
    try:
        result = wait_for_task(
            task_id,
            api_key,
            float(wait_timeout),
            float(request_timeout),
            DEFAULT_MAX_INTERVAL,
            True,
        )
    except TimeoutError as exc:
        waiter = os.path.abspath(os.path.join(os.path.dirname(__file__), "wait_for_task.py"))
        command = 'python3 "{}" --task-id "{}" --timeout {}'.format(
            waiter, task_id, int(float(wait_timeout))
        )
        raise RuntimeError("{}\nResume: {}".format(exc, command)) from None
    except KeyboardInterrupt:
        waiter = os.path.abspath(os.path.join(os.path.dirname(__file__), "wait_for_task.py"))
        command = 'python3 "{}" --task-id "{}" --timeout {}'.format(
            waiter, task_id, int(float(wait_timeout))
        )
        raise RuntimeError(
            "Monitoring interrupted. Do not resubmit the task.\nResume: {}".format(command)
        ) from None
    return {
        "ok": True,
        "task_id": task_id,
        "status": "succeeded",
        "data": result,
    }
