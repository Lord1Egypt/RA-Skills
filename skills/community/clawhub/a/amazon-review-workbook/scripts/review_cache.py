"""SQLite cache for Amazon reviews — persistent storage to avoid re-fetching."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path.cwd() / "amazon-review-output" / "amazon_review_cache.sqlite3"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def ensure_db(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create tables if they don't exist and return connection."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            host TEXT NOT NULL,
            asin TEXT NOT NULL,
            source_url TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            status TEXT NOT NULL DEFAULT 'running',
            current_seen_count INTEGER DEFAULT 0,
            new_review_count INTEGER DEFAULT 0,
            cached_total INTEGER DEFAULT 0,
            stats_json TEXT DEFAULT '[]'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            host TEXT NOT NULL,
            asin TEXT NOT NULL,
            review_id TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            rating_text TEXT NOT NULL DEFAULT '',
            country_date TEXT NOT NULL DEFAULT '',
            review_time TEXT NOT NULL DEFAULT '',
            helpful_votes TEXT NOT NULL DEFAULT '',
            author TEXT NOT NULL DEFAULT '',
            review_link TEXT NOT NULL DEFAULT '',
            source_combo TEXT NOT NULL DEFAULT '',
            first_seen_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            last_job_id TEXT NOT NULL,
            PRIMARY KEY (host, asin, review_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            host TEXT NOT NULL,
            asin TEXT NOT NULL,
            review_id TEXT NOT NULL,
            country TEXT NOT NULL DEFAULT '',
            rating TEXT NOT NULL DEFAULT '',
            review_text TEXT NOT NULL DEFAULT '',
            translated_text TEXT NOT NULL DEFAULT '',
            summary TEXT NOT NULL DEFAULT '',
            sentiment TEXT NOT NULL DEFAULT '',
            categories TEXT NOT NULL DEFAULT '',
            tags TEXT NOT NULL DEFAULT '',
            focus_marks TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL,
            PRIMARY KEY (host, asin, review_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS keyword_history (
            host TEXT NOT NULL,
            asin TEXT NOT NULL,
            keyword TEXT NOT NULL,
            searched_at TEXT NOT NULL,
            new_count INTEGER DEFAULT 0,
            best_new_count INTEGER DEFAULT 0,
            search_count INTEGER DEFAULT 1,
            total_at_search INTEGER DEFAULT 0,
            job_id TEXT NOT NULL,
            PRIMARY KEY (host, asin, keyword)
        )
    """)

    # Schema evolution: add missing columns
    _ensure_column(conn, "reviews", "review_time", "TEXT NOT NULL DEFAULT ''")
    _ensure_column(conn, "reviews", "helpful_votes", "TEXT NOT NULL DEFAULT ''")
    _ensure_column(conn, "reviews", "author", "TEXT NOT NULL DEFAULT ''")
    _ensure_column(conn, "keyword_history", "new_count", "INTEGER DEFAULT 0")
    _ensure_column(conn, "keyword_history", "best_new_count", "INTEGER DEFAULT 0")
    _ensure_column(conn, "keyword_history", "search_count", "INTEGER DEFAULT 1")
    _ensure_column(conn, "keyword_history", "total_at_search", "INTEGER DEFAULT 0")

    conn.commit()
    return conn


def _ensure_column(
    conn: sqlite3.Connection, table: str, column: str, definition: str
) -> None:
    columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def get_known_review_ids(conn: sqlite3.Connection, host: str, asin: str) -> set[str]:
    rows = conn.execute(
        "SELECT review_id FROM reviews WHERE host=? AND asin=?", (host, asin)
    ).fetchall()
    return {row[0] for row in rows}


def get_cached_review_count(conn: sqlite3.Connection, host: str, asin: str) -> int:
    row = conn.execute(
        "SELECT COUNT(*) FROM reviews WHERE host=? AND asin=?", (host, asin)
    ).fetchone()
    return row[0] if row else 0


def get_searched_keywords(conn: sqlite3.Connection, host: str, asin: str) -> set[str]:
    """Return set of keywords already searched for this host+asin."""
    rows = conn.execute(
        "SELECT keyword FROM keyword_history WHERE host=? AND asin=?", (host, asin)
    ).fetchall()
    return {row[0] for row in rows}


def get_keyword_history_map(
    conn: sqlite3.Connection, host: str, asin: str
) -> dict[str, dict[str, Any]]:
    rows = conn.execute(
        """SELECT keyword, searched_at, new_count, best_new_count, search_count, total_at_search, job_id
           FROM keyword_history WHERE host=? AND asin=?""",
        (host, asin),
    ).fetchall()
    return {
        row[0]: {
            "keyword": row[0],
            "searched_at": row[1],
            "new_count": row[2],
            "best_new_count": row[3],
            "search_count": row[4],
            "total_at_search": row[5],
            "job_id": row[6],
        }
        for row in rows
    }


