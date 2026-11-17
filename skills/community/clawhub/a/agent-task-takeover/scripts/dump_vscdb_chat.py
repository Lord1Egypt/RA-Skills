#!/usr/bin/env python3
"""Read chat history from Electron, VS Code-family agents (Cursor, Trae,
VS Code Copilot, Kiro, Windsurf, Antigravity).

These apps keep chat state in two places:
  - <App>/User/workspaceStorage/<hash>/state.vscdb  (SQLite, table ItemTable:
    keys like 'chat.ChatSessionStore.index', 'ChatStore', 'workbench.panel.chat')
  - <App>/User/workspaceStorage/<hash>/chatSessions/<uuid>.json  (VS Code
    Copilot sessions: {"sessionId":..., "requests":[{"message":{"text":...},
    "response":[{"value":...}]}]})

Stdlib only. Read-only (SQLite opened mode=ro). Secrets redacted unless
--show-sensitive is used.

Usage:
  python dump_vscdb_chat.py --app cursor --list
  python dump_vscdb_chat.py --db <state.vscdb> --list
  python dump_vscdb_chat.py --db <state.vscdb> --key chat.ChatSessionStore.index
  python dump_vscdb_chat.py --session <chatSessions/xxx.json> [--chars 2000]
"""
import argparse
import glob
import json
import os
import sqlite3
import sys
from pathlib import Path

from session_utils import blocks_text, ensure_utf8_stdout, redact_text, truncate_text

CHAT_KEY_PATTERNS = ("chat", "aichat", "ai-chat", "composer", "aiservice", "chatstore", "icube")

APP_DIRS = {
    "cursor": "Cursor",
    "trae": "Trae",
    "code": "Code",
    "vscode": "Code",
    "kiro": "Kiro",
    "windsurf": "Windsurf",
    "antigravity": "Antigravity",
}


def app_user_dir(app):
    home = Path.home()
    name = APP_DIRS[app]
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / name / "User"
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", home / "AppData/Roaming")) / name / "User"
    return home / ".config" / name / "User"


def find_dbs(args):
    if args.db:
        return [args.db]
    roots = []
    if args.dir:
        roots.append(Path(args.dir))
    elif args.app:
        user = app_user_dir(args.app)
        roots.extend([user / "workspaceStorage", user / "globalStorage"])
    dbs = []
    for root in roots:
        if root.name in ("workspaceStorage", "globalStorage"):
            dbs.extend(glob.glob(str(root / "**" / "state.vscdb"), recursive=True))
        else:
            dbs.extend(glob.glob(str(root / "state.vscdb")))
    return sorted(set(dbs))


def open_ro(path):
    try:
        return sqlite3.connect(f"file:{Path(path).resolve()}?mode=ro", uri=True)
    except (sqlite3.Error, ValueError) as exc:
        sys.exit(f"cannot open {path} read-only: {exc}")


def list_keys(db, path, show_sensitive):
    try:
        rows = db.execute("SELECT key, length(value) FROM ItemTable").fetchall()
    except sqlite3.Error as exc:
        print(f"# {path}: unreadable ({exc})")
        return
    hits = [
        (k, n) for k, n in rows
        if any(p in (k or "").lower() for p in CHAT_KEY_PATTERNS)
    ]
    if not hits:
        return
    print(f"\n# {path}")
    for key, size in sorted(hits):
        safe = key if show_sensitive else redact_text(key)[0]
        print(f"  {safe}  ({size or 0} bytes)")


def extract_messages(value, depth=0):
    """Best-effort: pull (role, text) pairs out of an unknown chat JSON shape."""
    out = []

    def walk(node, depth):
        if depth > 8:
            return
        if isinstance(node, dict):
            role = node.get("role")
            if role in ("user", "assistant", "human", "bot") and (
                node.get("content") or node.get("text")
            ):
                txt = blocks_text(node.get("content")) or (
                    node.get("text") if isinstance(node.get("text"), str) else ""
                )
                if txt.strip():
                    mapped = {"human": "user", "bot": "assistant"}.get(role, role)
                    out.append((mapped, txt))
                    return
            # VS Code request shape: {"message": {"text": ...}, "response": [...]}
            msg = node.get("message")
            if isinstance(msg, dict) and isinstance(msg.get("text"), str):
                out.append(("user", msg["text"]))
                resp = node.get("response")
                if isinstance(resp, list):
                    txt = "\n".join(
                        item["value"] for item in resp
                        if isinstance(item, dict) and isinstance(item.get("value"), str)
                    )
                    if txt.strip():
                        out.append(("assistant", txt))
                return
            for child in node.values():
                walk(child, depth + 1)
        elif isinstance(node, list):
            for child in node:
                walk(child, depth + 1)

    walk(value, depth)
    return out


def dump_key(db, key, args):
    row = db.execute("SELECT value FROM ItemTable WHERE key=?", (key,)).fetchone()
    if row is None:
        sys.exit(f"key not found: {key}")
    raw = row[0]
    print(f"# key: {key}  ({len(raw or '')} chars)")
    try:
        value = json.loads(raw)
    except Exception:
        value = None
    if value is None:
        txt = raw if args.show_sensitive else redact_text(raw)[0]
        print(truncate_text(txt, args.chars))
        return
    messages = extract_messages(value)
    if messages:
        print(f"# extracted {len(messages)} message(s)\n")
        for role, txt in messages:
            if not args.show_sensitive:
                txt = redact_text(txt)[0]
            print(f"\n=== {role.upper()} ===")
            print(truncate_text(txt, args.chars))
    else:
        txt = json.dumps(value, ensure_ascii=False, indent=2)
        if not args.show_sensitive:
            txt = redact_text(txt)[0]
        print(truncate_text(txt, args.chars))


def dump_session_file(path, args):
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError) as exc:
        sys.exit(f"cannot read {path}: {exc}")
    print(f"# session: {doc.get('sessionId', '?')}  requests: {len(doc.get('requests') or [])}")
    messages = extract_messages(doc)
    if args.last:
        messages = messages[-args.last:]
    if args.role != "all":
        messages = [m for m in messages if m[0] == args.role]
    print(f"# {len(messages)} messages\n")
    for role, txt in messages:
        if not args.show_sensitive:
            txt = redact_text(txt)[0]
        print(f"\n=== {role.upper()} ===")
        print(truncate_text(txt, args.chars))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--app", choices=sorted(APP_DIRS), help="Electron app to scan")
    parser.add_argument("--db", help="path to a state.vscdb file")
    parser.add_argument("--dir", help="workspaceStorage dir to scan")
    parser.add_argument("--list", action="store_true", help="list chat-ish keys (default)")
    parser.add_argument("--key", help="dump one ItemTable key")
    parser.add_argument("--session", help="dump a chatSessions/*.json file")
    parser.add_argument("--role", choices=("all", "user", "assistant"), default="all")
    parser.add_argument("--last", type=int, default=0)
    parser.add_argument("--chars", type=int, default=2000,
                        help="max chars per message; 0 means unlimited")
    parser.add_argument("--show-sensitive", action="store_true")
    args = parser.parse_args()
    ensure_utf8_stdout()

    if args.session:
        dump_session_file(args.session, args)
        return

    dbs = find_dbs(args)
    if not dbs:
        sys.exit("no state.vscdb found; pass --app, --dir, or --db")
    for path in dbs:
        db = open_ro(path)
        try:
            if args.key:
                dump_key(db, args.key, args)
            else:
                list_keys(db, path, args.show_sensitive)
        finally:
            db.close()


if __name__ == "__main__":
    main()
