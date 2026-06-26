#!/usr/bin/env python3
"""
Backward-compatible entrypoint for legacy script name.
"""
import sys

from guide_ai_avatar import main


if __name__ == "__main__":
    print(
        "Warning: this skill is now AI avatar guidance. "
        "Use scripts/guide_ai_avatar.py for the primary entrypoint.",
        file=sys.stderr,
    )
    sys.exit(main())
