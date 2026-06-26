#!/usr/bin/env python3
"""
Fetch Twitter/X posts from KOL accounts using X API.

Reads sources.json, filters Twitter sources, fetches recent posts using
either the official X API v2 or twitterapi.io, and outputs structured JSON.

Usage:
    python3 fetch-twitter.py [--config CONFIG_DIR] [--hours 24] [--output FILE] [--verbose]
    python3 fetch-twitter.py --backend twitterapiio  # force twitterapi.io backend

Environment:
    TWITTER_API_BACKEND - Backend selection: "auto" (default), "getxapi", "twitterapiio", or "official"
                        Auto priority: getxapi ($0.001/call) > twitterapi.io (~$5/mo) > official X API
    OPENCLI_MAX_WORKERS  - OpenCLI fetch concurrency for twitter tweets (1-10, default: 10)
    OPENCLI_AUTO_UPDATE  - Enable OpenCLI automatic update check (default: 1/true)
    OPENCLI_NO_UPDATE    - Disable OpenCLI automatic update for this run/environment (0/1)
    OPENCLI_UPDATE_COMMAND - Override OpenCLI update command, e.g. "self-update" or "update --yes"
    OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS - Minimum seconds between checks (default: 86400)
    OPENCLI_MIN_VERSION - Minimum supported OpenCLI version (default: 1.7.22)
    GETX_API_KEY        - GetXAPI API key (preferred backend, $0.001 per call)
    TWITTERAPI_IO_KEY   - twitterapi.io API key (alternative backend, ~$5/month)
    X_BEARER_TOKEN      - Twitter/X official API v2 bearer token (fallback)
"""

import json
import sys
import os
import argparse
import logging
import time
import tempfile
import re
import threading
import subprocess
import shutil
import hashlib
import shlex
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable

TIMEOUT = 30
MAX_WORKERS = 5  # Lower for API rate limits
RETRY_COUNT = 2
RETRY_DELAY = 2.0
MAX_TWEETS_PER_USER = 20
OPENCLI_TIMEOUT = 90
OPENCLI_TAB_COMMAND_TIMEOUT = 15
OPENCLI_DEFAULT_MAX_WORKERS = 10
OPENCLI_MAX_WORKERS_MAX = 10
OPENCLI_CLOSE_TABS_AFTER_RUN_DEFAULT = True
OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN_DEFAULT = True
OPENCLI_BROWSER_RECOVERABLE_RETRIES = 1
OPENCLI_AUTO_UPDATE_DEFAULT = True
OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS = 24 * 60 * 60
OPENCLI_UPDATE_COMMAND_CANDIDATES = ("self-update", "update", "upgrade")
OPENCLI_DEFAULT_MIN_VERSION = "1.7.22"
OPENCLI_UPDATE_ALREADY_UP_TO_DATE_MARKERS = (
    "already up to date",
    "already up-to-date",
    "already latest",
    "no updates available",
    "nothing to update",
)
OPENCLI_GLOBAL_ERROR_CODES = {
    "opencli_missing",
    "opencli_capability_missing",
    "opencli_browser_unavailable",
    "opencli_auth_required",
    "opencli_timeout",
    "opencli_parse_error",
}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_X_CACHE_DIR = PROJECT_ROOT / ".cache" / "x"
ID_CACHE_PATH = DEFAULT_X_CACHE_DIR / "user_ids.json"
ID_CACHE_TTL_DAYS = 7
X_CACHE_RETENTION_DAYS = 30
X_CACHE_MAX_BYTES = 512 * 1024 * 1024
X_CACHE_MAX_ENTRY_BYTES = 5 * 1024 * 1024
X_TIMELINE_CACHE_TTL_SECONDS = 5 * 60
X_PRIORITY_TIMELINE_CACHE_TTL_SECONDS = 5 * 60
X_REGULAR_TIMELINE_CACHE_TTL_SECONDS = 30 * 60
X_RATE_LIMIT_FALLBACK_SECONDS = 60
X_RESPONSE_CACHE_TTL_SECONDS = X_CACHE_RETENTION_DAYS * 86400

# Twitter API v2 endpoints
OFFICIAL_API_BASE = "https://api.x.com/2"
USER_LOOKUP_ENDPOINT = f"{OFFICIAL_API_BASE}/users/by"

# twitterapi.io endpoints
TWITTERAPIIO_BASE = "https://api.twitterapi.io"
GETXAPI_BASE = "https://api.getxapi.com"

CHROME_WINDOW_SNAPSHOT_SCRIPT = r'''
tell application "Google Chrome"
  if it is not running then return ""
  set rows to {}
  repeat with chromeWindow in windows
    set tabUrls to {}
    repeat with chromeTab in tabs of chromeWindow
      set end of tabUrls to URL of chromeTab
    end repeat
    set oldDelimiters to AppleScript's text item delimiters
    set AppleScript's text item delimiters to " ||| "
    set urlText to tabUrls as text
    set AppleScript's text item delimiters to oldDelimiters
    set end of rows to ((id of chromeWindow as text) & (character id 9) & urlText)
  end repeat
  set oldDelimiters to AppleScript's text item delimiters
  set AppleScript's text item delimiters to linefeed
  set outputText to rows as text
  set AppleScript's text item delimiters to oldDelimiters
  return outputText
end tell
'''

CHROME_WINDOW_CLOSE_SCRIPT = r'''
on run argv
  tell application "Google Chrome"
    if it is not running then return "Chrome not running"
    repeat with rawWindowId in argv
      try
        repeat with chromeWindow in windows
          if (id of chromeWindow as text) is (rawWindowId as text) then
            close chromeWindow
            exit repeat
          end if
        end repeat
      end try
    end repeat
  end tell
end run
'''


def setup_logging(verbose: bool) -> logging.Logger:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def clean_tweet_text(text: str) -> str:
    """Clean tweet text for better display."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Truncate if too long
    if len(text) > 280:
        text = text[:277] + "..."
    return text


class OpenCliBackendError(RuntimeError):
    """Error raised when OpenCLI cannot be used as a backend."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _parse_opencli_date(date_str: str) -> Optional[datetime]:
    """Parse OpenCLI Twitter date formats into an aware datetime."""
    if not date_str:
        return None

    value = str(date_str).strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        pass

    for fmt in ("%a %b %d %H:%M:%S %z %Y", "%Y-%m-%d %H:%M:%S"):
        try:
            parsed = datetime.strptime(str(date_str), fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except ValueError:
            continue

    logging.debug(f"Failed to parse OpenCLI date: {date_str}")
    return None


def _as_int(value: Any) -> int:
    """Best-effort conversion for OpenCLI metric fields."""
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def extract_opencli_tweet_records(payload: Any) -> List[Dict[str, Any]]:
    """Extract tweet records from common OpenCLI JSON output envelopes."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if not isinstance(payload, dict):
        return []

    for key in ("tweets", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    data = payload.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return extract_opencli_tweet_records(data)

    return []


def extract_opencli_browser_tabs(payload: Any) -> Dict[str, str]:
    """Extract browser tab target IDs and URLs from OpenCLI tab-list JSON."""
    if isinstance(payload, list):
        tabs = {}
        for item in payload:
            tabs.update(extract_opencli_browser_tabs(item))
        return tabs

    if isinstance(payload, dict):
        target_id = payload.get("targetId") or payload.get("target_id") or payload.get("page") or payload.get("id")
        if target_id:
            url = payload.get("url") or payload.get("href") or payload.get("location") or ""
            return {str(target_id): str(url)}

        tabs = {}
        for key in ("tabs", "items", "data", "targets"):
            if key in payload:
                tabs.update(extract_opencli_browser_tabs(payload[key]))
        return tabs

    return {}


def is_twitter_browser_tab(url: str) -> bool:
    """Return true for X/Twitter browser tabs created by OpenCLI."""
    value = (url or "").lower()
    return value.startswith(("https://x.com/", "https://twitter.com/", "https://mobile.twitter.com/"))


def parse_chrome_window_snapshot(raw_value: str) -> Dict[str, List[str]]:
    """Parse Chrome window snapshots emitted by the AppleScript helper."""
    windows: Dict[str, List[str]] = {}
    for line in (raw_value or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if "\t" in line:
            window_id, urls = line.split("\t", 1)
        elif "tab" in line:
            window_id, urls = line.split("tab", 1)
        else:
            continue
        window_id = window_id.strip()
        if not window_id:
            continue
        windows[window_id] = [url.strip() for url in urls.split(" ||| ") if url.strip()]
    return windows


def is_opencli_chrome_window(urls: List[str]) -> bool:
    """Return true for Chrome windows that look like OpenCLI automation leftovers."""
    if not urls:
        return False
    automation_urls = {"about:blank", "chrome://newtab/"}
    for url in urls:
        value = (url or "").lower()
        if value in automation_urls:
            continue
        if is_twitter_browser_tab(value):
            continue
        return False
    return True


def normalize_opencli_tweet(
    record: Dict[str, Any],
    source: Dict[str, Any],
    cutoff: datetime,
) -> Optional[Dict[str, Any]]:
    """Normalize one OpenCLI tweet into the existing Twitter article shape."""
    tweet_id = str(record.get("id") or record.get("tweet_id") or "").strip()
    text = str(record.get("text") or record.get("full_text") or "").strip()
    created_at = _parse_opencli_date(record.get("created_at") or record.get("date") or "")

    if not tweet_id or not text or not created_at:
        return None
    if created_at < cutoff:
        return None
    if record.get("is_retweet") or text.startswith("RT @"):
        return None

    handle = source["handle"].lstrip("@")
    link = record.get("url") or record.get("link") or f"https://x.com/{handle}/status/{tweet_id}"

    return {
        "title": clean_tweet_text(text),
        "link": link,
        "date": created_at.isoformat(),
        "topics": source["topics"][:],
        "metrics": {
            "like_count": _as_int(record.get("likes") or record.get("like_count")),
            "retweet_count": _as_int(record.get("retweets") or record.get("retweet_count")),
            "reply_count": _as_int(record.get("replies") or record.get("reply_count")),
            "quote_count": _as_int(record.get("quotes") or record.get("quote_count")),
            "impression_count": _as_int(record.get("views") or record.get("impression_count")),
        },
        "tweet_id": tweet_id,
    }


def resolve_opencli_bin() -> str:
    """Resolve the OpenCLI executable from OPENCLI_BIN or PATH."""
    configured = os.getenv("OPENCLI_BIN")
    if configured:
        return configured

    found = shutil.which("opencli")
    if found:
        return found

    raise OpenCliBackendError(
        "opencli_missing",
        "OpenCLI executable not found. Set OPENCLI_BIN or install opencli on PATH.",
    )


def _parse_opencli_version(value: str) -> Optional[List[int]]:
    """Extract a semantic version tuple from an OpenCLI version string."""
    match = re.search(r"\bv?(\d+)\.(\d+)(?:\.(\d+))?\b", value or "")
    if not match:
        return None

    return [
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3) or 0),
    ]


def _min_opencli_version() -> List[int]:
    raw_value = os.getenv("OPENCLI_MIN_VERSION", OPENCLI_DEFAULT_MIN_VERSION).strip()
    parsed = _parse_opencli_version(raw_value)
    if parsed:
        return parsed

    logging.warning(
        "Invalid OPENCLI_MIN_VERSION=%r; using default %s",
        raw_value,
        OPENCLI_DEFAULT_MIN_VERSION,
    )
    return _parse_opencli_version(OPENCLI_DEFAULT_MIN_VERSION) or [0, 0, 0]


def _opencli_version_str(version: List[int]) -> str:
    """Format an OpenCLI version tuple as a dotted string."""
    return ".".join(str(item) for item in version)


def _run_opencli_version_command(binary: str, args: List[str], timeout: int = 10) -> subprocess.CompletedProcess:
    """Run one OpenCLI version command without raising."""
    try:
        return subprocess.run(
            [binary] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=[binary] + args,
            returncode=75,
            stdout="",
            stderr=f"OpenCLI version check timed out: {exc}",
        )
    except Exception as exc:  # pragma: no cover - defensive
        return subprocess.CompletedProcess(
            args=[binary] + args,
            returncode=1,
            stdout="",
            stderr=str(exc),
        )


def _get_opencli_version(binary: str) -> Optional[str]:
    """Probe OpenCLI version from common CLI flags."""
    for args in (["--version"], ["version"], ["-v"], ["-V"]):
        result = _run_opencli_version_command(binary, args, timeout=10)
        if result.returncode != 0:
            continue
        version_text = f"{result.stdout}\n{result.stderr}".strip()
        parsed = _parse_opencli_version(version_text)
        if parsed is None:
            continue
        return _opencli_version_str(parsed)

    return None


def _ensure_opencli_min_version(binary: str) -> None:
    """Verify that installed OpenCLI meets the minimum required version."""
    minimum = _min_opencli_version()
    current = _get_opencli_version(binary)
    minimum_text = _opencli_version_str(minimum)
    if current is None:
        raise OpenCliBackendError(
            "opencli_version_unknown",
            f"Could not determine OpenCLI version. Install OpenCLI {minimum_text} or later.",
        )

    current_tuple = _parse_opencli_version(current)
    if current_tuple is None:
        raise OpenCliBackendError(
            "opencli_version_unknown",
            "Could not parse OpenCLI version output.",
        )

    if current_tuple < minimum:
        raise OpenCliBackendError(
            "opencli_version_too_old",
            f"OpenCLI is too old (current={current}); upgrade to {minimum_text} or later.",
        )


def _is_opencli_below_min_version(binary: str) -> bool:
    """Return true when OpenCLI has a known version below the minimum."""
    current = _get_opencli_version(binary)
    current_tuple = _parse_opencli_version(current or "")
    return current_tuple is not None and current_tuple < _min_opencli_version()


def _env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable."""
    raw = os.getenv(name)
    if raw is None:
        return default

    return raw.strip().lower() not in {"", "0", "false", "off", "no", "disabled"}


def _opencli_auto_update_enabled() -> bool:
    """Return whether automatic OpenCLI update is enabled."""
    if not _env_bool("OPENCLI_AUTO_UPDATE", OPENCLI_AUTO_UPDATE_DEFAULT):
        return False
    if _env_bool("OPENCLI_NO_UPDATE", False):
        return False
    return True


def _get_opencli_update_interval_seconds() -> int:
    """Get update-throttle interval in seconds."""
    raw = os.getenv("OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS")
    if not raw:
        return OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS

    try:
        value = int(raw.strip())
    except ValueError:
        logging.warning(
            "Invalid OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS=%r; using %s",
            raw,
            OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS,
        )
        return OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS

    if value <= 0:
        return OPENCLI_UPDATE_CHECK_INTERVAL_SECONDS
    return value


def _opencli_update_state_path() -> Path:
    """Path used to remember when the last update attempt happened."""
    cache_root = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    return Path(cache_root) / "follow-news" / "opencli-update-state.json"


def _is_opencli_update_due(state_path: Path, interval_seconds: int) -> bool:
    """Return True when an update check should be retried."""
    if not state_path.exists():
        return True
    try:
        return (time.time() - state_path.stat().st_mtime) >= interval_seconds
    except OSError:
        return True


def _record_opencli_update_state(state_path: Path, status: str, details: Dict[str, Any]) -> None:
    """Persist last OpenCLI update attempt metadata."""
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "last_attempt": int(time.time()),
            "status": status,
            **details,
        }
        state_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:  # pragma: no cover - best effort
        logging.debug("Failed to persist OpenCLI update state: %s", exc)


