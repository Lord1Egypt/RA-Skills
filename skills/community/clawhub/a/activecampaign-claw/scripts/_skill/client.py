"""ActiveCampaign v3 HTTP client with rate-limit handling and pagination."""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

if sys.version_info < (3, 9):  # noqa: UP036 - friendly error for users running scripts directly
    sys.stderr.write(
        f"ERROR: Python 3.9 or newer required (you have {sys.version_info.major}.{sys.version_info.minor}).\n"
    )
    sys.exit(1)

import urllib.error
import urllib.request
from urllib.parse import urlencode


class ACClientError(Exception):
    """Raised on non-retryable API errors."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class ReadOnlyModeError(Exception):
    """Raised when a write is attempted while AC_READ_ONLY=1 is set."""


class WriteCapExceededError(Exception):
    """Raised when a script tries to perform more writes than AC_MAX_WRITES allows."""


# Audit log lives next to history.jsonl. Importing _skill.state at module load
# would create a tight coupling, so we resolve the path lazily.
_WRITES_LOG_NAME = "writes.jsonl"


def _writes_log_path() -> Path:
    return Path.home() / ".activecampaign-skill" / _WRITES_LOG_NAME


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if raw in ("1", "true", "yes", "on"):
        return True
    if raw in ("0", "false", "no", "off", ""):
        return default
    return default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return max(0, int(raw))
    except ValueError:
        return default


def _hash_payload(data: bytes | None) -> str:
    if not data:
        return ""
    return hashlib.sha256(data).hexdigest()[:16]


def _append_writes_log(entry: dict) -> None:
    """Append a JSON line to the writes audit log. Best-effort — never raises."""
    try:
        path = _writes_log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        # Audit log is best-effort. We don't want to block a write if the
        # filesystem is read-only or the user's home dir is missing.
        pass


class ACClient:
    """ActiveCampaign v3 API client with rate-limit handling, exponential
    backoff, network error resilience, and proactive throttling."""

    MAX_REQUESTS_PER_SEC = 5
    MIN_REQUEST_INTERVAL = 1.0 / MAX_REQUESTS_PER_SEC  # 0.2s between requests

    def __init__(self, base_url: str | None = None, token: str | None = None):
        from _skill.secrets import get_credential
        url = base_url or get_credential("AC_API_URL") or ""
        tok = token or get_credential("AC_API_TOKEN") or ""
        if not url or not tok:
            sys.stderr.write(
                "ERROR: AC_API_URL and AC_API_TOKEN must be set "
                "(as env vars, OS keychain entries, or constructor args).\n"
                "Run `python3 scripts/auth.py status` to see what's configured.\n"
            )
            sys.exit(1)
        if not url.startswith("https://"):
            sys.stderr.write(
                "ERROR: AC_API_URL must use HTTPS. "
                "Sending API tokens over plain HTTP exposes credentials.\n"
            )
            sys.exit(1)
        self.base = url.rstrip("/") + "/api/3"
        self.token = tok
        self._request_count = 0
        self._last_request_time = 0.0
        # Lock for cross-thread throttle correctness when fetch_many() runs
        # multiple endpoint requests concurrently against the same client.
        self._throttle_lock = threading.Lock()
        # Write-safety state. Cap and read-only flag are read at __init__ time
        # so a single process has a fixed budget for its lifetime.
        self._write_count = 0
        self._max_writes = _env_int("AC_MAX_WRITES", 10)
        self._read_only = _env_bool("AC_READ_ONLY")

    def _throttle(self) -> None:
        """Proactive rate limiter — ensures we stay under 5 req/sec.

        Thread-safe: the lock makes spacing correct when multiple threads
        share a client via fetch_many() or any other concurrent caller.
        """
        with self._throttle_lock:
            elapsed = time.monotonic() - self._last_request_time
            if elapsed < self.MIN_REQUEST_INTERVAL:
                time.sleep(self.MIN_REQUEST_INTERVAL - elapsed)
            self._last_request_time = time.monotonic()

    @staticmethod
    def _backoff_delay(attempt: int, base: float = 1.0, cap: float = 60.0) -> float:
        """Exponential backoff with full jitter: random(0, min(cap, base * 2^attempt))."""
        delay = min(cap, base * (2 ** attempt))
        return random.uniform(0, delay)

    def _request(self, method: str, path: str, data: bytes | None = None,
                 params: dict | None = None, max_retries: int = 5) -> dict:
        url = f"{self.base}/{path}"
        if params:
            url += "?" + urlencode(params)
        headers = {
            "Api-Token": self.token,
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(url, method=method, headers=headers, data=data)

        retryable_http_codes = {429, 500, 502, 503, 504}
        last_error: Exception | None = None

        for attempt in range(max_retries):
            self._throttle()
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    self._request_count += 1
                    body = resp.read()
                    if not body:
                        return {}
                    return json.loads(body)

            except urllib.error.HTTPError as e:
                last_error = e
                if e.code == 429:
                    retry_after = int(e.headers.get("Retry-After", "0"))
                    delay = max(retry_after, self._backoff_delay(attempt))
                    sys.stderr.write(
                        f"  ⚠ Rate limited on {path}. "
                        f"Retry {attempt + 1}/{max_retries} in {delay:.1f}s\n"
                    )
                    time.sleep(delay)
                    continue
                if e.code in retryable_http_codes:
                    delay = self._backoff_delay(attempt)
                    sys.stderr.write(
                        f"  ⚠ Server error {e.code} on {path}. "
                        f"Retry {attempt + 1}/{max_retries} in {delay:.1f}s\n"
                    )
                    time.sleep(delay)
                    continue
                if e.code == 422:
                    body = e.read().decode("utf-8", errors="replace")
                    raise ACClientError(422, body) from e
                if e.code in (401, 403):
                    raise ACClientError(
                        e.code,
                        "Authentication failed. Check AC_API_URL and AC_API_TOKEN.",
                    ) from e
                if e.code == 404:
                    raise ACClientError(404, f"Resource not found: {path}") from e
                raise ACClientError(e.code, str(e)) from e

            except urllib.error.URLError as e:
                last_error = e
                delay = self._backoff_delay(attempt, base=2.0)
                sys.stderr.write(
                    f"  ⚠ Network error on {path}: {e.reason}. "
                    f"Retry {attempt + 1}/{max_retries} in {delay:.1f}s\n"
                )
                time.sleep(delay)
                continue

            except (TimeoutError, OSError) as e:
                last_error = e
                delay = self._backoff_delay(attempt, base=2.0)
                sys.stderr.write(
                    f"  ⚠ Timeout/connection error on {path}. "
                    f"Retry {attempt + 1}/{max_retries} in {delay:.1f}s\n"
                )
                time.sleep(delay)
                continue

        if isinstance(last_error, urllib.error.HTTPError):
            raise ACClientError(
                last_error.code,
                f"Exceeded {max_retries} retries on {path} (last: HTTP {last_error.code})",
            )
        raise ACClientError(
            0,
            f"Exceeded {max_retries} retries on {path} "
            f"(last error: {last_error})",
        )

    def get(self, path: str, params: dict | None = None) -> dict:
        return self._request("GET", path, params=params)

    def _check_write_allowed(self, method: str, path: str) -> None:
        """Enforce read-only mode + per-process write cap.

        Read-only mode raises immediately. The cap raises when the *next*
        write would exceed the limit, so callers know they were on the edge.
        """
        if self._read_only:
            raise ReadOnlyModeError(
                f"AC_READ_ONLY=1 is set — refusing {method} {path}. "
                f"Unset the env var to allow modifications."
            )
        if self._write_count >= self._max_writes:
            raise WriteCapExceededError(
                f"Per-process write cap reached "
                f"({self._write_count}/{self._max_writes}). "
                f"Re-run the script if this was intended, or raise the cap "
                f"with AC_MAX_WRITES=<n>."
            )

    def write(self, method: str, path: str, payload: dict | None = None) -> dict:
        """Single audited write path for POST / PUT / DELETE.

        Enforces:
          - `AC_READ_ONLY=1` short-circuits (no request goes out).
          - Per-process cap (`AC_MAX_WRITES`, default 10).
          - Best-effort audit line written to ~/.activecampaign-skill/writes.jsonl
            with endpoint, method, payload hash (NOT payload), and timestamp.
        """
        if method not in {"POST", "PUT", "DELETE"}:
            raise ValueError(f"write() called with non-write method {method!r}")
        self._check_write_allowed(method, path)

        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        _append_writes_log({
            "ts": datetime.now(timezone.utc).isoformat(),
            "method": method,
            "path": path,
            "payload_sha256_16": _hash_payload(data),
            "script": Path(sys.argv[0]).name if sys.argv else "",
            "write_seq": self._write_count + 1,
        })
        self._write_count += 1
        return self._request(method, path, data=data)

    def post(self, path: str, payload: dict) -> dict:
        return self.write("POST", path, payload)

    def put(self, path: str, payload: dict) -> dict:
        return self.write("PUT", path, payload)

    def delete(self, path: str) -> dict:
        return self.write("DELETE", path, None)

    def stream(self, path: str, key: str, params: dict | None = None,
               limit_per_page: int = 100, max_items: int | None = None):
        """Yield records from a paginated endpoint one at a time."""
        params = dict(params or {})
        params["limit"] = limit_per_page
        offset = 0
        yielded = 0
        while max_items is None or yielded < max_items:
            params["offset"] = offset
            resp = self.get(path, params)
            chunk = resp.get(key, [])
            if not chunk:
                break
            for record in chunk:
                yield record
                yielded += 1
                if max_items is not None and yielded >= max_items:
                    return
            if len(chunk) < limit_per_page:
                break
            offset += limit_per_page
            time.sleep(0.25)

    def paginate(self, path: str, key: str, params: dict | None = None,
                 limit_per_page: int = 100, max_items: int = 5000) -> list:
        return list(self.stream(path, key, params, limit_per_page, max_items))

    def fetch_many(
        self,
        requests: list[tuple[str, str, dict | None, int]],
        max_workers: int = 4,
    ) -> dict[str, list]:
        """Concurrently paginate multiple endpoints, respecting rate limits.

        `requests` is a list of `(label, path, params, max_items)` tuples.
        Returns `{label: list_of_records}`. On error, the value is
        `{"error": "...", "status_code": N}` for that label only — other
        endpoints continue.

        Thread safety: the shared client's `_throttle_lock` serializes
        outgoing requests at 5/sec total, so concurrency wins come from
        overlapping request preparation + parsing, not from breaking the
        rate limit. The default 4-worker pool is conservative.
        """
        results: dict = {}

        def _one(label: str, path: str, params: dict | None, max_items: int) -> tuple[str, object]:
            try:
                key = label  # AC v3 collection responses key on the resource name
                # If label != key (rare), the caller can post-process.
                records = self.paginate(path, key, params=params, max_items=max_items)
                return label, records
            except ACClientError as e:
                return label, {"error": str(e), "status_code": e.status_code}
            except Exception as e:  # noqa: BLE001 — best-effort one-of-many
                return label, {"error": str(e), "status_code": 0}

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [pool.submit(_one, label, path, params, max_items)
                       for (label, path, params, max_items) in requests]
            for fut in as_completed(futures):
                label, value = fut.result()
                results[label] = value
        return results

    def fetch_engagement_events(self, max_items: int = 30000, quiet: bool = False) -> list:
        """Return a normalized list of engagement events.

        Tries /messageActivities first (full open + click event log on plans
        that expose it). On 404 falls back to /linkData (clicks only) so
        click-driven analysis still works on accounts without messageActivities.
        """
        try:
            raw = self.paginate("messageActivities", "messageActivities", max_items=max_items)
            return [
                {
                    "event": (e.get("event") or "").lower(),
                    "contact": str(e.get("contact")) if e.get("contact") else None,
                    "tstamp": e.get("tstamp"),
                    "campaign": str(e.get("campaign")) if e.get("campaign") else None,
                    "email": e.get("email"),
                }
                for e in raw
            ]
        except ACClientError as e:
            if e.status_code != 404:
                raise
        if not quiet:
            sys.stderr.write(
                "NOTE: AC plan doesn't expose /messageActivities — "
                "falling back to /linkData (click events only, no open events).\n"
            )
        raw = self.paginate("linkData", "linkData", max_items=max_items)
        return [
            {
                "event": "click",
                "contact": str(d.get("contact")) if d.get("contact") else None,
                "tstamp": d.get("tstamp"),
                "campaign": str(d.get("campaign")) if d.get("campaign") else None,
                "link": str(d.get("link")) if d.get("link") else None,
                "email": d.get("email"),
            }
            for d in raw
        ]
