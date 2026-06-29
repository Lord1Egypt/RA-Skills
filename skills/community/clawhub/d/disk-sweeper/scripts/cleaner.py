"""disk-sweeper: Cleanup executor.

Handles file deletion with safety checks, trash support, and undo.
Supports preview, interactive, auto-safe, and custom cleanup modes.
"""
import os
import shutil
import subprocess
from typing import List, Dict, Optional, Callable


def move_to_trash(path: str) -> bool:
    """Move a file or directory to the system trash.

    Uses `trash` CLI if available, otherwise Python fallback.
    Returns True on success.
    """
    try:
        # Try macOS `trash` command first
        subprocess.run(["trash", path], check=True, capture_output=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        # Fallback: move to ~/.Trash
        trash_dir = os.path.expanduser("~/.Trash")
        os.makedirs(trash_dir, exist_ok=True)
        basename = os.path.basename(path)
        dest = os.path.join(trash_dir, basename)

        # Handle name conflicts
        counter = 1
        while os.path.exists(dest):
            name, ext = os.path.splitext(basename)
            dest = os.path.join(trash_dir, f"{name}_{counter}{ext}")
            counter += 1

        shutil.move(path, dest)
        return True
    except (OSError, shutil.Error):
        return False


def permanently_delete(path: str) -> bool:
    """Permanently delete a file or directory."""
    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except (OSError, PermissionError):
        return False


class CleanupResult:
    """Track cleanup results."""
    def __init__(self):
        self.files_removed = 0
        self.space_freed = 0
        self.errors = []
        self.trash_paths = []

    def add_success(self, path: str, size: int, trashed: bool):
        self.files_removed += 1
        self.space_freed += size
        if trashed:
            self.trash_paths.append(path)

    def add_error(self, path: str, error_msg: str):
        self.errors.append(f"{path}: {error_msg}")

    def to_dict(self) -> Dict:
        return {
            "files_removed": self.files_removed,
            "space_freed_human": _human_size(self.space_freed),
            "space_freed": self.space_freed,
            "errors": self.errors,
            "trash_paths": self.trash_paths,
        }


def preview_cleanup(items: List[Dict]) -> Dict:
    """Preview what would be cleaned without doing anything."""
    total_size = sum(item.get("size", 0) for item in items)
    return {
        "items_count": len(items),
        "total_size_bytes": total_size,
        "total_size_human": _human_size(total_size),
        "items": [
            {
                "path": item.get("path", ""),
                "size_human": _human_size(item.get("size", 0)),
                "safety": item.get("safety", "UNKNOWN"),
                "reason": item.get("safety_reason", ""),
            }
            for item in items
        ],
    }


def execute_cleanup(
    items: List[Dict],
    use_trash: bool = True,
    progress_callback: Optional[Callable] = None,
    dry_run: bool = False,
) -> CleanupResult:
    """Execute cleanup on the given items.

    Returns CleanupResult tracking what was done.
    """
    result = CleanupResult()

    for i, item in enumerate(items):
        path = item.get("path", "")
        size = item.get("size", 0)
        safety = item.get("safety", "UNKNOWN")

        if progress_callback:
            progress_callback(i + 1, len(items), path)

        if safety == "PROTECTED":
            result.add_error(path, "PROTECTED - cannot delete")
            continue

        if not os.path.exists(path):
            result.add_error(path, "Path does not exist")
            continue

        if dry_run:
            result.add_success(path, size, use_trash)
            continue

        if use_trash:
            if move_to_trash(path):
                result.add_success(path, size, True)
            else:
                result.add_error(path, "Failed to move to trash")
        else:
            if permanently_delete(path):
                result.add_success(path, size, False)
            else:
                result.add_error(path, "Failed to delete")

    return result


def _human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


if __name__ == "__main__":
    # Test preview mode
    test_items = [
        {"path": "~/Downloads/old-file.zip", "size": 500_000_000, "safety": "SAFE"},
        {"path": "~/Library/Caches/temp.db", "size": 100_000_000, "safety": "CLEANABLE"},
    ]
    preview = preview_cleanup(test_items)
    print(f"Preview: {preview['items_count']} items, {preview['total_size_human']}")
    for item in preview["items"]:
        print(f"  [{item['safety']}] {item['size_human']} - {item['path']}")
    print("Cleaner module ready")
