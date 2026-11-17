#!/usr/bin/env python3
"""Validate externalized SKILL structure, routing paths, and optional test prompts."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--index", required=True)
    parser.add_argument("--test-prompts", default="")
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--test-command", default="")
    args = parser.parse_args()

    ok = True
    skill = Path(args.skill)
    index = Path(args.index)
    root = Path(args.root)
    if not skill.exists():
        print(f"MISSING skill {skill}")
        ok = False
    if not index.exists():
        print(f"MISSING index {index}")
        ok = False

    if index.exists():
        text = index.read_text(encoding="utf-8", errors="ignore")
        paths = re.findall(r"`([^`]+)`", text)
        missing = [p for p in paths if not (root / p).exists()]
        for path in missing:
            print(f"MISSING indexed path {path}")
        if missing:
            ok = False
        else:
            print(f"indexed_paths={len(paths)}")

    if args.test_prompts:
        prompts_path = Path(args.test_prompts)
        if prompts_path.exists():
            data = json.loads(prompts_path.read_text(encoding="utf-8"))
            cases = data.get("test_cases", data if isinstance(data, list) else [])
            print(f"test_cases={len(cases)}")
        else:
            print(f"MISSING test-prompts {prompts_path}")
            ok = False

    if args.test_command:
        result = subprocess.run(args.test_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("test_command=OK")
        else:
            print(f"test_command=FAILED\n{result.stdout}\n{result.stderr}")
            ok = False

    print("VALIDATE_OK" if ok else "VALIDATE_FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
