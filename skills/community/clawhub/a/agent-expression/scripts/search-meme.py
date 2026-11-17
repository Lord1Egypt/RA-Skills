#!/usr/bin/env python3
"""Search local meme index by caption/keywords; print real absolute paths."""

from __future__ import annotations

import argparse
import importlib.util
import random
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
mdb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mdb)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Search meme index. Prints absolute paths (use stdout for MEDIA:)."
    )
    p.add_argument("query", nargs="?", default="", help="Search text, e.g. 无语 摸鱼")
    p.add_argument("--pack", help="Meme pack root")
    p.add_argument("--tag", default="", help="Optional category filter, e.g. sigh")
    p.add_argument("-n", "--limit", type=int, default=5, help="Max results (default 5)")
    p.add_argument(
        "--pick",
        action="store_true",
        help="Print only one path (best match, or random among top hits)",
    )
    p.add_argument(
        "--random-among",
        type=int,
        default=3,
        help="With --pick, random among top K (default 3)",
    )
    p.add_argument("--verbose", "-v", action="store_true", help="Show caption/score")
    p.add_argument("--stats", action="store_true", help="Print index stats and exit")
    args = p.parse_args(argv)

    pack_dir = Path(args.pack).expanduser() if args.pack else mdb.default_pack_dir()
    db_file = mdb.db_path_for_pack(pack_dir)
    if not db_file.is_file():
        print(
            f"ERROR: index not found: {db_file}\n"
            f"Run: python3 {_SCRIPTS}/index-memes.py --sync-only",
            file=sys.stderr,
        )
        return 1

    conn = mdb.connect(pack_dir)
    if args.stats:
        st = mdb.stats(conn)
        print(f"total={st['total']} captioned={st['captioned']}")
        for tag, c in st["by_tag"].items():
            print(f"{tag}\t{c}")
        return 0

    if not (args.query or "").strip() and not (args.tag or "").strip():
        print("ERROR: query or --tag required", file=sys.stderr)
        return 2

    hits = mdb.search(
        conn,
        args.query or "",
        tag=(args.tag or None),
        limit=max(args.limit, args.random_among),
    )
    if not hits:
        # Fallback: if tag given, pick random from tag via filesystem via DB
        if args.tag:
            hits = mdb.search(conn, "", tag=args.tag, limit=max(20, args.limit))
            if hits:
                random.shuffle(hits)
                hits = hits[: args.limit]
        if not hits:
            print("ERROR: no matches", file=sys.stderr)
            return 1

    if args.pick:
        pool = hits[: max(1, args.random_among)]
        chosen = random.choice(pool)
        if args.verbose:
            print(
                f"{chosen['path']}\t{chosen['tag']}\t{chosen['score']}\t{chosen['caption']}",
                file=sys.stderr,
            )
        print(chosen["path"])
        return 0

    for h in hits[: args.limit]:
        if args.verbose:
            print(f"{h['path']}\t{h['tag']}\t{h['score']}\t{h['caption']}")
        else:
            # machine-friendly: path first, then tag + caption for the model
            print(f"{h['path']}\t{h['tag']}\t{h['caption']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
