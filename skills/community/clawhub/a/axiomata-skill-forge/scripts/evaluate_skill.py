#!/usr/bin/env python3
"""
Skill Forge — Evaluate Skill Quality
Wrapper around axiomata-skill-evaluator-v3

ERROR HANDLING CASES:
1. Empty path → caught by validation, returns False with message
2. Missing evaluator → checked before run, returns False
3. Missing skill → checked before run, returns False
4. Missing SKILL.md in directory → checked before run, returns False
5. Subprocess failure → caught by returncode check, returns False
6. Permission denied → caught by OSError handling, returns False
7. Timeout (>300s) → terminates subprocess, returns False
"""
import os
import sys
import subprocess

def evaluate_skill(skill_path):
    """Evaluate skill quality with axiomata-skill-evaluator-v3"""
    evaluator_path = "/mnt/Morgana/skills/axioma-skill-evaluator-v3/scripts/kan_evaluator.py"
    
    # Error handling for empty path
    if not skill_path:
        print("❌ Error: skill_path is required")
        return False
    
    if not os.path.exists(evaluator_path):
        print(f"❌ Error: evaluator not found at {evaluator_path}")
        return False
    
    if not os.path.exists(skill_path):
        print(f"❌ Error: skill path not found: {skill_path}")
        return False
    
    # Check if it's a directory or SKILL.md
    skill_file = skill_path
    if os.path.isdir(skill_path):
        skill_file = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_file):
            print(f"❌ Error: SKILL.md not found in {skill_path}")
            return False
    
    try:
        cmd = [sys.executable, evaluator_path, skill_file, "--verbose"]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  Warnings: {result.stderr}")
        
        # Return True if evaluation ran (even with low score)
        return "SCORE" in result.stdout or result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print("❌ Error: Evaluation timed out after 300 seconds")
        return False
    except PermissionError as e:
        print(f"❌ Error: Permission denied - {e}")
        return False
    except OSError as e:
        print(f"❌ Error: OS error - {e}")
        return False

# Error handling cases:
# - Empty path: caught by validation
# - Missing evaluator: checked before run
# - Missing skill: checked before run
# - Missing SKILL.md in directory: checked before run
# - Subprocess failure: caught by returncode check

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 evaluate_skill.py <skill-path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    success = evaluate_skill(skill_path)
    sys.exit(0 if success else 1)