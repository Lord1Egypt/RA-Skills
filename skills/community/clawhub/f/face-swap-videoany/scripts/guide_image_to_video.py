#!/usr/bin/env python3
"""
Backward-compatible entrypoint for legacy script name.
"""
import sys

from guide_face_swap import main


if __name__ == "__main__":
    print(
        "Warning: this skill is now face-swap guidance. "
        "Use scripts/guide_face_swap.py for the primary entrypoint.",
        file=sys.stderr,
    )
    sys.exit(main())
