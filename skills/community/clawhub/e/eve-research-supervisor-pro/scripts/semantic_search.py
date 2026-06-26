#!/usr/bin/env python3
"""
semantic_search.py — Full-text semantic paper search via Semantic Scholar
Better than arXiv keyword search — finds by meaning, not just title words.
Usage: python3 semantic_search.py "<query>" [limit] [output_file]
"""

import sys
import os
import json
import time
import requests

SS_BASE = "https://api.semanticscholar.org/graph/v1"
FIELDS  = "paperId,title,abstract,authors,year,citationCount,openAccessPdf,externalIds"


def search_semantic_scholar(query, limit=30, output_file="semantic_results.json"):
    print(f"🔍 Semantic Scholar search: {query}")
    print(f"   Fetching up to {limit} results...\n")

    results = []
    offset = 0
    batch = min(limit, 100)

    while len(results) < limit:
        url = (
            f"{SS_BASE}/paper/search"
            f"?query={requests.utils.quote(query)}"
            f"&limit={batch}&offset={offset}"
            f"&fields={FIELDS}"
        )
        try:
            time.sleep(1.0)
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"❌ Search failed: {e}")
            break

        batch_data = data.get("data", [])
        if not batch_data:
            break

        results.extend(batch_data)
        total = data.get("total", 0)
        print(f"  Fetched {len(results)}/{min(limit, total)} results...")

        if len(results) >= limit or len(results) >= total:
            break
        offset += batch

    results = results[:limit]

    # Enrich with arXiv IDs where available
    enriched = []
    for r in results:
        arxiv_id = r.get("externalIds", {}).get("ArXiv", "")
        open_pdf = r.get("openAccessPdf", {}) or {}
        enriched.append({
            "paperId": r.get("paperId", ""),
            "title": r.get("title", ""),
            "abstract": r.get("abstract", ""),
            "authors": [a.get("name", "") for a in r.get("authors", [])[:5]],
            "year": r.get("year"),
            "citations": r.get("citationCount", 0),
            "arxiv_id": arxiv_id,
            "pdf_url": open_pdf.get("url", f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else ""),
            "ss_url": f"https://www.semanticscholar.org/paper/{r.get('paperId','')}"
        })

    # Sort by citation count
    enriched.sort(key=lambda x: x.get("citations", 0), reverse=True)

    # Save JSON
    with open(output_file, "w") as f:
        json.dump(enriched, f, indent=2)

    # Save readable markdown
    md_file = output_file.replace(".json", ".md")
    with open(md_file, "w") as f:
        f.write(f"# Semantic Scholar Search Results\n")
        f.write(f"**Query:** {query}\n")
        f.write(f"**Total found:** {len(enriched)}\n\n---\n\n")

        for i, p in enumerate(enriched, 1):
            f.write(f"## {i}. {p['title']}\n")
            f.write(f"**Authors:** {', '.join(p['authors'][:3])}\n")
            f.write(f"**Year:** {p.get('year','?')} | **Citations:** {p.get('citations',0)}\n")
            if p.get("arxiv_id"):
                f.write(f"**arXiv:** [{p['arxiv_id']}](https://arxiv.org/abs/{p['arxiv_id']})\n")
            if p.get("pdf_url"):
                f.write(f"**PDF:** {p['pdf_url']}\n")
            if p.get("abstract"):
                f.write(f"\n**Abstract:** {p['abstract'][:400]}...\n")
            f.write("\n---\n\n")

    print(f"\n✅ Found {len(enriched)} papers")
    print(f"   Saved: {output_file}, {md_file}")
    return enriched


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 semantic_search.py "<query>" [limit] [output_file]')
        sys.exit(1)
    query  = sys.argv[1]
    limit  = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    output = sys.argv[3] if len(sys.argv) > 3 else "semantic_results.json"
    search_semantic_scholar(query, limit, output)
