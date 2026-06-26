#!/usr/bin/env python3
"""
X (Twitter) Scraper using Playwright with cookies
Bypasses API rate limits by using browser automation
"""

import json
import sys
import asyncio
from playwright.async_api import async_playwright

COOKIES_PATH = "/root/cookies_fixed.json"


async def search_x(query: str, limit: int = 10):
    """Search X/Twitter using browser automation"""
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Load cookies
        try:
            with open(COOKIES_PATH, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print(f"✅ Loaded {len(cookies)} cookies", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Failed to load cookies: {e}", file=sys.stderr)
        
        page = await context.new_page()
        
        # Navigate to X search
        search_url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
        print(f"🔍 Searching: {query}", file=sys.stderr)
        
        try:
            await page.goto(search_url, wait_until='domcontentloaded', timeout=20000)
        except Exception as e:
            print(f"⚠️ Navigation warning: {e}", file=sys.stderr)
        
        await asyncio.sleep(5)  # Wait for content to load
        
        # Extract tweets
        tweets = await page.evaluate('''() => {
            const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
            const results = [];
            
            tweetElements.forEach((tweet, index) => {
                if (index >= 10) return; // Limit results
                
                const textEl = tweet.querySelector('div[data-testid="tweetText"]');
                const text = textEl ? textEl.innerText : '';
                
                const userEl = tweet.querySelector('div[data-testid="User-Name"] a');
                const username = userEl ? userEl.getAttribute('href').replace('/', '') : '';
                
                const timeEl = tweet.querySelector('time');
                const timestamp = timeEl ? timeEl.getAttribute('datetime') : '';
                
                if (text) {
                    results.push({
                        text: text,
                        username: username,
                        timestamp: timestamp
                    });
                }
            });
            
            return results;
        }''')
        
        await browser.close()
        
        return {
            'query': query,
            'count': len(tweets),
            'tweets': tweets
        }


async def get_user_tweets(username: str, limit: int = 10):
    """Get tweets from a specific user"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        # Load cookies
        try:
            with open(COOKIES_PATH, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
        except Exception as e:
            print(f"⚠️ Failed to load cookies: {e}", file=sys.stderr)
        
        page = await context.new_page()
        
        profile_url = f"https://twitter.com/{username.lstrip('@')}"
        print(f"👤 Fetching profile: @{username}", file=sys.stderr)
        
        await page.goto(profile_url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        tweets = await page.evaluate('''() => {
            const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
            const results = [];
            
            tweetElements.forEach((tweet, index) => {
                if (index >= 10) return;
                
                const textEl = tweet.querySelector('div[data-testid="tweetText"]');
                const text = textEl ? textEl.innerText : '';
                
                const timeEl = tweet.querySelector('time');
                const timestamp = timeEl ? timeEl.getAttribute('datetime') : '';
                
                if (text) {
                    results.push({text, timestamp});
                }
            });
            
            return results;
        }''')
        
        await browser.close()
        
        return {
            'username': username,
            'count': len(tweets),
            'tweets': tweets
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_x_playwright.py <command> [args...]")
        print("Commands:")
        print("  search <query> [limit]   - Search tweets")
        print("  user <username> [limit]  - Get user tweets")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'search':
        if len(sys.argv) < 3:
            print("Usage: fetch_x_playwright.py search <query> [limit]")
            sys.exit(1)
        query = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = asyncio.run(search_x(query, limit))
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == 'user':
        if len(sys.argv) < 3:
            print("Usage: fetch_x_playwright.py user <username> [limit]")
            sys.exit(1)
        username = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = asyncio.run(get_user_tweets(username, limit))
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
