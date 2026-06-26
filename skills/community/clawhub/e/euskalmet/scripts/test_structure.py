#!/usr/bin/env python3
"""Test script to verify the skill structure is correct."""

import os
import sys

def check_file(path, description):
    """Check if a file exists and report."""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("🔍 Euskalmet Skill Structure Test")
    print("=" * 50)
    
    checks = []
    
    # Check main files
    checks.append(check_file("scripts/main.py", "Main script"))
    checks.append(check_file("requirements.txt", "Requirements file"))
    checks.append(check_file(".env", "Environment file"))
    checks.append(check_file("available-locations.json", "Locations file"))
    checks.append(check_file("SKILL.md", "Skill documentation"))
    
    # Check directories
    checks.append(check_file("venv/bin/python3", "Virtual environment"))
    checks.append(check_file("forecasts", "Forecasts directory"))
    checks.append(check_file("images", "Images directory"))
    checks.append(check_file("images-modern", "Modern images directory"))
    
    # Check imports
    print("\n📦 Import tests:")
    try:
        import jwt
        print("✅ PyJWT import works")
    except ImportError as e:
        print(f"❌ PyJWT import failed: {e}")
        
    try:
        import requests
        print("✅ requests import works")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        
    try:
        import dotenv
        print("✅ python-dotenv import works")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 All structure checks passed!")
        return 0
    else:
        print("⚠️  Some checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
