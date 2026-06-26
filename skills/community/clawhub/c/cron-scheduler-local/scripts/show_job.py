#!/usr/bin/env python3
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs

def main():
    parser = argparse.ArgumentParser(description="Show one job")
    parser.add_argument("--id", required=True)
    args = parser.parse_args()

    jobs = load_jobs().get("jobs", {})
    if args.id not in jobs:
        print(f"Job not found: {args.id}")
        sys.exit(1)

    print(json.dumps(jobs[args.id], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
