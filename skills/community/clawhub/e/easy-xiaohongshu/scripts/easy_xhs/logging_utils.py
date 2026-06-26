from __future__ import annotations

import json
import sys
from typing import Any


class JsonFormatter:
    @staticmethod
    def dumps(data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)


def log(message: str) -> None:
    print(message, file=sys.stderr)


def info(message: str) -> None:
    log(f"[INFO] {message}")


def warn(message: str) -> None:
    log(f"[WARN] {message}")


def error(message: str) -> None:
    log(f"[ERROR] {message}")