def _parse_opencli_update_command_spec() -> List[List[str]]:
    """Resolve candidate update commands from environment."""
    explicit = os.getenv("OPENCLI_UPDATE_COMMAND", "").strip()
    if explicit:
        try:
            parts = shlex.split(explicit)
        except ValueError:
            parts = explicit.split()
        if parts:
            return [parts]
        return []

    return [[command] for command in OPENCLI_UPDATE_COMMAND_CANDIDATES]


def _looks_like_unsupported_opencli_command(stderr: str, stdout: str) -> bool:
    text = f"{stderr or ''} {stdout or ''}".lower()
    return any(
        marker in text
        for marker in (
            "unknown command",
            "unknown subcommand",
            "no such command",
        )
    )


def _looks_like_unknown_update_flag(stderr: str, stdout: str) -> bool:
    text = f"{stderr or ''} {stdout or ''}".lower()
    return "unknown argument" in text or "unrecognized args" in text or "unknown option" in text


def _looks_like_already_latest(stderr: str, stdout: str) -> bool:
    text = f"{stderr or ''} {stdout or ''}".lower()
    return any(marker in text for marker in OPENCLI_UPDATE_ALREADY_UP_TO_DATE_MARKERS)


def _extract_snippet(text: str, limit: int = 200) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else f"{text[:limit - 3]}..."


def _run_opencli_update_command(binary: str, args: List[str], timeout: int = 120) -> subprocess.CompletedProcess:
    """Run one OpenCLI update command variant."""
    try:
        return subprocess.run(
            [binary] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=[binary] + args,
            returncode=75,
            stdout="",
            stderr=f"OpenCLI update command timed out: {exc}",
        )
    except Exception as exc:  # pragma: no cover - defensive
        return subprocess.CompletedProcess(
            args=[binary] + args,
            returncode=1,
            stdout="",
            stderr=str(exc),
        )


def _ensure_opencli_latest(binary: str, force: bool = False) -> Dict[str, Any]:
    """Optionally check for and apply OpenCLI updates.

    Returns a structured result suitable for logging. This helper never raises.
    """
    result: Dict[str, Any] = {"status": "skipped", "command": None, "message": ""}
    if not _opencli_auto_update_enabled():
        result["message"] = "OpenCLI auto-update is disabled."
        return result

    state_path = _opencli_update_state_path()
    interval_seconds = _get_opencli_update_interval_seconds()
    if not force and not _is_opencli_update_due(state_path, interval_seconds):
        result["status"] = "throttled"
        result["message"] = f"OpenCLI update check throttled to every {interval_seconds}s."
        return result

    candidates = _parse_opencli_update_command_spec()
    if not candidates:
        result["status"] = "unsupported"
        result["message"] = "No OpenCLI update command candidate is configured."
        _record_opencli_update_state(state_path, result["status"], result)
        return result

    command_attempts: List[Dict[str, Any]] = []
    for candidate in candidates:
        arg_variants: List[List[str]] = [candidate]
        if "--yes" not in candidate:
            arg_variants.append(candidate + ["--yes"])
        if "-y" not in candidate:
            arg_variants.append(candidate + ["-y"])

        for variant_index, args in enumerate(arg_variants):
            cp = _run_opencli_update_command(binary, args)
            output = {
                "command": [binary] + args,
                "returncode": cp.returncode,
                "stdout": _extract_snippet(cp.stdout or "", 220),
                "stderr": _extract_snippet(cp.stderr or "", 220),
            }
            command_attempts.append(output)
            combined_stderr = cp.stderr or ""
            combined_stdout = cp.stdout or ""
            has_more_variants = variant_index < len(arg_variants) - 1

            if cp.returncode == 0:
                if _looks_like_already_latest(combined_stderr, combined_stdout):
                    result["status"] = "already_latest"
                    result["message"] = f"OpenCLI already on latest version ({' '.join(output['command'])})."
                else:
                    result["status"] = "updated"
                    result["message"] = f"OpenCLI updated successfully via {' '.join(output['command'])}."
                result["command"] = " ".join(output["command"])
                result["attempts"] = command_attempts
                _record_opencli_update_state(state_path, result["status"], result)
                return result

            if _looks_like_already_latest(combined_stderr, combined_stdout):
                result["status"] = "already_latest"
                result["message"] = "OpenCLI reports already on latest version."
                result["command"] = " ".join(output["command"])
                result["attempts"] = command_attempts
                _record_opencli_update_state(state_path, result["status"], result)
                return result

            if _looks_like_unknown_update_flag(combined_stderr, combined_stdout):
                if has_more_variants:
                    continue
                result["status"] = "failed"
                result["message"] = output["stderr"] or output["stdout"] or "OpenCLI update failed."
                result["command"] = " ".join(output["command"])
                result["attempts"] = command_attempts
                _record_opencli_update_state(state_path, result["status"], result)
                return result

            if _looks_like_unsupported_opencli_command(combined_stderr, combined_stdout):
                break

            if has_more_variants:
                continue

            result["status"] = "failed"
            result["message"] = output["stderr"] or output["stdout"] or "OpenCLI update failed."
            result["command"] = " ".join(output["command"])
            result["attempts"] = command_attempts
            _record_opencli_update_state(state_path, result["status"], result)
            return result

    result["status"] = "unsupported"
    result["message"] = "No usable OpenCLI update sub-command was found."
    result["attempts"] = command_attempts
    _record_opencli_update_state(state_path, result["status"], result)
    return result


def opencli_has_twitter_tweets(payload: Any) -> bool:
    """Return true when `opencli list -f json` exposes twitter tweets."""
    if isinstance(payload, list):
        for item in payload:
            if opencli_has_twitter_tweets(item):
                return True
        return False

    if isinstance(payload, str):
        value = " ".join(payload.lower().strip().split())
        return value in {"twitter tweets", "opencli twitter tweets"}

    if isinstance(payload, dict):
        site = str(payload.get("site") or payload.get("group") or "").lower()
        name = str(payload.get("name") or payload.get("command") or "").lower()
        command = " ".join(name.strip().split())
        if site == "twitter" and command == "tweets":
            return True
        if command in {"twitter tweets", "opencli twitter tweets"}:
            return True

        if "twitter" in payload:
            twitter_value = payload["twitter"]
            if isinstance(twitter_value, list):
                return "tweets" in [str(item).lower() for item in twitter_value]
            if isinstance(twitter_value, dict):
                return opencli_has_twitter_tweets(twitter_value)

        for key in ("commands", "items", "data", "sites"):
            if key in payload and opencli_has_twitter_tweets(payload[key]):
                return True

    return False


