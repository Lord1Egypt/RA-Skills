#!/usr/bin/env python3
"""
Academic source search via Semantic Scholar API.

Free tier: 100 requests per 5 minutes, no API key required for basic search.
Returns structured paper metadata for citation integration.

Usage:
  python scholar.py --query "AI education outcomes" --limit 10 --json
  python scholar.py --query "climate change policy" --year-min 2020 --year-max 2025 --field "Environmental Science"
  python scholar.py --doi "10.1016/j.edurev.2023.100512" --json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

API_BASE = "https://api.semanticscholar.org/graph/v1"
PAPER_FIELDS = "title,authors,year,abstract,externalIds,venue,referenceCount,citationCount,journal,publicationTypes"


def _api_get(url: str, max_retries: int = 3) -> Dict[str, Any]:
    """Make a GET request to the Semantic Scholar API with exponential backoff."""
    req = urllib.request.Request(url, headers={"User-Agent": "AcademicComposer-Skill/1.0"})
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                wait = 10 * (2 ** attempt)
                print(f"Rate limited (429). Retry {attempt + 1}/{max_retries} in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise


def search_papers(
    query: str,
    limit: int = 10,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    fields_of_study: Optional[str] = None,
) -> List[Dict[str, Any]]:
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": PAPER_FIELDS,
    }
    if year_min or year_max:
        y_min = year_min or 1900
        y_max = year_max or 2099
        params["year"] = f"{y_min}-{y_max}"
    if fields_of_study:
        params["fieldsOfStudy"] = fields_of_study

    url = f"{API_BASE}/paper/search?{urllib.parse.urlencode(params)}"
    data = _api_get(url)

    results = []
    for i, paper in enumerate(data.get("data", []), 1):
        record = _normalize_paper(paper, f"S{i}")
        if record:
            results.append(record)
    return results


def lookup_by_doi(doi: str) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE}/paper/DOI:{urllib.parse.quote(doi, safe='')}?fields={PAPER_FIELDS}"
    try:
        data = _api_get(url)
        return _normalize_paper(data, "S1")
    except Exception:
        return None


def _normalize_paper(paper: Dict[str, Any], source_id: str) -> Optional[Dict[str, Any]]:
    if not paper.get("title"):
        return None

    authors = []
    for a in paper.get("authors", []):
        name = a.get("name", "")
        if name:
            authors.append(name)

    ext_ids = paper.get("externalIds") or {}
    journal_info = paper.get("journal") or {}

    return {
        "id": source_id,
        "title": paper["title"],
        "authors": authors,
        "year": paper.get("year"),
        "abstract": (paper.get("abstract") or "")[:300],
        "doi": ext_ids.get("DOI"),
        "venue": paper.get("venue") or journal_info.get("name", ""),
        "journal": journal_info.get("name", ""),
        "volume": journal_info.get("volume"),
        "pages": journal_info.get("pages"),
        "citation_count": paper.get("citationCount", 0),
        "publication_types": paper.get("publicationTypes", []),
        "used_for": "",
    }


def format_source_list(sources: List[Dict[str, Any]], verbose: bool = False) -> str:
    lines = []
    for s in sources:
        authors_str = ", ".join(s["authors"][:3])
        if len(s["authors"]) > 3:
            authors_str += " et al."
        year = s.get("year") or "n.d."
        citations = s.get("citation_count", 0)
        doi = s.get("doi") or "no DOI"

        line = f"  [{s['id']}] {authors_str} ({year}). {s['title']}."
        if s.get("venue"):
            line += f" {s['venue']}."
        line += f" [citations: {citations}, DOI: {doi}]"
        lines.append(line)

        if verbose and s.get("abstract"):
            lines.append(f"        Abstract: {s['abstract']}...")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search academic papers via Semantic Scholar")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", type=str, help="Search query (keywords or phrase)")
    group.add_argument("--doi", type=str, help="Look up a single paper by DOI")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--year-min", type=int, help="Minimum publication year")
    parser.add_argument("--year-max", type=int, help="Maximum publication year")
    parser.add_argument("--field", type=str, help="Field of study filter")
    parser.add_argument("--verbose", action="store_true", help="Include abstracts in output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.doi:
        result = lookup_by_doi(args.doi)
        if result:
            sources = [result]
        else:
            print(f"Paper not found for DOI: {args.doi}", file=sys.stderr)
            sys.exit(1)
    else:
        sources = search_papers(
            query=args.query,
            limit=args.limit,
            year_min=args.year_min,
            year_max=args.year_max,
            fields_of_study=args.field,
        )

    if not sources:
        print("No papers found.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(sources, indent=2, ensure_ascii=False))
    else:
        print(f"\nFound {len(sources)} papers:\n")
        print(format_source_list(sources, verbose=args.verbose))
        print()


if __name__ == "__main__":
    main()
