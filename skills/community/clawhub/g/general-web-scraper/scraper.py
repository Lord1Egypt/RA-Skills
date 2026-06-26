#!/usr/bin/env python3
"""通用网页数据抓取工具 — General Web Scraper for AI Agents"""

import requests
import csv
import json
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_links(url, selector="a"):
    """抓取页面中所有匹配CSS选择器的链接"""
    try:
        resp = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for el in soup.select(selector):
            text = el.get_text(strip=True)
            href = el.get('href')
            if href:
                href = urljoin(url, href)
            results.append({"text": text, "href": href})
        return results
    except Exception as e:
        return [{"error": str(e)}]

def scrape_table(url, table_selector="table"):
    """抓取网页表格数据"""
    try:
        resp = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.select_one(table_selector)
        if not table:
            return []
        rows = []
        for tr in table.select('tr'):
            cells = [td.get_text(strip=True) for td in tr.select('td, th')]
            if cells:
                rows.append(cells)
        return rows
    except Exception as e:
        return [{"error": str(e)}]

def save_csv(data, filename="output.csv"):
    """保存为CSV"""
    if not data:
        return "No data to save"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data if isinstance(data[0], list) else [list(d.values()) for d in data])
    return f"Saved {len(data)} rows to {filename}"

def save_json(data, filename="output.json"):
    """保存为JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"Saved {len(data)} items to {filename}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <url> [selector] [--csv|--json]")
        print("  url      - Target webpage URL")
        print("  selector - CSS selector (default: 'a' for links)")
        print("  --csv    - Export as CSV (default)")
        print("  --json   - Export as JSON")
        print("  --table  - Scrape table data instead of links")
        sys.exit(1)
    
    url = sys.argv[1]
    selector = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "a"
    fmt = "--json" if "--json" in sys.argv else "--csv"
    is_table = "--table" in sys.argv
    
    print(f"🌐 Scraping: {url}")
    print(f"🔍 Selector: {selector}")
    
    if is_table:
        data = scrape_table(url, selector)
    else:
        data = scrape_links(url, selector)
    
    print(f"📊 Found {len(data)} items")
    
    if fmt == "--json":
        print(save_json(data))
    else:
        print(save_csv(data))
