#!/usr/bin/env python3
"""
Batch opening examples for the browser opener skill.
"""

from scripts.open_browser import BrowserOpener
import time

def open_multiple_urls(urls, browser_name="default", delay=1):
    """Open multiple URLs with optional delay between openings."""
    opener = BrowserOpener()
    
    print(f"Opening {len(urls)} URLs with {browser_name}...")
    
    for i, url in enumerate(urls, 1):
        print(f"Opening URL {i}/{len(urls)}: {url}")
        success = opener.open_url(url, browser_name=browser_name)
        
        if success:
            print(f"✓ Successfully opened {url}")
        else:
            print(f"✗ Failed to open {url}")
        
        if i < len(urls):
            print(f"Waiting {delay} second(s) before next URL...")
            time.sleep(delay)

def main():
    # List of URLs to open
    search_urls = [
        "https://www.google.com",
        "https://www.bing.com", 
        "https://www.duckduckgo.com",
        "https://www.yahoo.com"
    ]
    
    news_urls = [
        "https://www.bbc.com",
        "https://www.cnn.com",
        "https://www.reuters.com",
        "https://www.apnews.com"
    ]
    
    # Example 1: Open multiple search engines with default browser
    print("=== Opening Search Engines ===")
    open_multiple_urls(search_urls, browser_name="default", delay=2)
    
    # Example 2: Open news sites with Chrome
    print("\n=== Opening News Sites with Chrome ===")
    open_multiple_urls(news_urls, browser_name="chrome", delay=2)
    
    # Example 3: Open sites with Firefox private mode
    print("\n=== Opening Sites with Firefox Private Mode ===")
    open_multiple_urls(search_urls[:2], browser_name="firefox", incognito=True, delay=2)

if __name__ == "__main__":
    main()