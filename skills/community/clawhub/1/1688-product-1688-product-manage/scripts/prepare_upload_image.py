#!/usr/bin/env python3
"""Prepare a bounded-size upload copy. Preserve source; Pillow or macOS sips."""
import argparse
import importlib.util
import re
import shutil
import sys
from pathlib import Path

from _local_io import cached, emit, finish, run, workspace


def sips_info(path):
    output = run(["sips", "-g", "format", "-g", "pixelWidth", "-g", "pixelHeight",
                  "-g", "hasAlpha", str(path)])
    values = dict(re.findall(r"^\s+(format|pixelWidth|pixelHeight|hasAlpha):\s*(\S+)",
                             output, re.M))
    width, height = int(values["pixelWidth"]), int(values["pixelHeight"])
    if width <= 0 or height <= 0:
        raise ValueError("图片尺寸无效")
    return values["format"].lower(), width, height, values.get("hasAlpha") == "yes"


def prepare(source, output, backend="auto", max_bytes=500000, min_edge=640):
    if max_bytes <= 0 or min_edge <= 0:
        raise ValueError("大小和尺寸下限须为正数")
    if backend == "auto":
        backend = "pillow" if importlib.util.find_spec("PIL") else "sips"
    if backend == "sips" and not shutil.which("sips"):
        raise ValueError("Pillow 和 sips 均不可用，无法准备上传副本")
    source, folder, fingerprint = workspace(
        source, output, {"backend": backend, "maxBytes": max_bytes, "minEdge": min_edge}, __file__)
    old = cached(folder, fingerprint)
    if old:
        return old
    im = None
    if backend == "pillow":
        from PIL import Image, ImageOps
        with Image.open(source) as original:
            if getattr(original, "n_frames", 1) != 1:
                raise ValueError("多帧图片请先明确使用哪一帧")
            if original.width * original.height > 40000000:
                raise ValueError("图片像素过大，请提供清晰的较小副本")
            original.load()
            fmt = (original.format or "").lower()
            alpha = "A" in original.getbands() or "transparency" in original.info
            im = ImageOps.exif_transpose(original).convert("RGBA" if alpha else "RGB")
        width, height = im.size
    else:
        fmt, width, height, alpha = sips_info(source)
        if fmt not in ("jpeg", "png", "webp") or width * height > 40000000:
            raise ValueError("sips 备用路线仅处理单幅 JPEG/PNG/WebP 且不超过 4000 万像素")
    if fmt not in ("jpeg", "png", "webp"):
        raise ValueError("上传准备仅支持 JPEG/PNG/WebP，请提供支持格式")
    if source.stat().st_size <= max_bytes:
        return finish(folder, fingerprint, {
            "status": "ok", "backend": backend, "path": str(source),
            "bytes": source.stat().st_size, "width": width, "height": height,
            "mime": "image/" + fmt, "uploadName": source.stem + (".jpg" if fmt == "jpeg" else "." + fmt),
            "compressed": False, "needsVisualCheck": False}, [])
    target_fmt = "png" if alpha else "jpeg"
    target = folder / ("upload.png" if alpha else "upload.jpg")
    floor = min(max(width, height), min_edge)
    edge = max(width, height)
    for _ in range(16):
        for quality in ([None] if alpha else [95, 85, 75, 65]):
            if backend == "pillow":
                copy = im.copy()
                copy.thumbnail((edge, edge), Image.Resampling.LANCZOS)
                options = {"optimize": True}
                if quality:
                    options["quality"] = quality
                copy.save(target, format=target_fmt.upper(), **options)
                with Image.open(target) as check:
                    check.load()
                    out_w, out_h = check.size
                    if alpha and "A" not in check.getbands():
                        raise ValueError("上传副本丢失透明通道")
            else:
                argv = ["sips", "-s", "format", target_fmt]
                if quality:
                    argv += ["-s", "formatOptions", str(quality)]
                run(argv + ["-Z", str(edge), str(source), "--out", str(target)])
                actual, out_w, out_h, out_alpha = sips_info(target)
                if actual != target_fmt or (alpha and not out_alpha):
                    raise ValueError("sips 输出格式或透明通道不符合要求")
            size = target.stat().st_size
            if 0 < size <= max_bytes:
                return finish(folder, fingerprint, {
                    "status": "ok", "backend": backend, "path": str(target),
                    "bytes": size, "width": out_w, "height": out_h,
                    "mime": "image/" + target_fmt, "uploadName": target.name,
                    "compressed": True, "needsVisualCheck": True}, [target])
        if edge == floor:
            break
        edge = max(floor, int(edge * 0.8))
    raise ValueError("在质量及尺寸下限内无法达到大小要求；保留原图，请提供较小清晰图片")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--backend", choices=["auto", "pillow", "sips"], default="auto")
    p.add_argument("--max-bytes", type=int, default=500000)
    args = p.parse_args()
    try:
        result = prepare(args.input, args.output_dir, args.backend, args.max_bytes)
        emit(result)
        return 0
    except Exception as exc:
        emit({"status": "failed", "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
