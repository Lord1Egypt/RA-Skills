#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Memory System - Session Start Script

Usage:
    python3 session_start.py --user_id ou_xxx [--json]
"""

import os
import sys
import json
import argparse

# Add path
workspace_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, 'skills', 'memory'))

from openclaw_integration import OpenClawMemoryIntegration


def main():
    parser = argparse.ArgumentParser(description='OpenClaw Memory System Session Start')
    parser.add_argument('--user_id', required=True, help='User ID')
    parser.add_argument('--base_prompt', default='', help='Base system prompt')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Initialize memory system
    try:
        mem = OpenClawMemoryIntegration(user_id=args.user_id)
    except Exception as e:
        print(f"❌ Initialization failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate system prompt
    full_prompt = mem.get_session_system_prompt(args.base_prompt)
    
    # Get user profile
    profile = mem.get_user_profile()
    
    # Output
    if args.json:
        output = {
            "system_prompt": full_prompt,
            "user_profile": profile,
            "memory_stats": mem.memory.get_stats()
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(full_prompt)
    
    # Save to file (optional)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(full_prompt)
        print(f"\n✅ System prompt saved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
