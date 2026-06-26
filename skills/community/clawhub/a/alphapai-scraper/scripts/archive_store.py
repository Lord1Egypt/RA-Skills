#!/usr/bin/env python3
"""
Structured archive, SQLite/FTS, and vector search helpers for AlphaPai comments.
"""

from __future__ import annotations

import gc
import hashlib
import json
import os
import platform
import sqlite3
import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from common import ensure_runtime_dirs, resolve_path

warnings.filterwarnings("ignore")

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
KB_VENV_SITE = WORKSPACE_ROOT / "knowledge_bases/venv/lib/python3.9/site-packages"
HF_MODEL_CACHE_ROOT = Path.home() / ".cache/huggingface/hub" / "models--BAAI--bge-small-zh-v1.5"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"

if KB_VENV_SITE.exists():
    sys.path.insert(0, str(KB_VENV_SITE))

try:
    import chromadb  # type: ignore
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - environment fallback
    chromadb = None
    SentenceTransformer = None

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    source_name TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'alphapai',
    visibility TEXT NOT NULL DEFAULT 'shared',
    title TEXT NOT NULL,
    time_label TEXT NOT NULL,
    age_minutes INTEGER,
    content TEXT NOT NULL,
    source_strategy TEXT NOT NULL,
    raw_file TEXT NOT NULL,
    normalized_file TEXT NOT NULL,
    scraped_at TEXT NOT NULL,
    lookback_hours REAL NOT NULL,
    content_hash TEXT NOT NULL UNIQUE
);

