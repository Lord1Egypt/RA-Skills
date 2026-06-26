# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import base64
import json
import logging
import mimetypes
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence
from uuid import uuid4

from volcenginesdkarkruntime import Ark

logger = logging.getLogger("doubao")


def log_params(event: str, **kwargs: Any) -> None:
    """Log an event with a provider prefix and JSON payload."""
    params_str = json.dumps(kwargs, ensure_ascii=False, default=str)
    logger.info("火山引擎 - %s | %s", event, params_str)

# Per-execution trace ID, generated on first import
_trace_id: str = ""


def generate_trace_id() -> str:
    """Generate a 32-char unique trace ID for the current execution."""
    return uuid4().hex


def get_trace_id() -> str:
    """Return the current trace ID, generating one if not yet set."""
    global _trace_id
    if not _trace_id:
        _trace_id = generate_trace_id()
    return _trace_id


class _TraceIdFilter(logging.Filter):
    """Inject trace_id into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_OUTPUT_DIR = OUTPUT_ROOT / "outputs" / "doubao"
LOG_DIR = OUTPUT_ROOT / "outputs" / "logs"


def setup_logging() -> None:
    """Configure doubao logger: daily date-stamped log files, no console output."""
    if logger.handlers:
        return
    trace_filter = _TraceIdFilter()
    log_fmt = "%(asctime)s [%(trace_id)s] %(levelname)s %(message)s"
    fmt = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")

    # Normal file handler (all levels)
    file_handler = logging.FileHandler(LOG_DIR / f"{today}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.addFilter(trace_filter)
    logger.addHandler(file_handler)

    # Error-only file handler
    error_handler = logging.FileHandler(LOG_DIR / f"{today}.error.log", encoding="utf-8")
    error_handler.setFormatter(fmt)
    error_handler.addFilter(trace_filter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    api_key = os.getenv("ARK_API_KEY")
    if api_key:
        return api_key
    raise OSError("未设置环境变量 ARK_API_KEY")


def create_client(api_key: str | None = None) -> Ark:
    return Ark(
        base_url=BASE_URL,
        api_key=api_key or load_api_key(),
    )


def ensure_output_dir(*parts: str) -> Path:
    target_dir = DEFAULT_OUTPUT_DIR.joinpath(*parts)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def default_output_path(*parts: str, suffix: str = ".png", name: str = "") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    stem = f"{name}_{timestamp}" if name else timestamp
    return ensure_output_dir(*parts) / f"{stem}{suffix}"


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------

IMAGE_MODEL_FALLBACKS = [
    "doubao-seedream-5-0-260128",
    "doubao-seedream-4-5-251128",
]

QUOTA_ERROR_KEYWORDS = (
    "quota",
    "insufficient",
    "credit",
    "balance",
    "额度",
    "余额",
    "欠费",
    "用量",
    "resource exhausted",
    "ratelimit",
    "rate limit",
    "setlimitexceeded",
    "429",
)


def resolve_image_source(image_source: str | Path) -> str:
    source = Path(image_source)
    if source.exists():
        mime_type, _ = mimetypes.guess_type(source.name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        encoded = base64.b64encode(source.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"

    if "://" in str(image_source):
        return str(image_source)

    raise FileNotFoundError(
        f"图片路径不存在，也不是有效的 URL: {image_source}"
    )


def build_model_candidates(
    preferred_model: str,
    fallback_models: Sequence[str] = IMAGE_MODEL_FALLBACKS,
) -> list[str]:
    candidates = [preferred_model]
    for model in fallback_models:
        if model not in candidates:
            candidates.append(model)
    return candidates


def is_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return any(keyword in message for keyword in QUOTA_ERROR_KEYWORDS)


def generate_image_with_fallback(
    client: Ark,
    *,
    model: str,
    fallback_models: Sequence[str] = IMAGE_MODEL_FALLBACKS,
    **kwargs: Any,
) -> tuple[Any, str]:
    candidates = build_model_candidates(model, fallback_models)

    for index, candidate in enumerate(candidates):
        try:
            response = client.images.generate(model=candidate, **kwargs)
            return response, candidate
        except Exception as exc:
            has_next = index + 1 < len(candidates)
            if not has_next or not is_quota_error(exc):
                raise

            next_model = candidates[index + 1]
            print(f"模型 {candidate} 额度不足，自动切换到 {next_model}")
            logger.warning("模型 %s 额度不足，自动切换到 %s", candidate, next_model)


def save_image_payload(image_data: Any, output_path: Path) -> Path:
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    b64_json = getattr(image_data, "b64_json", None)
    if b64_json:
        output_path.write_bytes(base64.b64decode(b64_json))
        return output_path

    url = getattr(image_data, "url", None)
    if url:
        with urllib.request.urlopen(url) as response:
            output_path.write_bytes(response.read())
        return output_path

    raise RuntimeError("接口返回中既没有 b64_json，也没有 url，无法保存图片。")


def save_image_results(
    data: Sequence[Any],
    base_output_path: Path,
) -> list[dict[str, Any]]:
    """Save all images from response data (group image support).
    Returns list of {local_path, size, error} dicts."""
    results: list[dict[str, Any]] = []
    for index, item in enumerate(data):
        # Check for error item
        error = getattr(item, "error", None)
        if error is not None:
            err_info = {
                "index": index,
                "error": {"code": getattr(error, "code", ""), "message": getattr(error, "message", "")},
            }
            results.append(err_info)
            continue

        size = getattr(item, "size", "")
        stem = base_output_path.stem
        suffix = base_output_path.suffix or ".png"
        # For group images, append index to filename
        if len(data) > 1:
            path = base_output_path.with_stem(f"{stem}_{index}")
        else:
            path = base_output_path

        saved = save_image_payload(item, path)
        results.append({
            "index": index,
            "local_path": str(saved),
            "size": str(size) if size else "",
        })
    return results


# ---------------------------------------------------------------------------
# Video helpers
# ---------------------------------------------------------------------------

VIDEO_MODEL_FALLBACKS: list[str] = []


def _to_dict(obj: Any) -> dict[str, Any]:
    """Normalize SDK response objects to plain dict."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return {"raw": str(obj)}


