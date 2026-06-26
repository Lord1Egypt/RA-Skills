#!/usr/bin/env python3
"""Package skill into .skill file."""

import os
import sys
import zipfile
from pathlib import Path


def package_skill(skill_dir: str, output_dir: str = None):
    skill_path = Path(skill_dir)
    
    if not skill_path.exists():
        print(f"Error: Directory '{skill_dir}' not found")
        sys.exit(1)
    
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: SKILL.md not found")
        sys.exit(1)
    
    output_path = Path(output_dir) if output_dir else skill_path.parent
    skill_name = skill_path.name
    zip_path = output_path / f"{skill_name}.skill"
    
    print(f"Packing {skill_name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for file in files:
                if file.startswith(".") or file.endswith(".pyc"):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    print(f"\nCreated: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Package OpenClaw skill")
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument("--output", "-o", help="Output directory")
    args = parser.parse_args()
    package_skill(args.skill_dir, args.output)
