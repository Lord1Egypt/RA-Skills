#!/usr/bin/env python3
"""全流程：parse → search → parse-passengers → verify → order。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
PY = sys.executable
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}

QUERY = os.environ.get("FR_BOOKING_TEST_QUERY", "深圳到曼谷 6月2日")
PAX_TEXT = os.environ.get(
    "FR_BOOKING_TEST_PAX",
    "张三  男 1990-01-15 护照E12345678，2030-12-31 到期，国籍 CN。\n"
    "联系人：张三，手机 13800138000，邮箱 zhangsan@example.com",
)


def run(args: list[str]) -> dict:
    proc = subprocess.run(
        [PY] + args,
        cwd=str(_ROOT),
        env=ENV,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        print(proc.stderr)
        raise SystemExit(proc.returncode)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(proc.stdout)
        print(proc.stderr)
        raise


def main() -> int:
    print(f"ROOT={_ROOT}")
    from config import EXPORT_BASE_URL, GRAY_HEADER

    print(f"export={EXPORT_BASE_URL} gray={GRAY_HEADER}")

    print("\n--- 1. parse ---")
    p1 = run(["scripts/nl_to_search.py", "parse", "--text", QUERY])
    if p1.get("status") != "success":
        print("FAIL parse:", p1.get("message"))
        return 1
    print("OK:", (p1.get("userView") or {}).get("intentSummary"))

    print("\n--- 2. search ---")
    s = run(
        [
            "scripts/skill_search_client.py",
            "search",
            "--payload-file",
            ".cache/pending_search.json",
            "--selection",
            "direct",
        ]
    )
    if s.get("status") != "success":
        print("FAIL search:", s.get("message"))
        return 1
    uv = s.get("userView") or {}
    agent = s.get("agentOnly") or {}
    print("OK mode:", agent.get("searchMode"), "offer:", (uv.get("directLowest") or {}).get("flights"))

    if not agent.get("bookingEnabled"):
        print("SKIP booking: 未配置 NewApi，仅 Skill 搜索通过")
        return 0

    print("\n--- 3. parse-passengers ---")
    p3 = run(["scripts/skill_booking_client.py", "parse-passengers", "--text", PAX_TEXT])
    if p3.get("status") != "success":
        print("FAIL parse-passengers:", p3.get("message"))
        return 1
    print("OK confirmPhrase:", (p3.get("userView") or {}).get("confirmPhrase"))

    print("\n--- 4. verify ---")
    v = run(
        [
            "scripts/skill_booking_client.py",
            "verify",
            "--passenger-confirmed",
        ]
    )
    if v.get("status") != "success":
        print("FAIL verify:", v.get("message"))
        return 1
    uv = v.get("userView") or {}
    agent = v.get("agentOnly") or {}
    print("OK verifyOfferId:", agent.get("verifyOfferId"))
    if not uv.get("orderPreview"):
        print("FAIL: missing orderPreview")
        return 1

    if os.environ.get("FR_BOOKING_TEST_ORDER", "").lower() not in ("1", "true", "yes"):
        print("\nSKIP order: 见 setup-maintainer.md 开启真实生单测试")
        return 0

    print("\n--- 5. order ---")
    o = run(["scripts/skill_booking_client.py", "order", "--user-confirmed"])
    if o.get("status") != "success":
        print("FAIL order:", o.get("message"))
        return 1
    print("OK orderNo:", (o.get("userView") or {}).get("orderNo"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
