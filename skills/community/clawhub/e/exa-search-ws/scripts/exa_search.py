#!/usr/bin/env python3
"""
Exa Semantic Search and Content Extraction Utility
Author: Simon-Pierre Boucher
"""

import os
import sys
import json
import argparse
from exa_py import Exa

def main():
    parser = argparse.ArgumentParser(description="Exa Semantic Search & Extraction Utility")
    parser.add_argument("query", help="The search query or starting URL")
    parser.add_argument("--type", default="auto", choices=["auto", "instant", "fast", "deep-lite", "deep", "deep-reasoning"], help="Exa search type")
    parser.add_argument("--num-results", type=int, default=10, help="Number of results to return")
    parser.add_argument("--highlights", action="store_true", help="Extract key highlights relevant to query")
    parser.add_argument("--text", action="store_true", help="Extract clean Markdown full text")
    parser.add_argument("--summary", action="store_true", help="Generate an LLM summary of the page")
    parser.add_argument("--max-age", type=int, default=None, help="Cache freshness limit in hours (0 for live crawl)")
    parser.add_argument("--subpages", type=int, default=0, help="Number of subpages to crawl (0 to disable)")
    
    args = parser.parse_args()
    
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        print("Error: EXA_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
        
    exa = Exa(api_key=api_key)
    
    contents_spec = {}
    if args.highlights:
        contents_spec["highlights"] = True
    if args.text:
        contents_spec["text"] = True
    if args.summary:
        contents_spec["summary"] = True
        
    try:
        # Perform Search
        search_params = {
            "query": args.query,
            "type": args.type,
            "num_results": args.num_results
        }
        if contents_spec:
            search_params["contents"] = contents_spec
            
        results = exa.search(**search_params)
        
        output = {
            "requestId": getattr(results, "request_id", None),
            "results": []
        }
        
        for r in results.results:
            res = {
                "title": r.title,
                "url": r.url,
                "score": r.score,
                "publishedDate": r.published_date,
                "author": r.author,
                "id": r.id
            }
            if args.highlights and hasattr(r, "highlights"):
                res["highlights"] = r.highlights
            if args.text and hasattr(r, "text"):
                res["text"] = r.text
            if args.summary and hasattr(r, "summary"):
                res["summary"] = r.summary
            output["results"].append(res)
            
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"Error executing Exa search: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
