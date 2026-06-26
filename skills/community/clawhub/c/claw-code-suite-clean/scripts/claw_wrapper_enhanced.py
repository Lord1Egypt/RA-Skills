#!/usr/bin/env python3
"""
Enhanced OpenClaw skill wrapper for Claw Code harness.
Supports positional arguments and expanded command set.

Usage: python3 claw_wrapper_enhanced.py <command> [positional_args...] [--flag value]...

Examples:
  python3 claw_wrapper_enhanced.py summary
  python3 claw_wrapper_enhanced.py tools --limit 10
  python3 claw_wrapper_enhanced.py route "analyze bash script" --limit 5
  python3 claw_wrapper_enhanced.py exec-tool bashSecurity "$(cat script.sh)"
  python3 claw_wrapper_enhanced.py exec-command advisor "review this code"
"""

import sys
import json
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from claw_harness_enhanced import claw_invoke, COMMAND_DEFS, ALLOWED_COMMANDS
except ImportError as e:
    print(f"❌ Failed to import enhanced harness: {e}", file=sys.stderr)
    print(f"   Python path: {sys.path}", file=sys.stderr)
    sys.exit(1)


def parse_argv(argv):
    """Parse argv into command, positional args, and flag args."""
    if not argv:
        return None, [], {}
    
    command = argv[0]
    if command not in ALLOWED_COMMANDS:
        return command, [], {}  # Will be caught later
    
    positional_names, allowed_flags = COMMAND_DEFS[command]
    positional_args = []
    flag_args = {}
    
    i = 1
    # Collect positional arguments (until we hit a --flag or run out)
    while i < len(argv) and not argv[i].startswith("--"):
        if len(positional_args) >= len(positional_names):
            print(f"⚠️  Warning: extra positional argument '{argv[i]}' for command '{command}'", 
                  file=sys.stderr)
        positional_args.append(argv[i])
        i += 1
    
    # Collect flag arguments
    while i < len(argv):
        arg = argv[i]
        if not arg.startswith("--"):
            print(f"❌ Expected flag starting with '--', got: {arg}", file=sys.stderr)
            sys.exit(1)
        
        key = arg[2:].replace("-", "_")  # Convert kebab-case to snake_case
        i += 1
        if i >= len(argv):
            print(f"❌ Missing value for flag: {arg}", file=sys.stderr)
            sys.exit(1)
        
        value = argv[i]
        i += 1
        
        # Type inference
        if value.lower() == "true":
            flag_args[key] = True
        elif value.lower() == "false":
            flag_args[key] = False
        elif value.isdigit():
            flag_args[key] = int(value)
        else:
            try:
                flag_args[key] = float(value)
            except ValueError:
                flag_args[key] = value
    
    # Build args dict with positional values keyed by their names
    args = {}
    for idx, name in enumerate(positional_names):
        if idx < len(positional_args):
            args[name] = positional_args[idx]
        else:
            print(f"❌ Missing required positional argument: {name}", file=sys.stderr)
            sys.exit(1)
    
    # Add flag args
    args.update(flag_args)
    
    return command, positional_args, args


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 claw_wrapper_enhanced.py <command> [positional_args...] [--flag value]...", 
              file=sys.stderr)
        print("\nAvailable commands:", file=sys.stderr)
        for cmd, (pos_names, flags) in sorted(COMMAND_DEFS.items()):
            pos_str = " ".join(f"<{name}>" for name in pos_names)
            flag_str = " ".join(f"[--{flag.replace('_', '-')} VALUE]" for flag in sorted(flags))
            print(f"  {cmd} {pos_str} {flag_str}".strip(), file=sys.stderr)
        sys.exit(1)
    
    command, positional_args, args = parse_argv(sys.argv[1:])
    
    try:
        result = await claw_invoke(command, args)
        print(json.dumps(result, indent=2))
    except Exception as e:
        error_result = {
            "ok": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "command": command,
            "args": args,
            "positional_args": positional_args,
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())