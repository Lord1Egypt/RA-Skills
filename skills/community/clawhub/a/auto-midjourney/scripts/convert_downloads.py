#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_alpha import extract_result_urls, print_json, safe_slug
from mj_browser import browser_convert_image_bytes, browser_convert_image_url


@dataclass(frozen=True)
class SourceItem:
    kind: str
    path: Path | None = None
    anchor: Path | None = None
    url: str | None = None
    group_name: str | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert local downloaded image files or MJ JSON manifests to PNG.")
    parser.add_argument(
        "inputs",
        nargs="*",
        default=["outputs"],
        help="Files or directories to scan. Directories scan for matching images and known MJ manifests; JSON files rebuild from stored URLs.",
    )
    parser.add_argument(
        "--glob",
        default="*.webp",
        help="Filename glob to match inside directories. Defaults to *.webp",
    )
    parser.add_argument(
        "--output-dir",
        help="Optional output root. If omitted, PNGs are written next to source files or under a manifest-named folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PNG files",
    )
    parser.add_argument(
        "--delete-original",
        action="store_true",
        help="Delete the source file after successful PNG conversion",
    )
    parser.add_argument(
        "--page-url",
        default="https://alpha.midjourney.com/imagine",
        help="Browser page used for conversion context",
    )
    return parser


def collect_sources(inputs: list[str], pattern: str) -> list[SourceItem]:
    items: list[SourceItem] = []
    seen_files: set[str] = set()
    seen_urls: set[str] = set()

    def add_file(path: Path, anchor: Path) -> None:
        key = str(path.resolve())
        if key in seen_files:
            return
        seen_files.add(key)
        items.append(SourceItem(kind="file", path=path, anchor=anchor))

    def add_manifest(path: Path) -> None:
        for item in load_manifest_sources(path):
            assert item.url is not None
            if item.url in seen_urls:
                continue
            seen_urls.add(item.url)
            items.append(item)

    for raw_input in inputs:
        path = Path(raw_input)
        if not path.exists():
            raise SystemExit(f"Input path not found: {raw_input}")
        if path.is_dir():
            for file in sorted(path.rglob(pattern)):
                if file.is_file():
                    add_file(file, path)
            for manifest_name in ("recent-job.json", "downloads.json"):
                for manifest in sorted(path.rglob(manifest_name)):
                    if manifest.is_file():
                        add_manifest(manifest)
            continue
        if path.suffix.lower() == ".json":
            add_manifest(path)
            continue
        add_file(path, path.parent)
    if not items:
        raise SystemExit("No matching files or manifest URLs found for conversion.")
    return items


def load_manifest_sources(path: Path) -> list[SourceItem]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON manifest: {path}") from exc

    urls = extract_result_urls(data)
    if not urls:
        raise SystemExit(f"No image URLs found in manifest: {path}")
    return [
        SourceItem(
            kind="url",
            path=path,
            url=url,
            group_name=safe_slug(path.stem, fallback="manifest"),
        )
        for url in urls
    ]


def detect_mime_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "image/webp"


def looks_like_html(path: Path) -> bool:
    head = path.read_bytes()[:256].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def manifest_url_name(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    stem = Path(parsed.path).stem
    return safe_slug(stem or "image", fallback="image")


def build_output_path(source: SourceItem, output_root: Path | None) -> Path:
    if source.kind == "file":
        assert source.path is not None
        assert source.anchor is not None
        if output_root is None:
            return source.path.with_suffix(".png")
        relative_path = source.path.relative_to(source.anchor)
        return output_root / relative_path.with_suffix(".png")

    assert source.kind == "url"
    assert source.path is not None
    assert source.url is not None
    group_name = source.group_name or "manifest"
    if output_root is None:
        return source.path.parent / group_name / f"{manifest_url_name(source.url)}.png"
    return output_root / group_name / f"{manifest_url_name(source.url)}.png"


def convert_local_file(source: SourceItem, *, page_url: str) -> dict:
    assert source.path is not None
    if looks_like_html(source.path):
        raise RuntimeError(
            "Source file is an HTML challenge page, not a real image. "
            "Use a recent-job.json/downloads.json manifest to rebuild PNGs from the original URLs."
        )
    converted = browser_convert_image_bytes(
        source.path.read_bytes(),
        input_mime_type=detect_mime_type(source.path),
        output_format="png",
        page_url=page_url,
        timeout_seconds=60.0,
    )
    return {
        "bytes": converted["bytes"],
        "width": converted.get("width"),
        "height": converted.get("height"),
        "mime_type": converted.get("mime_type"),
    }


def convert_remote_url(source: SourceItem, *, page_url: str) -> dict:
    assert source.url is not None
    converted = browser_convert_image_url(
        source.url,
        output_format="png",
        page_url=page_url,
        timeout_seconds=60.0,
    )
    return {
        "bytes": converted["bytes"],
        "width": converted.get("width"),
        "height": converted.get("height"),
        "mime_type": converted.get("mime_type"),
    }


def convert_one(source: SourceItem, *, output_root: Path | None, overwrite: bool, delete_original: bool, page_url: str) -> dict:
    output_path = build_output_path(source, output_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and not overwrite:
        return {
            "kind": source.kind,
            "source": str(source.path if source.kind == "file" else source.url),
            "output": str(output_path),
            "skipped": True,
            "reason": "output_exists",
        }

    try:
        converted = convert_local_file(source, page_url=page_url) if source.kind == "file" else convert_remote_url(source, page_url=page_url)
        output_path.write_bytes(converted["bytes"])

        if delete_original and source.kind == "file" and source.path is not None and source.path.resolve() != output_path.resolve():
            source.path.unlink()

        return {
            "kind": source.kind,
            "source": str(source.path if source.kind == "file" else source.url),
            "manifest": str(source.path) if source.kind == "url" and source.path is not None else None,
            "output": str(output_path),
            "skipped": False,
            "deleted_original": bool(delete_original and source.kind == "file"),
            "size_bytes": len(converted["bytes"]),
            "width": converted.get("width"),
            "height": converted.get("height"),
            "mime_type": converted.get("mime_type"),
        }
    except Exception as exc:
        return {
            "kind": source.kind,
            "source": str(source.path if source.kind == "file" else source.url),
            "manifest": str(source.path) if source.kind == "url" and source.path is not None else None,
            "output": str(output_path),
            "skipped": True,
            "reason": "conversion_failed",
            "error": str(exc),
        }


def main() -> int:
    args = build_parser().parse_args()
    output_root = Path(args.output_dir) if args.output_dir else None
    sources = collect_sources(args.inputs, args.glob)
    results = [
        convert_one(
            source,
            output_root=output_root,
            overwrite=args.overwrite,
            delete_original=args.delete_original,
            page_url=args.page_url,
        )
        for source in sources
    ]
    converted = [item for item in results if not item.get("skipped")]
    skipped = [item for item in results if item.get("skipped")]
    print_json(
        {
            "count": len(results),
            "converted": len(converted),
            "skipped": len(skipped),
            "results": results,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
