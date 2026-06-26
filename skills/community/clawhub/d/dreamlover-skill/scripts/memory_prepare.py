from __future__ import annotations

import argparse
import json

from memory_logic import detect_read_reasons, detect_write_reasons, fetch_memory_payload
from memory_store import connect_memory_db, count_unsummarized_episodes


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare conditional memory context for a character reply.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-message", required=True)
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--summary-threshold", type=int, default=8)
    parser.add_argument("--profile-limit", type=int, default=8)
    parser.add_argument("--episodic-limit", type=int, default=5)
    parser.add_argument("--summary-limit", type=int, default=3)
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
        write_reasons = detect_write_reasons(args.user_message)
        should_read = bool(read_reasons)
        should_write_after_reply = bool(write_reasons)
        should_summarize_after_reply = should_write_after_reply and (unsummarized_count + 1 >= args.summary_threshold)

        memory_context = {
            "has_memory": False,
            "relationship_state": None,
            "profile_memory": [],
            "episodic_memory": [],
            "conversation_summary": [],
        }
        if should_read:
            memory_context = fetch_memory_payload(
                connection,
                args.character_slug,
                args.user_id,
                profile_limit=args.profile_limit,
                episodic_limit=args.episodic_limit,
                summary_limit=args.summary_limit,
            )

    payload = {
        "character_slug": args.character_slug,
        "user_id": args.user_id,
        "should_read": should_read,
        "should_write_after_reply": should_write_after_reply,
        "should_summarize_after_reply": should_summarize_after_reply,
        "read_reasons": read_reasons,
        "write_reasons": write_reasons,
        "memory_context": memory_context,
        "guidance": [
            "Stay silent about internal memory checks.",
            "If no relevant memory exists, reply naturally without claiming hidden memory lookup.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