def get_backend_order(backend_name: str) -> List[str]:
    """Return backend candidates in the order they should be attempted."""
    if backend_name == "auto":
        return ["opencli", "getxapi", "twitterapiio", "official"]
    return [backend_name]


def get_opencli_max_workers(raw_value: Optional[str] = None) -> int:
    """Return OpenCLI worker count, defaulting to parallel browser access."""
    if raw_value is None:
        raw_value = os.getenv("OPENCLI_MAX_WORKERS", "").strip()
    else:
        raw_value = str(raw_value).strip()

    if not raw_value:
        return OPENCLI_DEFAULT_MAX_WORKERS

    try:
        value = int(raw_value)
    except ValueError:
        logging.warning("Invalid OPENCLI_MAX_WORKERS=%r; using %s", raw_value, OPENCLI_DEFAULT_MAX_WORKERS)
        return OPENCLI_DEFAULT_MAX_WORKERS

    if value < 1:
        logging.warning("Invalid OPENCLI_MAX_WORKERS=%r; using %s", raw_value, OPENCLI_DEFAULT_MAX_WORKERS)
        return OPENCLI_DEFAULT_MAX_WORKERS
    if value > OPENCLI_MAX_WORKERS_MAX:
        logging.warning(
            "OPENCLI_MAX_WORKERS=%r exceeds max (%s); clamping to %s",
            raw_value,
            OPENCLI_MAX_WORKERS_MAX,
            OPENCLI_MAX_WORKERS_MAX,
        )
        return OPENCLI_MAX_WORKERS_MAX

    return value


def get_opencli_close_tabs_after_run() -> bool:
    """Return whether OpenCLI-created Twitter tabs should be closed after fetch."""
    raw_value = os.getenv("OPENCLI_CLOSE_TABS_AFTER_RUN", "").strip().lower()
    if not raw_value:
        return OPENCLI_CLOSE_TABS_AFTER_RUN_DEFAULT
    return raw_value not in {"0", "false", "no", "off"}


def get_opencli_close_chrome_windows_after_run() -> bool:
    """Return whether OpenCLI-created Chrome windows should be closed after fetch."""
    raw_value = os.getenv("OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN", "").strip().lower()
    if not raw_value:
        return OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN_DEFAULT
    return raw_value not in {"0", "false", "no", "off"}


def snapshot_chrome_windows() -> Optional[Dict[str, List[str]]]:
    """Return a best-effort snapshot of Chrome windows on macOS."""
    if not get_opencli_close_chrome_windows_after_run():
        return None
    if sys.platform != "darwin" or not shutil.which("osascript"):
        return None

    result = subprocess.run(
        ["osascript", "-e", CHROME_WINDOW_SNAPSHOT_SCRIPT],
        capture_output=True,
        text=True,
        timeout=OPENCLI_TAB_COMMAND_TIMEOUT,
    )
    if result.returncode != 0:
        logging.warning("Chrome window snapshot failed: %s", (result.stderr or result.stdout).strip()[:200])
        return None
    return parse_chrome_window_snapshot(result.stdout)


def close_chrome_windows(window_ids: List[str]) -> None:
    """Close Chrome windows by id on macOS."""
    if not window_ids or sys.platform != "darwin" or not shutil.which("osascript"):
        return

    result = subprocess.run(
        ["osascript", "-e", CHROME_WINDOW_CLOSE_SCRIPT] + window_ids,
        capture_output=True,
        text=True,
        timeout=OPENCLI_TAB_COMMAND_TIMEOUT,
    )
    if result.returncode != 0:
        logging.warning("Chrome window close failed: %s", (result.stderr or result.stdout).strip()[:200])


def cleanup_new_opencli_chrome_windows(before_windows: Optional[Dict[str, List[str]]]) -> None:
    """Close Chrome automation windows created during the OpenCLI fetch."""
    if before_windows is None:
        return

    closed_any = False
    for _ in range(6):
        time.sleep(0.5)
        after_windows = snapshot_chrome_windows()
        if after_windows is None:
            return

        new_window_ids = [
            window_id
            for window_id, urls in after_windows.items()
            if window_id not in before_windows and is_opencli_chrome_window(urls)
        ]
        if new_window_ids:
            close_chrome_windows(new_window_ids)
            closed_any = True
            continue
        if closed_any:
            return


def build_twitter_skipped_reason(backend_name: str, diagnostics: List[Dict[str, str]]) -> str:
    """Build a human-readable reason for an empty Twitter output."""
    opencli_diag = next((item for item in diagnostics if item.get("backend") == "opencli"), None)
    unavailable = {item.get("backend") for item in diagnostics if item.get("code") == "backend_unavailable"}

    parts = []
    if opencli_diag:
        message = opencli_diag.get("message", "").strip()
        if len(message) > 160:
            message = message[:157] + "..."
        detail = opencli_diag.get("code", "unknown")
        if message:
            detail = f"{detail}: {message}"
        parts.append(f"OpenCLI failed first ({detail})")

    missing = []
    if "getxapi" in unavailable:
        missing.append("GETX_API_KEY")
    if "twitterapiio" in unavailable:
        missing.append("twitterapi.io/TWITTERAPI_IO_KEY")
    if "official" in unavailable:
        missing.append("official X API/X_BEARER_TOKEN")

    if missing:
        parts.append("API fallbacks unavailable: " + ", ".join(missing))

    if parts:
        return "; ".join(parts)

    return f"No usable backend for '{backend_name}'"


def _classify_opencli_failure(returncode: int, stderr: str = "", stdout: str = "") -> str:
    """Map OpenCLI process failures into stable backend error codes."""
    text = f"{stderr or ''} {stdout or ''}".lower()
    if returncode == 69:
        return "opencli_browser_unavailable"
    if returncode == 75:
        return "opencli_timeout"
    if returncode == 77:
        return "opencli_auth_required"
    if "not logged" in text or "auth" in text or "permission" in text:
        return "opencli_auth_required"
    if "no tab with id" in text or ("securityerror" in text and "pushstate" in text):
        return "opencli_browser_unavailable"
    if "browser" in text and ("unavailable" in text or "connect" in text):
        return "opencli_browser_unavailable"
    return "opencli_source_error"


def _is_retriable_opencli_error(error_code: str) -> bool:
    """Return true when OpenCLI failure should be retried once before fallback."""
    return error_code == "opencli_browser_unavailable"


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

class RateLimiter:
    """Simple token-bucket rate limiter."""
    def __init__(self, qps: float):
        self._lock = threading.Lock()
        self._min_interval = 1.0 / qps
        self._last = 0.0

    def wait(self):
        with self._lock:
            now = time.monotonic()
            wait_time = self._min_interval - (now - self._last)
            if wait_time > 0:
                time.sleep(wait_time)
            self._last = time.monotonic()


class XRateLimitDeferred(RuntimeError):
    """Raised when a backend endpoint must wait for its rate-limit reset."""

    def __init__(self, deferred_until: float):
        super().__init__(f"Rate limit deferred until {int(deferred_until)}")
        self.deferred_until = deferred_until


def get_x_cache_dir() -> Path:
    """Return the project-local X cache directory."""
    configured = os.getenv("X_CACHE_DIR", "").strip()
    if configured:
        return Path(configured).expanduser()
    return DEFAULT_X_CACHE_DIR


def get_x_id_cache_path() -> Path:
    """Return the project-local username to user-id cache path."""
    return get_x_cache_dir() / "user_ids.json"


def get_env_int(name: str, default: int, minimum: int = 0) -> int:
    """Return a bounded integer environment value."""
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default
    try:
        value = int(raw_value)
    except ValueError:
        logging.warning("Invalid %s=%r; using %s", name, raw_value, default)
        return default
    if value < minimum:
        logging.warning("Invalid %s=%r; using %s", name, raw_value, default)
        return default
    return value


def get_x_cache_retention_seconds() -> int:
    """Return response cache retention in seconds."""
    days = get_env_int("X_CACHE_RETENTION_DAYS", X_CACHE_RETENTION_DAYS, minimum=1)
    return days * 86400


def get_x_cache_max_bytes() -> int:
    """Return the total response cache byte budget."""
    return get_env_int("X_CACHE_MAX_BYTES", X_CACHE_MAX_BYTES, minimum=1)


def get_x_cache_max_entry_bytes() -> int:
    """Return the maximum size for a single response cache entry."""
    return get_env_int("X_CACHE_MAX_ENTRY_BYTES", X_CACHE_MAX_ENTRY_BYTES, minimum=1)


def get_x_timeline_cache_ttl_seconds() -> int:
    """Return the fallback cache TTL for latest timeline/tweet-list responses."""
    return get_env_int("X_TIMELINE_CACHE_TTL_SECONDS", X_TIMELINE_CACHE_TTL_SECONDS, minimum=0)


def get_source_timeline_cache_ttl_seconds(source: Dict[str, Any]) -> int:
    """Return the timeline cache TTL for one Twitter source."""
    raw_value = source.get("twitter_cache_ttl_seconds")
    if raw_value is not None:
        try:
            value = int(raw_value)
            if value >= 0:
                return value
        except (TypeError, ValueError):
            pass
        logging.warning(
            "Invalid twitter_cache_ttl_seconds=%r for source %s; using default",
            raw_value,
            source.get("id", source.get("handle", "unknown")),
        )

    if source.get("priority"):
        return get_env_int(
            "X_PRIORITY_TIMELINE_CACHE_TTL_SECONDS",
            X_PRIORITY_TIMELINE_CACHE_TTL_SECONDS,
            minimum=0,
        )
    return get_env_int(
        "X_REGULAR_TIMELINE_CACHE_TTL_SECONDS",
        X_REGULAR_TIMELINE_CACHE_TTL_SECONDS,
        minimum=0,
    )


def is_x_response_cache_disabled() -> bool:
    """Return true when response body caching is disabled."""
    return os.getenv("X_CACHE_DISABLE_RESPONSE_CACHE", "").strip().lower() in {"1", "true", "yes", "on"}


