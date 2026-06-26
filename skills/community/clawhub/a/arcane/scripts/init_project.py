#!/usr/bin/env python3
import os
import sys
import shutil

def init_project(target_dir):
    print(f"Initializing Arcane project in {target_dir}...")
    
    # Path to the boilerplate in the skill's assets
    # (Assuming the skill is in a predictable location or we use relative paths)
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(skill_dir, 'assets', 'boilerplate')
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Copy boilerplate files
    for item in os.listdir(assets_dir):
        s = os.path.join(assets_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
            
    print("Arcane project initialized successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: init_project.py <target_directory>")
        sys.exit(1)
    init_project(sys.argv[1])
