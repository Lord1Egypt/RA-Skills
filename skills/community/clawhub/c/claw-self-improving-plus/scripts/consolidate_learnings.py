#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_jsonl(path: Path):
    items = []
    if not path.exists():
        return items
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            items.append(json.loads(line))
    return items


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def choose_best(items: list[dict]) -> dict:
    def rank(item: dict):
        conf = {"low": 0, "medium": 1, "high": 2}.get(item.get("confidence", "low"), 0)
        reuse = {"low": 0, "medium": 1, "high": 2}.get(item.get("reuse_value", "low"), 0)
        details = len(item.get("details", ""))
        return (conf, reuse, details)
    return sorted(items, key=rank, reverse=True)[0]


def merge_group(group: list[dict]) -> dict:
    best = choose_best(group)
    related_ids = []
    evidence = []
    targets = []
    summaries = []
    details = []
    for item in group:
        if item.get("id") != best.get("id"):
            related_ids.append(item.get("id"))
        if item.get("evidence"):
            evidence.append(item.get("evidence"))
        if item.get("summary"):
            summaries.append(item.get("summary"))
        if item.get("details"):
            details.append(item.get("details"))
        targets.extend(item.get("promotion_target_candidates") or [])

    merged = dict(best)
    merged["summary"] = best.get("summary") or (summaries[0] if summaries else "Merged learning")
    extra_summaries = [s for s in dict.fromkeys(summaries) if s != merged["summary"]]
    merged["details"] = best.get("details", "")
    if extra_summaries:
        merged["details"] = (merged["details"] + " Related patterns: " + " | ".join(extra_summaries)).strip()
    merged["related_ids"] = sorted(set((best.get("related_ids") or []) + related_ids))
    merged["evidence"] = " | ".join(dict.fromkeys(evidence))
    merged["promotion_target_candidates"] = list(dict.fromkeys(targets)) or best.get("promotion_target_candidates", [])
    merged["status"] = "merged"
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scored", help="Scored JSONL")
    ap.add_argument("merge", help="Merge JSON from merge_candidates.py")
    ap.add_argument("-o", "--output", help="Output JSONL")
    args = ap.parse_args()

    items = load_jsonl(Path(args.scored))
    merge = load_json(Path(args.merge))
    by_id = {item.get("id"): item for item in items}
    consumed = set()
    consolidated = []

    for group in merge.get("merge_groups", []):
        ids = group.get("ids", [])
        real_items = [by_id[i] for i in ids if i in by_id]
        if len(real_items) >= 2:
            consolidated.append(merge_group(real_items))
            consumed.update(ids)

    for item in items:
        if item.get("id") not in consumed:
            consolidated.append(item)

    lines = [json.dumps(x, ensure_ascii=False) for x in consolidated]
    if args.output:
        Path(args.output).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
