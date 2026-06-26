#!/usr/bin/env python3
"""
Google AI Mode CLI - Unofficial Google AI Mode Search Tool
⚠️  Use at your own risk. Not affiliated with Google.
📝 MIT License - See LICENSE file

Features:
- CDP mode: Connect to Chrome with debug port (recommended)
- Cookie mode: Use saved cookies (fallback)
"""

import argparse
import json
import os
import sys
import subprocess
import time
from pathlib import Path

COOKIE_FILE = Path.home() / ".config" / "gaimode" / "cookies.json"
COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)

def print_status(msg, status="INFO"):
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌"}
    print(f"{icons.get(status, '•')} {msg}")

def is_cdp_running():
    """Check if Chrome CDP is running on port 9222"""
    try:
        result = subprocess.run(['curl', '-s', '--max-time', '3', 'http://localhost:9222/json/version'], 
                               capture_output=True, text=True)
        return 'Chrome' in result.stdout
    except:
        return False

def get_cdp_ws_url():
    """Get WebSocket URL from Chrome CDP"""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:9222/json/version'], 
                               capture_output=True, text=True)
        data = json.loads(result.stdout)
        return data.get('webSocketDebuggerUrl')
    except:
        return None

def check_cookies():
    """Check if cookies file exists and is valid"""
    if not COOKIE_FILE.exists():
        return False
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
        return len(cookies) > 0
    except:
        return False

def fix_cookies():
    """Fix cookies for Playwright compatibility"""
    if not check_cookies():
        return []
    
    with open(COOKIE_FILE, 'r') as f:
        cookies = json.load(f)
    
    fixed = []
    for c in cookies:
        ss = c.get('sameSite', '')
        if ss not in ('Strict', 'Lax', 'None'):
            c['sameSite'] = 'Lax'
        c.pop('storeId', None)
        c.pop('id', None)
        fixed.append(c)
    
    return fixed

def cmd_cdp():
    """Guide user to start Chrome CDP"""
    print_status("Chrome CDP Mode Setup", "INFO")
    print()
    print("Chrome CDP (Chrome DevTools Protocol) connects directly to your")
    print("running Chrome browser - more reliable, less likely to be blocked!")
    print()
    print("Steps:")
    print("  1. Run: bash ~/start-chrome-cdp.sh")
    print("  2. Keep that Chrome window open")
    print("  3. Use 'gaimode search' normally")
    print()
    print("Or manually launch Chrome with:")
    print('  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222')

def cmd_status():
    """Check connection status"""
    cdp_ok = is_cdp_running()
    cookies_ok = check_cookies()
    
    print_status("Connection Status", "INFO")
    print()
    
    if cdp_ok:
        print_status("CDP Mode: ✅ Running on :9222", "OK")
    else:
        print_status("CDP Mode: ❌ Not running", "WARN")
        print("  Run: gaimode cdp")
    
    if cookies_ok:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
        import time
        now = time.time()
        expired = sum(1 for c in cookies if c.get('expirationDate', 0) < now)
        valid = len(cookies) - expired
        print_status(f"Cookie Mode: ✅ {valid}/{len(cookies)} valid", "OK" if valid > 0 else "WARN")
    else:
        print_status("Cookie Mode: ❌ No cookies found", "WARN")
    
    print()
    print("Priority: CDP → Cookies (auto-fallback)")

def search_cdp(query):
    """Search via CDP (Chrome browser)"""
    from playwright.sync_api import sync_playwright
    
    ws_url = get_cdp_ws_url()
    if not ws_url:
        return None
    
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        
        url = f"https://www.google.com/search?udm=50&q={query.replace(' ', '+')}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(8000)
        
        content = page.inner_text("body")[:4000]
        browser.disconnect()
        pw.stop()
        
        if "unusual traffic" in content.lower():
            return None
        return content
    except Exception as e:
        return None

def search_cookies(query):
    """Search via saved cookies (fallback)"""
    from playwright.sync_api import sync_playwright
    
    cookies = fix_cookies()
    if not cookies:
        return None
    
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        )
        context.add_cookies(cookies)
        
        page = context.new_page()
        url = f"https://www.google.com/search?udm=50&q={query.replace(' ', '+')}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(8000)
        
        content = page.inner_text("body")[:4000]
        browser.close()
        pw.stop()
        
        if "unusual traffic" in content.lower() or "CAPTCHA" in content:
            return None
        
        return content
    except Exception as e:
        return None

def cmd_search(query):
    """Search using best available method"""
    print_status(f"Searching: {query}", "INFO")
    
    # Try CDP first
    if is_cdp_running():
        print_status("Trying CDP mode...", "INFO")
        result = search_cdp(query)
        if result:
            print_status("CDP mode success!", "OK")
            print()
            print(result[:3500])
            return 0
    
    # Fallback to cookies
    if check_cookies():
        print_status("Trying cookie mode...", "INFO")
        result = search_cookies(query)
        if result:
            print_status("Cookie mode success!", "OK")
            print()
            print(result[:3500])
            return 0
    
    print_status("All methods failed!", "ERROR")
    print()
    print("Options:")
    print("  1. Start CDP: gaimode cdp")
    print("  2. Setup cookies: gaimode login")
    return 1

def main():
    parser = argparse.ArgumentParser(
        description="Google AI Mode CLI - Unofficial Google AI Mode search tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gaimode cdp                       Setup Chrome CDP mode
  gaimode status                    Check connection status
  gaimode search \"IPL score\"         Search Google AI Mode
  gaimode login                     Show cookie setup instructions

⚠️  Use at your own risk. Not affiliated with Google.
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    subparsers.add_parser('cdp', help='Setup Chrome CDP mode')
    subparsers.add_parser('status', help='Check connection status')
    subparsers.add_parser('login', help='Show cookie setup instructions')
    
    search_parser = subparsers.add_parser('search', help='Search Google AI Mode')
    search_parser.add_argument('query', help='Search query', nargs='?')
    search_parser.add_argument('-', dest='stdin', action='store_true', help='Read from stdin')
    
    args = parser.parse_args()
    
    if args.command == 'cdp':
        cmd_cdp()
    elif args.command == 'status':
        cmd_status()
    elif args.command == 'login':
        print_status("Cookie Login Guide", "INFO")
        print()
        print("1. Install EditThisCookie Chrome extension")
        print("2. Go to google.com")
        print("3. Click EditThisCookie → Export")
        print("4. Save to: ~/.config/gaimode/cookies.json")
    elif args.command == 'search':
        query = sys.stdin.read().strip() if args.stdin else (args.query or input("Query: ").strip())
        if not query:
            print("Error: No query", file=sys.stderr)
            return 1
        return cmd_search(query)
    else:
        parser.print_help()
        cmd_status()
        return 0

if __name__ == "__main__":
    sys.exit(main())
