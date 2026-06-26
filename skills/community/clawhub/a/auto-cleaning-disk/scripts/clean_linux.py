"""
Auto Disk Cleaner - Linux
Safely cleans temp files, browser cache, trash, and log files.
"""

import os
import shutil
from pathlib import Path

def get_size(path):
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except:
                    pass
    except:
        pass
    return total

def bytes_to_mb(b):
    return round(b / (1024 * 1024), 2)

def clean_folder(folder, confirm=False, label=""):
    if not os.path.exists(folder):
        return 0
    size = get_size(folder)
    if size == 0:
        return 0
    if confirm:
        ans = input(f"  {label} clean karein? ({bytes_to_mb(size)} MB) [y/n]: ")
        if ans.lower() != 'y':
            print(f"  ⏭️  Skip: {label}")
            return 0
    try:
        for item in Path(folder).iterdir():
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
            except:
                pass
        print(f"  ✅ {label}: {bytes_to_mb(size)} MB freed")
    except Exception as e:
        print(f"  ⚠️  {label}: {e}")
    return size

def clean_linux(confirm=False):
    print("\n🧹 Linux Disk Cleaner Start...\n")
    total_freed = 0
    home = str(Path.home())

    # 1. Temp Files
    print("📁 Temp Files...")
    total_freed += clean_folder("/tmp", confirm, "/tmp")
    total_freed += clean_folder("/var/tmp", confirm, "/var/tmp")

    # 2. Browser Cache
    print("\n🌐 Browser Cache...")
    browser_paths = {
        "Chrome":  f"{home}/.cache/google-chrome",
        "Chromium":f"{home}/.cache/chromium",
        "Firefox": f"{home}/.cache/mozilla/firefox",
    }
    for browser, path in browser_paths.items():
        total_freed += clean_folder(path, confirm, browser)

    # 3. Trash
    print("\n🗑️  Trash...")
    trash_paths = [
        f"{home}/.local/share/Trash/files",
        f"{home}/.local/share/Trash/info",
    ]
    for path in trash_paths:
        total_freed += clean_folder(path, confirm, f"Trash: {path}")

    # 4. Log Files
    print("\n📋 Log Files...")
    total_freed += clean_folder(f"{home}/.cache", confirm, "User Cache")

    print(f"\n{'='*40}")
    print(f"🎉 Total Space Freed: {bytes_to_mb(total_freed)} MB")
    print(f"{'='*40}\n")

if __name__ == "__main__":
    mode = input("Mode chunein:\n1. Auto (khud se)\n2. Confirm (har step pe poochna)\n> ")
    confirm = (mode.strip() == "2")
    clean_linux(confirm=confirm)
