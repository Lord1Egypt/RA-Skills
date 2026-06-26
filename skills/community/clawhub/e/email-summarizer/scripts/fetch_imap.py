#!/usr/bin/env python3
"""
fetch_imap.py — Fetch emails from an IMAP mailbox and write a JSON file.

Output JSON format:
  {
    "source":  "imap",
    "owner":   "you@163.com",
    "since":   "01-Mar-2026",
    "until":   "28-Mar-2026",
    "emails":  [ { id, direction, date, from, to, cc, subject, body }, ... ]
  }

Usage:
  export EMAIL_USER=you@163.com
  export EMAIL_PASS=your-app-password

  # Fetch last 7 days → emails.json
  python3 fetch_imap.py --days 7 --output emails.json

  # Fetch inbox + sent, custom date range
  python3 fetch_imap.py --since 2026-03-01 --until 2026-03-28 --with-sent --output emails.json

  # Print to stdout (pipe to build_report.py)
  python3 fetch_imap.py --days 30 | python3 build_report.py --output report

Supported --preset values:
  163 (default) | qq | exmail | gmail | outlook

Environment variables:
  EMAIL_USER    Mailbox address
  EMAIL_PASS    IMAP app password (not your login password)
  IMAP_HOST     Custom IMAP host (overrides --preset)
  IMAP_PORT     Custom IMAP port (default 993)
"""

import argparse, email, email.header, email.utils, imaplib
import json, os, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _core import decode_header, get_body, IMAP_DATE_FMT


# ── IMAP presets ──────────────────────────────────────────────────────────────
# (imap_host, port, sent_folder_name)
PRESETS = {
    "163":     ("imap.163.com",          993, "已发送"),
    "qq":      ("imap.qq.com",           993, "Sent Messages"),
    "exmail":  ("imap.exmail.qq.com",    993, "Sent Messages"),
    "gmail":   ("imap.gmail.com",        993, "[Gmail]/Sent Mail"),
    "outlook": ("outlook.office365.com", 993, "Sent Items"),
}


class _IMAP4_SSL_WithID(imaplib.IMAP4_SSL):
    """IMAP4_SSL with RFC 2971 ID support (required by 163/188 servers)."""
    def send_id(self, name="EmailSummarizer", version="1.0", vendor="OpenClaw"):
        tag = self._new_tag()
        cmd = f'{tag.decode()} ID ("name" "{name}" "version" "{version}" "vendor" "{vendor}")\r\n'
        self.send(cmd.encode())
        while True:
            resp = self.readline()
            if resp.startswith(tag):
                return resp


def _imap_utf7(s: str) -> str:
    """Encode a Unicode string to IMAP modified UTF-7 (RFC 3501)."""
    import base64
    res, non_ascii = [], []

    def flush():
        if non_ascii:
            enc = base64.b64encode("".join(non_ascii).encode("utf-16-be")).decode("ascii")
            res.append(f"&{enc}-")
            non_ascii.clear()

    for ch in s:
        if ord(ch) < 128 and ch != "&":
            flush(); res.append(ch)
        elif ch == "&":
            flush(); res.append("&-")
        else:
            non_ascii.append(ch)
    flush()
    return "".join(res)


def _connect(user: str, password: str, host: str, port: int):
    try:
        mail = _IMAP4_SSL_WithID(host, port)
        mail.login(user, password)
        try:
            mail.send_id()
        except Exception:
            pass
        return mail
    except imaplib.IMAP4.error as e:
        print(f"[error] Login failed: {e}", file=sys.stderr)
        print("Hint: enable IMAP in mailbox settings and use an app password.", file=sys.stderr)
        sys.exit(1)