def _atomic_json_write(path: Path, value: Any) -> None:
    """Write JSON atomically inside the destination directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(_pretty_json_text(value))
        os.replace(temp_path, path)
    finally:
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except OSError:
            pass


def _pretty_json_text(value: Any) -> str:
    """Return the exact JSON text used for project-local state files."""
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _pretty_json_size(value: Any) -> int:
    """Return the exact UTF-8 byte size written by _atomic_json_write."""
    return len(_pretty_json_text(value).encode("utf-8"))


class JsonStateStore:
    """Small JSON file store with atomic saves."""

    def __init__(self, path: Path, default: Optional[Dict[str, Any]] = None):
        self.path = Path(path)
        self.default = default if default is not None else {}
        self._lock = threading.RLock()

    def load(self) -> Dict[str, Any]:
        """Load the JSON state, returning a copy of the default on failure."""
        with self._lock:
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    value = json.load(f)
                return value if isinstance(value, dict) else dict(self.default)
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                return dict(self.default)

    def save(self, value: Dict[str, Any]) -> None:
        """Persist the JSON state atomically."""
        with self._lock:
            _atomic_json_write(self.path, value)


def _stable_json(value: Any) -> Any:
    """Return a JSON-stable shape for hashing request parameters."""
    if isinstance(value, dict):
        return {str(key): _stable_json(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_stable_json(item) for item in value]
    return value


def _credential_id(value: Optional[str]) -> str:
    """Return a non-secret credential identifier."""
    if not value:
        return "anonymous"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _headers_to_dict(headers: Any) -> Dict[str, str]:
    """Convert urllib/email headers into a lowercase dict."""
    result: Dict[str, str] = {}
    if not headers:
        return result
    items = headers.items() if hasattr(headers, "items") else []
    for key, value in items:
        result[str(key).lower()] = str(value)
    return result


def _header_value(headers: Any, name: str) -> Optional[str]:
    """Read a header by name from common mapping/header objects."""
    if not headers:
        return None
    if hasattr(headers, "get"):
        value = headers.get(name)
        if value is None:
            value = headers.get(name.lower())
        if value is None:
            value = headers.get(name.upper())
        return str(value) if value is not None else None
    lowered = name.lower()
    for key, value in getattr(headers, "items", lambda: [])():
        if str(key).lower() == lowered:
            return str(value)
    return None


def _parse_int_header(headers: Any, name: str) -> Optional[int]:
    """Parse an integer response header."""
    value = _header_value(headers, name)
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def _parse_retry_after_until(headers: Any, current: float) -> Optional[int]:
    """Parse Retry-After as an absolute epoch timestamp."""
    value = _header_value(headers, "retry-after")
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        delay_seconds = int(value)
        if delay_seconds < 0:
            return None
        return int(current + delay_seconds)
    except ValueError:
        pass
    try:
        retry_at = parsedate_to_datetime(value)
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=timezone.utc)
        return int(retry_at.timestamp())
    except (TypeError, ValueError, OSError):
        return None


_SHARED_FILE_LOCKS: Dict[str, threading.RLock] = {}
_SHARED_FILE_LOCKS_GUARD = threading.Lock()
_SHARED_RATE_LIMIT_MANAGERS: Dict[str, "XRateLimitManager"] = {}
_SHARED_FILE_CACHES: Dict[Tuple[str, str, bool, str], "XFileCache"] = {}
_SHARED_STATE_GUARD = threading.Lock()


def _shared_file_lock(path: Path) -> threading.RLock:
    """Return one in-process lock for all users of the same JSON state path."""
    key = str(path.resolve())
    with _SHARED_FILE_LOCKS_GUARD:
        lock = _SHARED_FILE_LOCKS.get(key)
        if lock is None:
            lock = threading.RLock()
            _SHARED_FILE_LOCKS[key] = lock
        return lock


class XRateLimitManager:
    """Project-local endpoint-aware X API rate-limit state."""

    def __init__(self, cache_dir: Optional[Path] = None, now_func=time.time):
        self.cache_dir = Path(cache_dir) if cache_dir is not None else get_x_cache_dir()
        self.store = JsonStateStore(self.cache_dir / "rate_limits.json")
        self.now_func = now_func
        self._lock = _shared_file_lock(self.store.path)

    @staticmethod
    def bucket_key(backend: str, endpoint: str, credential: Optional[str] = None) -> str:
        """Build a stable, non-secret bucket key."""
        return f"{backend}:{endpoint}:{_credential_id(credential)}"

    def can_request(
        self,
        backend: str,
        endpoint: str,
        credential: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Tuple[bool, Optional[float]]:
        """Return whether an endpoint can be called now."""
        current = self.now_func() if now is None else now
        key = self.bucket_key(backend, endpoint, credential)
        with self._lock:
            bucket = self.store.load().get(key, {})
        paused_until = float(bucket.get("paused_until") or 0)
        reset_at = float(bucket.get("reset_at") or 0)
        remaining = bucket.get("remaining")
        if paused_until > current:
            return False, paused_until
        if remaining == 0 and reset_at > current:
            return False, reset_at
        return True, None

    def require_request(self, backend: str, endpoint: str, credential: Optional[str] = None) -> None:
        """Raise when an endpoint should be deferred."""
        allowed, deferred_until = self.can_request(backend, endpoint, credential)
        if not allowed and deferred_until is not None:
            raise XRateLimitDeferred(deferred_until)

    def update_from_headers(
        self,
        backend: str,
        endpoint: str,
        credential: Optional[str],
        headers: Any,
        status_code: Optional[int] = None,
    ) -> None:
        """Persist rate-limit headers for an endpoint bucket."""
        current = self.now_func()
        limit = _parse_int_header(headers, "x-rate-limit-limit")
        remaining = _parse_int_header(headers, "x-rate-limit-remaining")
        reset_at = _parse_int_header(headers, "x-rate-limit-reset")
        retry_after_until = _parse_retry_after_until(headers, current)
        key = self.bucket_key(backend, endpoint, credential)

        with self._lock:
            state = self.store.load()
            bucket = dict(state.get(key, {}))
            if limit is not None:
                bucket["limit"] = limit
            if remaining is not None:
                bucket["remaining"] = remaining
            if reset_at is not None:
                bucket["reset_at"] = reset_at
            if status_code == 429:
                if reset_at is not None:
                    bucket["paused_until"] = reset_at
                elif retry_after_until is not None:
                    bucket["paused_until"] = retry_after_until
                else:
                    bucket["paused_until"] = int(current + X_RATE_LIMIT_FALLBACK_SECONDS)
                if remaining is None:
                    bucket["remaining"] = 0
            elif bucket.get("paused_until") and float(bucket["paused_until"]) <= current:
                bucket["paused_until"] = None
            bucket["updated_at"] = int(current)
            state[key] = bucket
            try:
                self.store.save(state)
            except Exception as exc:
                logging.warning("Failed to persist X rate-limit state: %s", exc)


def get_x_rate_limit_manager(cache_dir: Optional[Path] = None) -> "XRateLimitManager":
    """Return a shared rate-limit manager for the project-local state file."""
    resolved_cache_dir = Path(cache_dir) if cache_dir is not None else get_x_cache_dir()
    key = str((resolved_cache_dir / "rate_limits.json").resolve())
    with _SHARED_STATE_GUARD:
        manager = _SHARED_RATE_LIMIT_MANAGERS.get(key)
        if manager is None:
            manager = XRateLimitManager(cache_dir=resolved_cache_dir)
            _SHARED_RATE_LIMIT_MANAGERS[key] = manager
        return manager


def get_x_file_cache(
    backend: str,
    cache_dir: Optional[Path] = None,
    no_cache: bool = False,
    credential: Optional[str] = None,
) -> "XFileCache":
    """Return a shared response cache for one backend and credential scope."""
    resolved_cache_dir = Path(cache_dir) if cache_dir is not None else get_x_cache_dir()
    credential_id = _credential_id(credential)
    key = (str((resolved_cache_dir / "cache_index.json").resolve()), backend, no_cache, credential_id)
    with _SHARED_STATE_GUARD:
        cache = _SHARED_FILE_CACHES.get(key)
        if cache is None:
            cache = XFileCache(
                backend,
                cache_dir=resolved_cache_dir,
                no_cache=no_cache,
                credential=credential,
            )
            _SHARED_FILE_CACHES[key] = cache
        return cache


class XFileCache:
    """File response cache for X/Twitter fetchers."""

    def __init__(
        self,
        backend: str,
        cache_dir: Optional[Path] = None,
        no_cache: bool = False,
        credential: Optional[str] = None,
    ):
        self.backend = backend
        self.credential_id = _credential_id(credential)
        self.cache_dir = Path(cache_dir) if cache_dir is not None else get_x_cache_dir()
        self.no_cache = no_cache
        self.index_store = JsonStateStore(self.cache_dir / "cache_index.json")
        self._lock = _shared_file_lock(self.index_store.path)

    @staticmethod
    def endpoint_slug(endpoint: str) -> str:
        """Return a safe directory slug for an endpoint."""
        slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", endpoint.strip("/ "))
        return slug.strip("_") or "root"

    def make_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Return a stable request cache key."""
        payload = {
            "backend": self.backend,
            "credential_id": self.credential_id,
            "endpoint": endpoint,
            "params": _stable_json(params or {}),
        }
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def _entry_path(self, endpoint: str, cache_key: str) -> Path:
        return self.cache_dir / "responses" / self.backend / self.endpoint_slug(endpoint) / f"{cache_key}.json"

    def _indexed_entry_path(self, entry: Dict[str, Any]) -> Optional[Path]:
        """Return a cache-index path only when it stays inside cache_dir."""
        raw_path = str(entry.get("path") or "")
        if not raw_path:
            return None
        candidate = Path(raw_path)
        if candidate.is_absolute():
            return None
        try:
            cache_root = self.cache_dir.resolve()
            resolved = (self.cache_dir / candidate).resolve()
            resolved.relative_to(cache_root)
            return resolved
        except (OSError, ValueError):
            return None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """Return cached response body when present and fresh."""
        if self.no_cache or is_x_response_cache_disabled():
            return None

        current = time.time()
        cache_key = self.make_key(endpoint, params)
        with self._lock:
            index = self.index_store.load()
            entry = index.get(cache_key)
            if not entry:
                return None
            path = self._indexed_entry_path(entry)
            if path is None:
                return None
            expires_at = float(entry.get("expires_at") or 0)
            if expires_at and expires_at <= current:
                return None
            try:
                with open(path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                return None
            body = payload.get("body")
            try:
                entry["last_accessed_at"] = int(current)
                index[cache_key] = entry
                self.index_store.save(index)
            except Exception as exc:
                logging.warning("Failed to persist X response cache access time: %s", exc)
            return body

    @staticmethod
    def _is_cacheable_body(body: Any) -> bool:
        """Return false for provider error envelopes carried by HTTP 2xx responses."""
        if not isinstance(body, dict):
            return True
        if body.get("error"):
            return False
        errors = body.get("errors")
        if isinstance(errors, list) and errors:
            return False
        if isinstance(errors, dict) and errors:
            return False
        return True

    def put(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]],
        status_code: int,
        headers: Any,
        body: Any,
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """Persist a successful response body."""
        if self.no_cache or is_x_response_cache_disabled() or status_code >= 400:
            return
        if not self._is_cacheable_body(body):
            logging.debug("Skipping X cache write for %s: response body contains provider errors", endpoint)
            return

        current = int(time.time())
        ttl = ttl_seconds if ttl_seconds is not None else get_x_cache_retention_seconds()
        cache_key = self.make_key(endpoint, params)
        path = self._entry_path(endpoint, cache_key)
        payload = {
            "backend": self.backend,
            "credential_id": self.credential_id,
            "endpoint": endpoint,
            "params": _stable_json(params or {}),
            "status_code": status_code,
            "headers": _headers_to_dict(headers),
            "body": body,
            "fetched_at": current,
            "expires_at": current + ttl,
        }
        payload_size = _pretty_json_size(payload)
        if payload_size > get_x_cache_max_entry_bytes():
            logging.debug("Skipping X cache write for %s: response is %s bytes", endpoint, payload_size)
            return

        try:
            with self._lock:
                path.parent.mkdir(parents=True, exist_ok=True)
                _atomic_json_write(path, payload)
                index = self.index_store.load()
                index[cache_key] = {
                    "backend": self.backend,
                    "credential_id": self.credential_id,
                    "endpoint": endpoint,
                    "path": str(path.relative_to(self.cache_dir)),
                    "size": payload_size,
                    "fetched_at": current,
                    "expires_at": current + ttl,
                    "last_accessed_at": current,
                }
                self.index_store.save(index)
        except Exception as exc:
            logging.warning("Failed to persist X response cache entry: %s", exc)


