from __future__ import annotations

from dataclasses import dataclass
import os

from canvas_claw.errors import CanvasClawError


DEFAULT_TIMEOUT_SECONDS = 60.0
DEFAULT_POLL_INTERVAL_SECONDS = 5.0


@dataclass(frozen=True)
class RuntimeConfig:
    base_url: str
    token: str
    site_id: int
    timeout: float = DEFAULT_TIMEOUT_SECONDS
    poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS


def load_runtime_config() -> RuntimeConfig:
    base_url = os.environ.get("AI_VIDEO_AGENT_BASE_URL", "").strip()
    token = os.environ.get("AI_VIDEO_AGENT_TOKEN", "").strip()
    raw_site_id = os.environ.get("AI_VIDEO_AGENT_SITE_ID", "").strip()
    raw_timeout = os.environ.get("AI_VIDEO_AGENT_TIMEOUT", "").strip()
    raw_poll_interval = os.environ.get("AI_VIDEO_AGENT_POLL_INTERVAL", "").strip()

    if not base_url:
        raise CanvasClawError("Missing AI_VIDEO_AGENT_BASE_URL")
    if not token:
        raise CanvasClawError("Missing AI_VIDEO_AGENT_TOKEN")
    if not raw_site_id:
        raise CanvasClawError("Missing AI_VIDEO_AGENT_SITE_ID")

    try:
        site_id = int(raw_site_id)
    except ValueError as exc:
        raise CanvasClawError("AI_VIDEO_AGENT_SITE_ID must be an integer") from exc

    timeout = DEFAULT_TIMEOUT_SECONDS
    if raw_timeout:
        try:
            timeout = float(raw_timeout)
        except ValueError as exc:
            raise CanvasClawError("AI_VIDEO_AGENT_TIMEOUT must be a number") from exc

    poll_interval = DEFAULT_POLL_INTERVAL_SECONDS
    if raw_poll_interval:
        try:
            poll_interval = float(raw_poll_interval)
        except ValueError as exc:
            raise CanvasClawError("AI_VIDEO_AGENT_POLL_INTERVAL must be a number") from exc

    return RuntimeConfig(
        base_url=base_url.rstrip("/"),
        token=token,
        site_id=site_id,
        timeout=timeout,
        poll_interval=poll_interval,
    )
