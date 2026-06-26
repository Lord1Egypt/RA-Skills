from __future__ import annotations

import logging
import random
import time
from pathlib import Path
from typing import Any

import requests

from .config import AppConfig


SEARCH_URL = "https://www.cninfo.com.cn/new/fulltextSearch/full"


class HttpClient:
    def __init__(self, config: AppConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": config.user_agent,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Referer": config.referer,
            }
        )
        self._last_request_monotonic = 0.0

    def search(
        self,
        keyword: str,
        page_num: int,
        *,
        sdate: str = "",
        edate: str = "",
    ) -> dict[str, Any]:
        params = {
            "searchkey": keyword,
            "sdate": sdate,
            "edate": edate,
            "isfulltext": "false",
            "sortName": "pubdate",
            "sortType": "desc",
            "pageNum": page_num,
            "pageSize": self.config.page_size,
            "type": ",".join(self.config.board_types),
        }
        return self._request_json(SEARCH_URL, params=params, action=f"search[{keyword}#{page_num}]")

    def download_file(self, url: str, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target_path.with_suffix(target_path.suffix + ".part")

        try:
            response = self._request(url, stream=True, action=f"download[{target_path.name}]")
            with response:
                response.raise_for_status()
                with temp_path.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 64):
                        if chunk:
                            handle.write(chunk)
            temp_path.replace(target_path)
        finally:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

    def _request_json(self, url: str, params: dict[str, Any], action: str) -> dict[str, Any]:
        response = self._request(url, params=params, action=action)
        with response:
            response.raise_for_status()
            return response.json()

    def _request(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        stream: bool = False,
        action: str,
    ) -> requests.Response:
        last_error: Exception | None = None
        for attempt in range(1, self.config.max_retries + 1):
            self._throttle()
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.config.timeout_seconds,
                    stream=stream,
                )
                if response.status_code in {429, 500, 502, 503, 504}:
                    raise requests.HTTPError(
                        f"retryable status {response.status_code}",
                        response=response,
                    )
                return response
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                if attempt >= self.config.max_retries:
                    break
                delay = self.config.retry_backoff_seconds * (2 ** (attempt - 1))
                delay += random.uniform(0, 0.5)
                self.logger.warning(
                    "%s failed on attempt %s/%s: %s; retrying in %.2fs",
                    action,
                    attempt,
                    self.config.max_retries,
                    exc,
                    delay,
                )
                time.sleep(delay)
        raise RuntimeError(f"{action} failed after {self.config.max_retries} attempts") from last_error

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_monotonic
        wait_seconds = self.config.sleep_seconds - elapsed
        if wait_seconds > 0:
            time.sleep(wait_seconds)
        self._last_request_monotonic = time.monotonic()
