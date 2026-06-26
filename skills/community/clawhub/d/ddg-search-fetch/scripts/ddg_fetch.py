#!/usr/bin/env python3
"""
DuckDuckGo Web Fetcher
Fetch and extract readable content from URLs
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import re
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """Strip HTML tags and decode entities"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
        
    def handle_data(self, d):
        self.fed.append(d)
        
    def handle_entityref(self, name):
        entities = {
            'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"',
            'apos': "'", 'nbsp': ' ', 'copy': '©', 'reg': '®',
            'trade': '™', 'hellip': '…', 'mdash': '—', 'ndash': '–'
        }
        self.fed.append(entities.get(name, f'&{name};'))
        
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    """Remove HTML tags from string"""
    s = MLStripper()
    try:
        s.feed(html)
    except:
        return html
    return s.get_data()


def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep common ones
    text = re.sub(r'[^\w\s.,!?;:\-\'"()\[\]中文中文\-]', '', text)
    return text.strip()


def fetch_url(url: str, timeout: int = 30):
    """
    Fetch a URL and extract readable content.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
    
    Returns:
        dict: Fetched content with title, text, and metadata
    """
    result = {
        "url": url,
        "title": "",
        "text": "",
        "content": "",
        "error": None,
        "status_code": 0
    }
    
    try:
        # Validate URL
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            # Add https if missing
            url = 'https://' + url
            parsed = urllib.parse.urlparse(url)
        
        if not parsed.netloc:
            result["error"] = "Invalid URL"
            return result
        
        # Build request
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.0 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
            }
        )
        
        # Make request
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result["status_code"] = response.status
            
            # Get content encoding
            content_encoding = response.headers.get('Content-Encoding', '')
            
            # Read content
            content = response.read()
            
            # Decode based on encoding
            if content_encoding == 'gzip':
                import gzip
                content = gzip.decompress(content)
            
            html = content.decode('utf-8', errors='ignore')
        
        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            result["title"] = strip_tags(title_match.group(1)).strip()
        
        # Try to find main content
        contentSelectors = [
            # Common article content selectors
            (r'<article[^>]*>(.*?)</article>', 'article'),
            (r'<main[^>]*>(.*?)</main>', 'main'),
            (r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>', 'content div'),
            (r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>', 'article div'),
            (r'<div[^>]*class="[^"]*post[^"]*"[^>]*>(.*?)</div>', 'post div'),
            (r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>', 'content div'),
            (r'<div[^>]*id="[^"]*main[^"]*"[^>]*>(.*?)</div>', 'main div'),
        ]
        
        main_content = ""
        for pattern, name in contentSelectors:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                main_content = match.group(1)
                break
        
        # If no content found, use body
        if not main_content:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
            if body_match:
                main_content = body_match.group(1)
        
        # Extract text from content
        if main_content:
            # Remove script and style elements
            main_content = re.sub(r'<script[^>]*>.*?</script>', '', main_content, flags=re.DOTALL | re.IGNORECASE)
            main_content = re.sub(r'<style[^>]*>.*?</style>', '', main_content, flags=re.DOTALL | re.IGNORECASE)
            main_content = re.sub(r'<noscript[^>]*>.*?</noscript>', '', main_content, flags=re.DOTALL | re.IGNORECASE)
            main_content = re.sub(r'<!--.*?-->', '', main_content, flags=re.DOTALL)
            
            # Strip tags and clean
            text = strip_tags(main_content)
            text = clean_text(text)
            
            # Limit text length
            max_length = 10000
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            result["text"] = text
            result["content"] = main_content[:5000]  # Keep some HTML for reference
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        
        if desc_match:
            result["description"] = desc_match.group(1)
        
        return result
        
    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP Error {e.code}: {e.reason}"
        return result
    except urllib.error.URLError as e:
        result["error"] = f"URL Error: {str(e.reason)}"
        return result
    except Exception as e:
        result["error"] = f"Error: {type(e).__name__}: {str(e)}"
        return result


def main():
    parser = argparse.ArgumentParser(description="Fetch URL content (no API key required)")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--timeout", "-t", type=int, default=30,
                        help="Request timeout in seconds (default: 30)")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="json",
                        help="Output format (default: json)")
    
    args = parser.parse_args()
    
    # Fetch content
    result = fetch_url(args.url, args.timeout)
    
    # Output
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("error"):
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        if result.get("title"):
            print(f"Title: {result['title']}\n")
        print(result.get("text", ""))
    
    # Return error code if failed
    if result.get("error") and not result.get("text"):
        sys.exit(1)


if __name__ == "__main__":
    main()
