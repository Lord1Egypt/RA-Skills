#!/usr/bin/env python3
"""
Email Bridge skill installer and entry point.
When first called, installs the package if needed, then forwards commands.
"""

import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
VENV_DIR = SKILL_DIR / ".venv"
EMAIL_BRIDGE_CMD = "email-bridge"


def is_installed() -> bool:
    """Check if email-bridge is available."""
    try:
        subprocess.run(
            [EMAIL_BRIDGE_CMD, "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_package():
    """Install email-bridge package."""
    print("📧 正在安装 Email Bridge...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ 需要 Python 3.10 或更高版本")
        sys.exit(1)
    
    # Install using pip
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", str(SKILL_DIR)],
        check=True
    )
    
    print("✅ Email Bridge 安装完成")


def main():
    """Main entry point."""
    # Check if installed
    if not is_installed():
        install_package()
    
    # Forward command to email-bridge
    cmd = [EMAIL_BRIDGE_CMD] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()