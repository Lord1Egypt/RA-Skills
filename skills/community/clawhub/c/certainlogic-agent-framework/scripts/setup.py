#!/usr/bin/env python3
"""
Agent Framework Setup — full stack bootstrap.

Creates SOUL.md, AGENTS.md, MEMORY.md, and optionally initializes the timechain.

Usage:
    python3 setup.py                                    # interactive defaults
    python3 setup.py --name Alex --role "Chief of Staff" --principal Anton
    python3 setup.py --name Alex --init-chain           # also init timechain
    python3 setup.py --name Alex --chain-name "Alex"    # custom chain name
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = Path.cwd()
TEMPLATES = SKILL_DIR / "references"
TIMECHAIN = SKILL_DIR / "timechain"
STAGE_FILE = WORKSPACE / ".framework-stage"


def get_stage():
    """Read current framework stage from dotfile."""
    if STAGE_FILE.exists():
        return STAGE_FILE.read_text().strip()
    return "none"


def set_stage(stage):
    """Write current framework stage to dotfile."""
    STAGE_FILE.write_text(stage)
    print(f"  Stage set to: {stage}")


def bootstrap_soul(name, role, principal):
    """Create or update SOUL.md."""
    src = TEMPLATES / "SOUL.md.template"
    dst = WORKSPACE / "SOUL.md"

    if not src.exists():
        print("  ⚠️  Template not found, skipping SOUL.md")
        return False

    content = src.read_text()
    content = content.replace("[Agent Name]", name)
    content = content.replace("[Role]", role)
    content = content.replace("[Principal]", principal)

    if dst.exists():
        prev = dst.read_text()
        if prev == content:
            print(f"  SOUL.md — unchanged")
            return True

    dst.write_text(content)
    print(f"  Created {dst}")
    return True


def bootstrap_agents():
    """Create AGENTS.md."""
    src = TEMPLATES / "AGENTS.md.template"
    dst = WORKSPACE / "AGENTS.md"

    if not src.exists():
        print("  ⚠️  Template not found, skipping AGENTS.md")
        return False

    if dst.exists():
        print(f"  AGENTS.md — already exists, skipping")
        return True

    dst.write_text(src.read_text())
    print(f"  Created {dst}")
    return True


def bootstrap_memory():
    """Create MEMORY.md skeleton."""
    dst = WORKSPACE / "MEMORY.md"
    if dst.exists():
        return True

    content = "# MEMORY.md — Session Continuity\n\n"
    content += f"## Session Start\n\n"
    content += f"- **Date:** (set on first use)\n"
    content += f"- **Context:** (describe current state)\n"
    content += f"- **Active tasks:** (list)\n"
    dst.write_text(content)
    print(f"  Created {dst}")
    return True


def init_timechain(chain_name):
    """Initialize the timechain if not already done."""
    chain_path = TIMECHAIN / "chain"
    if chain_path.exists() and any(chain_path.iterdir()):
        print(f"  Timechain already initialized at {TIMECHAIN}")
        return True

    if not (TIMECHAIN / "timechain.py").exists():
        print(f"  ⚠️  timechain.py not found at {TIMECHAIN}")
        return False

    print(f"  Initializing timechain for '{chain_name}'...")
    result = subprocess.run(
        [sys.executable, str(TIMECHAIN / "timechain.py"), "init",
         "--name", chain_name, "--root", str(TIMECHAIN)],
        capture_output=True, text=True, timeout=30,
        cwd=str(WORKSPACE),
    )
    if result.returncode == 0:
        print(f"  Timechain initialized ✅")
        return True
    else:
        print(f"  ⚠️  Timechain init failed: {result.stderr[:200]}")
        print(f"     You can init manually: python3 timechain/timechain.py init --name \"{chain_name}\"")
        return False


def print_next_steps(name, chain_inited):
    """Print next-step instructions."""
    print(f"\n{'='*50}")
    print(f"  🚀  Setup Complete")
    print(f"{'='*50}")
    print(f"\n  Agent: {name}")
    print(f"  Stage: {'Level 3 — Full Stack' if chain_inited else 'Level 1 — Identity'}")
    print(f"\n  Next steps:")

    if not chain_inited:
        print(f"\n    1. Initialize the timechain for persistent memory:")
        print(f"       python3 skills/certainlogic-agent-framework/timechain/timechain.py init --name \"{name}\"")
        print(f"       python3 skills/certainlogic-agent-framework/timechain/timechain.py verify")
    else:
        print(f"\n    1. Verify the timechain:")
        print(f"       python3 skills/certainlogic-agent-framework/timechain/timechain.py verify")
        print(f"\n    2. Tell your agent:")
        print(f"       I am running the CertainLogic Agent Framework. Read SOUL.md and AGENTS.md.")
        print(f"       Activate the self-model per the skill instructions.")

    print(f"\n  Edit these files to customize:")
    print(f"    SOUL.md    — identity (name, role, style)")
    print(f"    AGENTS.md  — rules (add your own hard rules)")
    print(f"    MEMORY.md  — session continuity")

    print(f"\n  Upgrade path:")
    print(f"    Level 1 → Identity (current)" if not chain_inited else "    ✅ Level 1 — Identity")
    print(f"    Level 2 → Add AGENTS.md cycle" if not chain_inited else "    ✅ Level 2 — Cycle")
    print(f"    Level 3 → Init timechain" if not chain_inited else "    ✅ Level 3 — Self-Model")
    print(f"    Level 4 → Connect Brain API + Timechain services"
          if not (TIMECHAIN / "chain").exists() or not any((TIMECHAIN / "chain").iterdir()) else "")
    print()


def main():
    parser = argparse.ArgumentParser(description="Bootstrap agent identity + timechain")
    parser.add_argument("--name", default="Alex", help="Agent name")
    parser.add_argument("--role", default="Chief of Staff", help="Agent role")
    parser.add_argument("--principal", default="Your Principal", help="Principal name")
    parser.add_argument("--init-chain", action="store_true", help="Also initialize timechain")
    parser.add_argument("--chain-name", default=None, help="Timechain name (defaults to --name)")
    args = parser.parse_args()

    chain_name = args.chain_name or args.name

    print("=== CertainLogic Agent Framework Setup ===\n")

    # Layer 1: Identity
    print("[Layer 1] Identity...")
    bootstrap_soul(args.name, args.role, args.principal)

    # Layer 2: Cycle
    print("[Layer 2] Execution cycle...")
    bootstrap_agents()

    # Memory
    print("[Layer 2] Session memory...")
    bootstrap_memory()

    # Layer 3: Timechain (optional)
    chain_inited = False
    if args.init_chain:
        print("[Layer 3] Self-model timechain...")
        chain_inited = init_timechain(chain_name)

    print_next_steps(args.name, chain_inited)


if __name__ == "__main__":
    main()