"""Terminal UI helpers for /depradar — banners, spinners, status lines."""

from __future__ import annotations

import sys
import threading
import time
from typing import Optional

# ── Reconfigure stdout/stderr to UTF-8 on Windows ──────────────────────────
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")   # type: ignore[attr-defined]
    except Exception:
        pass

# ── Machine-mode output routing ─────────────────────────────────────────────
# When --emit=json or --emit=context, all progress/status output must go to
# stderr so stdout is pure machine-readable data.  Call set_machine_mode(True)
# before any status prints to activate this routing.

_status_file = sys.stdout


def set_machine_mode(enabled: bool) -> None:
    """Route all status/progress output to stderr (for --emit=json/context)."""
    global _status_file
    _status_file = sys.stderr if enabled else sys.stdout


# ── ANSI colours (gracefully degraded on Windows) ───────────────────────────

_USE_COLOUR = sys.stdout.isatty()

_RESET  = "\033[0m"  if _USE_COLOUR else ""
_BOLD   = "\033[1m"  if _USE_COLOUR else ""
_DIM    = "\033[2m"  if _USE_COLOUR else ""
_RED    = "\033[31m" if _USE_COLOUR else ""
_GREEN  = "\033[32m" if _USE_COLOUR else ""
_YELLOW = "\033[33m" if _USE_COLOUR else ""
_BLUE   = "\033[34m" if _USE_COLOUR else ""
_CYAN   = "\033[36m" if _USE_COLOUR else ""


def _c(colour: str, text: str) -> str:
    return f"{colour}{text}{_RESET}"


# ── Banner ───────────────────────────────────────────────────────────────────

BANNER = r"""
  /depradar  v2.0.0
  Breaking-change intelligence for your project dependencies
"""


def print_banner(config: dict, file=None) -> None:
    print(_c(_BOLD + _CYAN, BANNER), file=file)
    _print_source_status(config, file=file)
    print(file=file)


def _print_source_status(config: dict, file=None) -> None:
    lines = []
    gh = "✓ GitHub" if config.get("GITHUB_TOKEN") else "○ GitHub (unauth, 60/hr)"
    lines.append(gh)
    if config.get("SCRAPECREATORS_API_KEY"):
        lines.append("✓ Reddit")
    if config.get("XAI_API_KEY") or (config.get("AUTH_TOKEN") and config.get("CT0")):
        lines.append("✓ X/Twitter")
    if config.get("STACKOVERFLOW_API_KEY"):
        lines.append("✓ StackOverflow (enhanced)")
    else:
        lines.append("○ StackOverflow (limited)")
    lines.append("✓ npm/PyPI/crates.io")
    lines.append("✓ GitHub Issues")
    print(_c(_DIM, "  Sources: " + "  |  ".join(lines)), file=file)


# ── Status / progress messages ───────────────────────────────────────────────

def print_status(msg: str) -> None:
    print(_c(_BLUE, f"  {msg}"), flush=True, file=_status_file)


def print_ok(msg: str) -> None:
    print(_c(_GREEN, f"  ✓ {msg}"), flush=True, file=_status_file)


def print_warn(msg: str) -> None:
    print(_c(_YELLOW, f"  ⚠ {msg}"), flush=True, file=sys.stderr)


def print_error(msg: str) -> None:
    print(_c(_RED, f"  ✗ {msg}"), flush=True, file=sys.stderr)


def print_info(msg: str) -> None:
    print(_c(_DIM, f"  {msg}"), flush=True, file=_status_file)


# ── Spinner ──────────────────────────────────────────────────────────────────

class Spinner:
    """A simple non-blocking CLI spinner.

    Usage::

        with Spinner("Scanning codebase"):
            long_running_task()
    """

    _FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, label: str, silent: bool = False) -> None:
        self._label = label
        self._silent = silent or not _status_file.isatty()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def __enter__(self) -> "Spinner":
        if not self._silent:
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()
        else:
            print_status(f"{self._label}…")
        return self

    def __exit__(self, *_) -> None:
        if self._thread:
            self._stop_event.set()
            self._thread.join()
            # Clear the spinner line
            _status_file.write("\r" + " " * (len(self._label) + 10) + "\r")
            _status_file.flush()

    def _spin(self) -> None:
        idx = 0
        while not self._stop_event.is_set():
            frame = self._FRAMES[idx % len(self._FRAMES)]
            _status_file.write(f"\r  {_c(_CYAN, frame)} {self._label}  ")
            _status_file.flush()
            time.sleep(0.08)
            idx += 1


# ── Diagnose table ───────────────────────────────────────────────────────────

def print_diagnose(config: dict, test_calls: bool = False) -> None:
    """Print configuration status. If test_calls=True, test each API key live."""
    rows = [
        ("GITHUB_TOKEN",           "GitHub API auth (5 000 req/hr vs 60)"),
        ("SCRAPECREATORS_API_KEY", "Reddit search"),
        ("XAI_API_KEY",            "X/Twitter via xAI Grok"),
        ("AUTH_TOKEN",             "X/Twitter cookie (alternative to xAI)"),
        ("CT0",                    "X/Twitter cookie pair"),
        ("STACKOVERFLOW_API_KEY",  "Stack Overflow (10 000/day vs 300)"),
    ]
    print(_c(_BOLD, "\n  /depradar  — configuration status\n"))
    for key, desc in rows:
        val = config.get(key)
        if val:
            status = _c(_GREEN, "✓ set")
            preview = f"({val[:4]}…)" if len(val) > 4 else ""
        else:
            status = _c(_DIM, "○ not set")
            preview = ""
        print(f"  {key:<30} {status}  {preview}  {_c(_DIM, desc)}")

    # Live API key validation (Fix 40)
    if test_calls:
        print()
        print(_c(_DIM, "  Testing API keys (live calls)…"))
        github_token = config.get("GITHUB_TOKEN")
        if github_token:
            _test_github_token(github_token)
        stackoverflow_key = config.get("STACKOVERFLOW_API_KEY")
        if stackoverflow_key:
            _test_stackoverflow_key(stackoverflow_key)

    print()
    src = config.get("_CONFIG_SOURCE", "env_only")
    print(_c(_DIM, f"  Config loaded from: {src}\n"))


def _test_github_token(token: str) -> None:
    """Test GitHub token by checking rate limit — prints result."""
    try:
        import urllib.request
        import json as _json
        req = urllib.request.Request(
            "https://api.github.com/rate_limit",
            headers={"Authorization": f"token {token}", "User-Agent": "depradar/2.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read().decode())
        remaining = data.get("rate", {}).get("remaining", "?")
        limit     = data.get("rate", {}).get("limit", "?")
        print(_c(_GREEN, f"  GitHub Token:      ✓ valid — {remaining}/{limit} requests remaining"))
    except Exception as exc:
        print(_c("\033[31m", f"  GitHub Token:      ✗ INVALID — {exc}"))


def _test_stackoverflow_key(key: str) -> None:
    """Test Stack Overflow key by checking quota — prints result."""
    try:
        import urllib.request
        import urllib.parse
        import json as _json
        params = urllib.parse.urlencode({"key": key, "pagesize": 1, "filter": "total"})
        url = f"https://api.stackexchange.com/2.3/questions?{params}&site=stackoverflow"
        req = urllib.request.Request(url, headers={"User-Agent": "depradar/2.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read().decode())
        quota = data.get("quota_remaining", "?")
        print(_c(_GREEN, f"  StackOverflow Key: ✓ valid — quota_remaining: {quota}"))
    except Exception as exc:
        print(_c("\033[31m", f"  StackOverflow Key: ✗ INVALID — {exc}"))
