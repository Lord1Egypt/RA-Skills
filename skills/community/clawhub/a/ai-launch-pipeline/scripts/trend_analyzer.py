#!/usr/bin/env python3
"""Trend Analyzer — identify patterns and generate insights report."""

import json, os, sys, re
from collections import Counter
from datetime import datetime

DATA_DIR = os.environ.get("PIPELINE_DATA_DIR", "data")
ANALYSIS_DIR = os.environ.get("PIPELINE_ANALYSIS_DIR", "analysis")

STOPWORDS = set("the and for with that this from your are was will can has its not new but all ai also".split())


def load_launches(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def extract_keywords(titles: list[str]) -> dict:
    words = []
    for t in titles:
        tokens = re.findall(r"[A-Za-z]{4,}", t.lower())
        words.extend(w for w in tokens if w not in STOPWORDS)
    return dict(Counter(words).most_common(20))


def extract_orgs(titles: list[str]) -> dict:
    orgs = []
    for t in titles:
        matches = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", t)
        orgs.extend(m for m in matches if len(m) > 3)
    return dict(Counter(orgs).most_common(15))


def run(launches: list) -> dict:
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    titles = [l.get("title", "") for l in launches]
    sources = Counter(l.get("source", "unknown") for l in launches)
    categories = Counter(l.get("category", "unknown") for l in launches)
    keywords = extract_keywords(titles)
    orgs = extract_orgs(titles)

    trends = {
        "total_launches": len(launches),
        "by_source": dict(sources.most_common(10)),
        "by_category": dict(categories),
        "top_keywords": keywords,
        "top_organizations": orgs,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    # Write JSON
    trends_path = os.path.join(ANALYSIS_DIR, "trends.json")
    with open(trends_path, "w") as f:
        json.dump(trends, f, indent=2)

    # Write Markdown report
    report = generate_report(trends)
    report_path = os.path.join(ANALYSIS_DIR, "launch_analysis_report.md")
    with open(report_path, "w") as f:
        f.write(report)

    print(f"  Trends → {trends_path}")
    print(f"  Report → {report_path}")
    return trends


def generate_report(trends: dict) -> str:
    r = "# AI Product Launch Analysis Report\n\n"
    r += f"_Generated: {trends['generated_at']}_\n\n"
    r += f"**Total launches analyzed:** {trends['total_launches']}\n\n"

    r += "## Launches by Source\n"
    for src, cnt in trends["by_source"].items():
        r += f"- **{src}**: {cnt}\n"

    r += "\n## Launches by Category\n"
    for cat, cnt in trends["by_category"].items():
        r += f"- **{cat}**: {cnt}\n"

    r += "\n## Top Keywords\n"
    for kw, cnt in list(trends["top_keywords"].items())[:10]:
        r += f"- **{kw}**: {cnt} mentions\n"

    r += "\n## Top Organizations\n"
    for org, cnt in list(trends["top_organizations"].items())[:10]:
        r += f"- **{org}**: {cnt} mentions\n"

    return r


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=os.path.join(DATA_DIR, "enriched_launches.json"))
    args = p.parse_args()
    launches = load_launches(args.input)
    run(launches)
