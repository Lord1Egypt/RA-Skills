#!/usr/bin/env python3
"""Human-friendly Chronos config checker."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import inspect_config


def main() -> int:
    info = inspect_config()

    print("Chronos Configuration Check")
    print(f"status: {info['status']}")
    print(f"config_path: {info['config_path']}")
    print(f"config_exists: {'yes' if info['config_exists'] else 'no'}")
    print(f"env_chat_id_present: {'yes' if info['env_chat_id_present'] else 'no'}")
    print(f"file_chat_id_present: {'yes' if info['file_chat_id_present'] else 'no'}")
    print(f"resolved_source: {info['source'] or 'none'}")
    print(f"resolved_chat_id: {info['chat_id'] or 'none'}")

    if info['error']:
        print(f"error: {info['error']}")

    return 0 if info['status'] == 'ok' else 1


if __name__ == "__main__":
    raise SystemExit(main())
