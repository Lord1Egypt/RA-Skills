"""
Discovery and indexing of previously saved analysis reports.

Provides BaseReportIndex for O(1) lookup by commit SHA and fallback strategies.
"""

from pathlib import Path
from typing import Optional, Dict, Any


class BaseReportIndex:
    """Index for fast lookup of saved analysis reports by commit SHA."""

    async def find_by_commit(self, sha: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a saved report corresponding to the given commit SHA.

        Returns None if not found.
        """
        # Simple implementation: look in .ghostclaw/storage/reports/<sha>.json
        # This will be enhanced later with a proper index.
        reports_dir = Path.cwd() / ".ghostclaw" / "storage" / "reports"
        if not reports_dir.exists():
            return None
        report_file = reports_dir / f"{sha}.json"
        if report_file.exists():
            try:
                import json
                return json.loads(report_file.read_text())
            except Exception:
                return None
        return None


async def get_index(repo_path: Path) -> BaseReportIndex:
    """Get a BaseReportIndex instance for the given repository."""
    return BaseReportIndex()
