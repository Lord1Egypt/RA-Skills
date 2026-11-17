"""The symbol index: build it from a set of roots, query it cheaply.

Storage is a single SQLite file (stdlib sqlite3). A query returns compact
records (name, kind, signature, file:line) so an agent can locate a definition
without grepping then reading the whole enclosing file.
"""
from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass

from .extractors import EXT_LANG, extract

DEFAULT_DB = os.path.expanduser("~/.codemap/index.db")

# directories we never want to walk into
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".next", "dist", "build",
    ".venv", "venv", "site-packages", ".mypy_cache", ".pytest_cache",
    "coverage", ".cache",
}


@dataclass(frozen=True)
class Hit:
    name: str
    kind: str
    signature: str
    file: str
    line: int
    lang: str

    def compact(self) -> str:
        return f"{self.file}:{self.line}  [{self.kind}] {self.signature}"


def _connect(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS symbols (
            name TEXT NOT NULL,
            kind TEXT NOT NULL,
            signature TEXT NOT NULL,
            file TEXT NOT NULL,
            line INTEGER NOT NULL,
            lang TEXT NOT NULL
        )"""
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_name ON symbols(name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_file ON symbols(file)")
    return conn


def _iter_source_files(roots: list[str]):
    for root in roots:
        root = os.path.abspath(root)
        if os.path.isfile(root):
            if os.path.splitext(root)[1].lower() in EXT_LANG:
                yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() in EXT_LANG:
                    yield os.path.join(dirpath, fn)


def build(roots: list[str], db_path: str = DEFAULT_DB) -> dict:
    """(Re)build the index from scratch over the given roots."""
    conn = _connect(db_path)
    conn.execute("DELETE FROM symbols")
    files = 0
    symbols = 0
    rows = []
    for path in _iter_source_files(roots):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        files += 1
        for s in extract(path, text):
            rows.append((s.name, s.kind, s.signature, path, s.line, s.lang))
            symbols += 1
        if len(rows) >= 2000:
            conn.executemany("INSERT INTO symbols VALUES (?,?,?,?,?,?)", rows)
            rows = []
    if rows:
        conn.executemany("INSERT INTO symbols VALUES (?,?,?,?,?,?)", rows)
    conn.commit()
    conn.close()
    return {"files": files, "symbols": symbols, "db": db_path}


def find(name: str, db_path: str = DEFAULT_DB, *, kind: str | None = None,
         exact: bool = True, limit: int = 50) -> list[Hit]:
    conn = _connect(db_path)
    if exact:
        sql = "SELECT name,kind,signature,file,line,lang FROM symbols WHERE name=?"
        params: list = [name]
    else:
        sql = "SELECT name,kind,signature,file,line,lang FROM symbols WHERE name LIKE ?"
        params = [f"%{name}%"]
    if kind:
        sql += " AND kind=?"
        params.append(kind)
    sql += " ORDER BY name, file, line LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [Hit(*r) for r in rows]


def outline(file_path: str, db_path: str = DEFAULT_DB) -> list[Hit]:
    conn = _connect(db_path)
    target = os.path.abspath(file_path)
    rows = conn.execute(
        "SELECT name,kind,signature,file,line,lang FROM symbols "
        "WHERE file=? ORDER BY line", (target,)
    ).fetchall()
    conn.close()
    return [Hit(*r) for r in rows]


def stats(db_path: str = DEFAULT_DB) -> dict:
    conn = _connect(db_path)
    total = conn.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]
    files = conn.execute("SELECT COUNT(DISTINCT file) FROM symbols").fetchone()[0]
    by_kind = dict(
        conn.execute("SELECT kind, COUNT(*) FROM symbols GROUP BY kind").fetchall()
    )
    by_lang = dict(
        conn.execute("SELECT lang, COUNT(*) FROM symbols GROUP BY lang").fetchall()
    )
    conn.close()
    return {"symbols": total, "files": files, "by_kind": by_kind, "by_lang": by_lang}
