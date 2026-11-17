#!/usr/bin/env python3
"""List or dump opencode (sst/opencode) sessions from its local SQLite store.

Stdlib only. Read-only access (opens the DB with mode=ro so a live writer is
never disturbed). Secrets are redacted unless --show-sensitive is used.

Usage:
  python dump_opencode_session.py --list [--keyword AP] [-n 30]
  python dump_opencode_session.py --id ses_xxx --final-assistant
  python dump_opencode_session.py --id ses_xxx [--user-only] [--last 40] [--chars 2000]
"""
import argparse
import datetime
import json
import os
import sqlite3
import sys
from pathlib import Path

from session_utils import ensure_utf8_stdout, redact_text, truncate_text

DEFAULT_DB = os.path.expanduser(os.path.join("~", ".local", "share", "opencode", "opencode.db"))


def connect(path):
    db_path = Path(os.path.expanduser(path)).resolve()
    if not db_path.exists():
        sys.exit(f"opencode DB not found: {db_path}")
    try:
        uri = db_path.as_uri() + "?mode=ro"
        return sqlite3.connect(uri, uri=True)
    except (sqlite3.Error, ValueError) as exc:
        sys.exit(f"cannot open opencode DB read-only: {exc}")


def fmt_ts(ms):
    if not ms:
        return "?"
    return datetime.datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M")


def visible(text, show_sensitive):
    if show_sensitive or not text:
        return text or ""
    return redact_text(text)[0]


def list_sessions(db, n, keyword, show_sensitive):
    rows = db.execute(
        "SELECT id, title, directory, parent_id, time_created, time_updated FROM session"
    ).fetchall()
    rows.sort(key=lambda row: row[5] or 0, reverse=True)
    if keyword:
        needle = keyword.casefold()
        rows = [
            row
            for row in rows
            if needle in (row[1] or "").casefold()
            or needle in (row[2] or "").casefold()
        ]
    if not rows:
        print("no sessions match")
        return
    for sid, title, directory, parent, created, updated in rows[:n]:
        sub = f"  [subagent of {parent}]" if parent else ""
        print(f"{sid}\n    {fmt_ts(created)} -> {fmt_ts(updated)}  {directory}")
        print(f"    title: {visible(title, show_sensitive)}{sub}")


def text_of_parts(db, message_id, show_sensitive):
    out = []
    for (data,) in db.execute(
        "SELECT data FROM part WHERE message_id=? ORDER BY time_created", (message_id,)
    ):
        try:
            part = json.loads(data)
        except Exception:
            continue
        if part.get("type") == "text" and part.get("text"):
            out.append(visible(part["text"], show_sensitive))
    return "\n".join(out).strip()


def dump(db, sid, args):
    row = db.execute("SELECT title, directory FROM session WHERE id=?", (sid,)).fetchone()
    if row is None:
        sys.exit(f"opencode session not found: {sid}")
    print(f"# {visible(row[0], args.show_sensitive)}")
    print(f"# dir: {row[1]}")
    print(f"# id: {sid}")

    rows = db.execute(
        "SELECT id, data, time_created FROM message WHERE session_id=? ORDER BY time_created",
        (sid,),
    ).fetchall()
    messages = []
    for message_id, data, created in rows:
        try:
            payload = json.loads(data)
        except Exception:
            continue
        role = payload.get("role") or "?"
        if args.role != "all" and role != args.role:
            continue
        text = text_of_parts(db, message_id, args.show_sensitive)
        if text:
            messages.append((role, text, created))

    if args.last:
        messages = messages[-args.last:]

    if args.show_sensitive:
        print("# WARNING: sensitive redaction disabled")
    print(f"# {len(messages)} messages\n")
    for role, text, created in messages:
        print(f"\n=== {role.upper()} [{fmt_ts(created)}] ===")
        print(truncate_text(text, args.chars))

    subs = db.execute("SELECT id, title FROM session WHERE parent_id=?", (sid,)).fetchall()
    if subs:
        print("\n# subagent sessions:")
        for sub_id, title in subs:
            print(f"  {sub_id}  {visible(title, args.show_sensitive)}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--db", default=DEFAULT_DB, help="path to opencode.db")
    parser.add_argument("--list", action="store_true", help="list recent sessions")
    parser.add_argument("--keyword", help="filter session list by title/directory")
    parser.add_argument("-n", type=int, default=30, help="max sessions to list")
    parser.add_argument("--id", help="session id to dump (ses_...)")
    parser.add_argument("--role", choices=("all", "user", "assistant", "summary"),
                        default="all", help="only print this role (default: all)")
    parser.add_argument("--user-only", action="store_true",
                        help="legacy alias for --role user")
    parser.add_argument(
        "--final-assistant",
        action="store_true",
        help="shorthand for --role assistant --last 1 --chars 0",
    )
    parser.add_argument("--last", type=int, default=0,
                        help="only the last N messages AFTER role filtering")
    parser.add_argument("--chars", type=int, default=2000,
                        help="max chars per message; 0 means unlimited")
    parser.add_argument("--show-sensitive", action="store_true",
                        help="disable secret redaction (only for explicit local inspection)")
    args = parser.parse_args()

    if args.n < 1 or args.last < 0 or args.chars < 0:
        parser.error("-n must be >= 1; --last and --chars must be >= 0")
    if args.final_assistant:
        args.role = "assistant"
        args.last = 1
        args.chars = 0
    if args.user_only:
        args.role = "user"

    ensure_utf8_stdout()
    db = connect(args.db)
    try:
        if args.id:
            dump(db, args.id, args)
        else:
            list_sessions(db, args.n, args.keyword, args.show_sensitive)
    except sqlite3.Error as exc:
        sys.exit(f"cannot read opencode DB: {exc}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
