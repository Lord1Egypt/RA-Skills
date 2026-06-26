"""Directory scanner - scan and analyze directory sizes."""

import os
import subprocess
from pathlib import Path

from ..models import DirectoryInfo, FileInfo, LinkType, ScanResult


class DirectoryScanner:
    """
    Scanner for analyzing directory sizes and link status.

    Provides efficient scanning with configurable depth and filtering.
    """

    def __init__(self, follow_links: bool = False):
        """
        Initialize scanner.

        Args:
            follow_links: Whether to follow symbolic links when scanning
        """
        self.follow_links = follow_links

    def check_link_type(self, path: str) -> tuple[LinkType, str | None]:
        """
        Check if a path is a symbolic link, junction, or normal directory.

        Args:
            path: Path to check

        Returns:
            Tuple of (LinkType, target_path if link else None)
        """
        if not os.path.exists(path):
            return LinkType.NOT_FOUND, None

        try:
            # Check for symbolic link
            if os.path.islink(path):
                target = os.readlink(path)
                return LinkType.SYMBOLIC_LINK, target

            # On Windows, check for junction using fsutil
            if os.name == "nt":
                result = subprocess.run(
                    ["fsutil", "reparsepoint", "query", path],
                    capture_output=True,
                    # Use utf-8 with error handling for Chinese paths
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    timeout=10,
                )
                output = result.stdout or ""

                if "Tag value: 0xa000000c" in output or "Symbolic Link" in output:
                    target = None
                    for line in output.split("\n"):
                        if "Print Name:" in line:
                            target = line.split(":", 1)[1].strip()
                            break
                    return LinkType.SYMBOLIC_LINK, target

                elif "Tag value: 0xa0000003" in output or "Mount Point" in output:
                    target = None
                    for line in output.split("\n"):
                        if "Print Name:" in line:
                            target = line.split(":", 1)[1].strip()
                            break
                    return LinkType.JUNCTION, target

        except (subprocess.TimeoutExpired, FileNotFoundError, OSError, UnicodeDecodeError):
            pass

        return LinkType.NORMAL, None

    def get_directory_size(self, path: str) -> int:
        """
        Calculate total size of a directory in bytes (including all subdirectories).

        Args:
            path: Directory path

        Returns:
            Total size in bytes
        """
        if not os.path.exists(path):
            return 0

        total = 0
        try:
            for root, _, files in os.walk(path, followlinks=self.follow_links):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        total += os.path.getsize(fp)
                    except (OSError, FileNotFoundError):
                        pass
        except (OSError, PermissionError):
            pass

        return total

    def get_file_types(self, path: str, limit: int = 100) -> dict[str, int]:
        """
        Get file type distribution in a directory.

        Args:
            path: Directory path
            limit: Maximum number of files to sample

        Returns:
            Dict mapping file extensions to counts
        """
        extensions: dict[str, int] = {}
        count = 0

        try:
            for _root, _, files in os.walk(path):
                for f in files:
                    if count >= limit:
                        return extensions

                    ext = Path(f).suffix.lower() or "no_extension"
                    extensions[ext] = extensions.get(ext, 0) + 1
                    count += 1
        except (OSError, PermissionError):
            pass

        return extensions

    def count_files(self, path: str, limit: int = 10000) -> int:
        """
        Count files in a directory.

        Args:
            path: Directory path
            limit: Maximum count to prevent long scans

        Returns:
            Number of files
        """
        count = 0
        try:
            for _root, _, files in os.walk(path):
                count += len(files)
                if count >= limit:
                    return count
        except (OSError, PermissionError):
            pass

        return count

    def scan_directory(
        self,
        path: str,
        include_file_types: bool = False,
        count_link_target: bool = False,
    ) -> DirectoryInfo:
        """
        Scan a single directory.

        Args:
            path: Directory path
            include_file_types: Whether to include file type distribution
            count_link_target: If True, include symlink target size (default: False)

        Returns:
            DirectoryInfo with scan results
        """
        link_type, link_target = self.check_link_type(path)

        # 符号链接/Junction 默认返回 size=0（数据已在目标位置）
        # 除非显式指定 count_link_target=True
        if link_type != LinkType.NORMAL and not count_link_target:
            size = 0
        else:
            size = self.get_directory_size(path)

        file_types = {}
        file_count = 0

        if include_file_types and link_type == LinkType.NORMAL:
            file_types = self.get_file_types(path)
            file_count = self.count_files(path)

        return DirectoryInfo(
            path=path,
            size_bytes=size,
            link_type=link_type,
            link_target=link_target,
            file_types=file_types,
            file_count=file_count,
        )

    def scan_path(
        self,
        path: str,
        max_depth: int = 3,
        min_size_mb: float = 0,
    ) -> ScanResult:
        """
        Scan a path and all subdirectories up to a certain depth.

        Args:
            path: Root path to scan
            max_depth: Maximum depth to scan
            min_size_mb: Minimum size in MB to include

        Returns:
            ScanResult with all directories and files found
        """
        base_path = Path(path).expanduser().resolve()
        results: list[DirectoryInfo] = []
        files: list[FileInfo] = []
        root_subdirs_size = 0
        root_files_size = 0

        def scan_recursive(current_path: Path, depth: int, is_root: bool = False):
            if depth > max_depth:
                return

            try:
                for item in current_path.iterdir():
                    if item.is_dir():
                        info = self.scan_directory(str(item))

                        if info.size_bytes >= min_size_mb * 1024 * 1024:
                            results.append(info)

                        if is_root:
                            nonlocal root_subdirs_size
                            root_subdirs_size += info.size_bytes

                        if info.link_type == LinkType.NORMAL:
                            scan_recursive(item, depth + 1)
                    else:
                        try:
                            stat = item.stat()
                            file_info = FileInfo(
                                path=str(item),
                                name=item.name,
                                size_bytes=stat.st_size,
                                modified_time=stat.st_mtime,
                            )
                            files.append(file_info)
                            if is_root:
                                nonlocal root_files_size
                                root_files_size += stat.st_size
                        except (OSError, PermissionError):
                            pass

            except (OSError, PermissionError):
                pass

        scan_recursive(base_path, 0, is_root=True)

        total_size = root_subdirs_size + root_files_size

        results.sort(key=lambda x: x.size_bytes, reverse=True)
        files.sort(key=lambda x: x.size_bytes, reverse=True)

        return ScanResult(
            directories=results,
            files=files,
            total_size_bytes=total_size,
            scan_path=str(base_path),
        )

    def scan_user_profile(
        self,
        profile_path: str | None = None,
        depth: int = 3,
    ) -> ScanResult:
        """
        Scan a user profile directory (e.g., home directory).

        Args:
            profile_path: User profile path (default: home directory)
            depth: Depth of scan (1-3 levels)

        Returns:
            ScanResult with all directories found
        """
        if profile_path is None:
            profile_path = os.path.expanduser("~")

        return self.scan_path(profile_path, max_depth=depth)
