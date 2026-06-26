#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import random
import re
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
import base64
from dataclasses import dataclass
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any


DEFAULT_METADATA = {
    "isMobile": None,
    "imagePrompts": 0,
    "imageReferences": 0,
    "characterReferences": 0,
    "depthReferences": 0,
    "lightboxOpen": None,
}

IMAGE_URL_RE = re.compile(r"https://[^\s\"']+\.(?:png|jpg|jpeg|webp)(?:\?[^\s\"']*)?$", re.IGNORECASE)


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got: {value}") from exc


def load_dotenv(dotenv_path: str | Path | None = None) -> None:
    path = Path(dotenv_path or ".env")
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


@dataclass
class MJConfig:
    base_url: str
    submit_path: str
    user_state_path: str
    recent_jobs_url: str
    status_url_template: str | None
    cookie: str
    channel_id: str
    user_id: str | None
    mode: str
    private: bool
    timeout_seconds: float
    poll_interval_seconds: float
    min_submit_interval_seconds: float
    max_submits_per_hour: int
    max_submits_per_day: int
    state_dir: str
    referer_path: str
    origin: str
    csrf_protection: str
    user_agent: str
    metrics_token: str | None
    extra_headers: dict[str, str]

    @property
    def submit_url(self) -> str:
        return self.base_url.rstrip("/") + "/" + self.submit_path.lstrip("/")

    @property
    def user_state_url(self) -> str:
        return self.base_url.rstrip("/") + "/" + self.user_state_path.lstrip("/")


def load_config(dotenv_path: str | Path | None = None) -> MJConfig:
    load_dotenv(dotenv_path)

    extra_headers_raw = os.getenv("MJ_EXTRA_HEADERS_JSON", "").strip()
    extra_headers: dict[str, str] = {}
    if extra_headers_raw:
        try:
            parsed = json.loads(extra_headers_raw)
        except json.JSONDecodeError as exc:
            raise ValueError("MJ_EXTRA_HEADERS_JSON must be valid JSON") from exc
        if not isinstance(parsed, dict):
            raise ValueError("MJ_EXTRA_HEADERS_JSON must be a JSON object")
        extra_headers = {str(key): str(value) for key, value in parsed.items()}

    return MJConfig(
        base_url=os.getenv("MJ_BASE_URL", "https://alpha.midjourney.com"),
        submit_path=os.getenv("MJ_SUBMIT_PATH", "/api/submit-jobs"),
        user_state_path=os.getenv("MJ_USER_STATE_PATH", "/api/user-mutable-state"),
        recent_jobs_url=os.getenv("MJ_RECENT_JOBS_URL", "https://www.midjourney.com/api/app/recent-jobs/"),
        status_url_template=os.getenv("MJ_STATUS_URL_TEMPLATE") or None,
        cookie=os.getenv("MJ_COOKIE", ""),
        channel_id=os.getenv("MJ_CHANNEL_ID", ""),
        user_id=os.getenv("MJ_USER_ID") or None,
        mode=os.getenv("MJ_MODE", "fast"),
        private=env_bool("MJ_PRIVATE", True),
        timeout_seconds=env_float("MJ_TIMEOUT_SECONDS", 60.0),
        poll_interval_seconds=env_float("MJ_POLL_INTERVAL_SECONDS", 5.0),
        min_submit_interval_seconds=env_float("MJ_MIN_SUBMIT_INTERVAL_SECONDS", 3.0),
        max_submits_per_hour=int(os.getenv("MJ_MAX_SUBMITS_PER_HOUR", "0")),
        max_submits_per_day=int(os.getenv("MJ_MAX_SUBMITS_PER_DAY", "0")),
        state_dir=os.getenv("MJ_STATE_DIR", "state"),
        referer_path=os.getenv("MJ_REFERER_PATH", "/explore?tab=hot"),
        origin=os.getenv("MJ_ORIGIN", "https://alpha.midjourney.com"),
        csrf_protection=os.getenv("MJ_CSRF_PROTECTION", "1"),
        user_agent=os.getenv(
            "MJ_USER_AGENT",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        ),
        metrics_token=os.getenv("MJ_METRICS_TOKEN") or None,
        extra_headers=extra_headers,
    )


