"""Directory cleaner - safe directory cleaning operations."""

import os
import shutil
from pathlib import Path

from ..models import CleanResult


class DirectoryCleaner:
    """
    Cleaner for safely removing directory contents.

    Provides dry-run mode and safety checks before deletion.
    """

    def __init__(self, protected_paths: list[str] | None = None):
        """
        Initialize cleaner.

        Args:
            protected_paths: List of paths that should never be deleted
        """
        self.protected_paths = set()
        if protected_paths:
            for p in protected_paths:
                self.protected_paths.add(str(Path(p).expanduser().resolve()))

        # Add default protected paths
        home = str(Path.home().resolve())
        self.protected_paths.add(home)
        self.protected_paths.add(os.path.join(home, "Documents"))
        self.protected_paths.add(os.path.join(home, "Desktop"))

    def is_protected(self, path: str) -> bool:
        """Check if a path is protected from deletion."""
        resolved = str(Path(path).expanduser().resolve())
        return resolved in self.protected_paths

    def get_size(self, path: str) -> int:
        """Get total size of a directory in bytes."""
        if not os.path.exists(path):
            return 0

        total = 0
        try:
            for root, _, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        total += os.path.getsize(fp)
                    except (OSError, FileNotFoundError):
                        pass
        except (OSError, PermissionError):
            pass

        return total

    def clean(
        self,
        path: str,
        dry_run: bool = True,
        keep_root: bool = False,
    ) -> CleanResult:
        """
        Clean a directory.

        Args:
            path: Directory path to clean
            dry_run: If True, only report what would be deleted
            keep_root: If True, keep the root directory but delete contents

        Returns:
            CleanResult with operation details
        """
        path_obj = Path(path).expanduser().resolve()
        path_str = str(path_obj)

        # Check if path exists
        if not path_obj.exists():
            return CleanResult(
                success=False,
                path=path_str,
                error="Path does not exist",
                dry_run=dry_run,
            )

        # Check if protected
        if self.is_protected(path_str):
            return CleanResult(
                success=False,
                path=path_str,
                error="Path is protected and cannot be deleted",
                dry_run=dry_run,
            )

        # Get size before deletion
        size = self.get_size(path_str)

        if dry_run:
            return CleanResult(
                success=True,
                path=path_str,
                freed_bytes=size,
                dry_run=True,
            )

        # Perform deletion
        try:
            if keep_root:
                # Delete contents but keep directory
                for item in path_obj.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            else:
                # Delete entire directory
                shutil.rmtree(path_obj)

            return CleanResult(
                success=True,
                path=path_str,
                freed_bytes=size,
                dry_run=False,
            )
        except PermissionError as e:
            return CleanResult(
                success=False,
                path=path_str,
                error=f"Permission denied: {str(e)}",
                dry_run=False,
            )
        except Exception as e:
            return CleanResult(
                success=False,
                path=path_str,
                error=f"Clean failed: {str(e)}",
                dry_run=False,
            )

    def clean_contents(
        self,
        path: str,
        patterns: list[str] | None = None,
        dry_run: bool = True,
    ) -> CleanResult:
        """
        Clean specific files matching patterns in a directory.

        Args:
            path: Directory path
            patterns: File patterns to delete (e.g., ["*.log", "*.tmp"])
            dry_run: If True, only report what would be deleted

        Returns:
            CleanResult with operation details
        """
        path_obj = Path(path).expanduser().resolve()
        path_str = str(path_obj)

        if not path_obj.exists():
            return CleanResult(
                success=False,
                path=path_str,
                error="Path does not exist",
                dry_run=dry_run,
            )

        if not patterns:
            return self.clean(path_str, dry_run=dry_run, keep_root=True)

        # Find matching files
        matched_files: list[Path] = []
        matched_dirs: list[Path] = []

        for pattern in patterns:
            matched_files.extend(path_obj.glob(pattern))
            matched_dirs.extend(path_obj.glob(pattern))

        # Calculate total size
        total_size = 0
        for f in matched_files:
            if f.is_file():
                try:
                    total_size += f.stat().st_size
                except (OSError, FileNotFoundError):
                    pass

        if dry_run:
            return CleanResult(
                success=True,
                path=path_str,
                freed_bytes=total_size,
                dry_run=True,
            )

        # Delete matched files
        try:
            for f in matched_files:
                if f.is_file():
                    f.unlink()

            # Delete empty directories
            for d in reversed(sorted(matched_dirs, key=lambda x: len(x.parts))):
                if d.is_dir():
                    try:
                        d.rmdir()  # Only removes if empty
                    except OSError:
                        pass

            return CleanResult(
                success=True,
                path=path_str,
                freed_bytes=total_size,
                dry_run=False,
            )
        except Exception as e:
            return CleanResult(
                success=False,
                path=path_str,
                error=f"Clean failed: {str(e)}",
                dry_run=False,
            )
