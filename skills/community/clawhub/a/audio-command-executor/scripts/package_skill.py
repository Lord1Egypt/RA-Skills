#!/usr/bin/env python3
"""
Simple skill packaging script.
Creates a .skill file (ZIP) from the skill directory.
"""

import os
import sys
import zipfile
from pathlib import Path

def package_skill(skill_path, output_dir=None):
    """Package a skill directory into a .skill file."""
    
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        print(f"Error: Skill directory '{skill_path}' not found")
        sys.exit(1)
    
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: SKILL.md not found in '{skill_path}'")
        sys.exit(1)
    
    # Check for symlinks (security)
    for root, dirs, files in os.walk(skill_path):
        for f in files:
            filepath = Path(root) / f
            if filepath.is_symlink():
                print(f"Error: Symlinks are not allowed. Found: {filepath}")
                sys.exit(1)
    
    # Determine output directory
    if output_dir is None:
        output_dir = skill_path.parent / "dist"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .skill file
    skill_name = skill_path.name
    skill_file = output_dir / f"{skill_name}.skill"
    
    print(f"Packaging skill: {skill_name}")
    print(f"Output: {skill_file}")
    
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filepath in skill_path.rglob('*'):
            if filepath.is_file():
                # Store with relative path from skill directory
                arcname = filepath.relative_to(skill_path)
                zf.write(filepath, arcname)
                print(f"  Added: {arcname}")
    
    print(f"\n✅ Skill packaged successfully: {skill_file}")
    return skill_file

if __name__ == "__main__":
    # Default: package current directory
    skill_path = "."
    output_dir = None
    
    # Parse arguments
    if len(sys.argv) > 1:
        skill_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    package_skill(skill_path, output_dir)
