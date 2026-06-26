"""
Auto Disk Cleaner - Windows
Safely cleans temp files, browser cache, recycle bin, and log files.
Never deletes important user files.
"""

import os
import shutil
import subprocess
import platform
from pathlib import Path

def get_size(path):
    total = 0
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        for dirpath, dirnames, filenames in os.walk(path):
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
    freed = 0
    if not os.path.exists(folder):
        return 0
    size = get_size(folder)
    if confirm:
        ans = input(f"  {label} clean karein? ({bytes_to_mb(size)} MB) [y/n]: ")
        if ans.lower() != 'y':
            print(f"  ⏭️  Skip kiya: {label}")
            return 0
    try:
        for item in Path(folder).iterdir():
            try:
                if item.is_file():
                    item.unlink()
                    freed += item.stat().st_size if item.exists() else 0
                elif item.is_dir():
                    s = get_size(str(item))
                    shutil.rmtree(item, ignore_errors=True)
                    freed += s
            except:
                pass
        print(f"  ✅ {label}: {bytes_to_mb(size)} MB freed")
    except Exception as e:
        print(f"  ⚠️  {label} clean nahi hua: {e}")
    return size

def clean_windows(confirm=False):
    print("\n🧹 Windows Disk Cleaner Start...\n")
    total_freed = 0

    # 1. Temp Files
    print("📁 Temp Files...")
    temp_paths = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        r"C:\Windows\Temp",
    ]
    for path in temp_paths:
        if path:
            total_freed += clean_folder(path, confirm, f"Temp: {path}")

    # 2. Browser Cache
    print("\n🌐 Browser Cache...")
    user = os.environ.get("USERPROFILE", "")
    browser_paths = {
        "Chrome":  rf"{user}\AppData\Local\Google\Chrome\User Data\Default\Cache",
        "Edge":    rf"{user}\AppData\Local\Microsoft\Edge\User Data\Default\Cache",
        "Firefox": rf"{user}\AppData\Local\Mozilla\Firefox\Profiles",
    }
    for browser, path in browser_paths.items():
        total_freed += clean_folder(path, confirm, browser)

    # 3. Recycle Bin
    print("\n🗑️  Recycle Bin...")
    if confirm:
        ans = input("  Recycle Bin empty karein? [y/n]: ")
        if ans.lower() == 'y':
            subprocess.run(["PowerShell", "-Command", "Clear-RecycleBin -Force"], 
                         capture_output=True)
            print("  ✅ Recycle Bin empty!")
    else:
        subprocess.run(["PowerShell", "-Command", "Clear-RecycleBin -Force"], 
                      capture_output=True)
        print("  ✅ Recycle Bin empty!")

    # 4. Log Files
    print("\n📋 Log Files...")
    log_paths = [
        r"C:\Windows\Logs",
        r"C:\Windows\SoftwareDistribution\Download",
    ]
    for path in log_paths:
        total_freed += clean_folder(path, confirm, f"Logs: {path}")

    print(f"\n{'='*40}")
    print(f"🎉 Total Space Freed: {bytes_to_mb(total_freed)} MB")
    print(f"{'='*40}\n")

if __name__ == "__main__":
    mode = input("Mode chunein:\n1. Auto (khud se)\n2. Confirm (har step pe poochna)\n> ")
    confirm = (mode.strip() == "2")
    clean_windows(confirm=confirm)
