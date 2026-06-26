#!/usr/bin/env bash
# List all Claude Code remote control sessions.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/registry.py" list
