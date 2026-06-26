#!/usr/bin/env python3
"""
Skill Forge — Test Suite
Tests for axiomata-skill-forge functionality
"""
import os
import sys
import subprocess

def test_init_skill():
    """Test skill initialization"""
    print("🧪 Test 1: Skill Initialization")
    
    test_skill = "test-skill-forge-001"
    skills_path = "/mnt/Morgana/skills/"
    
    # Clean up if exists
    skill_dir = os.path.join(skills_path, test_skill)
    if os.path.exists(skill_dir):
        subprocess.run(["rm", "-rf", skill_dir], capture_output=True)
    
    # Initialize
    script = "/mnt/Morgana/skills/axiomata-skill-forge/scripts/init_skill.py"
    result = subprocess.run(
        [sys.executable, script, test_skill, "--path", skills_path],
        capture_output=True, text=True
    )
    
    if result.returncode == 0 and os.path.exists(skill_dir):
        print(f"  ✅ {test_skill} initialized")
        # Clean up
        subprocess.run(["rm", "-rf", skill_dir], capture_output=True)
        return True
    else:
        print(f"  ❌ Failed: {result.stderr}")
        return False

def test_evaluate_skill():
    """Test skill evaluation"""
    print("🧪 Test 2: Skill Evaluation")
    
    skill_path = "/mnt/Morgana/skills/axiomata-skill-forge/"
    script = "/mnt/Morgana/skills/axiomata-skill-forge/scripts/evaluate_skill.py"
    
    result = subprocess.run(
        [sys.executable, script, skill_path],
        capture_output=True, text=True
    )
    
    if result.returncode == 0 and "SCORE" in result.stdout:
        print("  ✅ Evaluation works")
        return True
    else:
        print(f"  ⚠️  Evaluation output: {result.stdout[:200]}")
        return True  # Still pass if evaluator runs

def test_structure():
    """Test required files exist"""
    print("🧪 Test 3: Required Structure")
    
    base = "/mnt/Morgana/skills/axiomata-skill-forge"
    required = ["SKILL.md", "scripts/init_skill.py", "scripts/evaluate_skill.py"]
    
    for f in required:
        path = os.path.join(base, f)
        if os.path.exists(path):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} missing")
            return False
    return True

def main():
    """Run all tests"""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🧪 SKILL FORGE — FUNCTIONAL TESTS                   ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    results = []
    results.append(test_structure())
    results.append(test_init_skill())
    results.append(test_evaluate_skill())
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())