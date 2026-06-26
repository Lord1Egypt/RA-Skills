#!/usr/bin/env python3
"""Douyin Automation Pipeline Runner - Cross-platform.

Reads CONFIG.md for paths, then runs the orchestrator.
Supports --dry-run and --no-ai flags.
"""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "CONFIG.md"


def load_config():
    """Load and parse CONFIG.md JSON block."""
    if not CONFIG_FILE.exists():
        print("ERROR: CONFIG.md not found. Run 'python scripts/setup.py' first.")
        sys.exit(1)
    text = CONFIG_FILE.read_text(encoding="utf-8")
    m = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if not m:
        print("ERROR: No JSON block found in CONFIG.md.")
        sys.exit(1)
    config = json.loads(m.group(1))
    if config.get("douyin_home") == "REQUIRED - run setup.py or edit manually":
        print("ERROR: CONFIG.md not configured. Run 'python scripts/setup.py' first.")
        sys.exit(1)
    return config


def main():
    parser = argparse.ArgumentParser(description="Douyin Automation Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, no actual publishing")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI text optimization")
    args = parser.parse_args()

    config = load_config()
    orchestrator = config["orchestrator"]

    # Check orchestrator exists
    if not Path(orchestrator).exists():
        print(f"ERROR: Orchestrator not found: {orchestrator}")
        print("Run 'python scripts/setup.py' to update paths.")
        sys.exit(1)

    # Build command
    cmd = [sys.executable, orchestrator]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.no_ai:
        cmd.append("--no-ai")

    print(f"[{time.strftime('%H:%M:%S')}] Douyin Pipeline START")
    print(f"[Config] Orchestrator: {orchestrator}")
    if args.dry_run:
        print("[Config] Mode: DRY RUN")
    if args.no_ai:
        print("[Config] AI: DISABLED")
    print()

    start = time.time()
    result = subprocess.run(cmd, cwd=str(Path(orchestrator).parent))
    duration = round(time.time() - start)

    print()
    status = "DONE" if result.returncode == 0 else "FAILED"
    print(f"[{time.strftime('%H:%M:%S')}] {status} (exit={result.returncode}, {duration}s)")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
