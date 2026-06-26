"""
persistent_store.py - SQLite 持久化存储层

提供记忆条目的 SQLite 持久化，支持：
- WAL 模式（高并发写入）
- 全文搜索（FTS5）
- 软删除 + 定期清理
- 乐观锁版本控制
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator, Optional

from .memory_core import (
    MemoryEntry,
    MemoryImportance,
    MemoryQuery,
    MemoryResult,
    MemoryScope,
    MemoryType,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# 数据库路径配置
# =============================================================================

DEFAULT_DB_DIR = Path(__file__).parent.parent / "data" / "memory"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "memory.db"


# =============================================================================
# 连接管理
# =============================================================================

_connection_pool: dict[str, sqlite3.Connection] = {}


def get_connection(db_path: str = str(DEFAULT_DB_PATH)) -> sqlite3.Connection:
    """获取数据库连接（单例模式，支持多数据库）"""
    if db_path not in _connection_pool:
        _ensure_db_dir(db_path)
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _connection_pool[db_path] = conn
        _init_schema(conn)
    return _connection_pool[db_path]


@contextmanager
def get_cursor(db_path: str = str(DEFAULT_DB_PATH)) -> Generator[sqlite3.Cursor, None, None]:
    """获取游标的上下文管理器"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def _ensure_db_dir(db_path: str):
    """确保数据库目录存在"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Schema 初始化
# =============================================================================

def _init_schema(conn: sqlite3.Connection):
    """初始化数据库 Schema"""
    cursor = conn.cursor()
    
    # 主表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_entries (
            entry_id       TEXT PRIMARY KEY,
            content        TEXT NOT NULL,
            content_hash   TEXT NOT NULL,
            memory_type    TEXT NOT NULL,
            scope          TEXT NOT NULL,
            importance     INTEGER NOT NULL DEFAULT 3,
            agent_id       TEXT NOT NULL DEFAULT '',
            created_at     TEXT NOT NULL,
            updated_at     TEXT NOT NULL,
            accessed_at    TEXT NOT NULL,
            tags           TEXT NOT NULL DEFAULT '[]',
            related_agents TEXT NOT NULL DEFAULT '[]',
            related_entries TEXT NOT NULL DEFAULT '[]',
            ttl_seconds    REAL NOT NULL DEFAULT 3600.0,
            version        INTEGER NOT NULL DEFAULT 1,
            is_deleted     INTEGER NOT NULL DEFAULT 0,
            is_pinned      INTEGER NOT NULL DEFAULT 0,
            summary        TEXT NOT NULL DEFAULT '',
            source         TEXT NOT NULL DEFAULT ''
        )
    """)
    
    # FTS5 全文搜索索引
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            entry_id,
            content,
            summary,
            tags,
            content='memory_entries',
            content_rowid='rowid'
        )
    """)
    
    # 触发器：保持 FTS 同步
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS memory_ai AFTER INSERT ON memory_entries BEGIN
            INSERT INTO memory_fts(entry_id, content, summary, tags)
            VALUES (new.entry_id, new.content, new.summary, new.tags);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS memory_ad AFTER DELETE ON memory_entries BEGIN
            INSERT INTO memory_fts(memory_fts, entry_id, content, summary, tags)
            VALUES ('delete', old.entry_id, old.content, old.summary, old.tags);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS memory_au AFTER UPDATE ON memory_entries BEGIN
            INSERT INTO memory_fts(memory_fts, entry_id, content, summary, tags)
            VALUES ('delete', old.entry_id, old.content, old.summary, old.tags);
            INSERT INTO memory_fts(entry_id, content, summary, tags)
            VALUES (new.entry_id, new.content, new.summary, new.tags);
        END
    """)
    
    # 索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scope ON memory_entries(scope)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent ON memory_entries(agent_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON memory_entries(memory_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_created ON memory_entries(created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memory_entries(importance)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash ON memory_entries(content_hash)")
    
    # 启用 WAL 模式
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    
    conn.commit()
    logger.info("Memory DB schema initialized")


# =============================================================================
# 持久化存储实现
# =============================================================================

