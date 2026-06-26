#!/usr/bin/env python3
"""
Exposure Sentinel - Check if IPs are listed on OpenClaw Exposure Watchboard
"""
import asyncio
import aiohttp
import sys
import argparse
from datetime import datetime

BASE_URL = "https://openclaw.allegro.earth/page/{}/"
TOTAL_PAGES = 3357
CONCURRENT_LIMIT = 50


def get_ip_patterns(ip: str):
    """Generate matching patterns for IP (handling partial masking)"""
    parts = ip.split('.')
    return [
        ip,  # Full IP
        f"{parts[0]}.{parts[1]}.{parts[2]}.",  # First 3 octets
        f"{parts[0]}.{parts[1]}.{parts[2]}•",  # With masking char
    ]


async def fetch_page(session: aiohttp.ClientSession, page_num: int, semaphore: asyncio.Semaphore):
    """Fetch a single page"""
    async with semaphore:
        url = BASE_URL.format(page_num)
        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    return page_num, await response.text()
                return page_num, None
        except Exception as e:
            return page_num, f"ERROR: {e}"


async def search_ip(target_ip: str, verbose: bool = False):
    """Search for a single IP across all pages"""
    found_pages = []
    errors = []
    patterns = get_ip_patterns(target_ip)
    
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, i, semaphore) for i in range(1, TOTAL_PAGES + 1)]
        
        completed = 0
        for coro in asyncio.as_completed(tasks):
            page_num, content = await coro
            completed += 1
            
            if verbose and (completed % 100 == 0 or completed == TOTAL_PAGES):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Checked {completed}/{TOTAL_PAGES} pages...", 
                      file=sys.stderr)
            
            if content is None or content.startswith("ERROR:"):
                errors.append(f"Page {page_num}: {content or 'HTTP error'}")
                continue
            
            for pattern in patterns:
                if pattern in content:
                    found_pages.append(page_num)
                    if verbose:
                        print(f"🎯 Found on page {page_num}!")
                    break
    
    return found_pages, errors


async def search_multiple(ips: list[str], verbose: bool = False):
    """Search for multiple IPs"""
    results = {}
    start_time = datetime.now()
    
    for ip in ips:
        if verbose:
            print(f"\nSearching for {ip}...")
        pages, errors = await search_ip(ip, verbose)
        results[ip] = {"pages": pages, "errors": errors}
    
    duration = (datetime.now() - start_time).total_seconds()
    return results, duration


def main():
    parser = argparse.ArgumentParser(
        description="Check if IPs are exposed on OpenClaw Exposure Watchboard"
    )
    parser.add_argument(
        "ips", 
        nargs="+", 
        help="One or more IP addresses to check"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Show progress"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    # Validate IPs
    for ip in args.ips:
        parts = ip.split('.')
        if len(parts) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            print(f"Invalid IP: {ip}", file=sys.stderr)
            sys.exit(1)
    
    if args.json:
        import json
    else:
        print(f"Searching {TOTAL_PAGES} pages for {len(args.ips)} IP(s)...")
        print("-" * 50)
    
    results, duration = asyncio.run(search_multiple(args.ips, verbose=args.verbose))
    
    if args.json:
        print(json.dumps({
            "duration_seconds": duration,
            "results": results
        }, indent=2))
    else:
        print("\n" + "=" * 50)
        print(f"Search complete in {duration:.2f}s")
        print("-" * 50)
        
        for ip, data in results.items():
            pages = data["pages"]
            if pages:
                print(f"\n⚠️  {ip} EXPOSED on {len(pages)} page(s):")
                for page in sorted(pages):
                    print(f"   → {BASE_URL.format(page)}")
            else:
                print(f"\n✅ {ip} - Not found (safe)")
        
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
