#!/usr/bin/env python3
"""
scan_drives.py — Detect all physical drives and run smartctl diagnostics.

Usage:
    python3 scan_drives.py [--json] [--sudo]

Output:
    JSON array of {device, smartctl_output, error} objects to stdout.
"""

import json
import os
import re
import subprocess
import sys
import platform
import shutil
from pathlib import Path


def find_smartctl():
    """Return path to smartctl or None if not found."""
    candidates = [
        shutil.which("smartctl"),
        "/usr/local/sbin/smartctl",
        "/opt/homebrew/sbin/smartctl",
        "/usr/sbin/smartctl",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    return None


def detect_drives_macos():
    """Return list of disk device paths using diskutil list."""
    try:
        result = subprocess.run(
            ["diskutil", "list", "-plist"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            # Fallback: parse text output
            return detect_drives_macos_text()
        # Parse plist for AllDisks
        import plistlib
        plist = plistlib.loads(result.stdout.encode())
        all_disks = plist.get("AllDisks", [])
        # Only whole disks (no slice suffix like disk0s1)
        drives = []
        for d in all_disks:
            # Whole disk has no 's' partition suffix pattern
            if re.match(r'^disk\d+$', d):
                drives.append(f"/dev/{d}")
        return drives
    except Exception:
        return detect_drives_macos_text()


def detect_drives_macos_text():
    """Fallback: parse diskutil list text output."""
    try:
        result = subprocess.run(
            ["diskutil", "list"],
            capture_output=True, text=True, timeout=15
        )
        drives = []
        for line in result.stdout.splitlines():
            # Lines like: /dev/disk0 (internal, physical):
            m = re.match(r'^(/dev/disk\d+)\s', line)
            if m:
                drives.append(m.group(1))
        return drives
    except Exception:
        return []


def detect_drives_linux():
    """Return list of block device paths using lsblk."""
    try:
        result = subprocess.run(
            ["lsblk", "-dno", "NAME,TYPE"],
            capture_output=True, text=True, timeout=15
        )
        drives = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[1] in ("disk",):
                drives.append(f"/dev/{parts[0]}")
        return drives
    except Exception:
        # Ultra-fallback: scan /sys/block
        try:
            block_devs = os.listdir("/sys/block")
            drives = []
            for dev in sorted(block_devs):
                # Skip loop, ram, dm devices
                if re.match(r'^(loop|ram|dm|sr|fd)', dev):
                    continue
                drives.append(f"/dev/{dev}")
            return drives
        except Exception:
            return []


def run_smartctl(device, smartctl_path, use_sudo=False):
    """Run smartctl -a on a device. Returns (output_str, error_str)."""
    cmd = []
    if use_sudo:
        cmd.append("sudo")
    cmd += [smartctl_path, "-a", device]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=30
        )
        # smartctl exit codes: bit field. 0=OK, non-zero may still have output.
        # Bit 0: command-line parsing error
        # Bit 1: device open error
        # Bit 2: disk failing
        # Bits 3-7: various health/warning flags
        rc = result.returncode
        if rc & 0x01:
            # Command line error or device not openable
            return None, result.stderr.strip() or f"smartctl error (exit {rc})"
        return result.stdout, None
    except subprocess.TimeoutExpired:
        return None, "smartctl timed out"
    except FileNotFoundError:
        return None, f"smartctl not found at {smartctl_path}"
    except PermissionError:
        return None, "Permission denied — try running with sudo"
    except Exception as e:
        return None, str(e)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scan drives with SMART diagnostics")
    parser.add_argument("--json", action="store_true", help="Force JSON output (default)")
    parser.add_argument("--sudo", action="store_true", help="Prepend sudo to smartctl commands")
    args = parser.parse_args()

    os_type = platform.system()

    # Detect drives
    if os_type == "Darwin":
        drives = detect_drives_macos()
    elif os_type == "Linux":
        drives = detect_drives_linux()
    else:
        result = {
            "error": f"Unsupported OS: {os_type}",
            "os": os_type,
            "drives": []
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    # Check smartctl availability
    smartctl_path = find_smartctl()
    if not smartctl_path:
        install_hint = (
            "brew install smartmontools" if os_type == "Darwin"
            else "sudo apt install smartmontools  # or: sudo dnf install smartmontools"
        )
        result = {
            "error": "smartctl not found",
            "install": install_hint,
            "os": os_type,
            "drives": drives,
            "scan_results": []
        }
        print(json.dumps(result, indent=2))
        sys.exit(2)

    # Run smartctl on each drive
    scan_results = []
    for device in drives:
        entry = {"device": device}
        output, error = run_smartctl(device, smartctl_path, use_sudo=args.sudo)
        if error:
            entry["error"] = error
            # Detect permission issue and suggest sudo
            if "permission" in error.lower() or "Operation not permitted" in error:
                entry["hint"] = "Run with --sudo flag or as root"
        else:
            entry["smartctl_output"] = output
        scan_results.append(entry)

    output_doc = {
        "os": os_type,
        "smartctl_path": smartctl_path,
        "drives_found": len(drives),
        "scan_results": scan_results
    }
    print(json.dumps(output_doc, indent=2))


if __name__ == "__main__":
    main()
