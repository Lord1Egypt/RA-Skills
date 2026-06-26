#!/usr/bin/env python3
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, EXPORT_DIR

def main():
    parser = argparse.ArgumentParser(description="Export a case to markdown")
    parser.add_argument("--id", required=True, help="Case ID")
    args = parser.parse_args()

    data = load_cases()
    case = data["cases"].get(args.id)
    if not case:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{args.id}.md")

    lines = []
    lines.append(f"# {case['title']}")
    lines.append("")
    lines.append(f"- ID: {case['id']}")
    lines.append(f"- Created: {case['created_at']}")
    lines.append(f"- Overall score: {case.get('score', {}).get('overall')}")
    lines.append(f"- Promotion status: {case.get('promotion_status', 'none')}")
    lines.append("")

    for key, label in [
        ("problem", "Problem"),
        ("goal", "Goal"),
    ]:
        lines.append(f"## {label}")
        lines.append(str(case.get(key, "")))
        lines.append("")

    for section_key, section_title in [
        ("assumptions", "Assumptions"),
        ("truths", "Truths"),
        ("components", "Components"),
        ("constraints", "Constraints"),
        ("anti_patterns", "Anti-patterns"),
        ("heuristics_used", "Heuristics used"),
        ("rebuilt_solution", "Rebuilt solution"),
        ("next_actions", "Next actions"),
    ]:
        lines.append(f"## {section_title}")
        for item in case.get(section_key, []):
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Reusable pattern candidate")
    lines.append(case.get("reusable_pattern_candidate", ""))
    lines.append("")

    lines.append("## Score")
    lines.append("```json")
    lines.append(json.dumps(case.get("score", {}), indent=2, ensure_ascii=False))
    lines.append("```")
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("✓ Exported:", path)

if __name__ == "__main__":
    main()