def create_video_task(
    client: Ark,
    *,
    model: str,
    content: list[dict[str, Any]],
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a video generation task via the Ark SDK."""
    params: dict[str, Any] = {"model": model, "content": content}
    params.update(kwargs)
    resp = client.content_generation.tasks.create(**params)
    return _to_dict(resp)


def query_video_task(
    client: Ark,
    task_id: str,
) -> dict[str, Any]:
    """Query the status of a video generation task."""
    resp = client.content_generation.tasks.get(task_id=task_id)
    return _to_dict(resp)


def wait_for_video_task(
    client: Ark,
    task_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 900,
) -> dict[str, Any]:
    """Poll a video task until succeeded, failed, expired, or cancelled."""
    deadline = __import__("time").monotonic() + timeout
    import time

    last_status: str | None = None
    while time.monotonic() < deadline:
        result = query_video_task(client, task_id)
        status = result.get("status", "")

        if status != last_status:
            print(f"视频任务状态: {status}")
            log_params("视频任务状态", status=status)
            last_status = status

        if status == "succeeded":
            return result
        if status == "failed":
            error = result.get("error", {})
            raise RuntimeError(
                f"视频任务失败: {json.dumps(error, ensure_ascii=False)}"
            )
        if status == "expired":
            raise TimeoutError(f"视频任务已过期，task_id={task_id}")
        if status == "cancelled":
            raise RuntimeError(f"视频任务已取消，task_id={task_id}")

        time.sleep(poll_interval)

    raise TimeoutError(f"视频任务超时，task_id={task_id}")


def extract_video_url(result: dict[str, Any]) -> str:
    """Extract the video URL from a succeeded task result."""
    content = result.get("content", {})
    if isinstance(content, dict):
        video_url = content.get("video_url", "")
    else:
        video_url = getattr(content, "video_url", "")

    video_url = str(video_url).strip()
    if not video_url:
        raise RuntimeError(
            f"视频结果中缺少 video_url: {json.dumps(result, ensure_ascii=False, default=str)}"
        )
    return video_url


def download_file(url: str, output_path: Path) -> Path:
    """Download a file from URL to local path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request) as response:
        output_path.write_bytes(response.read())
    return output_path


def list_video_tasks(
    client: Ark,
    *,
    page_num: int | None = None,
    page_size: int | None = None,
    status: str | None = None,
    task_ids: list[str] | None = None,
    model: str | None = None,
    service_tier: str | None = None,
) -> dict[str, Any]:
    """List video generation tasks with optional filters."""
    params: dict[str, Any] = {}
    if page_num is not None:
        params["page_num"] = page_num
    if page_size is not None:
        params["page_size"] = page_size
    if status is not None:
        params["filter.status"] = status
    if task_ids is not None:
        params["filter.task_ids"] = task_ids
    if model is not None:
        params["filter.model"] = model
    if service_tier is not None:
        params["filter.service_tier"] = service_tier
    resp = client.content_generation.tasks.list(**params)
    return _to_dict(resp)


def delete_video_task(
    client: Ark,
    task_id: str,
) -> None:
    """Cancel a queued task or delete a task record."""
    client.content_generation.tasks.delete(task_id=task_id)
