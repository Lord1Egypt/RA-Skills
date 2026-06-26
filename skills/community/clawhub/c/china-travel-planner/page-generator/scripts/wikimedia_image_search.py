#!/usr/bin/env python3
"""
wikimedia_image_search.py - Search Wikimedia Commons for free images by keyword.

Returns thumbnail URLs (1200px wide) suitable for travel pages.
All results are from Wikimedia Commons and carry free licenses (CC, Public Domain, etc).

Usage:
    python3 wikimedia_image_search.py "橘子洲 长沙"
    python3 wikimedia_image_search.py "Yueyang Tower" --limit 3
    python3 wikimedia_image_search.py "Changsha skyline" --width 1600
    python3 wikimedia_image_search.py "岳阳楼" --category "Yueyang Tower"
    python3 wikimedia_image_search.py --category "Orange Isle" --limit 5
    python3 wikimedia_image_search.py --batch landmarks.json --output results.json

Modes:
    1. Keyword search (default): searches file descriptions
    2. Category browse (--category): lists files in a Wikimedia Commons category
    3. Batch mode (--batch): reads a JSON file with {name: query/category} pairs

Output: JSON array of {title, url, thumbUrl, width, height, license, description}
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

API = "https://commons.wikimedia.org/w/api.php"


def api_get(params):
    """Make a GET request to the Wikimedia Commons API."""
    params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "TravelPageBot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"API error: {e}", file=sys.stderr)
        return None


def search_images(query, limit=5, width=1200):
    """Search Wikimedia Commons by keyword, return image info."""
    data = api_get({
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",  # File namespace
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": str(width),
    })
    return _parse_results(data)


def category_images(category, limit=10, width=1200):
    """List images from a Wikimedia Commons category."""
    # Normalize category name
    if not category.startswith("Category:"):
        category = "Category:" + category
    data = api_get({
        "action": "query",
        "generator": "categorymembers",
        "gcmtitle": category,
        "gcmtype": "file",
        "gcmlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": str(width),
    })
    return _parse_results(data)


def _parse_results(data):
    """Parse API response into a clean list of image objects."""
    if not data or "query" not in data:
        return []
    results = []
    for page_id, page in data["query"].get("pages", {}).items():
        if "imageinfo" not in page:
            continue
        info = page["imageinfo"][0]
        ext = info.get("extmetadata", {})

        # Skip non-image files (PDFs, SVGs that are maps, etc)
        url = info.get("url", "")
        if any(url.lower().endswith(x) for x in [".pdf", ".svg", ".ogv", ".webm"]):
            continue

        thumb = info.get("thumburl", url)
        result = {
            "title": page.get("title", "").replace("File:", ""),
            "url": url,
            "thumbUrl": thumb,
            "width": info.get("thumbwidth", info.get("width", 0)),
            "height": info.get("thumbheight", info.get("height", 0)),
            "license": ext.get("LicenseShortName", {}).get("value", "unknown"),
            "description": ext.get("ImageDescription", {}).get("value", ""),
        }
        results.append(result)
    return results


def batch_search(batch_file, width=1200):
    """
    Read a JSON file with search specs, return results for each.
    
    Input format (array of objects):
    [
        {"name": "五一广场", "query": "Changsha Wuyi Square", "category": null},
        {"name": "橘子洲", "query": null, "category": "Orange Isle"},
        {"name": "岳阳楼", "query": "Yueyang Tower Hunan"}
    ]
    
    Output: {name: [results]}
    """
    with open(batch_file, "r", encoding="utf-8") as f:
        specs = json.load(f)
    
    all_results = {}
    for spec in specs:
        name = spec.get("name", "unknown")
        cat = spec.get("category")
        query = spec.get("query")
        limit = spec.get("limit", 5)
        
        if cat:
            results = category_images(cat, limit=limit, width=width)
        elif query:
            results = search_images(query, limit=limit, width=width)
        else:
            results = []
        
        all_results[name] = results
        # Be polite to the API
        import time
        time.sleep(0.5)
    
    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Search Wikimedia Commons for free images"
    )
    parser.add_argument(
        "query", nargs="?", help="Search keywords (e.g. 'Changsha skyline')"
    )
    parser.add_argument(
        "--category", "-c",
        help="Browse a Wikimedia Commons category instead of searching"
    )
    parser.add_argument(
        "--limit", "-n", type=int, default=5,
        help="Number of results (default: 5)"
    )
    parser.add_argument(
        "--width", "-w", type=int, default=1200,
        help="Thumbnail width in pixels (default: 1200)"
    )
    parser.add_argument(
        "--batch", "-b",
        help="Batch mode: JSON file with search specs"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--pretty", action="store_true",
        help="Pretty-print JSON output"
    )
    args = parser.parse_args()

    if args.batch:
        results = batch_search(args.batch, width=args.width)
    elif args.category:
        results = category_images(args.category, limit=args.limit, width=args.width)
    elif args.query:
        results = search_images(args.query, limit=args.limit, width=args.width)
    else:
        parser.print_help()
        sys.exit(1)

    indent = 2 if args.pretty else None
    output = json.dumps(results, ensure_ascii=False, indent=indent)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
