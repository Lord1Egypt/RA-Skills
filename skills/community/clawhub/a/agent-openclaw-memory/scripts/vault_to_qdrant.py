"""
vault_to_qdrant.py — Vault → Qdrant incremental sync

Syncs markdown files from vault directories to Qdrant vector database.
Chunks markdown by headings, embeds via LM Studio, stores with version tracking.

Usage: python scripts/vault_to_qdrant.py
"""
import os
import re
import json
import uuid
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from shared_config import (
    VAULT_DIR, LMSTUDIO_EMBED_URL as LMSTUDIO_URL, LMSTUDIO_KEY,
    EMBED_MODEL, QDRANT_URL, KB_COLLECTION, SYNC_DIRS, EMBEDDING_WORKERS,
)
from qdrant_utils import QDRANT_URL as QDRANT_BASE_URL
QDRANT_POINTS_URL = f"{QDRANT_URL}/collections/{KB_COLLECTION}/points"

CHUNK_LINES = 15
STATE_FILE = Path(__file__).resolve().parent / ".vault_sync_state.json"

TECH_KEYWORDS = {
    "python", "javascript", "typescript", "rust", "go", "node",
    "react", "vue", "angular", "django", "flask", "fastapi",
    "sql", "postgresql", "mysql", "sqlite", "redis", "mongodb",
    "docker", "kubernetes", "nginx", "git", "api", "rest",
    "graphql", "websocket", "oauth", "jwt", "auth", "middleware",
    "vector", "embedding", "qdrant", "llm", "openai", "claude",
    "token", "prompt", "model", "training", "session",
    "pytest", "jest", "unittest", "ci/cd", "github", "action",
    "cache", "webhook", "async", "config", "memory",
    "agent", "heartbeat", "cron", "vault", "distill", "compress",
}

SKIP_PATTERNS = ["cache-optimization", "chat-", "cost-report", "MOC.md"]


def _extract_concepts(text: str) -> list:
    combined = text.lower()
    found = set()
    for kw in TECH_KEYWORDS:
        if kw in combined:
            found.add(kw)
    file_exts = re.findall(r'\.(\w+)(?:\s|$|/)', combined)
    for ext in file_exts:
        if ext in ("py", "js", "ts", "rs", "go", "java", "sql", "yaml", "yml",
                    "json", "md", "html", "css", "sh", "bat", "ps1"):
            found.add(f".{ext}")
    return sorted(found)


def should_sync(rel_path):
    in_sync_dir = any(rel_path.startswith(d) for d in SYNC_DIRS)
    if not in_sync_dir:
        return False
    filename = os.path.basename(rel_path)
    for pattern in SKIP_PATTERNS:
        if pattern in filename:
            return False
    full_path = os.path.join(VAULT_DIR, rel_path)
    if os.path.getsize(full_path) == 0:
        return False
    return True


def file_hash(path):
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except Exception:
        return None
    return h.hexdigest()


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"files": {}, "last_sync": None}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_embedding(text):
    from embedder import get_embedding as _embed
    return _embed(text)


def chunk_markdown(text, source_path):
    lines = text.split("\n")
    chunks = []
    current_heading = "概述"
    current_lines = []

    for line in lines:
        heading_match = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading_match:
            if current_lines:
                chunk_text = "\n".join(current_lines).strip()
                if len(chunk_text) > 20:
                    chunks.append({
                        "heading": current_heading,
                        "text": chunk_text,
                        "source": source_path,
                        "pipeline": "vault_sync",
                        "type": "knowledge",
                        "concepts": _extract_concepts(chunk_text),
                        "title": current_heading if current_heading != "概述" else Path(source_path).stem[:60]
                    })
            current_heading = heading_match.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)
            if len(current_lines) >= CHUNK_LINES:
                chunk_text = "\n".join(current_lines).strip()
                if len(chunk_text) > 20:
                    chunks.append({
                        "heading": current_heading,
                        "text": chunk_text,
                        "source": source_path,
                        "pipeline": "vault_sync",
                        "type": "knowledge",
                        "concepts": _extract_concepts(chunk_text),
                        "title": current_heading if current_heading != "概述" else Path(source_path).stem[:60]
                    })
                current_lines = []

    if current_lines:
        chunk_text = "\n".join(current_lines).strip()
        if len(chunk_text) > 20:
            chunks.append({
                "heading": current_heading,
                "text": chunk_text,
                "source": source_path,
                "pipeline": "vault_sync",
                "type": "knowledge",
                "concepts": _extract_concepts(chunk_text),
                "title": current_heading if current_heading != "概述" else Path(source_path).stem[:60]
            })
    return chunks


