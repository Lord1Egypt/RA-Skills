# FILE_META
# INPUT:  PipelineOptions (for ~/.claude root override) or None
# OUTPUT: Path helpers for Claude Code project dirs and cwd encoding
# POS:    skill lib adapters/claude_code — private path helper
# MISSION: Locate ~/.claude/projects/ and decode the slug directory names.

"""Locate Claude Code state and decode project directory slugs.

Claude Code stores each session as
``~/.claude/projects/<cwd-slug>/<sessionId>.jsonl``. The slug is the
original absolute cwd with every ``/`` replaced by ``-`` and a leading
``-`` kept for the root slash. We also see bare ``-`` slugs (internal
bookkeeping) which we skip rather than attempt to decode.

Environment override: ``CLAUDE_HOME`` points at the directory that
contains ``projects/`` (defaults to ``~/.claude``). Useful in tests.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

DEFAULT_CLAUDE_HOME = "~/.claude"


class ClaudeCodeNotInstalled(RuntimeError):
    """Raised when ~/.claude/projects/ cannot be located."""


def claude_home(opts: Any = None) -> Path:
    """Resolve the ~/.claude root, honoring CLAUDE_HOME env override."""
    env = os.environ.get("CLAUDE_HOME")
    if env:
        return Path(env).expanduser()
    opts_override = getattr(opts, "claude_home", None) if opts is not None else None
    if opts_override:
        return Path(opts_override).expanduser()
    return Path(DEFAULT_CLAUDE_HOME).expanduser()


def projects_dir(opts: Any = None) -> Path:
    return claude_home(opts) / "projects"


def decode_cwd_slug(slug: str) -> str | None:
    """Turn ``-Users-foo-bar`` into ``/Users/foo/bar``.

    Returns ``None`` for slugs we cannot reasonably decode (empty string,
    bare ``-`` seen in the wild, anything that does not start with ``-``).
    The caller treats a ``None`` decode as "skip this directory".

    Limitation: this is a lossy encoding — a directory named ``a-b`` in
    the real cwd cannot be distinguished from nested ``a/b``. We accept
    that upstream: the resulting cwd string is reported in the trajectory
    for traceability, but scope_id is derived from the slug, not the
    decoded path, so mismatches do not leak across sessions.
    """
    if not slug or slug == "-":
        return None
    if not slug.startswith("-"):
        return None
    return "/" + slug[1:].replace("-", "/")


__all__ = [
    "ClaudeCodeNotInstalled",
    "DEFAULT_CLAUDE_HOME",
    "claude_home",
    "projects_dir",
    "decode_cwd_slug",
]
