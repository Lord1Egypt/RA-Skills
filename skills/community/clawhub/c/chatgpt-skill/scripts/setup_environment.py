#!/usr/bin/env python3
"""Environment setup for ChatGPT skill."""

import os
import subprocess
import sys
import venv
from pathlib import Path


class SkillEnvironment:
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.venv_dir = self.skill_dir / ".venv"
        self.requirements_file = self.skill_dir / "requirements.txt"

        if os.name == "nt":
            self.venv_python = self.venv_dir / "Scripts" / "python.exe"
            self.venv_pip = self.venv_dir / "Scripts" / "pip.exe"
        else:
            self.venv_python = self.venv_dir / "bin" / "python"
            self.venv_pip = self.venv_dir / "bin" / "pip"

    def is_in_skill_venv(self) -> bool:
        if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
            return Path(sys.prefix) == self.venv_dir
        return False

    def ensure_venv(self) -> bool:
        if self.is_in_skill_venv():
            print("✅ Already running in skill virtual environment")
            return True

        if not self.venv_dir.exists():
            print(f"🔧 Creating virtual environment in {self.venv_dir.name}/")
            try:
                venv.create(self.venv_dir, with_pip=True)
            except Exception as error:
                print(f"❌ Failed to create venv: {error}")
                return False

        if self.requirements_file.exists():
            print("📦 Installing dependencies...")
            try:
                subprocess.run([str(self.venv_pip), "install", "--upgrade", "pip"], check=True)
                subprocess.run([str(self.venv_pip), "install", "-r", str(self.requirements_file)], check=True)
                print("🌐 Installing Google Chrome for Patchright...")
                try:
                    subprocess.run([str(self.venv_python), "-m", "patchright", "install", "chrome"], check=True)
                except subprocess.CalledProcessError as error:
                    print(f"⚠️ Warning: failed to install Chrome automatically: {error}")
                    print("   Run manually if needed: python -m patchright install chrome")
                return True
            except subprocess.CalledProcessError as error:
                print(f"❌ Dependency installation failed: {error}")
                return False

        return True


def main() -> int:
    env = SkillEnvironment()
    if env.ensure_venv():
        print("✅ Environment ready")
        return 0
    print("❌ Environment setup failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
