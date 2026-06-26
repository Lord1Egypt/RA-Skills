#!/usr/bin/env python3
"""banana-claws first-run preflight checker."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
from pathlib import Path


def check_env(var: str) -> dict:
    ok = bool(os.environ.get(var, "").strip())
    return {"kind": "env", "name": var, "required": True, "ok": ok, "detail": "set" if ok else "missing"}


def check_bin(name: str) -> dict:
    path = shutil.which(name)
    ok = path is not None
    return {"kind": "bin", "name": name, "required": True, "ok": ok, "detail": path or "not found"}


def check_dir(path: Path) -> dict:
    exists = path.exists() and path.is_dir()
    return {"kind": "dir", "name": str(path), "required": False, "ok": exists, "detail": "exists" if exists else "missing"}


def check_module(module_name: str) -> dict:
    spec = importlib.util.find_spec(module_name)
    ok = spec is not None
    return {"kind": "python_module", "name": module_name, "required": True, "ok": ok, "detail": "installed" if ok else "missing"}


def main() -> int:
    parser = argparse.ArgumentParser(description="banana-claws preflight")
    parser.add_argument("--queue-dir", default="./generated/imagegen-queue")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks = [
        check_env("OPENROUTER_API_KEY"),
        check_bin("python3"),
        check_module("requests"),
        check_dir(Path(args.queue_dir)),
    ]

    required_failures = [c for c in checks if c["required"] and not c["ok"]]
    status = "ok" if not required_failures else "failed"

    fixups = []
    failed = {c["name"] for c in required_failures}
    if "OPENROUTER_API_KEY" in failed:
        fixups.append('export OPENROUTER_API_KEY="<your_key>"')
    if "python3" in failed:
        fixups.append("Install Python 3 and verify: python3 --version")
    if "requests" in failed:
        fixups.append("Install dependency: python3 -m pip install requests")
    fixups.append("mkdir -p ./generated/imagegen-queue")
    fixups.append("python3 skill/scripts/preflight_check.py --json")

    payload = {"status": status, "checks": checks, "required_failures": required_failures, "fixups": fixups}

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(("✅" if status == "ok" else "❌") + f" banana-claws preflight: {status}")
        for c in checks:
            mark = "PASS" if (c["ok"] or not c["required"]) else "FAIL"
            req = "required" if c["required"] else "optional"
            print(f"- [{mark}] {c['kind']} {c['name']} ({req}) -> {c['detail']}")
        if required_failures:
            print("\nFixups:")
            for f in fixups:
                print(f"- {f}")

    return 0 if status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
