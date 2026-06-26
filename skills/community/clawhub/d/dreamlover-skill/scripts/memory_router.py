from __future__ import annotations

import argparse
import json

from memory_logic import detect_read_reasons, detect_write_reasons
from memory_store import connect_memory_db, count_unsummarized_episodes


def main() -> None:
    parser = argparse.ArgumentParser(description="Compatibility wrapper for conditional memory decisions.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-message", required=True)
    parser.add_argument("--assistant-message", default="")
    parser.add_argument("--phase", choices=["pre", "post"], default="pre")
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--summary-threshold", type=int, default=8)
    parser.add_argument("--data-root")
    args = parser.parse_args()

    with connect_memory_db(args.data_root) as connection:
        relationship_row = connection.execute(
            """
            SELECT 1
            FROM relationship_state
            WHERE character_slug = ? AND user_id = ?
            """,
            (args.character_slug, args.user_id),
        ).fetchone()
        relationship_exists = relationship_row is not None
        unsummarized_count = count_unsummarized_episodes(connection, args.character_slug, args.user_id)

    read_reasons = detect_read_reasons(args.user_message, relationship_exists)
    write_reasons = detect_write_reasons(args.user_message) if args.phase == "post" else []
    should_write_after_reply = bool(write_reasons)
    should_summarize_after_reply = should_write_after_reply and (
        unsummarized_count + 1 >= args.summary_threshold
    )

    payload = {
        "phase": args.phase,
        "should_read": bool(read_reasons),
        "should_write": should_write_after_reply,
        "should_summarize": should_summarize_after_reply,
        "should_write_after_reply": should_write_after_reply,
        "should_summarize_after_reply": should_summarize_after_reply,
        "read_reasons": read_reasons,
        "write_reasons": write_reasons,
        "state": {
            "relationship_state_exists": relationship_exists,
            "unsummarized_episodic_count": unsummarized_count,
            "summary_threshold": args.summary_threshold,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
