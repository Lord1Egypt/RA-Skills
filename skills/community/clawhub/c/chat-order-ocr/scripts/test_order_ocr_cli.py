#!/usr/bin/env python3
"""Small regression test for order_ocr_cli.py."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "order_ocr_cli.py"
FIXTURE = ROOT / "references" / "complex_chat_fixture.txt"
CATALOG = ROOT / "references" / "catalog.example.json"


def run(*args: str) -> dict:
    result = subprocess.run([sys.executable, str(CLI), *args], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main() -> int:
    payload = run("--input", str(FIXTURE), "--catalog", str(CATALOG), "--group-by", "person", "--format", "json")
    assert payload["sort"] == "name-asc"
    assert payload["summary"]["lines"] == 12, payload["summary"]
    assert payload["summary"]["units"] == 18, payload["summary"]
    assert payload["summary"]["people"] == 6, payload["summary"]
    assert payload["rows"][0]["person"] == "Lena"
    assert payload["rows"][0]["matched_item"] == "台灣葡萄"
    assert any(row["person"] == "小明" and row["matched_item"] == "紅肉火龍果大果" for row in payload["rows"])
    assert any(row["match_status"] == "未對應，請確認" for row in payload["rows"])
    assert all(row["confidence"] == "check" for row in payload["rows"] if row["match_status"] == "未對應，請確認")
    print("complex fixture PASS", payload["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
