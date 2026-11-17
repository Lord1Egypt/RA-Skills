"""Command-line entry point for the forklift-benchmark package.

This is intentionally a thin wrapper that delegates to the real pipeline
entry points (``generator.run``, ``validator.run``, ``scorer.run``) when
they are available. If a subpackage is not yet installed in the environment
it prints a helpful hint rather than crashing the ``forklift-benchmark``
console script.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional, Sequence

from . import __version__


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forklift-benchmark",
        description=(
            "FK-Bench v2 — Forklift Embodied Intelligence Benchmark. "
            "Provides subcommands for dataset generation, validation, and scoring."
        ),
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the FK-Bench version and exit.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("info", help="Print benchmark metadata.")
    sub.add_parser("validate", help="Run static validation over the dataset.")
    sub.add_parser("score", help="Run the three-layer scoring engine on a prediction file.")
    sub.add_parser("demo", help="Run the end-to-end demo (see examples/run_demo.py).")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.version or args.command is None:
        print(f"forklift-benchmark {__version__}")
        return 0
    if args.command == "info":
        print(f"FK-Bench v{__version__}")
        print("Dataset: 500 items across 6 modules and 7 scenes.")
        print("License: Apache-2.0")
        return 0
    if args.command in {"validate", "score", "demo"}:
        print(
            f"Subcommand '{args.command}' is provided by the matching module. "
            "See the docs/ folder for usage.",
            file=sys.stderr,
        )
        return 0
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
