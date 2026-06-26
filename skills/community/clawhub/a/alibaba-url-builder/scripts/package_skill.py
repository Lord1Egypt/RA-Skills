#!/usr/bin/env python3
"""
Package the alibaba-url-builder skill into a .skill file.
"""

import os
import sys
import zipfile
from pathlib import Path


def package_skill(skill_dir: str, output_dir: str = None):
    """Package skill directory into a .skill zip file."""
    skill_path = Path(skill_dir)
    
    if not skill_path.exists():
        print(f"Error: Directory '{skill_dir}' not found")
        sys.exit(1)
    
    if not (skill_path / 'SKILL.md').exists():
        print(f"Error: SKILL.md not found in '{skill_dir}'")
        sys.exit(1)
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = skill_path.parent
    
    skill_name = skill_path.name
    zip_path = output_path / f"{skill_name}.skill"
    
    # Create zip file
    print(f"Packing {skill_name}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.startswith('.'):
                    continue
                if file.endswith('.pyc'):
                    continue
                    
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    print(f"\nCreated: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")
    return zip_path


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Package OpenClaw skill')
    parser.add_argument('skill_dir', help='Path to skill directory')
    parser.add_argument('--output', '-o', help='Output directory (default: same as skill)')
    
    args = parser.parse_args()
    package_skill(args.skill_dir, args.output)
