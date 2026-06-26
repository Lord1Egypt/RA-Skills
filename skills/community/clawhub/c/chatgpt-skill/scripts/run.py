#!/usr/bin/env python3
"""Universal runner for ChatGPT skill scripts."""

import os
import subprocess
import sys
from pathlib import Path


def get_venv_python() -> Path:
    skill_dir = Path(__file__).parent.parent
    venv_dir = skill_dir / ".venv"
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def ensure_venv() -> Path:
    skill_dir = Path(__file__).parent.parent
    venv_dir = skill_dir / ".venv"
    setup_script = skill_dir / "scripts" / "setup_environment.py"

    if not venv_dir.exists():
        print("🔧 First-time setup: creating virtual environment...")
        result = subprocess.run([sys.executable, str(setup_script)])
        if result.returncode != 0:
            print("❌ Failed to set up environment")
            sys.exit(1)

    return get_venv_python()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/run.py <script_name> [args...]")
        print("   or: ./scripts/run.py <script_name> [args...]")
        print("Available scripts: auth_manager.py, ask_chatgpt.py, chat_manager.py, session_manager.py, cleanup_manager.py")
        return 1

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    if script_name.startswith("scripts/"):
        script_name = script_name[8:]
    if not script_name.endswith(".py"):
        script_name += ".py"

    skill_dir = Path(__file__).parent.parent
    script_path = skill_dir / "scripts" / script_name
    if not script_path.exists():
        print(f"❌ Script not found: {script_name}")
        print(f"   Looked for: {script_path}")
        return 1

    venv_python = ensure_venv()
    cmd = [str(venv_python), str(script_path)] + script_args

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        return 130
    except Exception as error:
        print(f"❌ Error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