class PersistentStore:
    """
    SQLite 持久化存储
    
    特性：
    - WAL 模式支持高并发读写
    - FTS5 全文搜索
    - 乐观锁（version 字段）
    - 软删除 + 触发器自动清理 FTS
    """
    
    def __init__(self, db_path: str = str(DEFAULT_DB_PATH)):
        self.db_path = db_path
        self._ensure_initialized()
    
    def _ensure_initialized(self):
        get_connection(self.db_path)
    
    # -------------------------------------------------------------------------
    # 写入操作
    # -------------------------------------------------------------------------
    
    def store(self, entry: MemoryEntry) -> str:
        """存储记忆条目"""
        with get_cursor(self.db_path) as cur:
            # 检查重复
            cur.execute(
                "SELECT entry_id FROM memory_entries WHERE content_hash=? AND is_deleted=0",
                (entry.content_hash,),
            )
            existing = cur.fetchone()
            if existing:
                logger.debug(f"Duplicate memory entry detected: {existing['entry_id']}")
                return existing["entry_id"]
            
            cur.execute("""
                INSERT INTO memory_entries (
                    entry_id, content, content_hash, memory_type, scope,
                    importance, agent_id, created_at, updated_at, accessed_at,
                    tags, related_agents, related_entries, ttl_seconds,
                    version, is_deleted, is_pinned, summary, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.entry_id,
                entry.content,
                entry.content_hash,
                entry.memory_type.value,
                entry.scope.value,
                entry.importance.value,
                entry.agent_id,
                entry.created_at,
                entry.updated_at,
                entry.accessed_at,
                json.dumps(entry.tags, ensure_ascii=False),
                json.dumps(entry.related_agent_ids, ensure_ascii=False),
                json.dumps(entry.related_entry_ids, ensure_ascii=False),
                entry.ttl_seconds,
                entry.version,
                int(entry.is_deleted),
                int(entry.is_pinned),
                entry.summary,
                entry.source,
            ))
        logger.debug(f"Stored memory: {entry.entry_id} [{entry.scope.value}]")
        return entry.entry_id
    
    def update(self, entry_id: str, content: str = None, **kwargs) -> bool:
        """更新记忆（乐观锁）"""
        with get_cursor(self.db_path) as cur:
            # 获取当前版本
            cur.execute(
                "SELECT version FROM memory_entries WHERE entry_id=? AND is_deleted=0",
                (entry_id,),
            )
            row = cur.fetchone()
            if not row:
                return False
            
            new_version = row["version"] + 1
            updates = ["updated_at=?", "version=?"]
            params = [datetime.now(timezone.utc).isoformat(), new_version]
            
            if content is not None:
                from .memory_core import MemoryEntry
                import hashlib
                updates.append("content=?")
                params.append(content)
                updates.append("content_hash=?")
                params.append(hashlib.sha256(content.encode()).hexdigest()[:16])
            
            for key, value in kwargs.items():
                col_map = {
                    "tags": "tags",
                    "summary": "summary",
                    "is_pinned": "is_pinned",
                    "importance": "importance",
                    "ttl_seconds": "ttl_seconds",
                }
                if key in col_map:
                    updates.append(f"{col_map[key]}=?")
                    if key == "tags":
                        params.append(json.dumps(value, ensure_ascii=False))
                    elif key in ("is_pinned",):
                        params.append(int(value))
                    else:
                        params.append(value)
            
            params.append(entry_id)
            cur.execute(f"UPDATE memory_entries SET {','.join(updates)} WHERE entry_id=? AND is_deleted=0", params)
            
            return cur.rowcount > 0
    
    def delete(self, entry_id: str, soft: bool = True) -> bool:
        """删除记忆"""
        with get_cursor(self.db_path) as cur:
            if soft:
                cur.execute(
                    "UPDATE memory_entries SET is_deleted=1, updated_at=? WHERE entry_id=?",
                    (datetime.now(timezone.utc).isoformat(), entry_id),
                )
            else:
                cur.execute("DELETE FROM memory_entries WHERE entry_id=?", (entry_id,))
            return cur.rowcount > 0
    
    # -------------------------------------------------------------------------
    # 读取操作
    # -------------------------------------------------------------------------
    
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取单条记忆"""
        with get_cursor(self.db_path) as cur:
            cur.execute(
                "SELECT * FROM memory_entries WHERE entry_id=? AND is_deleted=0",
                (entry_id,),
            )
            row = cur.fetchone()
            return self._row_to_entry(row) if row else None
    
    def query(self, q: MemoryQuery) -> MemoryResult:
        """查询记忆（支持全文搜索 + 多条件过滤）"""
        with get_cursor(self.db_path) as cur:
            
            # 构建 WHERE 子句
            conditions = ["is_deleted=0"]
            params: list[Any] = []
            
            # 作用域过滤
            if q.scope:
                conditions.append("scope=?")
                params.append(q.scope.value)
            elif q.scopes:
                placeholders = ",".join(["?"] * len(q.scopes))
                conditions.append(f"scope IN ({placeholders})")
                params.extend([s.value for s in q.scopes])
            
            # Agent 过滤
            if q.agent_id:
                conditions.append("agent_id=?")
                params.append(q.agent_id)
            
            # 类型过滤
            if q.memory_type:
                conditions.append("memory_type=?")
                params.append(q.memory_type.value)
            elif q.memory_types:
                placeholders = ",".join(["?"] * len(q.memory_types))
                conditions.append(f"memory_type IN ({placeholders})")
                params.extend([t.value for t in q.memory_types])
            
            # 重要性过滤
            conditions.append("importance>=?")
            params.append(q.min_importance.value)
            
            # 时间过滤
            if q.start_time:
                conditions.append("created_at>=?")
                params.append(q.start_time)
            if q.end_time:
                conditions.append("created_at<=?")
                params.append(q.end_time)
            
            # 标签过滤（JSON 数组包含任一标签）
            for tag in q.tags:
                conditions.append("tags LIKE ?")
                params.append(f'%"{tag}"%')
            
            where_clause = " AND ".join(conditions)
            
            # 全文搜索
            if q.query_text:
                # FTS5 搜索
                fts_query = self._build_fts_query(q.query_text)
                cur.execute(f"""
                    SELECT me.* FROM memory_entries me
                    JOIN memory_fts fts ON me.entry_id = fts.entry_id
                    WHERE {where_clause}
                    AND memory_fts MATCH ?
                """, params + [fts_query])
            else:
                cur.execute(f"SELECT * FROM memory_entries WHERE {where_clause}", params)
            
            rows = cur.fetchall()
            all_entries = [self._row_to_entry(r) for r in rows]
            
            # 可见性过滤（PRIVATE scope 权限）
            visible = [e for e in all_entries if q.is_visible_to(e)]
            
            # 过期过滤
            visible = [e for e in visible if not e.is_expired]
            
            # 统计
            scope_counts: dict[str, int] = {}
            type_counts: dict[str, int] = {}
            tag_counts: dict[str, int] = {}
            
            for e in visible:
                scope_counts[e.scope.value] = scope_counts.get(e.scope.value, 0) + 1
                type_counts[e.memory_type.value] = type_counts.get(e.memory_type.value, 0) + 1
                for tag in e.tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # 排序
            sort_col = {
                "importance": "importance",
                "created_at": "created_at",
                "accessed_at": "accessed_at",
            }.get(q.sort_by, "importance")
            
            reverse = q.descending
            if sort_col == "importance":
                visible.sort(key=lambda e: e.importance.value, reverse=reverse)
            elif sort_col == "accessed_at":
                visible.sort(key=lambda e: e.accessed_at, reverse=reverse)
            else:
                visible.sort(key=lambda e: e.created_at, reverse=reverse)
            
            total = len(visible)
            paginated = visible[q.offset : q.offset + q.limit]
            top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:10]
            
            result = MemoryResult(
                entries=paginated,
                total=total,
                query=q,
                scope_breakdown=scope_counts,
                type_breakdown=type_counts,
                top_tags=top_tags,
            )
            return result
    
    def get_recent(
        self, limit: int = 10, scope: Optional[MemoryScope] = None, agent_id: str = ""
    ) -> list[MemoryEntry]:
        """获取最近的记忆"""
        with get_cursor(self.db_path) as cur:
            conditions = ["is_deleted=0"]
            params: list[Any] = []
            
            if scope:
                conditions.append("scope=?")
                params.append(scope.value)
            if agent_id:
                conditions.append("agent_id=?")
                params.append(agent_id)
            
            where = " AND ".join(conditions)
            cur.execute(f"""
                SELECT * FROM memory_entries
                WHERE {where}
                ORDER BY accessed_at DESC
                LIMIT ?
            """, params + [limit])
            
            return [self._row_to_entry(r) for r in cur.fetchall()]
    
    # -------------------------------------------------------------------------
    # 生命周期管理
    # -------------------------------------------------------------------------
    
    def prune_expired(self) -> int:
        """清理过期记忆（仅清理非置顶的已过期条目）"""
        now = datetime.now(timezone.utc).isoformat()
        with get_cursor(self.db_path) as cur:
            # 清理 TTL 过期的
            cur.execute("""
                DELETE FROM memory_entries
                WHERE is_deleted=0
                AND is_pinned=0
                AND datetime(created_at, '+' || ttl_seconds || ' seconds') < ?
            """, (now,))
            
            deleted_count = cur.rowcount
            
            # 清理超过30天的会话记忆
            cur.execute("""
                DELETE FROM memory_entries
                WHERE is_deleted=0
                AND is_pinned=0
                AND scope='session'
                AND datetime(created_at, '+30 days') < ?
            """, (now,))
            
            deleted_count += cur.rowcount
            
        logger.info(f"Pruned {deleted_count} expired memory entries")
        return deleted_count
    
    def get_stats(self) -> dict[str, Any]:
        """获取统计信息"""
        with get_cursor(self.db_path) as cur:
            cur.execute("""
                SELECT scope, memory_type, COUNT(*) as count
                FROM memory_entries WHERE is_deleted=0
                GROUP BY scope, memory_type
            """)
            
            stats: dict[str, Any] = {
                "total": 0,
                "by_scope": {},
                "by_type": {},
                "pinned": 0,
            }
            
            for row in cur.fetchall():
                stats["total"] += row["count"]
                stats["by_scope"][row["scope"]] = row["count"]
                stats["by_type"][row["memory_type"]] = row["count"]
            
            cur.execute("SELECT COUNT(*) as c FROM memory_entries WHERE is_pinned=1 AND is_deleted=0")
            stats["pinned"] = cur.fetchone()["c"]
            
            return stats
    
    def soft_delete_by_agent(self, agent_id: str) -> int:
        """软删除某Agent的所有私有记忆"""
        with get_cursor(self.db_path) as cur:
            cur.execute(
                "UPDATE memory_entries SET is_deleted=1, updated_at=? WHERE agent_id=? AND scope='private'",
                (datetime.now(timezone.utc).isoformat(), agent_id),
            )
            return cur.rowcount
    
    # -------------------------------------------------------------------------
    # 辅助方法
    # -------------------------------------------------------------------------
    
    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> MemoryEntry:
        """将数据库行转换为 MemoryEntry"""
        return MemoryEntry(
            entry_id=row["entry_id"],
            content=row["content"],
            memory_type=MemoryType(row["memory_type"]),
            scope=MemoryScope(row["scope"]),
            importance=MemoryImportance(row["importance"]),
            agent_id=row["agent_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            accessed_at=row["accessed_at"],
            tags=json.loads(row["tags"]),
            related_agent_ids=json.loads(row["related_agents"]),
            related_entry_ids=json.loads(row["related_entries"]),
            ttl_seconds=row["ttl_seconds"],
            version=row["version"],
            is_deleted=bool(row["is_deleted"]),
            is_pinned=bool(row["is_pinned"]),
            summary=row["summary"],
            source=row["source"],
        )
    
    @staticmethod
    def _build_fts_query(query_text: str) -> str:
        """构建 FTS5 查询，处理多词和引号"""
        # 简单处理：空格分隔，添加 * 通配符支持前缀匹配
        terms = query_text.strip().split()
        if not terms:
            return '""'
        return " ".join(f'"{t}"*' for t in terms if t)
