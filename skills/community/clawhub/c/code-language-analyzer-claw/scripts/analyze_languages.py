#!/usr/bin/env python3
"""
Code Language Analyzer

Scans a project directory and reports the code volume distribution
by programming language (line count + percentage).

Usage:
    python analyze_languages.py <project-path> [--json] [--detail] [--exclude <dir1,dir2,...>]

Options:
    --json          Output results as JSON (for programmatic use)
    --detail        Show per-file breakdown in addition to summary
    --exclude       Comma-separated list of additional directories to exclude
    --extensions    Show supported extension map and exit
"""

import os
import sys
import json
import argparse
from collections import defaultdict

# ---------------------------------------------------------------------------
# Extension -> Language mapping
# ---------------------------------------------------------------------------
EXTENSION_MAP = {
    # Web frontend
    ".html": "HTML", ".htm": "HTML", ".xhtml": "HTML",
    ".css": "CSS", ".scss": "SCSS", ".sass": "Sass", ".less": "LESS",
    ".vue": "Vue", ".svelte": "Svelte",
    # JavaScript family
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".jsx": "JavaScript (JSX)",
    ".ts": "TypeScript", ".tsx": "TypeScript (TSX)",
    ".coffee": "CoffeeScript",
    # Python
    ".py": "Python", ".pyw": "Python",
    # Java / JVM
    ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin",
    ".scala": "Scala", ".groovy": "Groovy", ".clj": "Clojure",
    # C / C++
    ".c": "C", ".h": "C/C++ Header",
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++ Header", ".hh": "C++ Header",
    # C#
    ".cs": "C#",
    # Go
    ".go": "Go",
    # Rust
    ".rs": "Rust",
    # Ruby
    ".rb": "Ruby", ".erb": "Ruby (ERB)",
    # PHP
    ".php": "PHP",
    # Swift / Objective-C
    ".swift": "Swift",
    ".m": "Objective-C", ".mm": "Objective-C++",
    # Shell
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell", ".fish": "Shell",
    ".bat": "Batch", ".cmd": "Batch", ".ps1": "PowerShell",
    # Data / config
    ".sql": "SQL",
    ".json": "JSON", ".json5": "JSON", ".jsonc": "JSON",
    ".yaml": "YAML", ".yml": "YAML",
    ".toml": "TOML", ".ini": "INI", ".cfg": "INI",
    ".xml": "XML", ".svg": "XML (SVG)",
    # Markup / docs
    ".md": "Markdown", ".markdown": "Markdown",
    ".rst": "reStructuredText",
    ".tex": "LaTeX",
    # Mobile
    ".dart": "Dart",
    ".lua": "Lua",
    # Functional
    ".hs": "Haskell", ".elm": "Elm",
    ".ex": "Elixir", ".exs": "Elixir",
    ".erl": "Erlang",
    ".fs": "F#", ".fsx": "F#",
    # Assembly
    ".asm": "Assembly", ".s": "Assembly",
    # Hardware
    ".v": "Verilog", ".sv": "SystemVerilog", ".vhd": "VHDL",
    # Other
    ".r": "R", ".jl": "Julia",
    ".pl": "Perl", ".pm": "Perl",
    ".tcl": "Tcl",
    ".vim": "Vim Script",
    ".proto": "Protocol Buffers",
    ".graphql": "GraphQL", ".gql": "GraphQL",
    ".thrift": "Thrift",
    ".dockerfile": "Dockerfile",
    ".makefile": "Makefile",
    ".cmake": "CMake",
    ".gradle": "Gradle",
    ".rake": "Ruby (Rake)",
    ".gemspec": "Ruby (Gemspec)",
}

# Directories that should be skipped by default
DEFAULT_EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", ".bzr",
    "node_modules", "bower_components",
    "vendor", "vendors",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", ".env",
    "dist", "build", "out", "target",
    ".next", ".nuxt", ".output",
    "coverage", ".nyc_output",
    ".idea", ".vscode",
    "Pods", ".gradle",
    ".terraform",
    "bin", "obj",
    ".cache",
}

# Files matched by basename (no extension or special names)
BASENAME_MAP = {
    "dockerfile": "Dockerfile",
    "makefile": "Makefile",
    "rakefile": "Ruby (Rake)",
    "gemfile": "Ruby (Gemfile)",
    "cmakelists.txt": "CMake",
}


def get_language(filepath):
    """Return the language name for a given file path, or None if unknown."""
    filename = os.path.basename(filepath).lower()
    if filename in BASENAME_MAP:
        return BASENAME_MAP[filename]
    _, ext = os.path.splitext(filename)
    return EXTENSION_MAP.get(ext.lower())


