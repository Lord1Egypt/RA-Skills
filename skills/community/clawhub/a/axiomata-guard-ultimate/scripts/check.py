#!/usr/bin/env python3
"""
Axioma Guard Ultimate - Main Script
Complete security + quality check for downloaded skills
"""

import sys
import subprocess
import os

def main():
    skill_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    quick_mode = "--quick" in sys.argv
    
    print("=" * 60)
    print("AXIOMA GUARD ULTIMATE - Security + Quality Check")
    print("=" * 60)
    
    # Phase 1: Security Check
    print("\n[PHASE 1] Security Check...")
    guard_path = "/media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-guard"
    guard_script = os.path.join(guard_path, "merlin-guard.py")
    
    if os.path.exists(guard_script):
        result = subprocess.run(
            ["python3", guard_script, "scan", skill_path],
            capture_output=True, text=True
        )
        print(result.stdout if result.stdout else "Security scan completed")
    else:
        print("⚠️ merlin-guard.py not found at", guard_script)
    
    # Phase 2: Quality Evaluation
    print("\n[PHASE 2] Quality Evaluation...")
    eval_path = "/media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-skill-evaluator"
    eval_script = os.path.join(eval_path, "evaluator.py")
    iso_script = os.path.join(eval_path, "eval-skill.py")
    
    # Run Axioma evaluation
    if os.path.exists(eval_script):
        result = subprocess.run(
            ["python3", eval_script, skill_path, "--verbose"],
            capture_output=True, text=True
        )
        print(result.stdout)
    else:
        print("⚠️ evaluator.py not found at", eval_script)
    
    if not quick_mode:
        # Run ISO 25010 check
        if os.path.exists(iso_script):
            result = subprocess.run(
                ["python3", iso_script, skill_path, "--verbose"],
                capture_output=True, text=True
            )
            print(result.stdout)
    
    print("\n" + "=" * 60)
    print("CHECK COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()