"""
search_en.py — Search English academic databases
Sources: CrossRef API + Semantic Scholar API
"""

import requests
from rapidfuzz import fuzz

CROSSREF_URL = "https://api.crossref.org/works"
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

HEADERS = {
    "User-Agent": "CitationFinder/1.0 (mailto:citation-finder@example.com)"
}


def search_crossref(query: str, limit: int = 5) -> list[dict]:
    """Search CrossRef for papers matching query."""
    try:
        resp = requests.get(
            CROSSREF_URL,
            params={"query": query, "rows": limit, "select": "DOI,title,author,published,container-title,volume,issue,page,type,URL"},
            headers=HEADERS,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("message", {}).get("items", [])
        results = []
        for item in items:
            title_list = item.get("title", [])
            title = title_list[0] if title_list else ""
            authors = []
            for a in item.get("author", []):
                family = a.get("family", "")
                given = a.get("given", "")
                if family:
                    authors.append({"family": family, "given": given})
            pub_date = item.get("published", {}).get("date-parts", [[None]])[0]
            year = pub_date[0] if pub_date else None
            container = item.get("container-title", [])
            journal = container[0] if container else ""
            results.append({
                "source": "crossref",
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "volume": item.get("volume", ""),
                "issue": item.get("issue", ""),
                "pages": item.get("page", ""),
                "doi": item.get("DOI", ""),
                "url": item.get("URL", ""),
                "type": item.get("type", "journal-article"),
            })
        return results
    except Exception as e:
        print(f"[CrossRef] Error: {e}")
        return []


def search_semantic_scholar(query: str, limit: int = 5) -> list[dict]:
    """Search Semantic Scholar for papers matching query."""
    try:
        resp = requests.get(
            SEMANTIC_SCHOLAR_URL,
            params={
                "query": query,
                "limit": limit,
                "fields": "title,authors,year,venue,externalIds,url,publicationTypes"
            },
            headers=HEADERS,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", [])
        results = []
        for item in items:
            authors = []
            for a in item.get("authors", []):
                name = a.get("name", "")
                parts = name.rsplit(" ", 1)
                if len(parts) == 2:
                    authors.append({"given": parts[0], "family": parts[1]})
                else:
                    authors.append({"given": "", "family": name})
            ext_ids = item.get("externalIds", {})
            doi = ext_ids.get("DOI", "")
            results.append({
                "source": "semantic_scholar",
                "title": item.get("title", ""),
                "authors": authors,
                "year": item.get("year"),
                "journal": item.get("venue", ""),
                "volume": "",
                "issue": "",
                "pages": "",
                "doi": doi,
                "url": item.get("url", "") or (f"https://doi.org/{doi}" if doi else ""),
                "type": "journal-article",
            })
        return results
    except Exception as e:
        print(f"[Semantic Scholar] Error: {e}")
        return []


def search_english(query: str, limit: int = 5) -> list[dict]:
    """Search both CrossRef and Semantic Scholar, deduplicate and rank results."""
    crossref_results = search_crossref(query, limit)
    ss_results = search_semantic_scholar(query, limit)

    all_results = crossref_results + ss_results

    # Score by title similarity to query
    for r in all_results:
        score = fuzz.token_sort_ratio(query.lower(), r["title"].lower())
        r["confidence"] = score

    # Deduplicate by DOI
    seen_dois = set()
    deduped = []
    for r in all_results:
        doi = r.get("doi", "")
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        deduped.append(r)

    # Sort by confidence
    deduped.sort(key=lambda x: x["confidence"], reverse=True)
    return deduped[:limit]


if __name__ == "__main__":
    import json
    results = search_english("attention is all you need")
    print(json.dumps(results, indent=2, ensure_ascii=False))
