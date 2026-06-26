#!/usr/bin/env python3
"""
Package Excellent AI Employee Skill for ClawHub distribution
"""
import os
import sys
import zipfile
import shutil
from pathlib import Path

def package_skill(skill_path, output_dir=None):
    """Package skill into .skill file"""
    skill_path = Path(skill_path)
    skill_name = skill_path.name
    
    if output_dir is None:
        output_dir = skill_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .skill filename
    skill_file = output_dir / f"{skill_name}.skill"
    
    # Create zip file
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                # Skip the package script itself to avoid recursion
                if file == 'package_skill.py':
                    continue
                # Calculate archive name (relative to skill directory)
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
    
    print(f"✅ Packaged skill: {skill_file}")
    print(f"📁 Contains {len(zf.filelist)} files")
    return skill_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill_directory> [output_directory]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        package_skill(skill_dir, output_dir)
        print("🎉 Skill packaging completed successfully!")
        print("You can now upload the .skill file to ClawHub.")
    except Exception as e:
        print(f"❌ Error during packaging: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()