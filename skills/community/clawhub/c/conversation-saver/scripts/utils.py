#!/usr/bin/env python3
"""
Utils - Helper functions for conversation-saver.
"""

from typing import List, Dict, Set
import hashlib


def deduplicate_facts(facts: List[Dict]) -> List[Dict]:
    """Remove duplicate facts based on content similarity."""
    seen_hashes: Set[str] = set()
    deduped = []

    for fact in facts:
        content = fact["content"].strip()
        # Simple hash-based dedupe
        content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()[:8]
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            deduped.append(fact)

    return deduped


def is_relevant_message(message: Dict, min_length: int = 5) -> bool:
    """Check if a message is worth processing."""
    content = message.get("content", "").strip()
    if len(content) < min_length:
        return False
    # TODO: Add more heuristics (mentions user keywords, etc.)
    return True


def parse_date_from_string(s: str) -> str:
    """Extract date info from Chinese date expressions."""
    # Basic patterns - could be expanded
    patterns = {
        r"本周[三四五六日]": "this_week",
        r"下周[一二三四五六日]": "next_week",
        r"(\d+)月(\d+)日": "explicit_date"
    }
    for pattern, label in patterns.items():
        if re.search(pattern, s):
            return label
    return "unknown"
