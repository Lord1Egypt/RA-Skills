"""Configuration loading for /depradar.

Priority (highest → lowest):
  1. Environment variables  (os.environ)
  2. .claude/depradar.env   (per-project, walk up from cwd)
  3. ~/.config/depradar/.env (user-global)
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple


# Keys we care about
_KNOWN_KEYS = {
    "GITHUB_TOKEN",
    "SCRAPECREATORS_API_KEY",
    "XAI_API_KEY",
    "AUTH_TOKEN",           # X/Twitter cookie
    "CT0",                  # X/Twitter cookie pair
    "STACKOVERFLOW_API_KEY",
    "OPENAI_API_KEY",       # optional fallback
}

_GLOBAL_CONFIG_DIR  = Path.home() / ".config" / "depradar"
_GLOBAL_CONFIG_FILE = _GLOBAL_CONFIG_DIR / ".env"
_PROJECT_CONFIG_NAME = "depradar.env"   # lives inside .claude/


def get_config() -> Dict[str, str]:
    """Return a merged config dict plus metadata keys."""
    base: Dict[str, str] = {}
    source = "env_only"

    # Layer 3: global file
    global_file = _GLOBAL_CONFIG_FILE
    if global_file.is_file():
        base.update(_load_env_file(global_file))
        source = f"global:{global_file}"

    # Layer 2: per-project file (walk up from cwd)
    project_file = _find_project_env()
    if project_file:
        base.update(_load_env_file(project_file))
        source = f"project:{project_file}"

    # Layer 1: environment variables (always win)
    for key in _KNOWN_KEYS:
        val = os.environ.get(key)
        if val:
            base[key] = val

    base["_CONFIG_SOURCE"] = source
    return base


def is_github_authed(config: Dict[str, str]) -> bool:
    return bool(config.get("GITHUB_TOKEN"))


def is_reddit_available(config: Dict[str, str]) -> bool:
    return bool(config.get("SCRAPECREATORS_API_KEY"))


def is_twitter_available(config: Dict[str, str]) -> bool:
    return bool(config.get("XAI_API_KEY")) or bool(
        config.get("AUTH_TOKEN") and config.get("CT0")
    )


def is_stackoverflow_enhanced(config: Dict[str, str]) -> bool:
    return bool(config.get("STACKOVERFLOW_API_KEY"))


def github_headers(config: Dict[str, str]) -> Dict[str, str]:
    """Return auth headers for GitHub API calls."""
    hdrs: Dict[str, str] = {"Accept": "application/vnd.github+json",
                             "X-GitHub-Api-Version": "2022-11-28"}
    token = config.get("GITHUB_TOKEN")
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    return hdrs


def load_npmrc_registry(project_root: str = "") -> Tuple[Optional[str], Dict[str, str]]:
    """Read npm registry config from .npmrc in project or home directory.

    Parses both the global registry and per-scope registry overrides:
        registry=https://registry.npmjs.org           (global)
        @mycompany:registry=https://npm.mycompany.com (scoped)

    Returns:
        (global_registry_url, {scope: registry_url})
        e.g. ("https://registry.npmjs.org", {"@mycompany": "https://npm.mycompany.com"})
        Both values may be None / empty dict if not configured.
    """
    search_paths = []
    if project_root:
        search_paths.append(Path(project_root) / ".npmrc")
    search_paths.append(Path.home() / ".npmrc")

    global_registry: Optional[str] = None
    scope_registries: Dict[str, str] = {}

    for npmrc_path in search_paths:
        if not npmrc_path.exists():
            continue
        try:
            for line in npmrc_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                line_lower = line.lower()
                # Global registry: registry=https://...
                if line_lower.startswith("registry="):
                    url = line.split("=", 1)[1].strip().rstrip("/")
                    if url and global_registry is None:
                        global_registry = url
                # Scoped registry: @scope:registry=https://...
                elif ":registry=" in line_lower:
                    idx = line_lower.index(":registry=")
                    scope = line[:idx].strip().lower()   # "@mycompany"
                    url = line[idx + len(":registry="):].strip().rstrip("/")
                    if scope and url and scope not in scope_registries:
                        scope_registries[scope] = url
        except OSError:
            continue

    return global_registry, scope_registries


# ── Internal ─────────────────────────────────────────────────────────────────

def _find_project_env() -> Optional[Path]:
    """Walk up from cwd looking for .claude/depradar.env."""
    cwd = Path.cwd()
    for directory in [cwd, *cwd.parents]:
        candidate = directory / ".claude" / _PROJECT_CONFIG_NAME
        if candidate.is_file():
            return candidate
        # Stop at filesystem root or git root
        if (directory / ".git").exists() or directory == directory.parent:
            break
    return None


_ENV_LINE = re.compile(r"^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$")


def _load_env_file(path: Path) -> Dict[str, str]:
    result: Dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = _ENV_LINE.match(line)
            if m:
                key, val = m.group(1), m.group(2)
                if key in _KNOWN_KEYS:
                    # Strip surrounding quotes
                    if len(val) >= 2 and val[0] in ('"', "'") and val[-1] == val[0]:
                        val = val[1:-1]
                    result[key] = val
    except OSError:
        pass
    return result