def enrich_config_from_cookie(config: MJConfig) -> MJConfig:
    claims = extract_auth_claims_from_cookie(config.cookie)
    if claims:
        midjourney_id = claims.get("midjourney_id")
        if not config.user_id and midjourney_id:
            config.user_id = str(midjourney_id)
        if not config.channel_id and midjourney_id:
            config.channel_id = f"singleplayer_{midjourney_id}"
    return config


def require_config(
    config: MJConfig,
    need_status: bool = False,
    need_cookie: bool = True,
    need_channel_id: bool = True,
) -> None:
    missing: list[str] = []
    if need_cookie and not config.cookie:
        missing.append("MJ_COOKIE")
    if need_channel_id and not config.channel_id:
        missing.append("MJ_CHANNEL_ID")
    if need_status and not config.status_url_template:
        missing.append("MJ_STATUS_URL_TEMPLATE")

    if missing:
        raise SystemExit(f"Missing required config: {', '.join(missing)}")


def build_traceparent() -> str:
    trace_id = f"{random.getrandbits(128):032x}"
    parent_id = f"{random.getrandbits(64):016x}"
    return f"00-{trace_id}-{parent_id}-01"


def build_headers(config: MJConfig) -> dict[str, str]:
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "cookie": config.cookie,
        "origin": config.origin,
        "referer": config.origin.rstrip("/") + config.referer_path,
        "user-agent": config.user_agent,
        "x-csrf-protection": config.csrf_protection,
        "x-mj-traceparent": build_traceparent(),
    }
    if config.metrics_token:
        headers["x-metrics-token"] = config.metrics_token
    headers.update(config.extra_headers)
    return headers


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout_seconds: float) -> Any:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url=url, data=body, headers=headers, method="POST")
    return _open_json(request, timeout_seconds)


def get_json(url: str, headers: dict[str, str], timeout_seconds: float) -> Any:
    request = urllib.request.Request(url=url, headers=headers, method="GET")
    return _open_json(request, timeout_seconds)


def _open_json(request: urllib.request.Request, timeout_seconds: float) -> Any:
    try:
        raw = _open_text(request, timeout_seconds)
        if not raw.strip():
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"<pre[^>]*>(.*?)</pre>", raw, re.IGNORECASE | re.DOTALL)
            if match:
                return json.loads(match.group(1))
            raise
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {request.full_url}: {body}") from exc
    except (urllib.error.URLError, ssl.SSLError) as exc:
        raise RuntimeError(f"Request failed for {request.full_url}: {exc}") from exc


def _open_text(request: urllib.request.Request, timeout_seconds: float) -> str:
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError:
        raise
    except (urllib.error.URLError, ssl.SSLError) as exc:
        if not _is_tls_protocol_error(exc):
            raise
        return _curl_request_text(request, timeout_seconds)


def _is_tls_protocol_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "tlsv1 alert protocol version" in message or "wrong version number" in message


def _curl_request_text(request: urllib.request.Request, timeout_seconds: float) -> str:
    return _curl_request_bytes(request, timeout_seconds).decode("utf-8")


def _curl_request_bytes(request: urllib.request.Request, timeout_seconds: float) -> bytes:
    command = [
        "curl",
        "-sS",
        "-L",
        "--compressed",
        "--max-time",
        str(int(max(1, timeout_seconds))),
        "-X",
        request.get_method(),
        request.full_url,
    ]
    for key, value in request.header_items():
        command.extend(["-H", f"{key}: {value}"])

    data = request.data
    if data:
        command.extend(["--data-binary", "@-"])

    completed = subprocess.run(
        command,
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"curl request failed for {request.full_url}: {stderr}")
    return completed.stdout


def normalize_prompt(prompt: str, *, default_version: str = "8", add_raw: bool = True) -> str:
    cleaned = " ".join(prompt.strip().split())
    if not cleaned:
        raise ValueError("Prompt must not be empty")

    if "--v" not in cleaned and "--version" not in cleaned:
        cleaned = f"{cleaned} --v {default_version}"

    if add_raw and "--raw" not in cleaned:
        cleaned = f"{cleaned} --raw"

    return cleaned


