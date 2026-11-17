#!/usr/bin/env python3
"""AGY -> Codex Plus image adapter (built-in ``image_gen`` only).

Dispatches a single slide-image generation job from AGY to the Codex CLI, using
the already-authenticated local ChatGPT/Codex subscription session. Codex acts
purely as an image renderer:

    AGY
      -> codex_image_adapter.py
      -> codex exec --json           (subscription session, no API key)
      -> $imagegen skill
      -> built-in image_gen tool
      -> $CODEX_HOME/generated_images/<thread_id>/<artifact>.png
      -> move/copy into the workspace output path
      -> structured result
      -> AGY

Design constraints enforced here (see ``docs/codex-image-runtime.md``,
``docs/agent-routing.md`` and ``docs/oauth-subscription-runtime.md``):

* Subscription / OAuth only. The adapter never reads, copies, stores or
  forwards OAuth tokens. It relies on the already-authenticated ``codex`` CLI
  session. API-key style environment variables (``OPENAI_API_KEY`` etc.) are
  stripped from the child environment so a billed API fallback cannot silently
  happen.
* Built-in ``image_gen`` only. The worker prompt forbids the CLI/API fallback
  (``scripts/image_gen.py`` + ``OPENAI_API_KEY``). If the built-in tool is not
  available the adapter reports ``IMAGE_BACKEND_UNAVAILABLE`` and stops; it does
  not fall back to a paid API.
* Codex is a renderer, never an orchestrator. The prompt forbids editing slide
  content, editing source files, writing code, calling Kiro, assembling PPTX or
  advancing the deck workflow.
* Robust artifact discovery. The adapter records the state of
  ``$CODEX_HOME/generated_images/`` before the turn, runs exactly one Codex
  image turn, then finds the artifact the turn produced -- preferring an
  explicit path reported by Codex, falling back to a safe before/after diff
  scoped to the turn's ``thread_id``. If two or more valid new artifacts appear
  it never guesses; it reports ``IMAGE_ARTIFACT_AMBIGUOUS`` with the candidate
  paths and lets AGY choose. It validates the artifact is a real raster image
  before moving/copying it into the caller's workspace output path.
* Artifact safety. Output paths must resolve inside the workspace/repository
  root; path traversal and out-of-root writes are refused. Existing files are
  never overwritten unless the operation is an explicit ``regenerate``.
* Control returns to AGY. The adapter performs exactly one render turn, then
  reports a structured result and exits.

Usage::

    python3 codex_image_adapter.py --input job.json --output result.json
    cat job.json | python3 codex_image_adapter.py

Request JSON::

    {
      "slide_id": "slide_03",
      "operation": "generate",              # generate | regenerate | probe
      "prompt": "full image prompt",         # required for generate/regenerate
      "output_path": "origin_image/slide_03.png",
      "aspect_ratio": "16:9",
      "workspace_root": "/abs/path",         # defaults to cwd
      "command": ["codex", "exec", "--json", "--skip-git-repo-check"],
      "timeout_seconds": 300
    }

Success response JSON::

    {
      "status": "completed",
      "slide_id": "slide_03",
      "operation": "generate",
      "backend": "codex_builtin_imagegen",
      "output_path": "origin_image/slide_03.png",
      "warnings": [],
      "diagnostics": {"auth": "chatgpt_cli_session", "api_fallback_used": false}
    }

Backend unavailable response JSON::

    {
      "status": "error",
      "error_code": "IMAGE_BACKEND_UNAVAILABLE",
      "slide_id": "slide_03"
    }
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

RESULT_SCHEMA = "agy-ppt/codex-image-adapter-result/1"
REQUEST_SCHEMA = "agy-ppt/codex-image-adapter-request/1"

BACKEND = "codex_builtin_imagegen"

# Default Codex CLI invocation. `exec --json` is the non-interactive path; the
# prompt is delivered on stdin. `--skip-git-repo-check` keeps it usable inside
# any workspace, not only a git repo.
DEFAULT_COMMAND: tuple[str, ...] = ("codex", "exec", "--json", "--skip-git-repo-check")

DEFAULT_TIMEOUT_SECONDS = 300.0
DEFAULT_CANCEL_GRACE_SECONDS = 10.0

# Operations
OP_GENERATE = "generate"
OP_REGENERATE = "regenerate"
OP_PROBE = "probe"
SUPPORTED_OPERATIONS = (OP_GENERATE, OP_REGENERATE, OP_PROBE)
# Operations that create/replace an artifact (probe does not).
RENDER_OPERATIONS = (OP_GENERATE, OP_REGENERATE)

# Status values
STATUS_COMPLETED = "completed"
STATUS_ERROR = "error"
STATUS_AVAILABLE = "available"
STATUS_UNAVAILABLE = "unavailable"

# Error contract codes.
ERROR_BACKEND_UNAVAILABLE = "IMAGE_BACKEND_UNAVAILABLE"
ERROR_CODEX_CLI_UNAVAILABLE = "CODEX_CLI_UNAVAILABLE"
ERROR_CODEX_AUTH_UNAVAILABLE = "CODEX_AUTH_UNAVAILABLE"
ERROR_GENERATION_FAILED = "IMAGE_GENERATION_FAILED"
ERROR_ARTIFACT_NOT_FOUND = "IMAGE_ARTIFACT_NOT_FOUND"
ERROR_ARTIFACT_AMBIGUOUS = "IMAGE_ARTIFACT_AMBIGUOUS"
ERROR_OUTPUT_INVALID = "IMAGE_OUTPUT_INVALID"
ERROR_OUTPUT_PATH_CONFLICT = "IMAGE_OUTPUT_PATH_CONFLICT"
ERROR_TIMEOUT = "CODEX_TIMEOUT"
ERROR_INVALID_REQUEST = "IMAGE_TASK_INVALID"

# Environment variables that would turn this subscription-only path into a
# billed API path. Removed from the Codex child environment. Only the *name* is
# ever reported, never the value.
BLOCKED_ENV_VARS = (
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "CODEX_PPT_API_KEY",
    "CODEX_PPT_IMAGE_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "OPENAI_BASE_URL",
)
BLOCKED_ENV_PATTERN = re.compile(
    r"(?i)(?:^|_)(?:API_KEY|APIKEY|ACCESS_TOKEN|REFRESH_TOKEN|ID_TOKEN|BEARER_TOKEN|SESSION_TOKEN)$"
)

# Recognised raster image extensions / magic-number signatures.
ALLOWED_IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".webp"})
_IMAGE_ARTIFACT_PATH = re.compile(r"(?i)([^\s\"'`]+\.(?:png|jpe?g|webp))")

# Signals in Codex output that the built-in image_gen tool is not available in
# the current runtime. Matched case-insensitively against agent text.
_BACKEND_UNAVAILABLE_MARKERS = (
    ERROR_BACKEND_UNAVAILABLE,
    "image_gen tool is not available",
    "image_gen is not available",
    "image_gen tool is unavailable",
    "image_gen is unavailable",
    "built-in image_gen unavailable",
    "no image_gen tool",
    "image generation tool is unavailable",
)
_AUTH_FAILURE_MARKERS = (
    "not logged in",
    "please run codex login",
    "authentication required",
    "unauthorized",
    "401 unauthorized",
    "session expired",
    "login expired",
)

# Redaction for anything echoed back to AGY.
_REDACTIONS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._\-]{12,}"), r"\1 [REDACTED]"),
    (re.compile(r"\bsk-[A-Za-z0-9._\-]{12,}"), "[REDACTED]"),
    (
        re.compile(
            r"(?i)(\"?(?:access|refresh|id|session)_token\"?\s*[:=]\s*\"?)[A-Za-z0-9._\-]{12,}"
        ),
        r"\1[REDACTED]",
    ),
    (re.compile(r"(?i)(\"?api[_-]?key\"?\s*[:=]\s*\"?)[A-Za-z0-9._\-]{12,}"), r"\1[REDACTED]"),
)


def now_iso() -> str:
    """UTC timestamp, matching the style used by the other skill scripts."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def redact(text: str) -> str:
    """Strip credential-looking substrings from anything echoed back to AGY."""
    if not text:
        return text
    for pattern, replacement in _REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def sanitize_env(base: dict[str, str] | None = None) -> tuple[dict[str, str], list[str]]:
    """Return a child environment with API-key style variables removed.

    Only variable *names* are reported, never values.
    """
    source = dict(os.environ if base is None else base)
    removed: list[str] = []
    for name in list(source):
        if name in BLOCKED_ENV_VARS or BLOCKED_ENV_PATTERN.search(name):
            source.pop(name, None)
            removed.append(name)
    return source, sorted(removed)


