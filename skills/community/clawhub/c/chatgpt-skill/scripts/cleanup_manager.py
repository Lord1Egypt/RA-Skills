#!/usr/bin/env python3
"""Cleanup helpers for chatgpt-skill."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import SCREENSHOTS_DIR, SESSION_RUNTIME_DIR
from errors import result_from_exception


class CleanupManager:
    def runtime(self):
        removed = []
        if SESSION_RUNTIME_DIR.exists():
            shutil.rmtree(SESSION_RUNTIME_DIR)
            removed.append(str(SESSION_RUNTIME_DIR))
        SESSION_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        return {"status": "success", "removed": removed}

    def screenshots(self):
        removed = []
        if SCREENSHOTS_DIR.exists():
            shutil.rmtree(SCREENSHOTS_DIR)
            removed.append(str(SCREENSHOTS_DIR))
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        return {"status": "success", "removed": removed}

    def all(self):
        payload = self.runtime()
        screenshots = self.screenshots()
        return {"status": "success", "removed": payload["removed"] + screenshots["removed"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Cleanup ChatGPT skill artifacts")
    parser.add_argument("target", choices=["runtime", "screenshots", "all"])
    args = parser.parse_args()

    manager = CleanupManager()
    try:
        payload = getattr(manager, args.target)()
    except Exception as error:
        payload = result_from_exception(error)

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
