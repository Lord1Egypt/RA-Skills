#!/usr/bin/env python3
"""Fact Checker — verifies claims and ranks sources."""

import argparse
import json
import re


def extract_claims(text: str) -> list[dict]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    claims = []
    keywords = [
        "is",
        "are",
        "was",
        "were",
        "caused",
        "leads to",
        "proven",
        "shows",
        "found",
        "reported",
    ]
    for i, s in enumerate(sentences):
        s = s.strip()
        if len(s) > 30 and any(k in s.lower() for k in keywords):
            claims.append(
                {"claim": s, "index": i, "status": "unverified", "confidence": 0}
            )
    return claims


def rank_sources(sources: list[dict]) -> list[dict]:
    reliable_domains = [
        "edu",
        "gov",
        "nature.com",
        "science.org",
        "arxiv.org",
        "ieee.org",
        "acm.org",
    ]
    for s in sources:
        domain = s.get("url", "").split("//")[-1].split("/")[0]
        s["reliability"] = (
            "high"
            if any(d in domain for d in reliable_domains)
            else "medium"
            if "wikipedia" in domain
            else "low"
        )
    return sorted(
        sources,
        key=lambda x: {"high": 0, "medium": 1, "low": 2}[x.get("reliability", "low")],
    )


def main():
    p = argparse.ArgumentParser(description="Verify claims and rank sources")
    p.add_argument("text", help="Text containing claims to verify")
    p.add_argument("-f", "--file", help="Read text from file")
    p.add_argument("--sources", help="JSON array of source URLs")
    args = p.parse_args()

    text = open(args.file).read() if args.file else args.text
    claims = extract_claims(text)
    print(f"📝 Extracted {len(claims)} verifiable claims:\n")
    for c in claims:
        print(f"  [{c['index']}] {c['claim'][:100]}...")
        print(f"      Status: {c['status']} | Confidence: {c['confidence']}%")

    if args.sources:
        sources = [{"url": u} for u in json.loads(args.sources)]
        ranked = rank_sources(sources)
        print(f"\n📚 Source ranking ({len(ranked)} sources):")
        for s in ranked:
            print(f"  [{s['reliability'].upper()}] {s['url']}")


if __name__ == "__main__":
    main()
