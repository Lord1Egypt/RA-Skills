#!/usr/bin/env python3
"""Read-only storage scanner (macOS + Windows + Linux).

Collects disk usage, system info, and per-directory size breakdowns for the
hot spots that typically eat disk, and emits one JSON blob to stdout for Claude
to interpret and classify. Auto-detects the OS and scans the right locations.
Optimized with multi-threading (ThreadPoolExecutor) for faster scanning.

STRICTLY READ-ONLY: only sizes/lists/reads metadata. Never creates, moves, or
deletes anything.

Output shape (same on all OSes):
{
  "generated_at", "scan_seconds",
  "system": {os, build, arch, user, home, filesystem,
             disk_total, disk_used, disk_free, purgeable,
             disks: [{name, total, used, free}]},   # all volumes/drives
  "groups": { "<group>": [{name, path, size_kb, size_h}], ... }
}
"""
import concurrent.futures
import json
import os
import shutil
import sys
import time

HOME = os.path.expanduser("~")


def human(kb):
    """KB number -> human string like '12.3 GB'."""
    n = float(kb) * 1024
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit not in ("B", "KB") else f"{int(n)} {unit}"
        n /= 1024


# ======================================================================
# Unix helper (macOS + Linux)
# ======================================================================
import re
import subprocess


def run(cmd, timeout=180):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""


def du_children(path, min_kb=51200, limit=40, exclude_names=None):
    """Size immediate children of `path` via du in parallel. macOS + Linux."""
    if not os.path.isdir(path):
        return []
    if exclude_names is None:
        exclude_names = set()
    results = []
    try:
        entries = os.listdir(path)
    except PermissionError:
        return [{"name": "(permission denied)", "path": path,
                 "size_kb": 0, "size_h": "?", "denied": True}]
    
    valid_entries = []
    for name in entries:
        if name in (".", "..") or name in exclude_names:
            continue
        if name.startswith(".") and name != ".Trash":
            continue
        child = os.path.join(path, name)
        if os.path.islink(child):
            continue
        if os.path.isdir(child):
            valid_entries.append((name, child))
            
    def process_child(item):
        name, child_path = item
        out = run(["du", "-sk", child_path], timeout=90)
        m = re.match(r"\s*(\d+)", out)
        if not m:
            return None
        kb = int(m.group(1))
        if kb < min_kb:
            return None
        return {"name": name, "path": child_path, "size_kb": kb, "size_h": human(kb)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_child, entry): entry for entry in valid_entries}
        for future in concurrent.futures.as_completed(futures):
            try:
                res = future.result()
                if res:
                    results.append(res)
            except Exception:
                pass
                
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results[:limit]


# ======================================================================
# macOS
# ======================================================================
MAC_TARGETS = [
    ("home", HOME, 102400),
    ("library", os.path.join(HOME, "Library"), 51200),
    ("caches", os.path.join(HOME, "Library/Caches"), 51200),
    ("containers", os.path.join(HOME, "Library/Containers"), 51200),
    ("group_containers", os.path.join(HOME, "Library/Group Containers"), 51200),
    ("app_support", os.path.join(HOME, "Library/Application Support"), 51200),
    ("applications", "/Applications", 102400),
    ("downloads", os.path.join(HOME, "Downloads"), 51200),
    ("dev_caches", None, 51200),
]

MAC_DEV_CACHE_PATHS = [
    "~/Library/Caches/pip", "~/Library/Caches/uv", "~/.cache", "~/.cargo",
    "~/.npm", "~/.pnpm-store", "~/.gradle", "~/.m2",
    "~/Library/Developer/Xcode/DerivedData", "~/Library/Developer/CoreSimulator",
    "~/Library/Developer/Xcode/iOS DeviceSupport", "~/Library/pnpm",
    "~/go/pkg", "~/.docker", "~/.bun", "~/Library/Caches/ms-playwright",
    "~/Library/Caches/Yarn", "~/.cocoapods",
    "~/Library/Containers/com.docker.docker",
]