def append_negative_terms(prompt: str, negative_terms: str | None) -> str:
    if not negative_terms or not negative_terms.strip():
        return " ".join(prompt.strip().split())
    cleaned_prompt = " ".join(prompt.strip().split())
    cleaned_negative = " ".join(negative_terms.strip().split())
    if not cleaned_negative:
        return cleaned_prompt
    if "--no" in cleaned_prompt:
        return cleaned_prompt
    return f"{cleaned_prompt} --no {cleaned_negative}".strip()


def apply_preset(prompt: str, preset_suffix: str) -> str:
    cleaned_prompt = " ".join(prompt.strip().split())
    cleaned_suffix = " ".join(preset_suffix.strip().split())
    if not cleaned_suffix:
        return cleaned_prompt
    if cleaned_prompt.endswith(cleaned_suffix):
        return cleaned_prompt
    return f"{cleaned_prompt} {cleaned_suffix}".strip()


def resolve_named_suffix(path: str | Path, name: str | None, *, label: str) -> str | None:
    if not name:
        return None
    data = load_json(path, {})
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid {label} file: {path}")
    item = data.get(name)
    if not isinstance(item, dict):
        raise SystemExit(f"{label.title()} not found: {name}")
    suffix = item.get("suffix")
    if not isinstance(suffix, str):
        raise SystemExit(f"{label.title()} {name} does not define a valid suffix")
    return " ".join(suffix.strip().split())


def build_imagine_payload(
    prompt: str,
    *,
    channel_id: str,
    mode: str,
    private: bool,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "f": {
            "mode": mode,
            "private": private,
        },
        "channelId": channel_id,
        "metadata": metadata or DEFAULT_METADATA,
        "t": "imagine",
        "prompt": prompt,
    }


