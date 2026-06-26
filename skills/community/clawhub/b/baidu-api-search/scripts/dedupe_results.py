#!/usr/bin/env python3
"""Deduplicate Baidu raw results while preserving duplicate mappings."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {
    "from",
    "source",
    "spm",
    "share",
    "share_source",
    "share_from",
    "fr",
    "ssid",
    "bd_vid",
    "sa",
    "usg",
    "ved",
}

LOW_QUALITY_HINTS = ("采集", "聚合", "招商", "加盟", "广告", "推广")


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def canonicalize_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    for prefix in ("m.", "www."):
        if netloc.startswith(prefix):
            netloc = netloc[len(prefix):]
    query_items = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        key_lower = key.lower()
        if key_lower in TRACKING_KEYS or any(key_lower.startswith(prefix) for prefix in TRACKING_PREFIXES):
            continue
        query_items.append((key, value))
    query = urlencode(sorted(query_items), doseq=True)
    path = re.sub(r"/+$", "", parsed.path or "/")
    if path == "":
        path = "/"
    return urlunparse((scheme, netloc, path, "", query, ""))


def domain_of(url: str) -> str:
    return urlparse(url).netloc.lower()


def normalize_text(text: str) -> str:
    text = (text or "").casefold()
    text = re.sub(r"[\s\-_—|:：,，.。!！?？/\\()（）【】\[\]<>《》]+", "", text)
    text = re.sub(r"(百度快照|知乎专栏|哔哩哔哩|小红书|微博|贴吧)$", "", text)
    return text


def text_hash(text: str) -> str:
    return hashlib.sha1(normalize_text(text).encode("utf-8")).hexdigest()[:16]


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(a=normalize_text(a), b=normalize_text(b)).ratio()


def quality_flags(record: dict, domain: str) -> list[str]:
    text = " ".join(str(record.get(key, "")) for key in ("title", "snippet", "content", "website"))
    flags = []
    if any(hint in text for hint in LOW_QUALITY_HINTS):
        flags.append("possible_ad_or_low_quality")
    if domain.count(".") >= 3:
        flags.append("deep_subdomain")
    if not record.get("url"):
        flags.append("missing_url")
    return flags


def pick_best(source_records: list[dict]) -> dict:
    return sorted(
        source_records,
        key=lambda item: (
            int(item.get("rank") or 999999),
            -float(item.get("authority_score") or 0),
            -float(item.get("rerank_score") or 0),
        ),
    )[0]


def dedupe(records: list[dict], title_threshold: float, summary_threshold: float, domain_limit: int) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        canonical_url = canonicalize_url(str(record.get("url", "")))
        record["canonical_url"] = canonical_url
        groups[canonical_url or f"missing:{len(groups)}"].append(record)

    sources = []
    duplicates = []
    for canonical_url, group in groups.items():
        best = pick_best(group)
        domain = domain_of(best.get("canonical_url", ""))
        source_id = f"src_{len(sources) + 1:04d}"
        matched_queries = sorted({str(item.get("query", "")) for item in group if item.get("query")})
        matched_intents = sorted({str(item.get("query_intent", "")) for item in group if item.get("query_intent")})
        matched_stages = sorted({str(item.get("query_stage", "")) for item in group if item.get("query_stage")})
        matched_query_sources = sorted({str(item.get("query_source", "")) for item in group if item.get("query_source")})
        flags = quality_flags(best, domain)
        sources.append(
            {
                "source_id": source_id,
                "title": best.get("title") or "",
                "url": best.get("url") or "",
                "canonical_url": best.get("canonical_url") or "",
                "domain": domain,
                "snippet": best.get("snippet") or best.get("content") or "",
                "website": best.get("website") or "",
                "date": best.get("date") or "",
                "best_rank": int(best.get("rank") or 999999),
                "matched_queries": matched_queries,
                "matched_intents": matched_intents,
                "matched_stages": matched_stages,
                "matched_query_sources": matched_query_sources,
                "duplicate_count": len(group) - 1,
                "quality_flags": flags,
                "title_hash": text_hash(best.get("title") or ""),
            }
        )
        for dup in group[1:]:
            duplicates.append(
                {
                    "kept_source_id": source_id,
                    "reason": "duplicate_url",
                    "query": dup.get("query"),
                    "rank": dup.get("rank"),
                    "url": dup.get("url"),
                    "title": dup.get("title"),
                }
            )

    removed_by_text = set()
    for i, left in enumerate(sources):
        if left["source_id"] in removed_by_text:
            continue
        for right in sources[i + 1 :]:
            if right["source_id"] in removed_by_text:
                continue
            title_sim = similarity(left["title"], right["title"])
            summary_sim = similarity(left["snippet"], right["snippet"])
            if title_sim >= title_threshold or summary_sim >= summary_threshold:
                keep, drop = (left, right) if left["best_rank"] <= right["best_rank"] else (right, left)
                removed_by_text.add(drop["source_id"])
                duplicates.append(
                    {
                        "kept_source_id": keep["source_id"],
                        "dropped_source_id": drop["source_id"],
                        "reason": "near_duplicate_title_or_summary",
                        "title_similarity": round(title_sim, 3),
                        "summary_similarity": round(summary_sim, 3),
                        "url": drop["url"],
                        "title": drop["title"],
                    }
                )

    kept_sources = [source for source in sources if source["source_id"] not in removed_by_text]
    domain_counts = Counter()
    final_sources = []
    for source in sorted(kept_sources, key=lambda item: item["best_rank"]):
        domain = source["domain"]
        domain_counts[domain] += 1
        if domain_limit > 0 and domain_counts[domain] > domain_limit:
            source = dict(source)
            source["quality_flags"] = sorted(set(source["quality_flags"] + ["domain_limit_overflow"]))
        final_sources.append(source)

    return {
        "summary": {
            "raw_count": len(records),
            "deduped_count": len(final_sources),
            "duplicate_count": len(duplicates),
            "domain_count": len({source["domain"] for source in final_sources if source["domain"]}),
        },
        "sources": final_sources,
        "duplicates": duplicates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title-threshold", type=float, default=0.92)
    parser.add_argument("--summary-threshold", type=float, default=0.94)
    parser.add_argument("--domain-limit", type=int, default=8)
    args = parser.parse_args()

    result = dedupe(
        records=read_jsonl(Path(args.input)),
        title_threshold=args.title_threshold,
        summary_threshold=args.summary_threshold,
        domain_limit=args.domain_limit,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
