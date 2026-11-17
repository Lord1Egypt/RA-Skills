"""
SQLite persistence layer for Fleece user card profiles.

Database file: fleece.db (project root, next to this file).
Shared between the Streamlit UI and the CLI — both import this module directly.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DB_PATH = Path(__file__).parent / "fleece.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS cards (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL UNIQUE,
    last_four    TEXT    NOT NULL DEFAULT '',
    annual_fee   TEXT    NOT NULL DEFAULT '$0',
    credit_limit INTEGER NOT NULL DEFAULT 0,
    rewards      TEXT    NOT NULL DEFAULT '',
    expiration   TEXT    NOT NULL DEFAULT '',
    image_url    TEXT    NOT NULL DEFAULT '',
    date_added   TEXT    NOT NULL DEFAULT (date('now')),
    fee_date     TEXT    NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS profile (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL DEFAULT ''
);
"""

# Default profile fields and their human-readable labels
PROFILE_FIELDS = {
    "dining_monthly":        "Monthly dining spend ($)",
    "groceries_monthly":     "Monthly groceries spend ($)",
    "travel_monthly":        "Monthly travel spend ($)",
    "gas_monthly":           "Monthly gas spend ($)",
    "other_monthly":         "Monthly other spend ($)",
    "annual_fee_tolerance":  "Max annual fee willing to pay ($)",
    "points_programs":       "Preferred points programs (e.g. Amex MR, Chase UR)",
    "home_airport":          "Home airport IATA code (e.g. JFK)",
    "goal":                  "Current redemption goal (e.g. business class to Tokyo)",
    "preferences":           "Other preferences (e.g. no foreign transaction fees)",
}

_COLUMNS = ("id", "name", "last_four", "annual_fee", "credit_limit",
            "rewards", "expiration", "image_url", "date_added", "fee_date")


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db() -> None:
    """Create tables if they don't exist. Safe to call on every startup."""
    with _conn() as con:
        con.executescript(_SCHEMA)
        cols = {row[1] for row in con.execute("PRAGMA table_info(cards)")}
        if "fee_date" not in cols:
            con.execute("ALTER TABLE cards ADD COLUMN fee_date TEXT NOT NULL DEFAULT ''")


def _row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def get_cards() -> list[dict]:
    """Return all cards ordered by date_added desc."""
    init_db()
    with _conn() as con:
        rows = con.execute("SELECT * FROM cards ORDER BY date_added DESC").fetchall()
    return [_row_to_dict(r) for r in rows]


def get_card_names() -> list[str]:
    """Return just the card names — used by the CLI wallet/roi commands."""
    init_db()
    with _conn() as con:
        rows = con.execute("SELECT name FROM cards ORDER BY date_added DESC").fetchall()
    return [r["name"] for r in rows]


def get_card(name: str) -> dict | None:
    """Return a single card by exact name, or None."""
    init_db()
    with _conn() as con:
        row = con.execute("SELECT * FROM cards WHERE name = ?", (name,)).fetchone()
    return _row_to_dict(row) if row else None


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

def add_card(card: dict) -> None:
    """Insert a new card. Raises ValueError if name already exists."""
    init_db()
    with _conn() as con:
        try:
            con.execute(
                """
                INSERT INTO cards (name, last_four, annual_fee, credit_limit,
                                   rewards, expiration, image_url, date_added, fee_date)
                VALUES (:name, :last_four, :annual_fee, :credit_limit,
                        :rewards, :expiration, :image_url, :date_added, :fee_date)
                """,
                {
                    "name":         card.get("name", ""),
                    "last_four":    card.get("last_four", ""),
                    "annual_fee":   card.get("annual_fee", "$0"),
                    "credit_limit": card.get("credit_limit", 0),
                    "rewards":      card.get("rewards", ""),
                    "expiration":   card.get("expiration", ""),
                    "image_url":    card.get("image_url", ""),
                    "date_added":   card.get("date_added", ""),
                    "fee_date":     card.get("fee_date", ""),
                },
            )
        except sqlite3.IntegrityError:
            raise ValueError(f'Card "{card.get("name")}" already exists.')


