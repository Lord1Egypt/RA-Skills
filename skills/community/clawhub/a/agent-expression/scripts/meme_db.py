#!/usr/bin/env python3
"""SQLite index for local meme packs: path + tag + caption/keywords + search."""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import time
from pathlib import Path
from typing import Iterable, Optional

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}

# sqlite3.Connection may be slotted / non-weakrefable — key by id(conn).
_CONN_PACK_DIRS: dict[int, Path] = {}

SCHEMA = """
CREATE TABLE IF NOT EXISTS memes (
  path TEXT PRIMARY KEY,
  tag TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_hash TEXT,
  caption TEXT NOT NULL DEFAULT '',
  keywords TEXT NOT NULL DEFAULT '',
  mtime REAL,
  captioned_at REAL
);
CREATE INDEX IF NOT EXISTS idx_memes_tag ON memes(tag);
CREATE INDEX IF NOT EXISTS idx_memes_captioned ON memes(captioned_at);

CREATE VIRTUAL TABLE IF NOT EXISTS memes_fts USING fts5(
  path UNINDEXED,
  tag,
  caption,
  keywords,
  file_name,
  tokenize = 'unicode61'
);
"""


def data_home() -> Path:
    """Root for meme-packs/ and optional .env (host-agnostic).

    Priority: MEME_HOME → AGENT_EXPRESSION_HOME → HERMES_HOME →
    existing ~/.hermes (compat) → ~/.agent-expression.
    """
    for key in ("MEME_HOME", "AGENT_EXPRESSION_HOME", "HERMES_HOME"):
        v = os.environ.get(key, "").strip()
        if v:
            return Path(v).expanduser().resolve()
    hermes = Path("~/.hermes").expanduser()
    if (hermes / "meme-packs").is_dir():
        return hermes.resolve()
    return Path("~/.agent-expression").expanduser().resolve()


def default_pack_dir() -> Path:
    """Pack root: …/meme-packs/<id>/ containing memes/ + index.db."""
    for key in ("MEME_PACK", "HERMES_MEME_PACK"):
        override = os.environ.get(key, "").strip()
        if override:
            return Path(override).expanduser().resolve()
    pack_id = (
        os.environ.get("MEME_PACK_ID")
        or os.environ.get("HERMES_MEME_PACK_ID")
        or "official-001"
    ).strip() or "official-001"
    candidate = data_home() / "meme-packs" / pack_id
    if (candidate / "index.db").is_file() or (candidate / "memes").is_dir():
        return candidate
    # Bundled with the skill checkout
    bundled = Path(__file__).resolve().parents[1] / "packs" / pack_id
    if (bundled / "index.db").is_file() or (bundled / "memes").is_dir():
        return bundled
    return candidate


def dotenv_candidates() -> list[Path]:
    """Likely .env locations (first existing wins for loaders)."""
    seen: set[Path] = set()
    out: list[Path] = []
    for key in ("MEME_HOME", "AGENT_EXPRESSION_HOME", "HERMES_HOME"):
        v = os.environ.get(key, "").strip()
        if v:
            p = Path(v).expanduser().resolve() / ".env"
            if p not in seen:
                seen.add(p)
                out.append(p)
    for base in (
        Path("~/.agent-expression").expanduser(),
        Path("~/.hermes").expanduser(),
        Path(__file__).resolve().parents[1],  # skill root
        Path.cwd(),
    ):
        p = (base / ".env").resolve()
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def load_dotenv_merged() -> dict[str, str]:
    """Load key=value from the first existing dotenv, then overlay process env."""
    out: dict[str, str] = {}
    for env_path in dotenv_candidates():
        if not env_path.is_file():
            continue
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip().strip('"').strip("'")
        break
    out.update({k: v for k, v in os.environ.items() if v})
    return out


