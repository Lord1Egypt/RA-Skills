#!/usr/bin/env python3
"""Report declared dependencies; --max-deps is an explicit project policy, not a universal quality threshold."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from detect_lang import require_python  # noqa: E402

# Check the interpreter before importing modules that need Python 3.11+ (tomllib).
require_python()

from dependencies import read_dependencies  # noqa: E402
from detect_lang import (  # noqa: E402
    add_project_arguments,
    positive_int,
    print_report,
    select_language,
)


def main() -> int:
    """Audit a package and distinguish an exceeded policy limit from incomplete coverage."""
    parser = argparse.ArgumentParser(description=__doc__)
    add_project_arguments(parser)
    parser.add_argument("--max-deps", type=positive_int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    report = read_dependencies(root, select_language(root, args.lang))
    report["complete"] = not (report["warnings"] or report["errors"])
    exceeded = args.max_deps is not None and report["count"] > args.max_deps
    report["policy"] = {"max_deps": args.max_deps, "exceeded": exceeded}
    report["status"] = (
        "failed" if exceeded else ("completed" if report["complete"] else "incomplete")
    )
    print_report(report, args.json)
    return 1 if exceeded else (0 if report["complete"] else 2)


if __name__ == "__main__":
    sys.exit(main())
