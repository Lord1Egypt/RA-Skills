#!/usr/bin/env python3
import sys, re, requests
url = sys.argv[1] if len(sys.argv) > 1 else ""
if not url:
    print("Usage: sitemap_extractor.py https://example.com/sitemap.xml")
    sys.exit(1)
txt = requests.get(url, timeout=20).text
for loc in re.findall(r"<loc>(.*?)</loc>", txt):
    print(loc)
