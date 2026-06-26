"""BM25 full-text search using SQLite FTS5."""

import aiosqlite
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ghostclaw.qmd.fts")


def _extract_searchable_text_impl(report_json_str: str) -> str:
    """Extract searchable text from a JSON report string."""
    try:
        report = json.loads(report_json_str)
    except (json.JSONDecodeError, TypeError):
        return ""
    parts = []
    # Issues
    for issue in report.get("issues", []):
        if isinstance(issue, dict):
            parts.append(issue.get("message", ""))
            if issue.get("file"):
                parts.append(f"file:{issue['file']}")
        else:
            parts.append(str(issue))
    # Architectural ghosts
    for ghost in report.get("architectural_ghosts", []):
        if isinstance(ghost, dict):
            parts.append(ghost.get("message", ""))
        else:
            parts.append(str(ghost))
    # Red flags
    for flag in report.get("red_flags", []):
        if isinstance(flag, dict):
            parts.append(flag.get("message", ""))
        else:
            parts.append(str(flag))
    # AI synthesis and reasoning
    for field in ("ai_synthesis", "ai_reasoning"):
        if report.get(field):
            parts.append(str(report[field]))
    return " ".join(parts)


class BM25Search:
    """BM25 search implementation using SQLite FTS5."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._initialized = False

    def is_initialized(self) -> bool:
        return self._initialized

    async def ensure_initialized(self) -> None:
        """Create FTS5 table and triggers if they don't exist."""
        if self._initialized:
            return

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await self._register_searchable_function(db)
            async with db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='reports_fts'"
            ) as cursor:
                exists = await cursor.fetchone()

            if not exists:
                await db.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS reports_fts
                    USING fts5(
                        report_id UNINDEXED,
                        content,
                        tokenize = 'porter'
                    )
                """)
                await db.execute("""
                    INSERT INTO reports_fts(report_id, content)
                    SELECT id, extract_searchable_text(report_json)
                    FROM reports
                """)
                await db.executescript("""
                    CREATE TRIGGER reports_ai AFTER INSERT ON reports BEGIN
                        INSERT INTO reports_fts(report_id, content)
                        VALUES (new.id, extract_searchable_text(new.report_json));
                    END;
                    CREATE TRIGGER reports_ad AFTER DELETE ON reports BEGIN
                        DELETE FROM reports_fts WHERE report_id = old.id;
                    END;
                    CREATE TRIGGER reports_au AFTER UPDATE ON reports BEGIN
                        UPDATE reports_fts SET content = extract_searchable_text(new.report_json)
                        WHERE report_id = new.id;
                    END;
                """)
                logger.info("Created FTS5 table and triggers")
        self._initialized = True

    async def _register_searchable_function(self, db) -> None:
        """Register the extract_searchable_text SQL function."""
        await db.create_function("extract_searchable_text", 1, _extract_searchable_text_impl)

    async def search(
        self,
        query: str,
        limit: int = 10,
        repo_path: Optional[str] = None,
        stack: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Perform BM25 search."""
        results = []
        async with aiosqlite.connect(self.db_path) as db:
            await self._register_searchable_function(db)
            db.row_factory = aiosqlite.Row
            sql = """
                SELECT r.id, r.timestamp, r.vibe_score, r.stack, r.repo_path, r.report_json,
                       bm25(reports_fts) as bm25_score
                FROM reports_fts f
                JOIN reports r ON f.report_id = r.id
                WHERE reports_fts MATCH ?
            """
            params = [query]
            if repo_path:
                sql += " AND r.repo_path = ?"
                params.append(repo_path)
            if stack:
                sql += " AND r.stack = ?"
                params.append(stack)
            if min_score is not None:
                sql += " AND r.vibe_score >= ?"
                params.append(min_score)
            if max_score is not None:
                sql += " AND r.vibe_score <= ?"
                params.append(max_score)
            sql += " ORDER BY bm25(reports_fts) ASC LIMIT ?"
            params.append(limit * 2)  # oversample to dedup if needed

            async with db.execute(sql, params) as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    report = json.loads(row["report_json"])
                    results.append({
                        "id": row["id"],
                        "timestamp": row["timestamp"],
                        "vibe_score": row["vibe_score"],
                        "stack": row["stack"],
                        "repo_path": row["repo_path"],
                        "report": report,
                        "score": -row["bm25_score"],  # invert so higher = better
                        "matched_snippets": [],  # to be filled by caller
                    })
        return results