class XCacheJanitor:
    """Best-effort cleanup for project-local X response cache files."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = Path(cache_dir) if cache_dir is not None else get_x_cache_dir()
        self.index_store = JsonStateStore(self.cache_dir / "cache_index.json")

    def cleanup(self) -> None:
        """Delete expired and over-budget cached responses."""
        try:
            self._cleanup()
        except Exception as exc:
            logging.warning("X cache cleanup failed: %s", exc)

    @staticmethod
    def _refresh_entry_size(path: Path, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Update entry size without letting stat failures abort cleanup."""
        try:
            entry["size"] = path.stat().st_size
        except OSError:
            entry["size"] = int(entry.get("size") or 0)
        return entry

    def _cleanup(self) -> None:
        current = int(time.time())
        retention_cutoff = current - get_x_cache_retention_seconds()
        index = self.index_store.load()
        kept: Dict[str, Dict[str, Any]] = {}

        cache_path_guard = XFileCache("janitor", cache_dir=self.cache_dir)
        for cache_key, entry in index.items():
            path = cache_path_guard._indexed_entry_path(entry)
            if path is None:
                continue
            fetched_at = int(entry.get("fetched_at") or 0)
            expires_at = int(entry.get("expires_at") or 0)
            if not path.exists():
                continue
            if fetched_at < retention_cutoff or (expires_at and expires_at <= current):
                try:
                    path.unlink()
                except OSError:
                    kept[cache_key] = self._refresh_entry_size(path, entry)
                continue
            kept[cache_key] = self._refresh_entry_size(path, entry)

        max_bytes = get_x_cache_max_bytes()
        total_bytes = sum(int(entry.get("size") or 0) for entry in kept.values())
        if total_bytes > max_bytes:
            ordered = sorted(
                kept.items(),
                key=lambda item: int(item[1].get("last_accessed_at") or item[1].get("fetched_at") or 0),
            )
            for cache_key, entry in ordered:
                if total_bytes <= max_bytes:
                    break
                path = cache_path_guard._indexed_entry_path(entry)
                if path is None:
                    kept.pop(cache_key, None)
                    continue
                size = int(entry.get("size") or 0)
                try:
                    path.unlink()
                except OSError:
                    continue
                total_bytes -= size
                kept.pop(cache_key, None)

        self.index_store.save(kept)


def x_request_json(
    backend: str,
    endpoint: str,
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    credential: Optional[str] = None,
    no_cache: bool = False,
    cache_ttl_seconds: Optional[int] = None,
    before_network: Optional[Callable[[], None]] = None,
) -> Any:
    """Fetch JSON with project-local response caching and rate-limit tracking."""
    cache = get_x_file_cache(backend, no_cache=no_cache, credential=credential)
    cached = cache.get(endpoint, params)
    if cached is not None:
        return cached

    rate_limits = get_x_rate_limit_manager()
    rate_limits.require_request(backend, endpoint, credential)
    if before_network is not None:
        before_network()

    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            data = json.loads(raw.decode())
            rate_limits.update_from_headers(backend, endpoint, credential, resp.headers, status_code=resp.status)
            cache.put(endpoint, params, resp.status, resp.headers, data, ttl_seconds=cache_ttl_seconds)
            return data
    except HTTPError as exc:
        rate_limits.update_from_headers(backend, endpoint, credential, exc.headers, status_code=exc.code)
        raise


# ---------------------------------------------------------------------------
# Backend abstraction
# ---------------------------------------------------------------------------

class TwitterBackend(ABC):
    """Base class for Twitter API backends."""

    @staticmethod
    def _make_result(source, articles, attempt):
        return {
            "source_id": source["id"],
            "source_type": "twitter",
            "name": source["name"],
            "handle": source["handle"].lstrip('@'),
            "priority": source["priority"],
            "topics": source["topics"],
            "status": "ok",
            "attempts": attempt + 1,
            "count": len(articles),
            "articles": articles,
        }

    @staticmethod
    def _make_error(source, error_msg, attempt):
        return {
            "source_id": source["id"],
            "source_type": "twitter",
            "name": source["name"],
            "handle": source["handle"].lstrip('@'),
            "priority": source["priority"],
            "topics": source["topics"],
            "status": "error",
            "attempts": attempt + 1,
            "error": error_msg,
            "count": 0,
            "articles": [],
        }

    @abstractmethod
    def fetch_all(self, sources: List[Dict[str, Any]], cutoff: datetime) -> List[Dict[str, Any]]:
        """Fetch tweets for all sources. Returns list of source result dicts."""


class OpenCliBackend(TwitterBackend):
    """OpenCLI backend using the browser-backed twitter tweets adapter."""

    def __init__(
        self,
        command: Optional[str] = None,
        max_workers: Optional[int] = None,
        auto_update: bool = False,
        no_cache: bool = False,
    ):
        self.command = command or resolve_opencli_bin()
        self._max_workers = max_workers
        self._auto_update = auto_update
        self.no_cache = no_cache
        self._before_chrome_windows: Optional[Dict[str, List[str]]] = None
        try:
            if self._auto_update:
                update_result = _ensure_opencli_latest(self.command)
                if update_result["status"] == "throttled" and _is_opencli_below_min_version(self.command):
                    logging.info("OpenCLI update throttle bypassed because the installed version is below minimum.")
                    update_result = _ensure_opencli_latest(self.command, force=True)
                if update_result["status"] == "updated":
                    logging.info(update_result["message"])
                elif update_result["status"] == "already_latest":
                    logging.info(update_result["message"])
                elif update_result["status"] == "throttled":
                    logging.debug(update_result["message"])
                elif update_result["status"] == "disabled":
                    logging.debug(update_result["message"])
                elif update_result["status"] == "unsupported":
                    logging.warning(update_result["message"])
                else:
                    logging.warning(
                        "OpenCLI auto-update check did not complete successfully: %s",
                        update_result["message"],
                    )
            _ensure_opencli_min_version(self.command)
            self._before_chrome_windows = snapshot_chrome_windows()
            self._verify_capability()
            self._run_doctor()
        except Exception:
            cleanup_new_opencli_chrome_windows(self._before_chrome_windows)
            raise

    def _run_command(self, args: List[str], timeout: int = OPENCLI_TIMEOUT) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                [self.command] + args,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=os.environ,
            )
        except subprocess.TimeoutExpired as exc:
            raise OpenCliBackendError("opencli_timeout", f"OpenCLI command timed out: {exc}") from exc

    def _list_browser_tabs(self) -> Optional[Dict[str, str]]:
        if not get_opencli_close_tabs_after_run():
            return {}

        result = self._run_command(["browser", "tab", "list"], timeout=OPENCLI_TAB_COMMAND_TIMEOUT)
        if result.returncode != 0:
            logging.warning("opencli browser tab list failed: %s", (result.stderr or result.stdout).strip()[:200])
            return None

        try:
            payload = json.loads(result.stdout or "null")
        except json.JSONDecodeError:
            logging.warning("opencli browser tab list returned invalid JSON")
            return None
        return extract_opencli_browser_tabs(payload)

    def _cleanup_new_browser_tabs(self, before_tabs: Optional[Dict[str, str]]) -> None:
        if before_tabs is None or not get_opencli_close_tabs_after_run():
            return

        after_tabs = self._list_browser_tabs()
        if after_tabs is None:
            return

        pending_targets = [
            target_id
            for target_id, url in after_tabs.items()
            if target_id not in before_tabs and is_twitter_browser_tab(url)
        ]
        if not pending_targets:
            return

        for target_id in pending_targets:
            result = self._run_command(
                ["browser", "tab", "close", target_id],
                timeout=OPENCLI_TAB_COMMAND_TIMEOUT,
            )
            if result.returncode != 0:
                logging.warning(
                    "opencli browser tab close failed: %s",
                    (result.stderr or result.stdout).strip()[:200],
                )
        time.sleep(0.5)

    def _release_browser_lease(self) -> None:
        if not get_opencli_close_tabs_after_run():
            return

        result = self._run_command(["browser", "close"], timeout=OPENCLI_TAB_COMMAND_TIMEOUT)
        if result.returncode != 0:
            logging.warning("opencli browser close failed: %s", (result.stderr or result.stdout).strip()[:200])

    def _verify_capability(self) -> None:
        result = self._run_command(["twitter", "tweets", "--help"], timeout=30)
        if result.returncode != 0:
            raise OpenCliBackendError(
                "opencli_capability_missing",
                (result.stderr or result.stdout or "OpenCLI does not expose the twitter tweets command.").strip(),
            )

        help_text = f"{result.stdout}\n{result.stderr}".lower()
        if "twitter tweets" not in help_text:
            raise OpenCliBackendError(
                "opencli_capability_missing",
                "OpenCLI does not expose the twitter tweets command.",
            )

    def _run_doctor(self) -> None:
        result = self._run_command(["doctor"], timeout=30)
        if result.returncode == 0:
            return
        code = _classify_opencli_failure(result.returncode, result.stderr, result.stdout)
        if code in {"opencli_browser_unavailable", "opencli_auth_required"}:
            raise OpenCliBackendError(code, result.stderr.strip() or "opencli doctor failed")
        logging.warning(f"opencli doctor returned {result.returncode}: {(result.stderr or result.stdout).strip()[:200]}")

    def _parse_tweets_payload(self, payload: Any, source: Dict[str, Any], cutoff: datetime) -> List[Dict[str, Any]]:
        articles = []
        for record in extract_opencli_tweet_records(payload):
            article = normalize_opencli_tweet(record, source, cutoff)
            if article:
                articles.append(article)
        return articles

    def _parse_tweets_output(self, stdout: str, source: Dict[str, Any], cutoff: datetime) -> List[Dict[str, Any]]:
        try:
            payload = json.loads(stdout or "null")
        except json.JSONDecodeError as exc:
            raise OpenCliBackendError("opencli_parse_error", "opencli twitter tweets returned invalid JSON") from exc

        return self._parse_tweets_payload(payload, source, cutoff)

    def _fetch_user_tweets(self, source: Dict[str, Any], cutoff: datetime) -> Dict[str, Any]:
        handle = source["handle"].lstrip("@")
        cache = XFileCache("opencli", no_cache=self.no_cache)
        endpoint = "twitter/tweets"
        params = {"handle": handle, "limit": MAX_TWEETS_PER_USER}
        ttl_seconds = get_source_timeline_cache_ttl_seconds(source)
        cached_payload = cache.get(endpoint, params)
        if cached_payload is not None:
            articles = self._parse_tweets_payload(cached_payload, source, cutoff)
            return self._make_result(source, articles, 0)

        result = self._run_command(
            [
                "twitter",
                "tweets",
                handle,
                "--limit",
                str(MAX_TWEETS_PER_USER),
                "-f",
                "json",
            ]
        )

        if result.returncode != 0:
            code = _classify_opencli_failure(result.returncode, result.stderr, result.stdout)
            message = (result.stderr or result.stdout or "opencli twitter tweets failed").strip()
            if code in OPENCLI_GLOBAL_ERROR_CODES:
                raise OpenCliBackendError(code, message)
            return self._make_error(source, f"{code}: {message[:160]}", 0)

        try:
            payload = json.loads(result.stdout or "null")
        except json.JSONDecodeError as exc:
            raise OpenCliBackendError("opencli_parse_error", "opencli twitter tweets returned invalid JSON") from exc
        cache.put(endpoint, params, 200, {}, payload, ttl_seconds=ttl_seconds)
        articles = self._parse_tweets_payload(payload, source, cutoff)
        return self._make_result(source, articles, 0)

    def fetch_all(self, sources: List[Dict[str, Any]], cutoff: datetime) -> List[Dict[str, Any]]:
        if not sources:
            return []

        before_chrome_windows = self._before_chrome_windows
        before_tabs = self._list_browser_tabs()
        results: List[Dict[str, Any]] = []
        total = len(sources)

        try:
            first = self._fetch_user_tweets(sources[0], cutoff)
            results.append(first)
            logging.info(f"[1/{total}] @{first['handle']}: {first['count']} tweets via OpenCLI")

            remaining = sources[1:]
            if not remaining:
                return results

            done = 1
            max_workers = self._max_workers if self._max_workers is not None else get_opencli_max_workers()
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = {pool.submit(self._fetch_user_tweets, source, cutoff): source for source in remaining}
                for future in as_completed(futures):
                    source = futures[future]
                    try:
                        result = future.result()
                    except OpenCliBackendError as exc:
                        result = self._make_error(source, f"{exc.code}: {exc.message[:160]}", 0)
                    results.append(result)
                    done += 1
                    if result["status"] == "ok":
                        logging.info(f"[{done}/{total}] ✅ @{result['handle']}: {result['count']} tweets via OpenCLI")
                    else:
                        logging.warning(f"[{done}/{total}] ❌ @{result['handle']}: {result.get('error', 'unknown')}")

            return results
        finally:
            self._cleanup_new_browser_tabs(before_tabs)
            self._release_browser_lease()
            cleanup_new_opencli_chrome_windows(before_chrome_windows)


