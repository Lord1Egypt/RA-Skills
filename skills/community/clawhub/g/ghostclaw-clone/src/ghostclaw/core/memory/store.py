"""
Core storage logic for Ghostclaw memory.
"""

import json
import sqlite3
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import aiosqlite
    HAS_AIOSQLITE = True
except ImportError:
    HAS_AIOSQLITE = False

logger = logging.getLogger("ghostclaw.memory.store")


class MemoryStore:
    """
    Agent-facing memory interface over Ghostclaw's SQLite history.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Path.cwd() / ".ghostclaw" / "storage" / "ghostclaw.db"

    def _db_exists(self) -> bool:
        return self.db_path.exists()

    async def _ensure_db(self) -> None:
        """Create the database and tables if they don't exist yet."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    vibe_score INTEGER,
                    stack TEXT,
                    files_analyzed INTEGER,
                    total_lines INTEGER,
                    report_json TEXT,
                    repo_path TEXT
                )
            """)
            await db.commit()

    async def list_runs(
        self,
        limit: int = 20,
        repo_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List recent analysis runs with summary metadata."""
        if not self._db_exists():
            return []

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            if repo_path:
                query = (
                    "SELECT id, timestamp, vibe_score, stack, files_analyzed, "
                    "total_lines, repo_path FROM reports "
                    "WHERE repo_path = ? ORDER BY timestamp DESC LIMIT ?"
                )
                params = (repo_path, limit)
            else:
                query = (
                    "SELECT id, timestamp, vibe_score, stack, files_analyzed, "
                    "total_lines, repo_path FROM reports "
                    "ORDER BY timestamp DESC LIMIT ?"
                )
                params = (limit,)

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        """Get the full report for a specific run by its ID."""
        if not self._db_exists():
            return None

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            async with db.execute(
                "SELECT * FROM reports WHERE id = ?", (run_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                row_dict = dict(row)
                try:
                    row_dict["report"] = json.loads(row_dict.pop("report_json", "{}"))
                except (json.JSONDecodeError, TypeError):
                    row_dict["report"] = {}
                return row_dict

    async def get_previous_run(
        self, repo_path: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get the most recent analysis run, optionally filtered by repo path."""
        if not self._db_exists():
            return None

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            if repo_path:
                query = "SELECT * FROM reports WHERE repo_path = ? ORDER BY timestamp DESC LIMIT 1"
                params = (repo_path,)
            else:
                query = "SELECT * FROM reports ORDER BY timestamp DESC LIMIT 1"
                params = ()

            async with db.execute(query, params) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                row_dict = dict(row)
                try:
                    row_dict["report"] = json.loads(row_dict.pop("report_json", "{}"))
                except (json.JSONDecodeError, TypeError):
                    row_dict["report"] = {}
                return row_dict

    # Advanced functionality delegated to mcp submodule
    async def search(self, *args, **kwargs):
        from .mcp import search_memory
        return await search_memory(self, *args, **kwargs)

    async def diff_runs(self, *args, **kwargs):
        from .mcp import diff_analysis_runs
        return await diff_analysis_runs(self, *args, **kwargs)

    async def get_knowledge_graph(self, *args, **kwargs):
        from .mcp import generate_knowledge_graph
        return await generate_knowledge_graph(self, *args, **kwargs)