def dev_caches_macos():
    results = []
    def process_path(p):
        path = os.path.expanduser(p)
        if not os.path.isdir(path):
            return None
        out = run(["du", "-sk", path], timeout=180)
        m = re.match(r"\s*(\d+)", out)
        if not m:
            return None
        kb = int(m.group(1))
        if kb < 51200:
            return None
        return {"name": os.path.basename(path.rstrip("/")) or path,
                "path": path, "size_kb": kb, "size_h": human(kb)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_path, p): p for p in MAC_DEV_CACHE_PATHS}
        for future in concurrent.futures.as_completed(futures):
            try:
                res = future.result()
                if res:
                    results.append(res)
            except Exception:
                pass
                
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results


def system_info_macos():
    info = {}
    info["os"] = "macOS " + run(["sw_vers", "-productVersion"]).strip()
    info["build"] = run(["sw_vers", "-buildVersion"]).strip()
    arch = run(["uname", "-m"]).strip()
    brand = run(["sysctl", "-n", "machdep.cpu.brand_string"]).strip()
    info["arch"] = (f"Apple Silicon (arm64){' / ' + brand if brand else ''}"
                    if arch == "arm64" else f"{arch}{' / ' + brand if brand else ''}")
    info["user"] = os.environ.get("USER", "") or run(["whoami"]).strip()
    info["home"] = HOME
    total, used, free = "?", "?", "?"
    try:
        t, u, f = shutil.disk_usage("/")
        total, used, free = human(t // 1024), human(u // 1024), human(f // 1024)
    except Exception:
        pass
    info["disk_total"], info["disk_used"], info["disk_free"] = total, used, free
    dinfo = run(["diskutil", "info", "/"])
    fs = re.search(r"File System Personality:\s*(.+)", dinfo)
    info["filesystem"] = fs.group(1).strip() if fs else "APFS"
    pm = re.search(r"Purgeable Space:\s*([\d.,]+ \w+)", dinfo)
    info["purgeable"] = pm.group(1).strip() if pm else ""
    info["disk_name"] = "Macintosh HD"
    info["disks"] = [{"name": "Macintosh HD", "total": total, "used": used, "free": free}]
    return info


def scan_macos():
    system = system_info_macos()
    groups = {}
    
    def scan_one_target(target):
        key, path, floor = target
        if key == "dev_caches":
            res = dev_caches_macos()
        elif key == "home":
            res = du_children(path, min_kb=floor, exclude_names={"Library"})
        elif key == "library":
            res = du_children(path, min_kb=floor, exclude_names={"Caches", "Containers", "Group Containers", "Application Support"})
        else:
            res = du_children(path, min_kb=floor)
        return key, res

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scan_one_target, t): t for t in MAC_TARGETS}
        for future in concurrent.futures.as_completed(futures):
            try:
                key, res = future.result()
                groups[key] = res
            except Exception:
                pass
                
    return system, groups


# ======================================================================
# Linux
# ======================================================================
LINUX_TARGETS = [
    ("home", HOME, 102400),
    ("caches", os.path.join(HOME, ".cache"), 51200),
    ("downloads", os.path.join(HOME, "Downloads"), 51200),
    ("applications", "/usr/share/applications", 51200),
    ("dev_caches", None, 51200),
]

LINUX_DEV_CACHE_PATHS = [
    "~/.cache/pip", "~/.cache/uv", "~/.npm", "~/.cargo",
    "~/.gradle", "~/.m2", "~/.cache/yarn", "~/.pnpm-store",
    "~/.cache/ms-playwright", "~/go/pkg", "~/.docker", "~/.bun",
]


def dev_caches_linux():
    results = []
    def process_path(p):
        path = os.path.expanduser(p)
        if not os.path.isdir(path):
            return None
        out = run(["du", "-sk", path], timeout=180)
        m = re.match(r"\s*(\d+)", out)
        if not m:
            return None
        kb = int(m.group(1))
        if kb < 51200:
            return None
        return {"name": os.path.basename(path.rstrip("/")) or path,
                "path": path, "size_kb": kb, "size_h": human(kb)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_path, p): p for p in LINUX_DEV_CACHE_PATHS}
        for future in concurrent.futures.as_completed(futures):
            try:
                res = future.result()
                if res:
                    results.append(res)
            except Exception:
                pass
                
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results


