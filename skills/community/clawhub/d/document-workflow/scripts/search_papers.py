#!/usr/bin/env python3
"""Search academic papers via Tavily (priority) with Semantic Scholar fallback."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request


def search_papers(query: str, max_results: int = 5, year_from: int = None, year_to: int = None, use_tavily: bool = True) -> list[dict]:
    """
    Search academic papers.
    
    Args:
        query: Search query
        max_results: Maximum number of results
        year_from: Filter from year (e.g., 2024)
        year_to: Filter to year (e.g., 2026)
        use_tavily: If True (default), use Tavily first; otherwise use Semantic Scholar
    
    Returns:
        List of paper dictionaries with pdf_url
    """
    if use_tavily:
        print(f"[INFO] Searching via Tavily (arXiv)...", file=sys.stderr)
        papers = _search_tavily(query, max_results, year_from)
        if papers:
            return papers
        print(f"[INFO] Tavily returned no results, falling back to Semantic Scholar...", file=sys.stderr)
    
    # Fallback to Semantic Scholar
    print(f"[INFO] Searching via Semantic Scholar...", file=sys.stderr)
    return _search_semantic_scholar(query, max_results, year_from, year_to)


def _search_semantic_scholar(query: str, max_results: int = 5, year_from: int = None, year_to: int = None) -> list[dict]:
    """Search papers on Semantic Scholar API (fallback)."""
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "g7Rh7ivl2o8mxhyjTvNhUDXyrD6VuUw5PgrjZqD7")
    # Request openAccessPdf field to filter papers with PDF
    fields = "paperId,title,abstract,year,venue,citationCount,authors,url,openAccessPdf"
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&limit={max_results * 2}&fields={fields}"  # Get more to filter
    
    if year_from:
        url += f"&year={year_from}-{year_to if year_to else year_from}"
    
    req = urllib.request.Request(url, headers={"x-api-key": api_key, "Accept": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            papers = [_format_paper(p) for p in data.get("data", [])]
            # Filter papers with PDF URLs (check for non-empty string) and return top results
            papers_with_pdf = [p for p in papers if p.get("pdf_url") and p["pdf_url"].strip()]
            
            if papers_with_pdf:
                return papers_with_pdf[:max_results]
            # Fallback: return papers without PDF if none have PDF
            return papers[:max_results]
    except Exception as e:
        print(f"[WARNING] Semantic Scholar search failed: {e}", file=sys.stderr)
        return []


def _search_tavily(query: str, max_results: int = 5, year_from: int = None) -> list[dict]:
    """Search arXiv papers via Tavily MCP to get direct PDF URLs (priority method)."""
    mcporter_path = shutil.which("mcporter")
    if not mcporter_path:
        for path in [
            r"C:\Users\Lenovo\AppData\Roaming\npm\mcporter.cmd",
            r"C:\Users\Lenovo\AppData\Roaming\npm\mcporter",
        ]:
            if os.path.isfile(path):
                mcporter_path = path
                break
    
    if not mcporter_path:
        print("[WARNING] mcporter not found", file=sys.stderr)
        return []
    
    # Build search query with year filter if specified
    search_query = f"site:arxiv.org {query} pdf"
    if year_from:
        search_query += f" after:{year_from}-01-01"
    
    cmd = [
        mcporter_path, "call", "tavily.tavily_search",
        "query:", search_query,
        "max_results:", str(max_results * 2),
        "search_depth:", "fast"
    ]
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
            encoding='utf-8', errors='replace',
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        
        if not result.stdout.strip():
            return []
        
        data = json.loads(result.stdout)
        papers = []
        for r in data.get("results", []):
            url = r.get("url", "")
            arxiv_id = None
            
            # Extract arXiv ID from URL
            if "arxiv.org/pdf/" in url or "arxiv.org/abs/" in url:
                # Handle both www.arxiv.org and arxiv.org
                # URL format: https://arxiv.org/pdf/2406.09455 or https://www.arxiv.org/pdf/2406.09455
                if "/pdf/" in url:
                    arxiv_id = url.split("/pdf/")[-1].split("?")[0]
                elif "/abs/" in url:
                    arxiv_id = url.split("/abs/")[-1].split("?")[0]
            else:
                # Try to extract from content
                match = re.search(r'arXiv[:\s]*(\d+\.\d+)', r.get("content", "") or "")
                if match:
                    arxiv_id = match.group(1)
            
            # Validate arXiv ID (format: YYMM.NNNNN, at least 5 chars like 2406.09455)
            if arxiv_id and len(arxiv_id) >= 5 and re.match(r'^\d+\.\d+', arxiv_id):
                papers.append({
                    "title": r.get("title", "Unknown").replace("[PDF] ", "").strip(),
                    "authors": [],
                    "abstract": (r.get("content") or "")[:500],
                    "url": f"https://arxiv.org/abs/{arxiv_id}",
                    "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
                    "source": "tavily_arxiv",
                    "year": None,
                    "venue": "arXiv.org",
                    "citationCount": 0,
                    "paperId": arxiv_id,
                })
        
        return papers[:max_results]
    
    except Exception as e:
        print(f"[WARNING] Tavily search failed: {e}", file=sys.stderr)
        return []


def _format_paper(paper: dict) -> dict:
    """Format paper data to standard schema."""
    result = {
        "title": paper.get("title", "Unknown"),
        "authors": [a["name"] for a in paper.get("authors", [])],
        "abstract": (paper.get("abstract") or "")[:300],
        "url": paper.get("url", ""),
        "pdf_url": paper.get("openAccessPdf", {}).get("url"),
        "source": "semantic_scholar",
        "year": paper.get("year"),
        "venue": paper.get("venue", ""),
        "citationCount": paper.get("citationCount", 0),
        "paperId": paper.get("paperId", ""),
    }
    
    # Construct arXiv PDF URL if venue is arXiv but no pdf_url
    if not result["pdf_url"] and result["venue"] == "arXiv.org":
        if "arxiv.org/abs/" in result["url"]:
            arxiv_id = result["url"].split("/abs/")[-1]
            result["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}"
    
    return result


def main():
    import io
    # Fix Windows console encoding issue
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(description="Search academic papers")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--max_results", type=int, default=5, help="Max results")
    parser.add_argument("--year_from", type=int, help="Filter from year")
    parser.add_argument("--year_to", type=int, help="Filter to year")
    parser.add_argument("--use_tavily", action="store_true", default=True, help="Use Tavily first (default)")
    parser.add_argument("--use_semantic_scholar", action="store_true", help="Use Semantic Scholar first")
    args = parser.parse_args()
    
    # Determine which search method to use
    use_tavily = not args.use_semantic_scholar
    
    papers = search_papers(args.query, args.max_results, args.year_from, args.year_to, use_tavily=use_tavily)
    print(json.dumps(papers, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
