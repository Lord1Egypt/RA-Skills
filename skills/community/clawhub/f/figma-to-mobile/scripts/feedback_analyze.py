#!/usr/bin/env python3
"""
Feedback Analyzer for figma-to-mobile skill.

Parses feedback-log.md, groups corrections by platform and Figma node type,
identifies high-frequency issues, and generates rule candidates.

Usage:
    python feedback_analyze.py [feedback-log.md]

If no path is given, looks for feedback-log.md in the parent directory.
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def parse_feedback_log(path: str) -> list[dict]:
    """Parse feedback-log.md into a list of entry dicts."""
    text = Path(path).read_text(encoding="utf-8")
    entries = []
    # Split on ## YYYY-MM-DD HH:MM headers
    blocks = re.split(r"(?=^## \d{4}-\d{2}-\d{2} \d{2}:\d{2})", text, flags=re.MULTILINE)

    for block in blocks:
        block = block.strip()
        if not block.startswith("## "):
            continue

        entry = {}
        # Date
        date_match = re.match(r"## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", block)
        if date_match:
            entry["date"] = date_match.group(1)

        # Fields
        for field in ["Platform", "Figma node type", "Issue", "Before", "After", "Rule candidate"]:
            pattern = rf"\*\*{re.escape(field)}\*\*:\s*(.+?)(?=\n- \*\*|\n```|\Z)"
            match = re.search(pattern, block, re.DOTALL)
            if match:
                entry[field.lower().replace(" ", "_")] = match.group(1).strip()

        if entry.get("platform") and entry.get("issue"):
            entries.append(entry)

    return entries


def analyze(entries: list[dict]) -> dict:
    """Analyze entries and return statistics."""
    stats = {
        "total": len(entries),
        "by_platform": Counter(),
        "by_node_type": Counter(),
        "by_platform_node": Counter(),
        "issues": defaultdict(list),
        "rule_candidates": [],
    }

    for e in entries:
        platform = e.get("platform", "unknown")
        node_type = e.get("figma_node_type", "unknown")
        issue = e.get("issue", "")
        rule = e.get("rule_candidate", "")

        stats["by_platform"][platform] += 1
        stats["by_node_type"][node_type] += 1
        stats["by_platform_node"][(platform, node_type)] += 1
        stats["issues"][(platform, node_type)].append(issue)

        if rule:
            stats["rule_candidates"].append({
                "platform": platform,
                "node_type": node_type,
                "rule": rule,
                "source_issue": issue,
            })

    return stats


def generate_report(stats: dict) -> str:
    """Generate a human-readable report with rule candidates."""
    lines = []
    lines.append("# Feedback Analysis Report")
    lines.append(f"\nTotal corrections: **{stats['total']}**\n")

    # By platform
    lines.append("## By Platform\n")
    for platform, count in stats["by_platform"].most_common():
        lines.append(f"- {platform}: {count}")

    # By node type
    lines.append("\n## By Figma Node Type\n")
    for node_type, count in stats["by_node_type"].most_common():
        lines.append(f"- {node_type}: {count}")

    # Top issues (platform + node type combos with >= 2 occurrences)
    lines.append("\n## High-Frequency Issues (≥2 occurrences)\n")
    frequent = [(k, v) for k, v in stats["by_platform_node"].items() if v >= 2]
    frequent.sort(key=lambda x: x[1], reverse=True)

    if frequent:
        for (platform, node_type), count in frequent:
            lines.append(f"### {platform} — {node_type} ({count} corrections)\n")
            for issue in stats["issues"][(platform, node_type)]:
                lines.append(f"  - {issue}")
            lines.append("")
    else:
        lines.append("No patterns with ≥2 occurrences yet. Keep collecting feedback.\n")

    # Rule candidates
    lines.append("## Rule Candidates\n")
    lines.append("These are suggested rules extracted from feedback. **Review before merging into patterns.**\n")

    if stats["rule_candidates"]:
        for i, rc in enumerate(stats["rule_candidates"], 1):
            lines.append(f"### Candidate {i}")
            lines.append(f"- **Platform**: {rc['platform']}")
            lines.append(f"- **Node type**: {rc['node_type']}")
            lines.append(f"- **Rule**: {rc['rule']}")
            lines.append(f"- **Source issue**: {rc['source_issue']}")
            lines.append("")
    else:
        lines.append("No explicit rule candidates logged yet.\n")

    # Action items
    lines.append("## Suggested Actions\n")
    if frequent:
        lines.append("The following platform/node combos have recurring issues and likely need new or updated rules:\n")
        for (platform, node_type), count in frequent:
            target_file = {
                "Android XML": "xml-patterns.md",
                "Compose": "compose-patterns.md",
                "SwiftUI": "swiftui-patterns.md",
                "UIKit": "uikit-patterns.md",
            }.get(platform, "SKILL.md")
            lines.append(f"- [ ] **{platform} — {node_type}** ({count}x) → update `references/{target_file}`")
    else:
        lines.append("No action items yet. Collect more feedback.\n")

    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    else:
        # Look in parent directory
        log_path = str(Path(__file__).parent.parent / "feedback-log.md")

    if not Path(log_path).exists():
        print(f"feedback-log.md not found at: {log_path}")
        print("Usage: python feedback_analyze.py [path/to/feedback-log.md]")
        sys.exit(1)

    entries = parse_feedback_log(log_path)

    if not entries:
        print("No feedback entries found. The log file may be empty or have no valid entries.")
        print("Expected format: ## YYYY-MM-DD HH:MM followed by - **Platform**: ... etc.")
        sys.exit(0)

    stats = analyze(entries)
    report = generate_report(stats)

    # Write report
    report_path = Path(log_path).parent / "feedback-report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Report generated: {report_path}")
    print(f"  {stats['total']} entries analyzed")
    print(f"  {len(stats['rule_candidates'])} rule candidates found")

    frequent = sum(1 for v in stats["by_platform_node"].values() if v >= 2)
    if frequent:
        print(f"  {frequent} high-frequency pattern(s) detected — review suggested actions")


if __name__ == "__main__":
    main()
