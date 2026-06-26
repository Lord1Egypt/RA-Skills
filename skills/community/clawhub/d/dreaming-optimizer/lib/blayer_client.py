#!/usr/bin/env python3
"""B-layer SQLite read/write client for dreaming-optimizer."""
import sqlite3
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Any

logger = logging.getLogger("dreaming-optimizer.blayer")


class BLayerClient:
    """Client for reading and writing to the B-layer SQLite database."""
    
    def __init__(self, db_path: Path = None, agent: str = "main"):
        """Initialize B-layer client.
        
        Args:
            db_path: Explicit SQLite path. If None, derives from agent name.
            agent: Agent name (used to derive db_path if db_path is None)
        """
        if db_path is None:
            base = Path.home() / ".openclaw" / "memory"
            base.mkdir(parents=True, exist_ok=True)
            db_path = base / f"{agent}.sqlite"
        
        self.db_path = db_path
        self.agent = agent
        self._ensure_schema()
    
    # ─────────────────────────────────────────────────────────────────
    # Schema Management
    # ─────────────────────────────────────────────────────────────────
    
    SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        content_preview TEXT,
        score INTEGER DEFAULT 50,
        tag TEXT DEFAULT 'context' CHECK(tag IN ('fact','opinion','preference','learning','context')),
        source TEXT,
        source_agent TEXT DEFAULT 'dreaming-optimizer',
        is_merged BOOLEAN DEFAULT 0,
        merged_into INTEGER,
        created_at TEXT,
        updated_at TEXT,
        last_accessed_at TEXT,
        access_count INTEGER DEFAULT 0
    );
    
    CREATE INDEX IF NOT EXISTS idx_memories_score ON memories(score);
    CREATE INDEX IF NOT EXISTS idx_memories_tag ON memories(tag);
    CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
    
    CREATE TABLE IF NOT EXISTS dreaming_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_content_hash TEXT,
        action TEXT CHECK(action IN ('committed','archived','merged','discarded')),
        score INTEGER,
        similarity_score REAL,
        merged_into_id INTEGER,
        reason TEXT,
        ts TEXT DEFAULT (datetime('now')),
        source_file TEXT
    );
    
    CREATE INDEX IF NOT EXISTS idx_dreaming_log_ts ON dreaming_log(ts);
    CREATE INDEX IF NOT EXISTS idx_dreaming_log_action ON dreaming_log(action);
    """
    
    def _ensure_schema(self) -> None:
        """Ensure the B-layer schema exists."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.db_path))
            conn.executescript(self.SCHEMA_SQL)
            conn.commit()
            conn.close()
            logger.debug(f"Schema ensured at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to create schema: {e}")
            raise
    
    # ─────────────────────────────────────────────────────────────────
    # Read Operations
    # ─────────────────────────────────────────────────────────────────
    
    def get_memories(
        self,
        limit: int = 1000,
        min_score: int = 0,
        tag: str = None,
    ) -> list[dict]:
        """Read existing memories from B-layer.
        
        Args:
            limit: Max memories to return (default: 1000)
            min_score: Only return memories with score >= min_score
            tag: Filter by tag (optional)
            
        Returns:
            List of memory dicts with keys: id, content, score, tag, created_at, ...
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if tag:
                cursor.execute(
                    """SELECT id, content, content_preview, score, tag, source,
                              source_agent, is_merged, merged_into, created_at, updated_at
                       FROM memories
                       WHERE score >= ? AND tag = ?
                       ORDER BY created_at DESC
                       LIMIT ?""",
                    (min_score, tag, limit)
                )
            else:
                cursor.execute(
                    """SELECT id, content, content_preview, score, tag, source,
                              source_agent, is_merged, merged_into, created_at, updated_at
                       FROM memories
                       WHERE score >= ?
                       ORDER BY created_at DESC
                       LIMIT ?""",
                    (min_score, limit)
                )
            
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to read memories: {e}")
            return []
    
    def get_memory_count(self) -> int:
        """Get total count of memories in B-layer.
        
        Returns:
            int: Total row count
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except sqlite3.Error:
            return 0
    
    def get_memory_by_id(self, memory_id: int) -> Optional[dict]:
        """Get a single memory by ID.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            Memory dict or None if not found
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except sqlite3.Error:
            return None
    
    def content_hash(content: str) -> str:
        """Compute SHA256 hash of content for deduplication logging."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    # ─────────────────────────────────────────────────────────────────
    # Write Operations
    # ─────────────────────────────────────────────────────────────────
    
    def commit_entry(
        self,
        content: str,
        score: int,
        tag: str,
        source_file: str,
        content_preview: str = None,
        is_merged: bool = False,
        merged_into: int = None,
    ) -> Optional[int]:
        """Write a single entry to B-layer.
        
        Args:
            content: Full content text
            score: Priority score (0-100)
            tag: Entry tag (fact/opinion/preference/learning/context)
            source_file: Source file path
            content_preview: First 500 chars (auto-generated if None)
            is_merged: Whether this was merged from dedup
            merged_into: ID of entry it was merged into
            
        Returns:
            int: New row ID, or None on failure
        """
        if content_preview is None:
            content_preview = content[:500]
        
        now = datetime.now(tz=timezone.utc).isoformat()
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO memories
                   (content, content_preview, score, tag, source, source_agent,
                    is_merged, merged_into, created_at, updated_at, last_accessed_at, access_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    content,
                    content_preview,
                    score,
                    tag,
                    source_file,
                    self.agent,
                    int(is_merged),
                    merged_into,
                    now,
                    now,
                    now,
                    0,
                )
            )
            entry_id = cursor.lastrowid
            
            # Log the dreaming action
            cursor.execute(
                """INSERT INTO dreaming_log
                   (entry_content_hash, action, score, merged_into_id, reason, source_file)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    BLayerClient.content_hash(content),
                    "merged" if is_merged else "committed",
                    score,
                    merged_into,
                    f"score={score} tag={tag}",
                    source_file,
                )
            )
            
            conn.commit()
            conn.close()
            logger.debug(f"Committed entry id={entry_id}, score={score}, tag={tag}")
            return entry_id
        except sqlite3.Error as e:
            logger.error(f"Failed to commit entry: {e}")
            return None
    
    def log_action(
        self,
        content: str,
        action: str,
        score: int = None,
        reason: str = None,
        source_file: str = None,
        similarity_score: float = None,
        merged_into_id: int = None,
    ) -> None:
        """Log a dreaming action to the audit log.
        
        Args:
            content: Entry content (hashed for logging)
            action: 'committed'|'archived'|'merged'|'discarded'
            score: Entry score
            reason: Why this action was taken
            source_file: Source file
            similarity_score: Similarity score (for merged entries)
            merged_into_id: ID merged into (for merged entries)
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO dreaming_log
                   (entry_content_hash, action, score, similarity_score,
                    merged_into_id, reason, source_file)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    BLayerClient.content_hash(content),
                    action,
                    score,
                    similarity_score,
                    merged_into_id,
                    reason,
                    source_file,
                )
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to log action: {e}")
    
    # ─────────────────────────────────────────────────────────────────
    # Query Operations
    # ─────────────────────────────────────────────────────────────────
    
    def get_dreaming_log(self, limit: int = 100) -> list[dict]:
        """Read recent entries from the dreaming audit log.
        
        Args:
            limit: Max entries to return
            
        Returns:
            List of log entry dicts
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM dreaming_log ORDER BY ts DESC LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to read dreaming log: {e}")
            return []


# ─────────────────────────────────────────────────────────────────────────────
# Module-level convenience functions
# ─────────────────────────────────────────────────────────────────────────────

_client_cache: Optional[BLayerClient] = None


def get_client(agent: str = "main") -> BLayerClient:
    """Get a cached BLayerClient singleton.
    
    Args:
        agent: Agent name
        
    Returns:
        BLayerClient instance
    """
    global _client_cache
    if _client_cache is None:
        _client_cache = BLayerClient(agent=agent)
    return _client_cache


if __name__ == "__main__":
    client = BLayerClient()
    print(f"DB path: {client.db_path}")
    print(f"Memory count: {client.get_memory_count()}")
