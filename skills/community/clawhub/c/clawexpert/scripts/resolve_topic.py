#!/usr/bin/env python3
"""Resolve a user-provided topic or slug against the local knowledge base."""

from __future__ import annotations

import argparse
import json

from clawexpert_common import knowledge_dir, load_json, slugify


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    query = args.query.strip()
    query_slug = slugify(query)

    matches: list[dict] = []
    for child in sorted(kb.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        meta = load_json(child / "meta.json", default=None)
        if not meta:
            continue
        slug = meta.get("slug", child.name)
        topic = meta.get("topic", slug)
        score = 0
        reasons: list[str] = []
        if query == slug:
            score += 100
            reasons.append("exact_slug")
        if query_slug == slug:
            score += 90
            reasons.append("slugified_query")
        if query == topic:
            score += 80
            reasons.append("exact_topic")
        if query.lower() == str(topic).lower():
            score += 70
            reasons.append("casefold_topic")
        if query in str(topic) or str(topic) in query:
            score += 40
            reasons.append("substring_topic")
        if query_slug in slug or slug in query_slug:
            score += 35
            reasons.append("substring_slug")
        if score > 0:
            matches.append(
                {
                    "slug": slug,
                    "topic": topic,
                    "score": score,
                    "reasons": reasons,
                }
            )

    matches.sort(key=lambda item: (-item["score"], item["slug"]))
    best = matches[0] if matches else None
    payload = {
        "query": query,
        "query_slug": query_slug,
        "exists": bool(best),
        "best_match": best,
        "matches": matches[:5],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
