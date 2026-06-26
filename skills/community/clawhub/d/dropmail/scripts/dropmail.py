#!/usr/bin/env python3
"""
dropmail.py — CLI for disposable email management via GuerrillaMail API + local SQLite DB.

Usage:
  dropmail new                        Get a new disposable email address
  dropmail list                       List all tracked email addresses
  dropmail <email> inbox              Show all messages in inbox
  dropmail <email> inbox -c <n>       Show last n messages
  dropmail <email> read <id>          Read a specific message by ID
  dropmail <email> refresh            Refresh inbox from API
  dropmail <email> remove             Remove email from local DB
  dropmail <email> expire             Check remaining time before expiry
"""

import argparse
import json
import os
import re
import sqlite3
import ssl
import sys
import time
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.parse

# ── Config ────────────────────────────────────────────────────────────────────
DB_DIR = Path.home() / ".dropmail"
DB_PATH = DB_DIR / "dropmail.db"

# macOS Python (python.org installer) doesn't bundle system CA certs.
# Use certifi if available, otherwise fall back to unverified context.
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl._create_unverified_context()
API_BASE = "https://api.guerrillamail.com/ajax.php"
SESSION_FILE = DB_DIR / "sessions.json"

# ── DB Setup ──────────────────────────────────────────────────────────────────
def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS emails (
            email       TEXT PRIMARY KEY,
            created_at  INTEGER NOT NULL,
            expires_at  INTEGER NOT NULL,
            session_id  TEXT,
            subscr      TEXT
        );
        CREATE TABLE IF NOT EXISTS messages (
            id          TEXT PRIMARY KEY,
            email       TEXT NOT NULL,
            mail_from   TEXT,
            subject     TEXT,
            excerpt     TEXT,
            body        TEXT,
            received_at INTEGER,
            read        INTEGER DEFAULT 0,
            FOREIGN KEY(email) REFERENCES emails(email)
        );
    """)
    con.commit()
    return con


# ── Session helpers ───────────────────────────────────────────────────────────
def load_sessions():
    if SESSION_FILE.exists():
        return json.loads(SESSION_FILE.read_text())
    return {}


def save_sessions(sessions):
    SESSION_FILE.write_text(json.dumps(sessions, indent=2))


def api_call(params: dict, email: str = None) -> dict:
    """Make an API call, maintaining per-email session cookies."""
    sessions = load_sessions()
    key = email or "__default__"
    session_data = sessions.get(key, {})

    params.setdefault("ip", "127.0.0.1")
    params.setdefault("agent", "Mozilla_foo_bar")

    url = f"{API_BASE}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)

    # Inject saved PHPSESSID
    if "phpsessid" in session_data:
        req.add_header("Cookie", f"PHPSESSID={session_data['phpsessid']}")
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0")

    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0")
    try:
        with urllib.request.urlopen(req, timeout=10, context=_SSL_CTX) as resp:
            raw = resp.read().decode()
            data = json.loads(raw)

            # Extract and persist new PHPSESSID from response headers
            set_cookie = resp.getheader("Set-Cookie", "")
            if "PHPSESSID=" in set_cookie:
                for part in set_cookie.split(";"):
                    part = part.strip()
                    if part.startswith("PHPSESSID="):
                        session_data["phpsessid"] = part.split("=", 1)[1]
                        break

            sessions[key] = session_data
            save_sessions(sessions)
            return data
    except Exception as e:
        print(f"[error] API call failed: {e}", file=sys.stderr)
        sys.exit(1)


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_new(args, con):
    """Fetch a new disposable email address."""
    data = api_call({"f": "get_email_address", "lang": "en"})
    email = data.get("email_addr", "")
    ts = int(data.get("email_timestamp", time.time()))
    expires_at = ts + 3600  # 1 hour TTL

    cur = con.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO emails (email, created_at, expires_at) VALUES (?, ?, ?)",
        (email, ts, expires_at)
    )
    con.commit()

    remaining = max(0, expires_at - int(time.time()))
    print(f"✉  New email address: {email}")
    print(f"⏰  Expires in ~{remaining // 60}m {remaining % 60}s")
    print(f"💡  Copy this address anywhere you need to avoid spam.")


def cmd_list(args, con):
    """List all tracked email addresses."""
    cur = con.cursor()
    rows = cur.execute(
        "SELECT email, created_at, expires_at FROM emails ORDER BY created_at DESC"
    ).fetchall()

    if not rows:
        print("No email addresses tracked yet. Run: dropmail new")
        return

    now = int(time.time())
    print(f"{'EMAIL':<35} {'CREATED':<20} {'STATUS':<15}")
    print("-" * 72)
    for email, created_at, expires_at in rows:
        created = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M")
        if expires_at < now:
            status = "⛔ expired"
        else:
            rem = expires_at - now
            status = f"⏱ {rem // 60}m {rem % 60}s left"
        print(f"{email:<35} {created:<20} {status:<15}")


def cmd_inbox(args, con, email):
    """Show messages in an inbox, optionally limited to last n."""
    cur = con.cursor()

    # Check email exists
    row = cur.execute("SELECT 1 FROM emails WHERE email=?", (email,)).fetchone()
    if not row:
        print(f"[error] Email not tracked: {email}. Add it first with: dropmail new")
        sys.exit(1)

    query = "SELECT id, mail_from, subject, excerpt, received_at, read FROM messages WHERE email=? ORDER BY received_at DESC"
    params = [email]
    rows = cur.execute(query, params).fetchall()

    count = getattr(args, 'count', None)
    if count:
        rows = rows[:count]

    if not rows:
        print(f"📭  No messages in {email}")
        print(f"   Tip: run 'dropmail {email} refresh' to fetch from server")
        return

    print(f"\n📬  Inbox: {email} ({len(rows)} message{'s' if len(rows) != 1 else ''})\n")
    print(f"  {'ID':<12} {'FROM':<30} {'SUBJECT':<35} {'DATE':<16} {'READ'}")
    print("  " + "-" * 100)
    for msg_id, mail_from, subject, excerpt, received_at, read in rows:
        date_str = datetime.fromtimestamp(received_at).strftime("%m-%d %H:%M") if received_at else "?"
        read_mark = "✓" if read else "●"
        from_trunc = (mail_from or "")[:29]
        subj_trunc = (subject or "(no subject)")[:34]
        print(f"  {msg_id:<12} {from_trunc:<30} {subj_trunc:<35} {date_str:<16} {read_mark}")
    print(f"\n  Use: dropmail {email} read <id>  to read a message")


def cmd_refresh(args, con, email):
    """Fetch latest messages from the API for a tracked email."""
    cur = con.cursor()
    row = cur.execute("SELECT 1 FROM emails WHERE email=?", (email,)).fetchone()
    if not row:
        print(f"[error] Email not tracked: {email}")
        sys.exit(1)

    # Set the email user in the API session
    username = email.split("@")[0]
    api_call({"f": "set_email_user", "email_user": username, "lang": "en"}, email=email)

    # Fetch messages
    data = api_call({"f": "check_email", "seq": "0"}, email=email)
    msgs = data.get("list", [])

    new_count = 0
    for m in msgs:
        existing = cur.execute("SELECT 1 FROM messages WHERE id=?", (str(m["mail_id"]),)).fetchone()
        if not existing:
            cur.execute(
                "INSERT OR IGNORE INTO messages (id, email, mail_from, subject, excerpt, received_at, read) VALUES (?,?,?,?,?,?,?)",
                (str(m["mail_id"]), email, m.get("mail_from"), m.get("mail_subject"),
                 m.get("mail_excerpt"), int(m.get("mail_timestamp", time.time())), int(m.get("mail_read", 0)))
            )
            new_count += 1

    con.commit()
    total = cur.execute("SELECT COUNT(*) FROM messages WHERE email=?", (email,)).fetchone()[0]
    print(f"🔄  Refreshed {email}: {new_count} new message(s). Total: {total}")


def cmd_read(args, con, email, msg_id):
    """Read a specific message, fetching full body if needed."""
    cur = con.cursor()
    row = cur.execute(
        "SELECT id, mail_from, subject, body, received_at FROM messages WHERE id=? AND email=?",
        (msg_id, email)
    ).fetchone()

    if not row:
        print(f"[error] Message {msg_id} not found. Try 'dropmail {email} refresh' first.")
        sys.exit(1)

    _, mail_from, subject, body, received_at = row

    # Fetch full body if not cached
    if not body:
        data = api_call({"f": "fetch_email", "email_id": msg_id}, email=email)
        body = data.get("mail_body", "(empty)")
        # Strip basic HTML tags
        import re
        body = re.sub(r"<[^>]+>", "", body)
        body = body.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        cur.execute("UPDATE messages SET body=?, read=1 WHERE id=?", (body, msg_id))
        con.commit()
    else:
        cur.execute("UPDATE messages SET read=1 WHERE id=?", (msg_id,))
        con.commit()

    date_str = datetime.fromtimestamp(received_at).strftime("%Y-%m-%d %H:%M") if received_at else "?"
    print(f"\n{'─'*60}")
    print(f"From:    {mail_from}")
    print(f"Subject: {subject}")
    print(f"Date:    {date_str}")
    print(f"{'─'*60}\n")
    print(body.strip())
    print(f"\n{'─'*60}")


def cmd_remove(args, con, email):
    """Remove an email address and all its messages from local DB."""
    cur = con.cursor()
    row = cur.execute("SELECT 1 FROM emails WHERE email=?", (email,)).fetchone()
    if not row:
        print(f"[error] Email not found: {email}")
        sys.exit(1)

    msg_count = cur.execute("SELECT COUNT(*) FROM messages WHERE email=?", (email,)).fetchone()[0]
    cur.execute("DELETE FROM messages WHERE email=?", (email,))
    cur.execute("DELETE FROM emails WHERE email=?", (email,))
    con.commit()

    # Clean up session
    sessions = load_sessions()
    sessions.pop(email, None)
    save_sessions(sessions)

    print(f"🗑   Removed {email} and {msg_count} message(s) from local DB.")


def cmd_expire(args, con, email):
    """Show time remaining before email expires."""
    cur = con.cursor()
    row = cur.execute("SELECT expires_at FROM emails WHERE email=?", (email,)).fetchone()
    if not row:
        print(f"[error] Email not tracked: {email}")
        sys.exit(1)

    expires_at = row[0]
    now = int(time.time())
    remaining = expires_at - now

    if remaining <= 0:
        print(f"⛔  {email} has expired.")
    else:
        print(f"⏰  {email} expires in {remaining // 60}m {remaining % 60}s")
        print(f"   Expiry: {datetime.fromtimestamp(expires_at).strftime('%Y-%m-%d %H:%M:%S')}")


# ── CLI Parser ────────────────────────────────────────────────────────────────
def build_parser():
    parser = argparse.ArgumentParser(
        prog="dropmail",
        description="Disposable email manager powered by GuerrillaMail"
    )
    sub = parser.add_subparsers(dest="command")

    # dropmail new
    sub.add_parser("new", help="Get a new disposable email address")

    # dropmail list
    sub.add_parser("list", help="List all tracked email addresses")

    # dropmail <email> inbox [-c N]
    inbox_p = sub.add_parser("inbox", help="Show inbox for an email")
    inbox_p.add_argument("email")
    inbox_p.add_argument("-c", "--count", type=int, default=None,
                         help="Limit to last N messages")

    # dropmail <email> refresh
    refresh_p = sub.add_parser("refresh", help="Fetch new messages from server")
    refresh_p.add_argument("email")

    # dropmail <email> read <id>
    read_p = sub.add_parser("read", help="Read a specific message")
    read_p.add_argument("email")
    read_p.add_argument("id", help="Message ID")

    # dropmail <email> remove
    remove_p = sub.add_parser("remove", help="Remove email from local DB")
    remove_p.add_argument("email")

    # dropmail <email> expire
    expire_p = sub.add_parser("expire", help="Check time remaining before expiry")
    expire_p.add_argument("email")

    return parser


def main():
    # Handle positional syntax: dropmail <email> inbox / refresh / remove / expire / read <id>
    # Rewrite to subcommand form
    argv = sys.argv[1:]
    if len(argv) >= 2 and "@" in argv[0]:
        email = argv[0]
        cmd = argv[1]
        rest = argv[2:]
        if cmd in ("inbox", "refresh", "remove", "expire"):
            argv = [cmd, email] + rest
        elif cmd == "read" and rest:
            argv = ["read", email, rest[0]]
    sys.argv[1:] = argv

    parser = build_parser()
    args = parser.parse_args()

    con = init_db()

    if args.command == "new":
        cmd_new(args, con)
    elif args.command == "list":
        cmd_list(args, con)
    elif args.command == "inbox":
        cmd_inbox(args, con, args.email)
    elif args.command == "refresh":
        cmd_refresh(args, con, args.email)
    elif args.command == "read":
        cmd_read(args, con, args.email, args.id)
    elif args.command == "remove":
        cmd_remove(args, con, args.email)
    elif args.command == "expire":
        cmd_expire(args, con, args.email)
    else:
        parser.print_help()

    con.close()


if __name__ == "__main__":
    main()