def codex_home(env: dict[str, str] | None = None) -> Path:
    """Resolve ``$CODEX_HOME`` (default ``~/.codex``)."""
    source = os.environ if env is None else env
    value = source.get("CODEX_HOME")
    if value:
        return Path(value).expanduser()
    return Path(source.get("HOME", os.path.expanduser("~"))).expanduser() / ".codex"


def generated_images_root(env: dict[str, str] | None = None) -> Path:
    return codex_home(env) / "generated_images"


# ---------------------------------------------------------------------------
# Image validation
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ImageInfo:
    """Minimal decoded metadata for a raster image."""

    fmt: str
    width: int
    height: int


def sniff_image(path: Path) -> ImageInfo | None:
    """Return :class:`ImageInfo` for a supported raster image, else ``None``.

    Uses magic numbers and header parsing only -- no third-party image library
    is required, and this is deliberately *not* a substitute for image
    generation (it never draws or rewrites pixels).
    """
    try:
        with path.open("rb") as handle:
            head = handle.read(32)
    except OSError:
        return None
    if len(head) < 12:
        return None

    # PNG
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        if head[12:16] == b"IHDR":
            width, height = struct.unpack(">II", head[16:24])
            return ImageInfo("png", width, height)
        return ImageInfo("png", 0, 0)

    # JPEG
    if head[0:2] == b"\xff\xd8":
        dims = _jpeg_dimensions(path)
        if dims is not None:
            return ImageInfo("jpeg", dims[0], dims[1])
        return ImageInfo("jpeg", 0, 0)

    # WebP (RIFF....WEBP)
    if head[0:4] == b"RIFF" and head[8:12] == b"WEBP":
        dims = _webp_dimensions(head)
        if dims is not None:
            return ImageInfo("webp", dims[0], dims[1])
        return ImageInfo("webp", 0, 0)

    return None


