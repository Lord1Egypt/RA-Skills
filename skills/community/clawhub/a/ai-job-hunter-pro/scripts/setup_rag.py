#!/usr/bin/env python3
"""
AI Job Hunter Pro — Setup Script
Initializes the environment, database, and verifies dependencies.
"""

import os
import sys
import subprocess
import json

DATA_DIR = os.path.expanduser("~/.ai-job-hunter-pro")
DB_DIR = os.path.join(DATA_DIR, "chroma_db")
PROFILE_PATH = os.path.expanduser("~/job_profile.json")

def check_python_version():
    if sys.version_info < (3, 9):
        print(f"[ERROR] Python 3.9+ required. Found: {sys.version}")
        sys.exit(1)
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}")

def install_dependencies():
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_file):
        print("[SETUP] Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file, "-q"], check=True)
        print("[OK] Dependencies installed")
    else:
        print("[WARN] requirements.txt not found, installing core packages...")
        packages = ["chromadb", "sentence-transformers"]
        subprocess.run([sys.executable, "-m", "pip", "install"] + packages + ["-q"], check=True)

def init_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)
    print(f"[OK] Data directory: {DATA_DIR}")

def init_profile():
    if os.path.exists(PROFILE_PATH):
        print(f"[OK] Profile exists: {PROFILE_PATH}")
        return

    template_path = os.path.join(os.path.dirname(__file__), "..", "assets", "profile_template.json")
    if os.path.exists(template_path):
        import shutil
        shutil.copy(template_path, PROFILE_PATH)
        print(f"[SETUP] Profile template copied to {PROFILE_PATH}")
        print("[ACTION] Edit ~/job_profile.json with your information")
    else:
        print(f"[WARN] No profile found. Create one at {PROFILE_PATH}")

def verify_setup():
    print("\n" + "="*50)
    print("AI Job Hunter Pro — Setup Complete")
    print("="*50)
    print(f"  Data dir:    {DATA_DIR}")
    print(f"  Vector DB:   {DB_DIR}")
    print(f"  Profile:     {PROFILE_PATH}")
    print()
    print("Next steps:")
    print("  1. Edit ~/job_profile.json with your info")
    print("  2. Import your resume:")
    print("     python3 scripts/rag_engine.py --import-resume ~/resume.pdf")
    print("  3. Test job matching:")
    print("     python3 scripts/rag_engine.py --mode search --min-score 0.7")
    print()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Full initialization")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency install")
    args = parser.parse_args()

    print("="*50)
    print("AI Job Hunter Pro — Setup")
    print("="*50 + "\n")

    check_python_version()
    if not args.skip_deps:
        install_dependencies()
    init_directories()
    init_profile()
    verify_setup()

if __name__ == "__main__":
    main()
