#!/usr/bin/env python3
"""
Expert Library Plus - Installation Script

This script installs the Expert Library Plus system to ~/.openclaw/experts/
It handles cross-platform installation, backup, and verification.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def get_openclaw_dir():
    """Get OpenClaw configuration directory based on platform"""
    if sys.platform == "win32":
        return Path(os.environ["USERPROFILE"]) / ".openclaw"
    else:
        return Path.home() / ".openclaw"

def backup_existing_experts(openclaw_dir):
    """Backup existing experts directory"""
    experts_dir = openclaw_dir / "experts"
    if experts_dir.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = experts_dir.with_name(f"experts.backup.{timestamp}")
        print(f"Backing up existing experts to {backup_dir}")
        shutil.copytree(experts_dir, backup_dir)
        return backup_dir
    return None

def install_expert_library(source_dir, target_dir):
    """Install expert library from source to target"""
    print(f"Installing Expert Library Plus to {target_dir}")
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files and directories
    for item in source_dir.iterdir():
        if item.is_dir():
            shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target_dir / item.name)
    
    print("✅ Installation completed successfully!")

def main():
    parser = argparse.ArgumentParser(description="Install Expert Library Plus")
    parser.add_argument("--source", default=".", help="Source directory containing expert library")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup of existing experts")
    args = parser.parse_args()
    
    # Get directories
    openclaw_dir = get_openclaw_dir()
    experts_dir = openclaw_dir / "experts"
    source_dir = Path(args.source) / "experts"
    
    # Validate source directory
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        sys.exit(1)
    
    print("🚀 Installing Expert Library Plus...")
    print(f"📁 OpenClaw directory: {openclaw_dir}")
    
    # Backup existing experts (unless disabled)
    if not args.no_backup:
        backup_existing_experts(openclaw_dir)
    
    # Install expert library
    install_expert_library(source_dir, experts_dir)
    
    # Verify installation
    verify_path = Path(__file__).parent.parent / "verify.py"
    if verify_path.exists():
        print("\n🔍 Verifying installation...")
        os.system(f"python {verify_path}")
    
    print("\n🎉 Expert Library Plus is ready to use!")
    print("Try: '请专家帮我设计一个产品'")

if __name__ == "__main__":
    main()