class OfficialBackend(TwitterBackend):
    """Official X API v2 backend (existing logic)."""

    def __init__(self, bearer_token: str, no_cache: bool = False):
        self.bearer_token = bearer_token
        self.no_cache = no_cache

    # -- ID cache helpers --

    @staticmethod
    def _load_id_cache() -> Dict[str, Any]:
        return JsonStateStore(get_x_id_cache_path()).load()

    @staticmethod
    def _save_id_cache(cache: Dict[str, Any]) -> None:
        try:
            JsonStateStore(get_x_id_cache_path()).save(cache)
        except Exception as e:
            logging.warning(f"Failed to save ID cache: {e}")

    def _batch_resolve_user_ids(self, handles: List[str]) -> Dict[str, str]:
        now = time.time()
        cache = {} if self.no_cache else self._load_id_cache()
        ttl_seconds = ID_CACHE_TTL_DAYS * 86400

        result: Dict[str, str] = {}
        to_resolve: List[str] = []
        for handle in handles:
            key = handle.lower()
            entry = cache.get(key)
            if entry and (now - entry.get("ts", 0)) < ttl_seconds:
                result[key] = entry["id"]
            else:
                to_resolve.append(handle)

        if to_resolve:
            logging.info(f"Batch resolving {len(to_resolve)} usernames (cached: {len(result)})")
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                "User-Agent": "FollowNews/2.0"
            }
            for i in range(0, len(to_resolve), 100):
                batch = to_resolve[i:i+100]
                url = f"{USER_LOOKUP_ENDPOINT}?{urlencode({'usernames': ','.join(batch)})}"
                try:
                    data = x_request_json(
                        "official",
                        "GET /2/users/by",
                        url,
                        headers,
                        {"usernames": ",".join(batch)},
                        credential=self.bearer_token,
                        no_cache=self.no_cache,
                        cache_ttl_seconds=ID_CACHE_TTL_DAYS * 86400,
                    )

                    if 'data' in data:
                        for user in data['data']:
                            key = user['username'].lower()
                            result[key] = user['id']
                            cache[key] = {"id": user['id'], "ts": now}

                    if 'errors' in data:
                        for err in data['errors']:
                            logging.warning(f"User lookup error: {err.get('detail', err)}")

                except XRateLimitDeferred as e:
                    logging.warning(
                        "Batch user lookup rate-limit deferred until %s; skipping individual fallback",
                        int(e.deferred_until),
                    )
                    break

                except Exception as e:
                    logging.error(f"Batch user lookup failed: {e}")
                    for handle in batch:
                        try:
                            fallback_url = f"{USER_LOOKUP_ENDPOINT}?{urlencode({'usernames': handle})}"
                            fallback_data = x_request_json(
                                "official",
                                "GET /2/users/by",
                                fallback_url,
                                headers,
                                {"usernames": handle},
                                credential=self.bearer_token,
                                no_cache=self.no_cache,
                                cache_ttl_seconds=ID_CACHE_TTL_DAYS * 86400,
                            )
                            if 'data' in fallback_data and fallback_data['data']:
                                key = handle.lower()
                                result[key] = fallback_data['data'][0]['id']
                                cache[key] = {"id": result[key], "ts": now}
                        except Exception as e2:
                            logging.warning(f"Individual lookup failed for @{handle}: {e2}")

            if not self.no_cache:
                self._save_id_cache(cache)
        else:
            logging.info(f"All {len(result)} usernames resolved from cache")

        return result

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        try:
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            logging.debug(f"Failed to parse Twitter date: {date_str}")
            return None

    def _fetch_user_tweets(self, source: Dict[str, Any], cutoff: datetime,
                           user_id: Optional[str] = None) -> Dict[str, Any]:
        handle = source["handle"].lstrip('@')
        topics = source["topics"]

        for attempt in range(RETRY_COUNT + 1):
            try:
                params = {
                    "max_results": min(MAX_TWEETS_PER_USER, 100),
                    "tweet.fields": "created_at,public_metrics,context_annotations,referenced_tweets",
                    "expansions": "author_id",
                    "user.fields": "verified,public_metrics"
                }

                if not user_id:
                    user_url = f"{USER_LOOKUP_ENDPOINT}?{urlencode({'usernames': handle})}"
                    headers = {
                        "Authorization": f"Bearer {self.bearer_token}",
                        "User-Agent": "FollowNews/2.0"
                    }
                    user_data = x_request_json(
                        "official",
                        "GET /2/users/by",
                        user_url,
                        headers,
                        {"usernames": handle},
                        credential=self.bearer_token,
                        no_cache=self.no_cache,
                        cache_ttl_seconds=ID_CACHE_TTL_DAYS * 86400,
                    )
                    if 'data' not in user_data or not user_data['data']:
                        raise ValueError(f"User not found: {handle}")
                    user_id = user_data['data'][0]['id']

                headers = {
                    "Authorization": f"Bearer {self.bearer_token}",
                    "User-Agent": "FollowNews/2.0"
                }

                time.sleep(0.3)

                tweets_url = f"{OFFICIAL_API_BASE}/users/{user_id}/tweets?{urlencode(params)}"
                tweets_data = x_request_json(
                    "official",
                    "GET /2/users/:id/tweets",
                    tweets_url,
                    headers,
                    {"user_id": user_id, **params},
                    credential=self.bearer_token,
                    no_cache=self.no_cache,
                    cache_ttl_seconds=get_source_timeline_cache_ttl_seconds(source),
                )

                articles = []
                if 'data' in tweets_data:
                    for tweet in tweets_data['data']:
                        created_at = self._parse_date(tweet.get('created_at', ''))
                        if not created_at or created_at < cutoff:
                            continue

                        text = tweet.get('text', '')
                        if text.startswith('RT @'):
                            continue
                        referenced = tweet.get('referenced_tweets', [])
                        if any(ref.get('type') == 'replied_to' for ref in referenced):
                            continue

                        articles.append({
                            "title": clean_tweet_text(text),
                            "link": f"https://twitter.com/{handle}/status/{tweet['id']}",
                            "date": created_at.isoformat(),
                            "topics": topics[:],
                            "metrics": tweet.get('public_metrics', {}),
                            "tweet_id": tweet['id']
                        })

                return self._make_result(source, articles, attempt)

            except HTTPError as e:
                if e.code == 429:
                    error_msg = "Rate limit exceeded"
                    logging.warning(f"Rate limit hit for @{handle}, attempt {attempt + 1}")
                else:
                    error_msg = f"HTTP {e.code}: {e.reason}"

            except XRateLimitDeferred as e:
                error_msg = f"Rate limit deferred until {int(e.deferred_until)}"
                logging.warning(f"Rate limit deferred for @{handle} until {int(e.deferred_until)}")
                return self._make_error(source, error_msg, attempt)

            except Exception as e:
                error_msg = str(e)[:100]
                logging.debug(f"Attempt {attempt + 1} failed for @{handle}: {error_msg}")

            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue

            return self._make_error(source, error_msg, attempt)

    def fetch_all(self, sources: List[Dict[str, Any]], cutoff: datetime) -> List[Dict[str, Any]]:
        all_handles = [s["handle"].lstrip('@') for s in sources]
        user_id_map = self._batch_resolve_user_ids(all_handles)

        results: List[Dict[str, Any]] = []
        total = len(sources)
        done = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {}
            for source in sources:
                handle = source["handle"].lstrip('@')
                resolved_id = user_id_map.get(handle.lower())
                futures[pool.submit(self._fetch_user_tweets, source, cutoff, resolved_id)] = source

            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                done += 1
                if result["status"] == "ok":
                    logging.info(f"[{done}/{total}] ✅ @{result['handle']}: {result['count']} tweets"
                                 + (f" (top: {result['articles'][0]['metrics']['like_count']}❤️)" if result.get('articles') else ""))
                else:
                    logging.warning(f"[{done}/{total}] ❌ @{result['handle']}: {result.get('error','unknown')}")

        return results


