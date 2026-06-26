#!/usr/bin/env python3
"""Chrome Bookmarks CLI — search, list, open bookmarks from terminal.

Usage:
  python3 chrome_bookmarks.py search <keyword> [--limit N] [--folder FOLDER]
  python3 chrome_bookmarks.py list [--folder FOLDER] [--depth N]
  python3 chrome_bookmarks.py open <keyword_or_index>
  python3 chrome_bookmarks.py tree [--depth N]

Output format: JSON array of bookmark objects.
"""

import json
import os
import sys
import subprocess
import argparse
from pathlib import Path


def get_chrome_bookmarks_path():
    """Auto-detect Chrome Bookmarks file path across platforms and profiles."""
    home = Path.home()
    platform = sys.platform

    if platform == "darwin":
        chrome_dir = home / "Library/Application Support/Google/Chrome"
    elif platform == "win32":
        chrome_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/User Data"
    else:
        chrome_dir = home / ".config/google-chrome"

    if not chrome_dir.exists():
        return None

    # Check Default first, then Profile 1, 2, ...
    candidates = ["Default"] + sorted(
        [d.name for d in chrome_dir.iterdir() if d.name.startswith("Profile ") and d.is_dir()]
    )

    for profile in candidates:
        bm_path = chrome_dir / profile / "Bookmarks"
        if bm_path.exists():
            return str(bm_path)

    return None


def load_bookmarks(path=None):
    """Load and parse Chrome Bookmarks JSON file."""
    if path is None:
        path = get_chrome_bookmarks_path()
    if path is None:
        print(json.dumps({"error": "Chrome Bookmarks file not found"}))
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"error": f"Failed to read bookmarks: {e}"}))
        sys.exit(1)


def flatten_bookmarks(node, path_prefix=""):
    """Flatten bookmark tree into a list of {name, url, folder, path}."""
    results = []
    node_type = node.get("type", "")
    name = node.get("name", "")

    if node_type == "url":
        results.append({
            "name": name,
            "url": node.get("url", ""),
            "folder": path_prefix,
            "path": path_prefix + "/" + name if path_prefix else name,
        })
    elif node_type == "folder":
        current_path = path_prefix + "/" + name if path_prefix else name
        for child in node.get("children", []):
            results.extend(flatten_bookmarks(child, current_path))

    return results


def get_all_bookmarks_flat(data):
    """Get all bookmarks from all root folders as flat list."""
    roots = data.get("roots", {})
    all_bookmarks = []
    for key in ["bookmark_bar", "other", "synced"]:
        node = roots.get(key, {})
        if isinstance(node, dict):
            all_bookmarks.extend(flatten_bookmarks(node))
    return all_bookmarks


def search_bookmarks(keyword, limit=20, folder=None):
    """Search bookmarks by keyword in name and URL."""
    data = load_bookmarks()
    all_bm = get_all_bookmarks_flat(data)

    keyword_lower = keyword.lower()
    results = []
    for bm in all_bm:
        if folder and folder.lower() not in bm["folder"].lower():
            continue
        if keyword_lower in bm["name"].lower() or keyword_lower in bm["url"].lower():
            results.append(bm)
            if len(results) >= limit:
                break

    return results


def list_bookmarks(folder=None, depth=2):
    """List bookmarks under a specific folder or all top-level."""
    data = load_bookmarks()
    roots = data.get("roots", {})

    if folder:
        # Find the folder node
        target = None
        for key in ["bookmark_bar", "other", "synced"]:
            node = roots.get(key, {})
            if isinstance(node, dict):
                target = _find_folder(node, folder)
                if target:
                    break
        if target is None:
            return [{"error": f"Folder '{folder}' not found"}]
        return _list_node(target, depth=depth, current_depth=0)
    else:
        # List all root-level items
        results = []
        for key in ["bookmark_bar", "other", "synced"]:
            node = roots.get(key, {})
            if isinstance(node, dict):
                results.extend(_list_node(node, depth=depth, current_depth=0))
        return results


