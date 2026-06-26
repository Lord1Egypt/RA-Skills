#!/usr/bin/env python3
"""Basic regression checks for domestic_flight_service.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "domestic_flight_service.py"
SAMPLE = ROOT / "assets" / "sample-provider-response.json"


def run_command(*args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    payload = run_command(
        "search",
        "--from",
        "上海",
        "--to",
        "北京首都",
        "--date",
        "2026-03-20",
        "--sample-response",
        str(SAMPLE),
        "--limit",
        "1",
    )
    assert payload["route"]["from"]["code"] == "SHA"
    assert payload["route"]["to"]["code"] == "PEK"
    assert payload["count"] == 1
    assert payload["flights"][0]["ticket_price"] == 680
    assert payload["flights"][0]["flight_no"] == "MU5102"
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
