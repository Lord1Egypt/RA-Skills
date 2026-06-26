"""
SQLite数据库管理

建表、连接池、迁移。核心表：
- lecturers: 讲师画像
- lecturer_samples: 样本文案
- knowledge_docs: 知识库文档（FTS5虚拟表）
- knowledge_chunks: 知识库段落（向量索引）
- episodes: 系列文案集
- series_plans: 系列计划
"""

import json
import sqlite3
from pathlib import Path
from typing import Optional

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

SCHEMA_VERSION = 1

SCHEMA_SQL = """
-- 讲师画像主表
CREATE TABLE IF NOT EXISTS lecturers (
    lecturer_id    TEXT PRIMARY KEY,
    lecturer_name  TEXT NOT NULL,
    profile_json   TEXT NOT NULL,        -- 完整profile JSON
    qualitative    TEXT,                 -- 定性分析摘要JSON
    persona_mapping TEXT,               -- 人设映射JSON
    style_dimensions TEXT,              -- 文风五维JSON
    sample_count   INTEGER DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

-- 讲师样本文案
CREATE TABLE IF NOT EXISTS lecturer_samples (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id TEXT NOT NULL REFERENCES lecturers(lecturer_id),
    sample_name TEXT NOT NULL,
    content     TEXT,                     -- 正文（主存储在文件，DB仅冗余备份）
    is_reference INTEGER DEFAULT 0,      -- 是否参考示例
    added_at    TEXT NOT NULL
);

-- 知识库文档（源文件级）
CREATE TABLE IF NOT EXISTS knowledge_docs (
    doc_id      TEXT PRIMARY KEY,        -- 分类/产品/文件名 的组合ID
    category    TEXT NOT NULL,           -- 分类名
    product     TEXT,                    -- 产品名（扁平分类为NULL）
    filename    TEXT NOT NULL,
    layer       TEXT DEFAULT '公共',     -- 公共/私有
    content     TEXT NOT NULL,
    summary     TEXT,                    -- 自动生成的1-2句摘要
    keywords    TEXT,                    -- 关键词JSON数组
    created_at  TEXT NOT NULL
);

-- 知识库段落（用于向量检索，每300字左右切一段）
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id      TEXT NOT NULL REFERENCES knowledge_docs(doc_id),
    chunk_index INTEGER NOT NULL,
    content     TEXT NOT NULL,
    vector_blob BLOB                     -- 768维向量序列化
);

-- 系列计划
CREATE TABLE IF NOT EXISTS series_plans (
    series_id   TEXT PRIMARY KEY,
    lecturer_id TEXT REFERENCES lecturers(lecturer_id),
    title       TEXT NOT NULL,
    plan_json   TEXT NOT NULL,           -- 完整系列计划JSON
    total_episodes INTEGER DEFAULT 0,
    completed   INTEGER DEFAULT 0,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

-- 系列文案集
CREATE TABLE IF NOT EXISTS episodes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id   TEXT NOT NULL REFERENCES series_plans(series_id),
    episode_num INTEGER NOT NULL,
    title       TEXT NOT NULL,
    content     TEXT,                     -- 正文（主存储在文件，DB仅冗余备份）
    summary     TEXT,                    -- 100字摘要（连续性用）
    hook_prev   TEXT,                    -- 上集衔接点
    hook_next   TEXT,                    -- 下集预告点
    word_count  INTEGER DEFAULT 0,
    created_at  TEXT NOT NULL
);

-- 数据库元信息
CREATE TABLE IF NOT EXISTS _meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- FTS5虚拟表（知识库全文检索）
-- 使用unicode61分词器，中文通过预处理（每字插空格）适配
CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
    doc_id,
    category,
    product,
    content,
    summary,
    tokenize='unicode61'
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_samples_lecturer ON lecturer_samples(lecturer_id);
CREATE INDEX IF NOT EXISTS idx_chunks_doc ON knowledge_chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_episodes_series ON episodes(series_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge_docs(category);
"""


def resolve_db_path(db_path: str = None, data_dir: str = None) -> str:
    """
    解析数据库路径。优先级：
    1. db_path 显式指定 → 直接使用
    2. data_dir 指定 → data_dir/aicwos.db
    3. 都未指定 → 报错
    """
    if db_path:
        return db_path
    if data_dir:
        return str(Path(data_dir) / "aicwos.db")
    raise ValueError(
        "必须指定 --data-dir 来确定数据库位置。"
        "数据库路径为 <控制台目录>/aicwos.db"
    )


class DatabaseManager:
    """SQLite数据库管理器"""

    def __init__(self, db_path: str):
        if not db_path:
            raise ValueError(
                "db_path 不能为空。请通过 --data-dir 指定控制台目录，数据库路径为 <控制台目录>/aicwos.db"
            )
        self.db_path = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None

    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        if self._conn is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def initialize(self) -> dict:
        """初始化数据库，建表，返回状态"""
        conn = self.get_connection()
        conn.executescript(SCHEMA_SQL)

        # 迁移：已有数据库添加 layer 列
        try:
            cols = conn.execute("PRAGMA table_info(knowledge_docs)").fetchall()
            col_names = [c[1] for c in cols]
            if "layer" not in col_names:
                conn.execute(
                    "ALTER TABLE knowledge_docs ADD COLUMN layer TEXT DEFAULT '公共'")
                conn.commit()
        except Exception:
            pass

        # 检查/写入schema版本
        row = conn.execute("SELECT value FROM _meta WHERE key='schema_version'").fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO _meta (key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            conn.commit()
            return {"status": "created", "version": SCHEMA_VERSION}
        else:
            return {"status": "exists", "version": int(row["value"])}

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        conn = self.get_connection()
        return conn.execute(sql, params)

    def executemany(self, sql: str, params_list: list) -> sqlite3.Cursor:
        conn = self.get_connection()
        return conn.executemany(sql, params_list)

    def commit(self):
        if self._conn:
            self._conn.commit()

    def query_one(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        return self.execute(sql, params).fetchone()

    def query_all(self, sql: str, params: tuple = ()) -> list:
        return self.execute(sql, params).fetchall()

    def table_exists(self, table_name: str) -> bool:
        row = self.query_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return row is not None

    def get_stats(self) -> dict:
        """获取数据库统计信息"""
        stats = {}
        for table in ["lecturers", "lecturer_samples", "knowledge_docs",
                       "knowledge_chunks", "series_plans", "episodes"]:
            if self.table_exists(table):
                row = self.query_one(f"SELECT COUNT(*) as cnt FROM {table}")
                stats[table] = row["cnt"] if row else 0
        return stats
