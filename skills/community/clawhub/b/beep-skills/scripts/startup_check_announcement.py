#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beep - Small speaker Startup Check
Run after /RESET or /NEW to verify announcement is working
"""

import sys
from pathlib import Path

def check_announcement_setup():
    """Check if announcement system is ready"""
    issues = []

    # 1. Check edge-tts
    try:
        import edge_tts
    except ImportError:
        issues.append("edge-tts not installed (run: pip install edge-tts)")

    # 2. Check pygame
    try:
        import pygame
    except ImportError:
        issues.append("pygame not installed (run: pip install pygame) - recommended")

    # 3. Check config file
    config_file = Path.home() / ".config" / "audio-announcement" / "config.json"
    if not config_file.exists():
        issues.append("Config not found (run: beep config)")

    # 4. Check package
    try:
        import audio_announcement
    except ImportError:
        issues.append("audio_announcement not installed (run: pip install audio-announcement)")

    return issues

def main():
    print("[AUDIO] Beep startup check...")

    issues = check_announcement_setup()

    if not issues:
        print("[OK] All checks passed!")
        print("[SKIP] Skipping test announcement (startup check should not broadcast)")
        return 0
    else:
        print("[ERROR] Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n[SUGGEST] Suggestions:")
        print("   1. Install: pip install edge-tts pygame")
        print("   2. Test: beep test")
        print("   3. Config: beep config async_default=true")
        return 1

if __name__ == "__main__":
    sys.exit(main())