def _fetch_folder(mail, folder: str, since_str: str, until_str: str,
                  max_count: int, direction: str) -> list:
    """Fetch emails from one folder. Returns list of email dicts."""
    # Try UTF-7 encoded name, then raw, then unquoted
    for name in (f'"{_imap_utf7(folder)}"', f'"{folder}"', folder):
        status, _ = mail.select(name, readonly=True)
        if status == "OK":
            break
    if status != "OK":
        print(f"[skip] Cannot select folder: {folder}", file=sys.stderr)
        return []

    criteria = f'SINCE "{since_str}"'
    if until_str:
        criteria += f' BEFORE "{until_str}"'
    print(f"[search] {folder}: {criteria}", file=sys.stderr)
    _, data = mail.search(None, criteria)
    ids = data[0].split()
    print(f"[found]  {len(ids)} email(s) in {folder}", file=sys.stderr)

    ids = list(reversed(ids[-max_count:] if len(ids) > max_count else ids))
    results = []
    for i, uid in enumerate(ids):
        print(f"[fetch]  {folder} {i+1}/{len(ids)}", file=sys.stderr, end="\r")
        _, msg_data = mail.fetch(uid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        date_str = msg.get("Date", "")
        try:
            date_iso = email.utils.parsedate_to_datetime(date_str).isoformat()
        except Exception:
            date_iso = date_str

        results.append({
            "id":        uid.decode(),
            "direction": direction,
            "date":      date_iso,
            "from":      decode_header(msg.get("From", "")),
            "to":        decode_header(msg.get("To",   "")),
            "cc":        decode_header(msg.get("Cc",   "")),
            "subject":   decode_header(msg.get("Subject", "(no subject)")),
            "body":      get_body(msg),
        })

    print(f"\n[done]   {folder}: {len(results)} fetched", file=sys.stderr)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Fetch emails from IMAP and write JSON.")
    parser.add_argument("--days",      type=int, default=7,
                        help="Fetch last N days (default 7). Ignored if --since is set.")
    parser.add_argument("--since",     default=None,
                        help="Start date inclusive: YYYY-MM-DD or DD-Mon-YYYY")
    parser.add_argument("--until",     default=None,
                        help="End date exclusive: YYYY-MM-DD or DD-Mon-YYYY (default: today)")
    parser.add_argument("--max",       type=int, default=200,
                        help="Max emails per folder (default 200)")
    parser.add_argument("--folder",    default="INBOX",
                        help="Inbox folder name (default: INBOX)")
    parser.add_argument("--preset",    default="163",
                        choices=list(PRESETS.keys()),
                        help="Mailbox preset (default: 163)")
    parser.add_argument("--host",      default=None, help="Custom IMAP host")
    parser.add_argument("--port",      type=int, default=None, help="Custom IMAP port")
    parser.add_argument("--with-sent", action="store_true",
                        help="Also fetch Sent folder (better relationship analysis)")
    parser.add_argument("--output",    default=None,
                        help="Write JSON to this file. Prints to stdout if omitted.")
    args = parser.parse_args()

    # ── Date range ────────────────────────────────────────────────────────────
    def _parse(s):
        for fmt in ("%Y-%m-%d", "%d-%b-%Y", "%d-%B-%Y"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        raise ValueError(f"Cannot parse date: {s!r}")

    since_dt = _parse(args.since) if args.since else datetime.now() - timedelta(days=args.days)
    until_dt = _parse(args.until) if args.until else None
    since_str = since_dt.strftime(IMAP_DATE_FMT)
    until_str = until_dt.strftime(IMAP_DATE_FMT) if until_dt else None
    # ─────────────────────────────────────────────────────────────────────────

    user     = os.environ.get("EMAIL_USER") or input("Email: ").strip()
    password = os.environ.get("EMAIL_PASS") or __import__("getpass").getpass("App password: ")

    default_host, default_port, default_sent = PRESETS[args.preset]
    host = args.host or os.environ.get("IMAP_HOST") or default_host
    port = args.port or int(os.environ.get("IMAP_PORT", default_port))

    mail = _connect(user, password, host, port)
    emails = _fetch_folder(mail, args.folder, since_str, until_str, args.max, "received")

    if args.with_sent:
        emails += _fetch_folder(mail, default_sent, since_str, until_str, args.max, "sent")

    mail.logout()

    output = {
        "source": "imap",
        "owner":  user,
        "since":  since_str,
        "until":  until_str or "now",
        "emails": emails,
    }
    json_str = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"[done] {len(emails)} emails → {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
