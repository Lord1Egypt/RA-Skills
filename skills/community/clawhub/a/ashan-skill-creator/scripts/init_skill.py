#!/usr/bin/env python3
"""
Skill Initializer - Create a new OpenClaw Skill directory

Usage:
    python3 init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets] [--examples]

Examples:
    python3 init_skill.py erpnext-helper --path ~/workspace/skills
    python3 init_skill.py finance-reconcile --path . --resources scripts,references
    python3 init_skill.py my-skill --path . --resources scripts --examples
"""

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = '''---
name: {skill_name}
description: [TODO: Complete description of what this skill does and when to trigger it.
Format: description + specific trigger conditions.
Put trigger conditions HERE (not in body) — body only loads after trigger.
Example: "Export ERPNext invoices. Triggered: (1) user says 'export invoices for month X';
(2) user provides company+month combo."]
---

# {skill_title}

## When to Use This Skill

[TODO: Specific trigger scenarios, how the user phrases requests, what file types or tasks activate this Skill]

## Context / Background

[TODO: Domain knowledge the Agent needs, specific to your use case.
Do not write general knowledge — only what the Agent doesn't already know.]

## Instructions / Steps

[TODO: Step-by-step workflow with clear quality criteria per step.
Use numbered lists. For each step explain: what, how (commands/code), how to verify.]

## Constraints / Guardrails

[TODO: Prohibitions based on real failure experience.
Format: - Never do X (because Y)
       - Must do X before Y
       - Avoid X, prefer Y]

## Examples (Recommended)

[TODO: Good/bad output comparisons.
Each example includes: scenario, good output (meets standard), bad output (pitfall case)]
'''

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} - Helper script

Description: What this script does.
Usage: python3 scripts/example.py [args]

Dependencies:
  - Python 3.8+
  - requests (pip install requests)

Example:
    python3 scripts/example.py --input data.csv
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{skill_name} helper tool")
    parser.add_argument("--input", required=True, help="Input file path")
    args = parser.parse_args()

    print(f"Processing: {{args.input}}")
    # TODO: Implement logic


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = '''# {skill_title} - Reference Documentation

Detailed reference material for {skill_title}, loaded on demand.

## Table of Contents

- [Overview](#overview)
- [API Reference](#api-reference)
- [FAQ](#faq)

## Overview

[TODO: Detailed description]

## API Reference

[TODO: API endpoints, parameters, return values]

## FAQ

[TODO: FAQ based on real user questions]

---

**When to load this file:**
- When the Agent needs to perform complex queries
- When SKILL.md mentions "see references/xxx"
- When user questions involve details covered here
'''

EXAMPLE_ASSET = '''# assets/ README

This directory holds files NOT loaded into context, but used in output.

**Common uses:**
- Template files (.xlsx, .docx, .pptx)
- Logo / image assets
- Font files
- Sample data (.csv, .json)

**Principle:** These files are NOT read into context — they are copied or modified for final output.

**To add assets:**
Place template/resource files directly in this directory and describe their purpose in SKILL.md's Resources section.
'''


def normalize_skill_name(skill_name: str) -> str:
    """Normalize to lowercase hyphen-case."""
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case(name: str) -> str:
    """Convert hyphenated name to Title Case."""
    return " ".join(word.capitalize() for word in name.split("-"))


def parse_resources(raw: str) -> list[str]:
    if not raw:
        return []
    resources = [item.strip() for item in raw.split(",") if item.strip()]
    invalid = sorted({r for r in resources if r not in ALLOWED_RESOURCES})
    if invalid:
        print(f"[ERROR] Unknown resource types: {', '.join(invalid)}")
        print(f"   Allowed: {', '.join(sorted(ALLOWED_RESOURCES))}")
        sys.exit(1)
    deduped, seen = [], set()
    for r in resources:
        if r not in seen:
            deduped.append(r)
            seen.add(r)
    return deduped


def create_skill(skill_name: str, path: str, resources: list[str], include_examples: bool):
    skill_dir = Path(path).resolve() / skill_name
    if skill_dir.exists():
        print(f"[ERROR] Directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created directory: {skill_dir}")
    except Exception as e:
        print(f"[ERROR] Failed to create directory: {e}")
        return None

    # SKILL.md
    skill_title = title_case(skill_name)
    content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)
    try:
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        print("[OK] Created SKILL.md")
    except Exception as e:
        print(f"[ERROR] Failed to write SKILL.md: {e}")
        return None

    # Resource directories
    for res in resources:
        res_dir = skill_dir / res
        res_dir.mkdir(exist_ok=True)
        if res == "scripts":
            if include_examples:
                (res_dir / "example.py").write_text(
                    EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8"
                )
                (res_dir / "example.py").chmod(0o755)
                print("[OK] Created scripts/example.py")
            else:
                print("[OK] Created scripts/")
        elif res == "references":
            if include_examples:
                (res_dir / "reference.md").write_text(
                    EXAMPLE_REFERENCE.format(skill_title=skill_title), encoding="utf-8"
                )
                print("[OK] Created references/reference.md")
            else:
                print("[OK] Created references/")
        elif res == "assets":
            if include_examples:
                (res_dir / "README.txt").write_text(EXAMPLE_ASSET, encoding="utf-8")
                print("[OK] Created assets/README.txt")
            else:
                print("[OK] Created assets/")

    print(f"\\n[OK] Skill '{skill_name}' initialized at: {skill_dir}")
    print("\\nNext steps:")
    print("1. Edit SKILL.md, fill in TODO items")
    print("2. Validate: python3 quick_validate.py <skill-path>")
    return skill_dir


def main():
    parser = argparse.ArgumentParser(description="Create a new OpenClaw Skill directory")
    parser.add_argument("skill_name", help="Skill name (lowercase letters/digits/hyphens)")
    parser.add_argument("--path", required=True, help="Output directory")
    parser.add_argument("--resources", default="", help="Resource dirs: scripts,references,assets")
    parser.add_argument("--examples", action="store_true", help="Create example files in resource dirs")
    args = parser.parse_args()

    name = normalize_skill_name(args.skill_name)
    if not name:
        print("[ERROR] Name must contain at least one letter or digit")
        sys.exit(1)
    if len(name) > MAX_SKILL_NAME_LENGTH:
        print(f"[ERROR] Name too long ({len(name)} chars), max {MAX_SKILL_NAME_LENGTH}")
        sys.exit(1)
    if name != args.skill_name:
        print(f"Note: Normalized name '{args.skill_name}' -> '{name}'")

    resources = parse_resources(args.resources)
    if args.examples and not resources:
        print("[ERROR] --examples requires --resources")
        sys.exit(1)

    print(f"Initializing skill: {name}")
    print(f"   Location: {args.path}")
    if resources:
        print(f"   Resources: {', '.join(resources)}")
        if args.examples:
            print("   Examples: enabled")
    print()

    result = create_skill(name, args.path, resources, args.examples)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
