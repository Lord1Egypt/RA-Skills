#!/usr/bin/env python3
"""
abs_cache.py — ABS API metadata cache manager

Maintains ~/.cache/abs-data-api/ with a compact catalog of all ABS dataflows
and per-dataset structure/codelist files.

Usage:
    abs_cache.py refresh          # Fetch all dataflows from ABS API
    abs_cache.py search <term>    # Search cached catalog by keyword
    abs_cache.py status           # Show cache status
    abs_cache.py structure <id>   # Fetch and show structure for a dataflow
    abs_cache.py gen-metadata     # Generate metadata.generated.json from presets
"""

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

CACHE_DIR = Path(os.environ.get("ABS_CACHE_DIR", Path.home() / ".cache" / "abs-data-api"))
CATALOG_FILE = CACHE_DIR / "catalog.json"
STRUCTURE_DIR = CACHE_DIR / "structures"
META_GENERATED = CACHE_DIR / "metadata.generated.json"
BASE_URL = "https://data.api.abs.gov.au/rest"
MAX_AGE_HOURS = 24

SKILL_DIR = Path(__file__).parent.parent
PRESETS_FILE = SKILL_DIR / "presets.json"
META_OVERRIDES_FILE = SKILL_DIR / "metadata.overrides.json"


def _request(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def is_fresh() -> bool:
    """Return True if catalog exists and is less than MAX_AGE_HOURS old."""
    if not CATALOG_FILE.exists():
        return False
    age_h = (time.time() - CATALOG_FILE.stat().st_mtime) / 3600
    return age_h < MAX_AGE_HOURS


def refresh() -> dict:
    """Fetch all dataflows from ABS API and save compact catalog."""
    print("Fetching dataflow list from ABS API ...", file=sys.stderr)
    data = _request(f"{BASE_URL}/dataflow/ABS")
    refs = data.get("references", {})
    catalog = {}
    for urn, df in refs.items():
        did = df.get("id", "")
        if not did:
            continue
        catalog[did] = {
            "id": did,
            "version": df.get("version", "1.0.0"),
            "name": df.get("name", ""),
            "description": (df.get("description") or "")[:300],
            "agencyID": df.get("agencyID", "ABS"),
        }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, separators=(",", ":")))
    print(f"Cached {len(catalog)} dataflows → {CATALOG_FILE}", file=sys.stderr)
    return catalog


def load_catalog() -> dict:
    """Load catalog from disk, refreshing if stale."""
    if not is_fresh():
        return refresh()
    return json.loads(CATALOG_FILE.read_text())


def search(term: str, catalog: dict = None, limit: int = 20) -> list:
    """Search catalog by keyword. Returns list of matching dataflow dicts."""
    if catalog is None:
        catalog = load_catalog()
    term_lower = term.lower()
    tokens = term_lower.split()
    results = []
    for did, df in catalog.items():
        haystack = (did + " " + df.get("name", "") + " " + df.get("description", "")).lower()
        score = sum(1 for t in tokens if t in haystack)
        if score > 0:
            results.append((score, df))
    results.sort(key=lambda x: -x[0])
    return [df for _, df in results[:limit]]


def get_structure(dataflow_id: str, version: str = "1.0.0") -> dict:
    """Fetch and cache the DSD (dimensions + codelists) for a dataflow."""
    STRUCTURE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = STRUCTURE_DIR / f"{dataflow_id}.json"
    if cache_file.exists():
        age_h = (time.time() - cache_file.stat().st_mtime) / 3600
        if age_h < MAX_AGE_HOURS * 7:  # structure cache is valid for 7 days
            return json.loads(cache_file.read_text())

    print(f"Fetching structure for {dataflow_id} ...", file=sys.stderr)
    try:
        url = f"{BASE_URL}/datastructure/ABS/{dataflow_id}/{version}?references=codelist"
        data = _request(url)
        cache_file.write_text(json.dumps(data, separators=(",", ":")))
        return data
    except Exception as e:
        print(f"Warning: could not fetch structure: {e}", file=sys.stderr)
        return {}


def load_overrides() -> dict:
    """Load manual metadata overrides from metadata.overrides.json if present."""
    if META_OVERRIDES_FILE.exists():
        try:
            return json.loads(META_OVERRIDES_FILE.read_text())
        except Exception:
            pass
    return {}


