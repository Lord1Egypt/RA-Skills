"""Command-line interface.

    codemap build <root> [<root> ...]   # (re)build the index
    codemap find <name> [--like] [--kind class]
    codemap file <path>                 # outline: every symbol in one file
    codemap stats
"""
from __future__ import annotations

import argparse
import json
import sys

from . import index


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="codemap", description="Local code-symbol index.")
    p.add_argument("--db", default=index.DEFAULT_DB, help="index db path")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="(re)build the index over the given roots")
    b.add_argument("roots", nargs="+")

    f = sub.add_parser("find", help="locate a symbol by name")
    f.add_argument("name")
    f.add_argument("--like", action="store_true", help="substring match, not exact")
    f.add_argument("--kind", default=None, help="filter: function|class|method|interface|type")
    f.add_argument("--json", action="store_true")

    o = sub.add_parser("file", help="outline every symbol in a file")
    o.add_argument("path")
    o.add_argument("--json", action="store_true")

    sub.add_parser("stats", help="index size and composition")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.cmd == "build":
        res = index.build(args.roots, db_path=args.db)
        sys.stderr.write(
            f"codemap: indexed {res['symbols']} symbols across {res['files']} "
            f"files → {res['db']}\n"
        )
        return 0

    if args.cmd == "find":
        hits = index.find(
            args.name, db_path=args.db, kind=args.kind, exact=not args.like
        )
        if getattr(args, "json", False):
            print(json.dumps([h.__dict__ for h in hits], indent=2))
        elif not hits:
            sys.stderr.write(f"codemap: no symbol named {args.name!r}\n")
            return 1
        else:
            for h in hits:
                print(h.compact())
        return 0

    if args.cmd == "file":
        hits = index.outline(args.path, db_path=args.db)
        if getattr(args, "json", False):
            print(json.dumps([h.__dict__ for h in hits], indent=2))
        elif not hits:
            sys.stderr.write(f"codemap: no symbols indexed for {args.path}\n")
            return 1
        else:
            for h in hits:
                print(f"  L{h.line:>5}  [{h.kind}] {h.signature}")
        return 0

    if args.cmd == "stats":
        s = index.stats(db_path=args.db)
        print(json.dumps(s, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
