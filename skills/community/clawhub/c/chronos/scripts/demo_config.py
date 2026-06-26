#!/usr/bin/env python3
"""Demo script showing configuration priority in Chronos."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import get_chat_id, get_config

print("=" * 60)
print("Chronos Configuration Demo")
print("=" * 60)

print("\n[1] Current effective chat_id:")
try:
    print(f"    {get_chat_id()}")
except ValueError as exc:
    print(f"    Not configured ({exc})")

print("\n[2] Testing environment variable override:")
os.environ['CHRONOS_CHAT_ID'] = "ENV_TEST_123"
print(f"    Set CHRONOS_CHAT_ID='ENV_TEST_123'")
print(f"    Result: {get_chat_id()}")
del os.environ['CHRONOS_CHAT_ID']

print("\n[3] Full configuration object:")
config = get_config()
print(f"    chat_id: {config['chat_id']}")
print(f"    Other keys: {[k for k in config.keys() if k != 'chat_id']}")

print("\n" + "=" * 60)
print("Configuration sources:")
print("  1. Environment: CHRONOS_CHAT_ID")
print("  2. Config file: ~/.config/chronos/config.json (field: chat_id)")
print("  3. If neither is set, Chronos raises a configuration error")
print("=" * 60)
