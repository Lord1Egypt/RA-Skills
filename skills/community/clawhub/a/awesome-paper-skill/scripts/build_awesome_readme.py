#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone


AWESOME_BADGE = "[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)"


def topic_bucket(text: str):
    t = (text or "").lower()
    if any(k in t for k in ["security", "attack", "defense", "safety", "guardrail", "prompt injection"]):
        return "Security and Trustworthy Agents"
    if any(k in t for k in ["agent", "system", "architecture", "resource", "routing", "os"]):
        return "System Architecture and Resource Management"
    if any(k in t for k in ["memory", "benchmark", "evaluation", "reinforcement", "rl", "learning"]):
        return "Memory, Learning, and Evaluation"
    return "Applications and Human Factors"


def has_published_venue(p):
    return bool((p.get("venue") or "").strip())


def badge(label, link, color):
    return f"[![{label}](https://img.shields.io/badge/{label}-{color}.svg)]({link})"


def venue_tag(p):
    venue = (p.get("venue") or "").strip()
    if not venue:
        return ""
    clean = re.sub(r"\s+", " ", venue)
    return f"[{clean}]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    papers = data.get("papers", [])

    grouped = defaultdict(list)
    for p in papers:
        primary_text = f"{p.get('title', '')} {p.get('abstract', '')}"
        tcat = topic_bucket(primary_text)
        grouped[tcat].append(p)

    lines = []
    lines.append(f"# Awesome {args.topic.title()} Papers {AWESOME_BADGE}")
    lines.append("")
    lines.append(
        f"A curated list of papers related to **{args.topic}** (aggregated from arXiv, Crossref, and Semantic Scholar)."
    )
    lines.append("")
    lines.append(f"> Last updated: **{datetime.now(timezone.utc).strftime('%Y-%m-%d')}**")
    lines.append("")
    lines.append("## Table of Contents")

    category_order = [
        "Security and Trustworthy Agents",
        "System Architecture and Resource Management",
        "Memory, Learning, and Evaluation",
        "Applications and Human Factors",
    ]

    cats = [c for c in category_order if grouped.get(c)]
    for c in cats:
        anchor = re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")
        lines.append(f"- [{c}](#{anchor})")

    lines.append("")

    for c in cats:
        lines.append("---")
        lines.append("")
        lines.append(f"## {c}")
        lines.append("")

        items = sorted(grouped[c], key=lambda x: x.get("date", ""), reverse=True)
        for p in items:
            title = p.get("title", "Untitled").strip()
            primary = p.get("url") or p.get("arxiv") or "#"
            date = p.get("date") or "Unknown"
            arxiv = p.get("arxiv") or ""
            github = (p.get("github") or "").strip()

            lines.append(f"+ [{title}]({primary})")

            if has_published_venue(p):
                lines.append(f"  {venue_tag(p)}")

            if arxiv:
                lines.append(f"  {badge('arXiv', arxiv, 'b31b1b')}")

            if github:
                lines.append("  " + badge("GitHub", github, "9cf"))

            lines.append(f"  ({date})")
            lines.append("")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote README -> {args.output}")


if __name__ == "__main__":
    main()
