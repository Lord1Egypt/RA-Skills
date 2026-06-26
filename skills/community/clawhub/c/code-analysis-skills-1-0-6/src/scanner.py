"""
Repository Scanner - Discovers Git repositories.
"""

import os
import logging
from typing import List, Dict

from git import Repo, InvalidGitRepositoryError

logger = logging.getLogger(__name__)


class RepoScanner:
    """Scans file system paths to discover Git repositories."""

    def scan_single(self, path: str) -> List[Dict]:
        """
        Validate and return info for a single Git repository.

        Args:
            path: Path to a Git repository.

        Returns:
            A list containing one repo info dict, or empty if invalid.
        """
        path = os.path.abspath(path)
        try:
            repo = Repo(path)
            if repo.bare:
                logger.warning("Bare repository found, skipping: %s", path)
                return []
            return [self._repo_info(repo, path)]
        except InvalidGitRepositoryError:
            logger.error("Not a valid Git repository: %s", path)
            return []

    def scan_directory(self, root_path: str, max_depth: int = 5) -> List[Dict]:
        """
        Recursively scan a directory for Git repositories.

        Args:
            root_path: Root directory to scan.
            max_depth: Maximum directory depth to traverse.

        Returns:
            A list of repo info dicts.
        """
        root_path = os.path.abspath(root_path)
        repos = []
        visited = set()

        self._walk_for_repos(root_path, repos, visited, current_depth=0, max_depth=max_depth)

        logger.info("Scan complete. Found %d repositories under %s", len(repos), root_path)
        return repos

    def _walk_for_repos(
        self,
        directory: str,
        repos: List[Dict],
        visited: set,
        current_depth: int,
        max_depth: int,
    ):
        """Recursively walk directories to find .git folders."""
        if current_depth > max_depth:
            return

        real_dir = os.path.realpath(directory)
        if real_dir in visited:
            return
        visited.add(real_dir)

        try:
            entries = os.listdir(directory)
        except PermissionError:
            logger.debug("Permission denied: %s", directory)
            return

        if ".git" in entries:
            git_path = os.path.join(directory, ".git")
            if os.path.isdir(git_path):
                try:
                    repo = Repo(directory)
                    if not repo.bare:
                        repos.append(self._repo_info(repo, directory))
                        logger.debug("Found repository: %s", directory)
                except InvalidGitRepositoryError:
                    pass
                # Don't recurse into a repo's subdirectories for nested repos
                return

        for entry in sorted(entries):
            if entry.startswith("."):
                continue
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                self._walk_for_repos(full_path, repos, visited, current_depth + 1, max_depth)

    @staticmethod
    def _repo_info(repo: Repo, path: str) -> Dict:
        """Build a standardized repo info dictionary."""
        try:
            active_branch = repo.active_branch.name
        except TypeError:
            active_branch = "HEAD (detached)"

        return {
            "name": os.path.basename(path),
            "path": path,
            "active_branch": active_branch,
            "remotes": [r.name for r in repo.remotes] if repo.remotes else [],
        }
