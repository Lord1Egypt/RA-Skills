#!/usr/bin/env python3
"""Add an image into a local meme pack category (create category if needed)."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
MAX_BYTES = 8 * 1024 * 1024
TAG_RE = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")

# magic → preferred extension
_MAGIC = (
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"\xff\xd8\xff", ".jpg"),
    (b"GIF87a", ".gif"),
    (b"GIF89a", ".gif"),
    (b"RIFF", ".webp"),  # need WEBP at offset 8
    (b"BM", ".bmp"),
)

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
_mdb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mdb)


def default_pack_dir() -> Path:
    return _mdb.default_pack_dir()


def load_manifest(pack_dir: Path) -> dict:
    path = pack_dir / "manifest.json"
    if not path.is_file():
        return {"categories": {}}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if "categories" not in data or not isinstance(data["categories"], dict):
        data["categories"] = {}
    return data


def save_manifest(pack_dir: Path, data: dict) -> None:
    path = pack_dir / "manifest.json"
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def detect_ext(data: bytes, hint: str = "") -> Optional[str]:
    hint = hint.lower()
    if hint in IMAGE_EXTS:
        # still verify magic when possible
        pass
    for magic, ext in _MAGIC:
        if data.startswith(magic):
            if ext == ".webp":
                if len(data) >= 12 and data[8:12] == b"WEBP":
                    return ".webp"
                continue
            return ext
    if hint in IMAGE_EXTS:
        return hint
    return None


def _is_private_host(hostname: str) -> bool:
    host = (hostname or "").strip().lower()
    if not host or host == "localhost" or host.endswith(".local"):
        return True
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return True
    for info in infos:
        ip = info[4][0]
        if ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
            return True
        if ip.startswith("169.254.") or ip.startswith("::1") or ip.startswith("fc") or ip.startswith("fd"):
            return True
        # 172.16.0.0 – 172.31.255.255
        if ip.startswith("172."):
            try:
                second = int(ip.split(".")[1])
                if 16 <= second <= 31:
                    return True
            except (ValueError, IndexError):
                pass
    return False


def fetch_bytes(source: str) -> tuple[bytes, str]:
    """Return (bytes, filename_hint) from URL or local path."""
    source = source.strip()
    if source.startswith(("http://", "https://")):
        parsed = urlparse(source)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError(f"unsupported URL scheme: {parsed.scheme}")
        if _is_private_host(parsed.hostname or ""):
            raise ValueError("refusing to fetch private/local URL (SSRF guard)")
        req = urllib.request.Request(
            source,
            headers={"User-Agent": "agent-expression/add-meme"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError(f"image larger than {MAX_BYTES} bytes")
            name = Path(parsed.path).name or "download"
            return data, name

    path = Path(source).expanduser()
    if not path.is_file():
        raise ValueError(f"local file not found: {path}")
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(f"image larger than {MAX_BYTES} bytes")
    return path.read_bytes(), path.name


def ensure_category(pack_dir: Path, tag: str, description: str, create: bool) -> tuple[Path, bool]:
    """Return (category_dir, created)."""
    memes_root = pack_dir / "memes"
    category_dir = memes_root / tag
    exists = category_dir.is_dir()
    manifest = load_manifest(pack_dir)
    in_manifest = tag in manifest.get("categories", {})

    if not exists and not create:
        raise ValueError(
            f"category '{tag}' does not exist. Pass --create with a short Chinese description to create it."
        )

    if not exists:
        category_dir.mkdir(parents=True, exist_ok=True)

    if create or not in_manifest:
        desc = (description or "").strip() or f"自定义分类 {tag}"
        cats = manifest.setdefault("categories", {})
        if tag not in cats or create:
            cats[tag] = {"description": desc}
            save_manifest(pack_dir, manifest)

    return category_dir, (not exists)


def unique_name(category_dir: Path, ext: str, data: bytes) -> Path:
    digest = hashlib.sha1(data).hexdigest()[:10]
    # skip exact duplicates
    for existing in category_dir.iterdir():
        if not existing.is_file() or existing.suffix.lower() not in IMAGE_EXTS:
            continue
        try:
            if existing.stat().st_size == len(data) and existing.read_bytes() == data:
                return existing  # already there
        except OSError:
            continue
    stamp = int(time.time())
    candidate = category_dir / f"{stamp}_{digest}{ext}"
    n = 1
    while candidate.exists():
        candidate = category_dir / f"{stamp}_{digest}_{n}{ext}"
        n += 1
    return candidate


def cmd_add(
    pack_dir: Path,
    tag: str,
    source: str,
    *,
    create: bool,
    description: str,
) -> int:
    tag = tag.strip().lower()
    if not TAG_RE.match(tag):
        print(
            "ERROR: tag must be lowercase english, start with a letter, "
            "and match [a-z][a-z0-9_-]{0,31}",
            file=sys.stderr,
        )
        return 1
    if not pack_dir.is_dir():
        print(f"ERROR: pack directory not found: {pack_dir}", file=sys.stderr)
        return 1

    try:
        data, hint_name = fetch_bytes(source)
        ext = detect_ext(data, Path(hint_name).suffix.lower())
        if not ext:
            print("ERROR: not a supported image (png/jpg/gif/webp/bmp)", file=sys.stderr)
            return 1
        category_dir, created = ensure_category(pack_dir, tag, description, create=create)
        dest = unique_name(category_dir, ext, data)
        if dest.exists() and dest.read_bytes() == data:
            print(f"EXISTS\t{dest.resolve()}")
            return 0
        dest.write_bytes(data)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    status = "CREATED_CATEGORY+ADDED" if created else "ADDED"
    print(f"{status}\t{tag}\t{dest.resolve()}")
    # Keep SQLite caption index in sync (best-effort)
    try:
        import importlib.util

        _db_spec = importlib.util.spec_from_file_location(
            "meme_db", Path(__file__).resolve().parent / "meme_db.py"
        )
        _mdb = importlib.util.module_from_spec(_db_spec)
        assert _db_spec.loader is not None
        _db_spec.loader.exec_module(_mdb)
        _conn = _mdb.connect(pack_dir)
        _mdb.upsert_meme(_conn, path=dest.resolve(), tag=tag, keep_caption=True)
        _conn.commit()
        _conn.close()
    except Exception as exc:
        print(f"WARN: index upsert failed: {exc}", file=sys.stderr)
    return 0


def cmd_create_only(pack_dir: Path, tag: str, description: str) -> int:
    tag = tag.strip().lower()
    if not TAG_RE.match(tag):
        print("ERROR: invalid tag", file=sys.stderr)
        return 1
    if not pack_dir.is_dir():
        print(f"ERROR: pack directory not found: {pack_dir}", file=sys.stderr)
        return 1
    try:
        category_dir, created = ensure_category(
            pack_dir, tag, description, create=True
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        f"{'CREATED' if created else 'EXISTS'}\t{tag}\t{category_dir.resolve()}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Add image to local meme pack / create category."
    )
    p.add_argument(
        "--pack",
        help="Meme pack root (default: $MEME_PACK or ~/…/meme-packs/official-001)",
    )
    p.add_argument(
        "--create",
        action="store_true",
        help="Create category if missing (requires --desc when new).",
    )
    p.add_argument(
        "--desc",
        default="",
        help="Chinese description for a new/updated category.",
    )
    p.add_argument(
        "--create-only",
        action="store_true",
        help="Only create an empty category (no image).",
    )
    p.add_argument("tag", nargs="?", help="Category tag, e.g. happy or custom_smirk")
    p.add_argument("source", nargs="?", help="Local path or http(s) URL to image")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    pack_dir = Path(args.pack).expanduser() if args.pack else default_pack_dir()

    if args.create_only:
        if not args.tag:
            parser.error("tag is required with --create-only")
        if not (args.desc or "").strip():
            parser.error("--desc is required with --create-only")
        return cmd_create_only(pack_dir, args.tag, args.desc)

    if not args.tag or not args.source:
        parser.print_help()
        return 2

    create = bool(args.create)
    # auto-create if category missing and --desc provided
    memes_root = pack_dir / "memes" / args.tag.strip().lower()
    if not memes_root.is_dir() and (args.desc or "").strip():
        create = True
    if create and not (args.desc or "").strip() and not memes_root.is_dir():
        print("ERROR: new category requires --desc", file=sys.stderr)
        return 1

    return cmd_add(
        pack_dir,
        args.tag,
        args.source,
        create=create,
        description=args.desc,
    )


if __name__ == "__main__":
    raise SystemExit(main())
