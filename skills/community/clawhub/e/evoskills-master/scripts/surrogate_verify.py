#!/usr/bin/env python3
"""Build a surrogate verification plan for evolving a skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from skill_audit import analyze_skill


def build_prompt_matrix(skill_name: str, goal: str) -> list[dict]:
    return [
        {
            "id": "trigger-fit",
            "prompt": f"Use ${skill_name} to help with a task that clearly matches its intended purpose.",
            "checks": ["skill triggers", "workflow starts quickly", "uses the main path instead of generic fallback"],
        },
        {
            "id": "ambiguous-input",
            "prompt": f"Use ${skill_name} on a vague request related to {goal or 'the target domain'} and see whether it asks only necessary clarifying questions.",
            "checks": ["handles ambiguity", "makes safe assumptions", "does not stall"],
        },
        {
            "id": "resource-usage",
            "prompt": f"Use ${skill_name} on a task that should require bundled scripts or references.",
            "checks": ["loads referenced files", "uses bundled scripts when appropriate", "does not reinvent existing resources"],
        },
        {
            "id": "verification-discipline",
            "prompt": f"Use ${skill_name} to make a non-trivial change and confirm it reports what verification ran.",
            "checks": ["runs validation", "reports evidence", "does not claim completion without checks"],
        },
    ]


def build_report(skill_dir: Path, goal: str) -> dict:
    audit = analyze_skill(skill_dir)
    skill_name = audit.get("skill", {}).get("name") or skill_dir.name
    prompt_matrix = build_prompt_matrix(skill_name, goal)
    blocking = [issue for issue in audit["issues"] if issue["severity"] == "error"]
    upgrade_recommendations = []

    if audit["ok"]:
        upgrade_recommendations.append("Increase prompt ambiguity and include a missing-prerequisite case.")
        upgrade_recommendations.append("Check whether the skill uses bundled resources instead of rewriting them inline.")
    else:
        upgrade_recommendations.append("Fix structural errors before running forward tests.")
        if any(issue["code"] == "todo" for issue in audit["issues"]):
            upgrade_recommendations.append("Remove template placeholders and restate the workflow in task-ready language.")

    return {
        "skill_dir": str(skill_dir),
        "goal": goal,
        "audit": audit,
        "blocking_issues": blocking,
        "prompt_matrix": prompt_matrix,
        "next_upgrades": upgrade_recommendations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a verifier plan for evolving a skill.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--goal", default="", help="Short statement of the improvement goal")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    report = build_report(Path(args.skill_dir), args.goal)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Surrogate verifier for: {report['skill_dir']}")
        if report["goal"]:
            print(f"Goal: {report['goal']}")
        print(report["audit"]["summary"])
        print("Prompt matrix:")
        for item in report["prompt_matrix"]:
            checks = ", ".join(item["checks"])
            print(f"- {item['id']}: {item['prompt']}")
            print(f"  checks: {checks}")
        print("Next upgrades:")
        for item in report["next_upgrades"]:
            print(f"- {item}")
    return 0 if report["audit"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
