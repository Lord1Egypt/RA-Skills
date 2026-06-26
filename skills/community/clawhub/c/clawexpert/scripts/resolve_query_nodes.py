#!/usr/bin/env python3
"""Retrieve the most likely topic/node candidates for a user query."""

from __future__ import annotations

import argparse
import json
import pathlib

from clawexpert_common import (
    best_label,
    extract_bullets,
    extract_section,
    first_sentence,
    frontmatter_aliases,
    jaccard,
    knowledge_dir,
    list_all_knowledge_nodes,
    load_json,
    meta_path,
    parse_frontmatter_and_body,
    read_text,
    semantic_signature,
)


def topic_dirs(kb: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        child
        for child in kb.iterdir()
        if child.is_dir() and not child.name.startswith("_") and (child / "meta.json").exists()
    )


def score_signature(query_sig: dict, candidate_sig: dict) -> tuple[float, list[str]]:
    reasons: list[str] = []
    score = 0.0

    if query_sig["compact"] & candidate_sig["compact"]:
        score += 1.0
        reasons.append("exact_compact")
    if query_sig["stripped"] & candidate_sig["stripped"]:
        score += 0.85
        reasons.append("normalized_match")
    if query_sig["abbreviations"] & candidate_sig["abbreviations"]:
        score += 0.75
        reasons.append("abbreviation_match")

    query_compact = next(iter(query_sig["compact"]), "")
    candidate_compact = next(iter(candidate_sig["compact"]), "")
    if query_compact and candidate_compact:
        if query_compact in candidate_compact or candidate_compact in query_compact:
            score += 0.45
            reasons.append("compact_containment")

    token_overlap = jaccard(query_sig["tokens"], candidate_sig["tokens"])
    bigram_overlap = jaccard(query_sig["bigrams"], candidate_sig["bigrams"])
    if token_overlap > 0:
        score += token_overlap * 0.9
        reasons.append(f"token_overlap:{token_overlap:.2f}")
    if bigram_overlap > 0:
        score += bigram_overlap * 0.6
        reasons.append(f"bigram_overlap:{bigram_overlap:.2f}")

    return score, reasons


def infer_relation(query_sig: dict, candidate_sig: dict, reasons: list[str]) -> str:
    if "exact_compact" in reasons:
        return "exact"
    if "normalized_match" in reasons or "abbreviation_match" in reasons:
        return "alias_like"

    query_tokens = query_sig["tokens"]
    candidate_tokens = candidate_sig["tokens"]
    if query_tokens and candidate_tokens:
        if query_tokens < candidate_tokens:
            return "candidate_is_narrower"
        if candidate_tokens < query_tokens:
            return "candidate_is_broader"
    return "related"


def collect_topic_candidates(kb: pathlib.Path, query_sig: dict) -> list[dict]:
    candidates: list[dict] = []
    for root in topic_dirs(kb):
        meta = load_json(meta_path(kb, root.name), default={}) or {}
        index_categories = meta.get("index_categories", {}) or {}
        texts = [
            meta.get("topic", root.name),
            meta.get("slug", root.name),
            index_categories.get("l1_label", ""),
            index_categories.get("l1", ""),
            *[
                str(item.get("l2", ""))
                for item in (index_categories.get("subtopics", {}) or {}).values()
                if item.get("l2")
            ],
        ]
        topic_index = root / "index.md"
        if topic_index.exists():
            index_text = read_text(topic_index)
            texts.append(first_sentence(extract_section(index_text, "Core Findings Summary")))
        signature = semantic_signature(texts)
        score, reasons = score_signature(query_sig, signature)
        if score <= 0:
            continue
        candidates.append(
            {
                "kind": "topic",
                "slug": meta.get("slug", root.name),
                "topic": meta.get("topic", root.name),
                "score": round(score, 3),
                "relation": infer_relation(query_sig, signature, reasons),
                "reasons": reasons,
                "l1": index_categories.get("l1"),
                "l1_label": index_categories.get("l1_label"),
                "summary": texts[-1] if texts else "",
            }
        )
    return sorted(candidates, key=lambda item: (-item["score"], item["slug"]))


def collect_node_candidates(kb: pathlib.Path, query_sig: dict) -> list[dict]:
    candidates: list[dict] = []
    for root in topic_dirs(kb):
        meta = load_json(meta_path(kb, root.name), default={}) or {}
        for node_path in list_all_knowledge_nodes(root):
            frontmatter, body = parse_frontmatter_and_body(read_text(node_path))
            label = best_label(frontmatter, body, node_path.stem)
            aliases = frontmatter_aliases(frontmatter)
            summary = first_sentence(extract_section(body, "Summary"))
            conclusions = extract_bullets(extract_section(body, "Key Conclusions"))[:3]
            signature = semantic_signature([label, summary, *aliases, *conclusions])
            score, reasons = score_signature(query_sig, signature)
            if score <= 0:
                continue
            candidates.append(
                {
                    "kind": "node",
                    "slug": meta.get("slug", root.name),
                    "topic": meta.get("topic", root.name),
                    "node_id": frontmatter.get("id") or node_path.stem,
                    "label": label,
                    "aliases": aliases,
                    "path": str(node_path),
                    "parent": frontmatter.get("parent") or "root",
                    "score": round(score, 3),
                    "relation": infer_relation(query_sig, signature, reasons),
                    "reasons": reasons,
                    "summary": summary,
                }
            )
    return sorted(candidates, key=lambda item: (-item["score"], item["path"]))


def recommended_action(top_topic: dict | None, top_node: dict | None) -> str:
    if top_node and top_node["score"] >= 1.0:
        return "open_node"
    if top_node and top_node["score"] >= 0.28:
        return "inspect_node_then_neighbors"
    if top_topic and top_topic["score"] >= 0.15:
        return "open_topic_branch"
    return "ask_agent_to_create_or_expand"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    query_sig = semantic_signature([args.query])
    topics = collect_topic_candidates(kb, query_sig)[: args.top_k]
    nodes = collect_node_candidates(kb, query_sig)[: args.top_k]
    payload = {
        "query": args.query,
        "recommended_action": recommended_action(topics[0] if topics else None, nodes[0] if nodes else None),
        "top_topics": topics,
        "top_nodes": nodes,
        "agent_decision_required": True,
        "note": "This script only recalls likely candidates. The main agent must decide whether the query maps to an existing node, a broader branch, or a new node.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
