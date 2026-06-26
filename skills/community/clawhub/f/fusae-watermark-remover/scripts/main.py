#!/usr/bin/env python3
"""Watermark remover skill script wrapper

This script wraps the watermark-remover CLI for use as a Claude Code skill.
It requires the watermark-remover package to be installed.
"""

import sys
import subprocess
import shutil
from pathlib import Path


def check_installation():
    """Check if watermark-remover is installed"""
    return shutil.which("watermark-remover") is not None


def print_installation_help():
    """Print installation instructions"""
    print("\n❌ Error: watermark-remover is not installed.\n", file=sys.stderr)
    print("📦 Installation options:\n", file=sys.stderr)
    print("  Option 1 - Install from PyPI (when published):", file=sys.stderr)
    print("    pip install watermark-remover\n", file=sys.stderr)
    print("  Option 2 - Install from source:", file=sys.stderr)
    print("    git clone https://github.com/yourusername/watermark-remover.git", file=sys.stderr)
    print("    cd watermark-remover", file=sys.stderr)
    print("    pip install -e .\n", file=sys.stderr)
    print("  Option 3 - Install from local directory:", file=sys.stderr)

    # Try to find the project root
    skill_dir = Path(__file__).resolve().parent.parent
    possible_roots = [
        skill_dir.parent.parent,  # skills/watermark-remover -> project root
        Path.home() / "Projects" / "watermark-remover",
    ]

    for root in possible_roots:
        if (root / "pyproject.toml").exists():
            print(f"    cd {root}", file=sys.stderr)
            print("    pip install -e .\n", file=sys.stderr)
            break
    else:
        print("    cd /path/to/watermark-remover", file=sys.stderr)
        print("    pip install -e .\n", file=sys.stderr)

    print("📖 For more details, see:", file=sys.stderr)
    print(f"    {skill_dir / 'README.md'}\n", file=sys.stderr)


def main():
    """Run watermark-remover CLI"""
    # Check if installed
    if not check_installation():
        print_installation_help()
        sys.exit(1)

    # Run the CLI
    try:
        result = subprocess.run(
            ["watermark-remover"] + sys.argv[1:],
            check=False
        )
        sys.exit(result.returncode)
    except Exception as e:
        print(f"\n❌ Error running watermark-remover: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
