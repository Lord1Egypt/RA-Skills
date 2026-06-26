#!/usr/bin/env python3
"""Shared helpers for cocoloop-skill-factory CLI utilities."""

from __future__ import annotations

import json
import os
import platform
import shlex
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_print(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def load_json_value(value: str | None) -> Any:
    if value is None:
        return None

    candidate = Path(value)
    if candidate.exists():
        return json.loads(candidate.read_text(encoding="utf-8"))

    return json.loads(value)


def parse_json_or_text(value: str | None) -> tuple[Any | None, str]:
    if value is None:
        return None, "empty"

    try:
        return load_json_value(value), "json"
    except Exception:
        return value, "text"


def shell_split(command_template: str, **values: str) -> list[str]:
    formatted_values = {
        key: shlex.quote(value)
        for key, value in values.items()
    }
    if formatted_values:
        command = command_template.format(**formatted_values)
    else:
        command = command_template
    return shlex.split(command)


def run_command(args: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": completed.returncode == 0,
            "available": True,
            "command": args,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "available": False,
            "command": args,
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "available": True,
            "command": args,
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or f"timeout after {timeout}s",
        }


def command_exists(command: str) -> bool:
    if Path(command).exists():
        return True
    return shutil.which(command) is not None


def command_version(command: str, version_args: Iterable[str] | None = None) -> dict[str, Any]:
    version_args = list(version_args or ("--version", "-version"))
    if Path(command).exists():
        resolved = command
    else:
        resolved = shutil.which(command)
    if not resolved:
        return {"available": False, "path": None, "version": None}

    for version_arg in version_args:
        result = run_command([resolved, version_arg], timeout=10)
        version = (result["stdout"] or result["stderr"] or "").strip()
        if version:
            return {
                "available": True,
                "path": resolved,
                "version": version,
            }

    return {
        "available": True,
        "path": resolved,
        "version": None,
    }


def normalize_result_item(item: Any, source: str) -> dict[str, Any]:
    if isinstance(item, str):
        return {
            "source": source,
            "title": item.strip(),
            "summary": "",
            "url": "",
            "score": None,
            "tags": [],
            "raw": item,
        }

    if not isinstance(item, dict):
        return {
            "source": source,
            "title": "",
            "summary": "",
            "url": "",
            "score": None,
            "tags": [],
            "raw": item,
        }

    title = (
        item.get("title")
        or item.get("name")
        or item.get("label")
        or item.get("skill_name")
        or item.get("id")
        or ""
    )
    summary = (
        item.get("summary")
        or item.get("description")
        or item.get("brief")
        or item.get("subtitle")
        or item.get("snippet")
        or item.get("content")
        or item.get("body")
        or ""
    )
    url = (
        item.get("html_url")
        or item.get("url")
        or item.get("link")
        or item.get("href")
        or item.get("download_url")
        or ""
    )
    score = (
        item.get("stargazers_count")
        or item.get("score")
        or item.get("relevance")
        or item.get("rank")
        or item.get("recommend_index")
        or item.get("recommend_rate")
    )
    tags = item.get("tags") or item.get("labels") or item.get("topics") or []
    if isinstance(tags, str):
        tags = [tags]
    if not isinstance(tags, list):
        tags = []
    if item.get("security_level"):
        tags.append(f"security:{item['security_level']}")
    if item.get("source_credibility"):
        tags.append(f"credibility:{item['source_credibility']}")

    return {
        "source": item.get("source") or source,
        "title": title,
        "summary": summary,
        "url": url,
        "score": score,
        "tags": tags,
        "raw": item,
    }


def extract_items(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    for key in ("results", "items", "skills", "hits", "data", "entries", "matches"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            nested = extract_items(value)
            if nested:
                return nested

    return []


def normalize_search_payload(payload: Any, source: str) -> list[dict[str, Any]]:
    return [normalize_result_item(item, source) for item in extract_items(payload)]


def normalize_text_results(raw_text: str, source: str) -> list[dict[str, Any]]:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return [
        {
            "source": source,
            "title": line,
            "summary": "",
            "url": "",
            "score": None,
            "tags": [],
            "raw": line,
        }
        for line in lines
    ]


def safe_json_loads(value: str) -> Any | None:
    try:
        return json.loads(value)
    except Exception:
        return None


def default_platform_snapshot() -> dict[str, Any]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


def env_flag(name: str) -> bool:
    value = os.environ.get(name, "")
    return value.lower() in {"1", "true", "yes", "on"}
