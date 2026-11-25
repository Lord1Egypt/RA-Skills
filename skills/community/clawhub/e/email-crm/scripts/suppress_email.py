#!/usr/bin/env python3
"""Idempotently suppress an email and synchronize contact DNC state."""
import argparse

from email_crm import add_db_argument, add_email_arguments, connect, emit, initialize, normalize_email, read_email_argument, utc_now

parser = argparse.ArgumentParser()
add_db_argument(parser)
add_email_arguments(parser)
parser.add_argument("--reason", required=True, choices=("unsubscribe", "manual_dnc", "bounce", "complaint", "policy"))
args = parser.parse_args()

try:
    email = normalize_email(read_email_argument(args))
except ValueError as exc:
    parser.error(str(exc))

conn = connect(args.db)
try:
    initialize(conn)
    conn.execute(
        "INSERT INTO email_suppressions (email_normalized, reason, created_at) VALUES (?, ?, ?) "
        "ON CONFLICT(email_normalized) DO NOTHING",
        (email, args.reason, utc_now()),
    )
    updated = conn.execute("UPDATE contacts SET do_not_contact = 1, updated_at = ? WHERE email_normalized = ?", (utc_now(), email)).rowcount
    persisted = conn.execute(
        "SELECT reason FROM email_suppressions WHERE email_normalized = ?", (email,)
    ).fetchone()
    conn.commit()
    emit({"ok": True, "contacts_marked_do_not_contact": updated, "reason": persisted["reason"]})
finally:
    conn.close()
