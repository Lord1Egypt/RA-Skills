#!/usr/bin/env python3
"""Product Search — enrich launch items with DuckDuckGo search results."""

import json, os, sys, time, re, urllib.request, urllib.parse
from html import unescape

DDG_URL = "https://html.duckduckgo.com/html/"
USER_AGENT = "Mozilla/5.0 (compatible; AILaunchSearch/1.0)"
TIMEOUT = 10
DATA_DIR = os.environ.get("PIPELINE_DATA_DIR", "data")


def search(query: str, top_k: int = 3) -> list:
    data = urllib.parse.urlencode({"q": query}).encode()
    req = urllib.request.Request(DDG_URL, data=data, headers={
        "User-Agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        results = []
        for m in re.finditer(r'class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]+)</a>', html):
            if len(results) >= top_k:
                break
            href, title = m.group(1), unescape(m.group(2).strip())
            url = href
            uddg = re.search(r'uddg=([^&]+)', href)
            if uddg:
                url = urllib.parse.unquote(uddg.group(1))
            results.append({"title": title, "url": url})
        return results
    except Exception as e:
        print(f"    Search error: {e}", file=sys.stderr)
        return []


def run(launches: list) -> list:
    """Enrich each launch item with search results."""
    enriched = []
    for i, item in enumerate(launches):
        name = item.get("title", "").split("|")[0].split("—")[0].strip()
        print(f"  [{i+1}/{len(launches)}] Searching: {name[:60]}")
        results = search(f"{name} AI product launch details pricing")
        item["search_results"] = results
        item["search_collected_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        enriched.append(item)
        time.sleep(1)  # rate limit

    out_path = os.path.join(DATA_DIR, "enriched_launches.json")
    with open(out_path, "w") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)
    print(f"  Saved {len(enriched)} enriched items → {out_path}")
    return enriched


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=os.path.join(DATA_DIR, "raw_launches.json"))
    args = p.parse_args()
    with open(args.input) as f:
        launches = json.load(f)
    run(launches)
