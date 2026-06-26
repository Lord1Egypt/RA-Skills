#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def package_status(skill_dir: Path):
    cmd = ["python3", str(Path.home()/"project/openclaw/skills/skill-creator/scripts/package_skill.py"), str(skill_dir)]
    rc, out = run(cmd)
    if rc == 0:
        return None, "local package validation passed"
    low = out.lower()
    if "frontmatter" in low or "yaml" in low or "unexpected key" in low:
        return "frontmatter-invalid", out[-1200:]
    return "package-validation-failed", out[-1200:]


def inspect_status(slug: str, expected_version: str | None):
    rc, out = run(["clawhub", "inspect", slug, "--versions", "--limit", "10"])
    if rc != 0:
        return "inspect-failed", out[-1200:]
    latest = re.search(r"Latest:\s+([^\n]+)", out)
    latest_value = latest.group(1).strip() if latest else None
    versions = re.findall(r"^(\d+\.\d+\.\d+)\s+", out, re.M)
    if expected_version:
        if latest_value and expected_version != latest_value:
            return "latest-not-updated", f"expected {expected_version}, inspect latest is {latest_value}"
        if expected_version not in versions and latest_value != expected_version:
            return "version-not-visible", f"expected {expected_version} not found in recent versions"
    return None, f"inspect latest={latest_value or 'unknown'}"


def main():
    ap = argparse.ArgumentParser(description="Classify likely ClawHub publish failure buckets")
    ap.add_argument("--skill-dir")
    ap.add_argument("--slug")
    ap.add_argument("--expected-version")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    result = {"bucket": None, "details": [], "nextSteps": []}

    if args.skill_dir:
        bucket, detail = package_status(Path(args.skill_dir).expanduser().resolve())
        if bucket:
            result["bucket"] = bucket
            result["details"].append(detail)
            result["nextSteps"] = [
                "Fix local validation/package errors before any publish attempt.",
                "Trust validator output over memory of old formats.",
            ]
    if not result["bucket"] and args.slug:
        bucket, detail = inspect_status(args.slug, args.expected_version)
        if bucket:
            result["bucket"] = bucket
            result["details"].append(detail)
            if bucket == "latest-not-updated":
                result["nextSteps"] = [
                    "Confirm the publish command actually exited successfully.",
                    "Confirm you published from the skill folder, not a .skill archive.",
                    "Check whether the intended version exists in recent versions or the web page is still lagging.",
                ]
            else:
                result["nextSteps"] = ["Inspect the skill page and recent version history."]
    if not result["bucket"]:
        result["bucket"] = "no-hard-failure-detected"
        result["details"].append("No clear local package failure or latest-version mismatch detected.")
        result["nextSteps"] = [
            "If scan is still suspicious, investigate metadata drift between SKILL.md and scripts.",
            "If scan is pending, wait before republishing.",
            "If many versions were published quickly, inspect whether you are iterating docs/metadata rather than fixing a blocking failure.",
        ]

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Bucket: {result['bucket']}")
        print("Details:")
        for d in result['details']:
            print(f"- {d}")
        print("Next steps:")
        for s in result['nextSteps']:
            print(f"- {s}")


if __name__ == '__main__':
    main()
