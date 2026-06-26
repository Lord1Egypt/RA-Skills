"""Directory migrator - migrate directories using symbolic links."""

import os
import shutil
import subprocess
from pathlib import Path

from ..models import LinkType, MigrationResult


class DirectoryMigrator:
    """
    Migrator for moving directories and creating symbolic links.

    Handles the complete migration process:
    1. Copy directory to target location
    2. Verify copy success
    3. Delete original directory
    4. Create symbolic link or junction
    """

    def _has_admin_privilege(self) -> bool:
        """Check if running with administrator privileges on Windows."""
        if os.name != "nt":
            return True
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def check_link_type(self, path: str) -> tuple[LinkType, str | None]:
        """Check if a path is a link."""
        if not os.path.exists(path):
            return LinkType.NOT_FOUND, None

        try:
            if os.path.islink(path):
                target = os.readlink(path)
                return LinkType.SYMBOLIC_LINK, target

            if os.name == "nt":
                result = subprocess.run(
                    ["fsutil", "reparsepoint", "query", path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                output = result.stdout

                if "Tag value: 0xa000000c" in output:
                    for line in output.split("\n"):
                        if "Print Name:" in line:
                            return LinkType.SYMBOLIC_LINK, line.split(":", 1)[1].strip()
                    return LinkType.SYMBOLIC_LINK, None

                if "Tag value: 0xa0000003" in output:
                    for line in output.split("\n"):
                        if "Print Name:" in line:
                            return LinkType.JUNCTION, line.split(":", 1)[1].strip()
                    return LinkType.JUNCTION, None

        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        return LinkType.NORMAL, None

    def migrate(
        self,
        source: str,
        target: str,
        verify: bool = True,
        link_type: str = "auto",
    ) -> MigrationResult:
        """
        Migrate a directory to a new location and create a link.

        Args:
            source: Source directory path
            target: Target directory path
            verify: Whether to verify copy before deleting source
            link_type: Link type to create - "auto", "symlink", or "junction"
                      - "auto": Use junction if no admin, else symlink
                      - "symlink": Always use symbolic link (requires admin on Windows)
                      - "junction": Always use junction (no admin required)

        Returns:
            MigrationResult indicating success or failure
        """
        source_path = Path(source).expanduser().resolve()
        target_path = Path(target).expanduser().resolve()

        # Validate source
        if not source_path.exists():
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Source does not exist: {source_path}",
            )

        # Check if source is already a link
        existing_link_type, _ = self.check_link_type(str(source_path))
        if existing_link_type != LinkType.NORMAL:
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Source is already a {existing_link_type.value}",
            )

        # Check if target exists
        if target_path.exists():
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Target already exists: {target_path}",
            )

        # Ensure target parent exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy directory
        try:
            if os.name == "nt":
                # Use robocopy on Windows for better performance
                result = subprocess.run(
                    ["robocopy", str(source_path), str(target_path), "/E", "/R:1", "/W:1"],
                    capture_output=True,
                    timeout=3600,
                )
                # robocopy returns 0-7 for success
                if result.returncode > 7:
                    return MigrationResult(
                        success=False,
                        source=str(source_path),
                        target=str(target_path),
                        error=f"Copy failed with code {result.returncode}",
                    )
            else:
                # Use shutil on Unix
                shutil.copytree(source_path, target_path)
        except subprocess.TimeoutExpired:
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error="Copy timed out",
            )
        except Exception as e:
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Copy failed: {str(e)}",
            )

        # Verify copy
        if verify:
            if not target_path.exists():
                return MigrationResult(
                    success=False,
                    source=str(source_path),
                    target=str(target_path),
                    error="Copy verification failed: target not found",
                )

        # Delete source
        try:
            if os.name == "nt":
                subprocess.run(
                    ["rmdir", "/s", "/q", str(source_path)],
                    shell=True,
                    capture_output=True,
                    timeout=300,
                )
            else:
                shutil.rmtree(source_path)
        except Exception as e:
            # Rollback: remove target if we can't delete source
            try:
                if os.name == "nt":
                    subprocess.run(
                        ["rmdir", "/s", "/q", str(target_path)],
                        shell=True,
                        capture_output=True,
                        timeout=60,
                    )
                else:
                    shutil.rmtree(target_path)
            except Exception:
                pass

            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Delete source failed: {str(e)}",
            )

        # Create link
        use_junction = False
        if os.name == "nt":
            if link_type == "junction":
                use_junction = True
            elif link_type == "symlink":
                use_junction = False
            else:  # auto
                use_junction = not self._has_admin_privilege()

        try:
            if os.name == "nt":
                if use_junction:
                    # Junction: no admin required
                    cmd = ["mklink", "/J", str(source_path), str(target_path)]
                else:
                    # Symbolic link: requires admin
                    cmd = ["mklink", "/D", str(source_path), str(target_path)]

                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    return MigrationResult(
                        success=False,
                        source=str(source_path),
                        target=str(target_path),
                        error=(
                            f"Create link failed: "
                            f"{result.stderr.decode() if result.stderr else 'unknown error'}"
                        ),
                    )
            else:
                os.symlink(target_path, source_path)
        except Exception as e:
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Create link failed: {str(e)}",
            )

        # Verify link
        created_type, created_target = self.check_link_type(str(source_path))
        expected_type = LinkType.JUNCTION if use_junction else LinkType.SYMBOLIC_LINK
        if created_type != expected_type:
            return MigrationResult(
                success=False,
                source=str(source_path),
                target=str(target_path),
                error=f"Link verification failed: expected {expected_type.value}, got {created_type.value}",
            )

        return MigrationResult(
            success=True,
            source=str(source_path),
            target=str(target_path),
            link_type="junction" if use_junction else "symbolic_link",
        )

    def convert_junction_to_symlink(
        self,
        path: str,
        target: str | None = None,
    ) -> MigrationResult:
        """
        Convert a Windows Junction to a Symbolic Link.

        Args:
            path: Path to the junction
            target: Target path (if None, uses existing target)

        Returns:
            MigrationResult indicating success or failure
        """
        link_type, current_target = self.check_link_type(path)

        if link_type == LinkType.SYMBOLIC_LINK:
            return MigrationResult(
                success=True,
                source=path,
                target=current_target or "",
                link_type="symbolic_link",
            )

        if link_type != LinkType.JUNCTION:
            return MigrationResult(
                success=False,
                source=path,
                target=target or "",
                error=f"Path is not a junction: {link_type.value}",
            )

        # Use existing target if not specified
        actual_target = target or current_target
        if not actual_target:
            return MigrationResult(
                success=False,
                source=path,
                target="",
                error="Cannot determine target path",
            )

        # Remove junction (doesn't delete target)
        try:
            if os.name == "nt":
                subprocess.run(
                    ["rmdir", path],
                    shell=True,
                    capture_output=True,
                    timeout=60,
                )
            else:
                os.rmdir(path)
        except Exception as e:
            return MigrationResult(
                success=False,
                source=path,
                target=actual_target,
                error=f"Remove junction failed: {str(e)}",
            )

        # Create symbolic link
        try:
            if os.name == "nt":
                result = subprocess.run(
                    ["mklink", "/D", path, actual_target],
                    shell=True,
                    capture_output=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    return MigrationResult(
                        success=False,
                        source=path,
                        target=actual_target,
                        error="Create symbolic link failed",
                    )
            else:
                os.symlink(actual_target, path)
        except Exception as e:
            return MigrationResult(
                success=False,
                source=path,
                target=actual_target,
                error=f"Create symbolic link failed: {str(e)}",
            )

        return MigrationResult(
            success=True,
            source=path,
            target=actual_target,
            link_type="symbolic_link",
        )
