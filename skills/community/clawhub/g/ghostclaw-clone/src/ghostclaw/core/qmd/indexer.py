"""ReportIndexer — persists reports, managing FTS and vector embeddings together."""

import aiosqlite
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from .fts import BM25Search
from .embeddings import EmbeddingManager

logger = logging.getLogger("ghostclaw.qmd.indexer")


class ReportIndexer:
    """Handles report persistence: save, update, delete with FTS and embeddings."""

    def __init__(self, db_path: Path, fts: BM25Search, embedding_mgr: Optional[EmbeddingManager]):
        self.db_path = db_path
        self.fts = fts
        self.embedding_mgr = embedding_mgr

    async def save(self, report: Dict[str, Any], repo_path: str, timestamp: Optional[str] = None) -> int:
        """Save a new report and return its run_id."""
        await self._ensure_db()
        await self.fts.ensure_initialized()

        timestamp = timestamp or report.get("metadata", {}).get("timestamp") or datetime.now().isoformat()
        vcs = report.get("metadata", {}).get("vcs", {})

        async with aiosqlite.connect(self.db_path) as db:
            await self.fts._register_searchable_function(db)
            async with db.execute(
                "INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, repo_path, vcs_commit, vcs_branch, vcs_dirty, report_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    timestamp,
                    report.get("vibe_score", 0),
                    report.get("stack", ""),
                    report.get("files_analyzed", 0),
                    report.get("total_lines", 0),
                    repo_path,
                    vcs.get("commit", ""),
                    vcs.get("branch", ""),
                    vcs.get("dirty", False),
                    json.dumps(report),
                ),
            ) as cursor:
                run_id = cursor.lastrowid
                await db.commit()

            # Store embeddings if enhanced
            if self.embedding_mgr:
                try:
                    chunks = self.embedding_mgr._extract_chunks(report, run_id)
                    base_metadata = {
                        "repo_path": repo_path,
                        "timestamp": timestamp,
                        "vibe_score": report.get("vibe_score"),
                        "stack": report.get("stack"),
                    }
                    await self.embedding_mgr.vector_store.add_chunks(run_id, chunks, base_metadata)
                    logger.debug("Stored %d embeddings for run_id=%d", len(chunks), run_id)
                except Exception as e:
                    logger.error("Failed to store embeddings for run_id=%d: %s", run_id, e)

            return run_id

    async def delete(self, run_id: int) -> bool:
        """Delete a report by run_id. Returns True if deleted."""
        await self._ensure_db()
        async with aiosqlite.connect(self.db_path) as db:
            await self.fts._register_searchable_function(db)
            cursor = await db.execute("DELETE FROM reports WHERE id = ?", (run_id,))
            await db.commit()
            return cursor.rowcount > 0

    async def _ensure_db(self) -> None:
        """Ensure reports table exists and has required columns."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            # Create table if not exists
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    vibe_score INTEGER NOT NULL,
                    stack TEXT NOT NULL,
                    files_analyzed INTEGER,
                    total_lines INTEGER,
                    repo_path TEXT NOT NULL,
                    vcs_commit TEXT,
                    vcs_branch TEXT,
                    vcs_dirty BOOLEAN,
                    report_json TEXT NOT NULL
                )
            """
            )
            # Migration: add columns if missing (for older DBs)
            async with db.execute("PRAGMA table_info(reports)") as cursor:
                rows = await cursor.fetchall()
                column_names = [row[1] for row in rows]  # row[1] is name

            if 'files_analyzed' not in column_names:
                await db.execute("ALTER TABLE reports ADD COLUMN files_analyzed INTEGER")
            if 'total_lines' not in column_names:
                await db.execute("ALTER TABLE reports ADD COLUMN total_lines INTEGER")

            await db.commit()
