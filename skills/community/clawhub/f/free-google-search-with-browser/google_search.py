import sys
import json
import urllib.parse
from typing import List, Dict, Any

_import_error = None
try:
    from scrapling.fetchers import StealthyFetcher
except Exception as e:
    # Allow import for testing purposes if dependencies are missing, 
    # but actual usage will fail.
    StealthyFetcher = None
    _import_error = e

def google_search(query: str) -> List[Dict[str, str]]:
    """
    Search Google for the given query and return a list of structured results.
    
    Args:
        query: The search query string.
        
    Returns:
        A list of dictionaries containing 'title', 'link', and 'snippet'.
        
    Raises:
        ImportError: If scrapling or its dependencies are not installed.
        Exception: If the network request fails.
    """
    if StealthyFetcher is None:
        raise ImportError(
            f"The 'scrapling' library or its dependencies are missing. Error: {_import_error}\n"
            "Please ensure all requirements are installed: pip install -r requirements.txt\n"
            "You may also need to install browser binaries: playwright install"
        )

    # Enable adaptive mode for stealthy fetching
    StealthyFetcher.adaptive = True
    # Configure storage to use a local file instead of system directory
    StealthyFetcher.configure(storage_args={"storage_file": "scrapling_storage.db"})
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    # Fetch the page using StealthyFetcher class method
    # headless=True for automation, network_idle=True to wait for page load
    # User requested headless=False to avoid loading issues
    try:
        page = StealthyFetcher.fetch(url, headless=False, network_idle=True, solve_cloudflare=True)
    except Exception as e:
        sys.stderr.write(f"Error fetching Google search results: {e}\n")
        raise e
    
    results = []
    
    # Parse results
    # Strategy: Find all <h3> elements (titles), then find their parent <a> tag for link.
    h3_elements = page.css('h3')
    
    for h3 in h3_elements:
        try:
            title = h3.text.strip()
            if not title:
                continue
                
            # Find parent 'a' tag (usually direct parent or grandparent)
            link_element = h3.xpath('ancestor::a[1]')
            if not link_element:
                continue
                
            link = link_element[0].attrib.get('href')
            if not link:
                continue
                
            # Skip internal Google links or malformed links
            if link.startswith('/search') or not link.startswith('http'):
                continue

            # Try to find snippet
            # We look for the main result container (often a 'div.g' wrapper)
            container = link_element[0].xpath('ancestor::div[contains(@class, "g") or contains(@class, "MjjYud")]')
            snippet = ""
            
            if container:
                # Get text content
                if hasattr(container[0], 'text_content'):
                    full_text = container[0].text_content()
                else:
                    full_text = container[0].text
                
                # Remove title and url from text to get snippet approximation
                snippet = full_text.replace(title, "").replace(link, "").strip()
                # Clean up whitespace
                snippet = " ".join(snippet.split())
            
            # Fallback: look for 'notranslate' class nearby if snippet is empty
            if not snippet:
                snippet_el = link_element[0].xpath('following::div[contains(@class, "notranslate")][1]')
                if snippet_el:
                    snippet = snippet_el[0].text.strip()

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet[:300] + "..." if len(snippet) > 300 else snippet
            })
            
        except Exception:
            # Skip this result if parsing fails
            continue
            
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default query for testing if none provided
        query = "test"
    else:
        query = " ".join(sys.argv[1:])
    
    try:
        data = google_search(query)
        # Output as JSON
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except ImportError as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
