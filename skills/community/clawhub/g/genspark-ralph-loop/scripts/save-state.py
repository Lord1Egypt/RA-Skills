#!/usr/bin/env python3
"""Save one JSON state object from stdin using a single atomic replacement."""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


def save_state(destination: Path, state: object) -> None:
    if not isinstance(state, dict):
        raise ValueError("State must be a JSON object")
    payload = json.dumps(state, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        state = json.load(sys.stdin)
        save_state(args.destination, state)
    except (ValueError, OSError) as error:
        print(f"State save failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved state: {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
