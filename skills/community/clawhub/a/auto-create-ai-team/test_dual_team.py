#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test dual team functionality for Auto-Create-AI-Team Skill
"""

import os
import sys
import tempfile
import shutil
import subprocess
import argparse

def test_dual_team_creation(project_path, project_type="generic"):
    """Test creating dual team (internal + internet)"""
    print(f"Testing dual team creation for {project_type} project...")
    
    # Run the skill
    result = subprocess.run([
        "python3", "create_ai_team.py",
        "--project-path", project_path,
        "--project-type", project_type,
        "--team-type", "dual"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Dual team creation successful!")
        print(f"Output: {result.stdout}")
        
        # Verify directories exist
        ai_team_dir = os.path.join(project_path, "ai-team")
        internal_team = os.path.join(ai_team_dir, "internal-team")
        internet_team = os.path.join(ai_team_dir, "internet-team")
        
        if os.path.exists(internal_team) and os.path.exists(internet_team):
            print("✅ Both internal and internet teams created successfully!")
            return True
        else:
            print("❌ Missing team directories")
            return False
    else:
        print(f"❌ Dual team creation failed: {result.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test dual team functionality')
    parser.add_argument('--project-path', help='Project path for testing')
    parser.add_argument('--project-type', default='generic', 
                       choices=['generic'],  # Only generic type now
                       help='Project type (only generic supported)')
    
    args = parser.parse_args()
    
    if args.project_path:
        project_path = args.project_path
        os.makedirs(project_path, exist_ok=True)
    else:
        # Create temporary directory
        project_path = tempfile.mkdtemp(prefix="test_dual_team_")
        print(f"Using temporary directory: {project_path}")
    
    try:
        success = test_dual_team_creation(project_path, args.project_type)
        if success:
            print("🎉 All dual team tests passed!")
        else:
            print("❌ Dual team tests failed!")
            sys.exit(1)
    finally:
        if not args.project_path:
            # Clean up temporary directory
            shutil.rmtree(project_path)
            print("Cleaned up temporary directory")

if __name__ == '__main__':
    main()