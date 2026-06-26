#!/usr/bin/env python3
"""
parse_rss.py - Parse RSS/Atom feed from stdin and print matching articles.
Usage: curl -sL <feed_url> | python3 parse_rss.py [keyword] [cutoff_timestamp]
"""

import sys
import re
from html import unescape
from email.utils import parsedate_to_datetime
from datetime import datetime

keyword = sys.argv[1].lower() if len(sys.argv) > 1 else ""
cutoff = int(sys.argv[2]) if len(sys.argv) > 2 else 0

content = sys.stdin.read()

# Detect format: RSS <item> or Atom <entry>
items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
is_atom = False
if not items:
    items = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
    is_atom = True

count = 0
for item in items:
    # Title
    title_m = re.search(r'<title[^>]*><!\[CDATA\[(.*?)\]\]></title>|<title[^>]*>(.*?)</title>', item, re.DOTALL)
    title = unescape((title_m.group(1) or title_m.group(2) or '').strip()) if title_m else ''
    if not title:
        continue

    # Link
    if is_atom:
        link_m = re.search(r'<link[^>]+href=["\']([^"\']+)["\']|<id>(https?://[^<]+)</id>', item)
    else:
        link_m = re.search(r'<link>(https?://[^<]+)</link>|<guid[^>]*>(https?://[^<]+)</guid>', item, re.DOTALL)
    link = next((g for g in link_m.groups() if g), '').strip() if link_m else ''

    # Date
    if is_atom:
        date_m = re.search(r'<updated>(.*?)</updated>|<published>(.*?)</published>', item)
    else:
        date_m = re.search(r'<pubDate>(.*?)</pubDate>', item)
    date_str = next((g for g in date_m.groups() if g), '').strip() if date_m else ''

    # Time filter
    if date_str and cutoff:
        try:
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                dt = parsedate_to_datetime(date_str)
            if int(dt.timestamp()) < cutoff:
                continue
        except Exception:
            pass

    # Keyword filter
    if keyword and keyword not in title.lower():
        continue

    print(f"• {title}")
    if link:
        print(f"  {link}")
    count += 1
    if count >= 5:
        break

if count == 0:
    print("(no recent articles)")
