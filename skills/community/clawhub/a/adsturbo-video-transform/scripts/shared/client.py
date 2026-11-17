#!/usr/bin/env python3
"""HTTP client for the AdsTurbo Open API.

Covers the three response shapes the server can return:
  1. envelope success  {"ret": 1, "data": {"ent": {...}}}
  2. envelope failure  {"ret": <non-1>, "msg": "..."}  -- still HTTP 200
  3. auth failure      HTTP 401 with a plain-text body, no envelope at all

Standard library only (urllib), so the scripts run anywhere Python 3.8+ does
without a pip install step -- sandboxes and fresh agent environments included.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

DEFAULT_BASE_URL = "https://adsturbo.ai/klian/novartapi"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_POLL_TIMEOUT = 900
REQUEST_TIMEOUT = 60
UPLOAD_TIMEOUT = 300

WORK_STATUS_PATH = "/openapi/v1/work/status"
WORK_BATCH_STATUS_PATH = "/openapi/v1/work/batch-status"

TERMINAL_OK = "completed"
PLAN_REQUIRED = 2103  # "Pro plan or above is required": Pro-only features such as custom digital humans
SUBSCRIPTION_REQUIRED = 2100  # "Subscription required to proceed": 1080p+ video / 4K images
TERMINAL_FAIL = "failed"

USER_AGENT = "adsturbo-skill (+https://adsturbo.ai)"
SIGNUP_URL = "https://adsturbo.ai?channel=clawhub"
API_KEY_STEPS = [
    "Ask the user for their email, then run: python3 scripts/login.py start --email <email>",
    "If it returns next=enter_captcha, show the user the captcha image and run: python3 scripts/login.py captcha --code <what they typed>",
    "Ask the user for the code AdsTurbo emailed them, then run: python3 scripts/login.py verify --code <code>",
    "This signs them up (or logs them in) and saves an API key on this machine; then re-run the original command",
    f"Fallback: sign up at {SIGNUP_URL}, create a key at https://adsturbo.ai/iris/api, export ADSTURBO_API_KEY=<key>",
]
NO_KEY_MESSAGE = (
    "No AdsTurbo API key yet. Sign the user up or log them in right here with "
    "scripts/login.py (email + verification code), or set ADSTURBO_API_KEY."
)
CONFIG_DIR_ENV = "ADSTURBO_CONFIG_DIR"
CREDENTIALS_FILE = "credentials.json"


def config_dir() -> Path:
    return Path(os.environ.get(CONFIG_DIR_ENV) or Path.home() / ".config" / "adsturbo")


def resolve_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("ADSTURBO_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")


def site_origin(base_url: str) -> str:
    """https://adsturbo.ai/klian/novartapi -> https://adsturbo.ai: keys are saved per site."""
    parts = urllib.parse.urlsplit(base_url)
    return f"{parts.scheme}://{parts.netloc}"


def load_saved_key(base_url: str) -> str:
    """The key scripts/login.py saved for this site, or "" when there is none."""
    path = config_dir() / CREDENTIALS_FILE
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    entry = saved.get(site_origin(base_url)) if isinstance(saved, dict) else None
    return entry.get("api_key", "") if isinstance(entry, dict) else ""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Surface 3xx as an HTTPError: following it would turn the POST into a GET."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


class AdsTurboError(Exception):
    """A business-level failure reported by the API."""

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class AdsTurboAuthError(AdsTurboError):
    """The API key is missing, invalid or expired."""

    def __init__(self, msg: str = "API key is invalid or expired"):
        super().__init__(401, msg)


class AdsTurboClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.base_url = resolve_base_url(base_url)
        self.api_key = api_key or os.environ.get("ADSTURBO_API_KEY", "") or load_saved_key(self.base_url)
        if not self.api_key:
            raise AdsTurboAuthError(NO_KEY_MESSAGE)

    # ---------- transport ----------

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _send(self, path: str, body: bytes, content_type: str, timeout: float) -> tuple[int, dict, str]:
        """POST raw bytes; return (status, headers, text) for every HTTP status, raise only on network errors."""
        request = urllib.request.Request(
            self._url(path),
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": content_type,
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with _OPENER.open(request, timeout=timeout) as resp:
                return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as err:
            return err.code, dict(err.headers or {}), err.read().decode("utf-8", "replace")

    @staticmethod
    def _unwrap(status: int, headers: dict, text: str) -> dict:
        """Turn a raw response into the `ent` payload, or raise a typed error."""
        if status == 401:
            raise AdsTurboAuthError(
                "API key is invalid or expired. Log in again with scripts/login.py "
                "(email + verification code), or check ADSTURBO_API_KEY."
            )
        if 300 <= status < 400:
            # Following a redirect would downgrade POST to GET and surface as a
            # confusing 405. Point at the base URL instead, which is the real cause.
            raise AdsTurboError(
                status,
                f"Base URL redirects to {headers.get('Location', 'elsewhere')!r}. "
                f"Set ADSTURBO_BASE_URL to the final address (default: {DEFAULT_BASE_URL}).",
            )
        if status >= 400:
            raise AdsTurboError(status, f"HTTP {status}: {text[:200] or 'no response body'}")
        try:
            body = json.loads(text)
        except json.JSONDecodeError:
            raise AdsTurboError(-1, f"Malformed response: {text[:200]}") from None

        ret = body.get("ret", 0)
        if ret != 1:
            raise AdsTurboError(ret, body.get("msg") or "unknown error")

        data = body.get("data") or {}
        if isinstance(data, dict):
            return data.get("ent", data)
        return data

    def post(self, path: str, payload: dict | None = None) -> dict:
        """POST a JSON body and return the unwrapped `ent` payload."""
        body = json.dumps(_drop_empty(payload or {}), ensure_ascii=False).encode("utf-8")
        try:
            response = self._send(path, body, "application/json", REQUEST_TIMEOUT)
        except OSError as exc:
            raise AdsTurboError(-1, f"Network error calling {path}: {exc}") from exc
        return self._unwrap(*response)

    def upload(self, path: str, file_path: str | Path) -> dict:
        """POST a multipart file upload and return the unwrapped payload."""
        target = Path(file_path).expanduser()
        if not target.is_file():
            raise AdsTurboError(-1, f"File not found: {target}")
        # The part needs its own Content-Type: storage rejects an empty one
        # outright ("content type len 0").
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        boundary = uuid.uuid4().hex
        # ASCII filename in the header; the server only uses it to guess a missing type.
        filename = target.name if target.name.isascii() else "upload" + target.suffix
        filename = filename.replace('"', "_")
        head = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="data"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
        tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
        try:
            body = head + target.read_bytes() + tail
            response = self._send(path, body, f"multipart/form-data; boundary={boundary}", UPLOAD_TIMEOUT)
        except OSError as exc:
            raise AdsTurboError(-1, f"Network error uploading {target.name}: {exc}") from exc
        return self._unwrap(*response)

    # ---------- async task helpers ----------

    def work_status(self, workspace_id: str) -> dict:
        return self.post(WORK_STATUS_PATH, {"workspace_id": workspace_id})

    def batch_work_status(self, workspace_ids: list[str]) -> dict:
        return self.post(WORK_BATCH_STATUS_PATH, {"workspace_ids": workspace_ids})

    def poll(
        self,
        workspace_id: str,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        interval: float = DEFAULT_POLL_INTERVAL,
        verbose: bool = True,
    ) -> dict:
        """Poll work status until the task reaches a terminal state.

        Raises TimeoutError (task may still be running -- resume with `query`)
        or AdsTurboError when the task itself failed.
        """
        started = time.time()
        while True:
            elapsed = time.time() - started
            if elapsed > timeout:
                raise TimeoutError(
                    f"Still running after {timeout:.0f}s. The task is not lost -- "
                    f"resume with: query --workspace-id {workspace_id}"
                )
            result = self.work_status(workspace_id)
            status = result.get("status", "")
            if status == TERMINAL_OK:
                return result
            if status == TERMINAL_FAIL:
                raise AdsTurboError(-1, result.get("message") or "task failed")
            if verbose:
                print(
                    f"  {status or 'pending'} ... {elapsed:.0f}s elapsed",
                    file=sys.stderr,
                )
            time.sleep(interval)


def _drop_empty(payload: dict) -> dict:
    """Strip keys the caller left unset so the server applies its own defaults."""
    return {
        key: value
        for key, value in payload.items()
        if value is not None and value != [] and value != ""
    }


def emit(result: dict | list) -> None:
    """Print a result as indented JSON on stdout."""
    print(json.dumps(result, ensure_ascii=False, indent=2))


def run_cli(parser, handlers: dict) -> None:
    """Shared entrypoint: dispatch argparse results and render errors readably."""
    args = parser.parse_args()
    command = getattr(args, "command", None)
    if not command:
        parser.print_help()
        sys.exit(1)
    try:
        result = handlers[command](AdsTurboClient(), args)
    except AdsTurboAuthError as exc:
        print(f"Auth failed: {exc.msg}", file=sys.stderr)
        # Structured on stdout too, so the agent can tell the user exactly what to do next.
        emit({"ok": False, "error": "api_key_required", "message": exc.msg, "how_to_get_a_key": API_KEY_STEPS})
        sys.exit(2)
    except AdsTurboError as exc:
        print(f"Request failed: {exc.msg}", file=sys.stderr)
        if exc.code == PLAN_REQUIRED:
            print("This feature needs a Pro plan. Upgrade at https://adsturbo.ai/pricing", file=sys.stderr)
        elif exc.code == SUBSCRIPTION_REQUIRED:
            print("1080p+ video and 4K images need a subscription. Subscribe at https://adsturbo.ai/pricing", file=sys.stderr)
        sys.exit(1)
    except TimeoutError as exc:
        print(f"Timed out: {exc}", file=sys.stderr)
        sys.exit(3)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)
    if result is not None:
        emit(result)


def add_async_flags(sub) -> None:
    """Attach the polling flags every async submit command shares."""
    sub.add_argument("--callback-id", default="", help="your own tracking id, echoed back")
    sub.add_argument("--no-wait", action="store_true", help="submit only, do not poll")
    sub.add_argument("--timeout", type=float, default=DEFAULT_POLL_TIMEOUT)
    sub.add_argument("--interval", type=float, default=DEFAULT_POLL_INTERVAL)


def submit_and_maybe_poll(client: AdsTurboClient, path: str, payload: dict, args) -> dict:
    """Submit an async task, then either return the receipt or poll to completion."""
    receipt = client.post(path, payload)
    workspace_id = receipt.get("workspace_id", "")
    if getattr(args, "no_wait", False) or not workspace_id:
        return receipt
    print(f"  submitted, workspace_id={workspace_id}", file=sys.stderr)
    return client.poll(workspace_id, timeout=args.timeout, interval=args.interval)
