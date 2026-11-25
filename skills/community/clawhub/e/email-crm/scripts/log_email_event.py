#!/usr/bin/env python3
"""Append a non-sensitive email lifecycle event."""
import argparse

from email_crm import EVENT_TYPES, add_db_argument, connect, emit, initialize, parse_metadata, utc_now

parser = argparse.ArgumentParser()
add_db_argument(parser)
parser.add_argument("--contact-id", required=True, type=int)
parser.add_argument("--event-type", required=True, choices=EVENT_TYPES)
parser.add_argument("--metadata-json")
args = parser.parse_args()

try:
    metadata = parse_metadata(args.metadata_json)
except ValueError as exc:
    parser.error(f"metadata-json must be valid JSON: {exc}")

conn = connect(args.db)
try:
    initialize(conn)
    cursor = conn.execute(
        "INSERT INTO email_events (contact_id, event_type, metadata_json, occurred_at) VALUES (?, ?, ?, ?)",
        (args.contact_id, args.event_type, metadata, utc_now()),
    )
    conn.commit()
    emit({"ok": True, "event_id": cursor.lastrowid, "contact_id": args.contact_id, "event_type": args.event_type})
finally:
    conn.close()
