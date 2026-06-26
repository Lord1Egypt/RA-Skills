#!/usr/bin/env python3
"""
Patch feishu-live-card watcher.py to add reply_in_thread=True to reply_card().

Usage:
    python3 patch-live-card.py [--check-only] [--watcher-path PATH]

Default watcher path: ~/.openclaw/skills/feishu-live-card/watcher.py
"""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_WATCHER = Path.home() / ".openclaw/skills/feishu-live-card/watcher.py"

# Pattern: reply_card method without reply_in_thread parameter
OLD_SIGNATURE = 'def reply_card(self, reply_to_message_id: str, card: Dict) -> Optional[str]:'
NEW_SIGNATURE = 'def reply_card(self, reply_to_message_id: str, card: Dict, reply_in_thread: bool = True) -> Optional[str]:'

OLD_BODY_MARKER = '"content": json.dumps(card),'
NEW_BODY_LINES = '''"content": json.dumps(card),
            "reply_in_thread": reply_in_thread,'''


def check_patch(content: str) -> bool:
    """Return True if patch is already applied."""
    return 'reply_in_thread' in content and NEW_SIGNATURE.split('(')[1] in content


def apply_patch(content: str) -> str:
    """Apply the patch to watcher.py content."""
    # Patch signature
    content = content.replace(OLD_SIGNATURE, NEW_SIGNATURE)
    # Patch body - add reply_in_thread to the request body
    # Only add if not already present
    if '"reply_in_thread": reply_in_thread' not in content:
        content = content.replace(
            OLD_BODY_MARKER,
            NEW_BODY_LINES,
        )
    return content


def main():
    parser = argparse.ArgumentParser(description="Patch feishu-live-card for thread replies")
    parser.add_argument("--check-only", action="store_true", help="Only check if patch is applied")
    parser.add_argument("--watcher-path", type=Path, default=DEFAULT_WATCHER, help="Path to watcher.py")
    args = parser.parse_args()

    watcher = args.watcher_path
    if not watcher.exists():
        print(f"❌ watcher.py not found at: {watcher}")
        sys.exit(2)

    content = watcher.read_text()

    if check_patch(content):
        print(f"✅ Patch already applied: {watcher}")
        sys.exit(0)

    if args.check_only:
        print(f"❌ Patch NOT applied: {watcher}")
        sys.exit(1)

    patched = apply_patch(content)
    if patched == content:
        print(f"⚠️  Could not apply patch (source may have changed): {watcher}")
        sys.exit(1)

    watcher.write_text(patched)
    print(f"✅ Patched: {watcher}")
    print("   Restart watcher to apply: cd ~/.openclaw/skills/feishu-live-card && python3 watcher.py stop && python3 watcher.py start")


if __name__ == "__main__":
    main()
