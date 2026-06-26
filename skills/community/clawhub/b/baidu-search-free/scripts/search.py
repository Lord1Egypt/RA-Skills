#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import requests
import time
import re
from urllib.parse import quote, urlparse, parse_qs
from bs4 import BeautifulSoup


# Baidu anti-scraping retry config
MAX_RETRIES = 3
RETRY_DELAY = 2
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# Additional headers to mimic real browser
ADDITIONAL_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="125", "Chromium";v="125"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}


def resolve_baidu_redirect(baidu_link):
    """
    Resolve Baidu redirect link to get real destination URL.
    Returns the actual destination URL by following the redirect.
    Note: Baidu redirect URLs are preserved because following redirects often hits anti-bot pages.
    The redirect URLs work in browsers, but we also extract the actual URL from the redirect.
    """
    # Ensure full URL format for compatibility
    if baidu_link.startswith('/link'):
        baidu_link = f"https://www.baidu.com{baidu_link}"
    
    # Extract real URL from Baidu redirect if present
    # Baidu redirect format: https://www.baidu.com/link?url=XXX&wd=XXX
    if 'url=' in baidu_link:
        from urllib.parse import unquote
        try:
            parsed = urlparse(baidu_link)
            params = parse_qs(parsed.query)
            if 'url' in params and params['url']:
                return params['url'][0]
        except Exception:
            pass
    
    return baidu_link


def baidu_search(query, count=10, freshness=None):
    """
    Free Baidu web search, no API key required
    :param query: Search keywords
    :param count: Number of results to return, max 50
    :param freshness: Time range filter: pd(past day), pw(past week), pm(past month), py(past year), or YYYY-MM-DDtoYYYY-MM-DD
    """
    headers = {
        "User-Agent": USER_AGENT,
        **ADDITIONAL_HEADERS
    }
    
    # Build request parameters
    params = {
        "wd": query,
        "rn": min(count, 50),
        "ie": "utf-8",
        "cl": 3,
        "tn": "baiduadv"
    }
    
    # Handle time range filter
    if freshness:
        if freshness == "pd":
            params["gpc"] = "stf=" + str(int(time.time()) - 86400) + "," + str(int(time.time())) + "|stftype=1"
        elif freshness == "pw":
            params["gpc"] = "stf=" + str(int(time.time()) - 86400 * 7) + "," + str(int(time.time())) + "|stftype=1"
        elif freshness == "pm":
            params["gpc"] = "stf=" + str(int(time.time()) - 86400 * 30) + "," + str(int(time.time())) + "|stftype=1"
        elif freshness == "py":
            params["gpc"] = "stf=" + str(int(time.time()) - 86400 * 365) + "," + str(int(time.time())) + "|stftype=1"
        elif "to" in freshness:
            try:
                start_str, end_str = freshness.split("to")
                start_str = start_str.strip()
                end_str = end_str.strip()
                start_ts = int(time.mktime(time.strptime(start_str, "%Y-%m-%d")))
                end_ts = int(time.mktime(time.strptime(end_str, "%Y-%m-%d"))) + 86400
                params["gpc"] = f"stf={start_ts},{end_ts}|stftype=1"
            except ValueError as e:
                print(f"Warning: Invalid date format in freshness parameter: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Error parsing freshness dates: {e}", file=sys.stderr)
    
    # Retry mechanism
    for retry in range(MAX_RETRIES):
        try:
            resp = requests.get("https://www.baidu.com/s", params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            
            # Detect anti-scraping verification
            if "验证码" in resp.text or "安全验证" in resp.text or "timeout" in resp.text or resp.status_code != 200:
                if retry < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                raise RuntimeError("Baidu anti-scraping verification triggered, please try again later")
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []
            items = soup.select('.result') + soup.select('.c-container')
            max_results = min(params.get("rn", count), len(items))
            items = items[:max_results]
            
            for item in items:
                try:
                    # Get title
                    title_tag = item.select_one('h3') or item.select_one('.t a')
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    
                    # Get URL
                    url_tag = item.select_one('a[href]')
                    if not url_tag:
                        continue
                    baidu_link = url_tag['href']
                    real_url = resolve_baidu_redirect(baidu_link)
                    
                    # Get snippet
                    summary = ""
                    # Try multiple snippet selectors
                    for selector in ['.c-abstract', '.c-gap-top-small', '.content-right_8Zs40', '.op-stock-detail-sum', '.c-span-last']:
                        sum_tag = item.select_one(selector)
                        if sum_tag:
                            summary = sum_tag.get_text(strip=True)
                            break
                    if not summary:
                        # Fallback: extract all text
                        text = item.get_text(strip=True).replace(title, '').strip()
                        if len(text) > 20:
                            summary = text[:300] + "..."
                    
                    # Get publish time
                    time_str = ""
                    time_tag = item.select_one('.c-showurl') or item.select_one('.c-result-date')
                    if time_tag:
                        time_text = time_tag.get_text(strip=True)
                        time_match = re.search(r'(\d+天前|\d+小时前|\d+分钟前|\d{4}-\d{2}-\d{2})', time_text)
                        if time_match:
                            time_str = time_match.group(1)
                    
                    results.append({
                        "title": title,
                        "url": real_url,
                        "snippet": summary,
                        "time": time_str
                    })
                    
                except Exception as e:
                    # Log but continue processing other results
                    print(f"Warning: Failed to parse result item: {e}", file=sys.stderr)
                    continue
            return results
        
        except Exception as e:
            if retry < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            raise RuntimeError(f"Search failed: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py '{\"query\": \"keywords\", \"count\": 10, \"freshness\": \"pd/pw/pm/py/YYYY-MM-DDtoYYYY-MM-DD\"}'")
        sys.exit(1)
    
    try:
        params = json.loads(sys.argv[1])
        query = params.get('query')
        count = params.get('count', 10)
        freshness = params.get('freshness')
        
        if not query:
            print("Error: query parameter is required")
            sys.exit(1)
        
        results = baidu_search(query, count, freshness)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
