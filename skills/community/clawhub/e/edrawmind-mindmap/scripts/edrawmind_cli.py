#!/usr/bin/env python3
"""
edrawmind-cli — Convert Markdown to professional mind maps.

A zero-dependency command-line tool for the EdrawMind (万兴脑图) Markdown-to-Mindmap
HTTP API. Reads Markdown from files or stdin, generates a mind map, and returns an
online editing URL with a thumbnail preview.

Usage examples:

    # Basic — convert a Markdown file
    python edrawmind_cli.py roadmap.md

    # Pipe from stdin
    echo "# AI\\n## ML\\n- Deep Learning" | python edrawmind_cli.py -

    # Choose layout, theme, and background
    python edrawmind_cli.py --layout 7 --theme 9 --background 4 timeline.md

    # Hand-drawn sketch style
    python edrawmind_cli.py --line-hand-drawn --fill pencil --background 9 notes.md

    # Open result in browser and save JSON response
    python edrawmind_cli.py --open --json -o result.json input.md

Copyright (c) 2026 Wondershare EdrawMind. All rights reserved.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import ssl
import sys
import textwrap
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import NoReturn, Optional, Sequence

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

__version__ = "1.0.0"
__author__ = "EdrawMind AI Team"

_CN_API_URL = "https://mindapi.edrawsoft.cn/api/ai/mind_agent/skills/markdown_to_mindmap"
_GLOBAL_API_URL = "https://api.edrawmind.com/api/ai/mind_agent/skills/markdown_to_mindmap"
_REQUEST_TIMEOUT = 120  # seconds
_PROBE_TIMEOUT = 3     # TCP connect timeout for region detection
_REGION_CACHE_TTL = 86400  # 24 hours

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ANSI colors (auto-disabled when output is not a TTY or NO_COLOR is set)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class _Color:
    """Minimal ANSI color helper respecting the NO_COLOR convention."""

    _on: bool = sys.stderr.isatty() and os.getenv("NO_COLOR") is None

    @classmethod
    def _w(cls, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if cls._on else text

    # fmt: off
    green  = classmethod(lambda cls, t: cls._w("32", t))      # type: ignore[assignment]
    yellow = classmethod(lambda cls, t: cls._w("33", t))      # type: ignore[assignment]
    red    = classmethod(lambda cls, t: cls._w("1;31", t))     # type: ignore[assignment]
    cyan   = classmethod(lambda cls, t: cls._w("36", t))       # type: ignore[assignment]
    bold   = classmethod(lambda cls, t: cls._w("1", t))        # type: ignore[assignment]
    dim    = classmethod(lambda cls, t: cls._w("2", t))        # type: ignore[assignment]
    # fmt: on


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Data models
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class FillStyle(str, Enum):
    """Node fill hand-drawn styles."""

    NONE = "none"
    PENCIL = "pencil"
    WATERCOLOR = "watercolor"
    CHARCOAL = "charcoal"
    PAINT = "paint"
    GRAFFITI = "graffiti"


@dataclass(frozen=True)
class ExtraInfo:
    """Server-side metadata attached to a successful response."""

    elapsed_ms: int
    request_id: str


@dataclass(frozen=True)
class MindmapResult:
    """Parsed successful API response."""

    file_url: str
    thumbnail_url: str
    extra_info: ExtraInfo

    @classmethod
    def from_response(cls, data: dict) -> MindmapResult:
        extra = data.get("extra_info", {})
        return cls(
            file_url=data["file_url"],
            thumbnail_url=data["thumbnail_url"],
            extra_info=ExtraInfo(
                elapsed_ms=extra.get("elapsed_ms", 0),
                request_id=extra.get("request_id", ""),
            ),
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Exceptions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class EdrawMindError(Exception):
    """Base exception for all EdrawMind CLI errors."""


class APIError(EdrawMindError):
    """Raised on non-success API responses (4xx / 5xx)."""

    def __init__(self, status: int, code: str | int, message: str) -> None:
        self.status = status
        self.code = code
        self.message = message
        super().__init__(f"HTTP {status} — [{code}] {message}")


class RateLimitError(APIError):
    """Raised specifically on HTTP 429 responses."""

    def __init__(
        self,
        code: str,
        message: str,
        retry_after: int | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(429, code, message)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Markdown validation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_RE_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")


def validate_markdown(text: str) -> list[str]:
    """Return a list of warning strings if *text* may not produce a good mind map."""
    warnings: list[str] = []
    lines = text.strip().splitlines()

    if not lines:
        warnings.append("Input is empty.")
        return warnings

    has_heading = any(ln.lstrip().startswith("#") for ln in lines)
    has_list = any(_RE_LIST_ITEM.match(ln) for ln in lines)

    if not has_heading:
        warnings.append(
            "No Markdown heading found. "
            "At least one heading (# or ##) is required."
        )
    if not has_list:
        warnings.append(
            "No list item found. "
            "At least one list item (-, *, +, or 1.) is required."
        )

    node_count = sum(
        1 for ln in lines if ln.lstrip().startswith("#") or _RE_LIST_ITEM.match(ln)
    )
    if node_count > 150:
        warnings.append(
            f"Found ~{node_count} nodes. "
            "Consider splitting into multiple maps (recommended ≤ 150)."
        )

    return warnings


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  API client
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def markdown_to_mindmap(
    text: str,
    *,
    api_url: str = _CN_API_URL,
    api_key: str | None = None,
    layout_type: int | None = None,
    theme_style: int | None = None,
    background: str | None = None,
    line_hand_drawn: bool | None = None,
    fill_hand_drawn: str | None = None,
    insecure: bool = False,
) -> MindmapResult:
    """Convert Markdown *text* to a mind map via the EdrawMind HTTP API.

    Parameters
    ----------
    text:
        Structured Markdown. Must contain at least one heading and one list item.
    api_url:
        Full API endpoint URL.
    api_key:
        Optional API key sent as ``X-API-Key``.
    layout_type:
        Layout preset ``1``–``12``.
    theme_style:
        Theme preset ``1``–``10``.
    background:
        Background preset ``"1"``–``"15"`` or ``"#RRGGBB"``.
    line_hand_drawn:
        Whether connection lines use the hand-drawn style.
    fill_hand_drawn:
        Node fill style (``none``/``pencil``/``watercolor``/``charcoal``/``paint``/``graffiti``).

    Returns
    -------
    MindmapResult
        Contains ``file_url``, ``thumbnail_url``, and ``extra_info``.

    Raises
    ------
    EdrawMindError
        On network, validation, or unexpected errors.
    APIError
        On non-success HTTP responses.
    RateLimitError
        On HTTP 429 rate-limit responses.
    """
    body: dict = {"text": text}
    if layout_type is not None:
        body["layout_type"] = layout_type
    if theme_style is not None:
        body["theme_style"] = theme_style
    if background is not None:
        body["background"] = background
    if line_hand_drawn is not None:
        body["line_hand_drawn"] = line_hand_drawn
    if fill_hand_drawn is not None:
        # The upstream API field intentionally uses this spelling.
        body["fill_hand_drawm"] = fill_hand_drawn

    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")

    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if api_key:
        headers["X-API-Key"] = api_key

    req = urllib.request.Request(
        api_url, data=payload, headers=headers, method="POST"
    )

    ssl_ctx: ssl.SSLContext | None = None
    if insecure:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, timeout=_REQUEST_TIMEOUT, context=ssl_ctx) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        _raise_from_http_error(exc)
    except urllib.error.URLError as exc:
        raise EdrawMindError(f"Connection failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise EdrawMindError(f"Invalid JSON in response: {exc}") from exc

    # The success envelope uses code == 0.
    resp_code = raw.get("code")
    if resp_code not in (0, 200, None):
        raise APIError(200, resp_code, raw.get("msg", "Unknown server error"))

    try:
        data = raw.get("data", raw)
        if not isinstance(data, dict):
            raise EdrawMindError(
                f"Unexpected response: 'data' is not an object (got {type(data).__name__})"
            )
        return MindmapResult.from_response(data)
    except (KeyError, AttributeError, TypeError) as exc:
        raise EdrawMindError(
            f"Unexpected response structure: {exc}"
        ) from exc


def _raise_from_http_error(exc: urllib.error.HTTPError) -> NoReturn:
    """Parse an HTTP error response and raise the appropriate exception."""
    try:
        body = json.loads(exc.read().decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise APIError(exc.code, exc.code, exc.reason or "Unknown error") from exc

    if exc.code == 429:
        raise RateLimitError(
            code=body.get("code", "rate_limited"),
            message=body.get("message", body.get("error", "Rate limited")),
            retry_after=body.get("retry_after_sec"),
        )

    raise APIError(
        exc.code,
        body.get("code", exc.code),
        body.get("msg", body.get("error", exc.reason or "Unknown error")),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Region detection & caching
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_REGION_CACHE_FILE = "region.json"


def _get_cache_dir() -> Path:
    """Return the platform-appropriate cache directory for EdrawMind."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    else:  # Linux / other Unix — respect XDG spec
        base = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return base / "edrawmind"