def temp_workdir(name: str = "agent-expression-meme") -> Path:
    """Cross-platform scratch dir (Windows TEMP / Unix /tmp)."""
    import tempfile

    d = Path(tempfile.gettempdir()) / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def system_temp_roots() -> list[Path]:
    """Allowed temp roots for path sandboxing."""
    import tempfile

    roots: list[Path] = []
    for key in ("TMPDIR", "TEMP", "TMP"):
        v = os.environ.get(key, "").strip()
        if v:
            roots.append(Path(v).expanduser().resolve())
    roots.append(Path(tempfile.gettempdir()).resolve())
    # Unix fallback still listed for mixed environments
    for p in (Path("/tmp"), Path("/var/tmp")):
        if p.is_dir():
            roots.append(p.resolve())
    # de-dupe preserving order
    seen: set[Path] = set()
    out: list[Path] = []
    for r in roots:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def db_path_for_pack(pack_dir: Path) -> Path:
    return pack_dir / "index.db"


def connect(pack_dir: Path) -> sqlite3.Connection:
    pack_dir = pack_dir.expanduser().resolve()
    pack_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path_for_pack(pack_dir)))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _CONN_PACK_DIRS[id(conn)] = pack_dir
    return conn


def pack_dir_of(conn: sqlite3.Connection) -> Optional[Path]:
    return _CONN_PACK_DIRS.get(id(conn))


def to_store_path(pack_dir: Path, path: Path) -> str:
    """Prefer pack-relative POSIX path (portable across machines)."""
    path = path.expanduser().resolve()
    pack = pack_dir.expanduser().resolve()
    try:
        return path.relative_to(pack).as_posix()
    except ValueError:
        return str(path)


def from_store_path(pack_dir: Path, stored: str) -> Path:
    """Resolve DB path to an absolute filesystem path."""
    raw = (stored or "").strip()
    if not raw:
        return Path(raw)
    p = Path(raw)
    pack = pack_dir.expanduser().resolve()
    if not p.is_absolute():
        return (pack / p).resolve()
    if p.is_file():
        return p.resolve()
    # Legacy absolute path from another machine: remap …/memes/<tag>/<file>
    parts = p.parts
    if "memes" in parts:
        i = parts.index("memes")
        cand = pack.joinpath(*parts[i:])
        if cand.is_file():
            return cand.resolve()
    return p


def absolutize_path(conn: sqlite3.Connection, stored: str) -> str:
    pack = pack_dir_of(conn)
    if not pack:
        return stored
    return str(from_store_path(pack, stored))


def relocate_index_to_relative(conn: sqlite3.Connection, pack_dir: Optional[Path] = None) -> dict:
    """Rewrite absolute meme/embedding paths to pack-relative. Idempotent."""
    pack = (pack_dir or pack_dir_of(conn) or Path(".")).expanduser().resolve()
    memes = list(conn.execute("SELECT path FROM memes"))
    changed = 0
    for row in memes:
        old = row["path"]
        abs_p = from_store_path(pack, old)
        new = to_store_path(pack, abs_p) if abs_p.exists() else (
            Path(old).as_posix() if not Path(old).is_absolute() else old
        )
        # If still absolute but under pack via string remap
        if Path(new).is_absolute():
            try:
                new = Path(new).resolve().relative_to(pack).as_posix()
            except Exception:
                if "memes/" in old.replace("\\", "/"):
                    new = old.replace("\\", "/").split("memes/", 1)[-1]
                    new = "memes/" + new if not new.startswith("memes/") else new
        if new == old:
            continue
        # Update PK carefully
        conn.execute("UPDATE memes SET path=? WHERE path=?", (new, old))
        conn.execute("UPDATE memes_fts SET path=? WHERE path=?", (new, old))
        try:
            conn.execute("UPDATE meme_embeddings SET path=? WHERE path=?", (new, old))
        except sqlite3.OperationalError:
            pass
        changed += 1
    conn.commit()
    return {"rewritten": changed, "total": len(memes)}


def file_hash(path: Path, max_bytes: int = 1024 * 1024) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
            if f.tell() >= max_bytes:
                break
    return h.hexdigest()


