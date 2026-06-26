#!/usr/bin/env python3
"""Suggest node relationships to help the main agent merge with less fragmentation."""

from __future__ import annotations

import argparse
import json
import pathlib
from itertools import combinations

from clawexpert_common import (
    best_label,
    char_bigrams,
    extract_bullets,
    extract_section,
    first_sentence,
    frontmatter_aliases,
    jaccard,
    knowledge_dir,
    list_formal_nodes,
    list_subtopic_nodes,
    parse_frontmatter_and_body,
    read_text,
    semantic_signature,
    split_inline_list,
    topic_dir,
)


def load_nodes(root: pathlib.Path, formal_only: bool) -> list[dict]:
    paths = list_formal_nodes(root) if formal_only else list_subtopic_nodes(root)
    nodes: list[dict] = []
    for path in paths:
        frontmatter, body = parse_frontmatter_and_body(read_text(path))
        label = best_label(frontmatter, body, path.stem)
        summary = first_sentence(extract_section(body, "Summary"))
        conclusions = extract_bullets(extract_section(body, "Key Conclusions"))[:4]
        aliases = frontmatter_aliases(frontmatter)
        include_terms = split_inline_list(frontmatter.get("inclusion"))
        texts = [label, summary, *aliases, *conclusions, *include_terms]
        signature = semantic_signature(texts)
        nodes.append(
            {
                "path": str(path),
                "label": label,
                "summary": summary,
                "aliases": aliases,
                "parent": frontmatter.get("parent") or "root",
                "type": frontmatter.get("type") or "topic",
                "signature": signature,
            }
        )
    return nodes


def classify_pair(left: dict, right: dict) -> dict | None:
    left_sig = left["signature"]
    right_sig = right["signature"]

    exact_text = bool(left_sig["compact"] & right_sig["compact"])
    exact_alias = bool(left_sig["stripped"] & right_sig["stripped"])
    exact_abbreviation = bool(left_sig["abbreviations"] & right_sig["abbreviations"])
    token_overlap = jaccard(left_sig["tokens"], right_sig["tokens"])
    bigram_overlap = jaccard(left_sig["bigrams"], right_sig["bigrams"])
    similarity = max(token_overlap, bigram_overlap)

    left_compact = next(iter(left_sig["compact"]), "")
    right_compact = next(iter(right_sig["compact"]), "")
    containment = (
        bool(left_compact and right_compact and left_compact in right_compact and left_compact != right_compact),
        bool(left_compact and right_compact and right_compact in left_compact and left_compact != right_compact),
    )

    reasons: list[str] = []
    relation = None
    confidence = 0.0

    if exact_text:
        relation = "merge_candidate"
        confidence = 0.98
        reasons.append("exact_compact_match")
    elif exact_alias or exact_abbreviation:
        relation = "merge_candidate"
        confidence = 0.9
        reasons.append("normalized_or_abbreviation_match")
    elif similarity >= 0.62:
        relation = "merge_candidate"
        confidence = similarity
        reasons.append("high_lexical_overlap")
    elif containment[0] or containment[1]:
        relation = "parent_child_candidate"
        confidence = 0.72
        reasons.append("name_containment")
    elif similarity >= 0.28:
        relation = "related_candidate"
        confidence = similarity
        reasons.append("partial_overlap")

    if not relation:
        return None

    parent_hint = None
    child_hint = None
    if relation == "parent_child_candidate":
        if containment[0]:
            parent_hint, child_hint = left["label"], right["label"]
        elif containment[1]:
            parent_hint, child_hint = right["label"], left["label"]

    return {
        "left": {
            "label": left["label"],
            "path": left["path"],
            "aliases": left["aliases"],
            "parent": left["parent"],
        },
        "right": {
            "label": right["label"],
            "path": right["path"],
            "aliases": right["aliases"],
            "parent": right["parent"],
        },
        "relation": relation,
        "confidence": round(confidence, 3),
        "token_overlap": round(token_overlap, 3),
        "bigram_overlap": round(bigram_overlap, 3),
        "reasons": reasons,
        "parent_hint": parent_hint,
        "child_hint": child_hint,
        "agent_decision_required": True,
    }


def canonical_aliases(*nodes: dict) -> list[str]:
    values: list[str] = []
    for node in nodes:
        values.append(node["label"])
        values.extend(node["aliases"])
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(value.strip())
    return deduped


def build_merge_groups(pairs: list[dict]) -> list[dict]:
    groups: list[dict] = []
    used_paths: set[str] = set()
    for pair in sorted(pairs, key=lambda item: item["confidence"], reverse=True):
        left_path = pair["left"]["path"]
        right_path = pair["right"]["path"]
        if left_path in used_paths or right_path in used_paths:
            continue
        used_paths.update({left_path, right_path})
        aliases = canonical_aliases(pair["left"], pair["right"])
        groups.append(
            {
                "recommended_label": min(aliases, key=len),
                "aliases": aliases,
                "paths": [left_path, right_path],
                "reasons": pair["reasons"],
                "confidence": pair["confidence"],
                "agent_decision_required": True,
            }
        )
    return groups


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--formal-only", action="store_true")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    root = topic_dir(kb, args.slug)
    nodes = load_nodes(root, formal_only=args.formal_only)

    relations: list[dict] = []
    for left, right in combinations(nodes, 2):
        relation = classify_pair(left, right)
        if relation:
            relations.append(relation)

    merge_candidates = [item for item in relations if item["relation"] == "merge_candidate"]
    parent_child_candidates = [item for item in relations if item["relation"] == "parent_child_candidate"]
    related_candidates = [item for item in relations if item["relation"] == "related_candidate"]

    payload = {
        "slug": args.slug,
        "node_count": len(nodes),
        "merge_groups": build_merge_groups(merge_candidates),
        "merge_candidates": sorted(merge_candidates, key=lambda item: item["confidence"], reverse=True),
        "parent_child_candidates": sorted(parent_child_candidates, key=lambda item: item["confidence"], reverse=True),
        "related_candidates": sorted(related_candidates, key=lambda item: item["confidence"], reverse=True),
        "note": "This script only retrieves likely relationships. The main agent must make the final semantic decision.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