def _jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as handle:
            if handle.read(2) != b"\xff\xd8":
                return None
            while True:
                marker = handle.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    return None
                code = marker[1]
                if code in (0xD8, 0xD9):
                    continue
                length_bytes = handle.read(2)
                if len(length_bytes) < 2:
                    return None
                length = struct.unpack(">H", length_bytes)[0]
                # SOF markers carry the frame dimensions.
                if 0xC0 <= code <= 0xCF and code not in (0xC4, 0xC8, 0xCC):
                    data = handle.read(5)
                    if len(data) < 5:
                        return None
                    height, width = struct.unpack(">HH", data[1:5])
                    return width, height
                handle.seek(length - 2, os.SEEK_CUR)
    except (OSError, struct.error):
        return None


def _webp_dimensions(head: bytes) -> tuple[int, int] | None:
    try:
        chunk = head[12:16]
        if chunk == b"VP8 ":
            # lossy: dimensions live a bit deeper; header truncated here.
            if len(head) >= 30:
                width = struct.unpack("<H", head[26:28])[0] & 0x3FFF
                height = struct.unpack("<H", head[28:30])[0] & 0x3FFF
                return width, height
        elif chunk == b"VP8L":
            if len(head) >= 25:
                bits = struct.unpack("<I", head[21:25])[0]
                width = (bits & 0x3FFF) + 1
                height = ((bits >> 14) & 0x3FFF) + 1
                return width, height
    except (struct.error, IndexError):
        return None
    return None


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------
class InvalidRequestError(ValueError):
    """The AGY job could not be parsed into a valid render request."""


@dataclass(frozen=True)
class ImageRequest:
    operation: str
    slide_id: str = ""
    prompt: str = ""
    output_path: str = ""
    aspect_ratio: str = ""
    workspace_root: str = field(default_factory=os.getcwd)
    command: tuple[str, ...] = DEFAULT_COMMAND
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    cancel_grace_seconds: float = DEFAULT_CANCEL_GRACE_SECONDS
    env: dict[str, str] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImageRequest":
        if not isinstance(data, dict):
            raise InvalidRequestError("request must be a JSON object")

        operation = str(data.get("operation") or OP_GENERATE).strip().lower()
        if operation not in SUPPORTED_OPERATIONS:
            raise InvalidRequestError(
                f"unsupported operation {operation!r}; expected one of "
                f"{', '.join(SUPPORTED_OPERATIONS)}"
            )

        workspace_root = str(data.get("workspace_root") or data.get("repository_root") or os.getcwd())

        command_value = data.get("command")
        if command_value is None:
            command = DEFAULT_COMMAND
        elif isinstance(command_value, (list, tuple)) and all(
            isinstance(part, str) for part in command_value
        ):
            if not command_value:
                raise InvalidRequestError("command must not be empty")
            command = tuple(command_value)
        else:
            raise InvalidRequestError("command must be a list of strings")

        slide_id = str(data.get("slide_id") or "").strip()
        prompt = str(data.get("prompt") or "").strip()
        output_path = str(data.get("output_path") or "").strip()
        aspect_ratio = str(data.get("aspect_ratio") or "").strip()

        if operation in RENDER_OPERATIONS:
            if not prompt:
                raise InvalidRequestError(f"{operation} requires a non-empty prompt")
            if not output_path:
                raise InvalidRequestError(f"{operation} requires an output_path")

        timeout_seconds = _coerce_positive_float(
            data.get("timeout_seconds"), DEFAULT_TIMEOUT_SECONDS, "timeout_seconds"
        )
        cancel_grace_seconds = _coerce_positive_float(
            data.get("cancel_grace_seconds"),
            DEFAULT_CANCEL_GRACE_SECONDS,
            "cancel_grace_seconds",
        )

        env = data.get("env")
        if env is not None and not isinstance(env, dict):
            raise InvalidRequestError("env must be an object of string values")

        return cls(
            operation=operation,
            slide_id=slide_id,
            prompt=prompt,
            output_path=output_path,
            aspect_ratio=aspect_ratio,
            workspace_root=workspace_root,
            command=command,
            timeout_seconds=timeout_seconds,
            cancel_grace_seconds=cancel_grace_seconds,
            env=dict(env) if isinstance(env, dict) else None,
        )


