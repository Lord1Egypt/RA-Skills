#!/usr/bin/env python3
"""Install and verify PPTSmith's lockfile-pinned PptxGenJS runtime."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME = ROOT / "runtime" / "pptxgenjs"
REQUIRED_MODULES = ("pptxgenjs", "jszip")


def _report(runtime: Path) -> dict[str, Any]:
    missing_files = [name for name in ("package.json", "package-lock.json", "build-deck.mjs") if not (runtime / name).is_file()]
    if missing_files:
        return {
            "status": "blocked",
            "code": "PPTXGENJS_RUNTIME_LAYOUT_INVALID",
            "message": f"PptxGenJS runtime is incomplete at {runtime}; missing: {', '.join(missing_files)}.",
            "action": "restore a complete checkout, then run npm ci in the runtime directory",
            "runtime": str(runtime),
        }
    missing_modules = [module for module in REQUIRED_MODULES if not (runtime / "node_modules" / module / "package.json").is_file()]
    if missing_modules:
        return {
            "status": "blocked",
            "code": "PPTXGENJS_RUNTIME_UNAVAILABLE",
            "message": "PptxGenJS runtime dependencies are absent; package-lock.json is present for a reproducible install.",
            "action": "npm ci",
            "runtime": str(runtime),
            "missing_modules": missing_modules,
        }
    node = shutil.which("node")
    if node is None:
        return {
            "status": "blocked",
            "code": "NODE_RUNTIME_NOT_FOUND",
            "message": "Node.js is required to load the lockfile-pinned PptxGenJS runtime.",
            "action": "install a supported local Node.js runtime, then run npm ci",
            "runtime": str(runtime),
        }
    try:
        loaded = subprocess.run(
            [node, "--input-type=module", "-e", "await import('pptxgenjs'); await import('jszip');"],
            cwd=runtime,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "status": "blocked",
            "code": "PPTXGENJS_RUNTIME_MODULE_LOAD_FAILED",
            "message": f"PptxGenJS runtime could not be loaded: {exc}",
            "action": "rerun npm ci from the runtime directory",
            "runtime": str(runtime),
        }
    if loaded.returncode != 0:
        return {
            "status": "blocked",
            "code": "PPTXGENJS_RUNTIME_MODULE_LOAD_FAILED",
            "message": "PptxGenJS runtime dependencies are present but Node cannot import them.",
            "action": "rerun npm ci from the runtime directory",
            "runtime": str(runtime),
            "stderr": loaded.stderr[-2000:],
        }
    return {
        "status": "ready",
        "code": "PPTXGENJS_RUNTIME_READY",
        "message": "PptxGenJS and JSZip loaded from the local lockfile-pinned runtime.",
        "runtime": str(runtime),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Only report runtime readiness; do not install dependencies.")
    parser.add_argument("--runtime", type=Path, default=DEFAULT_RUNTIME, help="PptxGenJS runtime directory.")
    args = parser.parse_args(argv)
    runtime = args.runtime.resolve()

    before = _report(runtime)
    if args.check or before["code"] != "PPTXGENJS_RUNTIME_UNAVAILABLE":
        print(json.dumps(before, ensure_ascii=False))
        return 0 if before["status"] == "ready" else 2

    npm = shutil.which("npm")
    if npm is None:
        print(json.dumps({
            "status": "blocked", "code": "NPM_RUNTIME_NOT_FOUND",
            "message": "npm is required to install the lockfile-pinned PptxGenJS runtime.",
            "action": "install npm, then run npm ci", "runtime": str(runtime),
        }, ensure_ascii=False))
        return 2
    installed = subprocess.run([npm, "ci"], cwd=runtime, text=True, capture_output=True, check=False)
    if installed.returncode != 0:
        print(json.dumps({
            "status": "blocked", "code": "PPTXGENJS_BOOTSTRAP_FAILED",
            "message": "npm ci failed for the lockfile-pinned PptxGenJS runtime.",
            "action": "resolve the npm ci error without changing package-lock.json",
            "runtime": str(runtime), "stderr": installed.stderr[-2000:],
        }, ensure_ascii=False))
        return installed.returncode or 1
    after = _report(runtime)
    print(json.dumps(after, ensure_ascii=False))
    return 0 if after["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
