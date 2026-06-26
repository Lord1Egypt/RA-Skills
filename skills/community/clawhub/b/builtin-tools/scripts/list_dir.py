#!/usr/bin/env python3
"""list_dir — 目录浏览"""
import sys, os, fnmatch
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def main():
    params = parse_input()
    path = get_param(params, "path", ".")
    ignore = get_param(params, "ignore", [])
    show_hidden = get_param(params, "show_hidden", False)
    max_depth = get_param(params, "max_depth", 1)

    base = resolve_path(str(path))
    if not base.is_dir():
        output_error(f"不是目录: {base}", EXIT_EXEC_ERROR)

    def should_ignore(name):
        for pattern in ignore:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(name, f"**/{pattern}"):
                return True
        return False

    dirs = []
    files = []
    collected = []

    def walk(current, depth):
        if depth > max_depth:
            return
        try:
            entries = sorted(current.iterdir())
        except PermissionError:
            return
        for entry in entries:
            name = entry.name
            if not show_hidden and name.startswith("."):
                continue
            if should_ignore(name):
                continue
            rel = entry.relative_to(base)
            if entry.is_dir():
                dirs.append(str(rel))
                collected.append({"name": str(rel), "type": "dir"})
                walk(entry, depth + 1)
            else:
                size = entry.stat().st_size if entry.exists() else 0
                files.append(str(rel))
                collected.append({"name": str(rel), "type": "file", "size": size})

    walk(base, 1)

    output_ok({
        "path": str(base),
        "dirs": dirs,
        "files": files,
        "total_dirs": len(dirs),
        "total_files": len(files),
        "entries": collected,
    })

if __name__ == "__main__":
    main()
