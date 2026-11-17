#!/usr/bin/env python3
"""Query the index with weighted lexical ranking. English is normative; ZH-CN is paired. / 使用加权 lexical ranking 查询索引；英文为规范文本，简体中文为配对译文。"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
import sys
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from asset_index_registry import DEFAULT_REGISTRY_PATH, valid_asset_indexes
import embedding_rerank
import runtime_paths


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_./+-]*|\d+(?:[._-]\d+)*|[\u4e00-\u9fff]+")
TOKEN_VARIANTS = {
    "planner": {"plan", "planning"},
    "planning": {"plan", "planner"},
    "ranker": {"rank", "ranking"},
    "ranking": {"rank", "ranker"},
    "recommender": {"recommend", "recommendation"},
    "recommendation": {"recommend", "recommender"},
}
CODE_INTENT_TOKENS = {
    "code", "repo", "repository", "project", "service", "module", "branch", "build", "compile", "deploy",
    "debug", "api", "sdk", "cli", "workflow", "代码", "项目", "仓库", "服务", "模块", "分支", "构建",  # bilingual-compat: Chinese code and project intent terms.
    "编译", "部署", "调试", "工程", "脚本",  # bilingual-compat: Chinese build, deploy, debug, engineering, and script terms.
}
PROBE_FIELDS = ("title", "aliases", "search_terms", "use_when", "insights", "summary", "key_points")
PROBE_STOPWORDS = {"the", "a", "an", "of", "and", "for", "to", "in", "with", "service", "project", "code"}
FIELD_WEIGHTS = {
    "title": 7.0,
    "path": 3.5,
    "tags": 4.0,
    "aliases": 7.0,
    "search_terms": 6.0,
    "use_when": 5.0,
    "doc_type": 1.0,
    "headings": 2.0,
    "insights": 6.0,
    "key_points": 4.0,
    "summary": 4.0,
    "display_snippet": 0.25,
    "excerpt": 0.0,
}


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in TOKEN_RE.findall(text):
        lowered = raw.lower()
        tokens.append(lowered)
        if re.fullmatch(r"[\u4e00-\u9fff]+", raw):
            bounded = raw[:160]
            for width in range(2, min(4, len(bounded)) + 1):
                tokens.extend(bounded[index:index + width] for index in range(len(bounded) - width + 1))
        elif re.search(r"[A-Za-z]", raw):
            split = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", raw)
            for part in re.split(r"[_./+-]+|\s+", split):
                part = part.lower().strip()
                if not part:
                    continue
                tokens.append(part)
                tokens.extend(sorted(TOKEN_VARIANTS.get(part, set())))
        elif re.fullmatch(r"\d+(?:[._-]\d+)*", raw):
            tokens.extend(part for part in re.split(r"[._-]+", raw) if part)
    return tokens


def phrase_tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in TOKEN_RE.findall(text):
        if re.fullmatch(r"[\u4e00-\u9fff]+", raw):
            tokens.append(raw)
            continue
        split = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", raw)
        for part in re.split(r"[_./+-]+|\s+", split):
            normalized = part.lower().strip()
            if not normalized:
                continue
            if normalized in {"planner", "planning"}:
                normalized = "plan"
            elif normalized in {"ranker", "ranking"}:
                normalized = "rank"
            elif normalized in {"recommender", "recommendation"}:
                normalized = "recommend"
            tokens.append(normalized)
    return tokens


def normalized_phrase(text: str) -> str:
    return " ".join(phrase_tokenize(text))


def load_documents(index_path: Path) -> list[dict[str, Any]]:
    if not index_path.exists():
        raise FileNotFoundError(f"Index not found / 未找到索引: {index_path}")
    documents = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            documents.append(json.loads(line))
    return documents


def field_text(document: dict[str, Any], field: str) -> str:
    value = document.get(field, "")
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def score_field(
    text: str,
    query_tokens: list[str],
    document_frequency: Counter[str],
    corpus_size: int,
) -> float:
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    normalizer = math.sqrt(max(1, len(set(tokens))))
    score = 0.0
    haystack = set(tokens)
    for token in query_tokens:
        inverse_frequency = math.log((corpus_size + 1) / (document_frequency.get(token, 0) + 1)) + 1.0
        score += inverse_frequency * min(counts[token], 2) / normalizer
        if token in haystack:
            score += 0.1 * inverse_frequency
    return score


def boost_document(document: dict[str, Any]) -> float:
    path = document.get("path", "")
    boost = 0.0
    if document.get("record_type") == "collection":
        boost += 1.2
    if path.startswith("010 outbox/1. 原创"):  # bilingual-compat: authored-originals path prefix.
        boost += 0.8
    elif path.startswith("030 PKV"):
        boost += 0.5
    if "Untitled" in document.get("title", ""):
        boost -= 1.0
    return boost


def score_document(
    document: dict[str, Any],
    query_tokens: list[str],
    raw_query: str,
    document_frequency: Counter[str],
    corpus_size: int,
) -> float:
    score = boost_document(document)
    for field, weight in FIELD_WEIGHTS.items():
        score += weight * score_field(field_text(document, field), query_tokens, document_frequency, corpus_size)
    if raw_query.lower() in document.get("search_text", "").lower():
        score += 2.0
    query_windows = []
    unique_tokens = list(dict.fromkeys(token for token in phrase_tokenize(raw_query) if len(token) > 1))
    for width in (3, 2):
        query_windows.extend(
            " ".join(unique_tokens[index:index + width])
            for index in range(max(0, len(unique_tokens) - width + 1))
        )
    for field in ("title", "aliases", "search_terms", "use_when"):
        normalized = normalized_phrase(field_text(document, field))
        for window in query_windows:
            if window and window in normalized:
                score += 2.5 if field in {"title", "aliases"} else 1.5
                break
    return round(score, 4)


def search_documents(
    documents: list[dict[str, Any]],
    query: str,
    *,
    top_k: int = 10,
    tag: str | None = None,
    top_dir: str | None = None,
) -> list[dict[str, Any]]:
    query_tokens = list(dict.fromkeys(tokenize(query)))
    document_frequency: Counter[str] = Counter()
    for document in documents:
        field_tokens: set[str] = set()
        for field, weight in FIELD_WEIGHTS.items():
            if weight:
                field_tokens.update(tokenize(field_text(document, field)))
        document_frequency.update(field_tokens)
    results = []
    per_collection: Counter[str] = Counter()
    for document in documents:
        if tag and tag not in document.get("tags", []):
            continue
        if top_dir and top_dir != document.get("top_dir"):
            continue
        score = score_document(document, query_tokens, query, document_frequency, len(documents))
        if score <= 0:
            continue
        group_key = document.get("path", "")
        if document.get("record_type") == "document" and document.get("source_paths"):
            group_key = document.get("path", "").rsplit("/", 1)[0]
        results.append(
            {
                "record_id": document.get("record_id", document.get("path", "")),
                "record_type": document.get("record_type", "document"),
                "path": document["path"],
                "source_paths": document.get("source_paths", [document["path"]]),
                "title": document.get("title", ""),
                "doc_type": document.get("doc_type", ""),
                "score": score,
                "tags": document.get("tags", []),
                "aliases": document.get("aliases", []),
                "summary": document.get("summary", ""),
                "insights": document.get("insights", []),
                "key_points": document.get("key_points", []),
                "search_terms": document.get("search_terms", []),
                "use_when": document.get("use_when", []),
                "excerpt": document.get("display_snippet", document.get("excerpt", "")),
                "_group_key": group_key,
            }
        )
    ordered = sorted(results, key=lambda item: (-item["score"], item["path"]))
    diversified = []
    for item in ordered:
        limit = 2 if item["record_type"] == "collection" else 3
        if per_collection[item["_group_key"]] >= limit:
            continue
        per_collection[item["_group_key"]] += 1
        item.pop("_group_key", None)
        diversified.append(item)
        if len(diversified) >= top_k:
            break
    return diversified


def search(
    index_path: Path,
    query: str,
    *,
    top_k: int = 10,
    tag: str | None = None,
    top_dir: str | None = None,
) -> list[dict[str, Any]]:
    return search_documents(load_documents(index_path), query, top_k=top_k, tag=tag, top_dir=top_dir)


def apply_semantic_rerank(
    query: str,
    results: list[dict[str, Any]],
    documents: dict[str, dict[str, Any]],
    semantic_rerank: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    status: dict[str, Any] = {"requested": semantic_rerank, "status": "not_requested"}
    if semantic_rerank == "never":
        status["status"] = "disabled"
        return results, status
    if not results:
        status["status"] = "no_candidates"
        return results, status
    provider = embedding_rerank.provider_status()
    status["provider"] = provider.get("provider", "")
    if not provider.get("available"):
        status["status"] = "unavailable"
        status["reason"] = provider.get("reason", "no_configured_provider")
        return results, status
    candidates: list[dict[str, Any]] = []
    for item in results:
        enriched = dict(item)
        enriched["_rerank_id"] = str(item.get("record_id", item.get("path", "")))
        candidates.append(enriched)
    try:
        reranked = embedding_rerank.rerank_results(query, candidates, documents)
    except Exception as exc:
        status["status"] = "failed"
        status["reason"] = type(exc).__name__
        return results, status
    status["status"] = "applied"
    return [{key: value for key, value in item.items() if key != "_rerank_id"} for item in reranked], status


def search_with_semantic_rerank(
    index_path: Path,
    query: str,
    *,
    top_k: int = 10,
    tag: str | None = None,
    top_dir: str | None = None,
    semantic_rerank: str = "auto",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    documents = load_documents(index_path)
    results = search_documents(documents, query, top_k=top_k * 3, tag=tag, top_dir=top_dir)
    by_id = {str(document.get("record_id", document.get("path", ""))): document for document in documents}
    reranked, status = apply_semantic_rerank(query, results, by_id, semantic_rerank)
    return reranked[:top_k], status


def code_intent(query: str) -> bool:
    return bool(set(tokenize(query)) & CODE_INTENT_TOKENS)


def workspace_matches(entry: dict[str, Any], filters: list[str]) -> bool:
    if not filters:
        return True
    values = {
        str(entry.get("workspace_id", "")).lower(),
        str(entry.get("workspace_label", "")).lower(),
        str(entry.get("workspace_root", "")).lower(),
        Path(str(entry.get("workspace_root", ""))).name.lower(),
    }
    for raw in filters:
        value = raw.lower().strip()
        if value and any(value == candidate or value in candidate for candidate in values if candidate):
            return True
    return False


def strong_asset_match(query: str, entries: list[dict[str, Any]]) -> bool:
    normalized_query = normalized_phrase(query)
    raw_query = query.lower().strip()
    if not normalized_query:
        return False
    for entry in entries:
        try:
            documents = load_documents(Path(str(entry["index_path"])))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            continue
        for document in documents:
            for value in [document.get("title", ""), *document.get("aliases", []), *document.get("source_paths", [])]:
                text = str(value)
                if raw_query and raw_query in text.lower():
                    return True
                candidate = normalized_phrase(text)
                if candidate and (candidate in normalized_query or normalized_query in candidate):
                    return True
    return False


def probe_tokens(query: str) -> set[str]:
    return {
        token
        for token in tokenize(query)
        if len(token) > 1 and token not in PROBE_STOPWORDS and not token.isdigit()
    }


def asset_probe(query: str, entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    query_terms = probe_tokens(query)
    if not query_terms:
        return {}
    probes: dict[str, dict[str, Any]] = {}
    for entry in entries:
        try:
            documents = load_documents(Path(str(entry["index_path"])))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            continue
        ranked = search_documents(documents, query, top_k=1)
        if not ranked:
            continue
        candidate = ranked[0]
        source = next(
            (document for document in documents if str(document.get("record_id", document.get("path", ""))) == str(candidate.get("record_id", ""))),
            {},
        )
        document_terms: set[str] = set()
        for field in PROBE_FIELDS:
            document_terms.update(tokenize(field_text(source, field)))
        matches = query_terms & document_terms
        coverage = len(matches) / len(query_terms)
        minimum_matches = 2 if len(query_terms) >= 3 else 1
        minimum_coverage = 0.5
        if len(matches) >= minimum_matches and coverage >= minimum_coverage:
            probes[str(entry.get("workspace_id", ""))] = {
                "entry": entry,
                "top_title": candidate.get("title", ""),
                "score": candidate.get("score", 0),
                "coverage": round(coverage, 4),
                "matched_terms": sorted(matches)[:12],
            }
    return probes


def annotate_result(result: dict[str, Any], origin: str, entry: dict[str, Any] | None = None) -> dict[str, Any]:
    output = dict(result)
    output["origin"] = origin
    if entry is not None:
        output["workspace_id"] = entry.get("workspace_id", "")
        output["workspace_label"] = entry.get("workspace_label", "")
        output["workspace_root"] = entry.get("workspace_root", "")
    return output


def workspace_quality_requests_embedding(entry: dict[str, Any]) -> bool:
    report = Path(str(entry.get("workspace_root", ""))) / ".cleanup-extracted" / "retrieval-quality-strict-top1.json"
    try:
        payload = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    summary = payload.get("summary", {}) if isinstance(payload, dict) else {}
    return bool(summary.get("embedding_recommended", False)) if isinstance(summary, dict) else False


def federated_search(
    primary_index: Path,
    query: str,
    *,
    top_k: int = 10,
    tag: str | None = None,
    top_dir: str | None = None,
    asset_indexes: str = "auto",
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    workspace_filters: list[str] | None = None,
    semantic_rerank: str = "auto",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    workspace_filters = workspace_filters or []
    primary_documents = load_documents(primary_index)
    primary = [annotate_result(item, "primary") for item in search_documents(primary_documents, query, top_k=top_k * 3, tag=tag, top_dir=top_dir)]
    documents_by_key: dict[str, dict[str, Any]] = {
        "primary::" + str(document.get("record_id", document.get("path", ""))): document
        for document in primary_documents
    }
    valid_entries, skipped_entries = valid_asset_indexes(registry_path)
    valid_entries = [entry for entry in valid_entries if workspace_matches(entry, workspace_filters)]
    probes = asset_probe(query, valid_entries)
    reason = "disabled"
    include_assets = False
    selected_candidates = valid_entries
    if asset_indexes == "always":
        include_assets = True
        reason = "forced"
    elif asset_indexes == "auto":
        if workspace_filters:
            include_assets = True
            reason = "workspace_filter"
        elif code_intent(query):
            include_assets = True
            reason = "code_intent"
            if probes:
                selected_candidates = [value["entry"] for value in probes.values()]
        elif strong_asset_match(query, valid_entries):
            include_assets = True
            reason = "strong_project_match"
        elif probes:
            include_assets = True
            reason = "asset_probe"
            selected_candidates = [value["entry"] for value in probes.values()]
        else:
            reason = "no_project_intent"
    asset_results: list[dict[str, Any]] = []
    selected_entries: list[dict[str, Any]] = []
    if include_assets:
        for entry in selected_candidates:
            index_path = Path(str(entry["index_path"]))
            documents = load_documents(index_path)
            records = search_documents(documents, query, top_k=top_k * 3, tag=tag, top_dir=top_dir)
            if not records:
                continue
            selected_entries.append(entry)
            strong = strong_asset_match(query, [entry])
            workspace_id = str(entry.get("workspace_id", ""))
            documents_by_key.update(
                {
                    workspace_id + "::" + str(document.get("record_id", document.get("path", ""))): document
                    for document in documents
                }
            )
            for item in records:
                annotated = annotate_result(item, "asset", entry)
                annotated["score"] = round(float(annotated["score"]) + (4.0 if strong else 0.75), 4)
                asset_results.append(annotated)
    merged = primary + asset_results
    deduplicated: dict[tuple[str, str], dict[str, Any]] = {}
    for item in merged:
        key = (str(item.get("workspace_id", item.get("origin", "primary"))), str(item.get("record_id", item.get("path", ""))))
        current = deduplicated.get(key)
        if current is None or float(item["score"]) > float(current["score"]):
            deduplicated[key] = item
    ordered = sorted(
        deduplicated.values(),
        key=lambda item: (-float(item["score"]), 0 if item.get("origin") == "primary" else 1, str(item.get("path", ""))),
    )
    diversified: list[dict[str, Any]] = []
    groups: Counter[str] = Counter()
    for item in ordered:
        workspace = str(item.get("workspace_id", item.get("origin", "primary")))
        group_key = workspace + ":" + str(item.get("path", "")).rsplit("/", 1)[0]
        if groups[group_key] >= 3:
            continue
        groups[group_key] += 1
        diversified.append(item)
        if len(diversified) >= top_k:
            break
    rerank_status: dict[str, Any] = {"requested": semantic_rerank, "status": "not_requested"}
    rerank_eligible = semantic_rerank == "always" or (
        semantic_rerank == "auto" and any(workspace_quality_requests_embedding(entry) for entry in selected_entries)
    )
    if semantic_rerank == "never":
        rerank_status["status"] = "disabled"
    elif not rerank_eligible:
        rerank_status["status"] = "not_needed"
    elif not diversified:
        rerank_status["status"] = "no_candidates"
    else:
        provider = embedding_rerank.provider_status()
        rerank_status["provider"] = provider.get("provider", "")
        if not provider.get("available"):
            rerank_status["status"] = "unavailable"
            rerank_status["reason"] = provider.get("reason", "no_configured_provider")
        else:
            candidates: list[dict[str, Any]] = []
            candidate_documents: dict[str, dict[str, Any]] = {}
            for item in diversified:
                enriched = dict(item)
                rerank_id = str(item.get("workspace_id", "primary")) + "::" + str(item.get("record_id", item.get("path", "")))
                enriched["_rerank_id"] = rerank_id
                candidates.append(enriched)
                if rerank_id in documents_by_key:
                    candidate_documents[rerank_id] = documents_by_key[rerank_id]
            try:
                reranked = embedding_rerank.rerank_results(query, candidates, candidate_documents)
                diversified = [
                    {key: value for key, value in item.items() if key != "_rerank_id"}
                    for item in reranked[:top_k]
                ]
                rerank_status["status"] = "applied"
            except Exception as exc:
                rerank_status["status"] = "failed"
                rerank_status["reason"] = type(exc).__name__
    routing = {
        "primary_index": str(primary_index),
        "asset_mode": asset_indexes,
        "asset_reason": reason,
        "asset_indexes": [
            {"workspace_id": entry.get("workspace_id", ""), "workspace_label": entry.get("workspace_label", ""), "index_path": entry.get("index_path", "")}
            for entry in selected_entries
        ],
        "asset_probes": [
            {
                "workspace_id": workspace_id,
                "workspace_label": value["entry"].get("workspace_label", ""),
                "top_title": value["top_title"],
                "coverage": value["coverage"],
                "matched_terms": value["matched_terms"],
            }
            for workspace_id, value in sorted(probes.items())
        ],
        "skipped_asset_indexes": skipped_entries,
        "semantic_rerank": rerank_status,
    }
    return diversified, routing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="Search query. / 搜索查询。")
    parser.add_argument("--top-k", type=int, default=10, help="Maximum result count. / 最大结果数。")
    parser.add_argument("--tag", help="Filter by tag. / 按标签过滤。")
    parser.add_argument("--top-dir", help="Filter by top-level directory. / 按顶层目录过滤。")
    parser.add_argument("--asset-indexes", choices=["auto", "always", "never"], default="auto", help="Federated asset-index policy. / 联邦 asset index 策略。")
    parser.add_argument("--asset-registry", type=Path, default=DEFAULT_REGISTRY_PATH, help="Asset-index registry path. / Asset index 注册表路径。")
    parser.add_argument("--workspace", action="append", help="Restrict federated asset search to a registered workspace. / 将联邦 asset 搜索限制到已注册 workspace。")
    parser.add_argument("--semantic-rerank", choices=["auto", "always", "never"], default="auto", help="Semantic rerank policy. / Semantic rerank 策略。")
    parser.add_argument("--explain-routing", action="store_true", help="Include federated routing diagnostics. / 包含联邦 routing 诊断。")
    parser.add_argument("--json", action="store_true", help="Print JSON results. / 打印 JSON 结果。")
    parser.add_argument(
        "--index",
        type=Path,
        default=runtime_paths.DEFAULT_PATHS.index_dir / "documents.jsonl",
        help="Primary documents.jsonl path. / 主 documents.jsonl 路径。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results, routing = federated_search(
        args.index,
        args.query,
        top_k=args.top_k,
        tag=args.tag,
        top_dir=args.top_dir,
        asset_indexes=args.asset_indexes,
        registry_path=args.asset_registry,
        workspace_filters=args.workspace,
        semantic_rerank=args.semantic_rerank,
    )
    if args.json:
        payload: Any = {"routing": routing, "results": results} if args.explain_routing else results
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.explain_routing:
        print(json.dumps(routing, ensure_ascii=False))
    for item in results:
        tags = ", ".join(item["tags"])
        kind = item["record_type"]
        print(f"{item['score']:>7.4f}  {kind:<10} {item['path']}  [{tags}]")
        if item["summary"]:
            print(f"         {item['summary'][:220]}")
        if item["record_type"] == "collection":
            print(f"         sources / 来源: {len(item['source_paths'])}")


if __name__ == "__main__":
    main()
