#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def main():
    ap = argparse.ArgumentParser(description="Verify published ClawHub skill state")
    ap.add_argument("slug", help="owner/skill")
    ap.add_argument("--expected-version")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rc, out = run(["clawhub", "inspect", args.slug, "--versions", "--limit", "8"])
    result = {"ok": rc == 0, "errors": [], "warnings": [], "notes": [], "latest": None, "versions": []}
    if rc != 0:
        result["errors"].append(out)
    else:
        latest_match = re.search(r"Latest:\s+([^\n]+)", out)
        if latest_match:
            result["latest"] = latest_match.group(1).strip()
        versions = re.findall(r"^(\d+\.\d+\.\d+)\s+", out, re.M)
        result["versions"] = versions
        if args.expected_version and result["latest"] and args.expected_version not in result["latest"]:
            result["warnings"].append(f"Expected latest {args.expected_version}, but inspect shows {result['latest']}")
        if args.expected_version and args.expected_version not in versions and (result["latest"] != args.expected_version):
            result["warnings"].append(f"Expected version {args.expected_version} not visible in first page of versions")
        result["notes"].append("Check the web page scan state manually if scan details matter; inspect is good for version/tag verification.")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Slug: {args.slug}")
        print(f"Status: {'OK' if result['ok'] else 'FAIL'}")
        if result['latest']:
            print(f"Latest: {result['latest']}")
        if result['versions']:
            print("Recent versions: " + ", ".join(result['versions']))
        if result['errors']:
            print("\nErrors:")
            for e in result['errors']:
                print(f"- {e}")
        if result['warnings']:
            print("\nWarnings:")
            for w in result['warnings']:
                print(f"- {w}")
        if result['notes']:
            print("\nNotes:")
            for n in result['notes']:
                print(f"- {n}")
    sys.exit(0 if result['ok'] else 1)


if __name__ == '__main__':
    main()