def _coerce_positive_float(value: Any, default: float, name: str) -> float:
    if value is None:
        return default
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise InvalidRequestError(f"{name} must be a number") from exc
    if result <= 0:
        raise InvalidRequestError(f"{name} must be positive")
    return result


# ---------------------------------------------------------------------------
# Output-path safety
# ---------------------------------------------------------------------------
class OutputPathError(Exception):
    """The requested output path is unsafe or conflicts with an existing file."""

    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


def resolve_output_path(workspace_root: str, output_path: str, operation: str) -> Path:
    """Resolve and validate the caller's output path.

    * Must resolve inside the workspace root (rejects traversal / absolute
      escapes).
    * Parent directories are created.
    * An existing file is only accepted when the operation is ``regenerate``.
    """
    if not output_path:
        raise OutputPathError(ERROR_OUTPUT_INVALID, "output_path is required")

    root = Path(os.path.realpath(os.path.expanduser(workspace_root or os.getcwd())))
    raw = Path(os.path.expanduser(output_path))
    candidate = raw if raw.is_absolute() else root / raw

    # Resolve without requiring the file to exist, then confirm containment.
    resolved = Path(os.path.normpath(str(candidate)))
    try:
        resolved_real = Path(os.path.realpath(str(resolved)))
    except OSError:  # pragma: no cover - defensive
        resolved_real = resolved

    # Containment check against the real root. Use the resolved parent so a
    # not-yet-created file still validates correctly.
    check_target = resolved_real
    if not resolved.exists():
        parent_real = Path(os.path.realpath(str(resolved.parent)))
        check_target = parent_real / resolved.name

    if check_target != root and root not in check_target.parents:
        raise OutputPathError(
            ERROR_OUTPUT_INVALID,
            f"output_path {output_path!r} resolves outside the workspace root",
        )

    if resolved.exists():
        if resolved.is_dir():
            raise OutputPathError(
                ERROR_OUTPUT_INVALID, f"output_path {output_path!r} is a directory"
            )
        if operation != OP_REGENERATE:
            raise OutputPathError(
                ERROR_OUTPUT_PATH_CONFLICT,
                f"output_path {output_path!r} already exists; use operation "
                "'regenerate' to replace it",
            )

    return resolved


# ---------------------------------------------------------------------------
# Worker prompt
# ---------------------------------------------------------------------------
PROMPT_BOUNDARY = (
    "You are Codex acting only as a slide-image renderer for the AGY PPT workflow.\n"
    "\n"
    "Hard rules (obey all):\n"
    "- Use the $imagegen skill and the built-in `image_gen` tool ONLY.\n"
    "- Do NOT use scripts/image_gen.py, the OpenAI Images API, OPENAI_API_KEY,\n"
    "  or any paid API fallback. Never switch backend.\n"
    "- If the built-in `image_gen` tool is unavailable, reply with exactly\n"
    "  IMAGE_BACKEND_UNAVAILABLE and stop. Do NOT fall back to any API.\n"
    "- Do NOT modify slide content, outline, deck spec, slide jobs, or any\n"
    "  source file. Do NOT rewrite the presentation copy.\n"
    "- Do NOT write, run, or edit code. Do NOT call Kiro. Do NOT assemble PPTX.\n"
    "- Do NOT decide the next workflow phase. You only render one image.\n"
    "- Generate exactly ONE image in this turn.\n"
    "- After generating, report the absolute path of the generated image file\n"
    "  on its own line prefixed with 'ARTIFACT_PATH: '.\n"
)


def build_worker_prompt(request: ImageRequest) -> str:
    """Compose the authoritative worker prompt sent to Codex.

    The AGY-provided slide prompt is authoritative; the adapter only wraps it
    with the renderer boundary. It never rewrites the slide content.
    """
    lines = [PROMPT_BOUNDARY, ""]
    if request.slide_id:
        lines.append(f"Slide id: {request.slide_id}")
    verb = "Regenerate" if request.operation == OP_REGENERATE else "Generate"
    lines.append(f"Operation: {verb.lower()} a single slide image.")
    if request.aspect_ratio:
        lines.append(
            f"Requested aspect ratio: {request.aspect_ratio} (landscape slide). "
            "If the tool cannot produce this exact ratio, keep the closest "
            "supported landscape size; do not distort or re-draw."
        )
    lines.append("")
    lines.append("Authoritative image prompt (do not rewrite the content):")
    lines.append(request.prompt)
    lines.append("")
    lines.append(
        "When done, output one line 'ARTIFACT_PATH: <absolute path to the "
        "generated PNG>' so the caller can locate the artifact."
    )
    return "\n".join(lines)


