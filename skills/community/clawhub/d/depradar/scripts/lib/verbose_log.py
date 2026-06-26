"""Structured verbose logging for /depradar.

Activated by --verbose/-v flag. Writes to stderr so it doesn't pollute
stdout JSON/compact output.
"""

from __future__ import annotations

import sys
import time
from typing import Optional


class VerboseLog:
    """Conditional verbose logger. All methods are no-ops when disabled."""

    def __init__(self, enabled: bool = False) -> None:
        self._enabled = enabled
        self._start = time.monotonic()

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _elapsed(self) -> str:
        return f"{time.monotonic() - self._start:.1f}s"

    def step(self, step: str, detail: str = "") -> None:
        """Log a named pipeline step."""
        if not self._enabled:
            return
        suffix = f": {detail}" if detail else ""
        print(f"  [+{self._elapsed()}] {step}{suffix}", file=sys.stderr)

    def info(self, msg: str) -> None:
        """Log an informational message."""
        if not self._enabled:
            return
        print(f"  [+{self._elapsed()}] {msg}", file=sys.stderr)

    def warn(self, msg: str) -> None:
        """Log a warning."""
        if not self._enabled:
            return
        print(f"  [+{self._elapsed()}] ⚠ {msg}", file=sys.stderr)

    def hit(self, msg: str) -> None:
        """Log a cache hit."""
        if not self._enabled:
            return
        print(f"  [+{self._elapsed()}] ✓ cache hit: {msg}", file=sys.stderr)

    def miss(self, msg: str) -> None:
        """Log a cache miss (network call being made)."""
        if not self._enabled:
            return
        print(f"  [+{self._elapsed()}] → fetch: {msg}", file=sys.stderr)

    def result(self, source: str, count: int, extra: str = "") -> None:
        """Log a result count from a source."""
        if not self._enabled:
            return
        suffix = f" ({extra})" if extra else ""
        print(f"  [+{self._elapsed()}] {source}: {count} results{suffix}", file=sys.stderr)

    def error(self, source: str, err: str) -> None:
        """Log a source error."""
        if not self._enabled:
            return
        print(f"  [+{self._elapsed()}] ✗ {source}: {err}", file=sys.stderr)

    def scan(self, files_scanned: int, matches: int, skipped: int) -> None:
        """Log codebase scan summary."""
        if not self._enabled:
            return
        skip_str = f", {skipped} skipped" if skipped else ""
        print(
            f"  [+{self._elapsed()}] scan: {files_scanned} files, "
            f"{matches} symbol matches{skip_str}",
            file=sys.stderr,
        )


# Module-level singleton — replaced by depradar.py when --verbose is set
_log = VerboseLog(enabled=False)


def get_log() -> VerboseLog:
    """Return the current module-level VerboseLog instance."""
    return _log


def set_log(log: VerboseLog) -> None:
    """Replace the module-level VerboseLog instance."""
    global _log
    _log = log