def count_lines(filepath, encoding="utf-8", errors="replace"):
    """Count total lines and code lines (non-blank) in a file."""
    try:
        with open(filepath, "r", encoding=encoding, errors=errors) as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError):
        return 0, 0

    total = len(lines)
    code = sum(1 for line in lines if line.strip())
    return total, code


def analyze_project(root_path, extra_excludes=None):
    """
    Walk the project directory and collect per-language statistics.

    Returns a dict:
        {
            "language_name": {
                "files": int,
                "total_lines": int,
                "code_lines": int,
                "files_detail": [{"path": str, "total": int, "code": int}, ...]
            }
        }
    """
    excludes = set(DEFAULT_EXCLUDE_DIRS)
    if extra_excludes:
        excludes.update(d.strip() for d in extra_excludes if d.strip())

    stats = defaultdict(lambda: {"files": 0, "total_lines": 0, "code_lines": 0, "files_detail": []})

    root_path = os.path.abspath(root_path)

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Prune excluded directories in-place
        dirnames[:] = [d for d in dirnames if d not in excludes]

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            language = get_language(fpath)
            if not language:
                continue

            total, code = count_lines(fpath)
            if total == 0:
                continue

            rel_path = os.path.relpath(fpath, root_path)
            entry = stats[language]
            entry["files"] += 1
            entry["total_lines"] += total
            entry["code_lines"] += code
            entry["files_detail"].append({"path": rel_path, "total": total, "code": code})

    return stats


def print_report(stats, show_detail=False):
    """Print a human-readable report to stdout."""
    if not stats:
        print("No source code files found in the project.")
        return

    # Sort by total lines descending
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]["total_lines"], reverse=True)

    grand_total_lines = sum(s["total_lines"] for s in stats.values())
    grand_code_lines = sum(s["code_lines"] for s in stats.values())
    grand_files = sum(s["files"] for s in stats.values())

    # Header
    print("=" * 70)
    print("  Code Language Analysis Report")
    print("=" * 70)
    print()
    print(f"  Total files:     {grand_files:>8,}")
    print(f"  Total lines:     {grand_total_lines:>8,}")
    print(f"  Code lines:      {grand_code_lines:>8,}")
    print(f"  Blank/comment:   {grand_total_lines - grand_code_lines:>8,}")
    print(f"  Languages:       {len(stats):>8}")
    print()
    print("-" * 70)
    print(f"  {'Language':<28} {'Files':>8} {'Lines':>10} {'Code':>10} {'%':>8}")
    print("-" * 70)

    for lang, s in sorted_stats:
        pct = (s["total_lines"] / grand_total_lines) * 100 if grand_total_lines else 0
        print(f"  {lang:<28} {s['files']:>8,} {s['total_lines']:>10,} {s['code_lines']:>10,} {pct:>7.2f}%")

    print("-" * 70)
    print()

    if show_detail:
        for lang, s in sorted_stats:
            if not s["files_detail"]:
                continue
            print(f"\n--- {lang} (top files by lines) ---")
            sorted_files = sorted(s["files_detail"], key=lambda x: x["total"], reverse=True)
            for f in sorted_files[:20]:
                print(f"  {f['total']:>8,}  {f['path']}")
            if len(sorted_files) > 20:
                print(f"  ... and {len(sorted_files) - 20} more files")

    # ASCII bar chart
    print("\n" + "=" * 70)
    print("  Distribution Chart")
    print("=" * 70)
    max_bar = 40
    for lang, s in sorted_stats:
        pct = (s["total_lines"] / grand_total_lines) * 100 if grand_total_lines else 0
        bar_len = int(pct / 100 * max_bar)
        bar = "#" * bar_len
        print(f"  {lang:<20} |{bar:<{max_bar}}| {pct:>6.2f}%")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Analyze code language distribution in a project")
    parser.add_argument("path", nargs="?", help="Path to the project directory to analyze")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--detail", action="store_true", help="Show per-file breakdown")
    parser.add_argument("--exclude", type=str, default="", help="Comma-separated extra directories to exclude")
    parser.add_argument("--extensions", action="store_true", help="Show supported extensions and exit")

    args = parser.parse_args()

    if args.extensions:
        print("Supported file extensions:")
        for ext, lang in sorted(EXTENSION_MAP.items()):
            print(f"  {ext:<12} -> {lang}")
        print("\nSpecial filenames:")
        for name, lang in sorted(BASENAME_MAP.items()):
            print(f"  {name:<12} -> {lang}")
        return

    if not args.path:
        parser.error("project path is required (unless using --extensions)")

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    extra_excludes = [d.strip() for d in args.exclude.split(",") if d.strip()]
    stats = analyze_project(args.path, extra_excludes)

    if args.json:
        # Convert defaultdict to regular dict for JSON
        output = {lang: {k: v for k, v in d.items()} for lang, d in stats.items()}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_report(stats, show_detail=args.detail)


if __name__ == "__main__":
    main()
