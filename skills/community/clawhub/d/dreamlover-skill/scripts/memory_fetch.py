from __future__ import annotations

import argparse
import json

from memory_logic import fetch_memory_payload
from memory_store import connect_memory_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch relevant local memory for a child skill.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--user-message", required=True)
    parser.add_argument("--user-id", default="default")
    parser.add_argument("--profile-limit", type=int, default=8)
    parser.add_argument("--episodic-limit", type=int, default=5)
    parser.add_argument("--summary-limit", type=int, default=3)
    parser.add_argument("--data-root")
    args = parser.parse_args()

    with connect_memory_db(args.data_root) as connection:
        memory_payload = fetch_memory_payload(
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
        "query": args.user_message,
        **memory_payload,
        "guidance": [
            "Use only memory that is relevant to the current reply.",
            "If no memory is relevant, answer normally and do not pretend there is prior history.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
