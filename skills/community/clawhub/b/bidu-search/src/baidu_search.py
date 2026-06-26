#!/usr/bin/env python3
"""
Baidu Web Search Skill for OpenClaw

Search the web using Baidu Search API.
"""

import requests
import os
import json
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


class BaiduSearch:
    """Baidu Web Search client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Baidu Search client.
        
        Args:
            api_key: Baidu Search API key. If None, will try to load from .env or environment.
        """
        self.api_key = api_key or os.getenv('BAIDU_API_KEY')
        self.base_url = 'https://aip.baidubce.com/rest/2.0/search'
        
    def search(self, query: str, count: int = 10) -> List[Dict]:
        """
        Search the web using Baidu.
        
        Args:
            query: Search query string.
            count: Number of results to return (default: 10).
            
        Returns:
            List of search results with title, url, and snippet.
        """
        if not self.api_key:
            raise ValueError("Baidu API key is required. Set BAIDU_API_KEY environment variable.")
        
        # Baidu Search API endpoint
        url = f"{self.base_url}/v1/search"
        
        params = {
            'query': query,
            'count': count,
            'ak': self.api_key
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' not in data:
            return []
        
        return data['results']


def baidu_search(query: str, count: int = 10) -> str:
    """
    Search the web using Baidu.
    
    Args:
        query: Search query string.
        count: Number of results to return (default: 10).
        
    Returns:
        Formatted search results as string.
    """
    try:
        searcher = BaiduSearch()
        results = searcher.search(query, count)
        
        if not results:
            return "❌ No results found."
        
        output = []
        output.append(f"🔍 Baidu Search Results for: {query}\n")
        output.append(f"Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            url = result.get('url', 'N/A')
            snippet = result.get('abstract', result.get('snippet', 'N/A'))
            
            output.append(f"{i}. **{title}**")
            output.append(f"   URL: {url}")
            output.append(f"   {snippet}\n")
        
        return '\n'.join(output)
    
    except Exception as e:
        return f"❌ Search failed: {str(e)}"


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python baidu_search.py <query> [count]")
        print("  query: Search query string")
        print("  count: Number of results (default: 10)")
        sys.exit(1)
    
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    result = baidu_search(query, count)
    print(result)
