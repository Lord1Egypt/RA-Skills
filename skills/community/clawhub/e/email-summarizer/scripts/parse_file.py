#!/usr/bin/env python3
"""
parse_file.py — Parse local email files and write a JSON file.

Supported input formats:
  --pst FILE        Outlook .pst archive
  --mbox FILE       Unix mbox file
  --sent-mbox FILE  Additional sent-items mbox (use with --mbox)
  --msg-dir DIR     Folder of Outlook .msg files

Output JSON format (same as fetch_imap.py):
  {
    "source":  "pst" | "mbox" | "msg",
    "owner":   "inferred@address.or.empty",
    "since":   "YYYY-MM-DD",
    "until":   "YYYY-MM-DD",
    "emails":  [ { id, direction, date, from, to, cc, subject, body, to_addrs? }, ... ]
  }

Usage:
  # Parse a .pst file
  python3 parse_file.py --pst ~/Downloads/archive.pst --output emails.json

  # Parse .mbox (inbox + sent)
  python3 parse_file.py --mbox Inbox.mbox --sent-mbox Sent.mbox --output emails.json

  # Parse .msg folder, filter by date
  python3 parse_file.py --msg-dir ./exported/ --since 2026-01-01 --output emails.json

  # Pipe to build_report.py
  python3 parse_file.py --pst archive.pst | python3 build_report.py --output report

PST engine (--pst-engine):
  auto     Try native first, fall back to readpst (default)
  native   Node.js pst-extractor (requires: cd scripts && npm install)
  readpst  System binary readpst (requires: apt install pst-utils)

Dependencies:
  extract-msg   pip install extract-msg   (for .msg files)
  pst-extractor npm install               (for native .pst engine)
"""

import argparse, email, email.header, email.utils
import json, mailbox, os, re, shutil, subprocess, sys, tempfile
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _core import decode_header, get_body, strip_html, parse_addr, IMAP_DATE_FMT

HERE = os.path.dirname(os.path.abspath(__file__))
NODE = (
    os.environ.get("NODE_BIN")
    or shutil.which("node")
    or "/usr/local/lib/.nvm/versions/node/v22.17.0/bin/node"
)


# ── Date filter helpers ───────────────────────────────────────────────────────

