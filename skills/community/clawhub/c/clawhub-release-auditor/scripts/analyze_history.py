#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from collections import Counter

KEYWORDS = {
    "docs": ["description", "documentation", "readme", "reference", "summary", "title", "opening", "copy"],
    "metadata": ["metadata", "homepage", "requires", "install", "frontmatter", "env", "bins"],
    "scan_or_security": ["scan", "suspicious", "security", "risk", "warning"],
    "bugfix": ["fix", "bug", "stability", "error", "mismatch"],
    "feature": ["added", "new", "support", "workflow", "feature", "expanded"],
}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def classify(text):
    low = text.lower()
    tags = []
    for label, words in KEYWORDS.items():
        if any(w in low for w in words):
            tags.append(label)
    return tags or ["other"]


def main():
    ap = argparse.ArgumentParser(description="Analyze version history patterns for a ClawHub skill")
    ap.add_argument("slug", help="skill slug, e.g. proactive-agent")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rc, out = run(["clawhub", "inspect", args.slug, "--versions", "--limit", str(args.limit)])
    result = {"ok": rc == 0, "errors": [], "latest": None, "owner": None, "recentVersions": [], "categories": {}, "notes": []}
    if rc != 0:
        result["errors"].append(out)
    else:
        m = re.search(r"Latest:\s+([^\n]+)", out)
        if m:
            result["latest"] = m.group(1).strip()
        m = re.search(r"Owner:\s+([^\n]+)", out)
        if m:
            result["owner"] = m.group(1).strip()
        versions = []
        for line in out.splitlines():
            line = line.rstrip()
            vm = re.match(r"^(\d+\.\d+\.\d+)\s+(\S+)\s+(.*)$", line)
            if vm:
                ver, ts, summary = vm.groups()
                versions.append({"version": ver, "timestamp": ts, "summary": summary})
        result["recentVersions"] = versions
        counter = Counter()
        for item in versions:
            for tag in classify(item["summary"]):
                counter[tag] += 1
        result["categories"] = dict(counter)
        if len(versions) >= 5:
            result["notes"].append("Many recent versions detected; likely iterative refinement rather than a one-shot publish.")
        if counter.get("docs", 0) >= 2:
            result["notes"].append("Frequent documentation/description edits suggest trigger clarity and onboarding copy matter a lot.")
        if counter.get("metadata", 0) >= 1:
            result["notes"].append("Metadata-related releases detected; declaration drift is a real maintenance cost.")
        if counter.get("bugfix", 0) >= 1:
            result["notes"].append("Bugfix/stability releases detected; local validation is not enough by itself.")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Skill: {args.slug}")
        print(f"Status: {'OK' if result['ok'] else 'FAIL'}")
        if result['owner']:
            print(f"Owner: {result['owner']}")
        if result['latest']:
            print(f"Latest: {result['latest']}")
        if result['recentVersions']:
            print("\nRecent versions:")
            for item in result['recentVersions']:
                print(f"- {item['version']} {item['timestamp']} :: {item['summary'][:110]}")
        if result['categories']:
            print("\nCategory counts:")
            for k, v in sorted(result['categories'].items()):
                print(f"- {k}: {v}")
        if result['notes']:
            print("\nNotes:")
            for n in result['notes']:
                print(f"- {n}")
        if result['errors']:
            print("\nErrors:")
            for e in result['errors']:
                print(f"- {e}")
    sys.exit(0 if result['ok'] else 1)


if __name__ == '__main__':
    main()
