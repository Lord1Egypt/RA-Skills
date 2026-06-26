#!/usr/bin/env python3
"""
Construction Law Skill — Unified CLI

A top-level dispatcher providing a single entry point for all skill scripts.
Run without arguments or with --help to see the full list of sub-commands.

Usage:
    python3 construction_law.py                     # show help
    python3 construction_law.py --list              # list all sub-commands
    python3 construction_law.py notices --form fidic-red
    python3 construction_law.py claims --form fidic-red --type disruption-claim
    python3 construction_law.py sop --claim-date 2026-05-15
    python3 construction_law.py compare --forms red,yellow --topic claims
    python3 construction_law.py obligations --form fidic-red
    python3 construction_law.py register --form fidic-red --type both --output reg.xlsx
    python3 construction_law.py delay --baseline-start 2026-05-01 --baseline-end 2026-12-31
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Ensure sibling scripts are importable as plain modules (no dynamic loaders).
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

SUB_COMMANDS = {
    "intake":      ("intake",               "🏗️ Matter intake — guided issue triage (recommended starting point)"),
    "wizard":      ("wizard",               "🧙 Interactive guided prompts for tools"),
    "notices":     ("notice_calendar",      "Generate notice/obligations calendar for a contract form"),
    "claims":      ("claims_template",      "Generate claim notice/EOT/VO/disruption letters"),
    "sop":         ("sop_calculator",       "Singapore SOP Act payment timeline calculator"),
    "compare":     ("fidic_comparator",     "Compare FIDIC contract forms side-by-side"),
    "obligations": ("obligations_register", "Generate party-by-party obligations register"),
    "register":    ("excel_register",       "Generate Excel workbook of obligations + notices"),
    "delay":       ("delay_calculator",     "Delay analysis & EOT entitlement calculator"),
    "deadline":    ("fidic_deadline",       "FIDIC deadline calculator — Singapore bundled; bring-your-own-holidays for other seats"),
}

def print_help():
    print("Construction Law Skill — Unified CLI\n")
    print("Usage: construction_law.py <command> [options]\n")
    print("Available commands:\n")
    for cmd, (script, desc) in SUB_COMMANDS.items():
        print(f"  {cmd:12s} {desc}")
    print("\nRun any command with --help for its specific options, e.g.:")
    print("  python3 construction_law.py notices --help")
    print("  python3 construction_law.py claims --help\n")
    print("Or call the underlying script directly:")
    for cmd, (mod_name, _) in SUB_COMMANDS.items():
        print(f"  python3 {mod_name}.py ...")

def run_script(module_name, argv):
    """Import a sibling module by name and call its main() with the given argv."""
    saved_argv = sys.argv
    sys.argv = [f"{module_name}.py"] + argv
    try:
        mod = __import__(module_name)
        if hasattr(mod, "main"):
            mod.main()
        else:
            print(f"Error: module '{module_name}' has no main()", file=sys.stderr)
            sys.exit(2)
    finally:
        sys.argv = saved_argv

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)
    if sys.argv[1] in ("--list", "-l", "list"):
        for cmd, (script, desc) in SUB_COMMANDS.items():
            print(f"{cmd:12s} -> {script:28s} {desc}")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in SUB_COMMANDS:
        print(f"Error: unknown command '{cmd}'\n", file=sys.stderr)
        print_help()
        sys.exit(1)

    module_name, _ = SUB_COMMANDS[cmd]
    run_script(module_name, sys.argv[2:])

if __name__ == "__main__":
    main()
