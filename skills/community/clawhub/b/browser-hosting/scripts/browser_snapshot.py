#!/usr/bin/env python3
"""
Browser snapshot script for OpenClaw browser hosting skill.

This script provides a wrapper around the openclaw browser snapshot command
with intelligent defaults and error handling.
"""

import subprocess
import sys
import json
import argparse

def run_browser_command(args):
    """Run openclaw browser command with given arguments."""
    cmd = ["openclaw", "browser"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running browser command: {e}", file=sys.stderr)
        print(f"Command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Take browser snapshot")
    parser.add_argument("--profile", default="openclaw", help="Browser profile (default: openclaw)")
    parser.add_argument("--format", choices=["ai", "aria"], default="ai", help="Snapshot format")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode for role-based refs")
    parser.add_argument("--compact", action="store_true", help="Compact output")
    parser.add_argument("--depth", type=int, help="Tree depth limit")
    parser.add_argument("--selector", help="CSS selector to scope snapshot")
    parser.add_argument("--frame", help="Frame selector to scope snapshot")
    parser.add_argument("--json", action="store_true", help="JSON output format")
    parser.add_argument("--labels", action="store_true", help="Include labeled screenshot")
    
    args = parser.parse_args()
    
    # Build command arguments
    cmd_args = ["--browser-profile", args.profile]
    
    if args.format == "aria":
        cmd_args.append("--format")
        cmd_args.append("aria")
    
    if args.interactive:
        cmd_args.append("--interactive")
    if args.compact:
        cmd_args.append("--compact")
    if args.depth:
        cmd_args.append("--depth")
        cmd_args.append(str(args.depth))
    if args.selector:
        cmd_args.append("--selector")
        cmd_args.append(args.selector)
    if args.frame:
        cmd_args.append("--frame")
        cmd_args.append(args.frame)
    if args.json:
        cmd_args.append("--json")
    if args.labels:
        cmd_args.append("--labels")
    
    cmd_args.append("snapshot")
    
    result = run_browser_command(cmd_args)
    if result is not None:
        print(result)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())