def _read_region_cache() -> str | None:
    """Return the cached API URL if still valid, otherwise None."""
    try:
        cache_file = _get_cache_dir() / _REGION_CACHE_FILE
        if not cache_file.is_file():
            return None
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        if time.time() - data.get("ts", 0) > _REGION_CACHE_TTL:
            return None
        return data.get("url") or None
    except Exception:
        return None


def _write_region_cache(url: str) -> None:
    """Persist the chosen API URL to cache. Silently ignores write errors."""
    try:
        cache_dir = _get_cache_dir()
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / _REGION_CACHE_FILE).write_text(
            json.dumps({"url": url, "ts": time.time()}),
            encoding="utf-8",
        )
    except Exception:
        pass


def _clear_region_cache() -> None:
    """Remove the cached region file so the next call re-probes."""
    try:
        cache_file = _get_cache_dir() / _REGION_CACHE_FILE
        if cache_file.is_file():
            cache_file.unlink()
    except Exception:
        pass


def _probe_fastest_url() -> str:
    """TCP-connect to both API hosts concurrently; return the faster one's URL.

    Falls back to ``_CN_API_URL`` if both probes fail or time out.
    """
    candidates = [
        (_CN_API_URL, "mindapi.edrawsoft.cn"),
        (_GLOBAL_API_URL, "api.edrawmind.com"),
    ]

    winner: list[str | None] = [None]
    failure_count: list[int] = [0]
    done = threading.Event()
    lock = threading.Lock()

    def _probe(url: str, host: str) -> None:
        try:
            s = socket.create_connection((host, 443), timeout=_PROBE_TIMEOUT)
            s.close()
            with lock:
                if winner[0] is None:
                    winner[0] = url
                    done.set()
        except Exception:
            with lock:
                failure_count[0] += 1
                if failure_count[0] == len(candidates):
                    done.set()  # all probes failed — unblock

    threads = [
        threading.Thread(target=_probe, args=(url, host), daemon=True)
        for url, host in candidates
    ]
    for t in threads:
        t.start()
    done.wait(timeout=_PROBE_TIMEOUT + 1)

    return winner[0] or _CN_API_URL  # fallback if all probes failed


