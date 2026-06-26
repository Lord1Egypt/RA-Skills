#!/usr/bin/env python3
"""
Axioma Guard Ultimate - Auto-Improve Script
Automatically improves skill quality
"""

import sys
import subprocess
import re

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 improve.py <skill-path> [--verbose]")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    print("=" * 60)
    print("AXIOMA GUARD ULTIMATE - Auto-Improve")
    print("=" * 60)
    
    eval_path = "/media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-skill-evaluator"
    
    # Run evaluation with improve
    print("\n[IMPROVING] Running evaluation with improvements...")
    result = subprocess.run(
        ["python3", f"{eval_path}/evaluator.py", skill_path, "--verbose", "--improve"],
        capture_output=True, text=True
    )
    
    # Extract score
    score_match = re.search(r'Score: (\d+)/100', result.stdout)
    if score_match:
        score = int(score_match.group(1))
        print(f"\n📊 Current Score: {score}/100")
        
        if score >= 70:
            print("✅ Score is acceptable!")
        else:
            print("⚠️ Score still below 70 - manual intervention may be needed")
    
    if verbose:
        print(result.stdout)
    else:
        print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    
    print("\n" + "=" * 60)
    print("IMPROVE COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
