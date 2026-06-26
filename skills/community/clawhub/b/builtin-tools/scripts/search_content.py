#!/usr/bin/env python3
"""search_content — 正则内容搜索"""
import sys, os, re
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def main():
    params = parse_input()
    pattern = get_param(params, "pattern", required=True)
    path = get_param(params, "path", ".")
    case_sensitive = get_param(params, "case_sensitive", False)
    glob_filter = get_param(params, "glob")
    context_before = get_param(params, "context_before", 0)
    context_after = get_param(params, "context_after", 0)
    max_results = get_param(params, "max_results", 100)
    output_mode = get_param(params, "output_mode", "content")

    base = resolve_path(str(path))
    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        output_error(f"正则表达式无效: {e}", EXIT_PARAM_ERROR)

    matches = []

    def search_file(file_path):
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()
        except (PermissionError, OSError):
            return

        for i, line in enumerate(lines):
            if regex.search(line):
                match_entry = {
                    "file": str(file_path.relative_to(base)) if file_path.is_relative_to(base) else str(file_path),
                    "line": i + 1,
                    "text": line.strip()[:500],
                }
                # 上下文
                if context_before or context_after:
                    start = max(0, i - context_before)
                    end = min(len(lines), i + context_after + 1)
                    match_entry["context"] = [lines[j].strip()[:200] for j in range(start, end)]
                matches.append(match_entry)
                if len(matches) >= max_results:
                    return

    file_count = [0]

    def walk(current):
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
            if name.startswith("."):
                continue
            if entry.is_dir():
                if name not in ("node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"):
                    walk(entry)
            elif entry.is_file():
                if glob_filter:
                    import fnmatch
                    if not fnmatch.fnmatch(name, glob_filter):
                        continue
                file_count[0] += 1
                search_file(entry)

    walk(base)

    if output_mode == "count":
        file_matches = {}
        for m in matches:
            f = m["file"]
            file_matches[f] = file_matches.get(f, 0) + 1
        output_ok({
            "pattern": pattern,
            "files_with_matches": file_matches,
            "total_matches": len(matches),
            "files_scanned": file_count[0],
        })
    elif output_mode == "files":
        files = list(dict.fromkeys(m["file"] for m in matches))
        output_ok({
            "pattern": pattern,
            "files": files,
            "total": len(files),
        })
    else:
        output_ok({
            "pattern": pattern,
            "matches": matches,
            "total": len(matches),
            "files_scanned": file_count[0],
        })


if __name__ == "__main__":
    main()
