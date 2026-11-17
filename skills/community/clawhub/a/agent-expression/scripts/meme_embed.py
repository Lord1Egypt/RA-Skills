#!/usr/bin/env python3
"""Zhipu embedding-3 helpers for meme caption vector search."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable, Optional

import numpy as np

DEFAULT_MODEL = "embedding-3"
DEFAULT_BASE = "https://open.bigmodel.cn/api/paas/v4"
DEFAULT_DIM = 2048
BATCH_SIZE = 16

EMBED_SCHEMA = """
CREATE TABLE IF NOT EXISTS meme_embeddings (
  path TEXT PRIMARY KEY,
  model TEXT NOT NULL,
  dim INTEGER NOT NULL,
  vector BLOB NOT NULL,
  text_hash TEXT,
  embedded_at REAL
);
CREATE INDEX IF NOT EXISTS idx_meme_emb_model ON meme_embeddings(model);
"""


def _clear_proxy_env() -> None:
    for k in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        os.environ.pop(k, None)


def _load_dotenv() -> dict[str, str]:
    # Prefer shared loader from meme_db when available (same scripts dir).
    try:
        import importlib.util

        db_py = Path(__file__).resolve().parent / "meme_db.py"
        spec = importlib.util.spec_from_file_location("_ae_meme_db_env", db_py)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.load_dotenv_merged()
    except Exception:
        pass
    return {k: v for k, v in os.environ.items() if v}


def embed_config() -> dict[str, str]:
    env = _load_dotenv()
    api_key = (
        env.get("ZHIPU_API_KEY")
        or env.get("GLM_API_KEY")
        or env.get("Z_AI_API_KEY")
        or env.get("EMBEDDING_API_KEY")
        or ""
    ).strip()
    model = (
        env.get("ZHIPU_EMBEDDING_MODEL")
        or env.get("EMBEDDING_MODEL")
        or DEFAULT_MODEL
    ).strip()
    base = (
        env.get("ZHIPU_BASE_URL")
        or env.get("EMBEDDING_BASE_URL")
        or DEFAULT_BASE
    ).rstrip("/")
    return {"api_key": api_key, "model": model, "base_url": base}


def ensure_embed_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(EMBED_SCHEMA)


def embed_text_for_meme(tag: str, caption: str, keywords: str = "") -> str:
    parts = [p.strip() for p in (caption or "", keywords or "", tag or "") if p and p.strip()]
    return " ".join(parts)


def text_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def pack_vector(vec: list[float] | np.ndarray) -> bytes:
    arr = np.asarray(vec, dtype=np.float32)
    return arr.tobytes(order="C")


def unpack_vector(blob: bytes, dim: int) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32, count=dim)


def embed_texts(texts: list[str], *, cfg: Optional[dict] = None) -> list[list[float]]:
    """Call Zhipu embeddings API. Returns list of vectors aligned with texts."""
    if not texts:
        return []
    cfg = cfg or embed_config()
    if not cfg.get("api_key"):
        raise RuntimeError("ZHIPU_API_KEY not set")

    _clear_proxy_env()
    url = cfg["base_url"].rstrip("/") + "/embeddings"
    body = {"model": cfg["model"], "input": texts}
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json",
            "User-Agent": "agent-expression/meme-embed",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"embed HTTP {e.code}: {detail}") from e

    data = payload.get("data") or []
    # API may not preserve order; sort by index if present
    data = sorted(data, key=lambda d: int(d.get("index", 0)))
    if len(data) != len(texts):
        raise RuntimeError(f"embed count mismatch: got {len(data)} want {len(texts)}")
    out = []
    for item in data:
        emb = item.get("embedding")
        if not emb:
            raise RuntimeError("empty embedding in response")
        out.append(emb)
    return out


def upsert_embedding(
    conn: sqlite3.Connection,
    *,
    path: str,
    vector: list[float] | np.ndarray,
    model: str,
    text_hash_val: str,
) -> None:
    ensure_embed_schema(conn)
    arr = np.asarray(vector, dtype=np.float32)
    conn.execute(
        """INSERT INTO meme_embeddings(path, model, dim, vector, text_hash, embedded_at)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(path) DO UPDATE SET
             model=excluded.model,
             dim=excluded.dim,
             vector=excluded.vector,
             text_hash=excluded.text_hash,
             embedded_at=excluded.embedded_at
        """,
        (path, model, int(arr.shape[0]), pack_vector(arr), text_hash_val, time.time()),
    )


def rows_needing_embed(conn: sqlite3.Connection, *, model: str) -> list[dict]:
    ensure_embed_schema(conn)
    rows = conn.execute(
        """
        SELECT m.path, m.tag, m.caption, m.keywords, e.text_hash AS old_hash, e.model AS emb_model
        FROM memes m
        LEFT JOIN meme_embeddings e ON e.path = m.path
        WHERE m.caption IS NOT NULL AND m.caption != ''
        ORDER BY m.tag, m.path
        """
    ).fetchall()
    out = []
    for r in rows:
        text = embed_text_for_meme(r["tag"], r["caption"] or "", r["keywords"] or "")
        th = text_hash(text)
        if r["old_hash"] != th or (r["emb_model"] or "") != model:
            out.append(
                {
                    "path": r["path"],
                    "tag": r["tag"],
                    "caption": r["caption"] or "",
                    "keywords": r["keywords"] or "",
                    "text": text,
                    "text_hash": th,
                }
            )
    return out


def embed_meme_row(
    conn: sqlite3.Connection,
    *,
    path: str,
    tag: str,
    caption: str,
    keywords: str = "",
    cfg: Optional[dict] = None,
) -> None:
    cfg = cfg or embed_config()
    text = embed_text_for_meme(tag, caption, keywords)
    vec = embed_texts([text], cfg=cfg)[0]
    upsert_embedding(
        conn,
        path=path,
        vector=vec,
        model=cfg["model"],
        text_hash_val=text_hash(text),
    )


def load_matrix(
    conn: sqlite3.Connection,
    *,
    model: str,
    tag: Optional[str] = None,
) -> tuple[list[dict], np.ndarray]:
    """Return (meta list, float32 matrix [n,dim])."""
    ensure_embed_schema(conn)
    sql = """
      SELECT e.path, e.dim, e.vector, m.tag, m.caption, m.keywords
      FROM meme_embeddings e
      JOIN memes m ON m.path = e.path
      WHERE e.model = ?
    """
    params: list = [model]
    if tag:
        sql += " AND m.tag = ?"
        params.append(tag)
    rows = list(conn.execute(sql, params))
    if not rows:
        return [], np.zeros((0, DEFAULT_DIM), dtype=np.float32)
    dim = int(rows[0]["dim"])
    metas = []
    mats = []
    for r in rows:
        metas.append(
            {
                "path": r["path"],
                "tag": r["tag"],
                "caption": r["caption"] or "",
                "keywords": r["keywords"] or "",
            }
        )
        mats.append(unpack_vector(r["vector"], int(r["dim"])))
    return metas, np.vstack(mats).astype(np.float32)


def _resolve_result_path(conn: sqlite3.Connection, stored: str) -> str:
    import sys

    for mod in list(sys.modules.values()):
        fn = getattr(mod, "__file__", "") or ""
        if fn.endswith("meme_db.py") and hasattr(mod, "pack_dir_of") and hasattr(mod, "from_store_path"):
            pack = mod.pack_dir_of(conn)
            if pack is not None:
                return str(mod.from_store_path(pack, stored))
    return stored


def search_vector(
    conn: sqlite3.Connection,
    query: str,
    *,
    tag: Optional[str] = None,
    limit: int = 5,
    cfg: Optional[dict] = None,
    min_score: float = 0.25,
) -> list[dict]:
    """Embed query and rank by cosine similarity against stored caption vectors."""
    q = (query or "").strip()
    if not q:
        return []
    cfg = cfg or embed_config()
    if not cfg.get("api_key"):
        return []

    metas, mat = load_matrix(conn, model=cfg["model"], tag=tag)
    if mat.shape[0] == 0:
        return []

    qvec = np.asarray(embed_texts([q], cfg=cfg)[0], dtype=np.float32)
    qn = np.linalg.norm(qvec)
    if qn < 1e-8:
        return []
    qvec = qvec / qn
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-8)
    mat_n = mat / norms
    scores = mat_n @ qvec  # [n]

    top_k = min(max(limit * 3, limit), scores.shape[0])
    idx = np.argpartition(-scores, top_k - 1)[:top_k]
    idx = idx[np.argsort(-scores[idx])]

    results = []
    for i in idx:
        sc = float(scores[i])
        if sc < min_score:
            continue
        m = metas[int(i)]
        results.append(
            {
                "path": _resolve_result_path(conn, m["path"]),
                "tag": m["tag"],
                "caption": m["caption"],
                "keywords": m["keywords"],
                "score": round(sc * 100, 2),  # 0-100 scale for display
                "similarity": sc,
            }
        )
        if len(results) >= limit:
            break
    return results


def embed_stats(conn: sqlite3.Connection, *, model: Optional[str] = None) -> dict:
    ensure_embed_schema(conn)
    model = model or embed_config()["model"]
    total = conn.execute(
        "SELECT COUNT(*) AS c FROM memes WHERE caption IS NOT NULL AND caption != ''"
    ).fetchone()["c"]
    embedded = conn.execute(
        "SELECT COUNT(*) AS c FROM meme_embeddings WHERE model = ?", (model,)
    ).fetchone()["c"]
    return {"captioned": total, "embedded": embedded, "model": model}
