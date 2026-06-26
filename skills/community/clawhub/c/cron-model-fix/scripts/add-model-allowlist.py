#!/usr/bin/env python3
"""
Add model to OpenClaw agent allowlist.

Usage:
    python3 add-model-allowlist.py --model ollama/qwen3.5:0.8b
    python3 add-model-allowlist.py --model ollama/qwen3.5:0.8b --backup
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"

def main():
    parser = argparse.ArgumentParser(description='Add model to agent allowlist')
    parser.add_argument('--model', required=True, help='Model to add (e.g., ollama/qwen3.5:0.8b)')
    parser.add_argument('--backup', action='store_true', help='Create backup before modifying')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying')
    args = parser.parse_args()

    # Load config
    if not CONFIG_PATH.exists():
        print(f"❌ Config not found: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    # Check current allowlist
    models = config.setdefault('agents', {}).setdefault('defaults', {}).setdefault('models', {})
    
    if args.model in models:
        print(f"✅ Model '{args.model}' already in allowlist")
        return

    # Create backup
    if args.backup or not args.dry_run:
        backup_path = CONFIG_PATH.with_suffix(f'.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        with open(CONFIG_PATH, 'r') as f:
            with open(backup_path, 'w') as bf:
                bf.write(f.read())
        print(f"📦 Backup created: {backup_path}")

    # Add model
    if args.dry_run:
        print(f"🔍 DRY RUN: Would add '{args.model}' to agents.defaults.models")
        print(f"   Location: {CONFIG_PATH}")
    else:
        models[args.model] = {}
        
        # Write updated config
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Added '{args.model}' to agents.defaults.models")
        print(f"   Config updated: {CONFIG_PATH}")
        print(f"\n⚠️  Restart gateway to apply changes:")
        print(f"   openclaw gateway restart")

if __name__ == '__main__':
    main()