class TwitterApiIoBackend(TwitterBackend):
    """twitterapi.io backend."""

    def __init__(self, api_key: str, no_cache: bool = False):
        self.api_key = api_key
        self.no_cache = no_cache
        self._limiter = RateLimiter(qps=5)

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        """Parse twitterapi.io date format: 'Tue Dec 10 07:00:30 +0000 2024'."""
        try:
            return datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
        except (ValueError, TypeError):
            logging.debug(f"Failed to parse twitterapi.io date: {date_str}")
            return None

    def _parse_tweets_page(self, tweets: list, handle: str, topics: list, cutoff: datetime) -> list:
        """Parse a page of tweets into article dicts."""
        articles = []
        for tweet in tweets:
            # Skip retweets
            if tweet.get("retweeted_tweet"):
                continue
            created_at = self._parse_date(tweet.get("createdAt", ""))
            if not created_at or created_at < cutoff:
                continue

            text = tweet.get("text", "")
            if text.startswith("RT @"):
                continue

            tweet_id = tweet.get("id", "")
            link = tweet.get("url") or f"https://twitter.com/{handle}/status/{tweet_id}"

            articles.append({
                "title": clean_tweet_text(text),
                "link": link,
                "date": created_at.isoformat(),
                "topics": topics[:],
                "metrics": {
                    "like_count": tweet.get("likeCount", 0),
                    "retweet_count": tweet.get("retweetCount", 0),
                    "reply_count": tweet.get("replyCount", 0),
                    "quote_count": tweet.get("quoteCount", 0),
                    "impression_count": tweet.get("viewCount", 0),
                },
                "tweet_id": tweet_id,
            })
        return articles

    def _fetch_user_tweets(self, source: Dict[str, Any], cutoff: datetime) -> Dict[str, Any]:
        handle = source["handle"].lstrip('@')
        topics = source["topics"]

        for attempt in range(RETRY_COUNT + 1):
            try:
                params = urlencode({
                    "userName": handle,
                    "includeReplies": "false",
                })
                url = f"{TWITTERAPIIO_BASE}/twitter/user/last_tweets?{params}"
                headers = {
                    "X-API-Key": self.api_key,
                    "User-Agent": "FollowNews/2.0",
                }

                raw = x_request_json(
                    "twitterapiio",
                    "GET /twitter/user/last_tweets",
                    url,
                    headers,
                    {"userName": handle, "includeReplies": "false"},
                    credential=self.api_key,
                    no_cache=self.no_cache,
                    cache_ttl_seconds=get_source_timeline_cache_ttl_seconds(source),
                    before_network=self._limiter.wait,
                )

                # API wraps response in {"data": {...}} envelope
                data = raw.get("data", raw)

                articles = self._parse_tweets_page(
                    data.get("tweets", []), handle, topics, cutoff
                )

                # Pagination: fetch one more page if available and all tweets still in window
                has_next = data.get("has_next_page", False)
                next_cursor = data.get("next_cursor")
                if has_next and next_cursor and articles:
                    oldest = min(a["date"] for a in articles)
                    if oldest >= cutoff.isoformat():
                        page2_params = urlencode({
                            "userName": handle,
                            "includeReplies": "false",
                            "cursor": next_cursor,
                        })
                        page2_url = f"{TWITTERAPIIO_BASE}/twitter/user/last_tweets?{page2_params}"
                        raw2 = x_request_json(
                            "twitterapiio",
                            "GET /twitter/user/last_tweets",
                            page2_url,
                            headers,
                            {"userName": handle, "includeReplies": "false", "cursor": next_cursor},
                            credential=self.api_key,
                            no_cache=self.no_cache,
                            cache_ttl_seconds=get_source_timeline_cache_ttl_seconds(source),
                            before_network=self._limiter.wait,
                        )
                        data2 = raw2.get("data", raw2)
                        articles.extend(self._parse_tweets_page(
                            data2.get("tweets", []), handle, topics, cutoff
                        ))
                        has_next = data2.get("has_next_page", False)

                # Truncation warning
                if has_next and articles:
                    oldest = min(a["date"] for a in articles)
                    if oldest >= cutoff.isoformat():
                        logging.warning(f"@{handle}: results may be truncated ({len(articles)} tweets, more available)")

                return self._make_result(source, articles, attempt)

            except HTTPError as e:
                if e.code == 429:
                    error_msg = "Rate limit exceeded"
                    logging.warning(f"Rate limit hit for @{handle}, attempt {attempt + 1}")
                else:
                    error_msg = f"HTTP {e.code}: {e.reason}"

            except XRateLimitDeferred as e:
                error_msg = f"Rate limit deferred until {int(e.deferred_until)}"
                logging.warning(f"Rate limit deferred for @{handle} until {int(e.deferred_until)}")
                return self._make_error(source, error_msg, attempt)

            except Exception as e:
                error_msg = str(e)[:100]
                logging.debug(f"Attempt {attempt + 1} failed for @{handle}: {error_msg}")

            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue

            return self._make_error(source, error_msg, attempt)

    def fetch_all(self, sources: List[Dict[str, Any]], cutoff: datetime) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        total = len(sources)
        done = 0
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {pool.submit(self._fetch_user_tweets, source, cutoff): source
                       for source in sources}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                done += 1
                if result["status"] == "ok":
                    logging.info(f"[{done}/{total}] ✅ @{result['handle']}: {result['count']} tweets"
                                 + (f" (top: {result['articles'][0]['metrics']['like_count']}❤️)" if result['articles'] else ""))
                else:
                    logging.warning(f"[{done}/{total}] ❌ @{result['handle']}: {result['error']}")

        return results


