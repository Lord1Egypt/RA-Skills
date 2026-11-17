#!/usr/bin/env python3
"""Small, dependency-free client for the Reveyes review task API."""

from __future__ import annotations

import getpass
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable


DEFAULT_BASE_URL = "https://server.reveyes.cn/api/open"
ERROR_MESSAGES = {
    1001: "API Key 无效或已禁用",
    1002: "积分不足",
    1003: "请求参数错误",
    1004: "资源不存在",
    1005: "无权访问",
}
TERMINAL_FAILURE_STATUSES = {"failed", "error", "cancelled", "canceled", "expired"}


class ReveyesError(RuntimeError):
    """Raised for HTTP, API, task, and response-shape failures."""

    def __init__(
        self,
        message: str,
        *,
        api_code: int | None = None,
        http_status: int | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.api_code = api_code
        self.http_status = http_status
        self.payload = payload


def _read_env_file(path: Path) -> dict[str, str]:
    """Read KEY=VALUE pairs without evaluating shell syntax."""
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def load_api_key(*, env_file: str | None = None, prompt: bool = False) -> str:
    """Load the API key from the process, an explicit env file, or a hidden prompt."""
    key = os.environ.get("REVEYES_API_KEY", "").strip()
    if not key and env_file:
        path = Path(env_file).expanduser().resolve()
        if not path.is_file():
            raise ReveyesError(f"环境文件不存在: {path}")
        key = _read_env_file(path).get("REVEYES_API_KEY", "").strip()
    if not key and prompt:
        key = getpass.getpass("Reveyes API key (hidden): ").strip()
    if not key:
        raise ReveyesError(
            "未配置 REVEYES_API_KEY。请设置环境变量、传入 --env-file，"
            "或使用 --prompt-api-key。"
        )
    return key


class ReveyesClient:
    """HTTP client with retries, polling, and result pagination."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        retries: int = 3,
        user_agent: str = "analyze-amazon-reviews/1.0",
    ) -> None:
        self._api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = max(1, retries)
        self.user_agent = user_agent

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = self.base_url + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {
            "X-API-Key": self._api_key,
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if body is not None:
            headers["Content-Type"] = "application/json"

        last_error: BaseException | None = None
        for attempt in range(1, self.retries + 1):
            request = urllib.request.Request(url, data=body, method=method, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = response.read().decode("utf-8", "replace")
                    try:
                        result = json.loads(raw)
                    except json.JSONDecodeError as exc:
                        raise ReveyesError(
                            "接口返回了非 JSON 内容",
                            http_status=response.status,
                            payload=raw[:1000],
                        ) from exc
                    return self._validate_response(result, http_status=response.status)
            except urllib.error.HTTPError as exc:
                raw = exc.read().decode("utf-8", "replace")
                try:
                    result = json.loads(raw)
                except json.JSONDecodeError:
                    result = {"raw": raw[:1000]}
                if exc.code >= 500 and attempt < self.retries:
                    last_error = exc
                    time.sleep(min(2 ** (attempt - 1), 5))
                    continue
                raise self._to_error(result, http_status=exc.code) from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(min(2 ** (attempt - 1), 5))
                    continue
                raise ReveyesError(f"网络请求失败: {exc}") from exc

        raise ReveyesError(f"网络请求失败: {last_error}")

    @staticmethod
    def _to_error(result: Any, *, http_status: int | None = None) -> ReveyesError:
        if isinstance(result, dict):
            api_code = result.get("code")
            message = result.get("message") or ERROR_MESSAGES.get(api_code) or "接口调用失败"
            if api_code in ERROR_MESSAGES and ERROR_MESSAGES[api_code] not in str(message):
                message = f"{message}（{ERROR_MESSAGES[api_code]}）"
            return ReveyesError(
                str(message),
                api_code=api_code if isinstance(api_code, int) else None,
                http_status=http_status,
                payload=result,
            )
        return ReveyesError("接口调用失败", http_status=http_status, payload=result)

    @classmethod
    def _validate_response(cls, result: Any, *, http_status: int) -> dict[str, Any]:
        if not isinstance(result, dict):
            raise ReveyesError("接口顶层响应不是 JSON 对象", http_status=http_status, payload=result)
        if result.get("code") != 0:
            raise cls._to_error(result, http_status=http_status)
        data = result.get("data")
        if data is not None and not isinstance(data, dict):
            raise ReveyesError("响应 data 字段不是对象", http_status=http_status, payload=result)
        return result

    def submit(self, request_payload: dict[str, Any]) -> dict[str, Any]:
        result = self._request("POST", "/v1/reviews/fetch", payload=request_payload)
        task_id = result.get("data", {}).get("task_id")
        if not task_id:
            raise ReveyesError("提交成功但响应中缺少 data.task_id", payload=result)
        return result

    def result_page(self, task_id: str, *, page: int = 1, page_size: int = 100) -> dict[str, Any]:
        encoded = urllib.parse.quote(str(task_id), safe="")
        return self._request(
            "GET",
            f"/v1/reviews/result/{encoded}",
            query={"page": page, "page_size": page_size},
        )

    def collect_result(
        self,
        task_id: str,
        *,
        poll_interval: float = 5.0,
        max_wait: float = 1800.0,
        page_size: int = 100,
        on_poll: Callable[[str, int], None] | None = None,
    ) -> dict[str, Any]:
        """Poll until done, then retrieve every result page and merge review rows."""
        started = time.monotonic()
        attempt = 0
        first_page: dict[str, Any]
        while True:
            attempt += 1
            first_page = self.result_page(task_id, page=1, page_size=page_size)
            status = str(first_page.get("data", {}).get("status", "")).lower()
            if on_poll:
                on_poll(status or "unknown", attempt)
            if status == "done":
                break
            if status in TERMINAL_FAILURE_STATUSES:
                raise ReveyesError(f"任务 {task_id} 以状态 {status} 结束", payload=first_page)
            if time.monotonic() - started >= max_wait:
                raise ReveyesError(f"等待任务 {task_id} 超时（{max_wait:g} 秒）", payload=first_page)
            time.sleep(max(1.0, poll_interval))

        data = first_page.get("data", {})
        reviews_block = data.get("reviews")
        if not isinstance(reviews_block, dict):
            raise ReveyesError("完成响应缺少 data.reviews 对象", payload=first_page)
        rows = reviews_block.get("data")
        if not isinstance(rows, list):
            raise ReveyesError("完成响应缺少 data.reviews.data 数组", payload=first_page)
        total = reviews_block.get("total", len(rows))
        try:
            total = int(total)
        except (TypeError, ValueError):
            total = len(rows)

        merged_rows = list(rows)
        page = 2
        while len(merged_rows) < total:
            response = self.result_page(task_id, page=page, page_size=page_size)
            page_rows = response.get("data", {}).get("reviews", {}).get("data")
            if not isinstance(page_rows, list):
                raise ReveyesError(f"结果第 {page} 页缺少评论数组", payload=response)
            if not page_rows:
                raise ReveyesError(
                    f"结果声明共有 {total} 条，但第 {page} 页为空；已取得 {len(merged_rows)} 条",
                    payload=response,
                )
            merged_rows.extend(page_rows)
            page += 1

        merged_rows = merged_rows[:total]
        reviews_block["page"] = 1
        reviews_block["page_size"] = page_size
        reviews_block["data"] = merged_rows
        reviews_block["retrieved"] = len(merged_rows)
        return first_page