def _find_folder(node, folder_name):
    """Recursively find a folder by name."""
    if node.get("type") == "folder" and node.get("name", "").lower() == folder_name.lower():
        return node
    if node.get("type") == "folder":
        for child in node.get("children", []):
            result = _find_folder(child, folder_name)
            if result:
                return result
    return None


def _list_node(node, depth=2, current_depth=0):
    """List items in a node up to specified depth."""
    results = []
    node_type = node.get("type", "")
    name = node.get("name", "")

    if node_type == "folder":
        children_count = len(node.get("children", []))
        results.append({
            "type": "folder",
            "name": name,
            "children_count": children_count,
            "depth": current_depth,
        })
        if current_depth < depth - 1:
            for child in node.get("children", []):
                results.extend(_list_node(child, depth, current_depth + 1))
    elif node_type == "url":
        results.append({
            "type": "url",
            "name": name,
            "url": node.get("url", ""),
            "depth": current_depth,
        })

    return results


def tree_bookmarks(depth=1):
    """Show bookmark tree structure."""
    data = load_bookmarks()
    roots = data.get("roots", {})

    def _count_urls(node):
        if node.get("type") == "url":
            return 1
        count = 0
        for child in node.get("children", []):
            count += _count_urls(child)
        return count

    results = []
    for key in ["bookmark_bar", "other", "synced"]:
        node = roots.get(key, {})
        if isinstance(node, dict) and node.get("children"):
            url_count = _count_urls(node)
            results.append({
                "root": key,
                "name": node.get("name", ""),
                "total_urls": url_count,
                "children": _list_node(node, depth=depth + 1, current_depth=0),
            })

    return results


def open_bookmark(keyword_or_index):
    """Open a bookmark by keyword search (first match) or index from last search results."""
    data = load_bookmarks()
    all_bm = get_all_bookmarks_flat(data)

    # Try as numeric index first
    try:
        idx = int(keyword_or_index)
        if 0 <= idx < len(all_bm):
            url = all_bm[idx]["url"]
            subprocess.Popen(["open", url])
            return {"opened": True, "url": url, "name": all_bm[idx]["name"]}
    except ValueError:
        pass

    # Search by keyword, open first match
    keyword_lower = keyword_or_index.lower()
    for bm in all_bm:
        if keyword_lower in bm["name"].lower() or keyword_lower in bm["url"].lower():
            subprocess.Popen(["open", bm["url"]])
            return {"opened": True, "url": bm["url"], "name": bm["name"]}

    return {"opened": False, "error": f"No bookmark found matching '{keyword_or_index}'"}


def main():
    parser = argparse.ArgumentParser(description="Chrome Bookmarks CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # search
    search_parser = subparsers.add_parser("search", help="Search bookmarks by keyword")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    search_parser.add_argument("--folder", help="Filter by folder name")

    # list
    list_parser = subparsers.add_parser("list", help="List bookmarks in a folder")
    list_parser.add_argument("--folder", help="Folder name to list")
    list_parser.add_argument("--depth", type=int, default=2, help="Depth to traverse (default: 2)")

    # open
    open_parser = subparsers.add_parser("open", help="Open a bookmark in browser")
    open_parser.add_argument("keyword", help="Keyword to search or index number")

    # tree
    tree_parser = subparsers.add_parser("tree", help="Show bookmark tree structure")
    tree_parser.add_argument("--depth", type=int, default=1, help="Depth to show (default: 1)")

    args = parser.parse_args()

    if args.command == "search":
        result = search_bookmarks(args.keyword, limit=args.limit, folder=args.folder)
    elif args.command == "list":
        result = list_bookmarks(folder=args.folder, depth=args.depth)
    elif args.command == "open":
        result = open_bookmark(args.keyword)
    elif args.command == "tree":
        result = tree_bookmarks(depth=args.depth)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
