#!/usr/bin/env python3
"""
ArtClaw AI Creative Suite CLI — Agent-friendly REST API client.

Flow:  Submit Job → Poll Status → Return Result (JSON stdout)
API:   https://artclaw.com/api/v1
Auth:  X-API-KEY header (starts with vk_)

Requires:
  - pip install requests
  - ARTCLAW_API_KEY env var or config-init

All results output to stdout as JSON. Progress/diagnostics go to stderr.
"""

import argparse
import base64
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    import requests
except ImportError:
    print(json.dumps({
        "error": "requests package not installed",
        "install_command": "pip install requests",
    }), file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Section 1: Module-Level Constants
# ---------------------------------------------------------------------------

# Paths
STATE_DIR = Path(os.path.expanduser("~/.artclaw"))
CONFIG_FILE = STATE_DIR / "config.json"
LAST_JOB_FILE = STATE_DIR / "last_job.json"
HISTORY_DIR = STATE_DIR / "history"

# API
DEFAULT_BASE_URL = "https://artclaw.com/api/v1"
TOPUP_URL = "https://artclaw.com/settings"
GET_KEY_URL = "https://artclaw.com/settings"

# Self-update
GITHUB_REPO_URL = "https://github.com/ArtClaw1/artclaw-skill"
GITHUB_RAW_SCRIPT_URL = (
    "https://raw.githubusercontent.com/ArtClaw1/artclaw-skill/main/scripts/artclaw.py"
)
GITHUB_ARCHIVE_URL = (
    "https://github.com/ArtClaw1/artclaw-skill/archive/refs/heads/main.zip"
)

# Network
CONNECT_TIMEOUT = 15   # seconds — TCP handshake
READ_TIMEOUT = 60      # seconds — wait for response body
MAX_RETRIES = 2

# Polling profiles per job type
POLL_PROFILES: Dict[str, dict] = {
    "image":    {"interval": 5,  "timeout": 300,  "backoff": 1.5, "max_interval": 15},
    "video":    {"interval": 10, "timeout": 600,  "backoff": 1.5, "max_interval": 30},
    "workflow": {"interval": 30, "timeout": 1800, "backoff": 1.2, "max_interval": 60},
}

# Job type inference from subcommand
JOB_TYPE_MAP = {
    "generate-image": "image",
    "generate-video": "video",
    "generate-marketing-image": "image",
    "run-workflow": "workflow",
}

# Validation sets (module-level, not created per call)
VALID_ASPECT_RATIOS = frozenset({"16:9", "9:16", "1:1", "4:3", "21:9"})
VALID_RESOLUTIONS_IMAGE = frozenset({"1K", "2K", "4K"})
VALID_RESOLUTIONS_VIDEO = frozenset({"480p", "720p", "1080p"})
TERMINAL_STATUSES = frozenset({"success", "failed", "canceled", "expired"})
ALLOWED_URL_SCHEMES = ("http://", "https://")
ALLOWED_IMAGE_DATA_URI_PREFIX = "data:image/"

# Spawn
SPAWN_TIMEOUT_SECONDS = 2400  # 40 minutes


# ---------------------------------------------------------------------------
# Section 2: Exception Hierarchy
# ---------------------------------------------------------------------------

class ArtClawApiError(Exception):
    """Raised when an ArtClaw API call fails."""

    def __init__(self, message: str, *, status_code: int = 0,
                 code: str = "", detail: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.detail = detail

    def is_retryable(self) -> bool:
        if self.status_code >= 500:
            return True
        if self.status_code == 429:
            return True
        if self.code == "network_error":
            return True
        return False

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {"error": str(self)}
        if self.code:
            d["code"] = self.code
        if self.status_code:
            d["http_status"] = self.status_code
        if self.detail:
            d["detail"] = self.detail
        if self.status_code == 401:
            d["hint"] = f"API key invalid or missing. Get one at {GET_KEY_URL}"
        elif self.status_code == 402:
            d["hint"] = f"Insufficient credits. Top up at {TOPUP_URL}"
        elif self.status_code == 429:
            d["hint"] = "Rate limited (120 req/min). Wait a moment and retry."
        return d


class ArtClawPollTimeout(Exception):
    """Raised when polling exceeds the timeout for a job type."""

    def __init__(self, job_id: str, job_type: str, attempts: int,
                 elapsed: float, last_status: str = ""):
        msg = (f"Polling {job_type} job {job_id} timed out after "
               f"{attempts} attempts ({elapsed:.0f}s), last status: {last_status}")
        super().__init__(msg)
        self.job_id = job_id
        self.job_type = job_type
        self.attempts = attempts
        self.elapsed = elapsed
        self.last_status = last_status


class ArtClawPollFailed(Exception):
    """Raised when a polled job enters a terminal failure state."""

    def __init__(self, job_id: str, status: str, error_detail: Any = None):
        msg = f"Job {job_id} entered terminal failure: {status}"
        super().__init__(msg)
        self.job_id = job_id
        self.status = status
        self.error_detail = error_detail


# ---------------------------------------------------------------------------
# Section 3: Config / Credential Loading
# ---------------------------------------------------------------------------

def _file_to_base64(file_path: str) -> str:
    """Convert local image file to base64 data URI."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Reference file not found: {file_path}")

    # Determine MIME type from extension
    ext = path.suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif",
        ".webp": "image/webp", ".bmp": "image/bmp"
    }
    mime_type = mime_map.get(ext, "image/jpeg")

    # Read and encode
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    return f"data:{mime_type};base64,{encoded}"


def _ensure_dir():
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_history_dir():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def _load_raw_config() -> dict:
    """Load config from config.json. Warns on parse errors (does NOT swallow)."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            _log(f"WARNING: {CONFIG_FILE} has invalid JSON: {e}")
        except IOError as e:
            _log(f"WARNING: cannot read {CONFIG_FILE}: {e}")
    return {}


def _get_config() -> dict:
    """
    Resolve full config.

    Priority: env var ARTCLAW_API_KEY > config.json > defaults.
    """
    api_key = os.environ.get("ARTCLAW_API_KEY", "")
    base_url = os.environ.get("ARTCLAW_BASE_URL", "")

    file_cfg = {}
    if not api_key:
        file_cfg = _load_raw_config()
        api_key = file_cfg.get("apiKey", "")
    if not base_url:
        base_url = file_cfg.get("baseUrl", "") if file_cfg else ""

    return {
        "apiKey": api_key,
        "baseUrl": base_url or DEFAULT_BASE_URL,
    }


def _check_api_key(config: dict, *, allow_dry_run: bool = False):
    """Exit with setup instructions if API key is missing.

    If allow_dry_run=True and --dry-run is active, skip the check.
    """
    if allow_dry_run:
        return
    if not config.get("apiKey"):
        print(json.dumps({
            "error": "ArtClaw API key not configured",
            "setup_required": True,
            "step1": f"Visit {GET_KEY_URL} to get your API key (starts with vk_)",
            "step2": 'Run: artclaw.py config-init --api-key "vk_your_key"',
            "step3": "Or set env var: export ARTCLAW_API_KEY=vk_your_key",
        }, indent=2), file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Section 4: Low-Level HTTP — Unified _request_with_retry
# ---------------------------------------------------------------------------

def _log(msg: str):
    """Print progress info to stderr (never to stdout)."""
    print(f"[artclaw] {msg}", file=sys.stderr, flush=True)


def _parse_error_response(resp: requests.Response) -> ArtClawApiError:
    """Parse an error HTTP response into ArtClawApiError."""
    try:
        body = resp.json()
        return ArtClawApiError(
            message=body.get("detail", body.get("message", f"HTTP {resp.status_code}")),
            status_code=resp.status_code,
            code=str(body.get("code", "")),
            detail=body.get("details", body.get("data")),
        )
    except (ValueError, KeyError):
        return ArtClawApiError(
            message=f"HTTP {resp.status_code}: {resp.text[:500]}",
            status_code=resp.status_code,
        )


def _request_with_retry(
    method: str,
    url: str,
    *,
    api_key: str = "",
    json_body: Optional[dict] = None,
    params: Optional[dict] = None,
    max_retries: int = MAX_RETRIES,
    connect_timeout: int = CONNECT_TIMEOUT,
    read_timeout: int = READ_TIMEOUT,
    idempotency_key: Optional[str] = None,
    dry_run: bool = False,
) -> dict:
    """
    Unified HTTP request with exponential backoff retry.

    - Retries on 5xx, 429, and network errors
    - Does NOT retry other 4xx (client errors)
    - Returns parsed JSON response on 200
    """
    if dry_run:
        return {
            "__dry_run": True,
            "method": method,
            "url": url,
            "body": json_body,
            "params": params,
        }

    headers: Dict[str, str] = {"Accept": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    if json_body is not None:
        headers["Content-Type"] = "application/json"
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key

    last_err: Optional[ArtClawApiError] = None

    for attempt in range(max_retries + 1):
        try:
            resp = requests.request(
                method, url,
                headers=headers,
                json=json_body if json_body is not None else None,
                params=params,
                timeout=(connect_timeout, read_timeout),
            )
            if resp.status_code == 200:
                return resp.json()

            err = _parse_error_response(resp)
            # Don't retry client errors (except 429)
            if 400 <= resp.status_code < 500 and resp.status_code != 429:
                raise err
            last_err = err

        except ArtClawApiError:
            raise
        except requests.RequestException as e:
            last_err = ArtClawApiError(
                f"Network error: {e}", status_code=0, code="network_error",
            )

        if attempt < max_retries:
            wait = 2 ** attempt
            _log(f"Retry {attempt + 1}/{max_retries} in {wait}s...")
            time.sleep(wait)

    raise last_err or ArtClawApiError("Unknown error after retries")


# ---------------------------------------------------------------------------
# Section 5: Generic _poll_until
# ---------------------------------------------------------------------------

def _poll_until(
    config: dict,
    job_id: str,
    job_type: str,
    *,
    dry_run: bool = False,
) -> dict:
    """
    Generic job poller with type-aware intervals and timeouts.

    Uses POLL_PROFILES[job_type] for interval, timeout, backoff, max_interval.
    Returns the full job status dict when status == "success".
    Raises ArtClawPollTimeout or ArtClawPollFailed on failure/timeout.
    """
    if dry_run:
        return {"__dry_run": True, "job_id": job_id, "job_type": job_type,
                "action": "would_poll"}

    profile = POLL_PROFILES.get(job_type, POLL_PROFILES["image"])
    interval = profile["interval"]
    timeout = profile["timeout"]
    backoff = profile["backoff"]
    max_interval = profile["max_interval"]

    base_url = config["baseUrl"]
    api_key = config["apiKey"]
    start = time.time()
    attempt = 0
    last_status = ""

    while True:
        time.sleep(interval)
        attempt += 1
        elapsed = time.time() - start

        if elapsed > timeout:
            raise ArtClawPollTimeout(
                job_id, job_type, attempt, elapsed, last_status,
            )

        try:
            result = _request_with_retry(
                "GET", f"{base_url}/jobs/{job_id}",
                api_key=api_key,
            )
        except ArtClawApiError as e:
            if e.is_retryable():
                _log(f"Poll {job_type}: transient error attempt {attempt}: {e}")
                interval = min(interval * backoff, max_interval)
                continue
            # 404 early on can mean job not yet visible
            if e.status_code == 404 and attempt <= 5:
                _log(f"Poll {job_type}: job not found yet (404), retrying...")
                interval = min(interval * backoff, max_interval)
                continue
            raise

        status = result.get("status", "")
        last_status = status

        if attempt % 3 == 0 or status in TERMINAL_STATUSES:
            _log(f"Poll {job_type} [{job_id[:16]}]: attempt={attempt} "
                 f"status={status} elapsed={elapsed:.0f}s")

        if status == "success":
            return result

        if status in TERMINAL_STATUSES:
            error_detail = result.get("metadata", {}).get("error_detail")
            raise ArtClawPollFailed(job_id, status, error_detail)

        interval = min(interval * backoff, max_interval)


# ---------------------------------------------------------------------------
# Section 6: API Endpoint Functions
# ---------------------------------------------------------------------------

# --- Generation (async, returns job_id) ---

def api_generate_image(config: dict, prompt: str, *,
                       aspect_ratio: str = None, resolution: str = None,
                       reference_urls: List[str] = None, model: str = None,
                       callback_url: str = None,
                       idempotency_key: str = None,
                       dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"prompt": prompt}
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio
    if resolution:
        body["resolution"] = resolution
    if reference_urls:
        body["reference_urls"] = reference_urls
    if model:
        body["model"] = model
    if callback_url:
        body["callback_url"] = callback_url
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/generate/image",
        api_key=config["apiKey"], json_body=body,
        idempotency_key=idempotency_key, dry_run=dry_run,
    )


def api_generate_video(config: dict, prompt: str, *,
                       aspect_ratio: str = None, duration: int = None,
                       resolution: str = None,
                       reference_urls: List[str] = None, model: str = None,
                       callback_url: str = None,
                       idempotency_key: str = None,
                       dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"prompt": prompt}
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio
    if duration is not None:
        body["duration"] = duration
    if resolution:
        body["resolution"] = resolution
    if reference_urls:
        body["content_items"] = [{"role": "reference_image", "url": u} for u in reference_urls]
    if model:
        body["model"] = model
    if callback_url:
        body["callback_url"] = callback_url
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/generate/video",
        api_key=config["apiKey"], json_body=body,
        idempotency_key=idempotency_key, dry_run=dry_run,
    )


def api_generate_marketing_image(config: dict, prompt: str, *,
                                 size: str = None,
                                 callback_url: str = None,
                                 dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"prompt": prompt}
    if size:
        body["size"] = size
    if callback_url:
        body["callback_url"] = callback_url
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/generate/marketing-image",
        api_key=config["apiKey"], json_body=body, dry_run=dry_run,
    )


# --- Workflows ---

def api_list_workflows(config: dict, *, dry_run: bool = False) -> dict:
    # Trailing slash required! Without it: 307 redirect -> 502
    return _request_with_retry(
        "GET", f"{config['baseUrl']}/workflows/",
        api_key=config["apiKey"], dry_run=dry_run,
    )


def api_run_workflow(config: dict, workflow_id: str, inputs: dict, *,
                     timeout: int = None, callback_url: str = None,
                     dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"inputs": inputs}
    if timeout is not None:
        body["timeout"] = timeout
    if callback_url:
        body["callback_url"] = callback_url
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/workflows/{workflow_id}/run",
        api_key=config["apiKey"], json_body=body, dry_run=dry_run,
    )