def _resolve_api_url() -> str:
    """Return the best API URL: cached result or a fresh probe."""
    cached = _read_region_cache()
    if cached:
        return cached
    url = _probe_fastest_url()
    _write_region_cache(url)
    return url


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CLI helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_LAYOUT_NAMES: dict[int, str] = {
    1: "MindMap (双向导图)",
    2: "RightMap (右向导图)",
    3: "RightTree (右下树状图)",
    4: "DownTree (向下对称树状图)",
    5: "OrgDown (向下组织结构图)",
    6: "OrgTop (向上组织结构图)",
    7: "TimelineRight (向右时间轴)",
    8: "FishboneRight (右向鱼骨图)",
    9: "Sector (扇形放射图)",
    10: "BracketRight (右向括号图)",
    11: "TreeTable (树型表格)",
    12: "Matrix (矩阵图)",
}

_THEME_NAMES: dict[int, str] = {
    1: "Default (通用默认)",
    2: "Knowledge (知识学习)",
    3: "Vivid (活力时尚)",
    4: "Minimal (极简商务)",
    5: "Rainbow (彩虹创意)",
    6: "Paper (纸质文档)",
    7: "Fresh (清爽自然)",
    8: "Dark (暗色默认)",
    9: "Neon (霓虹科技)",
    10: "SciFi (科幻暗黑)",
}

_FILL_NAMES: dict[str, str] = {
    "none": "None (标准平面)",
    "pencil": "Pencil (铅笔素描)",
    "watercolor": "Watercolor (水彩晕染)",
    "charcoal": "Charcoal (木炭素描)",
    "paint": "Paint (油漆涂料)",
    "graffiti": "Graffiti (涂鸦网格)",
}


