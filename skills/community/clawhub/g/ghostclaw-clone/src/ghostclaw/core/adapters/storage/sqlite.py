"""Storage adapter using SQLite for vibe history persistence."""

import json
import sqlite3
import aiosqlite
from pathlib import Path
from typing import Dict, List, Any, Optional
from ghostclaw.core.adapters.base import StorageAdapter, AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl


class SQLiteStorageAdapter(StorageAdapter):
    """Persists ArchitectureReports to a local SQLite database."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Path.cwd() / ".ghostclaw" / "storage" / "ghostclaw.db"
        self._initialized = False

    async def _ensure_db(self):
        """Initialize the database schema if needed."""
        if self._initialized:
            return

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    vibe_score INTEGER,
                    stack TEXT,
                    files_analyzed INTEGER,
                    total_lines INTEGER,
                    report_json TEXT,
                    repo_path TEXT,
                    vcs_commit TEXT,
                    vcs_branch TEXT,
                    vcs_dirty BOOLEAN
                )
            """)
            await db.commit()

        self._initialized = True

    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="sqlite",
            version="0.1.0",
            description="Asynchronous SQLite storage for vibe history.",
            dependencies=["aiosqlite"],
        )

    async def is_available(self) -> bool:
        """aiosqlite is a python dependency, usually available if installed."""
        return True

    @hookimpl
    async def ghost_save_report(self, report: Any) -> Optional[str]:
        """Hook implementation for saving report."""
        return await self.save_report(report)

    async def save_report(self, report: Any) -> str:
        """Implementation of StorageAdapter interface."""
        await self._ensure_db()

        # report is expected to be an ArchitectureReport (Pydantic model)
        # or a dict. We'll handle both.
        if hasattr(report, "model_dump"):
            data = report.model_dump()
        else:
            data = report

        async with aiosqlite.connect(self.db_path) as db:
            repo_path = data.get("repo_path") or data.get("metadata", {}).get("repo_path") or str(Path.cwd())
            vcs = data.get("metadata", {}).get("vcs", {})
            cursor = await db.execute(
                "INSERT INTO reports (vibe_score, stack, files_analyzed, total_lines, repo_path, vcs_commit, vcs_branch, vcs_dirty, report_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    data.get("vibe_score", 0),
                    data.get("stack", "unknown"),
                    data.get("files_analyzed", 0),
                    data.get("total_lines", 0),
                    str(repo_path),
                    vcs.get("commit", ""),
                    vcs.get("branch", ""),
                    vcs.get("dirty", False),
                    json.dumps(data),
                ),
            )
            await db.commit()
            return str(cursor.lastrowid)

    async def get_history(self, limit: int = 10) -> List[Any]:
        """Implementation of StorageAdapter interface."""
        await self._ensure_db()

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            async with db.execute(
                "SELECT * FROM reports ORDER BY timestamp DESC LIMIT ?", (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    @hookimpl
    def ghost_get_metadata(self) -> Dict[str, Any]:
        """Expose metadata to the plugin manager."""
        meta = self.get_metadata()
        return {
            "name": meta.name,
            "version": meta.version,
            "description": meta.description,
            "available": True,
        }
