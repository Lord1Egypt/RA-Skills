#!/usr/bin/env python3
"""
Configuration module for flyai-travelmapify skill.
Dynamically determines paths and settings based on environment.
"""

import os
import sys
import subprocess
from pathlib import Path

def get_workspace_dir():
    """
    Determine the OpenClaw workspace directory dynamically.
    Uses relative path from skill directory.
    """
    # Current script directory (should be in skills/flyai-travelmapify/scripts/)
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    workspace_dir = skill_dir.parent.parent
    
    # Verify this is a valid OpenClaw workspace
    if (workspace_dir / "AGENTS.md").exists() or (workspace_dir / "SOUL.md").exists():
        return str(workspace_dir)
    
    # Fallback to current working directory
    return os.getcwd()

def find_flyai_executable():
    """
    Find the flyai executable in the system PATH or common locations.
    """
    # First, try to find it in PATH
    try:
        result = subprocess.run(['which', 'flyai'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    
    # Try npm global bin directory
    try:
        result = subprocess.run(['npm', 'bin', '-g'], capture_output=True, text=True)
        if result.returncode == 0:
            npm_bin = result.stdout.strip()
            flyai_path = Path(npm_bin) / "flyai"
            if flyai_path.exists():
                return str(flyai_path)
    except FileNotFoundError:
        pass
    
    # Try common Node.js installation paths
    home = Path.home()
    common_paths = [
        home / ".nvm" / "versions" / "node",
        home / ".local" / "share" / "npm" / "bin",
        "/usr/local/bin",
        "/opt/homebrew/bin"
    ]
    
    for base_path in common_paths:
        if base_path.exists():
            for flyai_path in base_path.rglob("flyai"):
                if flyai_path.is_file():
                    return str(flyai_path)
    
    # If not found, return None - caller should handle this
    return None

def get_skill_dir():
    """Get the skill directory path"""
    return str(Path(__file__).parent.parent)

# Configuration constants
WORKSPACE_DIR = get_workspace_dir()
SKILL_DIR = get_skill_dir()
FLYAI_EXECUTABLE = find_flyai_executable()

# Default ports
DEFAULT_HTTP_PORT = 9000
DEFAULT_HOTEL_PORT = 8780
DEFAULT_PROXY_URL = "http://localhost:8769/api/search"

if __name__ == "__main__":
    print(f"Workspace directory: {WORKSPACE_DIR}")
    print(f"Skill directory: {SKILL_DIR}")
    print(f"FlyAI executable: {FLYAI_EXECUTABLE}")