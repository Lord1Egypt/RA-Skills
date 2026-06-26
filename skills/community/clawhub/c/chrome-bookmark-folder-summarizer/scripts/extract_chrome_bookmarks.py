#!/usr/bin/env python3
"""Extract Chrome bookmark URLs under a target folder."""

import argparse
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def default_bookmarks_path() -> Path:
    system = platform.system().lower()
    home = Path.home()

    if "darwin" in system:
        return home / "Library/Application Support/Google/Chrome/Default/Bookmarks"
    if "windows" in system:
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "Google/Chrome/User Data/Default/Bookmarks"
    return home / ".config/google-chrome/Default/Bookmarks"


def read_bookmarks(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Chrome bookmarks file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def folder_name_match(folder_name: str, target: str, mode: str) -> bool:
    if mode == "exact":
        return folder_name == target
    return target.lower() in folder_name.lower()


def find_folders(
    node: Dict[str, Any],
    target: str,
    mode: str,
    folder_path: Optional[List[str]] = None,
    results: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    folder_path = folder_path or []
    results = results or []

    if node.get("type") == "folder":
        current_name = node.get("name", "")
        current_path = folder_path + ([current_name] if current_name else [])
        if folder_name_match(current_name, target, mode):
            results.append({"path": current_path, "node": node})

        for child in node.get("children", []):
            if isinstance(child, dict):
                find_folders(child, target, mode, current_path, results)
    return results


def collect_urls(folder_node: Dict[str, Any], recursive: bool) -> List[Dict[str, str]]:
    collected: List[Dict[str, str]] = []

    def walk(node: Dict[str, Any]) -> None:
        if node.get("type") == "url":
            collected.append(
                {
                    "title": node.get("name", "").strip(),
                    "url": node.get("url", "").strip(),
                }
            )
            return
        if node.get("type") == "folder":
            for child in node.get("children", []):
                if isinstance(child, dict):
                    if not recursive and child.get("type") == "folder":
                        continue
                    walk(child)

    walk(folder_node)

    seen: Set[str] = set()
    deduped: List[Dict[str, str]] = []
    for item in collected:
        url = item.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        deduped.append(item)
    return deduped


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract Chrome bookmark URLs by folder name")
    parser.add_argument("--folder", required=True, help="Target folder name")
    parser.add_argument(
        "--bookmarks",
        default=str(default_bookmarks_path()),
        help="Path to the Chrome Bookmarks file",
    )
    parser.add_argument(
        "--match-mode",
        choices=["exact", "contains"],
        default="exact",
        help="Folder name matching mode",
    )
    parser.add_argument(
        "--non-recursive",
        action="store_true",
        help="Extract only direct URLs under the target folder",
    )
    parser.add_argument(
        "--pick-first",
        action="store_true",
        help="Return only the first match when duplicate folder names exist",
    )
    args = parser.parse_args()

    try:
        bookmarks = read_bookmarks(Path(args.bookmarks).expanduser())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2

    roots = (bookmarks.get("roots") or {})
    search_nodes = [
        roots.get("bookmark_bar"),
        roots.get("other"),
        roots.get("synced"),
    ]

    matched: List[Dict[str, Any]] = []
    for root in search_nodes:
        if isinstance(root, dict):
            matched.extend(
                find_folders(
                    node=root,
                    target=args.folder,
                    mode=args.match_mode,
                )
            )

    if not matched:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Folder not found: {args.folder}",
                    "bookmarks_path": str(Path(args.bookmarks).expanduser()),
                },
                ensure_ascii=False,
            )
        )
        return 1

    if args.pick_first:
        matched = matched[:1]

    results: List[Dict[str, Any]] = []
    recursive = not args.non_recursive
    for match in matched:
        folder_node = match["node"]
        urls = collect_urls(folder_node, recursive=recursive)
        results.append(
            {
                "folder_name": folder_node.get("name", ""),
                "folder_path": " / ".join(part for part in match["path"] if part),
                "url_count": len(urls),
                "urls": urls,
            }
        )

    print(
        json.dumps(
            {
                "ok": True,
                "bookmarks_path": str(Path(args.bookmarks).expanduser()),
                "folder_query": args.folder,
                "match_mode": args.match_mode,
                "recursive": recursive,
                "folder_matches": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
