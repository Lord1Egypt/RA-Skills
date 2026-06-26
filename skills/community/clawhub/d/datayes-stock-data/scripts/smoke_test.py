#!/usr/bin/env python3
"""Smoke-test core Datayes skill flows."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "datayes_api.py"
TOKEN_ENV = "DATAYES_TOKEN"


class SmokeTestError(RuntimeError):
    pass


def run_json(args: list[str]) -> Any:
    cmd = [sys.executable, str(SCRIPT), *args]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=os.environ.copy())
    if result.returncode != 0:
        raise SmokeTestError(result.stderr.strip() or result.stdout.strip() or f"Command failed: {' '.join(cmd)}")
    return json.loads(result.stdout)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeTestError(message)


def main() -> int:
    if not os.environ.get(TOKEN_ENV, "").strip():
        print(f"Missing {TOKEN_ENV} environment variable", file=sys.stderr)
        return 1

    checks: list[str] = []

    search = run_json(["stock_search", "--param", "query=比亚迪", "--result-only"])
    hits = ((search or {}).get("data") or {}).get("hits") or []
    assert_true(bool(hits), "stock_search returned no hits")
    first_hit = hits[0]
    assert_true(first_hit.get("entity_id") == "002594", "stock_search did not resolve 比亚迪 to 002594")
    checks.append("stock_search")

    snapshot = run_json([
        "market_snapshot",
        "--param",
        "ticker=002594",
        "--param",
        "type=stock",
        "--result-only",
    ])
    snapshot_data = (snapshot or {}).get("data") or {}
    assert_true(snapshot.get("code") == 1, "market_snapshot did not return code=1")
    assert_true(snapshot_data.get("ticker") == "002594", "market_snapshot returned unexpected ticker")
    checks.append("market_snapshot")

    range_stats = run_json([
        "market_rang_statistics",
        "--param",
        "ticker=002594",
        "--param",
        "beginDate=20260301",
        "--param",
        "endDate=20260324",
        "--param",
        "type=stock",
        "--result-only",
    ])
    range_data = (range_stats or {}).get("data") or {}
    assert_true(range_stats.get("code") == 1, "market_rang_statistics did not return code=1")
    assert_true(range_data.get("ticker") == "002594", "market_rang_statistics returned unexpected ticker")
    checks.append("market_rang_statistics")

    income_statement = run_json([
        "fdmt_is_new_lt",
        "--param",
        "ticker=601988",
        "--param",
        "beginDate=20240101",
        "--param",
        "endDate=20241231",
        "--param",
        "reportType=A",
        "--result-only",
    ])
    income_rows = (income_statement or {}).get("data") or []
    assert_true(income_statement.get("retCode") == 1, "fdmt_is_new_lt did not return retCode=1")
    assert_true(bool(income_rows), "fdmt_is_new_lt returned no rows")
    assert_true(any(row.get("ticker") == "601988" for row in income_rows), "fdmt_is_new_lt returned unexpected ticker set")
    checks.append("fdmt_is_new_lt_without_field")

    invalid = subprocess.run(
        [sys.executable, str(SCRIPT), "stock_search", "--param", "keyword=比亚迪"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=os.environ.copy(),
    )
    assert_true(invalid.returncode != 0, "outdated parameter alias keyword should fail")
    assert_true("Unknown parameters" in (invalid.stderr or ""), "outdated parameter error message is missing")
    checks.append("invalid_param_guard")

    print(json.dumps({"ok": True, "checks": checks}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
