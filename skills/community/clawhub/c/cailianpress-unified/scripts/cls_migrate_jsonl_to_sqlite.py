#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from db import compute_content_hash, get_connection, stable_json

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
SNAPSHOT_FILE = Path(__file__).resolve().parent.parent / "data" / "telegraph_snapshots.jsonl"


def migrate_snapshot_row(conn, raw: dict, captured_at: int, batch_id: str):
    article_id = raw.get("id")
    if article_id is None:
        return "skipped"
    ctime = raw.get("ctime")
    modified_time = raw.get("modified_time") or ctime
    content_hash = compute_content_hash(raw)
    raw_json = stable_json(raw)
    date_key = datetime.fromtimestamp(int(ctime), SHANGHAI_TZ).strftime("%Y-%m-%d") if ctime else ""

    conn.execute(
        """
        INSERT INTO telegraph_raw_log (batch_id, source, article_id, ctime, modified_time, content_hash, captured_at, raw_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (batch_id, "jsonl.telegraph_snapshots", article_id, ctime, modified_time, content_hash, captured_at, raw_json),
    )

    current = conn.execute(
        "SELECT id, modified_time, content_hash FROM telegraph_raw_main WHERE id = ?",
        (article_id,),
    ).fetchone()

    values = (
        raw_json,
        raw.get("title") or "",
        raw.get("brief") or "",
        raw.get("content") or "",
        raw.get("level") or "",
        raw.get("reading_num") or 0,
        ctime,
        modified_time,
        raw.get("shareurl") or "",
        raw.get("category") if isinstance(raw.get("category"), str) else json.dumps(raw.get("category"), ensure_ascii=False),
        raw.get("type"),
        raw.get("sort_score"),
        raw.get("recommend"),
        raw.get("confirmed"),
        raw.get("jpush"),
        raw.get("share_num"),
        raw.get("comment_num"),
        json.dumps(raw.get("audio_url"), ensure_ascii=False) if raw.get("audio_url") is not None else None,
        json.dumps(raw.get("tags"), ensure_ascii=False) if raw.get("tags") is not None else None,
        json.dumps(raw.get("sub_titles"), ensure_ascii=False) if raw.get("sub_titles") is not None else None,
        json.dumps(raw.get("timeline"), ensure_ascii=False) if raw.get("timeline") is not None else None,
        json.dumps(raw.get("ad"), ensure_ascii=False) if raw.get("ad") is not None else None,
        json.dumps(raw.get("assocFastFact"), ensure_ascii=False) if raw.get("assocFastFact") is not None else None,
        raw.get("assocArticleUrl") or "",
        raw.get("assocVideoTitle") or "",
        raw.get("assocVideoUrl") or "",
        json.dumps(raw.get("assocCreditRating"), ensure_ascii=False) if raw.get("assocCreditRating") is not None else None,
        json.dumps(raw.get("stock_list"), ensure_ascii=False) if raw.get("stock_list") is not None else None,
        json.dumps(raw.get("subjects"), ensure_ascii=False) if raw.get("subjects") is not None else None,
        json.dumps(raw.get("plate_list"), ensure_ascii=False) if raw.get("plate_list") is not None else None,
        content_hash,
        date_key,
    )

    if current is None:
        conn.execute(
            """
            INSERT INTO telegraph_raw_main (
                id, raw_json, title, brief, content, level, reading_num, ctime, modified_time, shareurl,
                category, type, sort_score, recommend, confirmed, jpush, share_num, comment_num, audio_url,
                tags_json, sub_titles_json, timeline_json, ad_json, assoc_fast_fact_json, assoc_article_url,
                assoc_video_title, assoc_video_url, assoc_credit_rating_json, stock_list_json, subjects_json,
                plate_list_json, content_hash, first_seen_at, last_seen_at, seen_count, date_key
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (article_id, *values, captured_at, captured_at, 1),
        )
        return "inserted"

    changed = False
    if (modified_time or 0) > (current["modified_time"] or 0):
        changed = True
    elif content_hash != current["content_hash"]:
        changed = True

    if changed:
        conn.execute(
            """
            UPDATE telegraph_raw_main SET
                raw_json=?, title=?, brief=?, content=?, level=?, reading_num=?, ctime=?, modified_time=?, shareurl=?,
                category=?, type=?, sort_score=?, recommend=?, confirmed=?, jpush=?, share_num=?, comment_num=?, audio_url=?,
                tags_json=?, sub_titles_json=?, timeline_json=?, ad_json=?, assoc_fast_fact_json=?, assoc_article_url=?,
                assoc_video_title=?, assoc_video_url=?, assoc_credit_rating_json=?, stock_list_json=?, subjects_json=?,
                plate_list_json=?, content_hash=?, last_seen_at=?, seen_count=seen_count+1, date_key=?
            WHERE id=?
            """,
            (*values, captured_at, date_key, article_id),
        )
        return "updated"

    conn.execute(
        "UPDATE telegraph_raw_main SET last_seen_at=?, seen_count=seen_count+1 WHERE id=?",
        (captured_at, article_id),
    )
    return "unchanged"


def main():
    if not SNAPSHOT_FILE.exists():
        print(json.dumps({"ok": False, "reason": "snapshot_file_missing"}, ensure_ascii=False, indent=2))
        return

    captured_at = int(time.time())
    batch_id = datetime.now(SHANGHAI_TZ).strftime("migrate_%Y%m%d%H%M%S")
    conn = get_connection()
    inserted = updated = unchanged = skipped = 0
    migrated = 0
    try:
        with SNAPSHOT_FILE.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                raw = json.loads(line)
                result = migrate_snapshot_row(conn, raw, captured_at, batch_id)
                migrated += 1
                if result == "inserted":
                    inserted += 1
                elif result == "updated":
                    updated += 1
                elif result == "unchanged":
                    unchanged += 1
                else:
                    skipped += 1
        conn.commit()
        print(json.dumps({
            "ok": True,
            "batch_id": batch_id,
            "migrated": migrated,
            "inserted": inserted,
            "updated": updated,
            "unchanged": unchanged,
            "skipped": skipped,
        }, ensure_ascii=False, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
