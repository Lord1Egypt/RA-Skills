#!/usr/bin/env python3
"""Cross-platform Sparki Business API client utilities."""

from __future__ import annotations

import json
import mimetypes
import os
import time
import uuid
from dataclasses import dataclass
from http.client import HTTPConnection, HTTPSConnection, HTTPResponse
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


DEFAULT_API_URL = "https://business-agent-api.sparki.io"
DEFAULT_OUTPUT_DIR = "~/Movies/sparki"
DEFAULT_CONFIG_FILE = Path.home() / ".openclaw" / "config" / "sparki.env"
SUPPORT_EMAIL = "support@sparksview.com"
CHUNK_SIZE = 1024 * 1024
DEFAULT_USER_AGENT = "curl/8.7.1"


class SparkiError(RuntimeError):
    """Raised when the Sparki API workflow cannot continue."""


@dataclass(slots=True)
class SparkiConfig:
    api_key: str
    api_url: str
    output_dir: Path
    config_file: Path
    asset_poll_interval: int = 2
    asset_poll_max_interval: int = 30
    project_poll_interval: int = 10
    project_poll_max_interval: int = 60
    asset_timeout: int = 300
    project_timeout: int = 3600

    @property
    def business_api_base(self) -> str:
        return f"{self.api_url.rstrip('/')}/api/v1/business"


def load_env_file(config_file: Path) -> dict[str, str]:
    if not config_file.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in config_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip("'").strip('"')
        values[key.strip()] = os.path.expanduser(value)
    return values


def get_env_value(name: str, file_values: dict[str, str], default: str = "") -> str:
    return os.environ.get(name) or file_values.get(name) or default


def load_config(config_file: str | None = None) -> SparkiConfig:
    file_path = Path(config_file).expanduser() if config_file else DEFAULT_CONFIG_FILE
    file_values = load_env_file(file_path)

    api_key = get_env_value("SPARKI_API_KEY", file_values)
    if not api_key:
        raise SparkiError(
            f"SPARKI_API_KEY is not set. Configure it in the environment or {file_path}."
        )

    api_url = get_env_value("SPARKI_API_URL", file_values, DEFAULT_API_URL).rstrip("/")
    output_dir_raw = get_env_value("SPARKI_OUTPUT_DIR", file_values, DEFAULT_OUTPUT_DIR)
    output_dir = Path(output_dir_raw).expanduser()

    return SparkiConfig(
        api_key=api_key,
        api_url=api_url,
        output_dir=output_dir,
        config_file=file_path,
        asset_poll_interval=int(get_env_value("ASSET_POLL_INTERVAL", file_values, "2")),
        asset_poll_max_interval=int(
            get_env_value("ASSET_POLL_MAX_INTERVAL", file_values, "30")
        ),
        project_poll_interval=int(get_env_value("PROJECT_POLL_INTERVAL", file_values, "10")),
        project_poll_max_interval=int(
            get_env_value("PROJECT_POLL_MAX_INTERVAL", file_values, "60")
        ),
        asset_timeout=int(get_env_value("ASSET_TIMEOUT", file_values, "300")),
        project_timeout=int(get_env_value("PROJECT_TIMEOUT", file_values, "3600")),
    )


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def calculate_backoff_seconds(attempt: int, initial_interval: int, max_interval: int) -> int:
    delay = initial_interval
    for _ in range(max(attempt, 0)):
        delay = min(delay * 2, max_interval)
    return delay


def parse_json_response(body: str) -> dict[str, Any]:
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise SparkiError(f"Received invalid JSON response: {body}") from exc


