#!/usr/bin/env python3
"""
OpenClaw skill wrapper for Claw Code harness.
Call as: python3 claw_wrapper.py <command> [--flag value]...
"""

import sys
import json
import asyncio
from pathlib import Path

# Add the shared skills directory to path
sys.path.insert(0, ".")

try:
    import claw_harness
except ImportError as e:
    print(f"❌ Failed to import claw_harness: {e}", file=sys.stderr)
    print(f"   Python path: {sys.path}", file=sys.stderr)
    sys.exit(1)


def parse_args(argv):
    """Parse argv into command and dict of flags."""
    if not argv:
        return None, {}
    
    command = argv[0]
    args = {}
    i = 1
    while i < len(argv):
        arg = argv[i]
        if not arg.startswith("--"):
            print(f"❌ Expected flag starting with '--', got: {arg}", file=sys.stderr)
            sys.exit(1)
        key = arg[2:]
        i += 1
        if i >= len(argv):
            print(f"❌ Missing value for flag: {arg}", file=sys.stderr)
            sys.exit(1)
        value = argv[i]
        i += 1
        
        # Try to infer type
        if value.lower() == "true":
            args[key] = True
        elif value.lower() == "false":
            args[key] = False
        elif value.isdigit():
            args[key] = int(value)
        else:
            try:
                args[key] = float(value)
            except ValueError:
                args[key] = value
    return command, args


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 claw_wrapper.py <command> [--flag value]...", file=sys.stderr)
        print("Commands: summary, manifest, subsystems, commands, tools, parity-audit", file=sys.stderr)
        sys.exit(1)
    
    command, args = parse_args(sys.argv[1:])
    
    try:
        result = await claw_harness.claw_invoke(command, args)
        print(json.dumps(result, indent=2))
    except Exception as e:
        error_result = {
            "ok": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "command": command,
            "args": args,
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())