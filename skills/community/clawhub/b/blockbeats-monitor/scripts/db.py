# 本文件负责 SQLite 初始化、内容去重入库、关键词匹配关系和日报记录保存。

import hashlib
import json
import sqlite3
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from content_identity import canonical_content_key, pick_representative_record
from keywords import KEYWORD_GROUPS, item_text, match_groups


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references" / "schema.sql"


def connect(db_path):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path):
    """创建表结构，并写入固定关键词组配置。"""
    conn = connect(db_path)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as handle:
        conn.executescript(handle.read())
    now = datetime.now().isoformat()
    for group in KEYWORD_GROUPS:
        conn.execute(
            """
            INSERT INTO keyword_groups (id, name, expression, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              name = excluded.name,
              expression = excluded.expression
            """,
            (group.id, group.name, group.expression, now),
        )
    migrate_canonical_content(conn)
    conn.commit()
    return conn


def make_item_id(item):
    """用归一化内容 key 生成稳定 ID，避免 24h/important 双重入库。"""
    identity = canonical_content_key(item)
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _merge_item_payload(existing, incoming, seen_at):
    """保留代表记录，但缺失字段用另一个版本补齐。"""
    representative = pick_representative_record([existing, incoming])
    fallback = incoming if representative is existing else existing
    return {
        "id": make_item_id(incoming),
        "source": representative.get("source") or fallback.get("source") or "blockbeats",
        "source_type": representative.get("source_type") or fallback.get("source_type") or "",
        "title": representative.get("title") or fallback.get("title") or "",
        "abstract": representative.get("abstract") or fallback.get("abstract") or "",
        "content": representative.get("content") or fallback.get("content") or "",
        "url": representative.get("url") or fallback.get("url") or "",
        "published_at": representative.get("published_at") or fallback.get("published_at"),
        "raw_json": representative.get("raw_json") or fallback.get("raw_json") or json.dumps(representative, ensure_ascii=False),
        "first_seen_at": existing.get("first_seen_at") or seen_at,
        "last_seen_at": seen_at,
    }


def _merge_matched_text(existing_text, incoming_terms):
    terms = set()
    if existing_text:
        terms.update(part.strip() for part in existing_text.split(",") if part.strip())
    terms.update(incoming_terms)
    return ", ".join(sorted(terms))


def upsert_item(conn, item, seen_at):
    item_id = make_item_id(item)
    existing_row = conn.execute("SELECT * FROM source_items WHERE id = ?", (item_id,)).fetchone()
    existing = dict(existing_row) if existing_row else None
    existing_source_row = conn.execute(
        "SELECT * FROM item_sources WHERE item_id = ? AND source_type = ?",
        (item_id, item.get("source_type", "")),
    ).fetchone()
    existing_source = dict(existing_source_row) if existing_source_row else None
    payload = _merge_item_payload(existing, item, seen_at) if existing else {
        "id": item_id,
        "source": item.get("source", "blockbeats"),
        "source_type": item.get("source_type", ""),
        "title": item.get("title", ""),
        "abstract": item.get("abstract", ""),
        "content": item.get("content", ""),
        "url": item.get("url", ""),
        "published_at": item.get("published_at"),
        "raw_json": item.get("raw_json", json.dumps(item, ensure_ascii=False)),
        "first_seen_at": seen_at,
        "last_seen_at": seen_at,
    }
    conn.execute(
        """
        INSERT INTO source_items (
          id, source, source_type, title, abstract, content, url,
          published_at, raw_json, first_seen_at, last_seen_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          source = excluded.source,
          source_type = excluded.source_type,
          title = excluded.title,
          abstract = excluded.abstract,
          content = excluded.content,
          url = excluded.url,
          published_at = excluded.published_at,
          raw_json = excluded.raw_json,
          last_seen_at = excluded.last_seen_at
        """,
        (
            payload["id"],
            payload["source"],
            payload["source_type"],
            payload["title"],
            payload["abstract"],
            payload["content"],
            payload["url"],
            payload["published_at"],
            payload["raw_json"],
            payload["first_seen_at"],
            payload["last_seen_at"],
        ),
    )
    conn.execute(
        """
        INSERT INTO item_sources (item_id, source_type, raw_json, first_seen_at, last_seen_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(item_id, source_type) DO UPDATE SET
          raw_json = excluded.raw_json,
          last_seen_at = excluded.last_seen_at
        """,
        (
            item_id,
            item.get("source_type", ""),
            item.get("raw_json", json.dumps(item, ensure_ascii=False)),
            existing_source.get("first_seen_at") if existing_source else seen_at,
            seen_at,
        ),
    )
    return item_id