# --- Analysis (sync, returns result directly) ---

def api_analyze_image(config: dict, reference_urls: List[str], *,
                      query: str = "", dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"image_urls": reference_urls}
    if query:
        body["query"] = query
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/analyze/image",
        api_key=config["apiKey"], json_body=body, dry_run=dry_run,
    )


def api_analyze_video(config: dict, reference_urls: List[str], *,
                      query: str = "", dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"video_url": reference_urls[0]}
    if query:
        body["query"] = query
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/analyze/video",
        api_key=config["apiKey"], json_body=body, dry_run=dry_run,
    )


def api_analyze_script(config: dict, reference_paths: List[str], *,
                       original_script: str = "",
                       node_to_replace: str = "",
                       dry_run: bool = False) -> dict:
    body: Dict[str, Any] = {"reference_paths": reference_paths}
    if original_script:
        body["original_script"] = original_script
    if node_to_replace:
        body["node_to_replace"] = node_to_replace
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/analyze/script",
        api_key=config["apiKey"], json_body=body, dry_run=dry_run,
    )


def api_analyze_characters(config: dict, text: str, *,
                           dry_run: bool = False) -> dict:
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/analyze/characters",
        api_key=config["apiKey"], json_body={"story_text": text},
        dry_run=dry_run,
    )


