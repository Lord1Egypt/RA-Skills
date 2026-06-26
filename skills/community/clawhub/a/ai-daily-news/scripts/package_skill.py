#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package AI Daily News skill for distribution
"""

import os
import sys
import zipfile
from pathlib import Path


def validate_skill(skill_path):
    """Validate skill structure"""
    skill_path = Path(skill_path)
    
    errors = []
    
    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found")
    else:
        # Check frontmatter
        content = skill_md.read_text(encoding='utf-8')
        if not content.startswith('---'):
            errors.append("SKILL.md missing YAML frontmatter")
        elif 'name:' not in content or 'description:' not in content:
            errors.append("SKILL.md missing name or description in frontmatter")
    
    # Check for symlinks (security)
    for root, dirs, files in os.walk(skill_path):
        for name in files + dirs:
            full_path = Path(root) / name
            if full_path.is_symlink():
                errors.append(f"Symlink found: {full_path}")
    
    return errors


def package_skill(skill_path, output_dir=None):
    """Package skill into .skill file"""
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        print(f"Error: Skill path not found: {skill_path}")
        sys.exit(1)
    
    # Validate
    print("Validating skill...")
    errors = validate_skill(skill_path)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("[OK] Validation passed")
    
    # Determine output path
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir) / f"{skill_name}.skill"
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = skill_path.parent / f"{skill_name}.skill"
    
    # Create zip
    print(f"Packaging to: {output_path}")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
                print(f"  + {arcname}")
    
    print(f"\n[OK] Skill packaged: {output_path}")
    print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill-path> [output-dir]")
        print("Example: python package_skill.py ai-daily-news ./dist")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    package_skill(skill_path, output_dir)
