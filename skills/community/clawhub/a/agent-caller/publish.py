#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布Agency Agents Caller到ClawHub
"""

import os
import shutil
import tarfile
from datetime import datetime

def create_skill_package():
    """创建技能包"""
    
    skill_dir = "skills/agency-agents-caller"
    output_dir = "skills/packages"
    
    print("="*70)
    print("Creating Agency Agents Caller Skill Package")
    print("="*70)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打包文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"agency-agents-caller_{timestamp}.tar.gz"
    package_path = os.path.join(output_dir, package_name)
    
    print(f"\nSkill Directory: {skill_dir}")
    print(f"Package Name: {package_name}")
    
    # 创建tar.gz包
    with tarfile.open(package_path, "w:gz") as tar:
        # 添加必需文件
        files_to_pack = [
            "SKILL.md",
            "README.md",
            "package.json",
            "scripts/agent_caller.py",
            "examples/usage_demo.py"
        ]
        
        for file in files_to_pack:
            file_path = os.path.join(skill_dir, file)
            if os.path.exists(file_path):
                print(f"  Adding: {file}")
                tar.add(file_path, arcname=file)
            else:
                print(f"  Missing: {file}")
    
    print(f"\nPackage created: {package_path}")
    print(f"Package size: {os.path.getsize(package_path)} bytes")
    
    return package_path

def generate_publish_instructions():
    """生成发布指令"""
    
    print("\n" + "="*70)
    print("Publish to ClawHub")
    print("="*70)
    
    print("""
Option 1: Using ClawHub CLI (Recommended)

1. Install ClawHub CLI:
   npm install -g clawhub-cli

2. Login to ClawHub:
   clawhub login

3. Publish the skill:
   cd skills/agency-agents-caller
   clawhub publish


Option 2: Using ClawHub Web UI

1. Visit: https://clawhub.com/publish

2. Upload the package:
   - Package: skills/packages/agency-agents-caller_YYYYMMDD_HHMMSS.tar.gz

3. Fill in the details:
   - Name: agency-agents-caller
   - Version: 1.0.0
   - Description: Call 179 professional agents on-demand
   - Category: productivity
   - Keywords: agents, ai, collaboration, database, search

4. Submit for review


Option 3: Manual Publishing

1. Copy skill files to ClawHub:
   cp -r skills/agency-agents-caller ~/.clawhub/skills/

2. Register with ClawHub:
   clawhub register agency-agents-caller


After Publishing:

Your skill will be available at:
https://clawhub.com/skills/agency-agents-caller

Users can install it with:
clawhub install agency-agents-caller
""")

if __name__ == "__main__":
    package_path = create_skill_package()
    generate_publish_instructions()
    
    print("\n" + "="*70)
    print("Ready to Publish!")
    print("="*70)
    print(f"\nPackage: {package_path}")
    print("\nFollow the instructions above to publish to ClawHub.")
