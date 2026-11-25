#!/usr/bin/env python3
"""Shared configuration helpers for the cyber-security-engineer scripts.

Security settings can be given in two places:

- ``~/.openclaw/env``: ``NAME=value`` lines. This is the durable place, and the
  one the compliance assessment reports on.
- the process environment.

A setting that turns a protection on (for example ``OPENCLAW_REQUIRE_SESSION_ID=1``)
applies when either place sets it, so unsetting an environment variable cannot
switch off something the file requires. No network calls are made.
"""
import os
import tempfile
from pathlib import Path
from typing import Dict, Mapping, Optional

OPENCLAW_DIR = Path.home() / ".openclaw"
SECURITY_DIR = OPENCLAW_DIR / "security"
ENV_FILE = OPENCLAW_DIR / "env"


def is_private(path: Path) -> bool:
    """True when ``path`` belongs to the current user and nobody else can read or write it."""
    try:
        st = path.stat()
    except OSError:
        return False
    if os.name == "nt":
        return True  # POSIX permission bits are not meaningful on Windows
    return st.st_uid == os.geteuid() and (st.st_mode & 0o077) == 0


def write_private(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` atomically, readable and writable by the owner only."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, str(path))
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def parse_env_text(text: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load_env_file(path: Optional[Path] = None) -> Dict[str, str]:
    """Settings from ``~/.openclaw/env`` (empty when the file is missing or unreadable)."""
    path = ENV_FILE if path is None else path
    try:
        return parse_env_text(path.read_text(encoding="utf-8"))
    except OSError:
        return {}


def setting(
    name: str,
    file_values: Optional[Mapping[str, str]] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> Optional[str]:
    """Value of ``name``: the env file wins, then the process environment."""
    file_values = load_env_file() if file_values is None else file_values
    environ = os.environ if environ is None else environ
    value = file_values.get(name) or environ.get(name)
    return value or None


def flag(
    name: str,
    file_values: Optional[Mapping[str, str]] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> bool:
    """True when ``name`` is set to ``1`` in the env file or the process environment."""
    file_values = load_env_file() if file_values is None else file_values
    environ = os.environ if environ is None else environ
    return file_values.get(name) == "1" or environ.get(name) == "1"
