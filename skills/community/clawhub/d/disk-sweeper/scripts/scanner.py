"""disk-sweeper: Filesystem scanner.

Recursive directory scanner with streaming output, progress tracking,
auto-skip of no-permission directories, and depth limits.
"""
import os
import stat
from typing import List, Dict, Optional, Callable, Generator


# Permanently excluded system paths
PROTECTED_SYSTEM_PATHS = [
    "/System", "/bin", "/sbin", "/usr/bin", "/usr/sbin",
    "/etc", "/dev", "/proc", "/core", "/var/db",
    "/Library/SystemExtensions",
    "/System/Library",
]


def is_protected_path(path: str) -> bool:
    """Check if a path is in the system protection list."""
    real_path = os.path.realpath(os.path.abspath(os.path.expanduser(path)))
    for protected in PROTECTED_SYSTEM_PATHS:
        if real_path.startswith(protected):
            return True
    # Also check common dot-protected system paths
    if real_path.startswith("/"):
        parts = real_path.split(os.sep)
        for p in parts:
            if p in ("System", "bin", "sbin", "etc", "dev", "proc") and len(parts) > 3:
                return True
    return False


def should_skip_dir(dirpath: str) -> bool:
    """Determine if a directory should be skipped."""
    # Skip hidden directories unless scanning explicitly
    basename = os.path.basename(dirpath)
    if basename.startswith(".") and not basename in (".", ".."):
        return False  # Allow scanning hidden dirs in user home

    return False


def scan_directory(
    path: str,
    max_depth: int = 20,
    min_size_bytes: int = 0,
    exclude_paths: Optional[List[str]] = None,
    progress_callback: Optional[Callable] = None,
) -> Generator[Dict, None, None]:
    """Recursively scan a directory, yielding file info dicts.

    Yields dicts with keys: path, name, size, mtime, atime, is_dir, error
    """
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        yield {"error": f"Path does not exist: {path}", "path": path}
        return

    if os.path.isfile(path):
        yield _file_info(path)
        return

    if is_protected_path(path):
        yield {"error": f"Cannot scan protected system path: {path}", "path": path}
        return

    exclude_patterns = exclude_paths or []
    scanned_files = 0

    for root, dirs, files in os.walk(path, followlinks=False):
        depth = root.replace(path, "").count(os.sep)
        if depth > max_depth:
            dirs.clear()
            continue

        # Check if root is excluded
        if any(root.startswith(os.path.expanduser(p)) for p in exclude_patterns):
            dirs.clear()
            continue

        # Remove no-permission dirs
        dirs[:] = [d for d in dirs if os.access(os.path.join(root, d), os.R_OK | os.X_OK)]

        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                st = os.stat(filepath)
                if st.st_size < min_size_bytes:
                    continue
                yield _file_info(filepath, st)
                scanned_files += 1
                if progress_callback:
                    progress_callback(scanned_files, filepath)
            except (OSError, PermissionError):
                yield {"error": f"Permission denied: {filepath}", "path": filepath}


def _file_info(filepath: str, st: Optional[os.stat_result] = None) -> Dict:
    """Get file info dict."""
    if st is None:
        st = os.stat(filepath)
    return {
        "path": filepath,
        "name": os.path.basename(filepath),
        "size": st.st_size,
        "mtime": st.st_mtime,
        "atime": st.st_atime,
        "is_dir": stat.S_ISDIR(st.st_mode),
        "ext": os.path.splitext(filepath)[1].lower(),
    }


def scan_paths(
    paths: List[str],
    max_depth: int = 20,
    min_size_bytes: int = 0,
    exclude_paths: Optional[List[str]] = None,
) -> List[Dict]:
    """Scan multiple paths and return results as a list."""
    results = []
    for path in paths:
        for item in scan_directory(path, max_depth, min_size_bytes, exclude_paths):
            results.append(item)
    return results


if __name__ == "__main__":
    import json
    # Quick test - scan current user's home but only top-level
    count = 0
    for f in scan_directory("~", max_depth=1, min_size_bytes=1*1024*1024):  # 1MB min
        if "error" in f:
            print(f"  ⚠️  {f['error']}")
        else:
            print(f"  📄 {f['name']} ({f.get('size', 0) / 1024 / 1024:.1f} MB)")
            count += 1
            if count >= 5:
                print("  ... (showing first 5)")
                break
    print(f"Scan works! (scanned {count} files in top level)")
