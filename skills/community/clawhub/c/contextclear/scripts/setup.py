#!/usr/bin/env python3
"""
ContextClear Auto-Setup
Patches AGENTS.md and HEARTBEAT.md with context recovery instructions.

Usage:
  python3 setup.py --agent-id <id> --api-key <key> --workspace <path>
  python3 setup.py --agent-id <id> --api-key <key>  # defaults to ~/.openclaw/workspace

This is idempotent — safe to run multiple times.
"""

import argparse
import os
import sys

API_URL = "https://api.contextclear.com/api"

AGENTS_BLOCK = """
## Context Recovery (ContextClear)
On every session start (especially after compaction), recover your memory:
```bash
curl -s {api_url}/agents/{agent_id}/recover \\
  -H "X-API-Key: {api_key}"
```
This returns your last session context, open threads, repos, tools, and context gaps.
Use it to orient yourself before asking your human things you should already know.
"""

HEARTBEAT_BLOCK = """
## ContextClear — Context Recovery (after compaction or fresh session)
If you don't remember recent work, recover your context:
```bash
curl -s {api_url}/agents/{agent_id}/recover \\
  -H "X-API-Key: {api_key}"
```

## ContextClear — Context Snapshot (after real work, not idle heartbeats)
After meaningful work, save what you worked on:
```bash
curl -s -X POST {api_url}/agents/{agent_id}/context \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: {api_key}" \\
  -d '{{"sessionId":"YYYY-MM-DD-summary","summary":"...","repos":[...],"files":[...],"tools":[...],"decisions":[...],"openThreads":[...],"tags":[...]}}'
```
Keep it concise. Only report after real work, not idle heartbeats.
"""

MARKER = "## Context Recovery (ContextClear)"
HB_MARKER = "## ContextClear — Context Recovery"


def patch_file(filepath, block, marker):
    """Append block to file if marker not already present."""
    if not os.path.exists(filepath):
        print(f"  ⚠️  {filepath} not found — skipping")
        return False

    content = open(filepath, 'r').read()
    if marker in content:
        print(f"  ✅ {filepath} already patched")
        return False

    with open(filepath, 'a') as f:
        f.write(block)

    print(f"  ✅ {filepath} patched")
    return True


def main():
    parser = argparse.ArgumentParser(description="Auto-setup ContextClear context recovery")
    parser.add_argument("--agent-id", required=True, help="ContextClear agent ID")
    parser.add_argument("--api-key", required=True, help="ContextClear API key")
    parser.add_argument("--api-url", default=API_URL, help="ContextClear API URL")
    parser.add_argument("--workspace", default=os.path.expanduser("~/.openclaw/workspace"),
                        help="Workspace path (default: ~/.openclaw/workspace)")
    args = parser.parse_args()

    agents_block = AGENTS_BLOCK.format(
        api_url=args.api_url, agent_id=args.agent_id, api_key=args.api_key)
    heartbeat_block = HEARTBEAT_BLOCK.format(
        api_url=args.api_url, agent_id=args.agent_id, api_key=args.api_key)

    agents_path = os.path.join(args.workspace, "AGENTS.md")
    heartbeat_path = os.path.join(args.workspace, "HEARTBEAT.md")

    print(f"🔧 ContextClear Setup — Agent: {args.agent_id}")
    print(f"   Workspace: {args.workspace}")
    print()

    patched = False
    patched |= patch_file(agents_path, agents_block, MARKER)
    patched |= patch_file(heartbeat_path, heartbeat_block, HB_MARKER)

    if patched:
        print("\n✅ Done! Your agent will now auto-recover context after compaction.")
        print("   Context snapshots will be saved on heartbeats after real work.")
    else:
        print("\n✅ Already set up — no changes needed.")


if __name__ == "__main__":
    main()
