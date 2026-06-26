#!/usr/bin/env python3
"""Sticker/emoji manager: search local collection, search online (Tenor), add/tag/list stickers."""

import argparse
import json
import os
import ssl
import sys
import urllib.request
import urllib.parse
import shutil
from pathlib import Path


def _ssl_context():
    """Create an SSL context with robust cert discovery for macOS."""
    cert_paths = [
        os.environ.get("SSL_CERT_FILE", ""),
        "/private/etc/ssl/cert.pem",
        "/etc/ssl/cert.pem",
        "/usr/local/etc/openssl@3/cert.pem",
        "/usr/local/etc/openssl/cert.pem",
        "/opt/homebrew/etc/openssl@3/cert.pem",
    ]
    # Try certifi if available
    try:
        import certifi
        cert_paths.insert(0, certifi.where())
    except ImportError:
        pass

    for cafile in cert_paths:
        if cafile and os.path.isfile(cafile):
            try:
                ctx = ssl.create_default_context(cafile=cafile)
                return ctx
            except Exception:
                continue

    # Last resort: skip verification
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

STICKER_DIR = Path(os.environ.get("STICKER_DIR", os.path.expanduser("~/.openclaw/stickers")))
INDEX_FILE = STICKER_DIR / "index.json"


def ensure_dir():
    STICKER_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("[]")


def load_index():
    ensure_dir()
    return json.loads(INDEX_FILE.read_text())


def save_index(index):
    ensure_dir()
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2))


def search_local(query, limit=5):
    """Search local sticker collection by tags/name."""
    index = load_index()
    query_lower = query.lower()
    results = []
    for entry in index:
        name = entry.get("name", "").lower()
        tags = [t.lower() for t in entry.get("tags", [])]
        score = 0
        if query_lower in name:
            score += 2
        for tag in tags:
            if query_lower in tag:
                score += 1
        if score > 0:
            results.append((score, entry))
    results.sort(key=lambda x: -x[0])
    return [r[1] for r in results[:limit]]


def search_online(query, limit=5, provider="tenor"):
    """Search Tenor for sticker images. Returns list of {url, preview, title}."""
    api_key = os.environ.get("TENOR_API_KEY", "AIzaSyAyimkuYQYF_FXVALexPuGQctUWRURdCYQ")  # Tenor demo key
    params = urllib.parse.urlencode({
        "q": query,
        "key": api_key,
        "limit": limit,
        "media_filter": "tinygif,gif",
        "searchfilter": "sticker",
    })
    url = f"https://tenor.googleapis.com/v2/search?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Sticker/1.0"})
        with urllib.request.urlopen(req, timeout=10, context=_ssl_context()) as resp:
            data = json.loads(resp.read())
        results = []
        for item in data.get("results", []):
            media = item.get("media_formats", {})
            gif_url = media.get("gif", {}).get("url", "")
            tiny_url = media.get("tinygif", {}).get("url", "")
            results.append({
                "title": item.get("title", ""),
                "url": gif_url or tiny_url,
                "preview": tiny_url or gif_url,
                "id": item.get("id", ""),
                "source": "tenor",
            })
        return results
    except Exception as e:
        print(f"Online search failed: {e}", file=sys.stderr)
        return []


def add_sticker(path, name=None, tags=None):
    """Add a sticker image to local collection."""
    ensure_dir()
    src = Path(path)
    if not src.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    dest_name = name or src.stem
    dest_file = STICKER_DIR / f"{dest_name}{src.suffix}"
    counter = 1
    while dest_file.exists():
        dest_file = STICKER_DIR / f"{dest_name}_{counter}{src.suffix}"
        counter += 1

    shutil.copy2(str(src), str(dest_file))

    index = load_index()
    entry = {
        "name": dest_name,
        "file": str(dest_file),
        "tags": tags or [],
    }
    index.append(entry)
    save_index(index)
    print(json.dumps(entry, ensure_ascii=False))


def download_and_add(url, name=None, tags=None):
    """Download a sticker from URL and add to local collection."""
    ensure_dir()
    ext = ".gif"
    for e in [".gif", ".png", ".jpg", ".jpeg", ".webp"]:
        if e in url.lower():
            ext = e
            break

    dest_name = name or "sticker"
    dest_file = STICKER_DIR / f"{dest_name}{ext}"
    counter = 1
    while dest_file.exists():
        dest_file = STICKER_DIR / f"{dest_name}_{counter}{ext}"
        counter += 1

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Sticker/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
            dest_file.write_bytes(resp.read())
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
        sys.exit(1)

    index = load_index()
    entry = {
        "name": dest_name,
        "file": str(dest_file),
        "tags": tags or [],
    }
    index.append(entry)
    save_index(index)
    print(json.dumps(entry, ensure_ascii=False))


def list_stickers():
    """List all stickers in local collection."""
    index = load_index()
    print(json.dumps(index, ensure_ascii=False, indent=2))


def search(query, limit=5):
    """Hybrid search: local first, then online if not enough results."""
    local_results = search_local(query, limit=limit)
    output = {"local": local_results, "online": []}
    if len(local_results) < limit:
        online_results = search_online(query, limit=limit - len(local_results))
        output["online"] = online_results
    print(json.dumps(output, ensure_ascii=False, indent=2))


def remove_sticker(name):
    """Remove a sticker from local collection by name."""
    index = load_index()
    new_index = []
    removed = False
    for entry in index:
        if entry["name"] == name:
            path = Path(entry["file"])
            if path.exists():
                path.unlink()
            removed = True
            print(f"Removed: {entry['name']}")
        else:
            new_index.append(entry)
    if not removed:
        print(f"Not found: {name}", file=sys.stderr)
        sys.exit(1)
    save_index(new_index)


def main():
    parser = argparse.ArgumentParser(description="Sticker/emoji manager for OpenClaw")
    sub = parser.add_subparsers(dest="command")

    # search
    p_search = sub.add_parser("search", help="Hybrid search (local + online)")
    p_search.add_argument("query", help="Search keywords")
    p_search.add_argument("--limit", type=int, default=5)

    # search-local
    p_local = sub.add_parser("search-local", help="Search local collection only")
    p_local.add_argument("query")
    p_local.add_argument("--limit", type=int, default=5)

    # search-online
    p_online = sub.add_parser("search-online", help="Search online (Tenor) only")
    p_online.add_argument("query")
    p_online.add_argument("--limit", type=int, default=5)

    # add
    p_add = sub.add_parser("add", help="Add local file to collection")
    p_add.add_argument("path", help="Path to sticker image")
    p_add.add_argument("--name", help="Name for the sticker")
    p_add.add_argument("--tags", help="Comma-separated tags")

    # download
    p_dl = sub.add_parser("download", help="Download from URL and add to collection")
    p_dl.add_argument("url", help="URL of the sticker image")
    p_dl.add_argument("--name", help="Name for the sticker")
    p_dl.add_argument("--tags", help="Comma-separated tags")

    # list
    sub.add_parser("list", help="List all stickers in local collection")

    # remove
    p_rm = sub.add_parser("remove", help="Remove a sticker by name")
    p_rm.add_argument("name")

    args = parser.parse_args()

    if args.command == "search":
        search(args.query, args.limit)
    elif args.command == "search-local":
        results = search_local(args.query, args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.command == "search-online":
        results = search_online(args.query, args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.command == "add":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        add_sticker(args.path, name=args.name, tags=tags)
    elif args.command == "download":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        download_and_add(args.url, name=args.name, tags=tags)
    elif args.command == "list":
        list_stickers()
    elif args.command == "remove":
        remove_sticker(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
