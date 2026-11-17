"""HTTP client for the dLazy tool API, scoped to image generation.

Every slide image in this skill goes through here. The endpoints mirror what the
official `dlazy` CLI uses:

    POST /api/cli/tool                  run a tool, returns {output}
    GET  /api/cli/tool?generateId=...   poll an async task
    POST /api/cli/upload-url            signed URL for uploading local media

`gpt-image-2` answers synchronously today, but the tool API is free to switch a
model to the async task shape at any time, so a `generateId` in the response is
polled rather than treated as an error.

Results come back as URLs on files.dlazy.com; the callers here want raw bytes,
so every helper downloads before returning.
"""

from __future__ import annotations

import mimetypes
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional

DEFAULT_BASE_URL = "https://dlazy.com"
POLL_INTERVAL = 3
DEFAULT_TIMEOUT = 1800

# The tool API gates on X-CLI-Version and answers 426 without it. We speak the
# same contract as the official CLI, so we advertise the version we were built
# against; bump it if the server ever raises MIN_SUPPORTED_CLI_VERSION past this.
CLI_VERSION = "1.2.3"

API_KEY_URL = "https://dlazy.com/dashboard/organization/api-key"
CREDITS_URL = "https://dlazy.com/dashboard/organization/settings?tab=credits"

# A long generation is polled for minutes. A proxy or flaky link can abort a
# single poll, and giving up there would discard work that is already paid for
# and probably finished server-side — so transient errors are retried.
POLL_MAX_CONSECUTIVE_ERRORS = 5


class DlazyError(Exception):
    pass


def _requests():
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - depends on the install
        raise DlazyError(
            "the `requests` package is not installed in the active environment. "
            "Bootstrap the shared runtime with "
            "`python3 scripts/dlazy_ppt_runtime.py bootstrap`."
        ) from exc
    return requests


def base_url() -> str:
    return (os.getenv("DLAZY_BASE_URL") or DEFAULT_BASE_URL).strip().rstrip("/")


def api_key() -> Optional[str]:
    return (os.getenv("DLAZY_API_KEY") or "").strip() or None


def _headers() -> Dict[str, str]:
    key = api_key()
    if not key:
        raise DlazyError(
            f"DLAZY_API_KEY is not set. Get a key from {API_KEY_URL} and save it with "
            "`python3 scripts/dlazy_ppt_runtime.py config --api-key <key>`."
        )
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "X-CLI-Version": CLI_VERSION,
    }


def _fail(prefix: str, status: int, body: str) -> None:
    """Turn an API error into a message that names the fix, not just the code."""
    hint = ""
    lowered = body.lower()
    if status == 401 or "unauthorized" in lowered:
        hint = f" Check the key, or get a new one from {API_KEY_URL}."
    elif "insufficient_balance" in lowered:
        hint = f" The organization is out of credits — top up at {CREDITS_URL}."
    raise DlazyError(f"{prefix} ({status}): {body[:500]}{hint}")


def upload_file(path: Path) -> str:
    """Upload a local image to dLazy storage and return its public URL."""
    requests = _requests()
    filename = path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    resp = requests.post(
        f"{base_url()}/api/cli/upload-url",
        headers=_headers(),
        json={"filename": filename, "contentType": content_type},
        timeout=60,
    )
    if not resp.ok:
        _fail(f"upload-url failed for {filename}", resp.status_code, resp.text)
    data = resp.json()

    with path.open("rb") as fh:
        put_headers = dict(data.get("requiredHeaders") or {})
        put_headers.setdefault("Content-Type", content_type)
        put = requests.put(data["signedUrl"], data=fh, headers=put_headers, timeout=600)
    if not put.ok:
        _fail(f"upload failed for {filename}", put.status_code, put.text)
    return data["publicUrl"]


def _poll(generate_id: str, timeout: int) -> Any:
    requests = _requests()
    deadline = time.time() + timeout
    url = f"{base_url()}/api/cli/tool?generateId={generate_id}"
    errors = 0
    while time.time() < deadline:
        time.sleep(POLL_INTERVAL)
        try:
            resp = requests.get(url, headers=_headers(), timeout=60)
            if not resp.ok:
                _fail(f"poll failed for task {generate_id}", resp.status_code, resp.text)
            data = resp.json()
        except DlazyError:
            raise
        except Exception as exc:
            errors += 1
            if errors >= POLL_MAX_CONSECUTIVE_ERRORS:
                raise DlazyError(
                    f"task {generate_id}: polling failed {errors} times in a row: {exc}"
                ) from exc
            print(
                f"transient error polling {generate_id} "
                f"({errors}/{POLL_MAX_CONSECUTIVE_ERRORS}): {exc}",
                file=sys.stderr,
            )
            time.sleep(POLL_INTERVAL * errors)
            continue

        errors = 0
        status = data.get("status")
        if status == "completed":
            return data.get("result")
        if status == "failed":
            raise DlazyError(f"task {generate_id} failed: {data.get('error')}")
    raise DlazyError(f"task {generate_id} did not finish within {timeout}s")


def run_tool(model: str, payload: Dict[str, Any], timeout: int = DEFAULT_TIMEOUT) -> Any:
    """Run one dLazy tool and return its output, waiting out async tasks."""
    requests = _requests()
    resp = requests.post(
        f"{base_url()}/api/cli/tool",
        headers=_headers(),
        json={"model": model, "input": payload},
        timeout=timeout,
    )
    if not resp.ok:
        _fail(f"{model} failed", resp.status_code, resp.text)

    output = resp.json().get("output")
    if isinstance(output, dict) and isinstance(output.get("generateId"), str):
        print(f"{model} running as async task {output['generateId']}", file=sys.stderr)
        return _poll(output["generateId"], timeout)
    return output


def download_bytes(url: str) -> bytes:
    requests = _requests()
    resp = requests.get(url, timeout=600)
    if not resp.ok:
        _fail(f"download failed for {url}", resp.status_code, resp.text)
    return resp.content


def generate_images(model: str, payload: Dict[str, Any], timeout: int = DEFAULT_TIMEOUT) -> List[bytes]:
    """Run an image tool and return the rendered images as raw bytes."""
    output = run_tool(model, payload, timeout=timeout)
    urls = (output or {}).get("urls") or []
    if not urls:
        raise DlazyError(f"{model} returned no image url (output: {output})")
    return [download_bytes(u) for u in urls]
