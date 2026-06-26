"""Async SQLite database operations for agentMemo v3.0.0 — Connection pooling + optimized PRAGMAs."""
from __future__ import annotations
import asyncio
import gzip
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import aiosqlite

DB_PATH = os.environ.get("AGENTMEMO_DB", os.environ.get("AGENTVAULT_DB", "agentmemo.db"))  # fallback: agentvault.db supported via AGENTVAULT_DB env var
COMPRESS_THRESHOLD = 1024  # gzip text > 1KB

# --- Connection Pool ---
_pool: list[aiosqlite.Connection] = []
_pool_lock: asyncio.Lock | None = None
_POOL_SIZE = int(os.environ.get("AGENTMEMO_POOL_SIZE", os.environ.get("AGENTVAULT_POOL_SIZE", "5")))  # fallback for backward compat
_pool_initialized = False


def _get_pool_lock() -> asyncio.Lock:
    """Lazily create the pool lock in the current event loop."""
    global _pool_lock
    if _pool_lock is None:
        _pool_lock = asyncio.Lock()
    return _pool_lock


def get_db_path() -> str:
    return DB_PATH


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _age_hours(created_at: str) -> float:
    created = datetime.fromisoformat(created_at)
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - created
    return delta.total_seconds() / 3600.0


def effective_importance(importance: float, half_life_hours: float, created_at: str) -> float:
    age = _age_hours(created_at)
    return importance * (0.5 ** (age / half_life_hours))


def _compress_text(text: str) -> tuple[str | bytes, bool]:
    if len(text.encode("utf-8")) > COMPRESS_THRESHOLD:
        return gzip.compress(text.encode("utf-8")), True
    return text, False


def _decompress_text(data: str | bytes, compressed: bool) -> str:
    if compressed and isinstance(data, (bytes, memoryview)):
        return gzip.decompress(bytes(data)).decode("utf-8")
    if isinstance(data, (bytes, memoryview)):
        return bytes(data).decode("utf-8")
    return data


async def _create_connection() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(get_db_path())
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA journal_mode=WAL")
    await conn.execute("PRAGMA foreign_keys=ON")
    await conn.execute("PRAGMA cache_size=10000")
    await conn.execute("PRAGMA mmap_size=268435456")  # 256MB
    await conn.execute("PRAGMA synchronous=NORMAL")
    await conn.execute("PRAGMA temp_store=MEMORY")
    return conn


async def get_connection() -> aiosqlite.Connection:
    """Get a connection from the pool, or create a new one."""
    async with _get_pool_lock():
        if _pool:
            return _pool.pop()
    return await _create_connection()


async def release_connection(conn: aiosqlite.Connection):
    """Return a connection to the pool."""
    async with _get_pool_lock():
        if len(_pool) < _POOL_SIZE:
            _pool.append(conn)
            return
    await conn.close()


class PooledConnection:
    """Async context manager for pooled connections."""
    def __init__(self):
        self.conn: Optional[aiosqlite.Connection] = None

    async def __aenter__(self) -> aiosqlite.Connection:
        self.conn = await get_connection()
        return self.conn

    async def __aexit__(self, *args):
        if self.conn:
            await release_connection(self.conn)


def pooled() -> PooledConnection:
    return PooledConnection()