# --- Job management ---

def api_job_status(config: dict, job_id: str, *,
                   dry_run: bool = False) -> dict:
    return _request_with_retry(
        "GET", f"{config['baseUrl']}/jobs/{job_id}",
        api_key=config["apiKey"], dry_run=dry_run,
    )


def api_list_jobs(config: dict, *, status: str = None, job_type: str = None,
                  limit: int = None, dry_run: bool = False) -> dict:
    params: Dict[str, Any] = {}
    if status:
        params["status"] = status
    if job_type:
        params["type"] = job_type
    if limit is not None:
        params["limit"] = limit
    # Trailing slash required!
    return _request_with_retry(
        "GET", f"{config['baseUrl']}/jobs/",
        api_key=config["apiKey"], params=params or None, dry_run=dry_run,
    )


def api_cancel_job(config: dict, job_id: str, *,
                   dry_run: bool = False) -> dict:
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/jobs/{job_id}/cancel",
        api_key=config["apiKey"], dry_run=dry_run,
    )


# --- Account ---

def api_account_info(config: dict, *, dry_run: bool = False) -> dict:
    return _request_with_retry(
        "GET", f"{config['baseUrl']}/account/info",
        api_key=config["apiKey"], dry_run=dry_run,
    )


# --- Auth (public, no key required for verify) ---

def api_verify_key(config: dict, api_key_to_verify: str, *,
                   dry_run: bool = False) -> dict:
    return _request_with_retry(
        "POST", f"{config['baseUrl']}/auth/verify",
        json_body={"api_key": api_key_to_verify}, dry_run=dry_run,
    )


# ---------------------------------------------------------------------------
# Section 7: High-Level Operations
# ---------------------------------------------------------------------------

def _collect_optional_args(args, keys: List[str]) -> dict:
    """Extract optional args as dict, skipping None values.

    Replaces medeo's repetitive `if hasattr(args, "x") and args.x:` pattern.
    """
    return {k: getattr(args, k) for k in keys
            if getattr(args, k, None) is not None}


def _validate_url(url: str):
    is_http_url = any(url.startswith(s) for s in ALLOWED_URL_SCHEMES)
    is_image_data_uri = (
        url.startswith(ALLOWED_IMAGE_DATA_URI_PREFIX)
        and ";base64," in url[:128]
    )
    if not (is_http_url or is_image_data_uri):
        print(json.dumps({
            "error": (
                "Invalid URL scheme. Only http://, https://, and "
                "data:image/*;base64,... are allowed."
            ),
            "url": url[:100] + "..." if len(url) > 100 else url,
        }), file=sys.stderr)
        sys.exit(1)


def submit_and_poll(
    config: dict,
    subcommand: str,
    api_fn: Callable,
    api_kwargs: dict,
    *,
    no_wait: bool = False,
    dry_run: bool = False,
) -> dict:
    """Submit an async generation job. If wait=True, poll to completion.

    Returns the full result dict (either submission response or final result).
    """
    started_at = datetime.now(timezone.utc)
    job_type = JOB_TYPE_MAP.get(subcommand, "image")

    _log(f"Submitting {subcommand} job...")
    submit_result = api_fn(config, **api_kwargs, dry_run=dry_run)

    if dry_run:
        return submit_result

    job_id = submit_result.get("job_id", "")
    _log(f"Job submitted: {job_id} (type={job_type})")

    # Save submission record
    record = {
        "job_id": job_id,
        "job_type": job_type,
        "subcommand": subcommand,
        "status": "pending",
        "submitted_at": started_at.isoformat(),
    }
    save_job_record(record)

    if no_wait:
        submit_result["message"] = (
            f"Job submitted. Poll with: artclaw.py job-status --job-id {job_id}"
        )
        return submit_result

    # Poll until completion
    final = _poll_until(config, job_id, job_type)

    elapsed = time.time() - started_at.timestamp()
    final["_cli"] = {
        "subcommand": subcommand,
        "total_duration_seconds": round(elapsed, 1),
    }
    save_job_record(final)
    _log(f"Job complete: {job_id} ({elapsed:.0f}s)")
    return final