def mark_deleted_for_source(source_path):
    try:
        resp = requests.post(
            f"{QDRANT_POINTS_URL}/scroll",
            json={"limit": 1000, "with_payload": ["source"],
                  "filter": {"must": [{"key": "source", "match": {"value": source_path}}]}},
            timeout=10
        )
        if resp.status_code == 200:
            points = resp.json().get("result", {}).get("points", [])
            ids = [p["id"] for p in points]
            if ids:
                requests.post(
                    f"{QDRANT_POINTS_URL}/payload",
                    json={"points": ids, "payload": {"deleted": True, "is_latest": False}},
                    timeout=10
                )
                return len(ids)
        return 0
    except Exception:
        return 0


def get_latest_version(source_path):
    try:
        resp = requests.post(
            f"{QDRANT_POINTS_URL}/scroll",
            json={"limit": 50, "with_payload": ["source", "version"],
                  "filter": {"must": [{"key": "source", "match": {"value": source_path}}]}},
            timeout=10
        )
        if resp.status_code == 200:
            points = resp.json().get("result", {}).get("points", [])
            if points:
                return max(p.get("payload", {}).get("version", 0) for p in points)
        return 0
    except Exception:
        return 0


def mark_old_versions_not_latest(source_path):
    try:
        resp = requests.post(
            f"{QDRANT_POINTS_URL}/scroll",
            json={"limit": 1000, "with_payload": ["source", "version", "is_latest"],
                  "filter": {"must": [
                      {"key": "source", "match": {"value": source_path}},
                      {"key": "is_latest", "match": {"value": True}}
                  ]}},
            timeout=10
        )
        if resp.status_code == 200:
            points = resp.json().get("result", {}).get("points", [])
            ids = [p["id"] for p in points]
            if ids:
                requests.post(
                    f"{QDRANT_POINTS_URL}/payload",
                    json={"points": ids, "payload": {"is_latest": False}},
                    timeout=10
                )
                return ids
        return []
    except Exception:
        return []


def store_in_qdrant(chunks, file_mtime=None, supersede_ids=None):
    points = []
    mtime = file_mtime or 0
    old_ver = 0
    if chunks:
        old_ver = get_latest_version(chunks[0]["source"])
    new_version = int(old_ver) + 1
    supersedes = supersede_ids or []
    change_summary = f"v{new_version}" if new_version > 1 else "initial"

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk["text"])
        if embedding is None:
            continue
        if hasattr(embedding, 'tolist'):
            embedding = embedding.tolist()
        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{chunk['source']}#{i}#{mtime}#v{new_version}"))
        points.append({
            "id": point_id,
            "vector": embedding,
            "payload": {
                "source": chunk["source"],
                "heading": chunk["heading"],
                "text": chunk["text"][:2000],
                "type": chunk.get("type", "knowledge"),
                "title": chunk.get("title", Path(chunk["source"]).stem[:60]),
                "concepts": chunk.get("concepts", []),
                "chunk_index": i,
                "file_name": Path(chunk["source"]).name,
                "file_path": os.path.relpath(chunk["source"], str(VAULT_DIR)).replace("\\", "/"),
                "updated_at": datetime.now().isoformat(),
                "content_hash": hashlib.md5(chunk["text"].encode()).hexdigest(),
                "file_mtime": os.path.getmtime(chunk["source"]) if os.path.exists(chunk["source"]) else 0,
                "version": new_version,
                "change_summary": change_summary,
                "supersedes": supersedes,
                "is_latest": True,
                "deleted": False,
                "pipeline": "vault_sync"
            }
        })

    if not points:
        return 0

    stored = 0
    for i in range(0, len(points), 100):
        batch = points[i:i+100]
        try:
            resp = requests.put(
                f"{QDRANT_POINTS_URL}?wait=true",
                json={"points": batch},
                timeout=30
            )
            if resp.status_code == 200:
                stored += len(batch)
        except Exception:
            pass
    return stored