async def init_db():
    conn = await _create_connection()
    await conn.executescript("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            text BLOB NOT NULL,
            compressed INTEGER NOT NULL DEFAULT 0,
            namespace TEXT NOT NULL DEFAULT 'default',
            importance REAL NOT NULL DEFAULT 0.5,
            half_life_hours REAL NOT NULL DEFAULT 168.0,
            ttl_seconds INTEGER,
            metadata TEXT NOT NULL DEFAULT '{}',
            tags TEXT NOT NULL DEFAULT '[]',
            embedding BLOB,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_memories_namespace ON memories(namespace);
        CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
        CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories(tags);

        CREATE TABLE IF NOT EXISTS memory_versions (
            id TEXT PRIMARY KEY,
            memory_id TEXT NOT NULL,
            text BLOB NOT NULL,
            compressed INTEGER NOT NULL DEFAULT 0,
            namespace TEXT NOT NULL,
            importance REAL NOT NULL,
            tags TEXT NOT NULL DEFAULT '[]',
            metadata TEXT NOT NULL DEFAULT '{}',
            version INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_versions_memory ON memory_versions(memory_id);

        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            payload TEXT NOT NULL DEFAULT '{}',
            namespace TEXT NOT NULL DEFAULT 'default',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_events_namespace ON events(namespace);
        CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at);

        CREATE TABLE IF NOT EXISTS api_keys (
            key TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            namespaces TEXT NOT NULL DEFAULT '["*"]',
            created_at TEXT NOT NULL
        );
    """)
    # Migrate v1 tables
    for stmt in [
        "ALTER TABLE memories ADD COLUMN compressed INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE memories ADD COLUMN tags TEXT NOT NULL DEFAULT '[]'",
        "ALTER TABLE memories ADD COLUMN version INTEGER NOT NULL DEFAULT 1",
    ]:
        try:
            await conn.execute(stmt)
        except Exception:
            pass
    try:
        await conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(id, text, namespace, content=memories, content_rowid=rowid)")
    except Exception:
        pass
    await conn.commit()
    # Pre-fill pool
    async with _get_pool_lock():
        for _ in range(_POOL_SIZE - 1):
            _pool.append(await _create_connection())
    _pool.append(conn)


async def _row_to_memory(row: aiosqlite.Row) -> dict:
    d = dict(row)
    text_data = d["text"]
    compressed = bool(d.get("compressed", 0))
    d["text"] = _decompress_text(text_data, compressed)
    d["metadata"] = json.loads(d["metadata"]) if isinstance(d["metadata"], str) else d["metadata"]
    d["tags"] = json.loads(d["tags"]) if isinstance(d["tags"], str) else d.get("tags", [])
    d["age_hours"] = _age_hours(d["created_at"])
    d["effective_importance"] = effective_importance(d["importance"], d["half_life_hours"], d["created_at"])
    d.pop("compressed", None)
    return d


async def create_memory(text: str, namespace: str, importance: float, half_life_hours: float,
                        ttl_seconds: Optional[int], metadata: dict, embedding: bytes,
                        tags: list[str] | None = None) -> dict:
    mid = str(uuid.uuid4())
    now = _now_iso()
    stored_text, compressed = _compress_text(text)
    tags_json = json.dumps(tags or [])
    async with pooled() as conn:
        await conn.execute(
            "INSERT INTO memories (id, text, compressed, namespace, importance, half_life_hours, ttl_seconds, metadata, tags, embedding, version, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (mid, stored_text, int(compressed), namespace, importance, half_life_hours, ttl_seconds,
             json.dumps(metadata), tags_json, embedding, 1, now)
        )
        try:
            await conn.execute("INSERT INTO memories_fts(id, text, namespace) VALUES (?,?,?)", (mid, text, namespace))
        except Exception:
            pass
        await conn.commit()
    return {"id": mid, "created_at": now}


async def batch_create_memories(items: list[dict]) -> list[dict]:
    """Create multiple memories in a single transaction for performance."""
    results = []
    now = _now_iso()
    async with pooled() as conn:
        for item in items:
            mid = str(uuid.uuid4())
            stored_text, compressed = _compress_text(item["text"])
            tags_json = json.dumps(item.get("tags") or [])
            await conn.execute(
                "INSERT INTO memories (id, text, compressed, namespace, importance, half_life_hours, ttl_seconds, metadata, tags, embedding, version, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (mid, stored_text, int(compressed), item["namespace"], item["importance"],
                 item.get("half_life_hours", 168.0), item.get("ttl_seconds"),
                 json.dumps(item.get("metadata", {})), tags_json, item["embedding"], 1, now)
            )
            try:
                await conn.execute("INSERT INTO memories_fts(id, text, namespace) VALUES (?,?,?)",
                                   (mid, item["text"], item["namespace"]))
            except Exception:
                pass
            results.append({"id": mid, "created_at": now})
        await conn.commit()
    return results


async def get_memory(mid: str) -> Optional[dict]:
    async with pooled() as conn:
        row = await conn.execute("SELECT * FROM memories WHERE id=?", (mid,))
        row = await row.fetchone()
    if not row:
        return None
    return await _row_to_memory(row)


async def update_memory(mid: str, text: Optional[str] = None, importance: Optional[float] = None,
                        ttl_seconds: Optional[int] = None, metadata: Optional[dict] = None,
                        half_life_hours: Optional[float] = None, tags: Optional[list[str]] = None,
                        new_embedding: Optional[bytes] = None) -> Optional[dict]:
    async with pooled() as conn:
        row = await conn.execute("SELECT * FROM memories WHERE id=?", (mid,))
        row = await row.fetchone()
        if not row:
            return None
        old = dict(row)
        old_text = _decompress_text(old["text"], bool(old.get("compressed", 0)))

        # Save current version to history
        version_id = str(uuid.uuid4())
        await conn.execute(
            "INSERT INTO memory_versions (id, memory_id, text, compressed, namespace, importance, tags, metadata, version, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (version_id, mid, old["text"], old.get("compressed", 0), old["namespace"], old["importance"],
             old.get("tags", "[]"), old["metadata"], old.get("version", 1), _now_iso())
        )

        new_text = text if text is not None else old_text
        new_importance = importance if importance is not None else old["importance"]
        new_ttl = ttl_seconds if ttl_seconds is not None else old["ttl_seconds"]
        new_metadata = json.dumps(metadata) if metadata is not None else old["metadata"]
        new_half_life = half_life_hours if half_life_hours is not None else old["half_life_hours"]
        new_tags = json.dumps(tags) if tags is not None else old.get("tags", "[]")
        new_version = old.get("version", 1) + 1
        stored_text, compressed = _compress_text(new_text)
        emb = new_embedding if new_embedding is not None else old["embedding"]

        await conn.execute(
            "UPDATE memories SET text=?, compressed=?, importance=?, ttl_seconds=?, metadata=?, half_life_hours=?, tags=?, embedding=?, version=? WHERE id=?",
            (stored_text, int(compressed), new_importance, new_ttl, new_metadata, new_half_life, new_tags, emb, new_version, mid)
        )
        try:
            await conn.execute("DELETE FROM memories_fts WHERE id=?", (mid,))
            await conn.execute("INSERT INTO memories_fts(id, text, namespace) VALUES (?,?,?)", (mid, new_text, old["namespace"]))
        except Exception:
            pass
        await conn.commit()
    return await get_memory(mid)


async def get_memory_versions(mid: str) -> list[dict]:
    async with pooled() as conn:
        rows = await conn.execute(
            "SELECT * FROM memory_versions WHERE memory_id=? ORDER BY version DESC", (mid,))
        rows = await rows.fetchall()
    results = []
    for row in rows:
        d = dict(row)
        d["text"] = _decompress_text(d["text"], bool(d.get("compressed", 0)))
        d["tags"] = json.loads(d["tags"]) if isinstance(d["tags"], str) else d.get("tags", [])
        d["metadata"] = json.loads(d["metadata"]) if isinstance(d["metadata"], str) else d["metadata"]
        d.pop("compressed", None)
        results.append(d)
    return results


async def rollback_memory(mid: str, target_version: Optional[int] = None) -> Optional[dict]:
    async with pooled() as conn:
        if target_version:
            row = await conn.execute(
                "SELECT * FROM memory_versions WHERE memory_id=? AND version=?", (mid, target_version))
        else:
            row = await conn.execute(
                "SELECT * FROM memory_versions WHERE memory_id=? ORDER BY version DESC LIMIT 1", (mid,))
        row = await row.fetchone()
    if not row:
        return None
    ver = dict(row)
    text = _decompress_text(ver["text"], bool(ver.get("compressed", 0)))
    tags = json.loads(ver["tags"]) if isinstance(ver["tags"], str) else ver.get("tags", [])
    metadata = json.loads(ver["metadata"]) if isinstance(ver["metadata"], str) else ver["metadata"]
    from embeddings import embed_text
    new_emb = embed_text(text)
    return await update_memory(mid, text=text, importance=ver["importance"],
                               metadata=metadata, tags=tags, new_embedding=new_emb)


async def delete_memory(mid: str) -> bool:
    async with pooled() as conn:
        cur = await conn.execute("DELETE FROM memories WHERE id=?", (mid,))
        try:
            await conn.execute("DELETE FROM memories_fts WHERE id=?", (mid,))
        except Exception:
            pass
        await conn.commit()
        return cur.rowcount > 0


async def get_all_memories(namespace: Optional[str] = None, tags: Optional[list[str]] = None,
                           cursor: Optional[str] = None, limit: int = 1000) -> tuple[list[dict], Optional[str]]:
    conditions = []
    params: list[Any] = []

    if namespace:
        conditions.append("namespace=?")
        params.append(namespace)
    if cursor:
        import base64
        decoded = base64.b64decode(cursor).decode()
        cursor_ts, cursor_id = decoded.rsplit("|", 1)
        conditions.append("(created_at < ? OR (created_at = ? AND id < ?))")
        params.extend([cursor_ts, cursor_ts, cursor_id])
    # SQL-side tag filtering via json_each (SQLite JSON1 extension, always available)
    if tags:
        placeholders = ",".join("?" * len(tags))
        conditions.append(
            f"EXISTS (SELECT 1 FROM json_each(memories.tags) WHERE value IN ({placeholders}))"
        )
        params.extend(tags)

    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT * FROM memories{where} ORDER BY created_at DESC, id DESC LIMIT ?"
    params.append(limit + 1)

    async with pooled() as conn:
        rows = await conn.execute(query, params)
        rows = await rows.fetchall()

    results = []
    for row in rows[:limit]:
        mem = await _row_to_memory(row)
        results.append(mem)

    next_cursor = None
    if len(rows) > limit:
        import base64
        last = dict(rows[limit - 1])
        next_cursor = base64.b64encode(f"{last['created_at']}|{last['id']}".encode()).decode()

    return results, next_cursor


async def count_memories(namespace: Optional[str] = None) -> int:
    async with pooled() as conn:
        if namespace:
            row = await conn.execute("SELECT COUNT(*) as c FROM memories WHERE namespace=?", (namespace,))
        else:
            row = await conn.execute("SELECT COUNT(*) as c FROM memories")
        row = await row.fetchone()
    return row["c"]


async def keyword_search(query: str, namespace: Optional[str] = None, limit: int = 10) -> list[dict]:
    async with pooled() as conn:
        try:
            if namespace:
                rows = await conn.execute(
                    "SELECT id, rank FROM memories_fts WHERE memories_fts MATCH ? AND namespace=? ORDER BY rank LIMIT ?",
                    (query, namespace, limit))
            else:
                rows = await conn.execute(
                    "SELECT id, rank FROM memories_fts WHERE memories_fts MATCH ? ORDER BY rank LIMIT ?",
                    (query, limit))
            rows = await rows.fetchall()
        except Exception:
            return []

    results = []
    for row in rows:
        mem = await get_memory(row["id"])
        if mem:
            results.append(mem)
    return results


async def prune_expired() -> int:
    """Prune TTL-expired and importance-decayed memories using SQL-side filtering for efficiency."""
    async with pooled() as conn:
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        now_ts = now.timestamp()

        # TTL-expired: prune directly in SQL using datetime arithmetic
        # SQLite stores created_at as ISO string; compute expiry as created_at + ttl_seconds
        ttl_cur = await conn.execute(
            """SELECT id FROM memories
               WHERE ttl_seconds IS NOT NULL
               AND (unixepoch(created_at) + ttl_seconds) < unixepoch(?)""",
            (now_iso,)
        )
        ttl_expired = [r["id"] for r in await ttl_cur.fetchall()]

        # Importance decay: pre-filter in SQL to candidates with low base importance or old age,
        # then do precise math in Python on the small candidate set only.
        # Decay: importance * 0.5^(age_hours / half_life_hours) < 0.01
        # => age_hours > half_life_hours * log2(importance / 0.01)
        # Conservative pre-filter: importance < 0.5 AND age > 24 hours
        decay_candidates_cur = await conn.execute(
            """SELECT id, importance, half_life_hours, created_at FROM memories
               WHERE importance < 0.99
               AND unixepoch(created_at) < unixepoch(?) - 3600""",
            (now_iso,)
        )
        decay_candidates = await decay_candidates_cur.fetchall()
        decay_expired = []
        for row in decay_candidates:
            eff = effective_importance(row["importance"], row["half_life_hours"], row["created_at"])
            if eff < 0.01:
                decay_expired.append(row["id"])

        to_delete = list(set(ttl_expired + decay_expired))
        if to_delete:
            await conn.executemany("DELETE FROM memories WHERE id=?", [(i,) for i in to_delete])
            for mid in to_delete:
                try:
                    await conn.execute("DELETE FROM memories_fts WHERE id=?", (mid,))
                except Exception:
                    pass
            await conn.commit()
    return len(to_delete)


async def create_event(type_: str, payload: dict, namespace: str) -> dict:
    eid = str(uuid.uuid4())
    now = _now_iso()
    async with pooled() as conn:
        await conn.execute(
            "INSERT INTO events (id, type, payload, namespace, created_at) VALUES (?,?,?,?,?)",
            (eid, type_, json.dumps(payload), namespace, now)
        )
        await conn.commit()
    return {"id": eid, "type": type_, "payload": payload, "namespace": namespace, "created_at": now}


async def get_recent_events(limit: int = 50, namespace: Optional[str] = None) -> list[dict]:
    async with pooled() as conn:
        if namespace:
            rows = await conn.execute("SELECT * FROM events WHERE namespace=? ORDER BY created_at DESC LIMIT ?", (namespace, limit))
        else:
            rows = await conn.execute("SELECT * FROM events ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = await rows.fetchall()
    return [dict(r) | {"payload": json.loads(r["payload"])} for r in rows]


async def get_namespaces() -> list[dict]:
    async with pooled() as conn:
        mem_rows = await conn.execute("SELECT namespace, COUNT(*) as cnt FROM memories GROUP BY namespace")
        mem_counts = {r["namespace"]: r["cnt"] for r in await mem_rows.fetchall()}
        evt_rows = await conn.execute("SELECT namespace, COUNT(*) as cnt FROM events GROUP BY namespace")
        evt_counts = {r["namespace"]: r["cnt"] for r in await evt_rows.fetchall()}
    all_ns = set(mem_counts.keys()) | set(evt_counts.keys())
    return [{"namespace": ns, "memory_count": mem_counts.get(ns, 0), "event_count": evt_counts.get(ns, 0)} for ns in sorted(all_ns)]


async def get_stats() -> dict:
    async with pooled() as conn:
        mem_count = (await (await conn.execute("SELECT COUNT(*) as c FROM memories")).fetchone())["c"]
        evt_count = (await (await conn.execute("SELECT COUNT(*) as c FROM events")).fetchone())["c"]
        mem_ns = await (await conn.execute("SELECT DISTINCT namespace FROM memories")).fetchall()
        evt_ns = await (await conn.execute("SELECT DISTINCT namespace FROM events")).fetchall()
    ns_count = len(set([r["namespace"] for r in mem_ns] + [r["namespace"] for r in evt_ns]))
    db_path = get_db_path()
    size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    if size < 1024:
        human = f"{size} B"
    elif size < 1024**2:
        human = f"{size/1024:.1f} KB"
    else:
        human = f"{size/1024**2:.1f} MB"
    return {"total_memories": mem_count, "total_events": evt_count, "total_namespaces": ns_count,
            "storage_size_bytes": size, "storage_size_human": human}


# --- API Key Management ---

async def create_api_key(name: str, namespaces: list[str]) -> dict:
    import secrets
    key = "avk_" + secrets.token_urlsafe(32)
    now = _now_iso()
    async with pooled() as conn:
        await conn.execute("INSERT INTO api_keys (key, name, namespaces, created_at) VALUES (?,?,?,?)",
                           (key, name, json.dumps(namespaces), now))
        await conn.commit()
    return {"key": key, "name": name, "namespaces": namespaces, "created_at": now}


async def get_api_key(key: str) -> Optional[dict]:
    async with pooled() as conn:
        row = await conn.execute("SELECT * FROM api_keys WHERE key=?", (key,))
        row = await row.fetchone()
    if not row:
        return None
    d = dict(row)
    d["namespaces"] = json.loads(d["namespaces"])
    return d


async def list_api_keys() -> list[dict]:
    async with pooled() as conn:
        rows = await conn.execute("SELECT * FROM api_keys ORDER BY created_at DESC")
        rows = await rows.fetchall()
    return [dict(r) | {"namespaces": json.loads(r["namespaces"])} for r in rows]


async def delete_api_key(key: str) -> bool:
    async with pooled() as conn:
        cur = await conn.execute("DELETE FROM api_keys WHERE key=?", (key,))
        await conn.commit()
        return cur.rowcount > 0


async def export_memories(namespace: Optional[str] = None) -> list[dict]:
    async with pooled() as conn:
        if namespace:
            rows = await conn.execute("SELECT * FROM memories WHERE namespace=? ORDER BY created_at", (namespace,))
        else:
            rows = await conn.execute("SELECT * FROM memories ORDER BY created_at")
        rows = await rows.fetchall()
    results = []
    for row in rows:
        d = await _row_to_memory(row)
        d.pop("embedding", None)
        d.pop("age_hours", None)
        d.pop("effective_importance", None)
        results.append(d)
    return results
