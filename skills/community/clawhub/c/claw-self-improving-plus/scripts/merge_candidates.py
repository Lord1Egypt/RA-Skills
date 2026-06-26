#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

STOP = {"the", "a", "an", "and", "or", "to", "of", "in", "for", "on", "is", "are", "be", "this", "that", "it"}


def tokens(text: str):
    parts = re.findall(r"[a-z0-9]{3,}", text.lower())
    return {p for p in parts if p not in STOP}


def load_jsonl(path: Path):
    out = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def similarity(item_a, tok_a, item_b, tok_b):
    score = jaccard(tok_a, tok_b)

    summary_a = tokens(str(item_a.get("summary", "")))
    summary_b = tokens(str(item_b.get("summary", "")))
    detail_a = tokens(str(item_a.get("details", "")))
    detail_b = tokens(str(item_b.get("details", "")))

    summary_overlap = jaccard(summary_a, summary_b)
    detail_overlap = jaccard(detail_a, detail_b)
    if summary_overlap >= 0.3:
        score += 0.18
    if detail_overlap >= 0.2:
        score += 0.1

    if item_a.get("type") == item_b.get("type"):
        score += 0.08
    if set(item_a.get("promotion_target_candidates") or []) & set(item_b.get("promotion_target_candidates") or []):
        score += 0.08
    if item_a.get("impact_scope") == item_b.get("impact_scope"):
        score += 0.04

    key_terms = {"uv", "pip", "python", "policy", "workspace", ".venv"}
    if len((tok_a & tok_b) & key_terms) >= 2:
        score += 0.12

    return min(score, 1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input JSONL")
    ap.add_argument("-o", "--output", help="Output JSON")
    ap.add_argument("--threshold", type=float, default=0.52)
    args = ap.parse_args()

    items = load_jsonl(Path(args.input))
    sigs = []
    for item in items:
        text = " ".join(str(item.get(k, "")) for k in ["summary", "details", "evidence"])
        sigs.append((item, tokens(text)))

    groups = []
    used = set()
    for i, (item_i, tok_i) in enumerate(sigs):
        if i in used:
            continue
        group = [item_i]
        used.add(i)
        for j in range(i + 1, len(sigs)):
            if j in used:
                continue
            item_j, tok_j = sigs[j]
            sim = similarity(item_i, tok_i, item_j, tok_j)
            if sim >= args.threshold:
                merged = dict(item_j)
                merged["_similarity"] = round(sim, 3)
                group.append(merged)
                used.add(j)
        groups.append(group)

    result = {
        "group_count": len(groups),
        "merge_groups": [
            {
                "ids": [x.get("id") for x in group],
                "count": len(group),
                "summary": group[0].get("summary", "") if group else "",
                "max_similarity": max((x.get("_similarity", 1.0) for x in group[1:]), default=1.0),
            }
            for group in groups if len(group) > 1
        ],
        "singletons": [group[0].get("id") for group in groups if len(group) == 1],
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
