#!/usr/bin/env python3
"""
Validate asking-until-100 profile files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from planner import validate_profile_data
from planner import load_yaml_mapping


def validate_profile(path: Path, *, allow_partial: bool = False) -> list[str]:
    try:
        data = load_yaml_mapping(path)
    except OSError as exc:
        return [f"{path}: could not read file: {exc}"]
    except ValueError as exc:
        return [str(exc)]

    return validate_profile_data(data, path, allow_partial=allow_partial)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate asking-until-100 config profiles.")
    parser.add_argument("config", nargs="+", help="Config YAML file(s) to validate")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Allow partial override files instead of requiring a full effective profile.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    for raw_path in args.config:
        errors.extend(validate_profile(Path(raw_path), allow_partial=args.allow_partial))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print("All config profiles are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
