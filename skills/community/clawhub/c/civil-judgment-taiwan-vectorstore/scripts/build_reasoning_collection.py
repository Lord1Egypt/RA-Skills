#!/usr/bin/env python3
"""Build civil_case_reasoning collection from civil_case_doc.

Reads all civil_case_doc points, expands each reasoning_snippets[] entry into
an individual vector point in civil_case_reasoning.

Re-running is always safe — point IDs are deterministic (MD5 of doc_sha256 +
snippet index), so repeated runs produce upserts, not duplicates.

Usage:
    python3 scripts/build_reasoning_collection.py [options]

Examples:
    # Full rebuild (will take a few minutes — one Ollama call per snippet)
    python3 scripts/build_reasoning_collection.py

    # Dry run — count snippets without writing anything
    python3 scripts/build_reasoning_collection.py --dry-run

    # Test with first 10 source docs
    python3 scripts/build_reasoning_collection.py --limit 10

    # Custom endpoints
    python3 scripts/build_reasoning_collection.py \\
        --ollama http://192.168.122.1:11434 --qdrant http://192.168.122.1:6333
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from typing import Any, Dict, List

import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REASONING_COLLECTION = "civil_case_reasoning"
SOURCE_COLLECTION = "civil_case_doc"
DEFAULT_VECTOR_SIZE = 1024
DEFAULT_DISTANCE = qm.Distance.COSINE
UPSERT_BATCH_SIZE = 64


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class PreflightError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Utilities (mirrors patterns in ingest.py)
# ---------------------------------------------------------------------------


def make_uuid(seed: str) -> str:
    """Deterministic UUID-format string from an arbitrary seed string."""
    h = hashlib.md5(seed.encode("utf-8")).hexdigest()
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def ollama_embed(text: str, *, ollama: str, model: str, timeout: int = 60) -> List[float]:
    url = ollama.rstrip("/") + "/api/embeddings"
    r = requests.post(url, json={"model": model, "prompt": text}, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    emb = data.get("embedding")
    if not isinstance(emb, list):
        raise RuntimeError(f"Unexpected Ollama response: {data}")
    return emb


def ensure_collection(client: QdrantClient, name: str, *, vector_size: int, distance: qm.Distance) -> None:
    try:
        client.get_collection(name)
    except Exception:
        client.create_collection(
            collection_name=name,
            vectors_config=qm.VectorParams(size=vector_size, distance=distance),
        )


def upsert_batched(client: QdrantClient, collection: str, points: List[qm.PointStruct]) -> int:
    if not points:
        return 0
    total = 0
    for i in range(0, len(points), UPSERT_BATCH_SIZE):
        batch = points[i : i + UPSERT_BATCH_SIZE]
        client.upsert(collection_name=collection, points=batch)
        total += len(batch)
    return total


def scroll_all(client: QdrantClient, collection: str) -> List[Any]:
    points = []
    offset = None
    while True:
        result = client.scroll(
            collection_name=collection,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        pts, next_offset = result
        points.extend(pts)
        if next_offset is None:
            break
        offset = next_offset
    return points


# ---------------------------------------------------------------------------
# Pre-flight
# ---------------------------------------------------------------------------


def preflight(*, qdrant_url: str, ollama_url: str, embed_model: str) -> None:
    # Qdrant reachable
    try:
        r = requests.get(qdrant_url.rstrip("/") + "/collections", timeout=5)
        if r.status_code != 200:
            raise PreflightError(f"Qdrant not ready: GET /collections -> {r.status_code}")
    except requests.exceptions.ConnectionError as e:
        raise PreflightError(f"Qdrant not reachable at {qdrant_url}: {e}") from e

    # Source collection exists
    try:
        r = requests.get(qdrant_url.rstrip("/") + f"/collections/{SOURCE_COLLECTION}", timeout=5)
        if r.status_code != 200:
            raise PreflightError(
                f"Source collection '{SOURCE_COLLECTION}' not found. Run ingest.py first."
            )
    except requests.exceptions.ConnectionError as e:
        raise PreflightError(f"Qdrant not reachable: {e}") from e

    # Ollama reachable
    try:
        r = requests.get(ollama_url.rstrip("/") + "/api/tags", timeout=5)
        if r.status_code != 200:
            raise PreflightError(f"Ollama not ready: GET /api/tags -> {r.status_code}")
    except requests.exceptions.ConnectionError as e:
        raise PreflightError(f"Ollama not reachable at {ollama_url}: {e}") from e

    # Model available
    models = [m["name"] for m in r.json().get("models", [])]
    if embed_model not in models:
        raise PreflightError(
            f"Ollama model missing: {embed_model}. Pull it first: ollama pull {embed_model}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Build civil_case_reasoning from civil_case_doc reasoning_snippets."
    )
    ap.add_argument(
        "--ollama",
        default=os.environ.get("OLLAMA_URL", "http://localhost:11434"),
        help="Ollama base URL",
    )
    ap.add_argument(
        "--qdrant",
        default=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        help="Qdrant base URL",
    )
    ap.add_argument("--embed-model", default="bge-m3:latest")
    ap.add_argument("--vector-size", type=int, default=DEFAULT_VECTOR_SIZE)
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Process only first N source docs (0 = no limit; useful for testing)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and count without embedding or writing to Qdrant",
    )
    ap.add_argument(
        "--rebuild",
        action="store_true",
        help="Drop and recreate civil_case_reasoning before building (removes stale/incompatible points)",
    )
    args = ap.parse_args()

    # --- Pre-flight ---
    if not args.dry_run:
        try:
            preflight(
                qdrant_url=args.qdrant,
                ollama_url=args.ollama,
                embed_model=args.embed_model,
            )
        except PreflightError as e:
            print(f"PREFLIGHT_FAILED: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Dry run: only check Qdrant source collection
        try:
            r = requests.get(
                args.qdrant.rstrip("/") + f"/collections/{SOURCE_COLLECTION}", timeout=5
            )
            if r.status_code != 200:
                print(f"PREFLIGHT_FAILED: Source collection '{SOURCE_COLLECTION}' not found.", file=sys.stderr)
                sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            print(f"PREFLIGHT_FAILED: Qdrant not reachable: {e}", file=sys.stderr)
            sys.exit(1)

    client = QdrantClient(url=args.qdrant)

    if not args.dry_run:
        if args.rebuild:
            try:
                client.delete_collection(REASONING_COLLECTION)
                print(f"Dropped existing '{REASONING_COLLECTION}' collection.")
            except Exception:
                pass  # didn't exist yet
        ensure_collection(
            client,
            REASONING_COLLECTION,
            vector_size=args.vector_size,
            distance=DEFAULT_DISTANCE,
        )

    # --- Load source ---
    print(f"Loading {SOURCE_COLLECTION}...", flush=True)
    source_points = scroll_all(client, SOURCE_COLLECTION)
    total_source = len(source_points)
    print(f"  {total_source} doc points loaded")

    if args.limit:
        source_points = source_points[: args.limit]
        print(f"  Limited to first {args.limit} docs")

    # --- Build reasoning points ---
    docs_with_snippets = 0
    snippets_total = 0
    embed_errors = 0
    upserted = 0

    for doc_idx, doc in enumerate(source_points):
        snippets = doc.payload.get("reasoning_snippets", [])
        if not snippets:
            continue

        docs_with_snippets += 1

        # Parent metadata
        doc_id = doc.payload.get("point_id", str(doc.id))
        doc_sha256 = doc.payload.get("doc_sha256", "")
        title = doc.payload.get("title", "")
        doc_url = doc.payload.get("doc_url", "")
        cited_norms = doc.payload.get("cited_norms", [])
        source_run = doc.payload.get("source_run", "")

        ready_points: List[qm.PointStruct] = []
        seen_texts: set = set()  # dedup within this doc

        for idx, item in enumerate(snippets):
            cue = item.get("cue", "") if isinstance(item, dict) else ""
            text = item.get("snippet", "") if isinstance(item, dict) else str(item)
            if not text:
                continue
            if text in seen_texts:
                continue  # skip intra-doc duplicate snippet
            seen_texts.add(text)

            snippets_total += 1

            if args.dry_run:
                continue

            # Deterministic point ID: stable across rebuilds
            point_id = make_uuid(f"{doc_sha256}:reasoning:{idx}")

            try:
                vec = ollama_embed(text, ollama=args.ollama, model=args.embed_model)
            except Exception as e:
                print(f"\n  [embed_error] doc {doc_idx+1} snippet {idx}: {e}", flush=True)
                embed_errors += 1
                continue

            ready_points.append(
                qm.PointStruct(
                    id=point_id,
                    vector=vec,
                    payload={
                        "level": "reasoning",
                        "reasoning_text": text,
                        "cue_word": cue,
                        "doc_id": doc_id,
                        "doc_sha256": doc_sha256,
                        "title": title,
                        "doc_url": doc_url,
                        "cited_norms": cited_norms,
                        "source_run": source_run,
                    },
                )
            )

        if ready_points:
            upserted += upsert_batched(client, REASONING_COLLECTION, ready_points)

        # Progress every 10 docs
        done = doc_idx + 1
        if done % 10 == 0 or done == len(source_points):
            print(
                f"  [{done}/{len(source_points)}] docs | snippets so far: {snippets_total}",
                flush=True,
            )

    # --- Summary ---
    print()
    if args.dry_run:
        print("DRY RUN — no writes performed")
        print(f"  source_docs={total_source} docs_with_snippets={docs_with_snippets} snippets_total={snippets_total}")
    else:
        status = "OK" if embed_errors == 0 else "PARTIAL"
        print(
            f"{status}  docs_with_snippets={docs_with_snippets}"
            f" snippets_total={snippets_total}"
            f" upserted={upserted}"
            f" embed_errors={embed_errors}"
        )
        print(f"collection={REASONING_COLLECTION}")


if __name__ == "__main__":
    main()
