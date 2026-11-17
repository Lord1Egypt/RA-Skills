#!/usr/bin/env python3
"""Rerank bounded lexical candidates with embeddings. / 使用 embedding 重排有界 lexical 候选。"""

from __future__ import annotations

import json
import math
import os
from typing import Any, Callable
from urllib.parse import urlparse
from urllib import request


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
Embedder = Callable[[list[str]], list[list[float]]]


def provider_status(environ: dict[str, str] | None = None) -> dict[str, Any]:
    values = os.environ if environ is None else environ
    if values.get("SECOND_BRAIN_EMBEDDING_ENABLED", "").strip().lower() not in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return {"available": False, "provider": "", "reason": "explicit_opt_in_required"}
    requested = values.get("SECOND_BRAIN_EMBEDDING_PROVIDER", "").lower().strip()
    if requested not in {"azure", "openai"}:
        return {"available": False, "provider": requested, "reason": "unsupported_provider"}
    if not values.get("SECOND_BRAIN_EMBEDDING_API_KEY", "").strip():
        return {"available": False, "provider": requested, "reason": "missing_embedding_api_key"}
    base_url = values.get("SECOND_BRAIN_EMBEDDING_BASE_URL", "").strip()
    if not base_url:
        return {"available": False, "provider": requested, "reason": "missing_base_url"}
    parsed = urlparse(base_url)
    if parsed.scheme.lower() != "https" or not parsed.netloc:
        return {"available": False, "provider": requested, "reason": "https_required"}
    return {
        "available": True,
        "provider": requested,
        "model": values.get("SECOND_BRAIN_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        "base_url": base_url,
    }


def embedding_config() -> tuple[dict[str, Any], str]:
    status = provider_status()
    if not status["available"]:
        raise RuntimeError(str(status["reason"]))
    key = os.environ.get("SECOND_BRAIN_EMBEDDING_API_KEY", "").strip()
    if not key:
        raise RuntimeError("no_configured_provider")
    return status, key


def embed_texts(texts: list[str]) -> list[list[float]]:
    status, key = embedding_config()
    url = str(status["base_url"]).rstrip("/") + "/embeddings"
    payload = json.dumps({"model": status["model"], "input": texts}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    with request.urlopen(req, timeout=30) as response:  # nosec B310: endpoint is explicit configured provider.
        body = json.loads(response.read().decode("utf-8"))
    data = body.get("data", []) if isinstance(body, dict) else []
    vectors = [item.get("embedding") for item in data if isinstance(item, dict)]
    if len(vectors) != len(texts) or any(not isinstance(vector, list) for vector in vectors):
        raise RuntimeError("embedding provider returned an invalid response / embedding provider 返回了无效响应")
    return [[float(value) for value in vector] for vector in vectors]


def cosine(left: list[float], right: list[float]) -> float:
    if not left or len(left) != len(right):
        return 0.0
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


def rerank_results(
    query: str,
    results: list[dict[str, Any]],
    documents: dict[str, dict[str, Any]],
    *,
    embedder: Embedder = embed_texts,
    top_n: int = 20,
) -> list[dict[str, Any]]:
    candidates = results[:top_n]
    if not candidates:
        return []
    texts = [query]
    for item in candidates:
        document = documents.get(str(item.get("_rerank_id", item.get("record_id", ""))), {})
        texts.append(str(document.get("search_text") or document.get("summary") or item.get("summary", "")))
    vectors = embedder(texts)
    if len(vectors) != len(texts):
        raise RuntimeError("embedding provider returned a mismatched vector count / embedding provider 返回的 vector 数量不匹配")
    lexical_scores = [float(item.get("score", 0)) for item in candidates]
    low, high = min(lexical_scores), max(lexical_scores)
    enriched: list[dict[str, Any]] = []
    for index, item in enumerate(candidates):
        semantic_score = cosine(vectors[0], vectors[index + 1])
        lexical_score = 1.0 if high == low else (lexical_scores[index] - low) / (high - low)
        output = dict(item)
        output["semantic_score"] = round(semantic_score, 6)
        output["rerank_score"] = round(semantic_score + 0.15 * lexical_score, 6)
        enriched.append(output)
    reranked = sorted(enriched, key=lambda item: (-float(item["rerank_score"]), -float(item["score"]), str(item.get("path", ""))))
    return reranked + results[top_n:]
