
import sys
import json
import time
from playwright.sync_api import sync_playwright

def fetch_bensbites():
    results = []
    with sync_playwright() as p:
        try:
            # Launch Chromium (headless)
            browser = p.chromium.launch(headless=True)
            
            # Use specific context with real UA
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Go to new Substack homepage
            url = "https://www.bensbites.com/"
            print(f"Navigating to {url}...", file=sys.stderr)
            
            # Use the API endpoint for archive - much more reliable
            api_url = "https://www.bensbites.com/api/v1/archive?sort=new&limit=12"
            print(f"Fetching archive from API: {api_url}", file=sys.stderr)
            
            try:
                page.goto(api_url, timeout=60000)
                # Substack API returns JSON often wrapped in a <pre> or just raw
                content = page.inner_text("body")
                data = json.loads(content)
                
                # Substack API can return a list directly or a dict with 'posts'
                posts = data if isinstance(data, list) else data.get('posts', [])
                
                for post in posts:
                    results.append({
                        "source": "Ben's Bites",
                        "title": post.get('title'),
                        "url": f"https://www.bensbites.com/p/{post.get('slug')}",
                        "time": post.get('post_date', 'Recent').split('T')[0],
                        "summary": post.get('subtitle', 'AI News & Tools'),
                    })
                    if len(results) >= 5: break
            except Exception as e:
                print(f"API Fetch error: {e}. Falling back to DOM scraping...", file=sys.stderr)
                # Fallback to homepage DOM scraping if API fails
                try:
                    page.goto(url, timeout=60000, wait_until="domcontentloaded")
                    page.wait_for_timeout(5000)
                    links = page.query_selector_all('a')
                    seen_urls = set()
                    for link in links:
                        href = link.get_attribute('href')
                        if not href or "/p/" not in href: continue
                        full_url = href if href.startswith("http") else f"https://www.bensbites.com{href}"
                        if full_url in seen_urls: continue
                        seen_urls.add(full_url)
                        
                        title_el = link.query_selector("h1, h2, h3, h4, .post-title")
                        link_text = title_el.inner_text().strip() if title_el else link.inner_text().strip()
                        
                        if len(link_text) > 10:
                            results.append({
                                "source": "Ben's Bites",
                                "title": link_text,
                                "url": full_url,
                                "time": "Recent",
                                "summary": "AI News & Tools",
                            })
                        if len(results) >= 5: break
                except: pass

            if not results:
                results.append({
                    "source": "Ben's Bites",
                    "title": "Ben's Bites (Latest)",
                    "url": url,
                    "time": "Today", 
                    "summary": "Daily AI Digest. Content protected, visit link.",
                })

            browser.close()
            
        except Exception as e:
            # sys.stderr.write(f"Playwright Error: {str(e)}\n")
            # Return a safe fallback instead of failing
            if not results:
                results.append({
                    "source": "Ben's Bites",
                    "title": "Ben's Bites (Visit Site)",
                    "url": "https://bensbites.beehiiv.com/",
                    "time": "Today",
                    "summary": "Unable to fetch content. Please verify on site.",
                })
            try:
                if 'browser' in locals(): browser.close()
            except: pass
            
    print(json.dumps(results, indent=2))
    
if __name__ == "__main__":
    fetch_bensbites()
