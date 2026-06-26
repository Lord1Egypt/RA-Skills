#!/usr/bin/env python3
"""
Initialize a new skill directory with the standard structure.

Usage:
    python init_skill.py <skill-name> [--path <output-directory>]

Example:
    python init_skill.py my-company-api --path ./skills
"""

import sys
from pathlib import Path

SKILL_MD_TEMPLATE = """---
name: {skill_name}
description: [Describe what this skill does and when to trigger it. Include specific trigger phrases. Max 1024 characters.]
---

# {skill_title}

## Overview

[What this skill does and why it exists.]

## Quick start

[The most common use case with a concrete example.]

## Workflow

[Step-by-step instructions for using this skill.]

## Reference files

- `references/` — [Describe what reference files are available and when to read them]
"""

INIT_PY_CONTENT = ""  # Empty init file


def to_title(name: str) -> str:
    """Convert kebab-case name to Title Case."""
    return " ".join(word.capitalize() for word in name.split("-"))


def init_skill(skill_name: str, output_path: Path) -> Path:
    """Create a new skill directory with standard structure.

    Args:
        skill_name: Kebab-case skill name
        output_path: Parent directory where the skill folder will be created

    Returns:
        Path to the created skill directory
    """
    skill_dir = output_path / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create directories
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)

    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(SKILL_MD_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=to_title(skill_name),
    ))

    # Create scripts/__init__.py
    (skill_dir / "scripts" / "__init__.py").write_text(INIT_PY_CONTENT)

    # Create .gitkeep files so empty dirs are tracked
    (skill_dir / "references" / ".gitkeep").write_text("")
    (skill_dir / "assets" / ".gitkeep").write_text("")

    return skill_dir


def main():
    if len(sys.argv) < 2:
        print("Usage: python init_skill.py <skill-name> [--path <output-directory>]")
        print("\nExample:")
        print("  python init_skill.py my-company-api --path ./skills")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Parse --path option
    output_path = Path.cwd()
    if "--path" in sys.argv:
        path_idx = sys.argv.index("--path")
        if path_idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[path_idx + 1])
        else:
            print("Error: --path requires a value")
            sys.exit(1)

    output_path = output_path.resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    skill_dir = init_skill(skill_name, output_path)
    print(f"✅ Skill scaffolded at: {skill_dir}")
    print(f"\nCreated structure:")
    print(f"  {skill_dir}/")
    print(f"  ├── SKILL.md")
    print(f"  ├── scripts/")
    print(f"  │   └── __init__.py")
    print(f"  ├── references/")
    print(f"  └── assets/")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_dir}/SKILL.md")
    print(f"  2. Add scripts, references, and assets as needed")
    print(f"  3. Validate with: python scripts/quick_validate.py {skill_dir}")


if __name__ == "__main__":
    main()