def update_card(name: str, updates: dict) -> bool:
    """Update fields on an existing card. Returns True if found."""
    if not updates:
        return False
    allowed = set(_COLUMNS) - {"id", "name", "date_added"}
    fields = {k: v for k, v in updates.items() if k in allowed}
    if not fields:
        return False
    init_db()
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["_name"] = name
    with _conn() as con:
        cur = con.execute(f"UPDATE cards SET {set_clause} WHERE name = :_name", fields)
    return cur.rowcount > 0


def remove_card(name: str) -> bool:
    """Delete a card by exact name. Returns True if it existed."""
    init_db()
    with _conn() as con:
        cur = con.execute("DELETE FROM cards WHERE name = ?", (name,))
    return cur.rowcount > 0


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

def get_profile() -> dict[str, str]:
    """Return the full profile as {key: value}. Missing keys return ''."""
    init_db()
    with _conn() as con:
        rows = con.execute("SELECT key, value FROM profile").fetchall()
    return {r["key"]: r["value"] for r in rows}


def set_profile_field(key: str, value: str) -> None:
    """Upsert a single profile field."""
    if key not in PROFILE_FIELDS:
        raise ValueError(f'Unknown profile field "{key}". Valid fields: {", ".join(PROFILE_FIELDS)}')
    init_db()
    with _conn() as con:
        con.execute(
            "INSERT INTO profile (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def clear_profile_field(key: str) -> None:
    """Remove a single profile field."""
    init_db()
    with _conn() as con:
        con.execute("DELETE FROM profile WHERE key = ?", (key,))


def profile_as_context(cards: list[str] | None = None) -> str:
    """
    Return a compact natural-language summary of the user profile suitable
    for injecting into a Brave Search query or LLM prompt.
    """
    p = get_profile()
    parts = []

    spend_fields = [
        ("dining_monthly", "dining"),
        ("groceries_monthly", "groceries"),
        ("travel_monthly", "travel"),
        ("gas_monthly", "gas"),
        ("other_monthly", "other"),
    ]
    spend_parts = [f"${p[k]}/mo {label}" for k, label in spend_fields if p.get(k)]
    if spend_parts:
        parts.append("Spending: " + ", ".join(spend_parts))

    if p.get("annual_fee_tolerance"):
        parts.append(f"Max annual fee: ${p['annual_fee_tolerance']}")
    if p.get("points_programs"):
        parts.append(f"Points programs: {p['points_programs']}")
    if p.get("home_airport"):
        parts.append(f"Home airport: {p['home_airport']}")
    if p.get("goal"):
        parts.append(f"Goal: {p['goal']}")
    if p.get("preferences"):
        parts.append(f"Preferences: {p['preferences']}")
    if cards:
        parts.append(f"Current cards: {', '.join(cards)}")

    return " | ".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# Renewal schedule
# ---------------------------------------------------------------------------

def get_renewal_schedule() -> list[dict]:
    """Return cards with fee_date set, sorted by days until next annual fee renewal.

    Each dict includes the card's fields plus:
      next_renewal  — ISO date of the next renewal (this year or next)
      days_until    — integer days from today
    """
    import datetime
    today = datetime.date.today()
    schedule = []
    for card in get_cards():
        fee_date = card.get("fee_date", "")
        if not fee_date:
            continue
        try:
            month, day = map(int, fee_date.split("-"))
            next_renewal = datetime.date(today.year, month, day)
            if next_renewal < today:
                next_renewal = datetime.date(today.year + 1, month, day)
            schedule.append({
                **card,
                "next_renewal": next_renewal.isoformat(),
                "days_until":   (next_renewal - today).days,
            })
        except (ValueError, AttributeError):
            continue
    return sorted(schedule, key=lambda x: x["days_until"])


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------

def migrate_from_json(json_path: Path) -> int:
    """
    Import cards from a JSON file into SQLite. Skips duplicates.
    Returns the number of cards inserted.
    """
    import json

    if not json_path.exists():
        return 0

    raw = json.loads(json_path.read_text())
    if not isinstance(raw, list):
        return 0

    init_db()
    inserted = 0
    for card in raw:
        try:
            add_card(card)
            inserted += 1
        except ValueError:
            pass  # already exists — skip
    return inserted
