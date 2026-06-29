"""disk-sweeper: Safety grading engine.

Assigns safety levels to files/directories based on their location
and content type. Maintains the system protection list.
"""
import os
from typing import Dict, List, Optional, Tuple


# Safety levels
SAFE = "SAFE"
CLEANABLE = "CLEANABLE"
CAUTION = "CAUTION"
PROTECTED = "PROTECTED"

# Hardcoded protected system paths - user CANNOT override these
SYSTEM_PROTECTED_PATHS = [
    "/System",
    "/bin",
    "/sbin",
    "/usr/bin",
    "/usr/sbin",
    "/etc",
    "/dev",
    "/proc",
    "/core",
    "/var/db",
    "/private",
    "/usr/lib",
    "/usr/share",
    "/Library/SystemExtensions",
    "/System/Library",
]

# Paths that are SAFE to clean
SAFE_PATTERNS = [
    "Downloads",
    ".Trash",
    "tmp",
    ".npm/_cacache",
    ".yarn/cache",
    "npm-cache",
]

# Paths that are CAUTION to clean
CAUTION_PATTERNS = [
    "Library/Containers/com.tencent",
    "Library/Containers/com.dingtalk",
    "Library/Containers/com.kingsoft",
    "Library/Application Support/com.tencent",
    "Library/Application Support/com.dingtalk",
]


def grade_path(path: str) -> Tuple[str, str]:
    """Determine safety level for a given path.

    Returns (safety_level, reason).
    """
    real_path = os.path.realpath(os.path.abspath(os.path.expanduser(path)))

    # PROTECTED check
    for protected in SYSTEM_PROTECTED_PATHS:
        if real_path.startswith(protected):
            return (PROTECTED, f"System-critical path: {protected}")

    # CAUTION check
    for pattern in CAUTION_PATTERNS:
        if pattern.lower() in real_path.lower():
            return (CAUTION, f"Application data (may contain user content): {os.path.basename(path)}")

    # SAFE check
    for pattern in SAFE_PATTERNS:
        if pattern.lower() in real_path.lower():
            return (SAFE, f"Temporary/reconstructable directory")

    # Default for user home
    if real_path.startswith(os.path.expanduser("~")):
        return (CLEANABLE, "User data directory")

    return (CAUTION, f"Path outside home or unknown")


def grade_file(file_info: Dict) -> Dict:
    """Grade a single file with safety level."""
    path = file_info.get("path", "")
    level, reason = grade_path(path)
    return {**file_info, "safety": level, "safety_reason": reason}


def grade_files(files: List[Dict]) -> List[Dict]:
    """Grade a list of files."""
    return [grade_file(f) for f in files]


def verify_path_is_safe_to_clean(path: str) -> bool:
    """Double-check that a path is safe to clean before deletion."""
    level, _ = grade_path(path)
    if level == PROTECTED:
        return False
    if not os.path.exists(path):
        return False
    return True


def get_safe_cleanup_candidates(files: List[Dict], min_safety: str = SAFE) -> List[Dict]:
    """Get files that are safe to clean based on minimum safety level."""
    safety_order = {SAFE: 0, CLEANABLE: 1, CAUTION: 2, PROTECTED: 3}
    min_level = safety_order.get(min_safety, 0)
    return [
        f for f in grade_files(files)
        if safety_order.get(f.get("safety", PROTECTED), 3) <= min_level
    ]


if __name__ == "__main__":
    test_paths = [
        "/System/Library/CoreServices",
        "/bin/sh",
        "/Users/test/Downloads/bigfile.zip",
        "/Users/test/Library/Caches/com.example/cache.db",
        "/Users/test/Library/Containers/com.tencent.xinWeChat/Data/Caches",
        "/Users/test/Documents/work/report.pdf",
    ]
    for p in test_paths:
        level, reason = grade_path(p)
        icon = {"SAFE": "🟢", "CLEANABLE": "🟡", "CAUTION": "🟠", "PROTECTED": "🔴"}
        print(f"  {icon.get(level, '⚪')} [{level}] {p}")
        print(f"       {reason}")