class GetXApiBackend(TwitterBackend):
    """GetXAPI backend."""

    def __init__(self, api_key: str, no_cache: bool = False):
        """Initialize GetXAPI backend with API key validation."""
        if not api_key or len(api_key) < 10:
            raise ValueError("Invalid GETX_API_KEY format - expected at least 10 characters")
        self.api_key = api_key
        self.no_cache = no_cache
        self.logger = logging.getLogger("fetch-twitter")

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse GetXAPI date string with multiple format support.
        
        Supported formats:
        - 'Tue Dec 10 07:00:30 +0000 2024' (Twitter format)
        - '2024-12-10T07:00:30+00:00' (ISO 8601)
        - '2024-12-10 07:00:30' (Simple datetime)
        """
        formats = [
            "%a %b %d %H:%M:%S %z %Y",      # Twitter format
            "%Y-%m-%dT%H:%M:%S%z",          # ISO 8601
            "%Y-%m-%d %H:%M:%S",            # Simple datetime
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except (ValueError, TypeError):
                continue
        
        self.logger.debug(f"Failed to parse date '{date_str}' with all known formats")
        return None

    def _parse_tweets_page(self, tweets: list, handle: str, topics: list, cutoff: datetime) -> list:
        articles = []
        for tweet in tweets:
            tweet_id = tweet.get("id")
            text = tweet.get("text")
            created_at_raw = tweet.get("createdAt")
            if not tweet_id or not text or not created_at_raw:
                continue
            if tweet.get("isReply"):
                continue
            if text.startswith("RT @"):
                continue

            created_at = self._parse_date(created_at_raw)
            if not created_at or created_at < cutoff:
                continue

            link = tweet.get("url") or f"https://x.com/{handle}/status/{tweet_id}"

            articles.append({
                "title": clean_tweet_text(text),
                "link": link,
                "date": created_at.isoformat(),
                "topics": topics[:],
                "metrics": {
                    "like_count": tweet.get("likeCount", 0),
                    "retweet_count": tweet.get("retweetCount", 0),
                    "reply_count": tweet.get("replyCount", 0),
                    "quote_count": tweet.get("quoteCount", 0),
                    "impression_count": tweet.get("viewCount", 0),
                },
                "tweet_id": tweet_id,
            })
        return articles

    def _fetch_user_tweets(self, source: Dict[str, Any], cutoff: datetime) -> Dict[str, Any]:
        handle = source["handle"].lstrip('@')
        topics = source["topics"]

        for attempt in range(RETRY_COUNT + 1):
            try:
                url = f"{GETXAPI_BASE}/twitter/user/tweets?{urlencode({'userName': handle})}"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "User-Agent": "FollowNews/2.0",
                }

                raw = x_request_json(
                    "getxapi",
                    "GET /twitter/user/tweets",
                    url,
                    headers,
                    {"userName": handle},
                    credential=self.api_key,
                    no_cache=self.no_cache,
                    cache_ttl_seconds=get_source_timeline_cache_ttl_seconds(source),
                )

                if raw.get("error"):
                    return self._make_error(source, str(raw["error"])[:100], attempt)

                articles = self._parse_tweets_page(
                    raw.get("tweets", []), handle, topics, cutoff
                )

                has_more = raw.get("has_more", False)
                next_cursor = raw.get("next_cursor")
                
                # Fetch page 2 if more results available (with retry)
                if has_more and next_cursor and articles:
                    oldest = min(datetime.fromisoformat(a["date"]) for a in articles)
                    if oldest >= cutoff:
                        for page_attempt in range(RETRY_COUNT + 1):
                            try:
                                page2_url = f"{GETXAPI_BASE}/twitter/user/tweets?{urlencode({'userName': handle, 'cursor': next_cursor})}"
                                raw2 = x_request_json(
                                    "getxapi",
                                    "GET /twitter/user/tweets",
                                    page2_url,
                                    headers,
                                    {"userName": handle, "cursor": next_cursor},
                                    credential=self.api_key,
                                    no_cache=self.no_cache,
                                    cache_ttl_seconds=get_source_timeline_cache_ttl_seconds(source),
                                )
                                if raw2.get("error"):
                                    raise ValueError(str(raw2["error"])[:100])
                                articles.extend(self._parse_tweets_page(
                                    raw2.get("tweets", []), handle, topics, cutoff
                                ))
                                has_more = raw2.get("has_more", False)
                                break  # Success
                            except Exception as e:
                                self.logger.warning(f"@{handle}: page 2 attempt {page_attempt + 1} failed: {e}")
                                if page_attempt < RETRY_COUNT:
                                    time.sleep(RETRY_DELAY * (2 ** page_attempt))
                                else:
                                    self.logger.warning(f"@{handle}: page 2 failed after {RETRY_COUNT} attempts, keeping page 1 results")
                                    has_more = False

                if has_more and articles:
                    oldest = min(datetime.fromisoformat(a["date"]) for a in articles)
                    if oldest >= cutoff:
                        logging.warning(f"@{handle}: results may be truncated ({len(articles)} tweets, more available)")

                return self._make_result(source, articles, attempt)

            except HTTPError as e:
                if e.code == 429:
                    error_msg = "Rate limit exceeded"
                    logging.warning(f"Rate limit hit for @{handle}, attempt {attempt + 1}")
                else:
                    error_msg = f"HTTP {e.code}: {e.reason}"

            except XRateLimitDeferred as e:
                error_msg = f"Rate limit deferred until {int(e.deferred_until)}"
                logging.warning(f"Rate limit deferred for @{handle} until {int(e.deferred_until)}")
                return self._make_error(source, error_msg, attempt)

            except Exception as e:
                error_msg = str(e)[:100]
                logging.debug(f"Attempt {attempt + 1} failed for @{handle}: {error_msg}")

            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue

            return self._make_error(source, error_msg, attempt)

    def fetch_all(self, sources: List[Dict[str, Any]], cutoff: datetime) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        total = len(sources)
        done = 0
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {pool.submit(self._fetch_user_tweets, source, cutoff): source
                       for source in sources}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                done += 1
                if result["status"] == "ok":
                    logging.info(f"[{done}/{total}] ✅ @{result['handle']}: {result['count']} tweets"
                                 + (f" (top: {result['articles'][0]['metrics']['like_count']}❤️)" if result['articles'] else ""))
                else:
                    logging.warning(f"[{done}/{total}] ❌ @{result['handle']}: {result['error']}")

        return results


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------

def _instantiate_backend(
    backend_name: str,
    no_cache: bool = False,
    opencli_workers: Optional[int] = None,
    opencli_auto_update: bool = False,
) -> Optional[TwitterBackend]:
    """Instantiate one backend without applying fallback policy."""
    if backend_name == "opencli":
        logging.info("Using OpenCLI backend")
        return OpenCliBackend(
            max_workers=opencli_workers,
            auto_update=opencli_auto_update,
            no_cache=no_cache,
        )

    if backend_name == "getxapi":
        key = os.getenv("GETX_API_KEY")
        if not key:
            logging.info("GETX_API_KEY not set; getxapi backend unavailable")
            return None
        logging.info("Using GetXAPI backend")
        return GetXApiBackend(key, no_cache=no_cache)

    if backend_name == "twitterapiio":
        key = os.getenv("TWITTERAPI_IO_KEY")
        if not key:
            logging.info("TWITTERAPI_IO_KEY not set; twitterapi.io backend unavailable")
            return None
        logging.info("Using twitterapi.io backend")
        return TwitterApiIoBackend(key, no_cache=no_cache)

    if backend_name == "official":
        token = os.getenv("X_BEARER_TOKEN")
        if not token:
            logging.info("X_BEARER_TOKEN not set; official backend unavailable")
            return None
        logging.info("Using official X API v2 backend")
        return OfficialBackend(token, no_cache=no_cache)

    logging.error(f"Unknown backend: {backend_name}")
    return None


def fetch_with_backend_chain(
    backend_name: str,
    sources: List[Dict[str, Any]],
    cutoff: datetime,
    no_cache: bool = False,
    opencli_workers: Optional[int] = None,
    opencli_auto_update: bool = False,
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, str]]]:
    """Fetch Twitter data using explicit backend or auto fallback chain."""
    diagnostics: List[Dict[str, str]] = []
    explicit = backend_name != "auto"

    for candidate in get_backend_order(backend_name):
        max_retries = OPENCLI_BROWSER_RECOVERABLE_RETRIES if candidate == "opencli" else 0

        for attempt in range(max_retries + 1):
            try:
                backend = _instantiate_backend(
                    candidate,
                    no_cache=no_cache,
                    opencli_workers=opencli_workers,
                    opencli_auto_update=opencli_auto_update,
                )
            except OpenCliBackendError as exc:
                diagnostics.append({"backend": candidate, "code": exc.code, "message": exc.message})
                logging.warning(
                    f"{candidate} unavailable: {exc.code}: {exc.message} "
                    f"(attempt {attempt + 1}/{max_retries + 1})"
                )
                if exc.code == "opencli_version_too_old":
                    return candidate, [], diagnostics
                if _is_retriable_opencli_error(exc.code) and candidate == "opencli" and attempt < max_retries:
                    logging.warning("opencli recovery attempt enabled after browser-bridge failure; retrying")
                    continue
                if explicit:
                    return candidate, [], diagnostics
                break

            if backend is None:
                diagnostics.append({
                    "backend": candidate,
                    "code": "backend_unavailable",
                    "message": f"{candidate} backend is not configured",
                })
                if explicit:
                    return candidate, [], diagnostics
                break

            try:
                return candidate, backend.fetch_all(sources, cutoff), diagnostics
            except OpenCliBackendError as exc:
                diagnostics.append({"backend": candidate, "code": exc.code, "message": exc.message})
                logging.warning(
                    f"{candidate} failed globally: {exc.code}: {exc.message} "
                    f"(attempt {attempt + 1}/{max_retries + 1})"
                )
                if exc.code == "opencli_version_too_old":
                    return candidate, [], diagnostics
                if _is_retriable_opencli_error(exc.code) and candidate == "opencli" and attempt < max_retries:
                    logging.warning("opencli recovery attempt enabled after browser-bridge failure; retrying")
                    continue
                if explicit:
                    return candidate, [], diagnostics
                break

    return backend_name, [], diagnostics


# ---------------------------------------------------------------------------
# Source loading
# ---------------------------------------------------------------------------

def load_twitter_sources(defaults_dir: Path, config_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Load Twitter sources from unified configuration with overlay support."""
    try:
        from config_loader import load_merged_sources
    except ImportError:
        # Fallback for relative import
        import sys
        sys.path.append(str(Path(__file__).parent))
        from config_loader import load_merged_sources

    # Load merged sources from defaults + optional user overlay
    all_sources = load_merged_sources(defaults_dir, config_dir)

    # Filter Twitter sources that are enabled
    twitter_sources = []
    for source in all_sources:
        if source.get("type") == "twitter" and source.get("enabled", True):
            if not source.get("handle"):
                logging.warning(f"Twitter source {source.get('id')} missing handle, skipping")
                continue
            twitter_sources.append(source)

    logging.info(f"Loaded {len(twitter_sources)} enabled Twitter sources")
    return twitter_sources


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Main Twitter fetching function."""
    parser = argparse.ArgumentParser(
        description="Fetch recent tweets from Twitter/X KOL accounts. "
                   "Supports OpenCLI, GetXAPI, twitterapi.io, and official X API v2 backends.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    export X_BEARER_TOKEN="your_token_here"
    python3 fetch-twitter.py
    python3 fetch-twitter.py --defaults config/defaults --config workspace/config --hours 24 -o results.json
    python3 fetch-twitter.py --backend twitterapiio  # use twitterapi.io
    python3 fetch-twitter.py --config workspace/config --verbose  # backward compatibility
        """
    )

    parser.add_argument(
        "--defaults",
        type=Path,
        default=Path("config/defaults"),
        help="Default configuration directory with skill defaults (default: config/defaults)"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="User configuration directory for overlays (optional)"
    )

    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Time window in hours for tweets (default: 24)"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output JSON path (default: auto-generated temp file)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Bypass username→ID cache (official backend only)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-fetch even if cached output exists"
    )

    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Skip OpenCLI self-update check/update on this run.",
    )

    parser.add_argument(
        "--backend",
        choices=["opencli", "official", "twitterapiio", "getxapi", "auto"],
        default=None,
        help="Twitter backend (overrides TWITTER_API_BACKEND env var). "
             "auto = opencli first, then getxapi, twitterapiio, official"
    )

    parser.add_argument(
        "--opencli-workers",
        type=int,
        default=None,
        help="OpenCLI concurrency for twitter tweets (1-10). "
             f"Defaults to {OPENCLI_DEFAULT_MAX_WORKERS}.",
    )

    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    XCacheJanitor().cleanup()

    # Resume support: skip if output exists, is valid JSON, and < 1 hour old
    if args.output and args.output.exists() and not args.force:
        try:
            age_seconds = time.time() - args.output.stat().st_mtime
            if age_seconds < 3600:
                with open(args.output, 'r') as f:
                    json.load(f)
                logger.info(f"Skipping (cached output exists): {args.output}")
                return 0
        except (json.JSONDecodeError, OSError):
            pass

    # Resolve backend: CLI arg > env var > default (auto)
    backend_name = args.backend or os.getenv("TWITTER_API_BACKEND", "auto")

    # Auto-generate unique output path if not specified
    if not args.output:
        fd, temp_path = tempfile.mkstemp(prefix="follow-news-twitter-", suffix=".json")
        os.close(fd)
        args.output = Path(temp_path)

    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)

        # Backward compatibility: if only --config provided, use old behavior
        if args.config and args.defaults == Path("config/defaults") and not args.defaults.exists():
            logger.debug("Backward compatibility mode: using --config as sole source")
            sources = load_twitter_sources(args.config, None)
        else:
            sources = load_twitter_sources(args.defaults, args.config)

        if not sources:
            logger.warning("No Twitter sources found or all disabled")

        logger.info(f"Fetching {len(sources)} Twitter accounts (window: {args.hours}h, backend: {backend_name})")

        selected_backend, results, backend_diagnostics = fetch_with_backend_chain(
            backend_name,
            sources,
            cutoff,
            no_cache=args.no_cache,
            opencli_workers=args.opencli_workers,
            opencli_auto_update=(not args.no_update) and _opencli_auto_update_enabled(),
        )

        if not results:
            logger.warning("No Twitter backend available. Writing empty result and skipping Twitter fetch.")
            empty_result = {
                "generated": datetime.now(timezone.utc).isoformat(),
                "source_type": "twitter",
                "backend": selected_backend,
                "hours": args.hours,
                "sources_total": 0,
                "sources_ok": 0,
                "total_articles": 0,
                "sources": [],
                "skipped_reason": build_twitter_skipped_reason(backend_name, backend_diagnostics),
                "backend_diagnostics": backend_diagnostics,
            }
            with open(args.output, "w", encoding='utf-8') as f:
                json.dump(empty_result, f, ensure_ascii=False, indent=2)
            XCacheJanitor().cleanup()
            print(f"Output (empty): {args.output}")
            return 0

        # Sort: priority first, then by article count
        results.sort(key=lambda x: (not x.get("priority", False), -x.get("count", 0)))

        ok_count = sum(1 for r in results if r["status"] == "ok")
        total_tweets = sum(r.get("count", 0) for r in results)

        output = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "source_type": "twitter",
            "backend": selected_backend,
            "requested_backend": backend_name,
            "backend_diagnostics": backend_diagnostics,
            "defaults_dir": str(args.defaults),
            "config_dir": str(args.config) if args.config else None,
            "hours": args.hours,
            "sources_total": len(results),
            "sources_ok": ok_count,
            "total_articles": total_tweets,
            "sources": results,
        }

        # Write output
        json_str = json.dumps(output, ensure_ascii=False, indent=2)
        with open(args.output, "w", encoding='utf-8') as f:
            f.write(json_str)

        logger.info(f"✅ Done: {ok_count}/{len(results)} accounts ok, "
                   f"{total_tweets} tweets → {args.output}")

        XCacheJanitor().cleanup()
        return 0

    except Exception as e:
        logger.error(f"💥 Twitter fetch failed: {e}")
        XCacheJanitor().cleanup()
        return 1


if __name__ == "__main__":
    sys.exit(main())
