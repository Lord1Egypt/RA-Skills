#!/usr/bin/env python3
"""Command-line interface for ra-skills."""
import argparse
import os
import sys

from . import __version__, search, stats, show, fetch_content, download

BOLD, CYAN, MAG, YEL, RESET = "\033[1m", "\033[36m", "\033[35m", "\033[33m", "\033[0m"


def _no_color():
    return not sys.stdout.isatty()


def _c(code, text):
    return text if _no_color() else f"{code}{text}{RESET}"


def _print_skill(i, s):
    print(f"{i}. {_c(BOLD, s.get('name', '?'))}")
    print(f"   Identifier:  {s.get('identifier', '')}")
    print(f"   Description: {s.get('description', 'No description.')}")
    print(f"   Source:      {_c(CYAN, s.get('source', ''))}  |  Category: {_c(MAG, s.get('category', ''))}")
    if s.get("installCmd"):
        print(f"   Install:     {_c(YEL, s.get('installCmd'))}")
    if s.get("sourceUrl"):
        print(f"   URL:         {s.get('sourceUrl')}")
    print("-" * 60)


def cmd_search(args):
    results = search(args.query, source=args.source, category=args.category, limit=args.limit)
    total = len(search(args.query, source=args.source, category=args.category, limit=0))
    print(f"\nFound {total} matching skills (showing {min(total, len(results))}):\n")
    for i, s in enumerate(results, 1):
        _print_skill(i, s)


def cmd_show(args):
    s = show(args.name)
    if not s:
        print(f"Skill '{args.name}' not found.")
        sys.exit(1)
    _print_skill(1, s)


def cmd_stats(args):
    st = stats()
    print("=== RA-Skills Registry ===")
    print(f"Total:     {st['total']:,}")
    print(f"Built-in:  {st['built_in']:,}")
    print(f"Optional:  {st['optional']:,}")
    print(f"Community: {st['community']:,}")
    print("By source:")
    for src, n in st["by_source"].items():
        print(f"  {src:12} {n:,}")


def cmd_list(args):
    results = search(None, source=args.source, category=args.category, limit=args.limit)
    for i, s in enumerate(results, 1):
        print(f"{i:4}. {s.get('name', ''):40}  [{s.get('source', '')}]")


def cmd_get(args):
    if args.md_only:
        content = fetch_content(args.name)
        if not content:
            print(f"Could not fetch SKILL.md for '{args.name}'.")
            sys.exit(1)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved {len(content):,} bytes to {args.output}")
        else:
            print(content)
        return
    out = download(args.name, dest=args.output or ".")
    if not out:
        print(f"Could not download '{args.name}' (not found, or unreachable).")
        sys.exit(1)
    n = sum(len(files) for _, _, files in os.walk(out))
    print(f"Downloaded full skill folder → {out}  ({n} files)")


def main():
    p = argparse.ArgumentParser(
        prog="ra-skills",
        description="Search 90,896 Hermes Agent skills offline (RA-Skills registry).",
    )
    p.add_argument("--version", action="version", version=f"ra-skills {__version__}")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("search", help="Search skills by keyword")
    sp.add_argument("query", nargs="?", default=None)
    sp.add_argument("-s", "--source")
    sp.add_argument("-c", "--category")
    sp.add_argument("-l", "--limit", type=int, default=10)
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("show", help="Show one skill's metadata")
    sp.add_argument("name")
    sp.set_defaults(func=cmd_show)

    sp = sub.add_parser("stats", help="Registry statistics")
    sp.set_defaults(func=cmd_stats)

    sp = sub.add_parser("list", help="List skills (optionally filtered)")
    sp.add_argument("-s", "--source")
    sp.add_argument("-c", "--category")
    sp.add_argument("-l", "--limit", type=int, default=20)
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("get", help="Download a skill's full folder from GitHub")
    sp.add_argument("name")
    sp.add_argument("-o", "--output", help="Output dir (or file with --md-only)")
    sp.add_argument("--md-only", action="store_true", help="Fetch only SKILL.md, not the whole folder")
    sp.set_defaults(func=cmd_get)

    args = p.parse_args()
    if not getattr(args, "cmd", None):
        p.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
