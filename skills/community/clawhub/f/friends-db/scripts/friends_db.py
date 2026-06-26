#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


WORKSPACE_ROOT = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
STATE_DIR = Path(os.environ.get("OPENCLAW_FRIENDS_DB_DIR", WORKSPACE_ROOT / ".localdb" / "friends-db"))
DB_PATH = STATE_DIR / "friends.sqlite3"
BACKUP_DIR = STATE_DIR / "backups"
DEFAULT_SOURCE_MD = WORKSPACE_ROOT / "friends.md"
DEFAULT_CALENDAR_ACCOUNT = os.environ.get("OPENCLAW_FRIENDS_CALENDAR_ACCOUNT", "alexuser@gmail.com")
DEFAULT_CALENDAR_ID = os.environ.get("OPENCLAW_FRIENDS_CALENDAR_ID", "primary")
DEFAULT_TIMEZONE = os.environ.get("OPENCLAW_FRIENDS_TIMEZONE", "America/Los_Angeles")
ACTIVITY_TEMPLATES_PATH = Path(__file__).resolve().parent.parent / "assets" / "activity_templates.json"

VALID_METHOD_KINDS = {"email", "phone", "imessage", "sms", "other"}
VALID_IMPORTANCE = {"high", "medium", "low"}
VALID_INTERACTION_TYPES = {"in_person", "call", "text", "email"}
VALID_INTERACTION_SOURCES = {"calendar", "manual"}
VALID_TAG_TYPES = {"interest", "activity", "neighborhood", "group"}
IMPORTANCE_TO_DAYS = {"high": 20, "medium": 30, "low": 90}
MAX_SEARCH_LIMIT = 50
RECENT_INTERACTIONS_LIMIT = 10

EMAIL_RE = re.compile(r"(?P<email>[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})", re.IGNORECASE)
PHONE_RE = re.compile(r"(?P<phone>\+?\d[\d ()-]{6,}\d)")
HEADING_RE = re.compile(r"^\*\*(?P<name>.+?)\*\*(?:\s+\((?P<paren>.+?)\))?\s*$")
PREFERRED_RE = re.compile(r"^>\s*\*Preferred name:\s*(?P<name>.+?)\*\s*$", re.IGNORECASE)
EMOJI_PREFIX_RE = re.compile(r"^[^\w+@]+")
SPACE_RE = re.compile(r"\s+")


@dataclass
class ParsedContact:
    display_name: str
    parenthetical: str | None = None
    preferred_name: str | None = None
    aliases: list[str] = field(default_factory=list)
    methods: list[tuple[str, str, str | None, int]] = field(default_factory=list)
    facts: list[tuple[str, str]] = field(default_factory=list)


def local_timezone() -> ZoneInfo:
    return ZoneInfo(DEFAULT_TIMEZONE)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def now_local() -> datetime:
    return datetime.now(local_timezone()).replace(microsecond=0)


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, 0o700)


def ensure_private_file(path: Path) -> None:
    flags = os.O_CREAT | os.O_RDWR
    fd = os.open(path, flags, 0o600)
    os.close(fd)
    os.chmod(path, 0o600)


def normalize_free_text(text: str) -> str:
    cleaned = EMOJI_PREFIX_RE.sub("", text).strip()
    return SPACE_RE.sub(" ", cleaned)


def normalize_lookup_text(text: str) -> str:
    return SPACE_RE.sub(" ", text).strip().lower()


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    if "T" not in normalized:
        return datetime.combine(date.fromisoformat(normalized), time(hour=12), tzinfo=local_timezone())
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=local_timezone())
    return parsed


def serialize_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.replace(microsecond=0).isoformat()


def add_method(contact: ParsedContact, kind: str, value: str, label: str | None = None, primary: bool = False) -> None:
    value = value.strip()
    if not value:
        return
    if kind not in VALID_METHOD_KINDS:
        raise ValueError(f"Unsupported method kind: {kind}")
    method = (kind, value, label, 1 if primary else 0)
    if method not in contact.methods:
        contact.methods.append(method)


def add_alias(contact: ParsedContact, alias: str) -> None:
    alias = alias.strip()
    if alias and alias not in contact.aliases and alias != contact.display_name:
        contact.aliases.append(alias)


def add_fact(contact: ParsedContact, fact: str, fact_type: str = "note") -> None:
    fact = normalize_free_text(fact)
    if fact and (fact, fact_type) not in contact.facts:
        contact.facts.append((fact, fact_type))


def table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})")}


def ensure_contact_columns(conn: sqlite3.Connection) -> None:
    columns = table_columns(conn, "contacts")
    required = {
        "importance": "TEXT NOT NULL DEFAULT 'medium' CHECK(importance IN ('high','medium','low'))",
        "cadence_days": "INTEGER NOT NULL DEFAULT 30",
        "paused_until": "TEXT",
        "last_in_person_at": "TEXT",
        "last_contact_at": "TEXT",
        "notes_private": "TEXT",
        "home_area": "TEXT",
        "best_times": "TEXT",
    }
    for name, definition in required.items():
        if name not in columns:
            conn.execute(f"ALTER TABLE contacts ADD COLUMN {name} {definition}")
    conn.execute(
        """
        UPDATE contacts
        SET importance = COALESCE(NULLIF(importance, ''), 'medium')
        WHERE importance IS NULL OR importance = ''
        """
    )
    conn.execute(
        """
        UPDATE contacts
        SET cadence_days = CASE COALESCE(NULLIF(importance, ''), 'medium')
            WHEN 'high' THEN 20
            WHEN 'low' THEN 90
            ELSE 30
        END
        WHERE cadence_days IS NULL OR cadence_days <= 0
        """
    )