def iter_pack_images(pack_dir: Path) -> Iterable[tuple[str, Path]]:
    memes_root = pack_dir / "memes"
    if not memes_root.is_dir():
        return
    for tag_dir in sorted(memes_root.iterdir()):
        if not tag_dir.is_dir():
            continue
        tag = tag_dir.name
        for path in sorted(tag_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                yield tag, path.resolve()


def _fts_sync(conn: sqlite3.Connection, path: str, tag: str, file_name: str,
              caption: str, keywords: str) -> None:
    conn.execute("DELETE FROM memes_fts WHERE path = ?", (path,))
    conn.execute(
        "INSERT INTO memes_fts(path, tag, caption, keywords, file_name) VALUES (?,?,?,?,?)",
        (path, tag, caption or "", keywords or "", file_name),
    )


def upsert_meme(
    conn: sqlite3.Connection,
    *,
    path: Path,
    tag: str,
    caption: Optional[str] = None,
    keywords: Optional[str] = None,
    keep_caption: bool = True,
    pack_dir: Optional[Path] = None,
) -> None:
    path = path.expanduser().resolve()
    pack = pack_dir or pack_dir_of(conn)
    path_s = to_store_path(pack, path) if pack else str(path)
    mtime = path.stat().st_mtime
    fhash = file_hash(path)
    row = conn.execute("SELECT caption, keywords, file_hash FROM memes WHERE path=?", (path_s,)).fetchone()

    new_caption = caption
    new_keywords = keywords
    captioned_at = None
    if row and keep_caption and caption is None:
        new_caption = row["caption"]
        new_keywords = row["keywords"]
        # keep captioned_at if hash unchanged and caption exists
    if caption is not None:
        captioned_at = time.time()

    if row is None:
        conn.execute(
            """INSERT INTO memes(path, tag, file_name, file_hash, caption, keywords, mtime, captioned_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                path_s,
                tag,
                path.name,
                fhash,
                new_caption or "",
                new_keywords or "",
                mtime,
                captioned_at,
            ),
        )
    else:
        # If file changed and caller didn't pass new caption, clear caption so it gets re-captioned
        if row["file_hash"] != fhash and caption is None and keep_caption:
            new_caption = ""
            new_keywords = ""
            captioned_at = None
        elif caption is None:
            captioned_at = conn.execute(
                "SELECT captioned_at FROM memes WHERE path=?", (path_s,)
            ).fetchone()["captioned_at"]
        conn.execute(
            """UPDATE memes SET tag=?, file_name=?, file_hash=?, caption=?, keywords=?, mtime=?,
               captioned_at=COALESCE(?, captioned_at) WHERE path=?""",
            (
                tag,
                path.name,
                fhash,
                new_caption if new_caption is not None else row["caption"],
                new_keywords if new_keywords is not None else row["keywords"],
                mtime,
                captioned_at,
                path_s,
            ),
        )

    final = conn.execute(
        "SELECT tag, file_name, caption, keywords FROM memes WHERE path=?", (path_s,)
    ).fetchone()
    _fts_sync(
        conn,
        path_s,
        final["tag"],
        final["file_name"],
        final["caption"] or "",
        final["keywords"] or "",
    )


def sync_files(conn: sqlite3.Connection, pack_dir: Path) -> dict:
    """Scan pack on disk; upsert rows; delete missing. Returns counts."""
    pack_dir = pack_dir.expanduser().resolve()
    _CONN_PACK_DIRS[id(conn)] = pack_dir
    seen: set[str] = set()
    added = updated = 0
    for tag, path in iter_pack_images(pack_dir):
        path_s = to_store_path(pack_dir, path)
        seen.add(path_s)
        before = conn.execute("SELECT file_hash FROM memes WHERE path=?", (path_s,)).fetchone()
        upsert_meme(conn, path=path, tag=tag, keep_caption=True, pack_dir=pack_dir)
        if before is None:
            added += 1
        else:
            updated += 1
    # prune
    rows = conn.execute("SELECT path FROM memes").fetchall()
    deleted = 0
    for r in rows:
        if r["path"] not in seen:
            conn.execute("DELETE FROM memes_fts WHERE path=?", (r["path"],))
            conn.execute("DELETE FROM memes WHERE path=?", (r["path"],))
            try:
                conn.execute("DELETE FROM meme_embeddings WHERE path=?", (r["path"],))
            except sqlite3.OperationalError:
                pass
            deleted += 1
    conn.commit()
    return {"added": added, "scanned": len(seen), "deleted": deleted}


def needs_caption(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            """SELECT path, tag, file_name FROM memes
               WHERE caption IS NULL OR caption = '' OR captioned_at IS NULL
               ORDER BY tag, file_name"""
        )
    )


def _escape_like(s: str) -> str:
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search(
    conn: sqlite3.Connection,
    query: str,
    *,
    tag: Optional[str] = None,
    limit: int = 5,
) -> list[dict]:
    """Search by caption/keywords/tag. Returns list of dicts with path, tag, caption, score."""
    q = (query or "").strip()
    if not q and not tag:
        return []

    # Prefer FTS when query present; always allow tag filter.
    results: list[dict] = []
    if q:
        # Build FTS query: quote tokens, join with OR for recall
        tokens = [t for t in re.split(r"\s+", q) if t]
        fts_parts = []
        for t in tokens:
            safe = t.replace('"', " ")
            if safe:
                fts_parts.append(f'"{safe}"')
        fts_q = " OR ".join(fts_parts) if fts_parts else None

        rows = []
        if fts_q:
            sql = """
              SELECT m.path, m.tag, m.caption, m.keywords, m.file_name,
                     bm25(memes_fts) AS rank
              FROM memes_fts
              JOIN memes m ON m.path = memes_fts.path
              WHERE memes_fts MATCH ?
            """
            params: list = [fts_q]
            if tag:
                sql += " AND m.tag = ?"
                params.append(tag)
            sql += " ORDER BY rank LIMIT ?"
            params.append(max(limit * 3, limit))
            try:
                rows = list(conn.execute(sql, params))
            except sqlite3.OperationalError:
                rows = []

        # LIKE fallback / supplement for Chinese phrases FTS may miss as wholes
        like_sql = """
          SELECT path, tag, caption, keywords, file_name, 0 AS rank
          FROM memes WHERE 1=1
        """
        like_params: list = []
        if tag:
            like_sql += " AND tag = ?"
            like_params.append(tag)
        clauses = []
        for t in tokens:
            esc = f"%{_escape_like(t)}%"
            clauses.append(
                "(caption LIKE ? ESCAPE '\\' OR keywords LIKE ? ESCAPE '\\' OR tag LIKE ? ESCAPE '\\' OR file_name LIKE ? ESCAPE '\\')"
            )
            like_params.extend([esc, esc, esc, esc])
        if clauses:
            like_sql += " AND (" + " AND ".join(clauses) + ")"
        like_sql += " LIMIT ?"
        like_params.append(max(limit * 3, limit))
        like_rows = list(conn.execute(like_sql, like_params))

        seen: set[str] = set()
        for r in list(rows) + like_rows:
            p = r["path"]
            if p in seen:
                continue
            seen.add(p)
            cap = r["caption"] or ""
            kw = r["keywords"] or ""
            score = 0
            for t in tokens:
                if t in cap:
                    score += 3
                if t in kw:
                    score += 2
                if t == r["tag"]:
                    score += 4
                if t in (r["file_name"] or ""):
                    score += 1
            results.append(
                {
                    "path": absolutize_path(conn, p),
                    "tag": r["tag"],
                    "caption": cap,
                    "keywords": kw,
                    "score": score,
                }
            )
        results.sort(key=lambda x: (-x["score"], x["tag"], x["path"]))
        return results[:limit]

    # tag-only: random-ish by path order
    sql = "SELECT path, tag, caption, keywords FROM memes WHERE tag = ? ORDER BY file_name LIMIT ?"
    rows = conn.execute(sql, (tag, limit)).fetchall()
    return [
        {
            "path": absolutize_path(conn, r["path"]),
            "tag": r["tag"],
            "caption": r["caption"] or "",
            "keywords": r["keywords"] or "",
            "score": 0,
        }
        for r in rows
    ]


def stats(conn: sqlite3.Connection) -> dict:
    total = conn.execute("SELECT COUNT(*) AS c FROM memes").fetchone()["c"]
    captioned = conn.execute(
        "SELECT COUNT(*) AS c FROM memes WHERE caption IS NOT NULL AND caption != ''"
    ).fetchone()["c"]
    by_tag = {
        r["tag"]: r["c"]
        for r in conn.execute("SELECT tag, COUNT(*) AS c FROM memes GROUP BY tag ORDER BY tag")
    }
    return {"total": total, "captioned": captioned, "by_tag": by_tag}