def build_probe_prompt() -> str:
    """A tiny prompt that only asks Codex whether the built-in tool exists.

    It must not generate an image; it is a capability check only.
    """
    return (
        "You are Codex. Capability check only. Do NOT generate any image.\n"
        "Do NOT use scripts/image_gen.py, any API, or OPENAI_API_KEY.\n"
        "Question: is the built-in `image_gen` tool from the $imagegen skill\n"
        "available to you right now?\n"
        "Reply with exactly one line:\n"
        "- IMAGE_BACKEND_AVAILABLE if the built-in image_gen tool is available.\n"
        "- IMAGE_BACKEND_UNAVAILABLE if it is not.\n"
    )


# ---------------------------------------------------------------------------
# Codex process invocation
# ---------------------------------------------------------------------------
class CodexUnavailableError(Exception):
    """The codex executable could not be started."""


@dataclass
class CodexRun:
    """Outcome of one ``codex exec`` invocation."""

    returncode: int | None
    events: list[dict[str, Any]]
    agent_text: str
    stderr: str
    timed_out: bool
    thread_id: str = ""
    reported_paths: list[str] = field(default_factory=list)
    command: list[str] = field(default_factory=list)


def _parse_events(stdout: str) -> tuple[list[dict[str, Any]], str, str, list[str]]:
    """Parse Codex ``--json`` JSONL output.

    Returns (events, agent_text, thread_id, reported_artifact_paths).
    """
    events: list[dict[str, Any]] = []
    agent_chunks: list[str] = []
    thread_id = ""
    reported: list[str] = []

    for line in stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        events.append(event)

        etype = event.get("type")
        if etype == "thread.started" and event.get("thread_id"):
            thread_id = str(event["thread_id"])
        elif etype == "item.completed":
            item = event.get("item") if isinstance(event.get("item"), dict) else {}
            if item.get("type") == "agent_message" and item.get("text"):
                agent_chunks.append(str(item["text"]))
        elif etype in ("item.updated", "item.started"):
            item = event.get("item") if isinstance(event.get("item"), dict) else {}
            if item.get("type") == "agent_message" and item.get("text"):
                agent_chunks.append(str(item["text"]))

    agent_text = "\n".join(agent_chunks)
    for match in _IMAGE_ARTIFACT_PATH.finditer(agent_text):
        reported.append(match.group(1))
    return events, agent_text, thread_id, reported