def connect() -> sqlite3.Connection:
    ensure_private_dir(STATE_DIR.parent)
    ensure_private_dir(STATE_DIR)
    ensure_private_dir(BACKUP_DIR)
    ensure_private_file(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL UNIQUE,
            preferred_name TEXT,
            parenthetical TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
            alias TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            value TEXT NOT NULL,
            label TEXT,
            is_primary INTEGER NOT NULL DEFAULT 0,
            UNIQUE(contact_id, kind, value)
        );

        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
            fact TEXT NOT NULL,
            fact_type TEXT NOT NULL DEFAULT 'note',
            UNIQUE(contact_id, fact)
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
            occurred_at TEXT NOT NULL,
            interaction_type TEXT NOT NULL CHECK(interaction_type IN ('in_person','call','text','email')),
            source TEXT NOT NULL CHECK(source IN ('calendar','manual')),
            calendar_event_id TEXT,
            calendar_event_title TEXT,
            duration_minutes INTEGER,
            location TEXT,
            notes TEXT,
            counts_for_cadence INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS contact_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
            tag_type TEXT NOT NULL CHECK(tag_type IN ('interest','activity','neighborhood','group')),
            tag TEXT NOT NULL,
            UNIQUE(contact_id, tag_type, tag)
        );

        CREATE INDEX IF NOT EXISTS idx_contacts_display_name_nocase
            ON contacts(display_name COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_contacts_preferred_name_nocase
            ON contacts(preferred_name COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_aliases_alias_nocase
            ON aliases(alias COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_methods_value_nocase
            ON methods(value COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_interactions_contact_time
            ON interactions(contact_id, occurred_at DESC);
        CREATE INDEX IF NOT EXISTS idx_interactions_type
            ON interactions(interaction_type, occurred_at DESC);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_interactions_contact_event
            ON interactions(contact_id, calendar_event_id)
            WHERE calendar_event_id IS NOT NULL;
        CREATE INDEX IF NOT EXISTS idx_contact_tags_contact_type
            ON contact_tags(contact_id, tag_type);
        """
    )
    ensure_contact_columns(conn)
    conn.commit()
    return conn


def parse_markdown(path: Path) -> list[ParsedContact]:
    contacts: list[ParsedContact] = []
    current: ParsedContact | None = None

    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        heading_match = HEADING_RE.match(line.strip())
        if heading_match:
            current = ParsedContact(
                display_name=heading_match.group("name").strip(),
                parenthetical=heading_match.group("paren").strip() if heading_match.group("paren") else None,
            )
            add_alias(current, current.display_name)
            if current.parenthetical:
                email_match = EMAIL_RE.fullmatch(current.parenthetical)
                if email_match:
                    add_method(current, "email", email_match.group("email"), label="imported from heading", primary=True)
                else:
                    add_alias(current, current.parenthetical)
            contacts.append(current)
            continue

        if current is None:
            continue

        preferred_match = PREFERRED_RE.match(line.strip())
        if preferred_match:
            current.preferred_name = preferred_match.group("name").strip()
            add_alias(current, current.preferred_name)
            continue

        if line.lstrip().startswith("- "):
            bullet = line.lstrip()[2:].strip()
            bullet_text = normalize_free_text(bullet)
            email_match = EMAIL_RE.search(bullet_text)
            phone_match = PHONE_RE.search(bullet_text)
            lowered = bullet_text.lower()

            if email_match:
                add_method(current, "email", email_match.group("email"), label=bullet_text, primary=True)
                if bullet_text != email_match.group("email"):
                    add_fact(current, bullet_text, "note")
                continue

            if phone_match:
                phone = phone_match.group("phone").strip()
                add_method(current, "phone", phone, label=bullet_text, primary=True)
                if "imessage" in lowered:
                    add_method(current, "imessage", phone, label=bullet_text, primary=True)
                if bullet_text != phone:
                    add_fact(current, bullet_text, "note")
                continue

            if "imessage" in lowered:
                add_fact(current, bullet_text, "channel")
                continue

            fact_type = "event" if any(month in lowered for month in ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")) else "note"
            add_fact(current, bullet_text, fact_type)

    return contacts


def backup_file(path: Path) -> Path:
    ensure_private_dir(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"{path.stem}-{timestamp}{path.suffix}"
    shutil.copy2(path, backup_path)
    os.chmod(backup_path, 0o600)
    return backup_path


def validate_migration_source(source_arg: str) -> Path:
    requested = Path(source_arg).expanduser()
    expected = DEFAULT_SOURCE_MD.expanduser()
    if requested != expected:
        raise SystemExit(f"migrate only supports the workspace source: {expected}")
    if requested.is_symlink():
        raise SystemExit(f"Refusing to migrate from symlinked path: {requested}")
    source_path = requested.resolve()
    if source_path != expected.resolve():
        raise SystemExit(f"migrate only supports the workspace source: {expected.resolve()}")
    return source_path


def source_stub(db_path: Path, backup_path: Path) -> str:
    return (
        "# Friends Database\n\n"
        "This file is now a stub. The source of truth lives in a private local SQLite database.\n\n"
        f"- Database: `{db_path}`\n"
        f"- Backup of migrated markdown: `{backup_path}`\n"
        "- Search contacts: `python3 ./skills/friends-db/scripts/friends_db.py search \"<query>\"`\n"
        "- Friend CRM due list: `python3 ./skills/friends-db/scripts/friends_db.py due-list`\n"
        "- Sync calendar history: `python3 ./skills/friends-db/scripts/friends_db.py sync-calendar`\n"
        "- Update records through the helper script, not by editing this markdown file.\n"
    )


def upsert_contact(conn: sqlite3.Connection, contact: ParsedContact) -> int:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO contacts (display_name, preferred_name, parenthetical, created_at, updated_at, importance, cadence_days)
        VALUES (?, ?, ?, ?, ?, 'medium', 30)
        ON CONFLICT(display_name) DO UPDATE SET
            preferred_name = COALESCE(excluded.preferred_name, contacts.preferred_name),
            parenthetical = COALESCE(excluded.parenthetical, contacts.parenthetical),
            updated_at = excluded.updated_at
        """,
        (contact.display_name, contact.preferred_name, contact.parenthetical, now, now),
    )
    contact_id = conn.execute("SELECT id FROM contacts WHERE display_name = ?", (contact.display_name,)).fetchone()["id"]
    if contact.preferred_name:
        add_alias(contact, contact.preferred_name)
    if contact.parenthetical and not EMAIL_RE.fullmatch(contact.parenthetical or ""):
        add_alias(contact, contact.parenthetical)

    for alias in contact.aliases:
        conn.execute("INSERT OR IGNORE INTO aliases (contact_id, alias) VALUES (?, ?)", (contact_id, alias))
    for kind, value, label, is_primary in contact.methods:
        conn.execute(
            """
            INSERT INTO methods (contact_id, kind, value, label, is_primary)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(contact_id, kind, value) DO UPDATE SET
                label = COALESCE(excluded.label, methods.label),
                is_primary = MAX(methods.is_primary, excluded.is_primary)
            """,
            (contact_id, kind, value, label, is_primary),
        )
    for fact, fact_type in contact.facts:
        conn.execute("INSERT OR IGNORE INTO facts (contact_id, fact, fact_type) VALUES (?, ?, ?)", (contact_id, fact, fact_type))
    return contact_id


def fetch_contact_row(conn: sqlite3.Connection, contact_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if row is None:
        raise SystemExit(f"Contact id not found: {contact_id}")
    return row


def contact_methods(conn: sqlite3.Connection, contact_id: int) -> list[dict[str, Any]]:
    return [
        {
            "kind": row["kind"],
            "value": row["value"],
            "label": row["label"],
            "is_primary": bool(row["is_primary"]),
        }
        for row in conn.execute(
            "SELECT kind, value, label, is_primary FROM methods WHERE contact_id = ? ORDER BY is_primary DESC, kind, value",
            (contact_id,),
        )
    ]


def contact_facts(conn: sqlite3.Connection, contact_id: int) -> list[dict[str, Any]]:
    return [
        {"fact": row["fact"], "fact_type": row["fact_type"]}
        for row in conn.execute(
            "SELECT fact, fact_type FROM facts WHERE contact_id = ? ORDER BY fact_type, id",
            (contact_id,),
        )
    ]


def contact_aliases(conn: sqlite3.Connection, contact_id: int) -> list[str]:
    return [row["alias"] for row in conn.execute("SELECT alias FROM aliases WHERE contact_id = ? ORDER BY alias", (contact_id,))]


def contact_tags_grouped(conn: sqlite3.Connection, contact_id: int) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {tag_type: [] for tag_type in sorted(VALID_TAG_TYPES)}
    for row in conn.execute(
        "SELECT tag_type, tag FROM contact_tags WHERE contact_id = ? ORDER BY tag_type, tag",
        (contact_id,),
    ):
        grouped.setdefault(row["tag_type"], []).append(row["tag"])
    return {key: value for key, value in grouped.items() if value}


def recent_interactions(conn: sqlite3.Connection, contact_id: int, limit: int = RECENT_INTERACTIONS_LIMIT) -> list[dict[str, Any]]:
    return [
        {
            "occurred_at": row["occurred_at"],
            "interaction_type": row["interaction_type"],
            "source": row["source"],
            "calendar_event_id": row["calendar_event_id"],
            "calendar_event_title": row["calendar_event_title"],
            "duration_minutes": row["duration_minutes"],
            "location": row["location"],
            "notes": row["notes"],
            "counts_for_cadence": bool(row["counts_for_cadence"]),
        }
        for row in conn.execute(
            """
            SELECT occurred_at, interaction_type, source, calendar_event_id, calendar_event_title,
                   duration_minutes, location, notes, counts_for_cadence
            FROM interactions
            WHERE contact_id = ?
            ORDER BY occurred_at DESC, id DESC
            LIMIT ?
            """,
            (contact_id, limit),
        )
    ]


def contact_payload(conn: sqlite3.Connection, contact_id: int) -> dict[str, Any]:
    row = fetch_contact_row(conn, contact_id)
    return {
        "id": row["id"],
        "display_name": row["display_name"],
        "preferred_name": row["preferred_name"],
        "parenthetical": row["parenthetical"],
        "aliases": contact_aliases(conn, contact_id),
        "methods": contact_methods(conn, contact_id),
        "facts": contact_facts(conn, contact_id),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def importance_rank(value: str | None) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get((value or "medium").lower(), 1)


def compute_due_fields(row: sqlite3.Row, reference: datetime | None = None) -> dict[str, Any]:
    reference = reference or now_local()
    paused_until = parse_iso_datetime(row["paused_until"])
    last_in_person = parse_iso_datetime(row["last_in_person_at"])
    last_contact = parse_iso_datetime(row["last_contact_at"])
    cadence_days = int(row["cadence_days"] or IMPORTANCE_TO_DAYS.get(row["importance"] or "medium", 30))

    if paused_until and paused_until > reference:
        return {
            "paused_until": serialize_datetime(paused_until),
            "last_in_person_at": serialize_datetime(last_in_person),
            "last_contact_at": serialize_datetime(last_contact),
            "next_due_at": None,
            "overdue_days": None,
            "status": "paused",
        }

    if last_in_person is None:
        return {
            "paused_until": serialize_datetime(paused_until),
            "last_in_person_at": None,
            "last_contact_at": serialize_datetime(last_contact),
            "next_due_at": None,
            "overdue_days": None,
            "status": "overdue",
        }

    next_due = last_in_person + timedelta(days=cadence_days)
    overdue_days = max(0, (reference.date() - next_due.date()).days)
    status = "overdue" if next_due <= reference else "on_track"
    return {
        "paused_until": serialize_datetime(paused_until),
        "last_in_person_at": serialize_datetime(last_in_person),
        "last_contact_at": serialize_datetime(last_contact),
        "next_due_at": serialize_datetime(next_due),
        "overdue_days": overdue_days if status == "overdue" else 0,
        "status": status,
    }


def refresh_contact_cache(conn: sqlite3.Connection, contact_ids: list[int]) -> None:
    deduped = sorted(set(contact_ids))
    now = utc_now()
    for contact_id in deduped:
        aggregate = conn.execute(
            """
            SELECT
                MAX(CASE WHEN interaction_type = 'in_person' AND counts_for_cadence = 1 THEN occurred_at END) AS last_in_person_at,
                MAX(occurred_at) AS last_contact_at
            FROM interactions
            WHERE contact_id = ?
            """,
            (contact_id,),
        ).fetchone()
        conn.execute(
            """
            UPDATE contacts
            SET last_in_person_at = ?, last_contact_at = ?, updated_at = ?
            WHERE id = ?
            """,
            (aggregate["last_in_person_at"], aggregate["last_contact_at"], now, contact_id),
        )


def resolve_contact_ids(conn: sqlite3.Connection, term: str) -> list[int]:
    term = term.strip()
    exact = conn.execute(
        """
        SELECT DISTINCT c.id
        FROM contacts c
        LEFT JOIN aliases a ON a.contact_id = c.id
        LEFT JOIN methods m ON m.contact_id = c.id
        WHERE lower(c.display_name) = lower(?)
           OR lower(COALESCE(c.preferred_name, '')) = lower(?)
           OR lower(COALESCE(c.parenthetical, '')) = lower(?)
           OR lower(COALESCE(a.alias, '')) = lower(?)
           OR lower(COALESCE(m.value, '')) = lower(?)
        ORDER BY c.display_name
        """,
        (term, term, term, term, term),
    ).fetchall()
    if exact:
        return [row["id"] for row in exact]

    like_term = f"%{term.lower()}%"
    rows = conn.execute(
        """
        SELECT DISTINCT c.id
        FROM contacts c
        LEFT JOIN aliases a ON a.contact_id = c.id
        LEFT JOIN methods m ON m.contact_id = c.id
        LEFT JOIN facts f ON f.contact_id = c.id
        LEFT JOIN contact_tags t ON t.contact_id = c.id
        WHERE lower(c.display_name) LIKE ?
           OR lower(COALESCE(c.preferred_name, '')) LIKE ?
           OR lower(COALESCE(c.parenthetical, '')) LIKE ?
           OR lower(COALESCE(a.alias, '')) LIKE ?
           OR lower(COALESCE(m.value, '')) LIKE ?
           OR lower(COALESCE(m.label, '')) LIKE ?
           OR lower(COALESCE(f.fact, '')) LIKE ?
           OR lower(COALESCE(t.tag, '')) LIKE ?
        ORDER BY c.display_name
        """,
        (like_term, like_term, like_term, like_term, like_term, like_term, like_term, like_term),
    ).fetchall()
    return [row["id"] for row in rows]


def require_single_contact(conn: sqlite3.Connection, identifier: str) -> int:
    ids = resolve_contact_ids(conn, identifier)
    if not ids:
        raise SystemExit(f"No contact matched: {identifier}")
    if len(ids) > 1:
        raise SystemExit(f"Identifier matched multiple contacts: {identifier}")
    return ids[0]


def load_activity_templates() -> dict[str, Any]:
    return json.loads(ACTIVITY_TEMPLATES_PATH.read_text())


def phrase_matches(term: str, haystack: str) -> bool:
    normalized = normalize_lookup_text(term)
    if len(normalized) < 3:
        return False
    pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(normalized)}(?![A-Za-z0-9])", re.IGNORECASE)
    return pattern.search(haystack) is not None


def contact_match_terms(conn: sqlite3.Connection, contact_id: int) -> list[str]:
    row = fetch_contact_row(conn, contact_id)
    terms = [row["display_name"]]
    if row["preferred_name"]:
        terms.append(row["preferred_name"])
    if row["parenthetical"] and not EMAIL_RE.fullmatch(row["parenthetical"]):
        terms.append(row["parenthetical"])
    terms.extend(contact_aliases(conn, contact_id))
    deduped: list[str] = []
    for term in terms:
        cleaned = normalize_free_text(term)
        if cleaned and cleaned.lower() not in {item.lower() for item in deduped}:
            deduped.append(cleaned)
    return deduped


def build_contact_index(conn: sqlite3.Connection) -> dict[str, Any]:
    email_map: dict[str, set[int]] = {}
    terms_map: dict[int, list[str]] = {}
    for row in conn.execute("SELECT id FROM contacts ORDER BY display_name"):
        contact_id = row["id"]
        terms_map[contact_id] = contact_match_terms(conn, contact_id)
        for method in conn.execute("SELECT value FROM methods WHERE contact_id = ? AND kind = 'email'", (contact_id,)):
            email_map.setdefault(method["value"].strip().lower(), set()).add(contact_id)
    return {"email_map": email_map, "terms_map": terms_map}


def load_gog_env() -> dict[str, str]:
    env = os.environ.copy()
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            gog_env = config.get("skills", {}).get("entries", {}).get("gog", {}).get("env", {})
        except json.JSONDecodeError:
            gog_env = {}
        for key, value in gog_env.items():
            env.setdefault(key, str(value))
    return env


def run_gog_json(args: list[str]) -> Any:
    env = load_gog_env()
    cmd = ["gog", *args, "--json", "--results-only", "--no-input"]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
    except FileNotFoundError as exc:
        raise SystemExit("gog CLI not found; install it before syncing calendar") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise SystemExit(f"gog command failed: {message}") from exc
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit("gog returned invalid JSON") from exc


def parse_calendar_timestamp(payload: dict[str, Any]) -> datetime | None:
    if "dateTime" in payload:
        return parse_iso_datetime(payload["dateTime"])
    if "date" in payload:
        tz_name = payload.get("timeZone") or DEFAULT_TIMEZONE
        dt = datetime.combine(date.fromisoformat(payload["date"]), time(hour=12), tzinfo=ZoneInfo(tz_name))
        return dt
    return None


def duration_minutes(start: dict[str, Any], end: dict[str, Any]) -> int | None:
    if "dateTime" not in start or "dateTime" not in end:
        return None
    start_dt = parse_calendar_timestamp(start)
    end_dt = parse_calendar_timestamp(end)
    if start_dt is None or end_dt is None:
        return None
    minutes = int((end_dt - start_dt).total_seconds() // 60)
    return max(minutes, 0)


def insert_interaction(
    conn: sqlite3.Connection,
    contact_id: int,
    occurred_at: datetime,
    interaction_type: str,
    source: str,
    calendar_event_id: str | None = None,
    calendar_event_title: str | None = None,
    duration_minutes_value: int | None = None,
    location: str | None = None,
    notes: str | None = None,
    counts_for_cadence: bool | None = None,
) -> bool:
    counts = bool(counts_for_cadence if counts_for_cadence is not None else interaction_type == "in_person")
    cursor = conn.execute(
        """
        INSERT OR IGNORE INTO interactions (
            contact_id, occurred_at, interaction_type, source, calendar_event_id, calendar_event_title,
            duration_minutes, location, notes, counts_for_cadence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            contact_id,
            serialize_datetime(occurred_at),
            interaction_type,
            source,
            calendar_event_id,
            calendar_event_title,
            duration_minutes_value,
            location,
            notes,
            1 if counts else 0,
        ),
    )
    return cursor.rowcount > 0


def decorate_suggestion(base: str, location_hint: str | None, time_hint: str | None) -> str:
    suggestion = normalize_free_text(base)
    if location_hint and location_hint.lower() not in suggestion.lower() and " near " not in suggestion.lower() and " at " not in suggestion.lower():
        suggestion = f"{suggestion} near {location_hint}"
    if time_hint and time_hint.lower() not in suggestion.lower():
        if time_hint.lower().startswith(("on ", "this ", "next ", "today", "tonight")):
            suggestion = f"{suggestion} {time_hint}"
        else:
            suggestion = f"{suggestion} on {time_hint}"
    return suggestion


def build_suggestions(conn: sqlite3.Connection, contact_id: int, limit: int = 3) -> list[str]:
    templates = load_activity_templates()
    tag_map = contact_tags_grouped(conn, contact_id)
    row = fetch_contact_row(conn, contact_id)
    location_hint = None
    if tag_map.get("neighborhood"):
        location_hint = tag_map["neighborhood"][0]
    elif row["home_area"]:
        location_hint = row["home_area"]
    time_hint = row["best_times"]

    candidates: list[str] = []
    seen: set[str] = set()

    def add_candidate(text: str) -> None:
        normalized = normalize_lookup_text(text)
        if normalized and normalized not in seen:
            seen.add(normalized)
            candidates.append(decorate_suggestion(text, location_hint, time_hint))

    for tag in tag_map.get("activity", []):
        mapped = templates["activity"].get(normalize_lookup_text(tag), [tag.title()])
        for entry in mapped:
            add_candidate(entry)

    if not candidates:
        for tag in tag_map.get("interest", []):
            mapped = templates["interest"].get(normalize_lookup_text(tag), [f"{tag.title()} catch-up"])
            for entry in mapped:
                add_candidate(entry)

    for fallback in templates["fallback"]:
        add_candidate(fallback)
        if len(candidates) >= limit:
            break

    return candidates[:limit]


def contact_profile(conn: sqlite3.Connection, contact_id: int) -> dict[str, Any]:
    row = fetch_contact_row(conn, contact_id)
    due = compute_due_fields(row)
    return {
        "contact": contact_payload(conn, contact_id),
        "crm": {
            "importance": row["importance"],
            "cadence_days": row["cadence_days"],
            "paused_until": due["paused_until"],
            "last_in_person_at": due["last_in_person_at"],
            "last_contact_at": due["last_contact_at"],
            "next_due_at": due["next_due_at"],
            "overdue_days": due["overdue_days"],
            "status": due["status"],
            "notes_private": row["notes_private"],
            "home_area": row["home_area"],
            "best_times": row["best_times"],
        },
        "tags": contact_tags_grouped(conn, contact_id),
        "recent_interactions": recent_interactions(conn, contact_id),
        "suggestions": build_suggestions(conn, contact_id),
    }


def sync_calendar(conn: sqlite3.Connection, days_back: int, days_forward: int) -> dict[str, Any]:
    reference = now_local()
    start = (reference - timedelta(days=days_back)).date().isoformat()
    end = (reference + timedelta(days=days_forward + 1)).date().isoformat()
    events = run_gog_json(
        [
            "calendar",
            "events",
            DEFAULT_CALENDAR_ID,
            "--account",
            DEFAULT_CALENDAR_ACCOUNT,
            "--from",
            start,
            "--to",
            end,
            "--all-pages",
            "--max",
            "500",
        ]
    )
    if not isinstance(events, list):
        raise SystemExit("Expected gog calendar events to return a JSON array")

    index = build_contact_index(conn)
    touched: list[int] = []
    imported = 0
    duplicates = 0
    matched_events = 0

    for event in events:
        if event.get("status") == "cancelled":
            continue
        start_dt = parse_calendar_timestamp(event.get("start", {}))
        if start_dt is None or start_dt > reference:
            continue

        matched_contact_ids: set[int] = set()
        for attendee in event.get("attendees", []):
            email = normalize_lookup_text(attendee.get("email", ""))
            matched_contact_ids.update(index["email_map"].get(email, set()))

        haystack = normalize_lookup_text(" ".join(filter(None, [event.get("summary", ""), event.get("description", "")])))
        if haystack:
            for contact_id, terms in index["terms_map"].items():
                if any(phrase_matches(term, haystack) for term in terms):
                    matched_contact_ids.add(contact_id)

        if not matched_contact_ids:
            continue

        matched_events += 1
        event_id = event.get("id")
        for contact_id in sorted(matched_contact_ids):
            inserted = insert_interaction(
                conn,
                contact_id=contact_id,
                occurred_at=start_dt,
                interaction_type="in_person",
                source="calendar",
                calendar_event_id=event_id,
                calendar_event_title=event.get("summary"),
                duration_minutes_value=duration_minutes(event.get("start", {}), event.get("end", {})),
                location=event.get("location"),
                notes=None,
                counts_for_cadence=True,
            )
            if inserted:
                imported += 1
                touched.append(contact_id)
            else:
                duplicates += 1

    if touched:
        refresh_contact_cache(conn, touched)

    return {
        "calendar_account": DEFAULT_CALENDAR_ACCOUNT,
        "calendar_id": DEFAULT_CALENDAR_ID,
        "days_back": days_back,
        "days_forward": days_forward,
        "events_scanned": len(events),
        "events_matched": matched_events,
        "interactions_imported": imported,
        "duplicates_skipped": duplicates,
        "contacts_touched": len(set(touched)),
    }


def cmd_init(_: argparse.Namespace) -> None:
    with connect():
        pass
    print(json.dumps({"database": str(DB_PATH), "status": "ok"}, indent=2))


def cmd_migrate(args: argparse.Namespace) -> None:
    source_path = validate_migration_source(args.source)
    if not source_path.exists():
        raise SystemExit(f"Source markdown not found: {source_path}")
    contacts = parse_markdown(source_path)
    if not contacts:
        raise SystemExit(f"No contacts found in {source_path}")
    with connect() as conn:
        for contact in contacts:
            upsert_contact(conn, contact)
    backup_path = backup_file(source_path)
    if args.replace_with_stub:
        source_path.write_text(source_stub(DB_PATH, backup_path))
        os.chmod(source_path, 0o600)
    print(
        json.dumps(
            {
                "database": str(DB_PATH),
                "contacts_imported": len(contacts),
                "backup_path": str(backup_path),
                "source_replaced_with_stub": bool(args.replace_with_stub),
            },
            indent=2,
        )
    )


def cmd_list(_: argparse.Namespace) -> None:
    with connect() as conn:
        rows = conn.execute("SELECT id, display_name, preferred_name FROM contacts ORDER BY display_name").fetchall()
    print(json.dumps([dict(row) for row in rows], indent=2))


def cmd_search(args: argparse.Namespace) -> None:
    limit = max(1, min(args.limit, MAX_SEARCH_LIMIT))
    with connect() as conn:
        ids = resolve_contact_ids(conn, args.term)
        payload = [contact_payload(conn, contact_id) for contact_id in ids[:limit]]
    print(json.dumps(payload, indent=2))


def cmd_show(args: argparse.Namespace) -> None:
    with connect() as conn:
        ids = resolve_contact_ids(conn, args.identifier)
        if not ids:
            raise SystemExit(f"No contact matched: {args.identifier}")
        if len(ids) > 1:
            print(json.dumps({"matches": [contact_payload(conn, contact_id) for contact_id in ids]}, indent=2))
            return
        print(json.dumps(contact_payload(conn, ids[0]), indent=2))


def cmd_profile(args: argparse.Namespace) -> None:
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        print(json.dumps(contact_profile(conn, contact_id), indent=2))


def cmd_add_fact(args: argparse.Namespace) -> None:
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        conn.execute(
            "INSERT OR IGNORE INTO facts (contact_id, fact, fact_type) VALUES (?, ?, ?)",
            (contact_id, normalize_free_text(args.fact), args.fact_type),
        )
        conn.execute("UPDATE contacts SET updated_at = ? WHERE id = ?", (utc_now(), contact_id))
        print(json.dumps(contact_payload(conn, contact_id), indent=2))


def cmd_set_method(args: argparse.Namespace) -> None:
    kind = args.kind.lower()
    if kind not in VALID_METHOD_KINDS:
        raise SystemExit(f"Invalid method kind: {args.kind}")
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        conn.execute(
            """
            INSERT INTO methods (contact_id, kind, value, label, is_primary)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(contact_id, kind, value) DO UPDATE SET
                label = COALESCE(excluded.label, methods.label),
                is_primary = MAX(methods.is_primary, excluded.is_primary)
            """,
            (contact_id, kind, args.value.strip(), args.label, 1 if args.primary else 0),
        )
        conn.execute("UPDATE contacts SET updated_at = ? WHERE id = ?", (utc_now(), contact_id))
        print(json.dumps(contact_payload(conn, contact_id), indent=2))


def cmd_set_preferred_name(args: argparse.Namespace) -> None:
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        conn.execute(
            "UPDATE contacts SET preferred_name = ?, updated_at = ? WHERE id = ?",
            (args.preferred_name.strip(), utc_now(), contact_id),
        )
        conn.execute("INSERT OR IGNORE INTO aliases (contact_id, alias) VALUES (?, ?)", (contact_id, args.preferred_name.strip()))
        print(json.dumps(contact_payload(conn, contact_id), indent=2))


def cmd_set_importance(args: argparse.Namespace) -> None:
    importance = args.importance.lower()
    if importance not in VALID_IMPORTANCE:
        raise SystemExit(f"Invalid importance: {args.importance}")
    cadence_days = IMPORTANCE_TO_DAYS[importance]
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        conn.execute(
            "UPDATE contacts SET importance = ?, cadence_days = ?, updated_at = ? WHERE id = ?",
            (importance, cadence_days, utc_now(), contact_id),
        )
        print(json.dumps(contact_profile(conn, contact_id), indent=2))


def cmd_set_cadence(args: argparse.Namespace) -> None:
    cadence_days = max(1, args.days)
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        conn.execute(
            "UPDATE contacts SET cadence_days = ?, updated_at = ? WHERE id = ?",
            (cadence_days, utc_now(), contact_id),
            )
        print(json.dumps(contact_profile(conn, contact_id), indent=2))


def cmd_set_context(args: argparse.Namespace) -> None:
    updates: dict[str, Any] = {}
    if args.paused_until is not None:
        updates["paused_until"] = serialize_datetime(parse_iso_datetime(args.paused_until))
    if args.clear_paused:
        updates["paused_until"] = None
    if args.notes_private is not None:
        updates["notes_private"] = args.notes_private.strip() or None
    if args.home_area is not None:
        updates["home_area"] = args.home_area.strip() or None
    if args.best_times is not None:
        updates["best_times"] = args.best_times.strip() or None
    if not updates:
        raise SystemExit("No context fields provided")

    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        assignments = ", ".join(f"{column} = ?" for column in updates)
        params = list(updates.values()) + [utc_now(), contact_id]
        conn.execute(f"UPDATE contacts SET {assignments}, updated_at = ? WHERE id = ?", params)
        print(json.dumps(contact_profile(conn, contact_id), indent=2))


def cmd_add_tag(args: argparse.Namespace) -> None:
    tag_type = args.tag_type.lower()
    if tag_type not in VALID_TAG_TYPES:
        raise SystemExit(f"Invalid tag type: {args.tag_type}")
    tag = normalize_free_text(args.tag)
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        conn.execute(
            "INSERT OR IGNORE INTO contact_tags (contact_id, tag_type, tag) VALUES (?, ?, ?)",
            (contact_id, tag_type, tag),
        )
        conn.execute("UPDATE contacts SET updated_at = ? WHERE id = ?", (utc_now(), contact_id))
        print(json.dumps(contact_profile(conn, contact_id), indent=2))


def cmd_log_interaction(args: argparse.Namespace) -> None:
    interaction_type = args.type.lower()
    if interaction_type not in VALID_INTERACTION_TYPES:
        raise SystemExit(f"Invalid interaction type: {args.type}")
    source = args.source.lower()
    if source not in VALID_INTERACTION_SOURCES:
        raise SystemExit(f"Invalid interaction source: {args.source}")
    occurred_at = parse_iso_datetime(args.at)
    if occurred_at is None:
        raise SystemExit(f"Invalid interaction timestamp: {args.at}")

    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        insert_interaction(
            conn,
            contact_id=contact_id,
            occurred_at=occurred_at,
            interaction_type=interaction_type,
            source=source,
            duration_minutes_value=args.duration_minutes,
            location=args.location,
            notes=args.notes,
            counts_for_cadence=(interaction_type == "in_person"),
        )
        refresh_contact_cache(conn, [contact_id])
        print(json.dumps(contact_profile(conn, contact_id), indent=2))


def cmd_sync_calendar(args: argparse.Namespace) -> None:
    with connect() as conn:
        payload = sync_calendar(conn, days_back=max(0, args.days_back), days_forward=max(0, args.days_forward))
    print(json.dumps(payload, indent=2))


def cmd_due_list(args: argparse.Namespace) -> None:
    status_filter = args.status.lower()
    if status_filter not in {"overdue", "due-soon", "all"}:
        raise SystemExit(f"Invalid status: {args.status}")

    reference = now_local()
    due_soon_cutoff = reference + timedelta(days=max(0, args.within_days))
    entries: list[dict[str, Any]] = []

    with connect() as conn:
        rows = conn.execute("SELECT * FROM contacts ORDER BY display_name").fetchall()
        for row in rows:
            due = compute_due_fields(row, reference)
            if due["status"] == "paused":
                continue
            next_due_dt = parse_iso_datetime(due["next_due_at"])
            status = due["status"]
            if status == "on_track" and next_due_dt and next_due_dt <= due_soon_cutoff:
                status = "due-soon"
            if status_filter == "overdue" and status != "overdue":
                continue
            if status_filter == "due-soon" and status != "due-soon":
                continue
            entries.append(
                {
                    "contact_id": row["id"],
                    "display_name": row["display_name"],
                    "preferred_name": row["preferred_name"],
                    "importance": row["importance"],
                    "cadence_days": row["cadence_days"],
                    "last_in_person_at": due["last_in_person_at"],
                    "last_contact_at": due["last_contact_at"],
                    "next_due_at": due["next_due_at"],
                    "overdue_days": due["overdue_days"],
                    "status": status,
                    "suggestions": build_suggestions(conn, row["id"]),
                }
            )

    def sort_key(entry: dict[str, Any]) -> tuple[int, int, int, str]:
        status_rank = {"overdue": 0, "due-soon": 1, "on_track": 2}.get(entry["status"], 3)
        overdue_rank = entry["overdue_days"] if entry["overdue_days"] is not None else 10**9
        last_seen = entry["last_in_person_at"] or ""
        return (status_rank, -overdue_rank, importance_rank(entry["importance"]), last_seen)

    entries.sort(key=sort_key)
    print(json.dumps(entries, indent=2))


def cmd_suggest(args: argparse.Namespace) -> None:
    with connect() as conn:
        contact_id = require_single_contact(conn, args.identifier)
        row = fetch_contact_row(conn, contact_id)
        payload = {
            "id": contact_id,
            "display_name": row["display_name"],
            "preferred_name": row["preferred_name"],
            "suggestions": build_suggestions(conn, contact_id),
        }
    print(json.dumps(payload, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the local OpenClaw friends database and friend CRM.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create or upgrade the database if missing.")
    init_parser.set_defaults(func=cmd_init)

    migrate_parser = subparsers.add_parser("migrate", help="Import contacts from friends.md into SQLite.")
    migrate_parser.add_argument("--source", required=True, help="Path to the source markdown file.")
    migrate_parser.add_argument("--replace-with-stub", action="store_true", help="Rewrite the source markdown as a stub after import.")
    migrate_parser.set_defaults(func=cmd_migrate)

    list_parser = subparsers.add_parser("list", help="List all contacts.")
    list_parser.set_defaults(func=cmd_list)

    search_parser = subparsers.add_parser("search", help="Search contacts by name, alias, email, phone, fact text, or tag.")
    search_parser.add_argument("term", help="Search text.")
    search_parser.add_argument("--limit", type=int, default=10, help=f"Max results to return (1-{MAX_SEARCH_LIMIT}).")
    search_parser.set_defaults(func=cmd_search)

    show_parser = subparsers.add_parser("show", help="Show one contact or all matches for an ambiguous identifier.")
    show_parser.add_argument("identifier", help="Display name, alias, email, phone, or search text.")
    show_parser.set_defaults(func=cmd_show)

    profile_parser = subparsers.add_parser("profile", help="Show one contact's CRM profile.")
    profile_parser.add_argument("identifier", help="Display name, alias, email, phone, or search text.")
    profile_parser.set_defaults(func=cmd_profile)

    fact_parser = subparsers.add_parser("add-fact", help="Add a fact to one contact.")
    fact_parser.add_argument("identifier", help="Contact name or alias.")
    fact_parser.add_argument("fact", help="Fact text.")
    fact_parser.add_argument("--fact-type", default="note", help="Fact type label.")
    fact_parser.set_defaults(func=cmd_add_fact)

    method_parser = subparsers.add_parser("set-method", help="Add a method to one contact.")
    method_parser.add_argument("identifier", help="Contact name or alias.")
    method_parser.add_argument("kind", help="email | phone | imessage | sms | other")
    method_parser.add_argument("value", help="Method value.")
    method_parser.add_argument("--label", help="Optional human-readable label.")
    method_parser.add_argument("--primary", action="store_true", help="Mark as primary.")
    method_parser.set_defaults(func=cmd_set_method)

    preferred_parser = subparsers.add_parser("set-preferred-name", help="Set a contact's preferred name.")
    preferred_parser.add_argument("identifier", help="Contact name or alias.")
    preferred_parser.add_argument("preferred_name", help="Preferred name to store.")
    preferred_parser.set_defaults(func=cmd_set_preferred_name)

    importance_parser = subparsers.add_parser("set-importance", help="Set a contact's importance and default cadence.")
    importance_parser.add_argument("identifier", help="Contact name or alias.")
    importance_parser.add_argument("importance", help="high | medium | low")
    importance_parser.set_defaults(func=cmd_set_importance)

    cadence_parser = subparsers.add_parser("set-cadence", help="Override a contact's cadence target in days.")
    cadence_parser.add_argument("identifier", help="Contact name or alias.")
    cadence_parser.add_argument("days", type=int, help="Cadence target in days.")
    cadence_parser.set_defaults(func=cmd_set_cadence)

    context_parser = subparsers.add_parser("set-context", help="Set private CRM context such as notes, area, timing, or pause.")
    context_parser.add_argument("identifier", help="Contact name or alias.")
    context_parser.add_argument("--paused-until", help="Pause the contact until this ISO timestamp or date.")
    context_parser.add_argument("--clear-paused", action="store_true", help="Remove any pause.")
    context_parser.add_argument("--notes-private", help="Private CRM note.")
    context_parser.add_argument("--home-area", help="Home area or neighborhood.")
    context_parser.add_argument("--best-times", help="Best times to hang out.")
    context_parser.set_defaults(func=cmd_set_context)

    tag_parser = subparsers.add_parser("add-tag", help="Add a structured tag to one contact.")
    tag_parser.add_argument("identifier", help="Contact name or alias.")
    tag_parser.add_argument("tag_type", help="interest | activity | neighborhood | group")
    tag_parser.add_argument("tag", help="Tag value.")
    tag_parser.set_defaults(func=cmd_add_tag)

    interaction_parser = subparsers.add_parser("log-interaction", help="Log one interaction for a contact.")
    interaction_parser.add_argument("identifier", help="Contact name or alias.")
    interaction_parser.add_argument("--type", required=True, help="in_person | call | text | email")
    interaction_parser.add_argument("--at", required=True, help="Interaction timestamp as ISO datetime or date.")
    interaction_parser.add_argument("--duration-minutes", type=int, help="Optional interaction duration in minutes.")
    interaction_parser.add_argument("--location", help="Optional interaction location.")
    interaction_parser.add_argument("--source", default="manual", help="manual | calendar")
    interaction_parser.add_argument("--notes", help="Optional interaction notes.")
    interaction_parser.set_defaults(func=cmd_log_interaction)

    sync_parser = subparsers.add_parser("sync-calendar", help="Import in-person interactions from calendar history.")
    sync_parser.add_argument("--days-back", type=int, default=180, help="How far back to scan for events.")
    sync_parser.add_argument("--days-forward", type=int, default=0, help="Optional forward look window; only past events count.")
    sync_parser.set_defaults(func=cmd_sync_calendar)

    due_parser = subparsers.add_parser("due-list", help="Show which friends are overdue or due soon.")
    due_parser.add_argument("--within-days", type=int, default=14, help="Window for due-soon contacts.")
    due_parser.add_argument("--status", default="overdue", help="overdue | due-soon | all")
    due_parser.set_defaults(func=cmd_due_list)

    suggest_parser = subparsers.add_parser("suggest", help="Show activity suggestions for one contact.")
    suggest_parser.add_argument("identifier", help="Contact name or alias.")
    suggest_parser.set_defaults(func=cmd_suggest)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
