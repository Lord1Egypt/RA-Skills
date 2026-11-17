"""IFFManager — ASR 服务调度"""

from __future__ import annotations

import logging
import subprocess
import time

import httpx

from .exceptions import ASRServiceError

log = logging.getLogger(__name__)


class IFFManager:
    """确保 ASR 服务运行中"""

    def __init__(
        self,
        service_name: str = "sensevoice-small",
        base_url: str = "http://localhost:8881",
        switch_timeout: int = 120,
        health_timeout: int = 120,
        health_interval: float = 3.0,
    ):
        self._service_name = service_name
        self._base_url = base_url.rstrip("/")
        self._switch_timeout = switch_timeout
        self._health_timeout = health_timeout
        self._health_interval = health_interval

    def ensure_running(self) -> str:
        """确保 ASR 服务运行中，返回 base_url"""
        if self._is_healthy():
            return self._base_url

        log.info("ASR service not healthy, switching via IFF: %s", self._service_name)
        result = subprocess.run(
            ["iff", "switch", self._service_name],
            capture_output=True,
            text=True,
            timeout=self._switch_timeout,
        )
        if result.returncode != 0:
            raise ASRServiceError(
                f"iff switch {self._service_name} failed: {result.stderr.strip() or result.stdout.strip()}"
            )

        if not self._wait_healthy():
            raise ASRServiceError(
                f"ASR service {self._service_name} didn't become healthy within {self._health_timeout}s"
            )
        return self._base_url

    def _is_healthy(self) -> bool:
        try:
            resp = httpx.get(f"{self._base_url}/health", timeout=3)
            return resp.status_code == 200
        except Exception:
            return False

    def _wait_healthy(self) -> bool:
        deadline = time.monotonic() + self._health_timeout
        while time.monotonic() < deadline:
            if self._is_healthy():
                return True
            time.sleep(self._health_interval)
        return False
