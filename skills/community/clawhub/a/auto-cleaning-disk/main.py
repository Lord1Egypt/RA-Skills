"""
Auto Disk Cleaner - Main Launcher
Automatically detects OS and runs the correct cleaner.
"""

import platform
import sys
import os

def main():
    print("=" * 45)
    print("   🧹 AUTO DISK CLEANER - By ClawHub Skill")
    print("=" * 45)

    os_type = platform.system()
    print(f"\n💻 Operating System detected: {os_type}\n")

    print("Cleaning Mode chunein:")
    print("  1. Auto Mode   — Sab kuch khud se clean ho jaye")
    print("  2. Confirm Mode — Har category pe poochhe pehle")
    mode = input("\nApna choice likhein (1 ya 2): ").strip()
    confirm = (mode == "2")

    if os_type == "Windows":
        from scripts.clean_windows import clean_windows
        clean_windows(confirm=confirm)
    elif os_type == "Linux":
        from scripts.clean_linux import clean_linux
        clean_linux(confirm=confirm)
    elif os_type == "Darwin":  # macOS
        from scripts.clean_mac import clean_mac
        clean_mac(confirm=confirm)
    else:
        print(f"⚠️  OS '{os_type}' support nahi hai abhi.")
        sys.exit(1)

if __name__ == "__main__":
    main()
