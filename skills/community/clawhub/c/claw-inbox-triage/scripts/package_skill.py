#!/usr/bin/env python3
"""
Packaging script for inbox-triage skill.
Run this to create a distributable .skill package.
"""

import json
import os
import sys
from pathlib import Path

def get_file_list(root_path: Path) -> list:
    """Get all files in the skill directory."""
    files = []
    for root, dirs, filenames in os.walk(root_path):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                continue
            filepath = Path(root) / filename
            rel_path = filepath.relative_to(root_path)
            files.append(str(rel_path))
    return files

def validate_skill(root_path: Path) -> bool:
    """Validate skill structure."""
    required = [
        "SKILL.md",
        "scripts/"
    ]
    
    for item in required:
        if not (root_path / item).exists():
            print(f"❌ Missing required item: {item}")
            return False
    
    print("✅ Skill structure validated")
    return True

def main():
    """Create .skill package."""
    skill_dir = Path(__file__).parent.parent  # Parent is the skill root
    output_dir = sys.argv[1] if len(sys.argv) > 1 else skill_dir
    
    # Validate first
    if not validate_skill(skill_dir):
        print("❌ Validation failed")
        sys.exit(1)
    
    # Get file list
    files = get_file_list(skill_dir)
    
    # Create package metadata
    package = {
        "name": "inbox-triage",
        "version": "1.0.0",
        "description": "Automated message filtering, prioritization, and response drafting",
        "files": files,
        "created": Path(__file__).stat().st_ctime
    }
    
    # Output package info (for manual packaging)
    print("📦 Package metadata:")
    print(json.dumps(package, indent=2))

if __name__ == "__main__":
    main()
