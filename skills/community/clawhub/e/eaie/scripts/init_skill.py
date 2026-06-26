#!/usr/bin/env python3
"""
Initialize Excellent AI Employee Skill structure
"""
import os
import sys

def create_skill_structure(base_path):
    """Create the complete skill directory structure"""
    directories = [
        os.path.join(base_path, 'references'),
        os.path.join(base_path, 'scripts'),
        os.path.join(base_path, 'assets')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create placeholder files if they don't exist
    placeholder_files = {
        'scripts/__init__.py': '# Python package marker\n',
        'assets/README.md': '# Assets directory\n\nPlace output templates, images, or other resources here.\n'
    }
    
    for filepath, content in placeholder_files.items():
        full_path = os.path.join(base_path, filepath)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"Created placeholder: {full_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python init_skill.py <skill_directory>")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    create_skill_structure(skill_dir)
    print(f"Excellent AI Employee skill structure initialized at: {skill_dir}")