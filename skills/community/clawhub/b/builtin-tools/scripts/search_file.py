#!/usr/bin/env python3
"""search_file — 文件名搜索"""
import sys, os, fnmatch
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def main():
    params = parse_input()
    pattern = get_param(params, "pattern", required=True)
    path = get_param(params, "path", ".")
    recursive = get_param(params, "recursive", True)
    case_sensitive = get_param(params, "case_sensitive", False)
    ignore_dirs = get_param(params, "ignore_dirs", [
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", ".nuxt", "target",
    ])

    base = resolve_path(str(path))
    matches = []
    max_results = get_param(params, "max_results", 500)

    def match_name(name, pattern):
        if case_sensitive:
            return fnmatch.fnmatchcase(name, pattern)
        return fnmatch.fnmatch(name.lower(), pattern.lower())

    def search(current):
        if not current.is_dir():
            return
        try:
            entries = current.iterdir()
        except PermissionError:
            return
        for entry in entries:
            if len(matches) >= max_results:
                return
            name = entry.name
            if entry.name in ignore_dirs:
                continue
            if match_name(name, pattern):
                try:
                    rel = str(entry.relative_to(base))
                except ValueError:
                    rel = str(entry)
                size = entry.stat().st_size if entry.is_file() else 0
                matches.append({
                    "path": rel,
                    "name": name,
                    "type": "dir" if entry.is_dir() else "file",
                    "size": size,
                })
            if recursive and entry.is_dir():
                search(entry)

    search(base)

    output_ok({
        "pattern": pattern,
        "base": str(base),
        "matches": matches,
        "total": len(matches),
    })

if __name__ == "__main__":
    main()
