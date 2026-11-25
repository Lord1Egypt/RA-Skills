#!/usr/bin/env python3
"""Return a deterministic, fail-closed email readiness decision."""
import argparse
import sys

from email_crm import add_db_argument, add_email_arguments, connect, emit, initialize, normalize_email, read_email_argument

parser = argparse.ArgumentParser()
add_db_argument(parser)
add_email_arguments(parser)
args = parser.parse_args()

try:
    email = normalize_email(read_email_argument(args))
except ValueError:
    emit({"ready": False, "reasons": ["invalid_email"]})
    sys.exit(1)

conn = connect(args.db)
try:
    initialize(conn)
    contact = conn.execute("SELECT id, source, do_not_contact FROM contacts WHERE email_normalized = ?", (email,)).fetchone()
    suppression = conn.execute("SELECT 1 FROM email_suppressions WHERE email_normalized = ?", (email,)).fetchone()
    reasons = []
    if contact is None:
        reasons.append("contact_not_found")
    else:
        if not contact["source"].strip():
            reasons.append("missing_source")
        if contact["do_not_contact"]:
            reasons.append("contact_do_not_contact")
    if suppression is not None:
        reasons.append("email_suppressed")
    emit({"ready": not reasons, "reasons": reasons, "contact_id": contact["id"] if contact else None})
    if reasons:
        sys.exit(1)
finally:
    conn.close()
