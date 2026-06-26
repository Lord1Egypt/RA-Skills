import os
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, Any

def fetch_diffbot(url: str) -> Dict[str, Any]:
    """
    Fetch and extract article content using Diffbot API.
    """
    api_key = os.environ.get("DIFFBOT_API_KEY")
    if not api_key:
        print("Error: DIFFBOT_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # Prepare the API request URL
    base_url = "https://api.diffbot.com/v3/article"
    params = {
        "token": api_key,
        "url": url
    }
    query_string = urllib.parse.urlencode(params)
    request_url = f"{base_url}?{query_string}"

    try:
        req = urllib.request.Request(request_url)
        # Add a standard user agent just in case
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if "error" in data:
                print(f"Diffbot API Error: {data['error']}", file=sys.stderr)
                sys.exit(1)
                
            objects = data.get("objects", [])
            if not objects:
                print("Error: No objects returned from Diffbot API.", file=sys.stderr)
                sys.exit(1)
                
            # Extract title and text
            title = objects[0].get("title")
            if not title:
                print(f"Error: No title found in response. Raw data: {json.dumps(data)[:200]}...", file=sys.stderr)
                sys.exit(1)
                
            # Combine text from all objects if there are multiple
            texts = [obj.get("text", "") for obj in objects if obj.get("text")]
            combined_text = "\n\n".join(texts)
            
            return {
                "title": title,
                "text": combined_text,
                "author": objects[0].get("author", ""),
                "date": objects[0].get("date", ""),
                "siteName": objects[0].get("siteName", "")
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching from Diffbot: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    
    # Fix encoding for Windows console output
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        
    result = fetch_diffbot(url)
    
    # Format output as Markdown
    print(f"# {result['title']}\n")
    
    meta = []
    if result['author']:
        meta.append(f"**Author:** {result['author']}")
    if result['date']:
        meta.append(f"**Date:** {result['date']}")
    if result['siteName']:
        meta.append(f"**Site:** {result['siteName']}")
        
    if meta:
        print(" | ".join(meta) + "\n")
        
    print("---\n")
    print(result['text'])

if __name__ == "__main__":
    main()