def system_info_linux():
    info = {}
    info["os"] = "Linux " + run(["uname", "-r"]).strip()
    info["build"] = run(["uname", "-v"]).strip()
    info["arch"] = run(["uname", "-m"]).strip()
    info["user"] = os.environ.get("USER", "") or run(["whoami"]).strip()
    info["home"] = HOME
    total, used, free = "?", "?", "?"
    try:
        t, u, f = shutil.disk_usage("/")
        total, used, free = human(t // 1024), human(u // 1024), human(f // 1024)
    except Exception:
        pass
    info["disk_total"], info["disk_used"], info["disk_free"] = total, used, free
    info["filesystem"] = "ext4"
    out_df = run(["df", "-T", "/"])
    lines = out_df.splitlines()
    if len(lines) > 1:
        parts = lines[1].split()
        if len(parts) > 1:
            info["filesystem"] = parts[1]
            
    info["purgeable"] = ""
    info["disk_name"] = "Root FS"
    info["disks"] = [{"name": "/", "total": total, "used": used, "free": free}]
    return info


def scan_linux():
    system = system_info_linux()
    groups = {}
    
    def scan_one_target(target):
        key, path, floor = target
        if key == "dev_caches":
            res = dev_caches_linux()
        elif key == "home":
            res = du_children(path, min_kb=floor, exclude_names={".cache", "Library"})
        elif key == "caches":
            res = du_children(path, min_kb=floor, exclude_names={"pip", "uv", "ms-playwright", "yarn"})
        else:
            res = du_children(path, min_kb=floor)
        return key, res

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scan_one_target, t): t for t in LINUX_TARGETS}
        for future in concurrent.futures.as_completed(futures):
            try:
                key, res = future.result()
                groups[key] = res
            except Exception:
                pass
                
    return system, groups


# ======================================================================
# Windows
# ======================================================================
def dir_size_bytes(path):
    """Recursive size in bytes via os.scandir. Skips symlinks and unreadable."""
    total = 0
    try:
        with os.scandir(path) as it:
            for e in it:
                try:
                    if e.is_symlink():
                        continue
                    if e.is_file(follow_symlinks=False):
                        total += e.stat(follow_symlinks=False).st_size
                    elif e.is_dir(follow_symlinks=False):
                        total += dir_size_bytes(e.path)
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        pass
    return total


def scandir_children(path, min_kb=51200, limit=40):
    """Size every immediate child of `path` via os.scandir in parallel. Windows."""
    if not path or not os.path.isdir(path):
        return []
    results = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [{"name": "(permission denied)", "path": path,
                 "size_kb": 0, "size_h": "?", "denied": True}]
                 
    def process_child(name):
        child = os.path.join(path, name)
        if os.path.islink(child):
            return None
        try:
            kb = (os.path.getsize(child) if os.path.isfile(child)
                  else dir_size_bytes(child)) // 1024
        except (PermissionError, OSError):
            return None
        if kb < min_kb:
            return None
        return {"name": name, "path": child, "size_kb": kb, "size_h": human(kb)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_child, name): name for name in entries}
        for future in concurrent.futures.as_completed(futures):
            try:
                res = future.result()
                if res:
                    results.append(res)
            except Exception:
                pass
                
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results[:limit]


