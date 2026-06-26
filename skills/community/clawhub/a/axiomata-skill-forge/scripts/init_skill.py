#!/usr/bin/env python3
"""
Skill Forge — Initialize New Skill
Wrapper around skill-creator init_skill.py with additional logging
"""
import os
import sys
import subprocess

def init_skill(skill_name, skills_path="/mnt/Morgana/skills/"):
    """Initialize a new skill skeleton"""
    if not skill_name:
        print("❌ Error: skill_name is required")
        return False
    
    # Validate skill name
    if not all(c.islower() or c.isdigit() or c == '-' for c in skill_name):
        print("❌ Error: skill_name must be lowercase with hyphens only")
        return False
    
    # Validate path exists
    if not os.path.exists(skills_path):
        print(f"❌ Error: skills path does not exist: {skills_path}")
        return False
    
    script_path = "/mnt/Morgana/skills/skill-creator/scripts/init_skill.py"
    if not os.path.exists(script_path):
        print(f"❌ Error: {script_path} not found")
        return False
    
    try:
        cmd = [sys.executable, script_path, skill_name, "--path", skills_path]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            skill_dir = os.path.join(skills_path, skill_name)
            if os.path.exists(skill_dir):
                print(f"✅ Skill '{skill_name}' initialized at {skills_path}")
                return True
            else:
                print(f"❌ Error: init succeeded but directory not created")
                return False
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Error: Init timed out after 300 seconds")
        return False
    except PermissionError as e:
        print(f"❌ Error: Permission denied - {e}")
        return False
    except OSError as e:
        print(f"❌ Error: OS error - {e}")
        return False

# Error handling cases:
# - Invalid skill_name: caught by validation
# - Missing path: caught by path check
# - Script not found: caught by existence check
# - Subprocess failure: caught by returncode + directory check

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 init_skill.py <skill-name> [--path <path>]")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--path" else "/mnt/Morgana/skills/"
    
    success = init_skill(skill_name, path)
    sys.exit(0 if success else 1)