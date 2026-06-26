from __future__ import annotations

import argparse
import json

from memory_store import connect_memory_db, utc_now


def build_summary_text(rows: list[dict]) -> str:
    bullets = []
    for row in rows:
        bullets.append(f"- [{row['event_type']}] {row['summary']}")
    return "Recent memory summary:\n" + "\n".join(bullets)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize unsummarized episodic memory into a rolling conversation summary.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--summary-threshold", type=int, default=8)
    parser.add_argument("--max-items", type=int, default=12)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--data-root")
    args = parser.parse_args()

    with connect_memory_db(args.data_root) as connection:
        rows = connection.execute(
            """
            SELECT id, summary, event_type, created_at
            FROM episodic_memory
            WHERE character_slug = ? AND user_id = ? AND summarized = 0
            ORDER BY id ASC
            LIMIT ?
            """,
            (args.character_slug, args.user_id, args.max_items),
        ).fetchall()

        if len(rows) < args.summary_threshold and not args.force:
            print(
                json.dumps(
                    {
                        "status": "skipped",
                        "reason": "threshold_not_met",
                        "unsummarized_count": len(rows),
                        "summary_threshold": args.summary_threshold,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return

        if not rows:
            print(json.dumps({"status": "skipped", "reason": "no_unsummarized_memory"}, ensure_ascii=False, indent=2))
            return

        row_dicts = [dict(row) for row in rows]
        summary_text = build_summary_text(row_dicts)
        now = utc_now()
        cursor = connection.execute(
            """
            INSERT INTO conversation_summary (
                character_slug, user_id, turn_start, turn_end, summary, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                args.character_slug,
                args.user_id,
                row_dicts[0]["id"],
                row_dicts[-1]["id"],
                summary_text,
                now,
            ),
        )
        summary_id = int(cursor.lastrowid)
        connection.execute(
            """
            UPDATE episodic_memory
            SET summarized = 1, summary_id = ?
            WHERE id BETWEEN ? AND ?
            """,
            (summary_id, row_dicts[0]["id"], row_dicts[-1]["id"]),
        )
        connection.commit()

    print(
        json.dumps(
            {
                "status": "ok",
                "summary_id": summary_id,
                "turn_start": row_dicts[0]["id"],
                "turn_end": row_dicts[-1]["id"],
                "summary": summary_text,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
