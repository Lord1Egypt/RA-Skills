"""
Shared helpers for clean-text-toolkit.

Pure standard library. No third-party imports.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    """Reject paths containing shell metacharacters."""
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def read_text(path: Path, encoding: str = "utf-8") -> str:
    """Read a text file, falling back through several encodings if needed."""
    for enc in (encoding, "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    # Last resort: replace undecodable bytes
    return path.read_bytes().decode("utf-8", errors="replace")


def iter_lines(path: Path, encoding: str = "utf-8"):
    """Yield lines from a file, streaming. Strips the trailing newline."""
    for enc in (encoding, "utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open("r", encoding=enc, errors="replace") as f:
                for line in f:
                    yield line.rstrip("\n").rstrip("\r")
            return
        except UnicodeDecodeError:
            continue


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_lines(path: Path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            if not line.endswith("\n"):
                f.write("\n")


def open_input(arg: str | None):
    """Return (filehandle, label). If arg is None or '-', use stdin.
    Otherwise treat as a path (caller is responsible for safe_path)."""
    if arg is None or arg == "-":
        return sys.stdin, "<stdin>"
    p = safe_path(arg)
    if not p.is_file():
        raise FileNotFoundError(f"not a file: {p}")
    return p.open("r", encoding="utf-8", errors="replace"), str(p)
