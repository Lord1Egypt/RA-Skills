#!/usr/bin/env python3
"""Discover and scan all installed OpenClaw skills with Agent Audit.

Usage: python3 scan-all-skills.py
Exit codes: 0=ALL_SAFE, 1=SOME_WARNINGS, 2=CRITICAL_FOUND
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set


SELF_NAME = "agent-audit-scanner"

SKILL_LOCATIONS = [
    Path.home() / ".openclaw" / "workspace" / "skills",
    Path.home() / ".openclaw" / "skills",
]


def check_agent_audit() -> bool:
    """Verify agent-audit is installed."""
    try:
        subprocess.run(
            ["agent-audit", "--version"],
            capture_output=True, timeout=10,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def discover_skills() -> List[Path]:
    """Find all skill directories with SKILL.md files."""
    skills = []
    seen_names: Set[str] = set()

    for location in SKILL_LOCATIONS:
        if not location.is_dir():
            continue
        for child in sorted(location.iterdir()):
            if not child.is_dir():
                continue
            if not (child / "SKILL.md").exists() and not (child / "skill.md").exists():
                continue
            name = child.name.lower()
            if name == SELF_NAME:
                continue
            if name in seen_names:
                continue
            seen_names.add(name)
            skills.append(child)

    return skills


def scan_skill(skill_dir: Path) -> dict:
    """Run agent-audit scan on a single skill directory.

    Returns dict with keys: name, path, block, warn, info, findings, error
    """
    result = {
        "name": skill_dir.name,
        "path": str(skill_dir),
        "block": 0,
        "warn": 0,
        "info": 0,
        "findings": [],
        "error": None,
    }

    try:
        proc = subprocess.run(
            ["agent-audit", "scan", str(skill_dir), "--format", "json"],
            capture_output=True, text=True, timeout=120,
        )
        stdout = proc.stdout.strip()
        if not stdout:
            return result

        data = json.loads(stdout)
        findings = data.get("findings", data.get("results", []))
        if isinstance(data, list):
            findings = data

        for f in findings:
            tier = f.get("tier", f.get("level", "INFO")).upper()
            if tier == "BLOCK":
                result["block"] += 1
            elif tier == "WARN":
                result["warn"] += 1
            elif tier == "INFO":
                result["info"] += 1
            result["findings"].append(f)

    except json.JSONDecodeError as e:
        result["error"] = f"JSON parse error: {e}"
        result["warn"] += 1
    except subprocess.TimeoutExpired:
        result["error"] = "Scan timed out (120s)"
        result["warn"] += 1
    except Exception as e:
        result["error"] = str(e)
        result["warn"] += 1

    return result


def print_report(results: List[Dict]) -> int:
    """Print consolidated report and return exit code."""
    total = len(results)
    dangerous = [r for r in results if r["block"] > 0]
    review = [r for r in results if r["block"] == 0 and r["warn"] > 0]
    safe = [r for r in results if r["block"] == 0 and r["warn"] == 0]

    # Per-skill results
    for i, r in enumerate(results, 1):
        name = r["name"]
        pad = "." * max(1, 45 - len(name))
        if r["block"] > 0:
            status = f"\u274c {r['block']} BLOCK, {r['warn']} WARN"
        elif r["warn"] > 0:
            status = f"\u26a0\ufe0f  {r['warn']} WARN"
        else:
            status = "\u2705 Clean"
        print(f"  [{i}/{total}] {name} {pad} {status}")
        if r["error"]:
            print(f"         \u26a0\ufe0f  {r['error']}")

    # Summary
    print()
    print("\u2501" * 50)
    print("\ud83d\udcca Summary")
    print("\u2501" * 50)
    print()
    print(f"  Total scanned:  {total}")
    print(f"  \u2705 Safe:         {len(safe)}")
    print(f"  \u26a0\ufe0f  Review:      {len(review)}")
    print(f"  \u274c Dangerous:    {len(dangerous)}")
    print()

    if dangerous:
        print("  \ud83d\udeab DANGEROUS (do NOT enable):")
        for r in dangerous:
            print(f"    - {r['name']} ({r['block']} BLOCK)")
            for f in r["findings"]:
                if f.get("tier", f.get("level", "")).upper() == "BLOCK":
                    rule = f.get("rule_id", f.get("ruleId", "?"))
                    desc = f.get("description", f.get("message", ""))[:70]
                    print(f"      {rule}: {desc}")
        print()

    if review:
        print("  \u26a0\ufe0f  Skills needing review:")
        for r in review:
            print(f"    - {r['name']} ({r['warn']} WARN)")
        print()

    # Verdict
    if dangerous:
        print("  Overall: \u274c CRITICAL ISSUES FOUND")
        return 2
    elif review:
        print("  Overall: \u26a0\ufe0f  SOME SKILLS NEED REVIEW")
        return 1
    else:
        print("  Overall: \u2705 ALL SKILLS APPEAR SAFE")
        return 0


def main() -> int:
    print()
    print("\ud83d\udee1 Agent Audit \u2014 Full OpenClaw Skill Audit")
    print("\u2501" * 50)
    print()

    if not check_agent_audit():
        print("  Error: agent-audit is not installed.")
        print("  Install with: pip install agent-audit")
        return 1

    skills = discover_skills()
    if not skills:
        print("  No skills found in standard OpenClaw directories.")
        for loc in SKILL_LOCATIONS:
            print(f"    Checked: {loc}")
        return 0

    print(f"  Found {len(skills)} skill(s) to scan.")
    print()

    results = []
    for skill_dir in skills:
        result = scan_skill(skill_dir)
        results.append(result)

    return print_report(results)


if __name__ == "__main__":
    sys.exit(main())
