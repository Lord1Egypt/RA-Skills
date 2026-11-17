#!/usr/bin/env python3
"""
cn_names.py - Fetch and cache Chinese game names from Steam API
Usage:
  python3 cn_names.py update    - Fetch CN names for all Steam games (with cache)
  python3 cn_names.py lookup <english_name>  - Look up CN name
  python3 cn_names.py export    - Export all CN names as JSON
"""

import json, sys, os, time, urllib.request

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "cn_names_cache.json")

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def fetch_steam_library():
    """Get Steam library via CLI"""
    import subprocess
    result = subprocess.run(
        ["steam", "library", "--limit", "500", "--json"],
        capture_output=True, text=True, timeout=120
    )
    return json.loads(result.stdout)

def fetch_cn_name(appid):
    """Fetch Chinese name from Steam API for a single app"""
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=cn&l=schinese"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            app_data = data.get(str(appid), {})
            if app_data.get("success"):
                return app_data["data"]["name"]
    except:
        pass
    return None

def cmd_update():
    """Update CN names cache for all Steam games"""
    cache = load_cache()
    games = fetch_steam_library()
    
    total = len(games)
    updated = 0
    skipped = 0
    new_cn = 0
    
    print(f"Fetching CN names for {total} games...")
    
    for i, g in enumerate(games):
        appid = g.get("appId", "")
        name = g.get("name", "").strip()
        if not appid:
            continue
        
        # Skip if already cached
        cache_key = str(appid)
        if cache_key in cache:
            skipped += 1
            continue
        
        cn_name = fetch_cn_name(appid)
        if cn_name and cn_name != name:
            cache[cache_key] = {"en": name, "cn": cn_name, "appid": appid}
            new_cn += 1
            print(f"  [{i+1}/{total}] ✅ {name} → {cn_name}")
        else:
            cache[cache_key] = {"en": name, "cn": name, "appid": appid}
        
        updated += 1
        # Rate limit: Steam allows ~200 requests/5min
        time.sleep(1.5)
    
    save_cache(cache)
    print(f"\nDone! Updated: {updated}, Skipped (cached): {skipped}, New CN names: {new_cn}")
    print(f"Cache: {CACHE_FILE}")

def cmd_lookup(english_name):
    """Look up CN name by English name"""
    cache = load_cache()
    en_lower = english_name.lower().strip()
    
    for appid, info in cache.items():
        if info["en"].lower().strip() == en_lower:
            if info["cn"] != info["en"]:
                print(info["cn"])
            else:
                print(f"(无独立中文名) {info['en']}")
            return
    
    # Not in cache, try Steam API search
    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={urllib.parse.quote(english_name)}&l=schinese&cc=cn"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            if items:
                print(items[0]["name"])
                return
    except:
        pass
    
    print(f"(未找到) {english_name}")

def cmd_export():
    """Export CN names mapping"""
    cache = load_cache()
    # Build name->cn mapping
    mapping = {}
    for appid, info in cache.items():
        if info["cn"] != info["en"]:
            mapping[info["en"]] = info["cn"]
    print(json.dumps(mapping, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    if cmd == "update":
        cmd_update()
    elif cmd == "lookup":
        if len(sys.argv) < 3:
            print("Usage: cn_names.py lookup <english_name>")
            sys.exit(1)
        cmd_lookup(sys.argv[2])
    elif cmd == "export":
        cmd_export()
    else:
        print(__doc__)
