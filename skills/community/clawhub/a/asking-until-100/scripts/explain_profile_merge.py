#!/usr/bin/env python3
"""
Explain the effective profile after applying precedence rules.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from planner import render_profile_explanation


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain effective profile discovery and merging.")
    parser.add_argument(
        "--profile",
        help="Explicit override profile path. This wins over repo-local config.",
    )
    parser.add_argument(
        "--bundled-profile",
        default="default-profile",
        help="Bundled profile name or path to use beneath repo-local and explicit overrides.",
    )
    parser.add_argument(
        "--cwd",
        default=str(Path.cwd()),
        help="Directory used for repo-local .asking-until-100.yaml discovery.",
    )
    args = parser.parse_args()

    explicit_override = Path(args.profile).resolve() if args.profile else None
    try:
        output = render_profile_explanation(
            explicit_override=explicit_override,
            bundled_profile=args.bundled_profile,
            cwd=Path(args.cwd).resolve(),
        )
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