def _read_input(source: str) -> str:
    """Read Markdown text from a file path or ``-`` for stdin."""
    if source == "-":
        text = sys.stdin.read()
        if not text.strip():
            _die("No input received from stdin.")
        return text

    path = Path(source)
    if not path.is_file():
        _die(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def _info(msg: str) -> None:
    print(f"  {_Color.dim('→')} {msg}", file=sys.stderr)


def _warn(msg: str) -> None:
    print(f"  {_Color.yellow('⚠')} {msg}", file=sys.stderr)


def _die(msg: str, code: int = 1) -> NoReturn:
    print(f"\n  {_Color.red('✗')} {msg}\n", file=sys.stderr)
    raise SystemExit(code)


def _success(msg: str) -> None:
    print(f"  {_Color.green('✓')} {msg}", file=sys.stderr)


def _print_result(result: MindmapResult, *, quiet: bool = False) -> None:
    """Pretty-print the mind map result to stderr, URL to stdout."""
    if quiet:
        print(result.file_url)
        return

    print(file=sys.stderr)
    _success("Mind map generated successfully!")
    print(file=sys.stderr)
    print(
        f"    {_Color.bold('Edit URL')}:      {_Color.cyan(result.file_url)}",
        file=sys.stderr,
    )
    print(
        f"    {_Color.bold('Thumbnail')}:    {result.thumbnail_url}",
        file=sys.stderr,
    )
    ei = result.extra_info
    print(
        f"    {_Color.bold('Request ID')}:   {_Color.dim(ei.request_id)}",
        file=sys.stderr,
    )
    print(
        f"    {_Color.bold('Elapsed')}:      {_Color.dim(str(ei.elapsed_ms) + ' ms')}",
        file=sys.stderr,
    )
    print(file=sys.stderr)

    # Always emit the file_url on stdout so it can be piped.
    print(result.file_url)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Argument parser
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_LAYOUT_HELP = "\n".join(
    f"  {k:>2}  {v}" for k, v in _LAYOUT_NAMES.items()
)

_THEME_HELP = "\n".join(
    f"  {k:>2}  {v}" for k, v in _THEME_NAMES.items()
)

_FILL_HELP = ", ".join(_FILL_NAMES.keys())


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="edrawmind-cli",
        description=textwrap.dedent("""\
            Convert Markdown to a professional mind map via the EdrawMind API.

            Reads Markdown from --text, a file, or stdin (-), sends it to the
            EdrawMind API, and prints the online editing URL.
        """),
        epilog=textwrap.dedent(f"""\
            layout types (--layout):
            {_LAYOUT_HELP}

            theme styles (--theme):
            {_THEME_HELP}

            fill styles (--fill):
              {_FILL_HELP}

            examples:
              %(prog)s --text "# AI\\n## ML\\n- Deep Learning"
              %(prog)s --text "# AI\\n## ML\\n- DL" --layout 7 --theme 9
              %(prog)s notes.md
              %(prog)s --line-hand-drawn --fill pencil --background 9 sketch.md
              echo "# AI\\n## ML\\n- DL" | %(prog)s -
        """),

        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        default=None,
        help='Markdown file to convert, or "-" to read from stdin. '
             'Not needed when --text is used.',
    )
    parser.add_argument(
        "--text",
        metavar="MARKDOWN",
        dest="text",
        help='Inline Markdown content. Supports literal "\\n" for newlines. '
             'Mutually exclusive with FILE.',
    )

    # ── Styling options ──────────────────────────────────────────────────────
    style = parser.add_argument_group("styling options")

    style.add_argument(
        "-l", "--layout",
        type=int,
        choices=range(1, 13),
        metavar="N",
        dest="layout_type",
        help="Layout type 1–12 (default: 1 — MindMap).",
    )
    style.add_argument(
        "-t", "--theme",
        type=int,
        choices=range(1, 11),
        metavar="N",
        dest="theme_style",
        help="Theme style 1–10.",
    )
    style.add_argument(
        "-b", "--background",
        type=_validate_background,
        metavar="BG",
        help='Background: preset 1–15 or custom "#RRGGBB".',
    )
    style.add_argument(
        "--line-hand-drawn",
        action="store_true",
        default=None,
        help="Use hand-drawn connection lines.",
    )
    style.add_argument(
        "--fill",
        choices=[s.value for s in FillStyle],
        metavar="STYLE",
        dest="fill_hand_drawn",
        help=f"Node fill style: {_FILL_HELP}.",
    )

    # ── Connection options ───────────────────────────────────────────────────
    conn = parser.add_argument_group("connection options")

    conn.add_argument(
        "--api-key",
        metavar="KEY",
        help="API key for authentication.",
    )
    conn.add_argument(
        "--api-url",
        metavar="URL",
        help="API endpoint URL. Overrides --region.",
    )
    conn.add_argument(
        "--region",
        choices=["auto", "cn", "global"],
        default="auto",
        help=(
            "API region: 'auto' (default) probes CN and Global endpoints and caches "
            "the faster one for 24 h; 'cn' forces the mainland China endpoint; "
            "'global' forces the international endpoint."
        ),
    )

    # ── Output options ───────────────────────────────────────────────────────
    out = parser.add_argument_group("output options")

    out.add_argument(
        "-o", "--output",
        metavar="PATH",
        help="Save the JSON response to a file.",
    )
    out.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print full JSON response to stdout.",
    )
    out.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only print the file URL to stdout (no decoration).",
    )
    out.add_argument(
        "--open",
        action="store_true",
        dest="open_browser",
        help="Open the mind map URL in the default browser.",
    )
    out.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip Markdown input validation.",
    )
    out.add_argument(
        "--insecure",
        action="store_true",
        help="Skip SSL certificate verification (for dev/self-signed certs).",
    )
    out.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def _validate_background(value: str) -> str:
    """Argparse type validator for the --background option."""
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        return value
    if value.isdigit() and 1 <= int(value) <= 15:
        return value
    raise argparse.ArgumentTypeError(
        f"Invalid background '{value}'. Use a preset 1–15 or #RRGGBB."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Main entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Returns an exit code (0 = success)."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    # ── Resolve API configuration ────────────────────────────────────────────
    api_key: str | None = args.api_key
    if args.api_url:
        api_url: str = args.api_url
    elif args.region == "cn":
        api_url = _CN_API_URL
    elif args.region == "global":
        api_url = _GLOBAL_API_URL
    else:  # auto
        api_url = _resolve_api_url()

    # ── Read input ───────────────────────────────────────────────────────────
    if args.text and args.file:
        _die("Cannot use both --text and FILE. Choose one.")
    if args.text:
        text = args.text.replace("\\n", "\n")
        if not text.strip():
            _die("--text content is empty.")
    elif args.file:
        text = _read_input(args.file)
    else:
        _die("No input provided. Use --text or specify a FILE (or - for stdin).")

    # ── Validate ─────────────────────────────────────────────────────────────
    if not args.no_validate:
        warnings = validate_markdown(text)
        for w in warnings:
            _warn(w)
        if any("heading" in w.lower() or "empty" in w.lower() for w in warnings):
            _die(
                "Input does not look like valid Markdown for mind map generation. "
                "Use --no-validate to bypass."
            )

    # ── Resolve --line-hand-drawn sentinel ───────────────────────────────────
    line_hand_drawn: bool | None = True if args.line_hand_drawn else None

    # ── Call API ─────────────────────────────────────────────────────────────
    is_auto = args.region == "auto" and not args.api_url
    region_label = "auto → " if is_auto else ""
    _info(f"Sending {len(text):,} characters to {region_label}{api_url} …")

    def _call_api(url: str) -> MindmapResult:
        return markdown_to_mindmap(
            text,
            api_url=url,
            api_key=api_key,
            layout_type=args.layout_type,
            theme_style=args.theme_style,
            background=args.background,
            line_hand_drawn=line_hand_drawn,
            fill_hand_drawn=args.fill_hand_drawn,
            insecure=args.insecure,
        )

    try:
        result = _call_api(api_url)
    except RateLimitError as exc:
        retry = f" Retry after {exc.retry_after}s." if exc.retry_after else ""
        _die(f"Rate limited ({exc.code}).{retry}")
    except APIError as exc:
        _die(f"API error: {exc}")
    except EdrawMindError as exc:
        if not is_auto:
            _die(str(exc))
        # Auto mode: cached endpoint may be stale — clear cache and retry once.
        _warn(f"Connection failed ({exc}), re-probing endpoints …")
        _clear_region_cache()
        api_url = _resolve_api_url()
        _info(f"Retrying with {api_url} …")
        try:
            result = _call_api(api_url)
        except RateLimitError as exc2:
            retry = f" Retry after {exc2.retry_after}s." if exc2.retry_after else ""
            _die(f"Rate limited ({exc2.code}).{retry}")
        except APIError as exc2:
            _die(f"API error: {exc2}")
        except EdrawMindError as exc2:
            _die(str(exc2))

    # ── Output ───────────────────────────────────────────────────────────────
    response_dict = asdict(result)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(
            json.dumps(response_dict, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        _info(f"Response saved to {out_path}")

    if args.json_output:
        print(json.dumps(response_dict, indent=2, ensure_ascii=False))
    else:
        _print_result(result, quiet=args.quiet)

    if args.open_browser:
        _info("Opening in browser …")
        webbrowser.open(result.file_url)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
