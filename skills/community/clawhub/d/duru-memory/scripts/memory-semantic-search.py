#!/usr/bin/env python3
"""
Incremental semantic search for markdown memory using:
- Ollama embeddings (default model: qwen3-embedding:0.6b)
- SQLite persistent cache
- sqlite-vec vector extension (via APSW)

Usage:
  memory-semantic-search.py "query" [workspace] [--top 8]
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import apsw
import sqlite_vec
from common import load_config, env_or_cfg, cfg_get

DEFAULT_MODEL = "qwen3-embedding:0.6b"
DEFAULT_OLLAMA = "http://127.0.0.1:11434"
PIPELINE_VERSION = "v2.1"


def now_iso():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def ollama_embed(base_url: str, model: str, text: str):
    payload = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    emb = data.get("embedding")
    if not emb:
        raise RuntimeError("empty embedding returned by ollama")
    return emb


def split_chunks(text: str, max_chars=900, overlap=180):
    text = normalize_text(text)
    if not text:
        return []
    out = []
    i = 0
    n = len(text)
    step = max(1, max_chars - overlap)
    while i < n:
        out.append(text[i : i + max_chars])
        i += step
    return out


def open_db(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = apsw.Connection(str(db_path))
    con.enable_load_extension(True)
    con.load_extension(sqlite_vec.loadable_path())
    cur = con.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    return con


def ensure_base_schema(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
          path TEXT PRIMARY KEY,
          mtime_ns INTEGER NOT NULL,
          size INTEGER NOT NULL,
          file_hash TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
          chunk_id TEXT PRIMARY KEY,
          path TEXT NOT NULL,
          chunk_index INTEGER NOT NULL,
          text_hash TEXT NOT NULL,
          chunk_text TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(path);")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS embedding_cache (
          text_hash TEXT PRIMARY KEY,
          model TEXT NOT NULL,
          dim INTEGER NOT NULL,
          embedding BLOB NOT NULL,
          created_at TEXT NOT NULL
        );
        """
    )


def get_meta(cur, key, default=None):
    row = cur.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row[0] if row else default


def set_meta(cur, key, value):
    cur.execute(
        "INSERT INTO meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, str(value)),
    )


def ensure_vec_table(cur, dim: int):
    stored_dim = get_meta(cur, "embedding_dim")
    if stored_dim is not None and int(stored_dim) != dim:
        # dimension changed => rebuild vector/chunk indexes
        cur.execute("DROP TABLE IF EXISTS vec_chunks;")
        cur.execute("DELETE FROM chunks;")
        cur.execute("DELETE FROM files;")

    cur.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(chunk_id TEXT PRIMARY KEY, embedding float[{dim}]);")
    set_meta(cur, "embedding_dim", dim)


def list_memory_files(memory_dir: Path):
    out = []
    for p in memory_dir.rglob("*.md"):
        rel = p.relative_to(memory_dir)
        if str(rel).startswith("archive/"):
            continue
        out.append(p)
    return sorted(out)


def get_file_rows(cur):
    rows = {}
    for path, mtime_ns, size, file_hash in cur.execute("SELECT path,mtime_ns,size,file_hash FROM files"):
        rows[path] = (int(mtime_ns), int(size), file_hash)
    return rows


def get_cached_embedding(cur, text_hash: str, model: str, dim: int):
    row = cur.execute(
        "SELECT embedding FROM embedding_cache WHERE text_hash=? AND model=? AND dim=?",
        (text_hash, model, dim),
    ).fetchone()
    return row[0] if row else None


def put_cached_embedding(cur, text_hash: str, model: str, dim: int, emb_blob: bytes):
    cur.execute(
        """
        INSERT INTO embedding_cache(text_hash,model,dim,embedding,created_at)
        VALUES(?,?,?,?,?)
        ON CONFLICT(text_hash) DO UPDATE SET model=excluded.model, dim=excluded.dim, embedding=excluded.embedding, created_at=excluded.created_at
        """,
        (text_hash, model, dim, emb_blob, now_iso()),
    )


def delete_path(cur, path_rel: str):
    ids = [r[0] for r in cur.execute("SELECT chunk_id FROM chunks WHERE path=?", (path_rel,))]
    for cid in ids:
        cur.execute("DELETE FROM vec_chunks WHERE chunk_id=?", (cid,))
    cur.execute("DELETE FROM chunks WHERE path=?", (path_rel,))
    cur.execute("DELETE FROM files WHERE path=?", (path_rel,))


def upsert_file_chunks(cur, workspace: Path, file_path: Path, model: str, dim: int, ollama_url: str):
    rel = str(file_path.relative_to(workspace))
    st = file_path.stat()
    mtime_ns = int(st.st_mtime_ns)
    size = int(st.st_size)
    file_hash = sha256_file(file_path)

    # reset old chunks for this path
    delete_path(cur, rel)

    raw = file_path.read_text(encoding="utf-8", errors="ignore")
    chunks = split_chunks(raw, max_chars=900, overlap=180)

    for i, ch in enumerate(chunks):
        text_hash = sha256_text(ch)
        cid = f"{rel}#c{i}:{text_hash[:12]}"

        emb_blob = get_cached_embedding(cur, text_hash, model, dim)
        if emb_blob is None:
            emb = ollama_embed(ollama_url, model, ch)
            if len(emb) != dim:
                raise RuntimeError(f"embedding dim mismatch for {rel}: expected {dim}, got {len(emb)}")
            emb_blob = sqlite_vec.serialize_float32(emb)
            put_cached_embedding(cur, text_hash, model, dim, emb_blob)

        cur.execute(
            "INSERT INTO chunks(chunk_id,path,chunk_index,text_hash,chunk_text,created_at) VALUES(?,?,?,?,?,?)",
            (cid, rel, i, text_hash, ch, now_iso()),
        )
        cur.execute(
            "INSERT INTO vec_chunks(chunk_id, embedding) VALUES(?, ?)",
            (cid, emb_blob),
        )

    cur.execute(
        "INSERT OR REPLACE INTO files(path,mtime_ns,size,file_hash,updated_at) VALUES(?,?,?,?,?)",
        (rel, mtime_ns, size, file_hash, now_iso()),
    )


