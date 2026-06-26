#!/usr/bin/env python3
"""
Disk Space Analyzer - Scan disk usage and generate structured report data.
Outputs JSON to stdout for report generation.
Usage: python disk_scan.py [--top N] [--deep]
  --top N    : Number of top subdirectories to scan per drive (default: 10)
  --deep     : Scan two levels deep for top consumers
"""

import json
import os
import sys
import shutil
from datetime import datetime

def get_dir_size(path):
    """Calculate total size of a directory."""
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_dir_size(entry.path)
            except (OSError, PermissionError):
                pass
    except (OSError, PermissionError):
        pass
    return total

def scan_children(path, top_n=10):
    """Scan immediate children of a directory and return sorted list."""
    children = []
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    size = get_dir_size(entry.path)
                    if size > 0:
                        children.append({
                            "name": entry.name,
                            "path": entry.path,
                            "size_bytes": size,
                            "size_gb": round(size / (1024**3), 2)
                        })
            except (OSError, PermissionError):
                pass
    except (OSError, PermissionError):
        pass
    children.sort(key=lambda x: x["size_bytes"], reverse=True)
    return children[:top_n]

def trace_culprit(dir_info, used_gb, max_depth=5):
    """Recursively trace into the largest child to find the real culprit.

    Returns a dict with:
      - chain: list of directory names from root to leaf culprit
      - leaf: the deepest traced directory info
      - breadcrumb: list of {name, size_gb, size_bytes} at each level (for display)
    """
    chain = [dir_info["name"]]
    breadcrumb = [{
        "name": dir_info["name"],
        "path": dir_info["path"],
        "size_gb": dir_info["size_gb"],
        "children": []
    }]

    current = dir_info
    for depth in range(max_depth):
        children = scan_children(current["path"], top_n=10)
        if not children:
            break

        breadcrumb[-1]["children"] = children

        # Stop if the largest child is less than 40% of parent
        # (means the space is spread across many small dirs, no single culprit)
        # But don't stop if the child is still very large (>= 10 GB) — keep tracing
        largest_child = children[0]
        largest_ratio = largest_child["size_bytes"] / current["size_bytes"] if current["size_bytes"] > 0 else 0
        if largest_ratio < 0.4 and largest_child["size_gb"] < 10:
            break

        # Stop if the largest child's share of the whole drive is tiny (< 5%)
        # But keep going if the child is still >= 10 GB
        if largest_child["size_gb"] / used_gb < 0.05 and largest_child["size_gb"] < 10:
            break

        chain.append(largest_child["name"])
        current = largest_child
        breadcrumb.append({
            "name": current["name"],
            "path": current["path"],
            "size_gb": current["size_gb"],
            "children": []  # will be filled next iteration or left empty for leaf
        })

    return {
        "chain": chain,
        "leaf": current,
        "breadcrumb": breadcrumb
    }

def scan_drive(drive_letter, top_n=10, deep=False):
    """Scan a drive and return usage data."""
    path = f"{drive_letter}:\\"
    if not os.path.exists(path):
        return None

    # Get drive totals
    try:
        total, used, free = shutil.disk_usage(path)
    except OSError:
        return None

    # Scan top-level directories
    dir_sizes = []
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    size = get_dir_size(entry.path)
                    if size > 0:
                        dir_sizes.append({
                            "name": entry.name,
                            "path": entry.path,
                            "size_bytes": size,
                            "size_gb": round(size / (1024**3), 2)
                        })
            except (OSError, PermissionError):
                pass
    except (OSError, PermissionError):
        pass

    dir_sizes.sort(key=lambda x: x["size_bytes"], reverse=True)
    used_gb = round(used / (1024**3), 2)

    # Deep scan: trace culprits for top 3 directories
    deep_consumers = []
    if deep and dir_sizes:
        for top_dir in dir_sizes[:3]:
            print(f"  Deep tracing: {top_dir['name']} ({top_dir['size_gb']} GB)...", file=sys.stderr)
            # First get children of this directory for display
            level1_children = scan_children(top_dir["path"], top_n=10)

            # Then trace the biggest child recursively
            culprit_trace = None
            if level1_children:
                biggest_child = level1_children[0]
                culprit_trace = trace_culprit(biggest_child, used_gb, max_depth=5)
                # Prepend the top-level directory name to the chain
                culprit_trace["chain"].insert(0, top_dir["name"])

            deep_consumers.append({
                "name": top_dir["name"],
                "path": top_dir["path"],
                "size_gb": top_dir["size_gb"],
                "children": level1_children,
                "culprit_trace": culprit_trace  # recursive trace result
            })

    # Scan special locations
    special_locations = scan_special_locations(drive_letter)

    result = {
        "drive": drive_letter,
        "path": path,
        "total_gb": round(total / (1024**3), 2),
        "used_gb": used_gb,
        "free_gb": round(free / (1024**3), 2),
        "usage_percent": round(used / total * 100, 1) if total > 0 else 0,
        "top_directories": dir_sizes[:top_n],
        "special_locations": special_locations,
    }

    if deep and deep_consumers:
        result["deep_consumers"] = deep_consumers

    return result

