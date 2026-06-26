#!/usr/bin/env python3
"""
bioRxiv - Fetch preprints via official bioRxiv API
No authentication required
"""

import argparse
import json
import urllib.request
import urllib.parse
import sys

BIO_RXIV_API = "https://api.biorxiv.org/details/biorxiv"

COLLECTIONS = [
    "bioinformatics", "genomics", "molecular-biology", "cell-biology",
    "genetics", "evolutionary-biology", "ecology", "neuroscience",
    "plant-biology", "microbiology", "immunology", "cancer-biology",
    "biochemistry", "biophysics", "structural-biology", "systems-biology",
    "synthetic-biology", "developmental-biology", "computational-biology"
]

# Map collection names to API category names
COLLECTION_MAP = {
    "bioinformatics": "bioinformatics",
    "genomics": "genomics",
    "molecular-biology": "molecular_biology",
    "cell-biology": "cell_biology",
    "genetics": "genetics",
    "evolutionary-biology": "evolutionary_biology",
    "ecology": "ecology",
    "neuroscience": "neuroscience",
    "plant-biology": "plant_biology",
    "microbiology": "microbiology",
    "immunology": "immunology",
    "cancer-biology": "cancer_biology",
    "biochemistry": "biochemistry",
    "biophysics": "biophysics",
    "structural-biology": "structural_biology",
    "systems-biology": "systems_biology",
    "synthetic-biology": "synthetic_biology",
    "developmental-biology": "developmental_biology",
    "computational-biology": "computational_biology",
}


def get_papers(collection="bioinformatics", start_date=None, end_date=None, limit=50):
    """
    Fetch papers from bioRxiv API.
    
    API format: https://api.biorxiv.org/details/biorxiv/[start]/[end]/[cursor]
    - Dates: YYYY-MM-DD format
    - cursor: starting position (default 0)
    - Returns up to 100 papers per call
    - Handles pagination automatically
    """
    
    # Default to last 30 days if no dates provided
    if not start_date:
        start_date = "2020-01-01"
    if not end_date:
        import datetime
        end_date = datetime.date.today().isoformat()
    
    # Get API category name
    api_category = COLLECTION_MAP.get(collection, collection)
    
    all_papers = []
    cursor = 0
    
    try:
        while len(all_papers) < limit:
            # Build URL with cursor
            url = f"{BIO_RXIV_API}/{start_date}/{end_date}/{cursor}"
            url += f"?category={api_category}"
            
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/json')
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
            
            # Parse response
            messages = data.get("messages", [])
            collection_data = data.get("collection", [])
            
            if not collection_data:
                break
            
            # Check total available
            if cursor == 0:
                total = messages[0].get("total", 0) if messages else 0
                print(f"Total papers available: {total}", file=sys.stderr)
            
            # Format papers
            for p in collection_data:
                if len(all_papers) >= limit:
                    break
                all_papers.append({
                    "doi": p.get("doi", ""),
                    "title": p.get("title", ""),
                    "authors": p.get("authors", "").split("; ")[:5] if p.get("authors") else [],
                    "date": p.get("date", ""),
                    "category": p.get("category", ""),
                    "version": p.get("version", ""),
                    "url": f"https://doi.org/{p.get('doi', '')}" if p.get("doi") else ""
                })
            
            # Check if more pages available
            if len(collection_data) < 100:
                break
            cursor += 100
        
        return all_papers, None
        
    except Exception as e:
        return None, str(e)


def get_recent_papers(days=7, limit=20):
    """Get papers from the last N days."""
    return get_papers(collection="bioinformatics", start_date=None, end_date=None, limit=limit)


def main():
    parser = argparse.ArgumentParser(description="bioRxiv API client")
    parser.add_argument("--collection", "-c", default="bioinformatics",
                        help=f"Category: {', '.join(COLLECTIONS)}")
    parser.add_argument("--start", "-s", default=None, 
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", "-e", default=None,
                        help="End date (YYYY-MM-DD)")
    parser.add_argument("--limit", "-l", type=int, default=20)
    parser.add_argument("--list", action="store_true", help="List available collections")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--days", "-d", type=int, default=None,
                        help="Get papers from last N days (overrides start/end)")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available collections:")
        for c in COLLECTIONS:
            print(f"  - {c}")
        return
    
    # Get papers
    papers, error = get_papers(args.collection, args.start, args.end, args.limit)
    
    if not papers:
        print("No papers found" + (f" - {error}" if error else ""))
        return
    
    if args.json:
        print(json.dumps(papers, indent=2))
    else:
        print(f"Recent bioRxiv papers ({args.collection}):\n")
        for i, p in enumerate(papers, 1):
            print(f"{i}. {p['title']}")
            if p.get('date'):
                print(f"   Date: {p['date']} (v{p.get('version', '1')})")
            if p.get('category'):
                print(f"   Category: {p['category']}")
            if p.get('doi'):
                print(f"   DOI: {p['doi']}")
            print()


if __name__ == "__main__":
    main()
