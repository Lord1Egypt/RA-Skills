from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from app.core.settings import Settings


class DatabaseManager:
    """
    SQLite 数据库管理器。
    """

    def __init__(self, settings: Settings) -> None:
        db_file = settings.get("paths", "db_file")
        if not db_file:
            raise ValueError("config.yaml 中未配置 db_file")

        self.db_path = Path(db_file)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """
        初始化数据库表结构。
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS news_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    normalized_title TEXT,
                    source_name TEXT,
                    source_url TEXT UNIQUE,
                    publish_time TEXT,
                    related_companies TEXT,
                    category_level_1 TEXT,
                    category_level_2 TEXT,
                    content_hash TEXT,
                    importance TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS run_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    fetched_count INTEGER DEFAULT 0,
                    valid_count INTEGER DEFAULT 0,
                    deduped_count INTEGER DEFAULT 0,
                    excel_path TEXT,
                    word_path TEXT,
                    status TEXT,
                    error_message TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_news_publish_time ON news_history(publish_time)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_news_title ON news_history(title)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_news_content_hash ON news_history(content_hash)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_news_normalized_title ON news_history(normalized_title)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_news_source_url ON news_history(source_url)"
            )

            conn.commit()