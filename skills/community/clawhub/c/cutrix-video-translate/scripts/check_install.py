"""Verify the Cutrix SDK is importable (no API calls, no secrets)."""

from __future__ import annotations

import importlib.metadata
import sys


def main() -> int:
    try:
        import cutrix  # noqa: F401
    except ImportError as e:
        print("FAIL: cannot import cutrix:", e, file=sys.stderr)
        return 1
    try:
        ver = importlib.metadata.version("cutrix-video-translate-sdk")
    except importlib.metadata.PackageNotFoundError:
        ver = "unknown"
    print("OK: cutrix importable, distribution version:", ver)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
