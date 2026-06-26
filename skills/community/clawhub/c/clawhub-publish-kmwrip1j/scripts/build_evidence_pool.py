#!/usr/bin/env python3
"""Build an evidence pool from raw records."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from mbti_common import (
    clean_text,
    confidence_band,
    context_signal_score,
    is_noise_segment,
    is_pseudosignal,
    iso_now,
    load_json,
    match_signal_rules,
    normalize_for_match,
    read_jsonl,
    segment_context_flags,
    shorten,
    split_into_segments,
    strength_to_weight,
    summarize_line,
    write_json,
)


def base_rule_score(rule: Dict) -> float:
    score = {"weak": 0.26, "moderate": 0.42, "strong": 0.58}[rule["strength"]]
    score += {"behavior": 0.03, "decision": 0.08, "self-report": 0.1}.get(rule.get("basis", "behavior"), 0.0)
    return score


def mention_score(rule: Dict, flags: Dict[str, bool]) -> float:
    score = base_rule_score(rule) + context_signal_score(flags)
    basis = rule.get("basis", "behavior")
    if basis == "self-report" and not (flags["self_report"] or flags["habit"]):
        score -= 0.2
    if basis == "decision" and not (flags["decision"] or flags["pressure"]):
        score -= 0.16
    if basis == "behavior" and not any(flags.values()):
        score -= 0.04
    return max(0.18, min(0.95, round(score, 3)))


def context_note(flags: Dict[str, bool]) -> str:
    active = [label for label, enabled in flags.items() if enabled]
    return ", ".join(active) if active else "surface-only"


def source_day(record: Dict) -> str:
    timestamp = record.get("timestamp") or ""
    if isinstance(timestamp, (int, float)):
        timestamp = str(timestamp)
    return timestamp[:10] if timestamp else "unknown-day"


def mention_from_rule(rule: Dict, record: Dict, segment: str, flags: Dict[str, bool]) -> Dict:
    score = mention_score(rule, flags)
    return {
        "rule_id": rule["id"],
        "axis": rule["axis"],
        "side": rule["side"],
        "tag": rule["tag"],
        "strength": rule["strength"],
        "confidence_score": score,
        "confidence": confidence_band(score),
        "report_summary": rule["report_summary"],
        "reason": rule["reason"],
        "functions": list(rule["functions"]),
        "context_flags": flags,
        "summary": summarize_line(segment),
        "excerpt": shorten(segment, 220),
        "source_ref": {
            "primary": {
                "source_type": record["source_type"],
                "source_path": record["source_path"],
                "location": record["location"],
                "timestamp": record["timestamp"],
                "speaker": record["speaker"],
            },
            "alternatives": [],
        },
        "source_key": f'{record["source_type"]}:{record["source_path"]}',
        "day_key": source_day(record),
    }


def pseudo_item(record: Dict, segment: str, index: int) -> Dict:
    return {
        "evidence_id": f"ev_{index:05d}",
        "summary": summarize_line(segment),
        "excerpt": shorten(segment, 220),
        "source_ref": {
            "primary": {
                "source_type": record["source_type"],
                "source_path": record["source_path"],
                "location": record["location"],
                "timestamp": record["timestamp"],
                "speaker": record["speaker"],
            },
            "alternatives": [],
        },
        "behavior_tag": "assistant-or-tool-instruction",
        "dimension_hints": [],
        "function_hints": [],
        "strength": "weak",
        "confidence": "low",
        "independence_score": 0.45,
        "is_counterevidence": False,
        "is_pseudosignal": True,
        "notes": "Pseudo-signal retained for auditability, but excluded from scoring.",
    }


def dedupe_mentions(mentions: List[Dict]) -> List[Dict]:
    deduped: Dict[Tuple[str, str], Dict] = {}
    for mention in mentions:
        key = (mention["rule_id"], normalize_for_match(mention["excerpt"]))
        current = deduped.get(key)
        if current is None or mention["confidence_score"] > current["confidence_score"]:
            deduped[key] = mention
    return list(deduped.values())


def aggregated_summary(rule_id: str, items: List[Dict]) -> str:
    top = max(items, key=lambda item: item["confidence_score"])
    base = top["report_summary"]
    if len(items) == 1:
        return base
    source_types = {item["source_ref"]["primary"]["source_type"] for item in items}
    return clean_text(
        f"{base} This pattern appears in {len(items)} passages across {len(source_types)} source categories."
    )


def aggregate_mentions(mentions: List[Dict], start_counter: int) -> List[Dict]:
    grouped: Dict[str, List[Dict]] = defaultdict(list)
    for mention in dedupe_mentions(mentions):
        grouped[mention["rule_id"]].append(mention)

    evidence_items: List[Dict] = []
    counter = start_counter
    for rule_id, items in grouped.items():
        counter += 1
        items.sort(key=lambda item: item["confidence_score"], reverse=True)
        top = items[0]
        source_types = {item["source_ref"]["primary"]["source_type"] for item in items}
        source_keys = {item["source_key"] for item in items}
        day_keys = {item["day_key"] for item in items}
        aggregate_score = min(
            0.95,
            top["confidence_score"]
            + min(0.18, 0.06 * (len(items) - 1))
            + min(0.12, 0.05 * (len(source_types) - 1))
            + min(0.1, 0.04 * (len(day_keys) - 1)),
        )
        evidence_items.append(
            {
                "evidence_id": f"ev_{counter:05d}",
                "summary": aggregated_summary(rule_id, items),
                "excerpt": top["excerpt"],
                "source_ref": {
                    "primary": top["source_ref"]["primary"],
                    "alternatives": [item["source_ref"]["primary"] for item in items[1:6]],
                },
                "behavior_tag": top["tag"],
                "dimension_hints": [{"axis": top["axis"], "side": top["side"], "reason": top["reason"]}],
                "function_hints": [{"function": function_name, "source_rule": rule_id} for function_name in top["functions"]],
                "strength": top["strength"] if len(items) == 1 else "strong",
                "confidence": confidence_band(aggregate_score),
                "independence_score": round(min(1.25, 0.72 + 0.08 * (len(source_keys) - 1) + 0.05 * (len(day_keys) - 1)), 2),
                "is_counterevidence": False,
                "is_pseudosignal": False,
                "notes": clean_text(
                    f"Aggregated from {len(items)} passages; contexts: {context_note(top['context_flags'])}; "
                    f"source types: {len(source_types)}; independent source buckets: {len(source_keys)}."
                ),
            }
        )
    return evidence_items


def build_pool(records: List[Dict], source_summary: Dict) -> Dict:
    mentions: List[Dict] = []
    pseudo_pool: List[Dict] = []
    counter = 0
    for record in records:
        for segment in split_into_segments(record["content"]):
            if is_noise_segment(segment):
                continue
            flags = segment_context_flags(segment)
            matches = match_signal_rules(segment)
            pseudo = is_pseudosignal(segment)
            if pseudo and not (flags["self_report"] or flags["habit"] or flags["decision"]):
                counter += 1
                pseudo_pool.append(pseudo_item(record, segment, counter))
                continue
            if not matches:
                continue
            for rule in matches:
                mentions.append(mention_from_rule(rule, record, segment, flags))

    merged = pseudo_pool + aggregate_mentions(mentions, counter)
    return {
        "generated_at": iso_now(),
        "record_count": len(records),
        "source_summary": source_summary,
        "evidence_pool": merged,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build evidence pool from raw records.")
    parser.add_argument("--raw-records", required=True, help="Path to raw_records.jsonl")
    parser.add_argument("--source-summary", required=True, help="Path to source_summary.json")
    parser.add_argument("--output", required=True, help="Path to evidence_pool.json")
    args = parser.parse_args()

    records = read_jsonl(Path(args.raw_records).expanduser().resolve())
    source_summary = load_json(Path(args.source_summary).expanduser().resolve())
    payload = build_pool(records, source_summary)
    write_json(Path(args.output).expanduser().resolve(), payload)


if __name__ == "__main__":
    main()