def generate_metadata() -> dict:
    """
    Generate metadata.generated.json from presets and catalog.

    Structure:
      {
        "<dataflow_id>": {
          "id": "...",
          "name": "...",
          "version": "...",
          "cat_no": "...",    # from preset notes/search
          "description": "...",
          "preset_count": N,
          "presets": ["preset-name", ...]
        },
        ...
      }
    """
    presets = {}
    if PRESETS_FILE.exists():
        try:
            presets = json.loads(PRESETS_FILE.read_text())
        except Exception:
            pass

    catalog = {}
    if CATALOG_FILE.exists():
        try:
            catalog = json.loads(CATALOG_FILE.read_text())
        except Exception:
            pass

    overrides = load_overrides()

    # Build metadata from presets
    meta = {}
    for preset_name, preset in presets.items():
        did = preset.get("dataflow", "")
        if not did:
            continue
        if did not in meta:
            catalog_entry = catalog.get(did, {})
            meta[did] = {
                "id": did,
                "name": catalog_entry.get("name") or did,
                "version": catalog_entry.get("version", "1.0.0"),
                "cat_no": "",
                "description": catalog_entry.get("description", ""),
                "preset_count": 0,
                "presets": [],
            }
            # Try to extract cat_no from preset note
            note = preset.get("note", "")
            import re
            m = re.search(r"ABS\s+(\d{4}\.\d+)", note)
            if m:
                meta[did]["cat_no"] = m.group(1)

        meta[did]["preset_count"] += 1
        meta[did]["presets"].append(preset_name)

        # Apply preset description/note to parent if better
        if not meta[did]["description"] and preset.get("description"):
            meta[did]["description"] = preset["description"]

    # Apply manual overrides last
    for did, override in overrides.items():
        if did in meta:
            meta[did].update(override)
        else:
            meta[did] = override

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    META_GENERATED.write_text(json.dumps(meta, indent=2))
    print(f"Generated metadata for {len(meta)} dataflows → {META_GENERATED}", file=sys.stderr)
    return meta


def load_metadata() -> dict:
    """Load generated metadata, regenerating if missing or stale."""
    if not META_GENERATED.exists():
        return generate_metadata()
    age_h = (time.time() - META_GENERATED.stat().st_mtime) / 3600
    if age_h > MAX_AGE_HOURS * 7:
        return generate_metadata()
    try:
        return json.loads(META_GENERATED.read_text())
    except Exception:
        return generate_metadata()


def get_dataset_info(dataflow_id: str) -> dict:
    """
    Get best available name, version, cat_no for a dataflow.
    Uses generated metadata (which merges catalog + presets + overrides).
    Falls back to catalog-only, then returns bare id.
    """
    meta = {}
    if META_GENERATED.exists():
        try:
            all_meta = json.loads(META_GENERATED.read_text())
            meta = all_meta.get(dataflow_id, {})
        except Exception:
            pass

    if not meta and CATALOG_FILE.exists():
        try:
            catalog = json.loads(CATALOG_FILE.read_text())
            entry = catalog.get(dataflow_id, {})
            if entry:
                meta = {
                    "id": dataflow_id,
                    "name": entry.get("name", dataflow_id),
                    "version": entry.get("version", "1.0.0"),
                    "cat_no": "",
                    "description": entry.get("description", ""),
                }
        except Exception:
            pass

    return meta


def status() -> dict:
    """Return cache status dict."""
    info = {
        "cache_dir": str(CACHE_DIR),
        "catalog_exists": CATALOG_FILE.exists(),
        "is_fresh": is_fresh(),
        "dataflow_count": 0,
        "structure_count": 0,
        "metadata_generated": META_GENERATED.exists(),
    }
    if CATALOG_FILE.exists():
        info["catalog_mtime"] = time.ctime(CATALOG_FILE.stat().st_mtime)
        try:
            catalog = json.loads(CATALOG_FILE.read_text())
            info["dataflow_count"] = len(catalog)
        except Exception:
            pass
    if STRUCTURE_DIR.exists():
        info["structure_count"] = len(list(STRUCTURE_DIR.glob("*.json")))
    if META_GENERATED.exists():
        info["metadata_generated_mtime"] = time.ctime(META_GENERATED.stat().st_mtime)
    return info


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "refresh":
        catalog = refresh()
        print(f"OK: {len(catalog)} dataflows cached")

    elif cmd == "search":
        if len(args) < 2:
            print("Usage: abs_cache.py search <term>")
            sys.exit(1)
        term = " ".join(args[1:])
        results = search(term)
        if not results:
            print("No matches found.")
        else:
            for df in results:
                print(f"{df['id']}  (v{df['version']})  {df['name']}")

    elif cmd == "status":
        info = status()
        for k, v in info.items():
            print(f"  {k}: {v}")

    elif cmd == "structure":
        if len(args) < 2:
            print("Usage: abs_cache.py structure <dataflow_id> [version]")
            sys.exit(1)
        did = args[1]
        ver = args[2] if len(args) > 2 else "1.0.0"
        data = get_structure(did, ver)
        print(json.dumps(data, indent=2)[:4000])

    elif cmd == "gen-metadata":
        meta = generate_metadata()
        print(f"OK: metadata generated for {len(meta)} dataflows")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
