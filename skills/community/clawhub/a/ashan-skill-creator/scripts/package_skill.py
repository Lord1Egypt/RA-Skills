#!/usr/bin/env python3
"""
Skill Packager - Package a Skill directory into a distributable .skill file

Usage:
    python3 package_skill.py <skill-path> [output-directory]

Example:
    python3 package_skill.py ../skills/my-new-skill
    python3 package_skill.py ../skills/my-new-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from typing import Optional

from quick_validate import validate_skill

EXCLUDED_DIRS = {".git", ".svn", ".hg", "__pycache__", "node_modules", ".DS_Store"}


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def package_skill(skill_path: str, output_dir: Optional[str] = None) -> Optional[Path]:
    """Package a Skill directory into a .skill file (zip format)."""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"[ERROR] Directory not found: {skill_path}")
        return None
    if not skill_path.is_dir():
        print(f"[ERROR] Not a directory: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found: {skill_md}")
        return None

    # Validate before packaging
    print("Validating skill...")
    valid, msg = validate_skill(skill_path)
    if not valid:
        print(f"[ERROR] Validation failed: {msg}")
        print("   Please fix errors before packaging.")
        return None
    print(f"[OK] {msg}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_file = output_path / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in skill_path.rglob("*"):
                if file_path.is_symlink():
                    print(f"[SKIP] Symlink: {file_path}")
                    continue
                rel_parts = file_path.relative_to(skill_path).parts
                if any(p in EXCLUDED_DIRS for p in rel_parts):
                    continue
                if file_path.is_file():
                    resolved = file_path.resolve()
                    if not _is_within(resolved, skill_path):
                        print(f"[ERROR] File escapes Skill root: {file_path}")
                        return None
                    # Don't package the output file itself
                    if resolved == skill_file.resolve():
                        print(f"[SKIP] Output file: {file_path}")
                        continue
                    arcname = Path(skill_name) / file_path.relative_to(skill_path)
                    zf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n[OK] Packaged to: {skill_file}")
        return skill_file

    except Exception as e:
        print(f"[ERROR] Packaging failed: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 package_skill.py <skill-path> [output-directory]")
        print("\nExamples:")
        print("  python3 package_skill.py ../skills/my-new-skill")
        print("  python3 package_skill.py ../skills/my-new-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
