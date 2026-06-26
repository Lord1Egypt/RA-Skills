#!/usr/bin/env python3
"""
Simple skill packaging script for founder-article
Creates a .skill file (zip with .skill extension)
"""

import os
import zipfile
import sys
from pathlib import Path

def package_skill(skill_dir, output_dir=None):
    skill_path = Path(skill_dir)
    if not skill_path.exists():
        print(f"Error: Skill directory {skill_dir} does not exist")
        return False
    
    # Get skill name from directory or SKILL.md
    skill_name = skill_path.name
    
    # Output directory
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = skill_path.parent
    
    output_path.mkdir(exist_ok=True)
    
    # Create .skill file (zip)
    skill_file = output_path / f"{skill_name}.skill"
    
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            # Skip .git, __pycache__, .DS_Store
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                    
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
    
    print(f"✅ Skill packaged: {skill_file}")
    print(f"📦 Size: {skill_file.stat().st_size / 1024:.1f} KB")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python package.py <skill_directory> [output_directory]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = package_skill(skill_dir, output_dir)
    sys.exit(0 if success else 1)