def scan_special_locations(drive_letter):
    """Scan common cache/temp locations."""
    locations = []
    home = os.path.expanduser("~")
    
    targets = {
        "用户临时文件 (%TEMP%)": os.path.join(home, "AppData", "Local", "Temp"),
        "系统临时文件": os.path.join(f"{drive_letter}:\\", "Windows", "Temp"),
        "Windows更新缓存": os.path.join(f"{drive_letter}:\\", "Windows", "SoftwareDistribution", "Download"),
        "Edge浏览器缓存": os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"),
        "Chrome浏览器缓存": os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"),
        "npm缓存": os.path.join(home, "AppData", "Local", "npm-cache"),
        "pip缓存": os.path.join(home, "AppData", "Local", "pip", "cache"),
        "Docker数据": os.path.join(home, "AppData", "Local", "Docker"),
    }

    for name, path in targets.items():
        if os.path.exists(path):
            size = get_dir_size(path)
            if size > 1024 * 1024:  # Only show if > 1MB
                locations.append({
                    "name": name,
                    "path": path,
                    "size_bytes": size,
                    "size_gb": round(size / (1024**3), 2),
                    "size_mb": round(size / (1024**2), 1),
                })

    locations.sort(key=lambda x: x["size_bytes"], reverse=True)
    return locations

def scan_windows_components(drive_letter):
    """Scan Windows directory subfolders."""
    path = os.path.join(f"{drive_letter}:\\", "Windows")
    if not os.path.exists(path):
        return []

    components = []
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    size = get_dir_size(entry.path)
                    if size > 100 * 1024 * 1024:  # Only show if > 100MB
                        components.append({
                            "name": entry.name,
                            "path": entry.path,
                            "size_bytes": size,
                            "size_gb": round(size / (1024**3), 2)
                        })
            except (OSError, PermissionError):
                pass
    except (OSError, PermissionError):
        pass

    components.sort(key=lambda x: x["size_bytes"], reverse=True)
    return components[:15]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Disk Space Analyzer")
    parser.add_argument("--top", type=int, default=10, help="Top N directories per drive")
    parser.add_argument("--deep", action="store_true", help="Deep scan top consumer")
    parser.add_argument("--drive", type=str, default=None, help="Specific drive to scan (e.g., C)")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file path")
    args = parser.parse_args()

    # Detect available drives
    if args.drive:
        drives = [args.drive.upper()]
    else:
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if os.path.exists(f"{letter}:\\"):
                drives.append(letter)

    report = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": os.environ.get("COMPUTERNAME", os.environ.get("HOSTNAME", "unknown")),
        "drives": [],
        "windows_components": [],
        "special_locations": []
    }

    all_special = []

    for drive in drives:
        print(f"Scanning drive {drive}:...", file=sys.stderr)
        result = scan_drive(drive, args.top, args.deep)
        if result:
            report["drives"].append(result)
            all_special.extend(result.get("special_locations", []))

    # Deduplicate special locations by path
    seen = set()
    unique_special = []
    for loc in all_special:
        if loc["path"] not in seen:
            seen.add(loc["path"])
            unique_special.append(loc)
    unique_special.sort(key=lambda x: x["size_bytes"], reverse=True)
    report["special_locations"] = unique_special

    # Scan Windows components if C drive exists
    if "C" in drives:
        print("Scanning Windows components...", file=sys.stderr)
        report["windows_components"] = scan_windows_components("C")

    output = json.dumps(report, ensure_ascii=False, indent=2)

    # If --output specified, write to file; otherwise print to stdout
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