def _parse_date_arg(s: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%d-%b-%Y", "%d-%B-%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Cannot parse date: {s!r}. Use YYYY-MM-DD.")


def _in_range(date_str: str, since_dt, until_dt) -> bool:
    if not since_dt and not until_dt:
        return True
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        dt = dt.replace(tzinfo=None)
    except Exception:
        return True
    if since_dt and dt < since_dt:
        return False
    if until_dt and dt >= until_dt:
        return False
    return True


# ── mbox / msg shared helpers ─────────────────────────────────────────────────

def _email_record(uid: str, direction: str, msg) -> dict:
    date_str = msg.get("Date", "")
    try:
        date_iso = email.utils.parsedate_to_datetime(date_str).isoformat()
    except Exception:
        date_iso = date_str

    return {
        "id":        uid,
        "direction": direction,
        "date":      date_iso,
        "from":      decode_header(msg.get("From",    "")),
        "to":        decode_header(msg.get("To",      "")),
        "cc":        decode_header(msg.get("Cc",      "")),
        "subject":   decode_header(msg.get("Subject", "(no subject)")),
        "body":      get_body(msg),
    }


# ── mbox parser ───────────────────────────────────────────────────────────────

def _parse_mbox(path: str, direction: str, since_dt, until_dt, max_count: int) -> list:
    results = []
    try:
        mbox = mailbox.mbox(path)
    except Exception as e:
        print(f"[error] Cannot open mbox {path}: {e}", file=sys.stderr)
        return []

    for i, msg in enumerate(mbox):
        if len(results) >= max_count:
            break
        date_str = msg.get("Date", "")
        if not _in_range(date_str, since_dt, until_dt):
            continue
        results.append(_email_record(str(i), direction, msg))

    print(f"[mbox] {path}: {len(results)} emails loaded", file=sys.stderr)
    return results


# ── .msg parser ───────────────────────────────────────────────────────────────

def _parse_msg_dir(msg_dir: str, since_dt, until_dt, max_count: int) -> list:
    try:
        import extract_msg as extmsg
    except ImportError:
        print("[error] extract-msg not installed. Run: pip install extract-msg", file=sys.stderr)
        sys.exit(1)

    results = []
    files = sorted(f for f in os.listdir(msg_dir) if f.lower().endswith(".msg"))
    print(f"[msg] {len(files)} .msg files found in {msg_dir}", file=sys.stderr)

    for i, fname in enumerate(files):
        if len(results) >= max_count:
            break
        path = os.path.join(msg_dir, fname)
        try:
            m = extmsg.Message(path)
        except Exception as e:
            print(f"[skip] {fname}: {e}", file=sys.stderr)
            continue

        date_val = getattr(m, "date", None)
        if date_val:
            try:
                dt = date_val if isinstance(date_val, datetime) else datetime.fromisoformat(str(date_val))
                dt = dt.replace(tzinfo=None)
                if since_dt and dt < since_dt: continue
                if until_dt and dt >= until_dt: continue
                date_iso = dt.isoformat()
            except Exception:
                date_iso = str(date_val)
        else:
            date_iso = ""

        body = ""
        try:
            body = (m.body or "").strip()[:2000]
        except Exception:
            pass
        if not body:
            try:
                body = strip_html(m.htmlBody or "")[:2000]
            except Exception:
                pass

        results.append({
            "id":        f"msg-{i}",
            "direction": "received",
            "date":      date_iso,
            "from":      getattr(m, "sender",  "") or "",
            "to":        getattr(m, "to",      "") or "",
            "cc":        getattr(m, "cc",      "") or "",
            "subject":   getattr(m, "subject", "") or "(no subject)",
            "body":      body,
        })

    print(f"[msg] {len(results)} emails loaded", file=sys.stderr)
    return results


# ── PST native engine (Node.js pst-extractor) ─────────────────────────────────

def _parse_pst_native(pst_path: str, since_dt, until_dt, max_count: int) -> list:
    helper = os.path.join(HERE, "pst_extractor_helper.js")
    if not os.path.isfile(helper):
        raise FileNotFoundError(f"pst_extractor_helper.js not found at {helper}")
    if not shutil.which(NODE) and not os.path.isfile(NODE):
        raise RuntimeError(f"Node.js not found at {NODE}. Set NODE_BIN env var.")

    cmd = [NODE, helper, pst_path, "--max", str(max_count)]
    if since_dt:
        cmd += ["--since", since_dt.strftime("%Y-%m-%d")]
    if until_dt:
        cmd += ["--until", until_dt.strftime("%Y-%m-%d")]

    print(f"[pst-native] Running: {' '.join(cmd)}", file=sys.stderr)
    # subprocess.run is used here to invoke a fixed local Node.js script
    # (pst_extractor_helper.js bundled in this skill). The command list is
    # constructed from validated local paths only — no shell=True, no user
    # input is ever interpolated into the command string.
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stderr.splitlines():
        print(f"  {line}", file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"pst_extractor_helper.js exited with code {result.returncode}.")

    emails = json.loads(result.stdout)
    print(f"[pst-native] {len(emails)} emails loaded.", file=sys.stderr)
    return emails


# ── PST readpst engine ────────────────────────────────────────────────────────

def _parse_pst_readpst(pst_path: str, since_dt, until_dt, max_count: int) -> list:
    if not shutil.which("readpst"):
        raise RuntimeError("readpst not found. Install: apt install pst-utils  OR  brew install libpst")

    tmp_dir = tempfile.mkdtemp(prefix="pst_mbox_")
    try:
        # subprocess.run invokes the system-installed `readpst` binary with a
        # fixed argument list. No shell=True, no user-controlled strings in cmd.
        subprocess.run(
            ["readpst", "-o", tmp_dir, "-M", pst_path],
            check=True, capture_output=True,
        )
        emails = []
        for dirpath, _, filenames in os.walk(tmp_dir):
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                direction = "sent" if "sent" in fname.lower() else "received"
                emails += _parse_mbox(fpath, direction, since_dt, until_dt, max_count - len(emails))
                if len(emails) >= max_count:
                    break
        print(f"[pst-readpst] {len(emails)} emails loaded.", file=sys.stderr)
        return emails
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _parse_pst(pst_path: str, engine: str, since_dt, until_dt, max_count: int) -> list:
    if engine in ("auto", "native"):
        try:
            return _parse_pst_native(pst_path, since_dt, until_dt, max_count)
        except Exception as e:
            if engine == "native":
                print(f"[error] Native PST engine failed: {e}", file=sys.stderr)
                sys.exit(1)
            print(f"[warn] Native engine failed ({e}); trying readpst…", file=sys.stderr)

    return _parse_pst_readpst(pst_path, since_dt, until_dt, max_count)


# ── Owner inference (lightweight, without importing _analyze) ─────────────────

def _quick_infer_owner(emails: list) -> str:
    from collections import Counter
    counter: Counter = Counter()
    for e in emails:
        if e.get("direction", "received") == "received":
            for addr in e.get("to_addrs", []):
                if addr:
                    counter[addr.lower()] += 1
            if not e.get("to_addrs"):
                for part in e.get("to", "").split(","):
                    _, a = parse_addr(part.strip())
                    if a and "@" in a:
                        counter[a.lower()] += 1
    return counter.most_common(1)[0][0] if counter else ""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Parse local email files and write a JSON file.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--pst",     metavar="FILE", help="Outlook .pst archive")
    src.add_argument("--mbox",    metavar="FILE", help="Unix mbox file")
    src.add_argument("--msg-dir", metavar="DIR",  help="Folder of Outlook .msg files")

    parser.add_argument("--sent-mbox",  metavar="FILE", default=None,
                        help="Additional sent-items mbox (used with --mbox)")
    parser.add_argument("--pst-engine", default="auto",
                        choices=["auto", "native", "readpst"],
                        help="PST parse engine (default: auto)")
    parser.add_argument("--days",   type=int, default=None,
                        help="Only include emails from the last N days")
    parser.add_argument("--since",  default=None, help="Start date inclusive: YYYY-MM-DD")
    parser.add_argument("--until",  default=None, help="End date exclusive: YYYY-MM-DD")
    parser.add_argument("--max",    type=int, default=500,
                        help="Max emails to load (default 500)")
    parser.add_argument("--output", default=None,
                        help="Write JSON to file. Prints to stdout if omitted.")
    args = parser.parse_args()

    # ── Date range ────────────────────────────────────────────────────────────
    if args.since:
        since_dt = _parse_date_arg(args.since)
    elif args.days:
        since_dt = datetime.now() - timedelta(days=args.days)
    else:
        since_dt = None

    until_dt = _parse_date_arg(args.until) if args.until else None
    since_label = since_dt.strftime("%Y-%m-%d") if since_dt else "all"
    until_label = until_dt.strftime("%Y-%m-%d") if until_dt else "now"
    # ─────────────────────────────────────────────────────────────────────────

    # ── Parse ─────────────────────────────────────────────────────────────────
    if args.pst:
        emails = _parse_pst(args.pst, args.pst_engine, since_dt, until_dt, args.max)
        source = "pst"
    elif args.mbox:
        emails = _parse_mbox(args.mbox, "received", since_dt, until_dt, args.max)
        if args.sent_mbox:
            emails += _parse_mbox(args.sent_mbox, "sent", since_dt, until_dt,
                                   args.max - len(emails))
        source = "mbox"
    else:
        emails = _parse_msg_dir(args.msg_dir, since_dt, until_dt, args.max)
        source = "msg"

    owner = _quick_infer_owner(emails)
    if owner:
        print(f"[parse_file] Inferred owner: {owner}", file=sys.stderr)

    output = {
        "source": source,
        "owner":  owner,
        "since":  since_label,
        "until":  until_label,
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
