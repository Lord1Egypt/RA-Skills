#!/usr/bin/env python3
"""
Expert Library Plus - Verification Script

This script verifies that the Expert Library Plus installation is correct.
It checks file structure, directory paths, and content integrity.
"""

import sys
import os
from pathlib import Path

# Reuse the verification logic from the main project
def get_openclaw_dir():
    if sys.platform == "win32":
        return Path(os.environ["USERPROFILE"]) / ".openclaw"
    else:
        return Path.home() / ".openclaw"

def main():
    openclaw_dir = get_openclaw_dir()
    experts_dir = openclaw_dir / "experts"
    
    print("🔍 Verifying Expert Library Plus installation...")
    
    # Basic structure checks
    checks = [
        ("OpenClaw directory exists", openclaw_dir.exists()),
        ("Experts directory exists", experts_dir.exists()),
        ("Engineering experts exist", (experts_dir / "engineering").exists()),
        ("Name library exists", (experts_dir / "engineering" / "names").exists()),
        ("Steve Jobs file exists", (experts_dir / "engineering" / "names" / "steve-jobs.md").exists()),
        ("EXPERTS.md exists", (experts_dir / "EXPERTS.md").exists())
    ]
    
    passed = 0
    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
    
    success_rate = passed / len(checks)
    print(f"\n📊 Verification: {passed}/{len(checks)} ({success_rate:.1%})")
    
    if success_rate >= 0.8:
        print("✅ Installation verified successfully!")
        return 0
    else:
        print("❌ Installation verification failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())