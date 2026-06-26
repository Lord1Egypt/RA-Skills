# FILE_META
# INPUT:  PipelineOptions (claude_home override, session_id filter, ...)
# OUTPUT: iterable of SessionHandle (one per ~/.claude/projects/*/<sid>.jsonl)
# POS:    skill lib adapters/claude_code — session enumeration
# MISSION: Walk ~/.claude/projects/ and yield one SessionHandle per session jsonl file.

"""Enumerate Claude Code sessions.

Scan ``~/.claude/projects/<cwd-slug>/<sessionId>.jsonl``. For each file
we need light metadata only: cwd, version, gitBranch, started_at, main
model, and file size. Reading content blocks or DAG-walking happens in
``parse.py`` — here we stop as soon as we have enough to build a
SessionHandle.

The Claude Code jsonl has a few idiosyncrasies we account for:
  - Some files start with bookkeeping events (``queue-operation`` /
    ``permission-mode``) that carry no cwd/version. We keep reading
    until we hit a real content event (user/assistant/system/attachment).
  - ``version`` is the Claude Code CLI version and appears on almost
    every real event. We capture the *first* occurrence — risk #7 in
    docs/adapter-design.md §12 calls out mid-session version bumps;
    parse-time will re-check.
  - ``model`` only appears inside ``assistant.message.model``. If the
    file contains no assistant turn we yield ``model=None`` and let
    filter/parse decide.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .. import SessionHandle
from ._paths import decode_cwd_slug, projects_dir

# Events that carry cwd/version/gitBranch on every line once the session
# actually starts. We stop the metadata scan the first time we see any of
# these.
_CONTENT_TYPES = {"user", "assistant", "system", "attachment"}

# Hard cap on lines read per file during discover. A production Claude
# Code session rarely exceeds 50 lines before the first assistant turn;
# the cap protects us from pathological files without giving up on
# late-model-binding sessions (we still return model=None if not found).
_DISCOVER_LINE_CAP = 200


def discover(opts: Any = None) -> Iterable[SessionHandle]:
    """Yield one SessionHandle per session jsonl.

    Silent if ``~/.claude/projects/`` does not exist — Claude Code may
    not be installed, and auto-probing callers treat absence as "no
    sessions", not as an error.
    """
    root = projects_dir(opts)
    if not root.is_dir():
        return

    for project_dir in sorted(root.iterdir()):
        if not project_dir.is_dir():
            continue
        slug = project_dir.name
        decoded_cwd = decode_cwd_slug(slug)
        if decoded_cwd is None:
            # slug '-' and other non-decodable dirs: skip silently.
            continue

        for jsonl_path in sorted(project_dir.glob("*.jsonl")):
            handle = _build_handle(jsonl_path, slug, decoded_cwd)
            if handle is not None:
                yield handle


def _build_handle(path: Path, slug: str, decoded_cwd: str) -> SessionHandle | None:
    """Read just enough of a jsonl to populate SessionHandle fields."""
    try:
        size_bytes = path.stat().st_size
    except OSError:
        return None
    if size_bytes == 0:
        return None

    session_id = path.stem  # filename without .jsonl
    if not session_id:
        return None

    version: str | None = None
    git_branch: str | None = None
    started_at_raw: str | None = None
    model: str | None = None
    real_cwd: str | None = None

    try:
        with path.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= _DISCOVER_LINE_CAP:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    # Corrupt line mid-file is rare; tolerate and keep scanning.
                    continue

                etype = obj.get("type")

                # Version / cwd / gitBranch / timestamp ride on content events.
                if etype in _CONTENT_TYPES:
                    if version is None and obj.get("version"):
                        version = obj.get("version")
                    if git_branch is None and obj.get("gitBranch") is not None:
                        git_branch = obj.get("gitBranch")
                    if started_at_raw is None and obj.get("timestamp"):
                        started_at_raw = obj.get("timestamp")
                    # Prefer the real cwd from the event over the lossy
                    # slug decode: slug→cwd cannot distinguish ``a-b``
                    # from ``a/b``. Events record the original path.
                    if real_cwd is None and obj.get("cwd"):
                        real_cwd = obj.get("cwd")

                # Model lives inside assistant.message.model.
                if model is None and etype == "assistant":
                    msg = obj.get("message") or {}
                    m = msg.get("model")
                    if m:
                        model = m

                if (
                    version
                    and model
                    and git_branch is not None
                    and started_at_raw
                    and real_cwd
                ):
                    break
    except OSError:
        return None

    effective_cwd = real_cwd or decoded_cwd

    started_at = _parse_iso(started_at_raw)

    return SessionHandle(
        adapter="claude-code",
        session_id=session_id,
        path=path,
        cwd=effective_cwd,
        model=model,
        started_at=started_at,
        size_bytes=size_bytes,
        extras={
            "slug": slug,
            "decoded_cwd": decoded_cwd,
            "version": version,
            "git_branch": git_branch,
        },
    )


def _parse_iso(value: str | None):
    if not value:
        return None
    from datetime import datetime

    s = value.replace("Z", "+00:00") if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


__all__ = ["discover"]
