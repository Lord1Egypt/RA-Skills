from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "telegraph.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS telegraph_raw_main (
    id INTEGER PRIMARY KEY,
    raw_json TEXT NOT NULL,
    title TEXT,
    brief TEXT,
    content TEXT,
    level TEXT,
    reading_num INTEGER,
    ctime INTEGER,
    modified_time INTEGER,
    shareurl TEXT,
    category TEXT,
    type INTEGER,
    sort_score INTEGER,
    recommend INTEGER,
    confirmed INTEGER,
    jpush INTEGER,
    share_num INTEGER,
    comment_num INTEGER,
    audio_url TEXT,
    tags_json TEXT,
    sub_titles_json TEXT,
    timeline_json TEXT,
    ad_json TEXT,
    assoc_fast_fact_json TEXT,
    assoc_article_url TEXT,
    assoc_video_title TEXT,
    assoc_video_url TEXT,
    assoc_credit_rating_json TEXT,
    stock_list_json TEXT,
    subjects_json TEXT,
    plate_list_json TEXT,
    content_hash TEXT,
    first_seen_at INTEGER,
    last_seen_at INTEGER,
    seen_count INTEGER DEFAULT 1,
    date_key TEXT
);

CREATE TABLE IF NOT EXISTS telegraph_raw_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT,
    source TEXT,
    article_id INTEGER,
    ctime INTEGER,
    modified_time INTEGER,
    content_hash TEXT,
    captured_at INTEGER,
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS telegraph_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER,
    subject_id INTEGER,
    subject_name TEXT,
    attention_num INTEGER,
    plate_id INTEGER,
    channel TEXT,
    captured_at INTEGER,
    UNIQUE(article_id, subject_id)
);

CREATE TABLE IF NOT EXISTS telegraph_stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER,
    secu_code TEXT,
    secu_name TEXT,
    captured_at INTEGER,
    UNIQUE(article_id, secu_code)
);

CREATE TABLE IF NOT EXISTS telegraph_plates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER,
    plate_id INTEGER,
    plate_name TEXT,
    captured_at INTEGER,
    UNIQUE(article_id, plate_id)
);

CREATE VIEW IF NOT EXISTS v_telegraph_main AS
SELECT
    id,
    title,
    brief,
    content,
    level,
    CASE WHEN level IN ('A','B') THEN 1 ELSE 0 END AS is_red,
    CASE WHEN level IN ('A','B') THEN 'red' WHEN level='C' THEN 'normal' ELSE 'unknown' END AS telegraph_type,
    reading_num,
    ctime,
    modified_time,
    datetime(ctime, 'unixepoch', 'localtime') AS published_at,
    shareurl,
    category,
    type,
    sort_score,
    recommend,
    confirmed,
    jpush,
    share_num,
    comment_num,
    audio_url,
    first_seen_at,
    last_seen_at,
    seen_count,
    date_key,
    raw_json
FROM telegraph_raw_main;

CREATE INDEX IF NOT EXISTS idx_raw_main_ctime ON telegraph_raw_main(ctime DESC);
CREATE INDEX IF NOT EXISTS idx_raw_main_level ON telegraph_raw_main(level);
CREATE INDEX IF NOT EXISTS idx_raw_main_reading_num ON telegraph_raw_main(reading_num DESC);
CREATE INDEX IF NOT EXISTS idx_raw_main_date_key ON telegraph_raw_main(date_key);
CREATE INDEX IF NOT EXISTS idx_raw_log_captured_at ON telegraph_raw_log(captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_raw_log_article_id ON telegraph_raw_log(article_id);
CREATE INDEX IF NOT EXISTS idx_subjects_article_id ON telegraph_subjects(article_id);
CREATE INDEX IF NOT EXISTS idx_subjects_subject_id ON telegraph_subjects(subject_id);
CREATE INDEX IF NOT EXISTS idx_stocks_article_id ON telegraph_stocks(article_id);
CREATE INDEX IF NOT EXISTS idx_stocks_secu_code ON telegraph_stocks(secu_code);
CREATE INDEX IF NOT EXISTS idx_plates_article_id ON telegraph_plates(article_id);
CREATE INDEX IF NOT EXISTS idx_plates_plate_id ON telegraph_plates(plate_id);
"""


def ensure_db(db_path: Path | None = None) -> Path:
    path = db_path or DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()
    return path


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = ensure_db(db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def stable_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


def compute_content_hash(data: dict[str, Any]) -> str:
    payload = {
        "title": data.get("title") or "",
        "brief": data.get("brief") or "",
        "content": data.get("content") or "",
        "level": data.get("level") or "",
        "reading_num": data.get("reading_num") or 0,
        "shareurl": data.get("shareurl") or "",
    }
    return hashlib.sha256(stable_json(payload).encode("utf-8")).hexdigest()
