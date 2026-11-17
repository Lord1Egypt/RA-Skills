#!/usr/bin/env python3
"""Report safe, platform-specific DATAIFY_API_TOKEN setup guidance."""

import argparse
import json
import os
import platform


VARIABLE = "DATAIFY_API_TOKEN"


def detect_environment(system=None, shell=None):
    system = (system or platform.system()).lower()
    shell_name = os.path.basename(shell or os.environ.get("SHELL", "")).lower()
    if system == "windows":
        return "windows", shell_name or "powershell"
    if system in ("darwin", "macos"):
        return "macos", shell_name or "zsh"
    return "linux", shell_name or "bash"


def guidance(system, shell):
    if system == "windows" and shell == "cmd":
        return {
            "setup_command": "set DATAIFY_API_TOKEN=YOUR_TOKEN",
            "verify_command": "if defined DATAIFY_API_TOKEN (echo configured) else (echo missing)",
        }
    if system == "windows":
        return {
            "setup_command": '$env:DATAIFY_API_TOKEN = "YOUR_TOKEN"',
            "verify_command": 'if ($env:DATAIFY_API_TOKEN) { "configured" } else { "missing" }',
        }
    return {
        "setup_command": "export DATAIFY_API_TOKEN='YOUR_TOKEN'",
        "verify_command": 'test -n "$DATAIFY_API_TOKEN" && echo "configured" || echo "missing"',
    }


def report(system=None, shell=None):
    current_system, current_shell = detect_environment(system, shell)
    configured = bool(os.environ.get(VARIABLE, "").strip())
    result = {
        "variable": VARIABLE,
        "configured": configured,
        "platform": current_system,
        "shell": current_shell,
        "token_value_exposed": False,
    }
    if not configured:
        result.update(guidance(current_system, current_shell))
        result["restart_note"] = "Persistent changes require a new terminal or agent application restart."
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=("macos", "linux", "windows"))
    parser.add_argument("--shell", help="Override shell detection, for example zsh, bash, powershell, or cmd.")
    args = parser.parse_args()
    print(json.dumps(report(args.platform, args.shell), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
