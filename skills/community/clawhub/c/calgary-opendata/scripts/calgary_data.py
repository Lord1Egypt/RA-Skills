#!/usr/bin/env python3
"""
City of Calgary Open Data — CLI for the Socrata SODA API.
No dependencies beyond stdlib. Accesses data.calgary.ca.

Usage:
  python3 calgary_data.py <command> [args]

Commands:
  search <query>                              Search datasets by keyword
  list [--category <cat>]                     List datasets, optional category filter
  info <dataset-id>                           Show dataset metadata
  fetch <dataset-id> [options]                Fetch data rows
  categories                                  List all categories
  popular                                     Show most-viewed datasets
  geojson <dataset-id> [--limit N]            Export geocoded data as GeoJSON
"""

import json
import sys
import os
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

BASE_URL = "https://data.calgary.ca"
APP_TOKEN = os.environ.get("SOCRATA_APP_TOKEN", "")  # Optional: reduces rate limits

def api_request(path, params=None):
    """Make a request to the Socrata API."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    if APP_TOKEN:
        req.add_header("X-App-Token", APP_TOKEN)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error: HTTP {e.code} — {body[:200]}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")
        sys.exit(1)

def load_all_datasets():
    """Fetch the full dataset catalogue (cached locally for 1 hour)."""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "catalog_cache.json")
    
    # Check cache age
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < 3600:
            return json.loads(open(cache_file).read())
    
    data = api_request("/api/views.json")
    with open(cache_file, "w") as f:
        json.dump(data, f)
    return data

# --- Commands ---

def cmd_search(query):
    """Search datasets by name or description."""
    datasets = load_all_datasets()
    query_lower = query.lower()
    matches = []
    for d in datasets:
        name = d.get("name", "")
        desc = d.get("description", "") or ""
        cat = d.get("category", "Uncategorized")
        if query_lower in name.lower() or query_lower in desc.lower():
            matches.append((name, d.get("id", ""), cat))
    
    if not matches:
        print(f"No datasets found matching '{query}'.")
        return
    
    print(f"\n🔍 Search results for '{query}' — {len(matches)} found\n")
    for name, did, cat in matches:
        print(f"  • {name}")
        print(f"    ID: {did} | Category: {cat}")
        print(f"    {BASE_URL}/d/{did}")
    print()

def cmd_list(category=None):
    """List datasets, optionally filtered by category."""
    datasets = load_all_datasets()
    if category:
        cat_lower = category.lower()
        datasets = [d for d in datasets if cat_lower in (d.get("category", "") or "").lower()]
    
    print(f"\n📁 Datasets ({'category: ' + category if category else 'all'}) — {len(datasets)} total\n")
    for d in sorted(datasets, key=lambda x: x.get("name", "")):
        name = d.get("name", "N/A")
        did = d.get("id", "")
        cat = d.get("category", "Uncategorized")
        print(f"  • [{cat}] {name} — {did}")
    print()

def cmd_info(dataset_id):
    """Show metadata for a dataset."""
    data = api_request(f"/api/views/{dataset_id}.json")
    
    print(f"\n📊 Dataset: {data.get('name', 'N/A')}")
    print(f"   ID: {dataset_id}")
    print(f"   Category: {data.get('category', 'N/A')}")
    print(f"   Description: {(data.get('description') or 'N/A')[:300]}")
    print(f"   Rows: {data.get('metadata', {}).get('row_count', 'N/A')}")
    print(f"   Created: {data.get('createdAt', 'N/A')}")
    print(f"   Updated: {data.get('rowsUpdatedAt', 'N/A')}")
    print(f"   URL: {BASE_URL}/d/{dataset_id}")
    
    cols = data.get("columns", [])
    if cols:
        print(f"\n   Columns ({len(cols)}):")
        for c in cols:
            name = c.get("name", "?")
            dtype = c.get("dataTypeName", "?")
            desc = (c.get("description") or "")[:80]
            print(f"     • {name} ({dtype}){' — ' + desc if desc else ''}")
    print()

def cmd_fetch(dataset_id, options):
    """Fetch data rows from a dataset."""
    params = {}
    if options.get("limit"):
        params["$limit"] = options["limit"]
    if options.get("offset"):
        params["$offset"] = options["offset"]
    if options.get("where"):
        params["$where"] = options["where"]
    if options.get("select"):
        params["$select"] = options["select"]
    if options.get("order"):
        params["$order"] = options["order"]
    
    # Default limit
    if "$limit" not in params:
        params["$limit"] = 10
    
    data = api_request(f"/resource/{dataset_id}.json", params)
    
    if options.get("csv"):
        # CSV output
        if not data:
            print("No data returned.")
            return
        keys = list(data[0].keys())
        print(",".join(keys))
        for row in data:
            vals = [str(row.get(k, "")).replace(",", ";") for k in keys]
            print(",".join(vals))
    else:
        print(json.dumps(data, indent=2, default=str))

def cmd_categories():
    """List all categories with dataset counts."""
    datasets = load_all_datasets()
    cats = {}
    for d in datasets:
        cat = d.get("category") or "Uncategorized"
        cats[cat] = cats.get(cat, 0) + 1
    
    print(f"\n📂 Categories ({len(cats)})\n")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  • {cat}: {count} datasets")
    print()

def cmd_popular():
    """Show most-viewed datasets."""
    datasets = load_all_datasets()
    # Sort by download count if available
    scored = []
    for d in datasets:
        views = d.get("viewCount", 0)
        name = d.get("name", "")
        did = d.get("id", "")
        cat = d.get("category", "Uncategorized")
        scored.append((views, name, did, cat))
    
    scored.sort(reverse=True)
    print(f"\n🔥 Most Popular Datasets\n")
    for views, name, did, cat in scored[:20]:
        print(f"  • {name} ({views:,} views)")
        print(f"    ID: {did} | Category: {cat}")
    print()

def cmd_geojson(dataset_id, options):
    """Export geocoded data as GeoJSON."""
    params = {"$limit": options.get("limit", 100)}
    data = api_request(f"/resource/{dataset_id}.json", params)
    
    if not data:
        print("No data returned.")
        return
    
    # Find lat/lon columns
    sample = data[0]
    lat_col = lon_col = None
    for key in sample:
        kl = key.lower()
        if kl in ("latitude", "lat", ":latitude"):
            lat_col = key
        elif kl in ("longitude", "lon", "long", ":longitude"):
            lon_col = key
    
    # Also check for :computed_region or location fields
    if not lat_col:
        for key in sample:
            if "latitude" in key.lower():
                lat_col = key
            if "longitude" in key.lower():
                lon_col = key
    
    if not lat_col or not lon_col:
        # Try point/location field
        for key in sample:
            val = sample[key]
            if isinstance(val, dict) and "latitude" in val:
                lat_col = key + ".latitude"
                lon_col = key + ".longitude"
    
    if not lat_col or not lon_col:
        print(f"Error: No lat/lon columns found. Available: {list(sample.keys())}")
        sys.exit(1)
    
    features = []
    for row in data:
        # Handle nested location objects
        if "." in lat_col:
            parts_l = lat_col.split(".")
            parts_lo = lon_col.split(".")
            lat = row.get(parts_l[0], {}).get(parts_l[1]) if isinstance(row.get(parts_l[0]), dict) else None
            lon = row.get(parts_lo[0], {}).get(parts_lo[1]) if isinstance(row.get(parts_lo[0]), dict) else None
        else:
            lat = row.get(lat_col)
            lon = row.get(lon_col)
        
        if lat and lon:
            try:
                props = {k: v for k, v in row.items() if k not in (lat_col, lon_col, ":@computed_region_")}
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(lon), float(lat)]
                    },
                    "properties": props
                })
            except (ValueError, TypeError):
                continue
    
    geojson = {"type": "FeatureCollection", "features": features}
    print(json.dumps(geojson, indent=2, default=str))
    print(f"\n// {len(features)} features with coordinates", file=sys.stderr)

# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "search" and len(sys.argv) >= 3:
        cmd_search(" ".join(sys.argv[2:]))
    elif cmd == "list":
        cat = None
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--category" and i + 1 < len(args):
                cat = args[i + 1]; i += 2
            else:
                i += 1
        cmd_list(cat)
    elif cmd == "info" and len(sys.argv) >= 3:
        cmd_info(sys.argv[2])
    elif cmd == "fetch" and len(sys.argv) >= 3:
        dataset_id = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--limit" and i + 1 < len(args):
                options["limit"] = args[i + 1]; i += 2
            elif args[i] == "--offset" and i + 1 < len(args):
                options["offset"] = args[i + 1]; i += 2
            elif args[i] == "--where" and i + 1 < len(args):
                options["where"] = args[i + 1]; i += 2
            elif args[i] == "--select" and i + 1 < len(args):
                options["select"] = args[i + 1]; i += 2
            elif args[i] == "--order" and i + 1 < len(args):
                options["order"] = args[i + 1]; i += 2
            elif args[i] == "--csv":
                options["csv"] = True; i += 1
            elif args[i] == "--json":
                options["csv"] = False; i += 1
            else:
                i += 1
        cmd_fetch(dataset_id, options)
    elif cmd == "categories":
        cmd_categories()
    elif cmd == "popular":
        cmd_popular()
    elif cmd == "geojson" and len(sys.argv) >= 3:
        dataset_id = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--limit" and i + 1 < len(args):
                options["limit"] = int(args[i + 1]); i += 2
            else:
                i += 1
        cmd_geojson(dataset_id, options)
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