def save_job_record(record: dict):
    """Save job record to last_job.json and history (microsecond-precision)."""
    _ensure_dir()
    with open(LAST_JOB_FILE, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    _ensure_history_dir()
    # Microsecond precision avoids collisions (medeo used only seconds)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    hist_file = HISTORY_DIR / f"job_{ts}.json"
    with open(hist_file, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Prune old history (keep last 50)
    history_files = sorted(HISTORY_DIR.glob("job_*.json"))
    if len(history_files) > 50:
        for old_file in history_files[:-50]:
            old_file.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Section 8: Spawn Task Builder
# ---------------------------------------------------------------------------

def _build_delivery_instructions(deliver_to: str, channel: str,
                                 base_dir: str, subcommand: str) -> str:
    """Build channel-specific delivery instructions for spawn task."""
    # Determine if this is image or video generation
    is_image = subcommand in ("generate-image", "generate-marketing-image")

    if channel == "feishu":
        if is_image:
            return (
                "  1. Send via Feishu directly with URL:\n"
                f"     python3 {base_dir}/scripts/feishu_send_video.py "
                f"--image \"<result_url>\" --to \"{deliver_to}\"\n"
            )
        else:  # video
            return (
                "  1. Send via Feishu:\n"
                f"     python3 {base_dir}/scripts/feishu_send_video.py "
                f"--video-url \"<result_url>\" --to \"{deliver_to}\" "
                "--cover-url \"<thumbnail_url>\" --duration <duration_ms>\n"
                "     Note: duration is in milliseconds for Feishu"
            )
    if channel == "telegram":
        if is_image:
            return (
                "  1. Download the result locally (curl -o /tmp/artclaw_result.jpg \"<result_url>\")\n"
                "  2. Send via Telegram:\n"
                f"     TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN "
                f"python3 {base_dir}/scripts/telegram_send_video.py "
                f"--image /tmp/artclaw_result.jpg --to \"{deliver_to}\" "
                "--caption \"Result ready!\"\n"
            )
        else:  # video
            return (
                "  1. Download the result locally (curl -o /tmp/artclaw_result.mp4 \"<result_url>\")\n"
                "  2. Send via Telegram:\n"
                f"     TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN "
                f"python3 {base_dir}/scripts/telegram_send_video.py "
                f"--video /tmp/artclaw_result.mp4 --to \"{deliver_to}\" "
                "--cover-url \"<thumbnail_url>\" --duration <duration_seconds> "
                "--caption \"Result ready!\"\n"
                "     Note: duration is in seconds for Telegram"
            )
    if channel == "discord":
        media_file = "/tmp/artclaw_result.jpg" if is_image else "/tmp/artclaw_result.mp4"
        return (
            f"  1. Download the result locally:\n"
            f"     curl -sL -o {media_file} \"<result_url>\"\n"
            "  2. Use the message tool:\n"
            f"     message(action=\"send\", channel=\"discord\", "
            f"target=\"{deliver_to}\", message=\"Result ready!\", "
            f"filePath=\"{media_file}\")\n"
            "     (25 MB limit; for larger files share URL as link)"
        )
    return (
        f"  1. Deliver the result to \"{deliver_to}\" using the message tool,\n"
        "     or share the result URL as a link."
    )


def build_spawn_task(
    subcommand: str,
    args_dict: dict,
    *,
    deliver_to: Optional[str] = None,
    deliver_channel: Optional[str] = None,
    script_path: Optional[str] = None,
) -> dict:
    """Build a sessions_spawn payload for async generation via another agent.

    Returns:
        {
            "sessions_spawn_args": {"task": ..., "label": ..., "runTimeoutSeconds": ...},
            "command": "python3 .../artclaw.py generate-image --prompt ...",
        }
    """
    if script_path is None:
        script_path = str(Path(__file__).resolve())

    cmd_parts = ["python3", script_path, subcommand]
    for key, value in args_dict.items():
        if value is None or value is False:
            continue
        flag = f"--{key.replace('_', '-')}"
        if isinstance(value, bool) and value:
            cmd_parts.append(flag)
        elif isinstance(value, list):
            cmd_parts.append(flag)
            cmd_parts.extend(str(v) for v in value)
        else:
            cmd_parts.extend([flag, json.dumps(str(value), ensure_ascii=False)
                              if isinstance(value, str) and " " in value
                              else str(value)])

    cmd_str = " ".join(cmd_parts)
    base_dir = str(Path(__file__).resolve().parent.parent)
    deliver_to_str = deliver_to or "<user_id>"
    deliver_channel_str = deliver_channel or "feishu"

    delivery_instructions = _build_delivery_instructions(
        deliver_to_str, deliver_channel_str, base_dir, subcommand,
    )

    label_text = args_dict.get("prompt", subcommand)
    if isinstance(label_text, str) and len(label_text) > 60:
        label_text = label_text[:60] + "..."

    task_text = (
        "You are an ArtClaw creative worker. Execute the following command "
        "and deliver the result to the user.\n\n"
        f"Command:\n```\n{cmd_str}\n```\n\n"
        "This command calls the ArtClaw API and waits for completion. "
        "Typical times: images ~30s, videos ~2-5min, workflows ~5-15min. "
        "Wait for the command to complete — do NOT background it.\n\n"
        "When the command finishes:\n"
        "- If the JSON output contains \"status\": \"success\":\n"
        "  Extract the result URL from the JSON output.\n"
        f"{delivery_instructions}\n"
        "  Always include a short summary: what was generated, settings used.\n"
        "- If error indicates insufficient credits (402), inform the user and "
        f"guide them to top up at {TOPUP_URL}\n"
        "- For other failures, report the error and suggest retry."
    )

    return {
        "sessions_spawn_args": {
            "task": task_text,
            "label": f"artclaw: {label_text}",
            "runTimeoutSeconds": SPAWN_TIMEOUT_SECONDS,
        },
        "command": cmd_str,
    }


def _should_spawn(args) -> bool:
    """Infer spawn mode from args.

    Spawn is enabled if:
    - --spawn is explicitly provided, OR
    - both --deliver-to and --deliver-channel are provided.
    """
    has_deliver_to = bool(getattr(args, "deliver_to", None))
    has_deliver_channel = bool(getattr(args, "deliver_channel", None))

    if has_deliver_to ^ has_deliver_channel:
        print(json.dumps({
            "error": "Both --deliver-to and --deliver-channel are required together",
            "hint": "Provide both for async spawn delivery, or omit both for local execution",
        }, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    return bool(getattr(args, "spawn", False) or
                (has_deliver_to and has_deliver_channel))


# ---------------------------------------------------------------------------
# Section 9: CLI Command Handlers
# ---------------------------------------------------------------------------

# --- Generation commands ---

def cmd_generate_image(args, config: dict):
    """Generate an image from a text prompt."""
    dry_run = getattr(args, "dry_run", False)
    _check_api_key(config, allow_dry_run=dry_run)

    api_kwargs: Dict[str, Any] = {"prompt": args.prompt}
    api_kwargs.update(_collect_optional_args(args, [
        "aspect_ratio", "resolution", "model", "callback_url",
    ]))

    # Handle spawn mode differently: don't convert files to base64 yet
    if _should_spawn(args):
        # Pass reference URLs/files as-is to spawn task
        if args.reference_urls:
            api_kwargs["reference_urls"] = args.reference_urls
        if getattr(args, "reference_files", None):
            api_kwargs["reference_files"] = args.reference_files

        result = build_spawn_task(
            "generate-image", api_kwargs,
            deliver_to=getattr(args, "deliver_to", None),
            deliver_channel=getattr(args, "deliver_channel", None),
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Non-spawn mode: convert reference_files to base64 now
    reference_urls = list(args.reference_urls) if args.reference_urls else []
    if getattr(args, "reference_files", None):
        for file_path in args.reference_files:
            _log(f"Converting local file to base64: {file_path}")
            base64_uri = _file_to_base64(file_path)
            reference_urls.append(base64_uri)

    if reference_urls:
        api_kwargs["reference_urls"] = reference_urls
        for url in reference_urls:
            _validate_url(url)

    result = submit_and_poll(
        config, "generate-image", api_generate_image, api_kwargs,
        no_wait=args.no_wait, dry_run=dry_run,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_generate_video(args, config: dict):
    """Generate a video from a text prompt."""
    dry_run = getattr(args, "dry_run", False)
    _check_api_key(config, allow_dry_run=dry_run)

    api_kwargs: Dict[str, Any] = {"prompt": args.prompt}
    api_kwargs.update(_collect_optional_args(args, [
        "aspect_ratio", "duration", "resolution", "model", "callback_url",
    ]))

    # Handle spawn mode differently: don't convert files to base64 yet
    if _should_spawn(args):
        # Pass reference URLs/files as-is to spawn task
        if args.reference_urls:
            api_kwargs["reference_urls"] = args.reference_urls
        if getattr(args, "reference_files", None):
            api_kwargs["reference_files"] = args.reference_files

        result = build_spawn_task(
            "generate-video", api_kwargs,
            deliver_to=getattr(args, "deliver_to", None),
            deliver_channel=getattr(args, "deliver_channel", None),
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Non-spawn mode: convert reference_files to base64 now
    reference_urls = list(args.reference_urls) if args.reference_urls else []
    if getattr(args, "reference_files", None):
        for file_path in args.reference_files:
            _log(f"Converting local file to base64: {file_path}")
            base64_uri = _file_to_base64(file_path)
            reference_urls.append(base64_uri)

    if reference_urls:
        api_kwargs["reference_urls"] = reference_urls
        for url in reference_urls:
            _validate_url(url)

    result = submit_and_poll(
        config, "generate-video", api_generate_video, api_kwargs,
        no_wait=args.no_wait, dry_run=dry_run,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_generate_marketing_image(args, config: dict):
    """Generate a marketing image with auto-enhanced prompt."""
    dry_run = getattr(args, "dry_run", False)
    _check_api_key(config, allow_dry_run=dry_run)

    api_kwargs: Dict[str, Any] = {"prompt": args.prompt}
    api_kwargs.update(_collect_optional_args(args, ["size", "callback_url"]))

    result = submit_and_poll(
        config, "generate-marketing-image",
        api_generate_marketing_image, api_kwargs,
        no_wait=args.no_wait, dry_run=dry_run,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- Workflow commands ---

def cmd_list_workflows(args, config: dict):
    """List available preset workflows."""
    dry_run = getattr(args, "dry_run", False)
    _check_api_key(config, allow_dry_run=dry_run)
    result = api_list_workflows(config, dry_run=dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_run_workflow(args, config: dict):
    """Execute a preset workflow."""
    dry_run = getattr(args, "dry_run", False)
    _check_api_key(config, allow_dry_run=dry_run)

    try:
        inputs = json.loads(args.inputs)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": f"--inputs must be valid JSON: {e}",
            "hint": 'Example: --inputs \'{"prompt": "a cat"}\'',
        }), file=sys.stderr)
        sys.exit(1)

    api_kwargs: Dict[str, Any] = {
        "workflow_id": args.workflow_id,
        "inputs": inputs,
    }
    api_kwargs.update(_collect_optional_args(args, ["timeout", "callback_url"]))

    if _should_spawn(args):
        result = build_spawn_task(
            "run-workflow", api_kwargs,
            deliver_to=getattr(args, "deliver_to", None),
            deliver_channel=getattr(args, "deliver_channel", None),
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    result = submit_and_poll(
        config, "run-workflow", api_run_workflow, api_kwargs,
        no_wait=args.no_wait, dry_run=dry_run,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- Analysis commands (sync) ---

def cmd_analyze_image(args, config: dict):
    """Analyze images with AI vision."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    for url in args.reference_urls:
        _validate_url(url)
    result = api_analyze_image(
        config, args.reference_urls,
        query=getattr(args, "query", "") or "",
        dry_run=getattr(args, "dry_run", False),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_analyze_video(args, config: dict):
    """Analyze video content with AI."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    for url in args.reference_urls:
        _validate_url(url)
    result = api_analyze_video(
        config, args.reference_urls,
        query=getattr(args, "query", "") or "",
        dry_run=getattr(args, "dry_run", False),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_analyze_script(args, config: dict):
    """Extract script from video and design interactive nodes."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    for url in args.reference_paths:
        _validate_url(url)
    kwargs: Dict[str, Any] = {"reference_paths": args.reference_paths}
    kwargs.update(_collect_optional_args(args, [
        "original_script", "node_to_replace",
    ]))
    result = api_analyze_script(config, **kwargs,
                                dry_run=getattr(args, "dry_run", False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_analyze_characters(args, config: dict):
    """Parse character profiles from story text."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    result = api_analyze_characters(
        config, args.text,
        dry_run=getattr(args, "dry_run", False),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- Job management commands ---

def cmd_job_status(args, config: dict):
    """Check a job's current status."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    result = api_job_status(config, args.job_id,
                            dry_run=getattr(args, "dry_run", False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_list_jobs(args, config: dict):
    """List historical jobs."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    kwargs = _collect_optional_args(args, ["status", "job_type", "limit"])
    result = api_list_jobs(config, **kwargs,
                           dry_run=getattr(args, "dry_run", False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_cancel_job(args, config: dict):
    """Cancel a pending or running job."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    result = api_cancel_job(config, args.job_id,
                            dry_run=getattr(args, "dry_run", False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- Account commands ---

def cmd_account_info(args, config: dict):
    """Show account balance and usage."""
    _check_api_key(config, allow_dry_run=getattr(args, "dry_run", False))
    result = api_account_info(config,
                              dry_run=getattr(args, "dry_run", False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_verify_key(args, config: dict):
    """Verify an API key is valid (no auth required)."""
    key = args.api_key or config.get("apiKey", "")
    if not key:
        print(json.dumps({"error": "No API key provided or configured"}),
              file=sys.stderr)
        sys.exit(1)
    result = api_verify_key(config, key,
                            dry_run=getattr(args, "dry_run", False))
    print(json.dumps(result, indent=2, ensure_ascii=False))

# --- Config commands ---

def cmd_config(args, config: dict):
    """Show current configuration."""
    safe = dict(config)
    key = safe.get("apiKey", "")
    if key and len(key) > 10:
        safe["apiKey"] = key[:6] + "..." + key[-4:]
    elif key:
        safe["apiKey"] = "***"
    safe["source_env_var"] = "ARTCLAW_API_KEY"
    safe["config_file"] = str(CONFIG_FILE)
    safe["state_dir"] = str(STATE_DIR)
    print(json.dumps(safe, indent=2, ensure_ascii=False))


def cmd_config_init(args, config: dict):
    """Initialize or update config.json with API key."""
    _ensure_dir()

    if not args.api_key.startswith("vk_"):
        _log(f"WARNING: API key should start with 'vk_'. Got: {args.api_key[:8]}...")

    raw = _load_raw_config()
    raw["apiKey"] = args.api_key
    raw.setdefault("baseUrl", DEFAULT_BASE_URL)

    with open(CONFIG_FILE, "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)

    _log(f"Config saved to {CONFIG_FILE}")
    print(json.dumps({
        "status": "ok",
        "config_file": str(CONFIG_FILE),
    }, indent=2))


# --- Spawn task command ---

def cmd_spawn_task(args, config: dict):
    """Build sessions_spawn payload for async generation."""
    _check_api_key(config)

    args_dict: Dict[str, Any] = {"prompt": args.prompt}
    args_dict.update(_collect_optional_args(args, [
        "aspect_ratio", "resolution", "duration", "model",
        "size", "workflow_id", "inputs",
    ]))
    if args.reference_urls:
        args_dict["reference_urls"] = args.reference_urls
    if args.no_wait:
        args_dict["no_wait"] = True

    result = build_spawn_task(
        args.subcommand,
        args_dict,
        deliver_to=getattr(args, "deliver_to", None),
        deliver_channel=getattr(args, "deliver_channel", None),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- Self-update ---

def _repo_root() -> Path:
    """Return the root directory of the artclaw-skill repo.

    Assumes this script lives at <repo_root>/scripts/artclaw.py.
    """
    return Path(__file__).resolve().parent.parent


def _apply_archive(archive_zip_bytes: bytes, repo_root: Path, *,
                   dry_run: bool = False) -> dict:
    """Extract a GitHub main.zip archive over repo_root.

    The zip contains a single top-level directory (e.g. artclaw-skill-main/).
    We strip that prefix and merge the contents into repo_root.

    Returns a summary dict with lists of added/modified/deleted files.
    """
    import io
    import zipfile
    import shutil
    import tempfile

    with zipfile.ZipFile(io.BytesIO(archive_zip_bytes)) as zf:
        names = zf.namelist()

    # Determine the top-level prefix to strip (e.g. "artclaw-skill-main/")
    prefix = names[0] if names[0].endswith("/") else names[0].split("/")[0] + "/"

    # Collect incoming file paths (relative to repo_root) and their content
    incoming: Dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(archive_zip_bytes)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            rel = info.filename
            if not rel.startswith(prefix):
                continue
            rel_path = rel[len(prefix):]  # strip top-level dir prefix
            if not rel_path:
                continue
            incoming[rel_path] = zf.read(info.filename)

    # Collect existing files under repo_root
    existing: set = set()
    for p in repo_root.rglob("*"):
        if p.is_file():
            existing.add(str(p.relative_to(repo_root)))

    added, modified, unchanged = [], [], []
    for rel_path, new_bytes in sorted(incoming.items()):
        dest = repo_root / rel_path
        if not dest.exists():
            added.append(rel_path)
        else:
            try:
                old_bytes = dest.read_bytes()
            except IOError:
                old_bytes = b""
            if old_bytes != new_bytes:
                modified.append(rel_path)
            else:
                unchanged.append(rel_path)

    # Files in existing but not in incoming are untouched (we never delete)
    # unless --delete is someday added.

    if dry_run:
        return {
            "status": "dry_run",
            "added": added,
            "modified": modified,
            "unchanged_count": len(unchanged),
        }

    # Write new/modified files atomically via temp file + rename
    for rel_path in added + modified:
        dest = repo_root / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(dir=dest.parent,
                                            prefix=".artclaw_upd_")
        try:
            with os.fdopen(tmp_fd, "wb") as f:
                f.write(incoming[rel_path])
            if dest.exists():
                shutil.copymode(str(dest), tmp_path)
            os.replace(tmp_path, str(dest))
        except OSError as e:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise OSError(f"Failed to write {dest}: {e}") from e

    return {
        "status": "updated",
        "added": added,
        "modified": modified,
        "unchanged_count": len(unchanged),
    }


def cmd_self_update(args, config: dict):
    """Update the entire artclaw-skill repo from GitHub (downloads archive ZIP)."""
    dry_run = getattr(args, "dry_run", False)
    repo_root = _repo_root()

    _log(f"Downloading archive from {GITHUB_ARCHIVE_URL} ...")
    _log(f"Repo root: {repo_root}")

    try:
        resp = requests.get(
            GITHUB_ARCHIVE_URL,
            timeout=(CONNECT_TIMEOUT, 120),
            stream=False,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(json.dumps({
            "error": f"Failed to download archive: {e}",
            "url": GITHUB_ARCHIVE_URL,
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    _log(f"Downloaded {len(resp.content):,} bytes. Applying update...")

    try:
        summary = _apply_archive(resp.content, repo_root, dry_run=dry_run)
    except OSError as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)

    if not summary["added"] and not summary["modified"]:
        summary["message"] = "Already up to date. No files changed."
    else:
        n_add = len(summary["added"])
        n_mod = len(summary["modified"])
        parts = []
        if n_add:
            parts.append(f"{n_add} added")
        if n_mod:
            parts.append(f"{n_mod} modified")
        action = "Would update" if dry_run else "Updated"
        summary["message"] = f"{action}: {', '.join(parts)}."

    summary["repo_root"] = str(repo_root)
    summary["source"] = GITHUB_ARCHIVE_URL
    print(json.dumps(summary, indent=2, ensure_ascii=False))


# --- History commands ---

def cmd_last_job(args, config: dict):
    """Show the most recent job record."""
    if not LAST_JOB_FILE.exists():
        print(json.dumps({"message": "No job records found."}))
        return
    with open(LAST_JOB_FILE, "r") as f:
        record = json.load(f)
    print(json.dumps(record, indent=2, ensure_ascii=False))


def cmd_history(args, config: dict):
    """Show job history."""
    if not HISTORY_DIR.exists():
        print(json.dumps({"message": "No history found.", "jobs": []}))
        return

    files = sorted(HISTORY_DIR.glob("job_*.json"), reverse=True)
    limit = args.limit
    jobs = []
    for fpath in files[:limit]:
        try:
            with open(fpath, "r") as fh:
                record = json.load(fh)
            jobs.append({
                "file": fpath.name,
                "job_id": record.get("job_id", ""),
                "status": record.get("status", "unknown"),
                "submitted_at": record.get("submitted_at", ""),
                "subcommand": record.get("subcommand", ""),
            })
        except (json.JSONDecodeError, IOError):
            pass

    print(json.dumps({
        "count": len(jobs),
        "total_records": len(files),
        "jobs": jobs,
    }, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Section 10: CLI Parser
# ---------------------------------------------------------------------------

def _add_wait_and_dry_run(parser):
    """Add --no-wait and --dry-run flags to async command parsers."""
    parser.add_argument("--no-wait", action="store_true", default=False,
                        help="Return immediately after submission (don't poll)")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Print what would be sent without making API calls")
    parser.add_argument("--callback-url", default=None,
                        help="Webhook URL for completion notification")


def _add_dry_run(parser):
    """Add --dry-run flag to sync command parsers."""
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Print what would be sent without making API calls")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="artclaw",
        description="ArtClaw AI Creative Suite CLI — agent-friendly API client",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # --- generate-image ---
    p = sub.add_parser("generate-image", help="Generate image from prompt")
    p.add_argument("--prompt", required=True, help="Text description of the image")
    p.add_argument("--aspect-ratio", default=None,
                   choices=sorted(VALID_ASPECT_RATIOS),
                   help="Aspect ratio (default: 16:9)")
    p.add_argument("--resolution", default=None,
                   choices=sorted(VALID_RESOLUTIONS_IMAGE),
                   help="Resolution: 1K, 2K, 4K")
    p.add_argument("--reference-urls", nargs="+", default=None,
                   help="Reference images (HTTPS URLs or base64: data:image/png;base64,...)")
    p.add_argument("--reference-files", nargs="+", default=None,
                   help="Reference images (local file paths, auto-converted to base64)")
    p.add_argument("--model", default=None, help="Model ID override")
    p.add_argument("--spawn", action="store_true", default=False,
                   help="Output sessions_spawn_args payload instead of running directly")
    p.add_argument("--deliver-to", default=None,
                   help="Delivery target (ou_xxx, chat_id, channel_id) — used with --spawn")
    p.add_argument("--deliver-channel", default=None,
                   choices=["feishu", "telegram", "discord"],
                   help="Delivery channel — used with --spawn")
    _add_wait_and_dry_run(p)

    # --- generate-video ---
    p = sub.add_parser("generate-video", help="Generate video from prompt")
    p.add_argument("--prompt", required=True, help="Text description of the video")
    p.add_argument("--aspect-ratio", default=None,
                   choices=sorted(VALID_ASPECT_RATIOS),
                   help="Aspect ratio (default: 16:9)")
    p.add_argument("--duration", type=int, default=None,
                   help="Video duration in seconds (2-12)")
    p.add_argument("--resolution", default=None,
                   choices=sorted(VALID_RESOLUTIONS_VIDEO),
                   help="Resolution: 480p, 720p, 1080p")
    p.add_argument("--reference-urls", nargs="+", default=None,
                   help="Reference images for I2V (HTTPS URLs or base64)")
    p.add_argument("--reference-files", nargs="+", default=None,
                   help="Reference images for I2V (local file paths, auto-converted to base64)")
    p.add_argument("--model", default=None, help="Model ID override")
    p.add_argument("--spawn", action="store_true", default=False,
                   help="Output sessions_spawn_args payload instead of running directly")
    p.add_argument("--deliver-to", default=None,
                   help="Delivery target (ou_xxx, chat_id, channel_id) — used with --spawn")
    p.add_argument("--deliver-channel", default=None,
                   choices=["feishu", "telegram", "discord"],
                   help="Delivery channel — used with --spawn")
    _add_wait_and_dry_run(p)

    # --- generate-marketing-image ---
    p = sub.add_parser("generate-marketing-image",
                       help="Generate marketing image with auto-enhanced prompt")
    p.add_argument("--prompt", required=True, help="Marketing image description")
    p.add_argument("--size", default=None,
                   help="Image size (e.g. 1080x1920)")
    _add_wait_and_dry_run(p)

    # --- list-workflows ---
    p = sub.add_parser("list-workflows", help="List available preset workflows")
    _add_dry_run(p)

    # --- run-workflow ---
    p = sub.add_parser("run-workflow", help="Execute a preset workflow")
    p.add_argument("--workflow-id", required=True, help="Workflow ID to run")
    p.add_argument("--inputs", required=True,
                   help='Workflow inputs as JSON string (e.g. \'{"prompt": "a cat"}\')')
    p.add_argument("--timeout", type=int, default=None,
                   help="Workflow timeout in seconds")
    p.add_argument("--spawn", action="store_true", default=False,
                   help="Output sessions_spawn_args payload instead of running directly")
    p.add_argument("--deliver-to", default=None,
                   help="Delivery target (ou_xxx, chat_id, channel_id) — used with --spawn")
    p.add_argument("--deliver-channel", default=None,
                   choices=["feishu", "telegram", "discord"],
                   help="Delivery channel — used with --spawn")
    _add_wait_and_dry_run(p)

    # --- analyze-image ---
    p = sub.add_parser("analyze-image", help="Analyze images with AI vision")
    p.add_argument("--reference-urls", nargs="+", required=True,
                   help="Image URLs to analyze")
    p.add_argument("--query", default=None,
                   help="Specific question about the image")
    _add_dry_run(p)

    # --- analyze-video ---
    p = sub.add_parser("analyze-video", help="Analyze video content")
    p.add_argument("--reference-urls", nargs="+", required=True,
                   help="Video URLs to analyze")
    p.add_argument("--query", default=None,
                   help="Specific question about the video")
    _add_dry_run(p)

    # --- analyze-script ---
    p = sub.add_parser("analyze-script",
                       help="Extract script from video + interactive nodes")
    p.add_argument("--reference-paths", nargs="+", required=True,
                   help="Video URLs/paths to analyze")
    p.add_argument("--original-script", default=None,
                   help="Existing script for regeneration mode")
    p.add_argument("--node-to-replace", default=None,
                   help="Specific node to regenerate")
    _add_dry_run(p)

    # --- analyze-characters ---
    p = sub.add_parser("analyze-characters",
                       help="Parse character profiles from story text")
    p.add_argument("--text", required=True,
                   help="Story text to extract characters from")
    _add_dry_run(p)

    # --- job-status ---
    p = sub.add_parser("job-status", help="Check job status")
    p.add_argument("--job-id", required=True, help="Job ID to check")
    _add_dry_run(p)

    # --- list-jobs ---
    p = sub.add_parser("list-jobs", help="List historical jobs")
    p.add_argument("--status", default=None,
                   help="Filter by status (pending, running, success, failed, ...)")
    p.add_argument("--job-type", default=None,
                   help="Filter by type (image_generation, video_generation, ...)")
    p.add_argument("--limit", type=int, default=None,
                   help="Number of jobs to return (1-100)")
    _add_dry_run(p)

    # --- cancel-job ---
    p = sub.add_parser("cancel-job", help="Cancel a pending/running job")
    p.add_argument("--job-id", required=True, help="Job ID to cancel")
    _add_dry_run(p)

    # --- account-info ---
    p = sub.add_parser("account-info", help="Show account balance and usage")
    _add_dry_run(p)

    # --- verify-key ---
    p = sub.add_parser("verify-key",
                       help="Verify an API key (no auth required)")
    p.add_argument("--api-key", default=None,
                   help="API key to verify (uses configured key if omitted)")
    _add_dry_run(p)

    # --- config ---
    sub.add_parser("config", help="Show current configuration")

    # --- config-init ---
    p = sub.add_parser("config-init", help="Initialize or update config")
    p.add_argument("--api-key", required=True,
                   help="ArtClaw API key (starts with vk_)")

    # --- spawn-task ---
    p = sub.add_parser("spawn-task",
                       help="Build sessions_spawn payload for async agent execution")
    p.add_argument("--subcommand", required=True,
                   choices=["generate-image", "generate-video",
                            "generate-marketing-image", "run-workflow"],
                   help="Which generation command to spawn")
    p.add_argument("--prompt", default=None, help="Generation prompt")
    p.add_argument("--aspect-ratio", default=None, help="Aspect ratio")
    p.add_argument("--resolution", default=None, help="Resolution")
    p.add_argument("--duration", type=int, default=None,
                   help="Video duration (seconds)")
    p.add_argument("--model", default=None, help="Model ID override")
    p.add_argument("--size", default=None, help="Marketing image size")
    p.add_argument("--workflow-id", default=None, help="Workflow ID")
    p.add_argument("--inputs", default=None, help="Workflow inputs (JSON)")
    p.add_argument("--reference-urls", nargs="+", default=None,
                   help="Reference URLs")
    p.add_argument("--no-wait", action="store_true", default=False,
                   help="Don't wait for completion in spawned task")
    p.add_argument("--deliver-to", default=None,
                   help="Delivery target (ou_xxx, chat_id, channel_id)")
    p.add_argument("--deliver-channel", default=None,
                   choices=["feishu", "telegram", "discord"],
                   help="Delivery channel")

    # --- last-job ---
    sub.add_parser("last-job", help="Show last job record")

    # --- history ---
    p = sub.add_parser("history", help="Show local job history")
    p.add_argument("--limit", type=int, default=20,
                   help="Number of records to show")

    # --- self-update ---
    p = sub.add_parser("self-update",
                       help="Update the entire artclaw-skill repo from GitHub")
    _add_dry_run(p)

    return parser


# ---------------------------------------------------------------------------
# Section 11: Command Map & Main Entry Point
# ---------------------------------------------------------------------------

COMMAND_MAP = {
    "generate-image": cmd_generate_image,
    "generate-video": cmd_generate_video,
    "generate-marketing-image": cmd_generate_marketing_image,
    "list-workflows": cmd_list_workflows,
    "run-workflow": cmd_run_workflow,
    "analyze-image": cmd_analyze_image,
    "analyze-video": cmd_analyze_video,
    "analyze-script": cmd_analyze_script,
    "analyze-characters": cmd_analyze_characters,
    "job-status": cmd_job_status,
    "list-jobs": cmd_list_jobs,
    "cancel-job": cmd_cancel_job,
    "account-info": cmd_account_info,
    "verify-key": cmd_verify_key,
    "config": cmd_config,
    "config-init": cmd_config_init,
    "spawn-task": cmd_spawn_task,
    "last-job": cmd_last_job,
    "history": cmd_history,
    "self-update": cmd_self_update,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = _get_config()

    handler = COMMAND_MAP.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)

    try:
        handler(args, config)
    except ArtClawApiError as e:
        if e.is_retryable():
            _log(f"[retryable] {e.to_dict()}")
            print(json.dumps({
                "error": "service_unavailable",
                "message": "ArtClaw service is temporarily unavailable. Please try again.",
                "retryable": True,
            }, indent=2), file=sys.stderr)
        else:
            print(json.dumps(e.to_dict(), indent=2, ensure_ascii=False),
                  file=sys.stderr)
        sys.exit(1)
    except ArtClawPollTimeout as e:
        print(json.dumps({
            "error": "poll_timeout",
            "job_id": e.job_id,
            "job_type": e.job_type,
            "elapsed_seconds": round(e.elapsed),
            "last_status": e.last_status,
            "message": (f"Job timed out after {round(e.elapsed)}s. "
                        f"Check with: artclaw.py job-status --job-id {e.job_id}"),
            "retryable": True,
        }, indent=2), file=sys.stderr)
        sys.exit(1)
    except ArtClawPollFailed as e:
        print(json.dumps({
            "error": "job_failed",
            "job_id": e.job_id,
            "status": e.status,
            "detail": e.error_detail,
        }, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        _log("Interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
