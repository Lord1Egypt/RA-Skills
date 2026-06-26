
import sys
import json
import argparse
from playwright.sync_api import sync_playwright

def fetch_content(url):
    results = []
    with sync_playwright() as p:
        try:
            # Launch Chromium (headless)
            # Add args to look more like a real browser
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            # Use specific context with real UA
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Go to the URL
            # Wait until network is idle which might indicate challenge is solved or feed loaded
            response = page.goto(url, timeout=30000, wait_until="networkidle")
            
            # Get content
            content = page.content()
            
            # If it's an RSS feed rendered in browser, it might be wrapped in <pre> or just text
            # Chrome often wraps XML in a style. 
            # Let's try to get innerText of body
            body_text = page.inner_text("body")
            
            # Print raw content for the caller (rss_parser) to handle? 
            # Or if we want to return JSON directly?
            # The caller expects items.
            # But here we are just bypassing the firewall.
            # It's better if this script returns the RAW HTML/XML content to stdout, 
            # and let the python script parse it using the robust rss_parser logic.
            
            print(content)
            
            # Debugging info to stderr
            title = page.title()
            sys.stderr.write(f"Page Title: {title}\n")
            if "Just a moment" in title or "Challenge" in title:
                sys.stderr.write("Cloudflare Challenge Detected! Waiting longer...\n")
                page.wait_for_timeout(10000)
                content = page.content()
                print(content) # Print again after wait? No, let's just update content variable.
            
            browser.close()
            
        except Exception as e:
            sys.stderr.write(f"Playwright Error: {str(e)}\n")
            # Don't exit 1, just let it return empty so we don't crash main script

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to fetch")
    args = parser.parse_args()
    fetch_content(args.url)