def store_items(conn, items, seen_at):
    """入库内容后立即写入关键词匹配关系。"""
    stored_ids = set()
    matched_pairs = set()
    for item in items:
        item_id = upsert_item(conn, item, seen_at)
        stored_ids.add(item_id)
        matches = match_groups(item_text(item))
        for group, terms in matches:
            existing_match = conn.execute(
                "SELECT matched_text FROM item_matches WHERE item_id = ? AND group_id = ?",
                (item_id, group.id),
            ).fetchone()
            conn.execute(
                """
                INSERT OR REPLACE INTO item_matches (item_id, group_id, matched_text, matched_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    item_id,
                    group.id,
                    _merge_matched_text(existing_match["matched_text"] if existing_match else "", set(terms)),
                    seen_at,
                ),
            )
            matched_pairs.add((item_id, group.id))
    conn.commit()
    return {"stored": len(stored_ids), "matched": len(matched_pairs), "source_variants": len(items)}


def rows_to_dicts(rows):
    return [dict(row) for row in rows]


def fetch_matched_items(conn, window_start, window_end):
    """查询窗口内所有命中关键词的内容，并附带命中的关键词组。"""
    rows = conn.execute(
        """
        SELECT
          si.*,
          kg.id AS group_id,
          kg.name AS group_name,
          im.matched_text
        FROM source_items si
        JOIN item_matches im ON im.item_id = si.id
        JOIN keyword_groups kg ON kg.id = im.group_id
        WHERE si.published_at >= ? AND si.published_at < ?
        ORDER BY si.published_at DESC
        """,
        (window_start, window_end),
    ).fetchall()
    return rows_to_dicts(rows)


def save_daily_metric(conn, report_date, window_start, window_end, group_id, mention_count, previous_mention_count):
    conn.execute(
        """
        INSERT INTO daily_keyword_metrics (
          report_date, window_start, window_end, group_id, mention_count, previous_mention_count
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(report_date, group_id) DO UPDATE SET
          window_start = excluded.window_start,
          window_end = excluded.window_end,
          mention_count = excluded.mention_count,
          previous_mention_count = excluded.previous_mention_count
        """,
        (report_date, window_start, window_end, group_id, mention_count, previous_mention_count),
    )


def save_report_run(conn, report_date, window_start, window_end, markdown, telegram_status=None):
    run_id = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO report_runs (
          id, report_date, window_start, window_end, markdown, telegram_status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (run_id, report_date, window_start, window_end, markdown, telegram_status, datetime.now().isoformat()),
    )
    conn.commit()
    return run_id


def migrate_canonical_content(conn):
    """把旧库里按 source_type 拆开的重复内容合并成 canonical 内容。"""
    rows = rows_to_dicts(conn.execute("SELECT * FROM source_items").fetchall())
    if not rows:
        return

    grouped_items = defaultdict(list)
    for row in rows:
        grouped_items[canonical_content_key(row)].append(row)

    match_rows = rows_to_dicts(
        conn.execute(
            """
            SELECT si.*, im.group_id, im.matched_text, im.matched_at
            FROM source_items si
            JOIN item_matches im ON im.item_id = si.id
            """
        ).fetchall()
    )
    grouped_matches = defaultdict(list)
    for row in match_rows:
        grouped_matches[(canonical_content_key(row), row["group_id"])].append(row)

    has_item_sources = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'item_sources'"
    ).fetchone()
    provenance_by_key = defaultdict(list)
    if has_item_sources:
        provenance_rows = rows_to_dicts(
            conn.execute(
                """
                SELECT
                  si.url,
                  si.title,
                  si.published_at,
                  src.source_type,
                  src.raw_json,
                  src.first_seen_at,
                  src.last_seen_at
                FROM item_sources src
                JOIN source_items si ON si.id = src.item_id
                """
            ).fetchall()
        )
        for row in provenance_rows:
            provenance_by_key[canonical_content_key(row)].append(row)

    merged_items = []
    merged_sources = []
    merged_matches = []

    for content_key, item_rows in grouped_items.items():
        representative = pick_representative_record(item_rows)
        canonical_id = make_item_id(representative)
        merged_items.append((
            canonical_id,
            representative.get("source", "blockbeats"),
            representative.get("source_type", ""),
            representative.get("title", ""),
            representative.get("abstract", ""),
            representative.get("content", ""),
            representative.get("url", ""),
            representative.get("published_at"),
            representative.get("raw_json", json.dumps(representative, ensure_ascii=False)),
            min(row.get("first_seen_at") or "" for row in item_rows),
            max(row.get("last_seen_at") or "" for row in item_rows),
        ))
        source_groups = defaultdict(list)
        source_rows_for_key = provenance_by_key.get(content_key) or item_rows
        for row in source_rows_for_key:
            source_groups[row.get("source_type", "")].append(row)
        for source_type, source_rows in source_groups.items():
            chosen = pick_representative_record(source_rows)
            merged_sources.append((
                canonical_id,
                source_type,
                chosen.get("raw_json", json.dumps(chosen, ensure_ascii=False)),
                min(row.get("first_seen_at") or "" for row in source_rows),
                max(row.get("last_seen_at") or "" for row in source_rows),
            ))

    for (content_key, group_id), rows_for_group in grouped_matches.items():
        representative = pick_representative_record(rows_for_group)
        merged_matches.append((
            make_item_id(representative),
            group_id,
            _merge_matched_text("", {
                term.strip()
                for row in rows_for_group
                for term in (row.get("matched_text") or "").split(",")
                if term.strip()
            }),
            max(row.get("matched_at") or "" for row in rows_for_group),
        ))

    conn.execute("DELETE FROM item_matches")
    conn.execute("DELETE FROM item_sources")
    conn.execute("DELETE FROM source_items")

    conn.executemany(
        """
        INSERT INTO source_items (
          id, source, source_type, title, abstract, content, url,
          published_at, raw_json, first_seen_at, last_seen_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        merged_items,
    )
    conn.executemany(
        """
        INSERT INTO item_sources (item_id, source_type, raw_json, first_seen_at, last_seen_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        merged_sources,
    )
    conn.executemany(
        """
        INSERT INTO item_matches (item_id, group_id, matched_text, matched_at)
        VALUES (?, ?, ?, ?)
        """,
        merged_matches,
    )