def main():
    print("=" * 50)
    print("[INFO] Vault → Qdrant sync")
    print("=" * 50)

    from embedder import prewarm
    emb_ready = prewarm()
    print(f"  Embedding ready: {emb_ready}")

    state = load_state()
    old_files = set(state["files"].keys())

    all_files = []
    for root, dirs, files in os.walk(VAULT_DIR):
        if ".obsidian" in root or ".git" in root:
            continue
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, VAULT_DIR)
                all_files.append((full_path, rel_path))

    current_files = set()
    added = changed = deleted = skipped_noise = total_chunks = total_stored = 0

    print(f"  Found {len(all_files)} markdown files")

    all_chunks_data = []
    for full_path, rel_path in all_files:
        if not should_sync(rel_path):
            skipped_noise += 1
            continue

        current_files.add(rel_path)
        current_hash = file_hash(full_path)
        old_info = state["files"].get(rel_path, {})

        if old_info.get("hash") == current_hash:
            continue

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                text = f.read()
        except:
            try:
                with open(full_path, "r", encoding="gbk") as f:
                    text = f.read()
            except:
                continue

        supersede_ids = []
        if rel_path in old_files:
            supersede_ids = mark_old_versions_not_latest(full_path)
            changed += 1
        else:
            added += 1

        file_mtime = os.path.getmtime(full_path)
        chunks = chunk_markdown(text, full_path)
        if chunks:
            all_chunks_data.append((chunks, file_mtime, supersede_ids, rel_path, current_hash))

    print(f"  {len(all_chunks_data)} files to sync, embedding with {EMBEDDING_WORKERS} workers...")

    def _embed_file(data):
        chunks, file_mtime, supersede_ids, rel_path, current_hash = data
        n_stored = store_in_qdrant(chunks, file_mtime=file_mtime, supersede_ids=supersede_ids)
        return {"rel_path": rel_path, "n_chunks": len(chunks), "n_stored": n_stored,
                "current_hash": current_hash, "file_mtime": file_mtime}

    results = []
    if len(all_chunks_data) <= 3:
        for data in all_chunks_data:
            results.append(_embed_file(data))
    else:
        with ThreadPoolExecutor(max_workers=EMBEDDING_WORKERS) as pool:
            futures = [pool.submit(_embed_file, data) for data in all_chunks_data]
            for future in as_completed(futures):
                results.append(future.result())

    for r in results:
        rel_path = r["rel_path"]
        total_chunks += r["n_chunks"]
        total_stored += r["n_stored"]
        state["files"][rel_path] = {"hash": r["current_hash"], "chunks": r["n_chunks"], "mtime": r["file_mtime"]}
        print(f"  [OK] {rel_path} → {r['n_chunks']} chunks, {r['n_stored']} stored")

    deleted_files = old_files - current_files
    for rel_path in deleted_files:
        full_path = os.path.join(VAULT_DIR, rel_path)
        marked = mark_deleted_for_source(full_path)
        if marked > 0:
            print(f"  [DEL] {rel_path}: marked {marked} vectors as deleted")
            deleted += 1
        del state["files"][rel_path]

    state["last_sync"] = datetime.now().isoformat()
    save_state(state)

    print(f"\n{'=' * 50}")
    print(f"[OK] Sync complete:")
    print(f"  Added: {added}, Changed: {changed}, Deleted: {deleted}")
    print(f"  Skipped (noise): {skipped_noise}")
    print(f"  Vectors stored: {total_stored}")
    print(f"{'=' * 50}")

    from embedder import print_stats
    print_stats()


if __name__ == "__main__":
    main()
