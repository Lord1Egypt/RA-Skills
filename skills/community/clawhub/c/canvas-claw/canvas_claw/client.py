from __future__ import annotations

import json
from typing import Any
from urllib import parse, request
from urllib.error import HTTPError, URLError

from canvas_claw.config import RuntimeConfig
from canvas_claw.errors import CanvasClawError


class CanvasClawClient:
    def __init__(self, config: RuntimeConfig):
        self.config = config

    def _build_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "token": self.config.token,
            "site-id": str(self.config.site_id),
        }
        if extra:
            headers.update(extra)
        return headers

    def request_json(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.config.base_url}{path}"
        if query:
            url = f"{url}?{parse.urlencode(query)}"

        req = request.Request(
            url,
            data=data,
            headers=self._build_headers(headers),
            method=method,
        )
        try:
            with request.urlopen(req, timeout=self.config.timeout) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise CanvasClawError(f"HTTP {exc.code} for {path}: {detail}") from exc
        except URLError as exc:
            raise CanvasClawError(f"Request failed for {path}: {exc.reason}") from exc

        if not raw.strip():
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise CanvasClawError(f"Invalid JSON response from {path}") from exc

    def login(self, username: str, password: str) -> dict[str, Any]:
        payload = json.dumps(
            {
                "username": username,
                "password": password,
            }
        ).encode("utf-8")
        return self.request_json(
            "POST",
            "/api/login",
            data=payload,
            headers={"Content-Type": "application/json"},
        )

    def list_models(self) -> dict[str, Any]:
        return self.request_json("GET", "/api/models")

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request_json(
            "POST",
            "/api/tasks",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

    def get_task(self, task_id: str) -> dict[str, Any]:
        return self.request_json("GET", f"/api/tasks/{task_id}")

    def materialize_binary(
        self,
        *,
        media_type: str,
        filename: str | None,
        content: bytes,
        content_type: str,
    ) -> dict[str, Any]:
        query = {"media_type": media_type}
        if filename:
            query["filename"] = filename
        return self.request_json(
            "POST",
            "/api/assets/materialize-binary",
            query=query,
            data=content,
            headers={"Content-Type": content_type},
        )
