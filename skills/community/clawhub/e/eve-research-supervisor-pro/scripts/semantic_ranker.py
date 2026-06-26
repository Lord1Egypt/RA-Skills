#!/usr/bin/env python3
"""
semantic_ranker.py — Rank papers by citation count using Semantic Scholar API
Reads metadata.json from arxiv_downloader.py output
Usage: python3 semantic_ranker.py [papers_dir]
"""

import json
import os
import sys
import time
import requests

def rank_papers(papers_dir="papers_pdf"):
    metadata_path = f"{papers_dir}/metadata.json"

    if not os.path.exists(metadata_path):
        print(f"❌ metadata.json not found in {papers_dir}/")
        print("   Run arxiv_downloader.py first.")
        sys.exit(1)

    with open(metadata_path) as f:
        papers = json.load(f)

    print(f"📊 Ranking {len(papers)} papers via Semantic Scholar...")

    ranked = []

    for i, paper in enumerate(papers):
        title = paper.get("title", "")
        arxiv_id = paper.get("arxiv_id", "").replace("_", "/")

        citations = 0
        year = None

        try:
            # Try ArXiv ID lookup first (more reliable)
            url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id.split('v')[0]}?fields=citationCount,year,title"
            time.sleep(1.2)  # Respect rate limits
            r = requests.get(url, timeout=15)

            if r.status_code == 200:
                data = r.json()
                citations = data.get("citationCount", 0) or 0
                year = data.get("year")
            else:
                # Fallback: title search
                url2 = f"https://api.semanticscholar.org/graph/v1/paper/search?query={requests.utils.quote(title)}&limit=1&fields=citationCount,year"
                r2 = requests.get(url2, timeout=15)
                if r2.status_code == 200:
                    results = r2.json().get("data", [])
                    if results:
                        citations = results[0].get("citationCount", 0) or 0
                        year = results[0].get("year")

        except Exception as e:
            print(f"  ⚠️  [{i+1}] Could not fetch citations for: {title[:50]} ({e})")

        paper["citations"] = citations
        paper["year"] = year
        ranked.append(paper)
        print(f"  [{i+1}/{len(papers)}] {citations:>5} citations | {title[:55]}...")

    # Sort by citation count descending
    ranked.sort(key=lambda x: x.get("citations", 0), reverse=True)

    # Save ranked results
    with open("top_papers.json", "w") as f:
        json.dump(ranked, f, indent=2)

    # Also save human-readable txt
    with open("top_papers.txt", "w") as f:
        f.write(f"# Top Papers by Citation Count\n\n")
        for rank, p in enumerate(ranked[:40], 1):
            f.write(f"{rank}. [{p.get('citations',0)} citations] {p['title']}\n")
            f.write(f"   Authors: {', '.join(p['authors'][:3])}\n")
            f.write(f"   Published: {p.get('published','?')[:10]}\n")
            f.write(f"   arXiv: {p['arxiv_id']}\n\n")

    print(f"\n✅ Ranked {len(ranked)} papers")
    print(f"📋 Saved to top_papers.json + top_papers.txt")
    return ranked


if __name__ == "__main__":
    papers_dir = sys.argv[1] if len(sys.argv) > 1 else "papers_pdf"
    rank_papers(papers_dir)
