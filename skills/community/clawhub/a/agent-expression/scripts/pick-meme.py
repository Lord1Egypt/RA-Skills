#!/usr/bin/env python3
"""Pick a random local meme image from an installed meme pack."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
mdb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mdb)


def load_manifest(pack_dir: Path) -> dict:
    manifest_path = pack_dir / "manifest.json"
    if not manifest_path.is_file():
        return {}
    return json.loads(manifest_path.read_text(encoding="utf-8-sig"))


def list_images(tag_dir: Path) -> list[Path]:
    if not tag_dir.is_dir():
        return []
    return sorted(
        p for p in tag_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Pick a random meme by tag")
    p.add_argument("tag", help="Category tag, e.g. shy / sigh")
    p.add_argument(
        "--pack",
        help="Meme pack root (default: $MEME_PACK or data_home/meme-packs/<id>)",
    )
    args = p.parse_args(argv)

    pack_dir = Path(args.pack).expanduser() if args.pack else mdb.default_pack_dir()
    images = list_images(pack_dir / "memes" / args.tag)
    if not images:
        print(f"ERROR: no images under {pack_dir / 'memes' / args.tag}", file=sys.stderr)
        return 1
    print(str(random.choice(images).resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
