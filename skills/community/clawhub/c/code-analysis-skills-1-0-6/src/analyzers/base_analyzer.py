"""
Base Analyzer - Abstract base class for all analyzers.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from pydriller import Repository

logger = logging.getLogger(__name__)


class BaseAnalyzer(ABC):
    """
    Abstract base class providing common infrastructure for all analyzers.

    Each analyzer receives repository path and optional filters, then
    implements the `analyze()` method to produce structured metrics.
    """

    def __init__(
        self,
        repo_path: str,
        authors: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        branch: Optional[str] = None,
    ):
        self.repo_path = repo_path
        self.authors = authors
        self.since = since
        self.until = until
        self.branch = branch

    def _get_commits(self):
        """
        Yield commits from the repository applying configured filters.

        Uses PyDriller for rich commit traversal with author/date filtering.
        """
        kwargs = {"path_to_repo": self.repo_path}

        if self.since:
            from datetime import datetime
            kwargs["since"] = datetime.fromisoformat(self.since)
        if self.until:
            from datetime import datetime
            kwargs["to"] = datetime.fromisoformat(self.until)
        if self.branch:
            kwargs["only_in_branch"] = self.branch

        try:
            for commit in Repository(**kwargs).traverse_commits():
                if self.authors:
                    if not self._author_matches(commit.author.name, commit.author.email):
                        continue
                yield commit
        except Exception as e:
            logger.error("Error traversing commits in %s: %s", self.repo_path, e)

    def _author_matches(self, name: str, email: str) -> bool:
        """Check if a commit author matches the configured author filters."""
        for author_filter in self.authors:
            af_lower = author_filter.lower()
            if af_lower in name.lower() or af_lower in email.lower():
                return True
        return False

    @abstractmethod
    def analyze(self) -> Dict:
        """
        Run analysis and return structured metrics.

        Returns:
            A dict of metrics keyed by author name.
        """
        ...
