#!/usr/bin/env python3
"""Small helpers for stable checked-in test reports."""

from __future__ import annotations

import re
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any


WINDOWS_FIND_COMMUNITY_HELP_TEMP_RE = re.compile(
    r"[A-Za-z]:\\Users\\[^\\]+\\AppData\\Local\\Temp\\find-community-help-"
    r"(?:reliability|community|ablation|real-trigger)-[A-Za-z0-9_-]+\\"
)
POSIX_FIND_COMMUNITY_HELP_TEMP_RE = re.compile(
    r"(?:/tmp|/var/folders/[^/]+/[^/]+/T)/find-community-help-"
    r"(?:reliability|community|ablation|real-trigger)-[A-Za-z0-9_-]+/"
)
WINDOWS_AGENT_TRAVEL_TEMP_RE = re.compile(
    r"[A-Za-z]:\\Users\\[^\\]+\\AppData\\Local\\Temp\\agent-travel-"
    r"(?:reliability|community|ablation)-[A-Za-z0-9_-]+\\"
)
POSIX_AGENT_TRAVEL_TEMP_RE = re.compile(
    r"(?:/tmp|/var/folders/[^/]+/[^/]+/T)/agent-travel-"
    r"(?:reliability|community|ablation)-[A-Za-z0-9_-]+/"
)
WINDOWS_WORKSPACE_TEMP_RE = re.compile(
    r"[A-Za-z]:\\[^\r\n\"]*\\tmp\\(?:find-community-help|agent-travel)-"
    r"(?:reliability|community|ablation|real-trigger)-[A-Za-z0-9_-]+\\"
)
POSIX_WORKSPACE_TEMP_RE = re.compile(
    r"/[^\r\n\"]*/tmp/(?:find-community-help|agent-travel)-"
    r"(?:reliability|community|ablation|real-trigger)-[A-Za-z0-9_-]+/"
)


@contextmanager
def temporary_workspace_dir(root: Path, prefix: str):
    """Create test temp directories under the repo to avoid host temp ACL issues."""

    temp_root = root / "tmp"
    temp_root.mkdir(exist_ok=True)
    path = temp_root / f"{prefix}{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield str(path)
    finally:
        shutil.rmtree(path, ignore_errors=True)


def normalize_report_paths(value: Any) -> Any:
    """Replace per-run temp paths so report diffs reflect behavior, not cwd noise."""

    if isinstance(value, dict):
        return {key: normalize_report_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_report_paths(item) for item in value]
    if isinstance(value, str):
        normalized = WINDOWS_FIND_COMMUNITY_HELP_TEMP_RE.sub("<tmp>/", value)
        normalized = POSIX_FIND_COMMUNITY_HELP_TEMP_RE.sub("<tmp>/", normalized)
        normalized = WINDOWS_AGENT_TRAVEL_TEMP_RE.sub("<tmp>/", normalized)
        normalized = POSIX_AGENT_TRAVEL_TEMP_RE.sub("<tmp>/", normalized)
        normalized = WINDOWS_WORKSPACE_TEMP_RE.sub("<tmp>/", normalized)
        return POSIX_WORKSPACE_TEMP_RE.sub("<tmp>/", normalized)
    return value