def sync_index(cur, workspace: Path, memory_dir: Path, model: str, dim: int, ollama_url: str):
    db_files = get_file_rows(cur)
    disk_files = list_memory_files(memory_dir)
    disk_rel = {str(p.relative_to(workspace)): p for p in disk_files}

    # delete removed files
    for rel in list(db_files.keys()):
        if rel not in disk_rel:
            delete_path(cur, rel)

    indexed = 0
    skipped = 0
    for rel, p in disk_rel.items():
        st = p.stat()
        mtime_ns = int(st.st_mtime_ns)
        size = int(st.st_size)

        prev = db_files.get(rel)
        if prev and prev[0] == mtime_ns and prev[1] == size:
            skipped += 1
            continue

        # if size/mtime changed, hash check can still avoid reindex in rare same-content case
        file_hash = sha256_file(p)
        if prev and prev[2] == file_hash:
            cur.execute(
                "UPDATE files SET mtime_ns=?, size=?, updated_at=? WHERE path=?",
                (mtime_ns, size, now_iso(), rel),
            )
            skipped += 1
            continue

        upsert_file_chunks(cur, workspace, p, model, dim, ollama_url)
        indexed += 1

    return indexed, skipped


def run_query(cur, query_emb_blob: bytes, top_k: int):
    rows = list(
        cur.execute(
            """
            SELECT c.path, c.chunk_index, c.chunk_text, v.distance
            FROM vec_chunks v
            JOIN chunks c ON c.chunk_id = v.chunk_id
            WHERE v.embedding MATCH ? AND k = ?
            ORDER BY v.distance ASC
            LIMIT ?
            """,
            (query_emb_blob, top_k, top_k),
        )
    )

    path_best = {}
    for path, chunk_index, chunk_text, distance in rows:
        distance = float(distance)
        score = 1.0 / (1.0 + max(0.0, distance))
        prev = path_best.get(path)
        if prev is None or distance < prev["distance"]:
            path_best[path] = {
                "path": path,
                "score": round(score, 4),
                "distance": round(distance, 6),
                "chunk": int(chunk_index),
                "preview": chunk_text[:180],
            }

    hits = sorted(path_best.values(), key=lambda x: x["distance"])[:top_k]
    for h in hits:
        h.pop("distance", None)
        h.pop("chunk", None)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("workspace", nargs="?", default=os.getcwd())
    ap.add_argument("--config", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--ollama", default=None)
    ap.add_argument("--top", type=int, default=None)
    ap.add_argument("--min-score", type=float, default=None)
    ap.add_argument("--build-only", action="store_true", help="only sync index/cache, do not run retrieval")
    args = ap.parse_args()

    cfg = load_config(args.config)
    args.model = args.model or env_or_cfg("DURU_MEMORY_EMBEDDING_MODEL", cfg, "models.embedding", DEFAULT_MODEL)
    args.ollama = args.ollama or env_or_cfg("DURU_MEMORY_OLLAMA_URL", cfg, "ollama.base_url", DEFAULT_OLLAMA)
    if args.top is None:
        args.top = int(cfg_get(cfg, "semantic.top_k", 8))
    if args.min_score is None:
        args.min_score = float(cfg_get(cfg, "semantic.min_score", 0.48))

    workspace = Path(args.workspace).resolve()
    memory_dir = workspace / "memory"
    if not memory_dir.exists():
        print(f"memory directory not found: {memory_dir}", file=sys.stderr)
        sys.exit(1)

    probe_text = args.query if not args.build_only else "memory warmup"

    # Probe embedding first to get exact model dim
    try:
        q_vec = ollama_embed(args.ollama, args.model, probe_text)
    except Exception as e:
        print(f"semantic unavailable: {e}", file=sys.stderr)
        sys.exit(3)

    dim = len(q_vec)
    query_blob = sqlite_vec.serialize_float32(q_vec)

    db_path = memory_dir / ".semantic-index.db"
    con = open_db(db_path)
    cur = con.cursor()

    ensure_base_schema(cur)
    ensure_vec_table(cur, dim)
    set_meta(cur, "embedding_model", args.model)
    set_meta(cur, "pipeline_version", cfg_get(cfg, "semantic.pipeline_version", PIPELINE_VERSION))
    set_meta(cur, "last_query_at", now_iso())

    indexed, skipped = sync_index(cur, workspace, memory_dir, args.model, dim, args.ollama)
    hits = []
    if not args.build_only:
        raw_hits = run_query(cur, query_blob, top_k=max(1, args.top))
        hits = [h for h in raw_hits if float(h.get("score", 0.0)) >= float(args.min_score)]

    out = {
        "model": args.model,
        "dimension": dim,
        "index": {
            "db": str(db_path.relative_to(workspace)),
            "indexed_files": indexed,
            "skipped_files": skipped,
            "pipeline_version": cfg_get(cfg, "semantic.pipeline_version", PIPELINE_VERSION),
        },
        "min_score": args.min_score,
        "build_only": bool(args.build_only),
        "hits": hits,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