def record_keyword_search(
    conn: sqlite3.Connection,
    host: str,
    asin: str,
    keyword: str,
    job_id: str,
    new_count: int,
    total_count: int,
) -> None:
    """Record that a keyword was searched, with results."""
    now = utc_now()
    conn.execute(
        """INSERT INTO keyword_history (
               host, asin, keyword, searched_at, new_count, best_new_count, search_count, total_at_search, job_id
           )
           VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
           ON CONFLICT(host, asin, keyword) DO UPDATE SET
               searched_at=excluded.searched_at,
               new_count=excluded.new_count,
               best_new_count=MAX(keyword_history.best_new_count, excluded.best_new_count),
               search_count=keyword_history.search_count + 1,
               total_at_search=excluded.total_at_search,
               job_id=excluded.job_id""",
        (host, asin, keyword, now, new_count, new_count, total_count, job_id),
    )
    conn.commit()


def upsert_reviews(
    conn: sqlite3.Connection,
    host: str,
    asin: str,
    job_id: str,
    rows: list[dict[str, Any]],
) -> int:
    """Insert or update reviews. Returns count of NEW reviews."""
    now = utc_now()
    new_count = 0
    for row in rows:
        review_id = row.get("review_id", "")
        if not review_id:
            continue

        exists = conn.execute(
            "SELECT 1 FROM reviews WHERE host=? AND asin=? AND review_id=?",
            (host, asin, review_id),
        ).fetchone()

        if exists:
            conn.execute(
                """UPDATE reviews SET
                    title=?, body=?, rating_text=?, country_date=?,
                    review_time=?, helpful_votes=?, author=?, review_link=?,
                    source_combo=?, last_seen_at=?, last_job_id=?
                    WHERE host=? AND asin=? AND review_id=?""",
                (
                    row.get("title", ""),
                    row.get("body", ""),
                    row.get("rating_text", ""),
                    row.get("country_date", ""),
                    row.get("review_time", ""),
                    row.get("helpful_votes", ""),
                    row.get("author", ""),
                    row.get("review_link", ""),
                    row.get("source_combo", ""),
                    now,
                    job_id,
                    host,
                    asin,
                    review_id,
                ),
            )
        else:
            conn.execute(
                """INSERT INTO reviews (
                    host, asin, review_id, title, body, rating_text,
                    country_date, review_time, helpful_votes, author,
                    review_link, source_combo, first_seen_at, last_seen_at, last_job_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    host,
                    asin,
                    review_id,
                    row.get("title", ""),
                    row.get("body", ""),
                    row.get("rating_text", ""),
                    row.get("country_date", ""),
                    row.get("review_time", ""),
                    row.get("helpful_votes", ""),
                    row.get("author", ""),
                    row.get("review_link", ""),
                    row.get("source_combo", ""),
                    now,
                    now,
                    job_id,
                ),
            )
            new_count += 1

    conn.commit()
    return new_count


def fetch_cached_reviews(
    conn: sqlite3.Connection, host: str, asin: str
) -> list[dict[str, Any]]:
    """Load all cached reviews for this host+asin."""
    rows = conn.execute(
        """SELECT review_id, title, body, rating_text, country_date,
                  review_time, helpful_votes, author, review_link, source_combo,
                  first_seen_at, last_seen_at
           FROM reviews WHERE host=? AND asin=?
           ORDER BY first_seen_at ASC, review_id ASC""",
        (host, asin),
    ).fetchall()

    results = []
    for row in rows:
        results.append(
            {
                "review_id": row[0],
                "title": row[1],
                "body": row[2],
                "rating_text": row[3],
                "country_date": row[4],
                "review_time": row[5],
                "helpful_votes": row[6],
                "author": row[7],
                "review_link": row[8],
                "source_combo": row[9],
                "first_seen_at": row[10],
                "last_seen_at": row[11],
            }
        )
    return results


def upsert_analysis_records(
    conn: sqlite3.Connection,
    host: str,
    asin: str,
    records: list[dict[str, Any]],
) -> int:
    """Insert or update analysis records. Returns count updated."""
    now = utc_now()
    count = 0
    for rec in records:
        review_id = rec.get("review_id", "")
        if not review_id:
            continue
        conn.execute(
            """INSERT INTO analyses (
                host, asin, review_id, country, rating, review_text,
                translated_text, summary, sentiment, categories, tags,
                focus_marks, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(host, asin, review_id) DO UPDATE SET
                country=excluded.country, rating=excluded.rating,
                review_text=excluded.review_text,
                translated_text=excluded.translated_text,
                summary=excluded.summary, sentiment=excluded.sentiment,
                categories=excluded.categories, tags=excluded.tags,
                focus_marks=excluded.focus_marks, updated_at=excluded.updated_at""",
            (
                host,
                asin,
                review_id,
                rec.get("country", ""),
                rec.get("rating", ""),
                rec.get("review_text", ""),
                rec.get("translated_text", ""),
                rec.get("summary", ""),
                rec.get("sentiment", ""),
                rec.get("categories", ""),
                rec.get("tags", ""),
                rec.get("focus_marks", ""),
                now,
            ),
        )
        count += 1
    conn.commit()
    return count


def fetch_cached_analysis_map(
    conn: sqlite3.Connection, host: str, asin: str
) -> dict[str, dict[str, Any]]:
    """Load all analysis records indexed by review_id."""
    rows = conn.execute(
        "SELECT * FROM analyses WHERE host=? AND asin=?", (host, asin)
    ).fetchall()
    col_names = [
        desc[0] for desc in conn.execute("SELECT * FROM analyses LIMIT 1").description
    ]

    result = {}
    for row in rows:
        rec = dict(zip(col_names, row))
        result[rec["review_id"]] = rec
    return result


def create_job(
    conn: sqlite3.Connection,
    job_id: str,
    host: str,
    asin: str,
    source_url: str,
) -> None:
    conn.execute(
        """INSERT INTO jobs (job_id, host, asin, source_url, started_at, status)
           VALUES (?, ?, ?, ?, ?, 'running')""",
        (job_id, host, asin, source_url, utc_now()),
    )
    conn.commit()


def finish_job(
    conn: sqlite3.Connection,
    job_id: str,
    status: str,
    *,
    current_seen_count: int = 0,
    new_review_count: int = 0,
    cached_total: int = 0,
    stats: list[dict[str, Any]] | None = None,
) -> None:
    try:
        conn.execute(
            """UPDATE jobs SET
                finished_at=?, status=?, current_seen_count=?,
                new_review_count=?, cached_total=?, stats_json=?
                WHERE job_id=?""",
            (
                utc_now(),
                status,
                current_seen_count,
                new_review_count,
                cached_total,
                json.dumps(stats or [], ensure_ascii=False),
                job_id,
            ),
        )
        conn.commit()
    except Exception:
        pass  # best-effort, don't mask original error


def cleanup_stale_jobs(conn: sqlite3.Connection, *, max_age_minutes: int = 180) -> int:
    """Mark jobs running longer than max_age_minutes as 'interrupted'."""
    from datetime import timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=max_age_minutes)
    cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    rows = conn.execute(
        "SELECT job_id FROM jobs WHERE status='running' AND started_at < ?",
        (cutoff_str,),
    ).fetchall()
    stale_ids = [row[0] for row in rows]
    if stale_ids:
        conn.executemany(
            "UPDATE jobs SET finished_at=?, status='interrupted' WHERE job_id=?",
            [(utc_now(), jid) for jid in stale_ids],
        )
        conn.commit()
    return len(stale_ids)


def export_analysis_to_records(
    conn: sqlite3.Connection, host: str, asin: str
) -> list[dict[str, Any]]:
    """Export full analysis records (reviews JOIN analyses) for delivery."""
    rows = conn.execute(
        """SELECT r.review_id, r.review_link, r.review_time, r.helpful_votes,
                  r.author, r.country_date, r.rating_text, r.body,
                  a.country, a.rating, a.review_text, a.translated_text,
                  a.summary, a.sentiment, a.categories, a.tags, a.focus_marks
           FROM reviews r
           LEFT JOIN analyses a ON a.host=r.host AND a.asin=r.asin AND a.review_id=r.review_id
           WHERE r.host=? AND r.asin=?
           ORDER BY r.first_seen_at ASC, r.review_id ASC""",
        (host, asin),
    ).fetchall()

    records = []
    for i, row in enumerate(rows, start=1):
        records.append(
            {
                "序号": str(i),
                "评论用户名": row[4] or "",
                "国家": row[8] or "",
                "星级评分": row[9] or (row[6] or ""),
                "评论原文": row[7] or "",
                "评论中文版": row[11] or "",
                "评论概括": row[12] or "",
                "情感倾向": row[13] or "",
                "类别分类": row[14] or "",
                "标签": row[15] or "",
                "重点标记": row[16] or "",
                "评论链接网址": row[1] or "",
                "评论时间": row[2] or "",
                "评论点赞数": row[3] or "",
                "review_id": row[0],
            }
        )
    return records
