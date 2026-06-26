#!/usr/bin/env python3
"""
Preview the questioning mode and report structure for a prompt.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from planner import CANONICAL_TASK_TYPES, render_preview_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview the asking-until-100 question plan.")
    parser.add_argument("prompt", help="Prompt to analyze")
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
        "--task-type",
        choices=CANONICAL_TASK_TYPES,
        help="Override task-type inference with a canonical task type.",
    )
    parser.add_argument(
        "--cwd",
        default=str(Path.cwd()),
        help="Directory used for repo-local .asking-until-100.yaml discovery.",
    )
    parser.add_argument(
        "--repo-root",
        help="Directory used for repo inspection when generating repo-aware previews.",
    )
    args = parser.parse_args()

    explicit_override = Path(args.profile).resolve() if args.profile else None
    repo_root = Path(args.repo_root).resolve() if args.repo_root else None
    try:
        output = render_preview_text(
            args.prompt,
            explicit_task_type=args.task_type,
            explicit_override=explicit_override,
            bundled_profile=args.bundled_profile,
            cwd=Path(args.cwd).resolve(),
            repo_root=repo_root,
        )
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