def list_drives_windows():
    drives = []
    import string
    for letter in string.ascii_uppercase:
        root = f"{letter}:\\"
        if os.path.exists(root):
            try:
                t, u, f = shutil.disk_usage(root)
                drives.append({"name": root, "total": human(t // 1024),
                               "used": human(u // 1024), "free": human(f // 1024)})
            except Exception:
                continue
    return drives


def system_info_windows():
    import platform
    info = {}
    info["os"] = platform.system() + " " + platform.release()
    info["build"] = platform.version()
    info["arch"] = os.environ.get("PROCESSOR_ARCHITECTURE", platform.machine())
    info["user"] = os.environ.get("USERNAME", "")
    info["home"] = os.environ.get("USERPROFILE", HOME)
    sysdrive = os.environ.get("SystemDrive", "C:") + "\\"
    total, used, free = "?", "?", "?"
    try:
        t, u, f = shutil.disk_usage(sysdrive)
        total, used, free = human(t // 1024), human(u // 1024), human(f // 1024)
    except Exception:
        pass
    info["disk_total"], info["disk_used"], info["disk_free"] = total, used, free
    info["filesystem"] = "NTFS"
    info["purgeable"] = ""
    info["disk_name"] = sysdrive
    info["disks"] = list_drives_windows()
    return info


def scan_windows():
    profile = os.environ.get("USERPROFILE", HOME)
    local = os.environ.get("LOCALAPPDATA", os.path.join(profile, "AppData", "Local"))
    roaming = os.environ.get("APPDATA", os.path.join(profile, "AppData", "Roaming"))
    targets = [
        ("user_profile", profile, 102400),
        ("appdata_local", local, 51200),
        ("appdata_roaming", roaming, 51200),
        ("temp", os.environ.get("TEMP", os.path.join(local, "Temp")), 51200),
        ("downloads", os.path.join(profile, "Downloads"), 51200),
        ("program_files", os.environ.get("ProgramFiles", r"C:\Program Files"), 102400),
        ("program_files_x86", os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), 102400),
    ]
    groups = {}
    
    def scan_one_target(target):
        key, path, floor = target
        return key, scandir_children(path, min_kb=floor)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scan_one_target, t): t for t in targets}
        for future in concurrent.futures.as_completed(futures):
            try:
                key, res = future.result()
                groups[key] = res
            except Exception:
                pass

    dev_paths = [
        os.path.join(profile, ".cache"), os.path.join(profile, ".npm"),
        os.path.join(profile, ".gradle"), os.path.join(profile, ".m2"),
        os.path.join(profile, ".nuget", "packages"), os.path.join(profile, ".cargo"),
        os.path.join(local, "pip", "Cache"), os.path.join(local, "Yarn"),
        os.path.join(local, "uv"), os.path.join(local, "ms-playwright"),
        os.path.join(local, "go-build"), os.path.join(profile, ".bun"),
    ]
    
    docker_wsl = os.path.join(local, "Docker", "wsl")
    if os.path.isdir(docker_wsl):
        dev_paths.append(docker_wsl)
        
    packages_dir = os.path.join(local, "Packages")
    if os.path.isdir(packages_dir):
        try:
            for dist in os.listdir(packages_dir):
                vhdx_path = os.path.join(packages_dir, dist, "LocalState", "ext4.vhdx")
                if os.path.isfile(vhdx_path):
                    dev_paths.append(vhdx_path)
        except Exception:
            pass

    dev = []
    def scan_dev_path(path):
        if not os.path.exists(path):
            return None
        try:
            kb = (os.path.getsize(path) if os.path.isfile(path)
                  else dir_size_bytes(path)) // 1024
        except (PermissionError, OSError):
            return None
        if kb < 51200:
            return None
        return {"name": os.path.basename(path.rstrip("\\/")) or path,
                "path": path, "size_kb": kb, "size_h": human(kb)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(scan_dev_path, p): p for p in dev_paths}
        for future in concurrent.futures.as_completed(futures):
            try:
                res = future.result()
                if res:
                    dev.append(res)
            except Exception:
                pass
                
    dev.sort(key=lambda r: r["size_kb"], reverse=True)
    groups["dev_caches"] = dev
    return system_info_windows(), groups


# ======================================================================
def main():
    started = time.time()
    if sys.platform == "darwin":
        system, groups = scan_macos()
    elif sys.platform.startswith("linux"):
        system, groups = scan_linux()
    elif sys.platform.startswith("win"):
        system, groups = scan_windows()
    else:
        print(json.dumps({"error": "unsupported_platform", "platform": sys.platform,
                          "message": "scan.py supports macOS, Linux, and Windows only."},
                         ensure_ascii=False))
        return
    data = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": system,
        "groups": groups,
        "scan_seconds": round(time.time() - started, 1),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
