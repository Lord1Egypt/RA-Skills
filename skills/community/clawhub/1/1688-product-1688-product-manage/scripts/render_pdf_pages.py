#!/usr/bin/env python3
"""Render PDF evidence pages using Poppler or PDFKit plus sips; never OCR."""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from _local_io import cached, digest, emit, finish, run, workspace


def png_size(path):
    import struct
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("未得到有效 PNG 页图")
    width, height = struct.unpack(">II", header[16:24])
    if not width or not height:
        raise ValueError("页图尺寸无效")
    return width, height


def render(source, output, backend="auto", first=1, last=100):
    if first < 1 or last < first or last - first >= 100:
        raise ValueError("每次明确处理 1—100 页，页码从 1 开始")
    if backend == "auto":
        backend = "poppler" if shutil.which("pdfinfo") and shutil.which("pdftoppm") else "macos"
    needed = ["pdfinfo", "pdftoppm"] if backend == "poppler" else ["swift", "sips"]
    if any(not shutil.which(cmd) for cmd in needed):
        raise ValueError("无可用的完整逐页转图路线；需要 Poppler 或 macOS Swift/PDFKit 与 sips")
    helper = Path(__file__).with_name("pdf_pages.swift")
    source, folder, fingerprint = workspace(source, output, {
        "backend": backend, "first": first, "last": last,
        "pdfKitHelper": digest(helper)}, __file__)
    old = cached(folder, fingerprint)
    if old:
        return old
    paths, pages, errors = [], [], []
    if backend == "poppler":
        info = run(["pdfinfo", str(source)])
        count = re.search(r"^Pages:\s+(\d+)", info, re.M)
        if not count:
            raise ValueError("无法确认 PDF 总页数")
        total = int(count[1])
        if first > total:
            raise ValueError("起始页超出 PDF 页数")
        inputs = [{"page": n, "path": str(source)} for n in range(first, min(last, total) + 1)]
    else:
        result = json.loads(run(["swift", str(helper), str(source), str(folder),
                                 str(first), str(last)], timeout=60))
        total, inputs = result["pageCount"], result["pages"]
        paths.extend(Path(p["path"]) for p in inputs)
    for entry in inputs:
        n = entry["page"]
        target = folder / f"page-{n}.png"
        try:
            if backend == "poppler":
                run(["pdftoppm", "-f", str(n), "-l", str(n), "-singlefile",
                     "-scale-to", "1800", "-png", str(source), str(target.with_suffix(""))])
            else:
                run(["sips", "-s", "format", "png", "-Z", "1800",
                     entry["path"], "--out", str(target)])
            width, height = png_size(target)
            pages.append({"page": n, "path": str(target), "width": width, "height": height})
            paths.append(target)
        except Exception as exc:
            errors.append({"page": n, "error": str(exc)})
    covered = {p["page"] for p in pages}
    missing = [n for n in range(1, total + 1) if n not in covered]
    return finish(folder, fingerprint, {
        "status": "partial" if missing else "ok", "backend": backend,
        "pageCount": total, "pages": pages, "unrenderedPages": missing, "errors": errors,
        "visualReadingComplete": False}, paths)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--backend", choices=["auto", "poppler", "macos"], default="auto")
    p.add_argument("--first", type=int, default=1)
    p.add_argument("--last", type=int, default=100)
    args = p.parse_args()
    try:
        result = render(args.input, args.output_dir, args.backend, args.first, args.last)
        emit(result)
        return 0 if result["status"] == "ok" else 2
    except Exception as exc:
        emit({"status": "failed", "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