def run_codex(
    command: Sequence[str],
    prompt: str,
    cwd: str,
    env: dict[str, str],
    timeout: float,
    cancel_grace: float,
) -> CodexRun:
    """Run one ``codex exec`` turn with the prompt delivered on stdin.

    The child runs in its own process group so any helper processes are cleaned
    up together on timeout.
    """
    try:
        process = subprocess.Popen(  # noqa: S603 - command originates from the AGY job
            list(command),
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
    except FileNotFoundError as exc:
        raise CodexUnavailableError(f"codex executable not found: {command[0]}") from exc
    except OSError as exc:
        raise CodexUnavailableError(f"failed to start codex: {exc}") from exc

    timed_out = False
    try:
        stdout, stderr = process.communicate(input=prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _terminate_group(process, cancel_grace)
        try:
            stdout, stderr = process.communicate(timeout=cancel_grace)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive
            stdout, stderr = "", ""

    events, agent_text, thread_id, reported = _parse_events(stdout or "")
    return CodexRun(
        returncode=process.returncode,
        events=events,
        agent_text=redact(agent_text),
        stderr=redact((stderr or "").strip()[:4000]),
        timed_out=timed_out,
        thread_id=thread_id,
        reported_paths=reported,
        command=list(command),
    )


def _terminate_group(process: "subprocess.Popen[str]", grace: float) -> None:
    if process.poll() is not None:
        return
    _signal_group(process, signal.SIGTERM)
    try:
        process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        _signal_group(process, signal.SIGKILL)
        try:
            process.wait(timeout=grace)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive
            pass


def _signal_group(process: "subprocess.Popen[str]", sig: int) -> None:
    if process.poll() is not None:
        return
    if hasattr(os, "killpg"):
        try:
            os.killpg(os.getpgid(process.pid), sig)
            return
        except (ProcessLookupError, PermissionError, OSError):
            pass
    try:
        process.send_signal(sig)
    except (ProcessLookupError, OSError):  # pragma: no cover - defensive
        pass


# ---------------------------------------------------------------------------
# Artifact discovery
# ---------------------------------------------------------------------------
def snapshot_generated_images(root: Path) -> dict[str, float]:
    """Map every existing artifact under ``root`` to its mtime.

    Used for the before/after diff when Codex does not report an explicit path.
    """
    snapshot: dict[str, float] = {}
    if not root.exists():
        return snapshot
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in ALLOWED_IMAGE_SUFFIXES:
            try:
                snapshot[str(path)] = path.stat().st_mtime
            except OSError:  # pragma: no cover - defensive
                continue
    return snapshot


@dataclass(frozen=True)
class ArtifactDiscovery:
    path: Path | None
    method: str
    candidates: list[str] = field(default_factory=list)
    ambiguous: bool = False


def discover_artifact(
    run: CodexRun,
    images_root: Path,
    before: dict[str, float],
) -> ArtifactDiscovery:
    """Locate the artifact produced by this turn.

    Preference order:

    1. An explicit ``ARTIFACT_PATH:`` / path reported by Codex, if it exists,
       is a supported image, and lives under ``$CODEX_HOME/generated_images``.
    2. A safe before/after diff scoped to the turn's ``thread_id`` directory.
    3. A before/after diff across the whole generated_images root.
    """
    # 1. Explicit path reported by Codex.
    for reported in run.reported_paths:
        cleaned = reported.strip()
        # Tolerate a stray "ARTIFACT_PATH:" prefix if it slipped through.
        cleaned = re.sub(r"(?i)^artifact_path\s*:\s*", "", cleaned).strip().strip("'\"")
        candidate = Path(os.path.expanduser(cleaned))
        if not candidate.is_absolute():
            candidate = images_root / cleaned
        candidate = Path(os.path.normpath(str(candidate)))
        if candidate.is_file() and candidate.suffix.lower() in ALLOWED_IMAGE_SUFFIXES:
            return ArtifactDiscovery(candidate, "explicit_reported_path", [str(candidate)])

    # 2. before/after diff, scoped to this turn's thread dir when known.
    scoped_root = images_root
    method = "thread_scoped_diff"
    if run.thread_id:
        thread_dir = images_root / run.thread_id
        if thread_dir.exists():
            scoped_root = thread_dir
        else:
            method = "root_diff"
    else:
        method = "root_diff"

    after = snapshot_generated_images(scoped_root)
    new_or_changed = [
        path
        for path, mtime in after.items()
        if path not in before or mtime > before.get(path, 0.0)
    ]
    # Only keep valid images.
    valid = [p for p in new_or_changed if sniff_image(Path(p)) is not None]

    if not valid:
        return ArtifactDiscovery(None, method, sorted(new_or_changed), ambiguous=False)
    if len(valid) == 1:
        return ArtifactDiscovery(Path(valid[0]), method, valid)

    # Two or more valid new artifacts: ambiguous. The adapter never guesses
    # (not newest, not largest, not by filename). It reports the candidates and
    # leaves the choice to AGY.
    valid_sorted = sorted(valid)
    return ArtifactDiscovery(None, method, valid_sorted, ambiguous=True)


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------
@dataclass
class AdapterResult:
    status: str
    slide_id: str = ""
    operation: str = ""
    error_code: str | None = None
    error_message: str = ""
    backend: str | None = None
    output_path: str = ""
    warnings: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema": RESULT_SCHEMA,
            "status": self.status,
            "control": "returned_to_agy",
            "next_step_owner": "AGY",
            "slide_id": self.slide_id,
            "operation": self.operation,
            "timestamp": now_iso(),
        }
        if self.error_code is not None:
            payload["error_code"] = self.error_code
        if self.error_message:
            payload["error_message"] = redact(self.error_message)
        if self.backend is not None:
            payload["backend"] = self.backend
        if self.output_path:
            payload["output_path"] = self.output_path
        payload["warnings"] = list(self.warnings)
        payload["diagnostics"] = self.diagnostics
        return payload


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------
class CodexImageAdapter:
    """Dispatches one Codex image render / probe turn and returns a result."""

    def __init__(self, request: ImageRequest) -> None:
        self.request = request
        self.env, self.stripped_env = sanitize_env(request.env)
        self.images_root = generated_images_root(self.env)

    def base_diagnostics(self) -> dict[str, Any]:
        return {
            "auth": "chatgpt_cli_session",
            "api_fallback_used": False,
            "credential_env_stripped": self.stripped_env,
            "command": list(self.request.command),
            "codex_home": str(codex_home(self.env)),
            "generated_images_root": str(self.images_root),
        }

    def run(self) -> AdapterResult:
        if self.request.operation == OP_PROBE:
            return self._run_probe()
        return self._run_render()

    # -- probe -------------------------------------------------------------
    def _run_probe(self) -> AdapterResult:
        diagnostics = self.base_diagnostics()
        try:
            run = run_codex(
                self.request.command,
                build_probe_prompt(),
                cwd=self.request.workspace_root,
                env=self.env,
                timeout=self.request.timeout_seconds,
                cancel_grace=self.request.cancel_grace_seconds,
            )
        except CodexUnavailableError as exc:
            diagnostics["detail"] = str(exc)
            return AdapterResult(
                status=STATUS_UNAVAILABLE,
                operation=OP_PROBE,
                error_code=ERROR_CODEX_CLI_UNAVAILABLE,
                error_message=str(exc),
                diagnostics=diagnostics,
            )

        diagnostics["thread_id"] = run.thread_id
        diagnostics["codex_returncode"] = run.returncode

        if run.timed_out:
            return AdapterResult(
                status=STATUS_UNAVAILABLE,
                operation=OP_PROBE,
                error_code=ERROR_TIMEOUT,
                error_message="codex probe timed out",
                diagnostics=diagnostics,
            )

        text_lower = run.agent_text.lower()
        if _matches_any(text_lower, _AUTH_FAILURE_MARKERS) or _stderr_auth_failure(run.stderr):
            return AdapterResult(
                status=STATUS_UNAVAILABLE,
                operation=OP_PROBE,
                error_code=ERROR_CODEX_AUTH_UNAVAILABLE,
                error_message="codex session is not authenticated",
                diagnostics=diagnostics,
            )
        if "image_backend_available" in text_lower and not _matches_any(
            text_lower, _BACKEND_UNAVAILABLE_MARKERS
        ):
            return AdapterResult(
                status=STATUS_AVAILABLE,
                operation=OP_PROBE,
                backend=BACKEND,
                diagnostics=diagnostics,
            )
        if _matches_any(text_lower, _BACKEND_UNAVAILABLE_MARKERS):
            return AdapterResult(
                status=STATUS_UNAVAILABLE,
                operation=OP_PROBE,
                error_code=ERROR_BACKEND_UNAVAILABLE,
                diagnostics=diagnostics,
            )
        # Inconclusive probe -> treat as unavailable, never assume a paid path.
        diagnostics["probe_text"] = run.agent_text[:500]
        return AdapterResult(
            status=STATUS_UNAVAILABLE,
            operation=OP_PROBE,
            error_code=ERROR_BACKEND_UNAVAILABLE,
            error_message="could not confirm built-in image_gen availability",
            diagnostics=diagnostics,
        )

    # -- render ------------------------------------------------------------
    def _run_render(self) -> AdapterResult:
        request = self.request
        diagnostics = self.base_diagnostics()

        # Validate the output path before spending a Codex turn.
        try:
            output_target = resolve_output_path(
                request.workspace_root, request.output_path, request.operation
            )
        except OutputPathError as exc:
            return AdapterResult(
                status=STATUS_ERROR,
                slide_id=request.slide_id,
                operation=request.operation,
                error_code=exc.error_code,
                error_message=str(exc),
                diagnostics=diagnostics,
            )

        before = snapshot_generated_images(self.images_root)

        try:
            run = run_codex(
                request.command,
                build_worker_prompt(request),
                cwd=request.workspace_root,
                env=self.env,
                timeout=request.timeout_seconds,
                cancel_grace=request.cancel_grace_seconds,
            )
        except CodexUnavailableError as exc:
            diagnostics["detail"] = str(exc)
            return AdapterResult(
                status=STATUS_ERROR,
                slide_id=request.slide_id,
                operation=request.operation,
                error_code=ERROR_CODEX_CLI_UNAVAILABLE,
                error_message=str(exc),
                diagnostics=diagnostics,
            )

        diagnostics["thread_id"] = run.thread_id
        diagnostics["codex_returncode"] = run.returncode

        if run.timed_out:
            return self._error(request, ERROR_TIMEOUT, "codex render timed out", diagnostics)

        text_lower = run.agent_text.lower()
        if _matches_any(text_lower, _AUTH_FAILURE_MARKERS) or _stderr_auth_failure(run.stderr):
            return self._error(
                request,
                ERROR_CODEX_AUTH_UNAVAILABLE,
                "codex session is not authenticated",
                diagnostics,
            )
        if _matches_any(text_lower, _BACKEND_UNAVAILABLE_MARKERS):
            return self._error(
                request, ERROR_BACKEND_UNAVAILABLE, "built-in image_gen unavailable", diagnostics
            )
        if run.returncode not in (0, None):
            diagnostics["stderr_tail"] = run.stderr[-800:]
            return self._error(
                request,
                ERROR_GENERATION_FAILED,
                f"codex exited with code {run.returncode}",
                diagnostics,
            )

        discovery = discover_artifact(run, self.images_root, before)
        diagnostics["artifact_discovery"] = {
            "method": discovery.method,
            "candidates": discovery.candidates[:10],
            "ambiguous": discovery.ambiguous,
        }
        if discovery.ambiguous:
            # Two or more valid candidates. Do not guess: report and hand to AGY.
            return self._error(
                request,
                ERROR_ARTIFACT_AMBIGUOUS,
                "multiple valid image artifacts were produced; AGY must choose",
                diagnostics,
            )
        if discovery.path is None:
            return self._error(
                request,
                ERROR_ARTIFACT_NOT_FOUND,
                "no new image artifact was produced by the codex turn",
                diagnostics,
            )

        info = sniff_image(discovery.path)
        if info is None:
            return self._error(
                request,
                ERROR_OUTPUT_INVALID,
                "generated artifact is not a valid raster image",
                diagnostics,
            )
        try:
            size = discovery.path.stat().st_size
        except OSError:
            size = 0
        if size <= 0:
            return self._error(
                request, ERROR_OUTPUT_INVALID, "generated artifact is zero bytes", diagnostics
            )

        diagnostics["artifact_source"] = str(discovery.path)
        diagnostics["artifact_format"] = info.fmt
        diagnostics["artifact_dimensions"] = {"width": info.width, "height": info.height}

        warnings: list[str] = []
        ratio_warning = _aspect_ratio_warning(request.aspect_ratio, info)
        if ratio_warning:
            warnings.append(ratio_warning)

        # Move the validated artifact into the workspace output path.
        try:
            self._place_artifact(discovery.path, output_target, request.operation)
        except OutputPathError as exc:
            return self._error(request, exc.error_code, str(exc), diagnostics)
        except OSError as exc:
            return self._error(
                request, ERROR_OUTPUT_INVALID, f"failed to place artifact: {exc}", diagnostics
            )

        # Final validation of the placed file.
        placed_info = sniff_image(output_target)
        if placed_info is None or output_target.stat().st_size <= 0:
            return self._error(
                request, ERROR_OUTPUT_INVALID, "placed output is not a valid image", diagnostics
            )

        return AdapterResult(
            status=STATUS_COMPLETED,
            slide_id=request.slide_id,
            operation=request.operation,
            backend=BACKEND,
            output_path=request.output_path,
            warnings=warnings,
            diagnostics=diagnostics,
        )

    def _place_artifact(self, source: Path, target: Path, operation: str) -> None:
        """Copy the artifact into the workspace, honouring the overwrite policy."""
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and operation != OP_REGENERATE:
            raise OutputPathError(
                ERROR_OUTPUT_PATH_CONFLICT,
                f"output path {target} already exists",
            )
        # Copy (not move) so the Codex artifact cache stays intact; write to a
        # temp sibling first for an atomic replace.
        fd, tmp_name = tempfile.mkstemp(dir=str(target.parent), suffix=target.suffix)
        os.close(fd)
        tmp_path = Path(tmp_name)
        try:
            shutil.copyfile(source, tmp_path)
            os.replace(tmp_path, target)
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:  # pragma: no cover - defensive
                    pass

    def _error(
        self, request: ImageRequest, code: str, message: str, diagnostics: dict[str, Any]
    ) -> AdapterResult:
        return AdapterResult(
            status=STATUS_ERROR,
            slide_id=request.slide_id,
            operation=request.operation,
            error_code=code,
            error_message=message,
            diagnostics=diagnostics,
        )


def _matches_any(text_lower: str, markers: Iterable[str]) -> bool:
    return any(marker.lower() in text_lower for marker in markers)


def _stderr_auth_failure(stderr: str) -> bool:
    return _matches_any(stderr.lower(), _AUTH_FAILURE_MARKERS)


def _aspect_ratio_warning(aspect_ratio: str, info: ImageInfo) -> str | None:
    """Warn (never re-draw) when the output does not match a requested ratio."""
    if not aspect_ratio or not info.width or not info.height:
        return None
    match = re.match(r"^\s*(\d+)\s*:\s*(\d+)\s*$", aspect_ratio)
    if not match:
        return None
    want_w, want_h = int(match.group(1)), int(match.group(2))
    if want_w <= 0 or want_h <= 0:
        return None
    want = want_w / want_h
    have = info.width / info.height
    if abs(want - have) / want > 0.02:
        return (
            f"requested aspect ratio {aspect_ratio} but artifact is "
            f"{info.width}x{info.height} (~{have:.3f}); kept as generated, not redrawn"
        )
    return None


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def _load_request(path: str | None) -> dict[str, Any]:
    if path and path != "-":
        raw = Path(path).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        raise InvalidRequestError("empty request")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InvalidRequestError(f"request is not valid JSON: {exc}") from exc
    return data


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AGY -> Codex image adapter")
    parser.add_argument("--input", help="path to the request JSON (default: stdin)")
    parser.add_argument("--output", help="path to write the result JSON (default: stdout)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        data = _load_request(args.input)
        request = ImageRequest.from_dict(data)
    except InvalidRequestError as exc:
        result = AdapterResult(
            status=STATUS_ERROR,
            error_code=ERROR_INVALID_REQUEST,
            error_message=str(exc),
            diagnostics={"auth": "chatgpt_cli_session", "api_fallback_used": False},
        )
        _emit(result.to_dict(), args.output)
        return 2

    result = CodexImageAdapter(request).run()
    payload = result.to_dict()
    _emit(payload, args.output)
    return 0 if result.status in (STATUS_COMPLETED, STATUS_AVAILABLE) else 1


def _emit(payload: dict[str, Any], output: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if output and output != "-":
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    raise SystemExit(main())