def api_request(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = b""
    headers = {
        "X-API-Key": api_key,
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    parsed = urlparse(url)
    path = parsed.path
    if parsed.query:
        path = f"{path}?{parsed.query}"

    connection_class = HTTPSConnection if parsed.scheme == "https" else HTTPConnection
    connection = connection_class(parsed.hostname, parsed.port, timeout=60)
    try:
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        response_body = response.read().decode("utf-8", errors="replace")
    except OSError as exc:
        raise SparkiError(f"Unable to reach API: {exc}") from exc
    finally:
        connection.close()

    if response.status >= 400:
        raise SparkiError(f"HTTP {response.status} from API: {response_body}")

    data = parse_json_response(response_body)
    validate_api_response(data)
    return data


def validate_api_response(data: dict[str, Any]) -> None:
    code = str(data.get("code", "unknown"))
    if code not in {"0", "200"}:
        raise SparkiError(f"API request failed (code={code}): {data.get('message', 'unknown')}")


def upload_asset(config: SparkiConfig, video_path: Path) -> str:
    url = f"{config.business_api_base}/assets/upload"
    parsed = urlparse(url)
    connection_class = HTTPSConnection if parsed.scheme == "https" else HTTPConnection
    connection = connection_class(parsed.hostname, parsed.port, timeout=300)

    boundary = f"----SparkiBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(video_path.name)[0] or "application/octet-stream"
    preamble = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files"; filename="{video_path.name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8")
    epilogue = f"\r\n--{boundary}--\r\n".encode("utf-8")
    content_length = len(preamble) + video_path.stat().st_size + len(epilogue)

    try:
        connection.putrequest("POST", parsed.path)
        connection.putheader("X-API-Key", config.api_key)
        connection.putheader("User-Agent", DEFAULT_USER_AGENT)
        connection.putheader("Accept", "application/json")
        connection.putheader("Content-Type", f"multipart/form-data; boundary={boundary}")
        connection.putheader("Content-Length", str(content_length))
        connection.endheaders()
        connection.send(preamble)

        with video_path.open("rb") as video_file:
            while True:
                chunk = video_file.read(CHUNK_SIZE)
                if not chunk:
                    break
                connection.send(chunk)

        connection.send(epilogue)
        response: HTTPResponse = connection.getresponse()
        response_body = response.read().decode("utf-8")
    except OSError as exc:
        raise SparkiError(f"Upload failed: {exc}") from exc
    finally:
        connection.close()

    data = parse_json_response(response_body)
    validate_api_response(data)
    uploads = ((data.get("data") or {}).get("uploads") or [])
    object_key = ((uploads[0] if uploads else {}) or {}).get("object_key", "")
    if not object_key:
        raise SparkiError(f"Upload succeeded without object_key: {response_body}")
    return object_key


def create_render_project(
    config: SparkiConfig,
    object_key: str,
    tips_arg: str,
    user_prompt: str,
    aspect_ratio: str,
    duration: str,
) -> str:
    payload: dict[str, Any] = {
        "object_keys": [object_key],
        "aspect_ratio": aspect_ratio or "9:16",
    }

    tips = parse_tips(tips_arg)
    if tips:
        payload["tips"] = tips
    if user_prompt:
        payload["user_prompt"] = user_prompt
    if duration:
        payload["duration"] = int(duration)

    data = api_request(
        "POST",
        f"{config.business_api_base}/projects/render",
        config.api_key,
        payload,
    )
    project_id = ((data.get("data") or {}).get("project_id")) or ""
    if not project_id:
        raise SparkiError(f"Project creation succeeded without project_id: {data}")
    return project_id


def get_asset_status(config: SparkiConfig, object_key: str) -> tuple[str, dict[str, Any]]:
    data = api_request(
        "POST",
        f"{config.business_api_base}/assets/batch",
        config.api_key,
        {"object_keys": [object_key]},
    )
    assets = ((data.get("data") or {}).get("assets") or [])
    first = assets[0] if assets else {}
    return str(first.get("status", "unknown")), data


def get_project_status(config: SparkiConfig, project_id: str) -> tuple[str, dict[str, Any]]:
    data = api_request(
        "POST",
        f"{config.business_api_base}/projects/batch",
        config.api_key,
        {"project_ids": [project_id]},
    )
    projects = ((data.get("data") or {}).get("projects") or [])
    first = projects[0] if projects else {}
    return str(first.get("status", "unknown")), data


def wait_for_terminal_status(
    fetch_status: Any,
    timeout_seconds: int,
    initial_interval: int,
    max_interval: int,
    label: str,
) -> dict[str, Any]:
    start = time.time()
    attempt = 0
    while True:
        status, response = fetch_status()
        print(f"  {label} status: {status}")
        if status == "completed":
            return response
        if status in {"failed", "error"}:
            raise SparkiError(f"{label} processing failed: {json.dumps(response, ensure_ascii=False)}")
        if time.time() - start >= timeout_seconds:
            raise SparkiError(f"{label} processing timed out after {timeout_seconds}s")

        delay = calculate_backoff_seconds(attempt, initial_interval, max_interval)
        print(f"  Retrying {label.lower()} status in {delay}s...")
        time.sleep(delay)
        attempt += 1


def parse_tips(raw: str) -> list[Any]:
    values: list[Any] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        values.append(int(item) if item.isdigit() else item)
    return values


def validate_video_path(video_path: Path) -> Path:
    if not video_path.is_file():
        raise SparkiError(f"Video file not found: {video_path}")
    if video_path.suffix.lower() != ".mp4":
        raise SparkiError("Only MP4 is supported by this Business API workflow.")
    max_bytes = 3 * 1024 * 1024 * 1024
    file_size = video_path.stat().st_size
    if file_size > max_bytes:
        raise SparkiError(
            f"Video file is too large ({file_size // 1024 // 1024} MB). Maximum is 3 GB."
        )
    return video_path


def validate_inputs(tips_arg: str, user_prompt: str, duration: str) -> None:
    if not tips_arg and len(user_prompt) < 10:
        raise SparkiError("When tips is empty, user_prompt must be at least 10 characters.")
    if duration:
        int(duration)


def get_result_url(project_response: dict[str, Any]) -> str:
    projects = ((project_response.get("data") or {}).get("projects") or [])
    project = projects[0] if projects else {}
    output_videos = project.get("output_videos") or []
    first = output_videos[0] if output_videos else {}
    result_url = first.get("url") or project.get("result_url") or ""
    if not result_url:
        raise SparkiError(f"Missing output video URL in project response: {project_response}")
    return str(result_url)


def download_file(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    path = parsed.path
    if parsed.query:
        path = f"{path}?{parsed.query}"

    connection_class = HTTPSConnection if parsed.scheme == "https" else HTTPConnection
    connection = connection_class(parsed.hostname, parsed.port, timeout=300)
    try:
        connection.request("GET", path, headers={"User-Agent": DEFAULT_USER_AGENT})
        response = connection.getresponse()
        if response.status >= 400:
            body = response.read().decode("utf-8", errors="replace")
            raise SparkiError(f"Download failed with HTTP {response.status}: {body}")

        with destination.open("wb") as output_file:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                output_file.write(chunk)
    except OSError as exc:
        raise SparkiError(f"Unable to download result: {exc}") from exc
    finally:
        connection.close()

    if not destination.is_file():
        raise SparkiError("Download failed: output file was not created.")
    return destination


def verify_api_connectivity(config: SparkiConfig) -> None:
    api_request(
        "GET",
        f"{config.business_api_base}/assets?page=1&page_size=1",
        config.api_key,
    )


def format_file_size(path: Path) -> str:
    size = path.stat().st_size
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    value = float(size)
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    return f"{value:.1f}{units[unit_index]}"
