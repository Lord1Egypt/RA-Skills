from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REVIEW_MARKERS = (
    "maybe",
    "perhaps",
    "rumored",
    "implied",
    "seems",
    "appears",
    "likely",
    "可能",
    "似乎",
    "大概",
    "也许",
)

SOURCE_LABELS = {
    "manual": "user_summary",
    "wiki": "fandom_wiki",
    "quotes": "quoted_text",
    "plot": "quoted_text",
}

ATTRIBUTE_PATTERNS = {
    "relationship": re.compile(r"\b(friend|brother|sister|mentor|partner|rival|mother|father)\b|关系|姐姐|哥哥|师父|同伴"),
    "official_statement": re.compile(r"official|guidebook|profile|设定集|官方|访谈"),
    "setting_attribute": re.compile(r"\b(age|height|rank|job|class|species)\b|年龄|身高|职业|种族|称号"),
    "plot_event": re.compile(r"\b(after|before|during|battle|incident|chapter|episode)\b|后来|曾经|在.*中|事件|战斗"),
}


def classify_bucket(text: str) -> str:
    for bucket, pattern in ATTRIBUTE_PATTERNS.items():
        if pattern.search(text):
            return bucket
    return "objective_fact"


def needs_review(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower or marker in text for marker in REVIEW_MARKERS)


def index_payload(payload: dict) -> dict:
    entries = []
    counts: Counter[str] = Counter()
    for entry in payload.get("entries", []):
        source_type = entry.get("source_type") or payload.get("source", {}).get("source_type", "manual")
        evidence_label = SOURCE_LABELS.get(source_type, "user_summary")
        indexed = dict(entry)
        indexed["evidence_label"] = evidence_label
        indexed["candidate_bucket"] = classify_bucket(entry.get("text", ""))
        indexed["needs_review"] = needs_review(entry.get("text", ""))
        counts[evidence_label] += 1
        entries.append(indexed)
    return {
        "schema_version": "0.1",
        "source": payload.get("source", {}),
        "entries": entries,
        "summary": dict(counts),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Attach evidence labels and review flags to normalized entries.")
    parser.add_argument("--input", required=True, help="Path to normalized JSON.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    indexed = index_payload(payload)
    content = json.dumps(indexed, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(content + "\n", encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