CREATE VIRTUAL TABLE IF NOT EXISTS comments_fts USING fts5(
    id UNINDEXED,
    title,
    content,
    tokenize='unicode61'
);
"""

UPSERT_SQL = """
INSERT OR IGNORE INTO comments (
    id,
    run_id,
    source_name,
    scope,
    visibility,
    title,
    time_label,
    age_minutes,
    content,
    source_strategy,
    raw_file,
    normalized_file,
    scraped_at,
    lookback_hours,
    content_hash
) VALUES (
    :id,
    :run_id,
    :source_name,
    :scope,
    :visibility,
    :title,
    :time_label,
    :age_minutes,
    :content,
    :source_strategy,
    :raw_file,
    :normalized_file,
    :scraped_at,
    :lookback_hours,
    :content_hash
);
"""

FTS_UPSERT_SQL = """
INSERT OR REPLACE INTO comments_fts (rowid, id, title, content)
SELECT rowid, id, title, content
FROM comments
WHERE id = :id;
"""

DEFAULT_ENTITY_ALIASES: dict[str, list[str]] = {
    "英伟达": ["英伟达", "NVIDIA", "Nvda", "NVDA", "Blackwell", "GB200", "H20", "H100", "H200"],
    "台积电": ["台积电", "TSMC", "台积", "CoWoS"],
    "苹果": ["苹果", "Apple", "iPhone", "Vision Pro"],
    "特斯拉": ["特斯拉", "Tesla", "FSD", "Cybertruck"],
}

NEGATION_HINTS = [
    "无直接关系",
    "不相关",
    "无关",
    "没有关系",
    "关联不大",
]

_model: Any | None = None


def _detect_device() -> str:
    try:
        import torch  # type: ignore

        if platform.system() == "Darwin" and torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


DEVICE = _detect_device()


def _resolve_local_model_path() -> Path | None:
    refs_dir = HF_MODEL_CACHE_ROOT / "refs"
    snapshots_dir = HF_MODEL_CACHE_ROOT / "snapshots"

    ref_name = None
    ref_file = refs_dir / "main"
    if ref_file.exists():
        ref_name = ref_file.read_text(encoding="utf-8").strip()

    if ref_name:
        snapshot_dir = snapshots_dir / ref_name
        if snapshot_dir.exists():
            return snapshot_dir

    snapshot_candidates = sorted(
        [p for p in snapshots_dir.glob("*") if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return snapshot_candidates[0] if snapshot_candidates else None


def get_vector_model() -> Any | None:
    global _model
    if chromadb is None or SentenceTransformer is None:
        return None
    if _model is None:
        local_model_path = _resolve_local_model_path()
        if local_model_path is not None:
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
            os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
            _model = SentenceTransformer(
                str(local_model_path),
                device=DEVICE,
                local_files_only=True,
            )
        else:
            _model = SentenceTransformer(MODEL_NAME, device=DEVICE)
    return _model


def get_database_path(settings: dict[str, Any]) -> Path:
    base_dir = resolve_path(settings["output"]["base_dir"])
    assert base_dir is not None
    index_dir = base_dir / str(settings["archive"]["index_subdir"])
    return index_dir / str(settings["archive"]["database_name"])


def _ensure_comment_columns(conn: sqlite3.Connection) -> None:
    columns = {row[1] for row in conn.execute("PRAGMA table_info(comments)").fetchall()}
    if "scope" not in columns:
        conn.execute("ALTER TABLE comments ADD COLUMN scope TEXT NOT NULL DEFAULT 'alphapai'")
    if "visibility" not in columns:
        conn.execute("ALTER TABLE comments ADD COLUMN visibility TEXT NOT NULL DEFAULT 'shared'")
    conn.commit()


def connect_database(settings: dict[str, Any]) -> sqlite3.Connection:
    db_path = get_database_path(settings)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    _ensure_comment_columns(conn)
    return conn


def build_comment_id(run_id: str, title: str, time_label: str, content: str) -> str:
    seed = f"{run_id}|{title}|{time_label}|{content}".encode("utf-8")
    return hashlib.sha1(seed).hexdigest()[:16]


def build_content_hash(title: str, content: str) -> str:
    seed = f"{title}|{content}".encode("utf-8")
    return hashlib.sha1(seed).hexdigest()


def article_to_record(
    article: Any,
    *,
    settings: dict[str, Any],
    run_id: str,
    raw_file: str,
    normalized_file: str,
    scraped_at: str,
    lookback_hours: float,
) -> dict[str, Any]:
    title = str(getattr(article, "title", "") or "未命名点评").strip()
    time_label = str(getattr(article, "time_label", "") or "未知时间").strip()
    content = str(getattr(article, "content", "") or "").strip()
    source_strategy = str(getattr(article, "source_strategy", "unknown") or "unknown").strip()
    age_minutes = getattr(article, "age_minutes", None)
    return {
        "id": build_comment_id(run_id, title, time_label, content),
        "run_id": run_id,
        "source_name": "alphapai",
        "scope": str(settings["archive"].get("scope") or "alphapai"),
        "visibility": str(settings["archive"].get("visibility") or "shared"),
        "title": title,
        "time_label": time_label,
        "age_minutes": age_minutes,
        "content": content,
        "source_strategy": source_strategy,
        "raw_file": raw_file,
        "normalized_file": normalized_file,
        "scraped_at": scraped_at,
        "lookback_hours": lookback_hours,
        "content_hash": build_content_hash(title, content),
    }


def write_normalized_file(
    settings: dict[str, Any],
    *,
    run_id: str,
    raw_file: str,
    scraped_at: str,
    lookback_hours: float,
    articles: list[Any],
) -> str:
    runtime_dirs = ensure_runtime_dirs(settings)
    normalized_path = runtime_dirs["normalized_dir"] / f"{run_id}.json"
    records = [
        article_to_record(
            article,
            settings=settings,
            run_id=run_id,
            raw_file=raw_file,
            normalized_file=str(normalized_path),
            scraped_at=scraped_at,
            lookback_hours=lookback_hours,
        )
        for article in articles
    ]
    payload = {
        "run_id": run_id,
        "raw_file": raw_file,
        "scraped_at": scraped_at,
        "lookback_hours": lookback_hours,
        "count": len(records),
        "records": records,
    }
    normalized_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(normalized_path)


def _record_by_content_hash(conn: sqlite3.Connection, content_hash: str) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM comments WHERE content_hash = ?", (content_hash,)).fetchone()
    return dict(row) if row else None


def _record_by_id(conn: sqlite3.Connection, comment_id: str) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
    return dict(row) if row else None


def index_records(settings: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    inserted = 0
    canonical_records: list[dict[str, Any]] = []
    with connect_database(settings) as conn:
        for record in records:
            cursor = conn.execute(UPSERT_SQL, record)
            if cursor.rowcount:
                inserted += 1
                conn.execute(FTS_UPSERT_SQL, {"id": record["id"]})
                canonical_records.append(record)
            else:
                existing = _record_by_content_hash(conn, record["content_hash"])
                if existing:
                    canonical_records.append(existing)
        conn.commit()
    return {
        "inserted": inserted,
        "total": len(records),
        "db_path": str(get_database_path(settings)),
        "canonical_records": canonical_records,
    }


def chunk_text(text: str, chunk_size: int = 420, overlap: int = 80) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            for sep in ["。", "！", "？", "\n\n", "\n", "；", ".", "!", "?"]:
                idx = chunk.rfind(sep)
                if idx > chunk_size // 2:
                    chunk = chunk[: idx + 1]
                    break
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start += max(len(chunk) - overlap, 1)
        if start >= len(text):
            break
    return chunks


def get_vector_path(settings: dict[str, Any]) -> Path:
    base_dir = resolve_path(settings["output"]["base_dir"])
    assert base_dir is not None
    return (
        base_dir
        / str(settings["archive"]["index_subdir"])
        / str(settings["archive"]["vector_subdir"])
    )


def get_vector_collection(settings: dict[str, Any]):
    if chromadb is None:
        return None
    vector_path = get_vector_path(settings)
    vector_path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(vector_path))
    return client.get_or_create_collection(
        name=str(settings["archive"].get("vector_collection") or "alphapai_comments"),
        embedding_function=None,
        metadata={"hnsw:space": "cosine"},
    )


def index_vector_records(settings: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {
            "enabled": chromadb is not None,
            "indexed_comments": 0,
            "indexed_chunks": 0,
            "vector_path": str(get_vector_path(settings)),
        }

    model = get_vector_model()
    collection = get_vector_collection(settings)
    if model is None or collection is None:
        return {
            "enabled": False,
            "indexed_comments": 0,
            "indexed_chunks": 0,
            "vector_path": str(get_vector_path(settings)),
            "reason": "向量依赖不可用",
        }

    chunk_size = int(settings["archive"].get("vector_chunk_size") or 420)
    overlap = int(settings["archive"].get("vector_chunk_overlap") or 80)
    batch_size = int(settings["archive"].get("vector_batch_size") or 8)

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict[str, Any]] = []
    for record in records:
        source_text = f"{record['title']}\n\n{record['content']}".strip()
        for index, chunk in enumerate(chunk_text(source_text, chunk_size=chunk_size, overlap=overlap)):
            ids.append(f"{record['id']}::{index}")
            documents.append(chunk)
            metadatas.append(
                {
                    "comment_id": record["id"],
                    "title": record.get("title", ""),
                    "time_label": record.get("time_label", ""),
                    "scraped_at": record.get("scraped_at", ""),
                    "source_name": record.get("source_name", "alphapai"),
                    "scope": record.get("scope", "alphapai"),
                    "visibility": record.get("visibility", "shared"),
                    "source_strategy": record.get("source_strategy", ""),
                    "chunk_index": index,
                }
            )

    embeddings: list[list[float]] = []
    for batch_start in range(0, len(documents), batch_size):
        batch_docs = documents[batch_start : batch_start + batch_size]
        embeddings.extend(model.encode(batch_docs, show_progress_bar=False).tolist())

    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
    del embeddings, documents, metadatas
    gc.collect()
    return {
        "enabled": True,
        "indexed_comments": len(records),
        "indexed_chunks": len(ids),
        "vector_path": str(get_vector_path(settings)),
    }


def index_articles(
    settings: dict[str, Any],
    *,
    run_id: str,
    raw_file: str,
    scraped_at: str,
    lookback_hours: float,
    articles: list[Any],
) -> dict[str, Any]:
    normalized_path = write_normalized_file(
        settings,
        run_id=run_id,
        raw_file=raw_file,
        scraped_at=scraped_at,
        lookback_hours=lookback_hours,
        articles=articles,
    )
    records = [
        article_to_record(
            article,
            settings=settings,
            run_id=run_id,
            raw_file=raw_file,
            normalized_file=normalized_path,
            scraped_at=scraped_at,
            lookback_hours=lookback_hours,
        )
        for article in articles
    ]
    result = index_records(settings, records)
    vector_result = index_vector_records(settings, result.get("canonical_records", []))
    result["normalized_file"] = normalized_path
    result["vector_enabled"] = vector_result.get("enabled", False)
    result["vector_path"] = vector_result.get("vector_path", str(get_vector_path(settings)))
    result["vector_chunks"] = vector_result.get("indexed_chunks", 0)
    if vector_result.get("reason"):
        result["vector_reason"] = vector_result["reason"]
    return result


def normalize_query_terms(query: str, aliases: dict[str, list[str]] | None = None) -> list[str]:
    terms: list[str] = []
    source = aliases or DEFAULT_ENTITY_ALIASES
    query_lower = query.lower()
    for canonical, variants in source.items():
        if canonical in query and canonical not in terms:
            terms.append(canonical)
        for variant in variants:
            if variant.lower() in query_lower:
                if canonical not in terms:
                    terms.append(canonical)
                if variant not in terms:
                    terms.append(variant)
    if not terms:
        for token in query.replace("，", " ").replace(",", " ").split():
            cleaned = token.strip()
            if cleaned and cleaned not in terms:
                terms.append(cleaned)
    return terms


def _build_match_expression(terms: list[str]) -> str:
    cleaned = [term.replace('"', ' ').strip() for term in terms if term.strip()]
    if not cleaned:
        return ""
    return " OR ".join(f'"{term}"' for term in cleaned)


def _enrich_exact_item(base: dict[str, Any], *, score: float, mode: str) -> dict[str, Any]:
    item = dict(base)
    item["exact_score"] = max(float(item.get("exact_score") or 0.0), score)
    modes = set(item.get("retrieval_modes") or [])
    modes.add(mode)
    item["retrieval_modes"] = sorted(modes)
    item["retrieval_score"] = max(float(item.get("retrieval_score") or 0.0), score)
    return item


def _apply_precision_hints(item: dict[str, Any]) -> dict[str, Any]:
    text = f"{item.get('title', '')}\n{item.get('content', '')}"
    penalty = 0.0
    if any(marker in text for marker in NEGATION_HINTS):
        penalty = 0.35
    item["precision_penalty"] = penalty
    item["retrieval_score"] = max(float(item.get("retrieval_score") or 0.0) - penalty, 0.0)
    if penalty:
        item["negation_hint"] = True
    return item


def _query_exact_comments(
    settings: dict[str, Any],
    *,
    terms: list[str],
    lookback_days: float,
    limit: int,
) -> list[dict[str, Any]]:
    match_expr = _build_match_expression(terms)
    if not terms:
        return []

    since = (datetime.now() - timedelta(days=lookback_days)).isoformat(timespec="seconds")
    merged: dict[str, dict[str, Any]] = {}

    with connect_database(settings) as conn:
        if match_expr:
            fts_sql = """
            SELECT c.*
            FROM comments_fts f
            JOIN comments c ON c.rowid = f.rowid
            WHERE comments_fts MATCH ?
              AND c.scraped_at >= ?
            ORDER BY c.scraped_at DESC, COALESCE(c.age_minutes, 999999) ASC
            LIMIT ?;
            """
            for row in conn.execute(fts_sql, (match_expr, since, limit)).fetchall():
                item = _enrich_exact_item(dict(row), score=1.0, mode="exact_fts")
                merged[item["id"]] = item

        like_clauses = []
        params: list[Any] = [since]
        for term in terms:
            like_clauses.append("(title LIKE ? OR content LIKE ?)")
            like_value = f"%{term}%"
            params.extend([like_value, like_value])
        params.append(limit)
        like_sql = f"""
        SELECT *
        FROM comments
        WHERE scraped_at >= ?
          AND ({' OR '.join(like_clauses)})
        ORDER BY scraped_at DESC, COALESCE(age_minutes, 999999) ASC
        LIMIT ?;
        """
        for row in conn.execute(like_sql, params).fetchall():
            item = merged.get(row["id"], dict(row))
            item = _enrich_exact_item(item, score=0.82, mode="exact_like")
            merged[item["id"]] = item

    return sorted(
        merged.values(),
        key=lambda item: (float(item.get("retrieval_score") or 0.0), item.get("scraped_at", "")),
        reverse=True,
    )[:limit]


def _build_vector_query(query: str, terms: list[str]) -> str:
    extras = [term for term in terms if term not in query]
    if not extras:
        return query
    return f"{query}\n相关实体：{' / '.join(extras[:8])}"


def _fetch_comments_by_ids(settings: dict[str, Any], comment_ids: list[str]) -> dict[str, dict[str, Any]]:
    if not comment_ids:
        return {}
    placeholders = ",".join("?" for _ in comment_ids)
    with connect_database(settings) as conn:
        rows = conn.execute(
            f"SELECT * FROM comments WHERE id IN ({placeholders})",
            comment_ids,
        ).fetchall()
    return {row["id"]: dict(row) for row in rows}


def _query_vector_comments(
    settings: dict[str, Any],
    *,
    query: str,
    terms: list[str],
    lookback_days: float,
    limit: int,
    score_threshold: float | None = None,
) -> dict[str, Any]:
    model = get_vector_model()
    collection = get_vector_collection(settings)
    vector_path = str(get_vector_path(settings))
    if model is None or collection is None:
        return {"items": [], "vector_path": vector_path, "enabled": False, "reason": "向量依赖不可用"}
    if collection.count() == 0:
        return {"items": [], "vector_path": vector_path, "enabled": True, "reason": "向量索引为空"}

    since = (datetime.now() - timedelta(days=lookback_days)).isoformat(timespec="seconds")
    threshold = score_threshold if score_threshold is not None else float(settings["archive"].get("vector_score_threshold") or 0.3)
    top_k = max(limit, int(settings["archive"].get("vector_top_k") or limit))
    query_embedding = model.encode([_build_vector_query(query, terms)], show_progress_bar=False).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    grouped: dict[str, dict[str, Any]] = {}
    for doc, meta, dist in zip(
        results.get("documents", [[]])[0],
        results.get("metadatas", [[]])[0],
        results.get("distances", [[]])[0],
    ):
        score = 1 - dist
        if score < threshold:
            continue
        if str(meta.get("scraped_at") or "") < since:
            continue
        comment_id = str(meta.get("comment_id") or "").strip()
        if not comment_id:
            continue
        current = grouped.get(comment_id)
        snippet = str(doc or "").strip()[:220]
        if not current or score > current["vector_score"]:
            grouped[comment_id] = {
                "comment_id": comment_id,
                "vector_score": round(score, 4),
                "vector_preview": snippet,
                "retrieval_modes": ["vector"],
                "retrieval_score": round(score, 4),
            }

    db_items = _fetch_comments_by_ids(settings, list(grouped.keys()))
    items: list[dict[str, Any]] = []
    for comment_id, hit in grouped.items():
        base = db_items.get(comment_id)
        if not base:
            continue
        item = dict(base)
        item.update(hit)
        items.append(item)

    items.sort(
        key=lambda item: (float(item.get("vector_score") or 0.0), item.get("scraped_at", "")),
        reverse=True,
    )
    return {"items": items[:limit], "vector_path": vector_path, "enabled": True}


def query_comments(
    settings: dict[str, Any],
    *,
    query: str,
    lookback_days: float = 7,
    limit: int = 50,
    aliases: dict[str, list[str]] | None = None,
    retrieval_mode: str = "hybrid",
    score_threshold: float | None = None,
) -> dict[str, Any]:
    terms = normalize_query_terms(query, aliases=aliases)
    if not terms:
        return {
            "terms": [],
            "items": [],
            "db_path": str(get_database_path(settings)),
            "vector_path": str(get_vector_path(settings)),
            "lookback_days": lookback_days,
            "retrieval_mode": retrieval_mode,
        }

    exact_items = []
    vector_result: dict[str, Any] = {"items": [], "vector_path": str(get_vector_path(settings))}
    if retrieval_mode in {"exact", "hybrid"}:
        exact_items = _query_exact_comments(settings, terms=terms, lookback_days=lookback_days, limit=limit)
    if retrieval_mode in {"vector", "hybrid"}:
        vector_result = _query_vector_comments(
            settings,
            query=query,
            terms=terms,
            lookback_days=lookback_days,
            limit=limit,
            score_threshold=score_threshold,
        )

    merged: dict[str, dict[str, Any]] = {}
    for item in exact_items:
        merged[item["id"]] = dict(item)
    for item in vector_result.get("items", []):
        existing = merged.get(item["id"])
        if existing:
            modes = set(existing.get("retrieval_modes") or [])
            modes.update(item.get("retrieval_modes") or [])
            existing["retrieval_modes"] = sorted(modes)
            existing["vector_score"] = max(float(existing.get("vector_score") or 0.0), float(item.get("vector_score") or 0.0))
            existing["retrieval_score"] = max(
                float(existing.get("exact_score") or 0.0) * 1.15 + float(existing.get("vector_score") or 0.0),
                float(item.get("vector_score") or 0.0),
            )
            if item.get("vector_preview") and not existing.get("vector_preview"):
                existing["vector_preview"] = item["vector_preview"]
        else:
            item = dict(item)
            item["retrieval_score"] = max(float(item.get("retrieval_score") or 0.0), float(item.get("vector_score") or 0.0))
            merged[item["id"]] = item

    items = sorted(
        [_apply_precision_hints(item) for item in merged.values()],
        key=lambda item: (
            float(item.get("retrieval_score") or 0.0),
            item.get("scraped_at", ""),
            -(int(item.get("age_minutes") or 999999)),
        ),
        reverse=True,
    )[:limit]
    match_expr = _build_match_expression(terms)
    result = {
        "terms": terms,
        "match_expr": match_expr,
        "items": items,
        "db_path": str(get_database_path(settings)),
        "vector_path": vector_result.get("vector_path", str(get_vector_path(settings))),
        "lookback_days": lookback_days,
        "retrieval_mode": retrieval_mode,
        "vector_enabled": vector_result.get("enabled", False),
    }
    if vector_result.get("reason"):
        result["vector_reason"] = vector_result["reason"]
    return result