def submit_imagine(
    config: MJConfig,
    prompt: str,
    *,
    mode: str | None = None,
    private: bool | None = None,
    channel_id: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    payload = build_imagine_payload(
        prompt,
        channel_id=channel_id or config.channel_id,
        mode=mode or config.mode,
        private=config.private if private is None else private,
    )

    if dry_run:
        return {
            "dry_run": True,
            "submit_url": config.submit_url,
            "payload": payload,
            "headers_preview": redact_headers(build_headers(config)),
        }

    response = post_json(
        config.submit_url,
        payload,
        headers=build_headers(config),
        timeout_seconds=config.timeout_seconds,
    )
    return {
        "dry_run": False,
        "submit_url": config.submit_url,
        "payload": payload,
        "response": response,
        "job_ids": extract_job_ids(response),
    }


def resolve_status_url(status_url_template: str | None, job_id: str) -> str | None:
    if not status_url_template:
        return None
    return status_url_template.format(job_id=job_id)


def get_user_state(config: MJConfig) -> dict[str, Any]:
    return get_json(
        config.user_state_url,
        headers=build_headers(config),
        timeout_seconds=config.timeout_seconds,
    )


def request_recent_jobs(
    config: MJConfig,
    *,
    user_id: str | None = None,
    page: int = 1,
    amount: int = 50,
    order_by: str = "new",
    job_status: str | None = None,
    job_type: str | None = None,
    ) -> Any:
    resolved_user_id = user_id or config.user_id
    if not resolved_user_id:
        raise RuntimeError("MJ_USER_ID is not configured and could not be inferred from the auth cookie")

    params = {
        "userId": resolved_user_id,
        "page": str(page),
        "amount": str(amount),
        "orderBy": order_by,
    }
    if job_status:
        params["jobStatus"] = job_status
    if job_type:
        params["jobType"] = job_type

    url = f"{config.recent_jobs_url}?{urllib.parse.urlencode(params)}"
    return get_json(
        url,
        headers=build_headers(config),
        timeout_seconds=config.timeout_seconds,
    )


def find_job_by_id(data: Any, job_id: str) -> dict[str, Any] | None:
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and str(item.get("id", "")) == job_id:
                return item
    elif isinstance(data, dict):
        if str(data.get("id", "")) == job_id:
            return data
        for value in data.values():
            found = find_job_by_id(value, job_id)
            if found:
                return found
    return None


def wait_for_recent_job(
    config: MJConfig,
    job_id: str,
    *,
    page: int = 1,
    amount: int = 25,
    attempts: int = 40,
    interval_seconds: float | None = None,
    job_status: str = "completed",
) -> dict[str, Any]:
    interval = config.poll_interval_seconds if interval_seconds is None else interval_seconds
    history: list[dict[str, Any]] = []

    for attempt in range(1, max(1, attempts) + 1):
        response = request_recent_jobs(
            config,
            page=page,
            amount=amount,
            job_status=job_status,
        )
        found = find_job_by_id(response, job_id)
        history.append(
            {
                "attempt": attempt,
                "timestamp": int(time.time()),
                "match_found": found is not None,
            }
        )
        if found:
            return {
                "job_id": job_id,
                "attempts": attempt,
                "done": True,
                "history": history,
                "job": found,
                "result_urls": list(found.get("image_paths") or []),
            }
        if attempt < attempts:
            time.sleep(interval)

    return {
        "job_id": job_id,
        "attempts": attempts,
        "done": False,
        "history": history,
        "job": None,
        "result_urls": [],
    }


def poll_job(
    config: MJConfig,
    job_id: str,
    *,
    attempts: int = 60,
    interval_seconds: float | None = None,
    once: bool = False,
) -> dict[str, Any]:
    status_url = resolve_status_url(config.status_url_template, job_id)
    if not status_url:
        raise RuntimeError("MJ_STATUS_URL_TEMPLATE is not configured")

    interval = config.poll_interval_seconds if interval_seconds is None else interval_seconds
    headers = build_headers(config)
    history: list[dict[str, Any]] = []

    for attempt in range(1, max(1, attempts) + 1):
        data = get_json(status_url, headers=headers, timeout_seconds=config.timeout_seconds)
        snapshot = {
            "attempt": attempt,
            "timestamp": int(time.time()),
            "data": data,
        }
        history.append(snapshot)

        if once or is_terminal_job_response(data):
            return {
                "job_id": job_id,
                "status_url": status_url,
                "attempts": attempt,
                "done": True,
                "history": history,
                "result_urls": extract_result_urls(data),
            }

        if attempt < attempts:
            time.sleep(interval)

    return {
        "job_id": job_id,
        "status_url": status_url,
        "attempts": attempts,
        "done": False,
        "history": history,
        "result_urls": extract_result_urls(history[-1]["data"]) if history else [],
    }


def is_terminal_job_response(data: Any) -> bool:
    if not isinstance(data, (dict, list)):
        return True

    result_urls = extract_result_urls(data)
    if result_urls:
        return True

    terminal_values = {"complete", "completed", "done", "finished", "failed", "cancelled", "canceled", "error"}
    for value in iter_scalar_values(data):
        lowered = str(value).strip().lower()
        if lowered in terminal_values:
            return True

    progress = find_progress_value(data)
    if progress is not None and progress >= 100:
        return True

    return False


def find_progress_value(data: Any) -> float | None:
    if isinstance(data, dict):
        for key, value in data.items():
            if str(key).lower() in {"progress", "percent", "percentage"}:
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return None
            nested = find_progress_value(value)
            if nested is not None:
                return nested
    elif isinstance(data, list):
        for item in data:
            nested = find_progress_value(item)
            if nested is not None:
                return nested
    return None


def iter_scalar_values(data: Any) -> list[Any]:
    values: list[Any] = []
    if isinstance(data, dict):
        for value in data.values():
            values.extend(iter_scalar_values(value))
    elif isinstance(data, list):
        for item in data:
            values.extend(iter_scalar_values(item))
    else:
        values.append(data)
    return values


def extract_job_ids(data: Any) -> list[str]:
    job_ids: list[str] = []
    walk_and_collect(data, lambda value: isinstance(value, str) and looks_like_job_id(value), job_ids)
    return dedupe(job_ids)


def extract_result_urls(data: Any) -> list[str]:
    urls: list[str] = []
    walk_and_collect(data, lambda value: isinstance(value, str) and IMAGE_URL_RE.match(value) is not None, urls)
    return dedupe(urls)


def fetch_binary(url: str, headers: dict[str, str], timeout_seconds: float) -> tuple[bytes, str | None]:
    request = urllib.request.Request(url=url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return response.read(), response.headers.get_content_type()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {request.full_url}: {body}") from exc
    except (urllib.error.URLError, ssl.SSLError) as exc:
        if _is_tls_protocol_error(exc):
            return _curl_request_bytes(request, timeout_seconds), None
        raise RuntimeError(f"Request failed for {request.full_url}: {exc}") from exc


def infer_extension_from_url_or_type(url: str, content_type: str | None = None) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix:
        return suffix
    if content_type == "image/png":
        return ".png"
    if content_type == "image/jpeg":
        return ".jpg"
    if content_type == "image/webp":
        return ".webp"
    return ".bin"


def safe_slug(value: str, fallback: str = "image") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-_.")
    return cleaned[:80] or fallback


def convert_image_bytes_to_png(data: bytes) -> dict[str, Any]:
    from PIL import Image

    with Image.open(BytesIO(data)) as image:
        width, height = image.size
        converted = BytesIO()
        image.save(converted, format="PNG")
        return {
            "bytes": converted.getvalue(),
            "mime_type": "image/png",
            "width": width,
            "height": height,
        }


def download_image(
    config: MJConfig,
    image_url: str,
    output_dir: str | Path,
    *,
    filename_stem: str,
    convert_to: str = "original",
) -> dict[str, Any]:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    if convert_to.lower() == "png":
        from mj_browser import browser_convert_image_url, browser_fetch_binary_url

        converted: dict[str, Any] | None = None
        last_error: Exception | None = None
        for attempt in range(1, 4):
            try:
                converted = browser_convert_image_url(
                    image_url,
                    output_format="png",
                    page_url="https://alpha.midjourney.com/imagine",
                    timeout_seconds=max(config.timeout_seconds, 60.0),
                )
                break
            except Exception as exc:
                last_error = exc
                try:
                    fetched = browser_fetch_binary_url(
                        image_url,
                        page_url="https://alpha.midjourney.com/imagine",
                        timeout_seconds=max(config.timeout_seconds, 60.0),
                    )
                    converted = convert_image_bytes_to_png(fetched["bytes"])
                    break
                except Exception as fetch_exc:
                    last_error = fetch_exc
                    if attempt < 3:
                        time.sleep(float(attempt))
        if converted is None:
            raise last_error or RuntimeError(f"Failed to download image as PNG: {image_url}")
        output_path = path / f"{safe_slug(filename_stem)}.png"
        output_path.write_bytes(converted["bytes"])
        return {
            "url": image_url,
            "content_type": converted.get("mime_type"),
            "size_bytes": len(converted["bytes"]),
            "path": str(output_path),
            "converted_to": "png",
            "width": converted.get("width"),
            "height": converted.get("height"),
        }

    data, content_type = fetch_binary(
        image_url,
        headers=build_headers(config),
        timeout_seconds=config.timeout_seconds,
    )
    extension = infer_extension_from_url_or_type(image_url, content_type)
    output_path = path / f"{safe_slug(filename_stem)}{extension}"
    output_path.write_bytes(data)
    return {
        "url": image_url,
        "content_type": content_type,
        "size_bytes": len(data),
        "path": str(output_path),
        "converted_to": "original",
    }


def summarize_job_images(job: dict[str, Any]) -> dict[str, Any]:
    image_paths = list(job.get("image_paths") or [])
    batch_size = None
    for key in ("batch_size",):
        if key in job:
            batch_size = job.get(key)
    if batch_size is None and isinstance(job.get("meta"), dict):
        batch_size = job["meta"].get("batch_size")
    if batch_size is None:
        batch_size = 4 if image_paths else None

    return {
        "job_id": job.get("id"),
        "prompt": job.get("prompt") or job.get("full_command"),
        "job_type": job.get("job_type"),
        "image_count": len(image_paths),
        "batch_size": batch_size,
        "image_paths": image_paths,
        "enqueue_time": job.get("enqueue_time"),
    }


def looks_like_job_id(value: str) -> bool:
    return re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        value,
        re.IGNORECASE,
    ) is not None


def walk_and_collect(data: Any, predicate: Any, sink: list[str]) -> None:
    if isinstance(data, dict):
        for value in data.values():
            walk_and_collect(value, predicate, sink)
        return
    if isinstance(data, list):
        for item in data:
            walk_and_collect(item, predicate, sink)
        return
    if predicate(data):
        sink.append(str(data))


def dedupe(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    redacted = dict(headers)
    for key in list(redacted):
        lowered = key.lower()
        if lowered == "cookie" or "token" in lowered or "authorization" in lowered or lowered.startswith("x-auth"):
            redacted[key] = "<redacted>"
    return redacted


def save_json(path: str | Path, data: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_json(data: Any) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def load_json(path: str | Path, default: Any) -> Any:
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def state_dir(config: MJConfig) -> Path:
    path = Path(config.state_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def usage_log_path(config: MJConfig) -> Path:
    return state_dir(config) / "usage-log.json"


def load_usage_log(config: MJConfig) -> list[dict[str, Any]]:
    data = load_json(usage_log_path(config), [])
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def save_usage_log(config: MJConfig, entries: list[dict[str, Any]]) -> None:
    save_json(usage_log_path(config), entries)


def enforce_safe_limits(config: MJConfig, *, now_ts: float | None = None) -> dict[str, Any]:
    now = now_ts or time.time()
    entries = load_usage_log(config)
    one_hour_ago = now - 3600
    one_day_ago = now - 86400

    recent_hour = [entry for entry in entries if float(entry.get("timestamp", 0)) >= one_hour_ago]
    recent_day = [entry for entry in entries if float(entry.get("timestamp", 0)) >= one_day_ago]
    last_submit = max((float(entry.get("timestamp", 0)) for entry in entries), default=0.0)
    seconds_since_last = now - last_submit if last_submit else None

    if seconds_since_last is not None and seconds_since_last < config.min_submit_interval_seconds:
        wait_for = round(config.min_submit_interval_seconds - seconds_since_last, 1)
        raise RuntimeError(
            f"Safe limit blocked this submit: wait at least {wait_for} more seconds "
            f"before sending the next Midjourney request."
        )

    if config.max_submits_per_hour > 0 and len(recent_hour) >= config.max_submits_per_hour:
        raise RuntimeError(
            f"Safe limit blocked this submit: hourly cap reached "
            f"({len(recent_hour)}/{config.max_submits_per_hour})."
        )

    if config.max_submits_per_day > 0 and len(recent_day) >= config.max_submits_per_day:
        raise RuntimeError(
            f"Safe limit blocked this submit: daily cap reached "
            f"({len(recent_day)}/{config.max_submits_per_day})."
        )

    return {
        "last_submit_at": int(last_submit) if last_submit else None,
        "submits_last_hour": len(recent_hour),
        "submits_last_day": len(recent_day),
        "min_submit_interval_seconds": config.min_submit_interval_seconds,
        "max_submits_per_hour": config.max_submits_per_hour,
        "max_submits_per_day": config.max_submits_per_day,
    }


def record_submit(
    config: MJConfig,
    *,
    prompt: str,
    mode: str,
    private: bool,
    job_id: str | None,
    dry_run: bool,
    submit_url: str,
) -> dict[str, Any]:
    now = time.time()
    entry = {
        "timestamp": now,
        "iso_utc": datetime.fromtimestamp(now, tz=timezone.utc).isoformat(),
        "prompt": prompt,
        "mode": mode,
        "private": private,
        "job_id": job_id,
        "dry_run": dry_run,
        "submit_url": submit_url,
    }
    entries = load_usage_log(config)
    entries.append(entry)
    entries = [item for item in entries if float(item.get("timestamp", 0)) >= now - (7 * 86400)]
    save_usage_log(config, entries)
    return entry


def decode_jwt_without_verification(token: str) -> dict[str, Any] | None:
    parts = token.split(".")
    if len(parts) < 2:
        return None
    payload = parts[1]
    padding = "=" * (-len(payload) % 4)
    try:
        decoded = base64.urlsafe_b64decode(payload + padding)
        parsed = json.loads(decoded.decode("utf-8"))
    except Exception:
        return None
    if not isinstance(parsed, dict):
        return None
    return parsed


def extract_auth_claims_from_cookie(cookie_header: str) -> dict[str, Any] | None:
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        segment = part.strip()
        if not segment or "=" not in segment:
            continue
        key, value = segment.split("=", 1)
        if key.strip() == "__Host-Midjourney.AuthUserTokenV3_i":
            return decode_jwt_without_verification(value.strip())
    return None
