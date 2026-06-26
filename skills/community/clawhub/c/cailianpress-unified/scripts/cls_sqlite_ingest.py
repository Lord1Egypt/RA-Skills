#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from adapters.telegraph_nodeapi import fetch_telegraph_list
from db import compute_content_hash, get_connection, stable_json

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


def jdump(value):
    return json.dumps(value, ensure_ascii=False) if value is not None else None


def main():
    captured_at = int(time.time())
    batch_id = datetime.now(SHANGHAI_TZ).strftime("%Y%m%d%H%M%S")
    rows = fetch_telegraph_list()
    conn = get_connection()
    inserted = 0
    updated = 0
    unchanged = 0
    raw_logged = 0
    try:
        for raw in rows:
            article_id = raw.get("id")
            if article_id is None:
                continue
            ctime = raw.get("ctime")
            modified_time = raw.get("modified_time")
            content_hash = compute_content_hash(raw)
            raw_json = stable_json(raw)
            date_key = datetime.fromtimestamp(int(ctime), SHANGHAI_TZ).strftime("%Y-%m-%d") if ctime else ""

            conn.execute(
                """
                INSERT INTO telegraph_raw_log (batch_id, source, article_id, ctime, modified_time, content_hash, captured_at, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (batch_id, "nodeapi.telegraphList", article_id, ctime, modified_time, content_hash, captured_at, raw_json),
            )
            raw_logged += 1

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
                raw.get("category") if isinstance(raw.get("category"), str) else jdump(raw.get("category")),
                raw.get("type"),
                raw.get("sort_score"),
                raw.get("recommend"),
                raw.get("confirmed"),
                raw.get("jpush"),
                raw.get("share_num"),
                raw.get("comment_num"),
                jdump(raw.get("audio_url")),
                jdump(raw.get("tags")),
                jdump(raw.get("sub_titles")),
                jdump(raw.get("timeline")),
                jdump(raw.get("ad")),
                jdump(raw.get("assocFastFact")),
                raw.get("assocArticleUrl") or "",
                raw.get("assocVideoTitle") or "",
                raw.get("assocVideoUrl") or "",
                jdump(raw.get("assocCreditRating")),
                jdump(raw.get("stock_list")),
                jdump(raw.get("subjects")),
                jdump(raw.get("plate_list")),
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
                inserted += 1
            else:
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
                    updated += 1
                else:
                    conn.execute(
                        "UPDATE telegraph_raw_main SET last_seen_at=?, seen_count=seen_count+1 WHERE id=?",
                        (captured_at, article_id),
                    )
                    unchanged += 1

            for subject in raw.get("subjects") or []:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO telegraph_subjects
                    (article_id, subject_id, subject_name, attention_num, plate_id, channel, captured_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article_id,
                        subject.get("subject_id"),
                        subject.get("subject_name") or "",
                        subject.get("attention_num") or 0,
                        subject.get("plate_id") or 0,
                        subject.get("channel") or "",
                        captured_at,
                    ),
                )

            for stock in raw.get("stock_list") or []:
                secu_code = stock.get("secu_code") or stock.get("code") or stock.get("symbol")
                secu_name = stock.get("secu_name") or stock.get("name") or ""
                if not secu_code:
                    continue
                conn.execute(
                    """
                    INSERT OR REPLACE INTO telegraph_stocks
                    (article_id, secu_code, secu_name, captured_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (article_id, secu_code, secu_name, captured_at),
                )

            for plate in raw.get("plate_list") or []:
                plate_id = plate.get("plate_id") or plate.get("id")
                plate_name = plate.get("plate_name") or plate.get("name") or ""
                if plate_id is None:
                    continue
                conn.execute(
                    """
                    INSERT OR REPLACE INTO telegraph_plates
                    (article_id, plate_id, plate_name, captured_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (article_id, plate_id, plate_name, captured_at),
                )

        conn.commit()
        print(json.dumps({
            "ok": True,
            "batch_id": batch_id,
            "raw_logged": raw_logged,
            "inserted": inserted,
            "updated": updated,
            "unchanged": unchanged,
        }, ensure_ascii=False, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
