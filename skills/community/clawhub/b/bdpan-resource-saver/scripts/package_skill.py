#!/usr/bin/env python3
"""
Skill Packager - Packages a skill into a .skill file

Usage:
    package_skill.py <path/to/skill-folder> [output-directory]
"""

import sys
import os
import zipfile
from pathlib import Path


def package_skill(skill_path, output_dir=None):
    """
    Package a skill directory into a .skill file.
    
    Args:
        skill_path: Path to the skill directory
        output_dir: Optional output directory (defaults to skill parent directory)
    
    Returns:
        Path to created .skill file, or None if error
    """
    skill_path = Path(skill_path).resolve()
    
    if not skill_path.exists():
        print(f"❌ Error: Skill path does not exist: {skill_path}")
        return None
    
    if not skill_path.is_dir():
        print(f"❌ Error: Skill path is not a directory: {skill_path}")
        return None
    
    # Check for required SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        print(f"❌ Error: Required file SKILL.md not found in {skill_path}")
        return None
    
    # Determine output path
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = skill_path.parent
    
    skill_file = output_path / f"{skill_name}.skill"
    
    # Create zip file with .skill extension
    try:
        with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(skill_path):
                # Skip __pycache__ and .pyc files
                dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith('.')]
                
                for file in files:
                    if file.endswith('.pyc') or file.startswith('.'):
                        continue
                    
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(skill_path)
                    zf.write(file_path, arcname)
                    print(f"  Added: {arcname}")
        
        print(f"\n✅ Skill packaged successfully: {skill_file}")
        return skill_file
        
    except Exception as e:
        print(f"❌ Error packaging skill: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExamples:")
        print("  package_skill.py my-skill")
        print("  package_skill.py my-skill ./dist")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()
    
    result = package_skill(skill_path, output_dir)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
