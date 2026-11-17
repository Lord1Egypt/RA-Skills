#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 3
SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER NOT NULL,
  library_id TEXT NOT NULL,
  title TEXT NOT NULL,
  format TEXT NOT NULL,
  file_hash TEXT NOT NULL,
  lang TEXT NOT NULL,
  summary TEXT NOT NULL,
  highlights_json TEXT NOT NULL,
  reread_json TEXT NOT NULL,
  tags_json TEXT NOT NULL,
  coverage_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(book_id, library_id, format, file_hash, lang)
);
CREATE INDEX IF NOT EXISTS idx_analyses_target ON analyses(library_id, book_id, format);
"""

def default_db() -> str:
    root = os.environ.get("CALIBRE_CATALOG_STATE_DIR") or os.path.join(
        os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state")), "calibre-catalog-read"
    )
    return os.environ.get("CALIBRE_CATALOG_DB", os.path.join(root, "calibre_analysis.sqlite"))

def connect(db: str) -> sqlite3.Connection:
    Path(db).parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    con = sqlite3.connect(db)
    con.execute("PRAGMA busy_timeout=5000")
    version = con.execute("PRAGMA user_version").fetchone()[0]
    tables = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    if tables and version != SCHEMA_VERSION:
        con.close()
        raise ValueError("legacy/incompatible cache preserved; choose a new --db, no automatic migration")
    con.executescript(SCHEMA)
    con.execute("PRAGMA user_version=3")
    con.commit()
    return con

def ensure_record(obj: dict) -> dict:
    if not isinstance(obj, dict): raise ValueError("record must be an object")
    if "book_id" not in obj and "id" in obj: obj = {**obj, "book_id": obj["id"]}
    required = ("book_id", "library_id", "title", "format", "file_hash", "lang", "summary", "highlights", "reread", "tags")
    missing = [k for k in required if k not in obj]
    if missing: raise ValueError("record missing: " + ", ".join(missing))
    if type(obj["book_id"]) is not int: raise ValueError("book_id must be an integer")
    book_id = obj["book_id"]
    if book_id < 1: raise ValueError("book_id must be positive")
    if not isinstance(obj["library_id"], str) or not obj["library_id"].strip(): raise ValueError("library_id must be non-empty")
    if obj["lang"] not in ("ja", "en"): raise ValueError("lang must be ja or en")
    if not isinstance(obj["file_hash"], str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", obj["file_hash"]): raise ValueError("file_hash must be sha256:<hex>")
    for key in ("highlights", "reread", "tags"):
        if not isinstance(obj[key], list): raise ValueError(key + " must be an array")
    return {**obj, "book_id": book_id, "format": str(obj["format"]).upper(), "library_id": obj["library_id"].strip()}

def init_db(db: str) -> None:
    con = connect(db)
    con.commit(); con.close()

def upsert(db: str, obj: dict) -> None:
    obj = ensure_record(obj)
    con = connect(db)
    con.execute("""INSERT INTO analyses(book_id,library_id,title,format,file_hash,lang,summary,highlights_json,reread_json,tags_json,coverage_json,created_at)
      VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(book_id,library_id,format,file_hash,lang) DO UPDATE SET
        title=excluded.title, lang=excluded.lang, summary=excluded.summary,
        highlights_json=excluded.highlights_json, reread_json=excluded.reread_json,
        tags_json=excluded.tags_json, coverage_json=excluded.coverage_json, created_at=excluded.created_at""",
      (obj["book_id"], obj["library_id"], str(obj["title"]), obj["format"], obj["file_hash"], obj["lang"],
       str(obj["summary"]), json.dumps(obj["highlights"], ensure_ascii=False), json.dumps(obj["reread"], ensure_ascii=False),
       json.dumps(obj["tags"], ensure_ascii=False), json.dumps(obj.get("coverage", {}), ensure_ascii=False), datetime.now(timezone.utc).isoformat()))
    con.commit(); con.close()

def status(db: str, book_id: int, library_id: str, fmt: str, lang: str = "ja"):
    if not Path(db).exists(): return None
    con = connect(db)
    row = con.execute("SELECT book_id,library_id,format,file_hash,lang,coverage_json,created_at FROM analyses WHERE book_id=? AND library_id=? AND format=? AND lang=? ORDER BY created_at DESC LIMIT 1", (book_id, library_id, fmt.upper(), lang)).fetchone()
    con.close()
    if not row: return None
    return {"book_id": row[0], "library_id": row[1], "format": row[2], "file_hash": row[3], "lang": row[4], "coverage": json.loads(row[5]), "created_at": row[6]}

def search(db: str, query: str, limit: int):
    if not Path(db).exists(): return []
    con = connect(db)
    needle = "%" + query.casefold() + "%"
    rows = con.execute("""SELECT book_id,library_id,title,format,file_hash,created_at FROM analyses
      WHERE lower(title) LIKE ? OR lower(summary) LIKE ? OR lower(highlights_json) LIKE ? OR lower(reread_json) LIKE ?
      ORDER BY id DESC LIMIT ?""", (needle, needle, needle, needle, limit)).fetchall()
    con.close(); return rows

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("init", "upsert", "status", "search"))
    ap.add_argument("--db", default=default_db())
    ap.add_argument("--book-id", type=int)
    ap.add_argument("--library-id")
    ap.add_argument("--format", default="EPUB")
    ap.add_argument("--lang", choices=("ja", "en"), default="ja")
    ap.add_argument("--query")
    ap.add_argument("--limit", type=int, default=10)
    ns = ap.parse_args()
    if ns.cmd == "init": init_db(ns.db); print(json.dumps({"ok": True, "db": ns.db}, ensure_ascii=False)); return
    if ns.cmd == "upsert":
        try: obj = json.load(sys.stdin)
        except json.JSONDecodeError as exc: raise SystemExit("invalid JSON input: " + str(exc))
        upsert(ns.db, obj); print(json.dumps({"ok": True, "book_id": obj.get("book_id", obj.get("id"))}, ensure_ascii=False)); return
    if ns.cmd == "status":
        if ns.book_id is None or not ns.library_id: raise SystemExit("--book-id and --library-id required")
        print(json.dumps({"ok": True, "status": status(ns.db, ns.book_id, ns.library_id, ns.format, ns.lang)}, ensure_ascii=False)); return
    if not ns.query or ns.limit < 1 or ns.limit > 1000: raise SystemExit("--query and bounded --limit required")
    rows = search(ns.db, ns.query, ns.limit)
    print(json.dumps({"ok": True, "items": [{"book_id": r[0], "library_id": r[1], "title": r[2], "format": r[3], "file_hash": r[4], "created_at": r[5]} for r in rows]}, ensure_ascii=False))

if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print(str(exc), file=sys.stderr); raise SystemExit(1)
