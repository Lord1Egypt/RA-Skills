#!/usr/bin/env python3
"""analyze_tokens.py - Estimate token usage for a Claude skill directory.

Usage: python3 analyze_tokens.py <skill-directory>

Reads all files in the skill directory, estimates token counts using a ~4 chars/token
heuristic, and categorizes by file type. Checks for progressive disclosure patterns.

Outputs JSON to stdout.
"""

import json
import os
import re
import sys


def count_tokens(text: str) -> int:
    """Estimate token count using ~4 chars per token heuristic."""
    return max(1, len(text) // 4)


def check_progressive_disclosure(skill_md_content: str) -> dict:
    """Check if SKILL.md uses progressive disclosure (references to external files)."""
    patterns = {
        "file_references": len(re.findall(r'(?:Read|read|load|see|refer to)\s+[`"\']?[\w/.-]+\.\w+', skill_md_content)),
        "script_calls": len(re.findall(r'(?:Run|run|execute)\s+[`"\']?scripts/', skill_md_content)),
        "reference_links": len(re.findall(r'references/', skill_md_content)),
        "asset_links": len(re.findall(r'assets/', skill_md_content)),
    }
    total_refs = sum(patterns.values())
    patterns["total_external_references"] = total_refs
    patterns["uses_progressive_disclosure"] = total_refs >= 2
    return patterns


def categorize_file(filepath: str, base_dir: str) -> str:
    """Categorize a file based on its location and name."""
    rel_path = os.path.relpath(filepath, base_dir)

    if os.path.basename(filepath) == "SKILL.md":
        return "skill_md"
    elif rel_path.startswith("references") or rel_path.startswith("refs"):
        return "reference"
    elif rel_path.startswith("scripts") or rel_path.startswith("script"):
        return "script"
    elif rel_path.startswith("assets") or rel_path.startswith("asset"):
        return "asset"
    else:
        return "other"


def analyze_directory(skill_dir: str) -> dict:
    """Analyze all files in a skill directory for token usage."""
    categories = {
        "skill_md": {"files": [], "total_tokens": 0, "total_chars": 0},
        "reference": {"files": [], "total_tokens": 0, "total_chars": 0},
        "script": {"files": [], "total_tokens": 0, "total_chars": 0},
        "asset": {"files": [], "total_tokens": 0, "total_chars": 0},
        "other": {"files": [], "total_tokens": 0, "total_chars": 0},
    }

    skill_md_content = ""

    for root, _dirs, files in os.walk(skill_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, skill_dir)

            # Skip hidden files and common non-content files
            if filename.startswith(".") or filename in ("__pycache__",):
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except (IOError, OSError):
                continue

            char_count = len(content)
            token_count = count_tokens(content)
            category = categorize_file(filepath, skill_dir)

            if category == "skill_md":
                skill_md_content = content

            categories[category]["files"].append({
                "path": rel_path,
                "chars": char_count,
                "tokens": token_count,
            })
            categories[category]["total_tokens"] += token_count
            categories[category]["total_chars"] += char_count

    # Calculate totals
    total_tokens = sum(cat["total_tokens"] for cat in categories.values())
    total_chars = sum(cat["total_chars"] for cat in categories.values())
    total_files = sum(len(cat["files"]) for cat in categories.values())

    # Check progressive disclosure
    disclosure = check_progressive_disclosure(skill_md_content)

    # Rate token usage
    if total_tokens < 2000 and disclosure["uses_progressive_disclosure"]:
        rating = "Low"
        reasoning = f"Total ~{total_tokens} tokens with progressive disclosure. Efficient design."
    elif total_tokens <= 5000:
        rating = "Medium"
        reasoning = f"Total ~{total_tokens} tokens."
        if not disclosure["uses_progressive_disclosure"]:
            reasoning += " Consider adding progressive disclosure to reduce context usage."
    else:
        rating = "High"
        reasoning = f"Total ~{total_tokens} tokens."
        if not disclosure["uses_progressive_disclosure"]:
            reasoning += " No progressive disclosure detected — all content loaded at once."
        else:
            reasoning += " Even with progressive disclosure, total content is substantial."

    # SKILL.md line count
    skill_md_lines = len(skill_md_content.splitlines()) if skill_md_content else 0

    return {
        "summary": {
            "total_tokens": total_tokens,
            "total_chars": total_chars,
            "total_files": total_files,
            "skill_md_lines": skill_md_lines,
            "rating": rating,
            "reasoning": reasoning,
        },
        "progressive_disclosure": disclosure,
        "categories": {
            "skill_md_tokens": categories["skill_md"]["total_tokens"],
            "reference_tokens": categories["reference"]["total_tokens"],
            "script_tokens": categories["script"]["total_tokens"],
            "asset_tokens": categories["asset"]["total_tokens"],
            "other_tokens": categories["other"]["total_tokens"],
        },
        "details": {k: v for k, v in categories.items() if v["files"]},
    }


def main():
    if len(sys.argv) < 2:
        print("Error: Missing skill directory path", file=sys.stderr)
        print("Usage: python3 analyze_tokens.py <skill-directory>", file=sys.stderr)
        sys.exit(1)

    skill_dir = sys.argv[1]

    if not os.path.isdir(skill_dir):
        print(f"Error: Not a directory: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    result = analyze_directory(skill_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
