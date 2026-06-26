#!/usr/bin/env python3
"""
DuckDuckGo Search Script
Search the web using DuckDuckGo (no API key required)
Fallback to alternative search methods if DDG blocks
"""

import argparse
import json
import sys
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import re


def search_with_curl(query: str, max_results: int = 10):
    """Use curl to fetch DuckDuckGo results"""
    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
        
        cmd = [
            'curl', '-s', '-L', 
            '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.0',
            '--connect-timeout', '10',
            '--max-time', '20',
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        html = result.stdout
        
        if result.returncode != 0:
            return {"error": f"curl failed: {result.stderr}", "results": []}
        
        # Parse results
        results = []
        
        # Pattern 1: Standard result format
        result_pattern = r'<tr>.*?class="result-link"[^\u003e]*href="([^"]*)"[^\u003e]*>([^\u003c]*)</a>.*?class="result-snippet"[^\u003e]*>([^\u003c]*)<'
        matches = re.findall(result_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for url, title, snippet in matches[:max_results]:
            title = title.strip()
            snippet = snippet.strip()
            
            # Clean up URL
            if url.startswith('/'):
                url = 'https://duckduckgo.com' + url
            
            if title:
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet[:200] if snippet else ""
                })
        
        return {"results": results}
        
    except Exception as e:
        return {"error": str(e), "results": []}


def search_ddg(query: str, max_results: int = 10):
    """
    Search DuckDuckGo
    """
    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.0',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Parse results
        results = []
        
        # Find result rows
        import re
        rows = re.findall(r'<tr[^\u003e]*>(.*?)</tr>', html, re.DOTALL)
        
        for row in rows:
            # Extract link
            link_match = re.search(r'<a[^\u003e]*href="([^"]*)"[^\u003e]*>([^\u003c]*)</a>', row)
            if link_match:
                url = link_match.group(1)
                title = link_match.group(2).strip()
                
                # Extract snippet
                snippet_match = re.search(r'<td[^\u003e]*class="[^"]*snippet[^"]*"[^\u003e]*>([^\u003c]*)<', row)
                snippet = snippet_match.group(1).strip() if snippet_match else ""
                
                # Clean URL - decode DuckDuckGo redirect URLs
                if url.startswith('/'):
                    url = 'https://duckduckgo.com' + url
                
                # Decode DuckDuckGo redirect URLs
                if 'uddg=' in url:
                    match = re.search(r'uddg=([^&]+)', url)
                    if match:
                        url = urllib.parse.unquote(match.group(1))
                
                if title and len(title) > 3:
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet[:200]
                    })
        
        return {
            "query": query,
            "count": len(results),
            "results": results[:max_results]
        }
        
    except Exception as e:
        # Try curl fallback
        fallback = search_with_curl(query, max_results)
        if fallback.get("results"):
            return {
                "query": query,
                "count": len(fallback["results"]),
                "results": fallback["results"]
            }
        return {
            "query": query,
            "error": str(e),
            "results": []
        }


def main():
    parser = argparse.ArgumentParser(description="Search DuckDuckGo (no API key required)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", "-n", type=int, default=10,
                        help="Maximum results (1-20, default: 10)")
    
    args = parser.parse_args()
    
    # Validate max_results
    max_results = max(1, min(20, args.max_results))
    
    # Perform search
    result = search_ddg(args.query, max_results)
    
    # Output JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Return error code if search failed
    if "error" in result and not result.get("results"):
        sys.exit(1)


if __name__ == "__main__":
    main()
