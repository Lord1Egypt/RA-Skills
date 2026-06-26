"""蝉镜 Open API：带 access_token 的 JSON GET/POST，与 base.API_BASE 环境约定一致。"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Any

from exceptions import SkillHTTPError

API_BASE = os.environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")


def api_get(
    token: str,
    path: str,
    query: dict[str, Any] | None = None,
    *,
    query_doseq: bool = False,
    timeout: int = 30,
) -> Any:
    query = query or {}
    suffix = ""
    if query:
        suffix = "?" + urllib.parse.urlencode(query, doseq=query_doseq)
    url = f"{API_BASE}{path}{suffix}"
    req = urllib.request.Request(url, headers={"access_token": token}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        raise SkillHTTPError(str(exc)) from exc
    if body.get("code") != 0:
        raise SkillHTTPError(str(body.get("msg", body)))
    return body.get("data")


def api_post(token: str, path: str, payload: dict[str, Any], *, timeout: int = 30) -> Any:
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"access_token": token, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        raise SkillHTTPError(str(exc)) from exc
    if body.get("code") != 0:
        raise SkillHTTPError(str(body.get("msg", body)))
    return body.get("data")
