"""
One-shot migration: user_cards.json → fleece.db

Run once:
    python migrate.py

What it does:
  1. Creates fleece.db and the cards table if not already present
  2. Imports all cards from user_cards.json
  3. Renames user_cards.json → user_cards.json.bak (preserves original)
"""
from pathlib import Path

import db

JSON_FILE = Path(__file__).parent / "user_cards.json"
BAK_FILE  = JSON_FILE.with_suffix(".json.bak")


def main() -> None:
    if not JSON_FILE.exists():
        print("user_cards.json not found — nothing to migrate.")
        return

    count = db.migrate_from_json(JSON_FILE)
    print(f"Migrated {count} card(s) to fleece.db.")

    JSON_FILE.rename(BAK_FILE)
    print(f"Original file preserved at {BAK_FILE.name}")

    cards = db.get_cards()
    print(f"\nCards now in database ({len(cards)} total):")
    for c in cards:
        print(f"  • {c['name']}  (fee: {c['annual_fee']})")


if __name__ == "__main__":
    main()
