#!/usr/bin/env python3
"""
upgrade_cc.py
Upgrade Claude Code to the latest published version and re-run the date-line
audit. Dry-run by default; pass --apply to actually run the npm install.

The upgrade is a global npm side effect -- only run with --apply AND after the
user has explicitly agreed.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "audit_cc_date_prompt.py")

def run(cmd):
    print("+ " + " ".join(cmd))
    return subprocess.run(cmd)

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    if apply:
        run(["npm", "install", "-g", "@anthropic-ai/claude-code@latest"])
    else:
        print("DRY RUN -- would run: npm install -g @anthropic-ai/claude-code@latest")
        print("Re-run with --apply to perform the upgrade (needs your confirmation).")
    print("\nRe-auditing:")
    run([sys.executable, AUDIT])
