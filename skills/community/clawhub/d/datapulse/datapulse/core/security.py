"""Security helpers for secret values and environment-backed credentials."""

from __future__ import annotations

import os
import re
from pathlib import Path

_DEFAULT_OBSIDIAN_SECRET_FILE = (
    Path.home()
    / "Library"
    / "Mobile Documents"
    / "iCloud~md~obsidian"
    / "Documents"
    / "SunYifei"
    / "\u4fe1\u606f\u8d44\u4ea7"
    / "ob-digital-asset-facts"
    / "Secrets"
    / "API Token Store.md"
)

_SECRET_LINE_RE = (
    re.compile(
        r"""
    ^\s*                      # optional indentation
    (?:[-*+]\s+)?             # optional markdown bullet
    `?(?P<key>[A-Z][A-Z0-9_]{1,})`?   # env-like key token
    \s*[:：=]\s*              # delimiter
    (?P<value>.+?)           # value
    \s*$
""",
        re.VERBOSE,
    ),
    re.compile(
        r"""
    ^\s*\|\s*                 # optional markdown table pipe prefix
    `?(?P<key>[A-Z][A-Z0-9_]{1,})`?   # env-like key token
    \s*\|\s*                  # table cell delimiter
    (?P<value>[^|]+?)         # value
    \s*(?:\|.*)?$             # optional extra columns
""",
        re.VERBOSE,
    ),
)
_SECRET_SECTION_KEY_RE = re.compile(r"^\s*###\s+([A-Za-z0-9_]+)$")
_SECRET_SECTION_SOURCE_RE = re.compile(
    r"^\s*-\s*Source(?:\s*\([^)]*\))?\s*:\s*(.+)$",
)
_SECRET_SECTION_VALUE_RE = re.compile(r"^\s*-\s*Value(?:\s*\([^)]*\))?\s*:\s*(.+)$")
_ENV_FILE_LINE_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")
_LOCAL_SECRET_CACHE: dict[Path, dict[str, str]] = {}


def _normalize_secret_value(raw: str) -> str:
    """Strip markdown formatting from parsed secret values."""

    value = raw.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1].strip()
    value = value.strip().strip('"').strip("'")
    return value.strip()


def _read_secret_file(path: Path) -> dict[str, str]:
    """Load env=value pairs from a local markdown note once."""

    if path in _LOCAL_SECRET_CACHE:
        return _LOCAL_SECRET_CACHE[path]

    if not path.is_file():
        _LOCAL_SECRET_CACHE[path] = {}
        return {}

    secrets: dict[str, str] = {}
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        _LOCAL_SECRET_CACHE[path] = {}
        return {}

    current_section_key: str | None = None
    for line in content.splitlines():
        stripped = line.strip()
        section_match = _SECRET_SECTION_KEY_RE.match(stripped)
        if section_match:
            current_section_key = section_match.group(1).upper().strip()
            continue

        match = None
        for pattern in _SECRET_LINE_RE:
            match = pattern.match(line)
            if match:
                break
        if match:
            key = match.group("key").upper()
            value = _normalize_secret_value(match.group("value"))
            if value:
                secrets[key] = value
            continue

        if not current_section_key:
            continue

        source_match = _SECRET_SECTION_SOURCE_RE.match(stripped)
        if source_match:
            source_ref = _normalize_secret_value(source_match.group(1))
            if source_ref:
                source_path = (
                    Path(source_ref)
                    if source_ref.startswith("/")
                    else (path.parent / source_ref).expanduser()
                )
                if source_path.is_file():
                    try:
                        source_text = source_path.read_text(encoding="utf-8", errors="ignore")
                    except OSError:
                        source_text = ""
                    for source_line in source_text.splitlines():
                        env_match = _ENV_FILE_LINE_RE.match(source_line.strip())
                        if not env_match:
                            continue
                        env_key = env_match.group(1).strip().upper()
                        if env_key != current_section_key:
                            continue
                        env_value = _normalize_secret_value(env_match.group(2))
                        if env_value:
                            secrets[current_section_key] = env_value
                        break
            continue

        value_match = _SECRET_SECTION_VALUE_RE.match(stripped)
        if value_match:
            value = _normalize_secret_value(value_match.group(1))
            if value:
                secrets[current_section_key] = value

    _LOCAL_SECRET_CACHE[path] = secrets
    return secrets


def _load_local_secret(env_name: str) -> str:
    """Load a single secret from configured local markdown stores."""

    key = env_name.upper().strip()
    if not key:
        return ""

    candidate_paths = []
    configured = os.getenv("DATAPULSE_LOCAL_SECRET_FILE", "").strip()
    if configured:
        candidate_paths.append(Path(configured).expanduser())
    else:
        candidate_paths.append(_DEFAULT_OBSIDIAN_SECRET_FILE)

    for path in candidate_paths:
        value = _read_secret_file(path).get(key)
        if value:
            return value
    return ""


def get_secret(env_name: str, *, default: str = "", required: bool = False, required_for: str | None = None) -> str:
    """Read a secret-like environment value with optional required validation.

    The returned value is trimmed. If `required` is True and the value is empty
    or missing, a `ValueError` is raised.
    """

    env_defined = env_name in os.environ
    if env_defined:
        value = os.getenv(env_name, "").strip()
    else:
        value = (default or "").strip()

    if not value and not env_defined:
        value = _load_local_secret(env_name)

    if required and not value:
        raise ValueError(f"{required_for or env_name} is required")
    return value


def has_secret(env_name: str) -> bool:
    """Return whether a secret environment value is configured."""
    return bool(get_secret(env_name))


def mask_secret(secret: str, *, prefix: int = 4, suffix: int = 4, max_mid: int = 6) -> str:
    """Return a masked representation for logs and diagnostics."""
    if not secret:
        return "<empty>"

    clean = secret.strip()
    if len(clean) <= prefix + suffix:
        return "*" * len(clean)

    mid_len = len(clean) - (prefix + suffix)
    visible_mid = min(mid_len, max_mid)
    return f"{clean[:prefix]}{'*' * visible_mid}{clean[-suffix:]}"
