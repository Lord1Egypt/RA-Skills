#!/usr/bin/env bash
# Market News — CNBC + MarketWatch RSS
set -euo pipefail

python3 << 'PYEOF'
import urllib.request, re, html
from xml.etree import ElementTree as ET
from datetime import datetime

def fetch_feed(url, label):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        xml_text = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, [f"(获取失败: {e})"]

    xml_text = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_text)
    try:
        root = ET.fromstring(xml_text)
        items = root.findall(".//item")[:5]
    except:
        return None, ["(解析失败)"]

    results = []
    for item in items:
        title_el = item.find("title")
        date_el = item.find("pubDate")
        title = html.unescape(title_el.text.strip()) if title_el is not None and title_el.text else ""
        date_str = date_el.text if date_el is not None and date_el.text else ""

        if date_str:
            try:
                for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"]:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        date_str = dt.strftime("%m/%d %H:%M")
                        break
                    except: pass
            except: pass

        if title:
            results.append((title, date_str))

    return results, None

sources = [
    ("CNBC", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"),
    ("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories"),
]

print("\n===== 市场要闻 =====\n")

for label, url in sources:
    items, err = fetch_feed(url, label)
    print(f"--- {label} ---")
    if err:
        for e in err:
            print(f"  {e}")
    elif items:
        for title, date_str in items:
            print(f"  • {title}")
            if date_str:
                print(f"    {date_str}")
            print()
    print()

print(f"来源: CNBC + MarketWatch RSS")
print(f"⏰ {datetime.now().strftime('%m/%d %H:%M')}")
PYEOF
