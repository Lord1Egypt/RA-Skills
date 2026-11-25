#!/usr/bin/env python3
"""Initialize the portable email CRM database."""
import argparse

from email_crm import add_db_argument, connect, emit, initialize, resolve_db_path

parser = argparse.ArgumentParser()
add_db_argument(parser)
args = parser.parse_args()
conn = connect(args.db)
try:
    version = initialize(conn)
    emit({"ok": True, "schema_version": version, "db": str(resolve_db_path(args.db))})
finally:
    conn.close()
