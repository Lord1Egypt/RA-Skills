#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图纸源发现：扫描本机与所有挂载盘（含压缩包内）的 CAD 图纸，只列清单不读内容。

设计要点
- 挂载盘优先：默认先扫 /Volumes 下各挂载盘（扩展盘优先），最后才扫 $HOME。
- 只列元数据：不解压、不复制、不移动、不上传任何图纸，图纸字节不出本机。
- 压缩包只读目录：zip 走标准库 zipfile 列举；rar/7z 探测本机已装工具，
  没有则如实标 unavailable，不静默跳过。
- 中文名还原：zipfile 对未置 UTF-8 标志位的条目按 cp437 解码，
  中文（GBK）文件名会变乱码，需 encode('cp437') 再按 gbk 还原。

用法
    python3 scripts/drawing_source.py                          # 默认扫挂载盘
    python3 scripts/drawing_source.py --json-out /tmp/dwg.json
    python3 scripts/drawing_source.py --roots /sample-drive --no-archive
    python3 scripts/drawing_source.py --stats-only
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import zipfile
from pathlib import Path

FORMATS = (".dwg", ".dxf", ".dwt", ".pdf")
ARCHIVE_EXTS = (".zip", ".rar", ".7z")
# 系统与隐藏目录：跳过，避免 Spotlight/fsevents 等噪声
SKIP_DIRS = {".Spotlight-V100", ".fseventsd", ".Trashes", ".Trash", ".obsidian",
             ".git", "node_modules", "__pycache__", ".DocumentRevisions-V100"}
# zipfile 对非 UTF-8 条目名的原始编码；中文多为 GBK
ZIP_NAME_FALLBACK_ENCODINGS = ("gbk", "utf-8", "big5", "cp932")


# --------------------------------------------------------------- 路径与编码
def mounted_volumes() -> list[Path]:
    """返回 /Volumes 下的挂载盘，扩展盘排在最前。"""
    base = Path("/Volumes")
    if not base.is_dir():
        return []
    vols = [p for p in base.iterdir() if p.is_dir() and p.name not in SKIP_DIRS]
    preferred = [p for p in vols if "扩展" in p.name]
    rest = [p for p in vols if p not in preferred]
    return preferred + rest


def default_roots() -> list[Path]:
    """默认扫描根：挂载盘优先（扩展盘最前），最后才是 $HOME。

    可用环境变量 CAD_DRAWING_ROOTS 覆盖（os.pathsep 分隔）。
    """
    env = os.environ.get("CAD_DRAWING_ROOTS")
    if env:
        return [Path(x) for x in env.split(os.pathsep) if x.strip()]
    roots = mounted_volumes()
    home = Path.home()
    # 系统盘（Macintosh HD）体量巨大且多为非图纸，默认只扫用户目录
    roots.append(home)
    return roots


def decode_zip_name(name: str) -> str:
    """还原 zip 内被 cp437 误解码的中文文件名（多为 GBK）。

    zipfile 在条目 flag_bits 未置 UTF-8 位时按 cp437 解码字节串，
    中文 GBK 字节因此变成乱码；还原方法是先 encode 回 cp437 再按 gbk 解。
    """
    try:
        raw = name.encode("cp437")
    except UnicodeEncodeError:
        return name  # 已是合法 unicode，无需还原
    for enc in ZIP_NAME_FALLBACK_ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return name


# --------------------------------------------------------------- 压缩包
def _archive_tool(ext: str) -> str | None:
    """探测本机可用于列举 rar/7z 的工具；都没有则返回 None。"""
    if ext == ".zip":
        return "zipfile"
    for tool in ("7z", "7zz", "unar", "bsdtar", "7za"):
        try:
            subprocess.run([tool, "--help"], capture_output=True, timeout=10)
            return tool
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
    return None


def list_zip(archive: Path, formats: tuple[str, ...]) -> tuple[list[dict], str | None]:
    """用标准库列举 zip 内图纸。返回 (条目列表, 错误信息)。"""
    out: list[dict] = []
    try:
        with zipfile.ZipFile(archive) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                name = decode_zip_name(info.filename)
                if Path(name).suffix.lower() not in formats:
                    continue
                out.append({
                    "path": f"{archive}!{name}",
                    "inner_path": name,
                    "size_bytes": info.file_size,
                    "format": Path(name).suffix.lower().lstrip("."),
                    "in_archive": True,
                    "archive": str(archive),
                    "archive_kind": ".zip",
                })
    except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
        return out, f"{type(exc).__name__}: {exc}"
    return out, None


def list_other_archive(archive: Path, formats: tuple[str, ...], tool: str) -> tuple[list[dict], str | None]:
    """用外部工具列举 rar/7z 内图纸（只列不解压）。"""
    out: list[dict] = []
    if tool.startswith("7z"):
        cmd = [tool, "l", "-ba", "-slt", "--", str(archive)]
    elif tool == "unar":
        cmd = ["unar", "-l", "--", str(archive)]
    else:  # bsdtar
        cmd = ["bsdtar", "-tf", str(archive)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return out, f"{type(exc).__name__}: {exc}"
    if proc.returncode != 0:
        return out, (proc.stderr or proc.stdout or "").strip().splitlines()[-1][:200]
    for line in (proc.stdout or "").splitlines():
        name = line.strip()
        if not name or Path(name).suffix.lower() not in formats:
            continue
        out.append({
            "path": f"{archive}!{name}",
            "inner_path": name,
            "size_bytes": None,
            "format": Path(name).suffix.lower().lstrip("."),
            "in_archive": True,
            "archive": str(archive),
            "archive_kind": archive.suffix.lower(),
        })
    return out, None


# --------------------------------------------------------------- 主扫描
def guess_project(path: Path, root: Path) -> str:
    """按 root 下的目录层级推测项目名（备份/<项目>/... 取第二层）。"""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return ""
    parts = rel.parts
    if len(parts) >= 2:
        return parts[1] if parts[0] in ("备份", "其他") else parts[0]
    return parts[0] if parts else ""


def scan(roots: list[Path], formats: tuple[str, ...] = FORMATS,
         include_archive: bool = True, progress: bool = False) -> dict:
    items: list[dict] = []
    archives: list[dict] = []
    started = time.time()
    fmt = {f.lower() for f in formats}

    for root in roots:
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith("._")]
            for fn in filenames:
                if fn.startswith("._"):
                    continue
                full = Path(dirpath) / fn
                suffix = full.suffix.lower()
                if suffix in fmt:
                    try:
                        st = full.stat()
                    except OSError:
                        continue
                    items.append({
                        "path": str(full),
                        "size_bytes": st.st_size,
                        "format": suffix.lstrip("."),
                        "root": str(root),
                        "project": guess_project(full, root),
                        "mtime": int(st.st_mtime),
                        "in_archive": False,
                    })
                elif include_archive and suffix in ARCHIVE_EXTS:
                    tool = _archive_tool(suffix)
                    if tool is None:
                        archives.append({"archive": str(full), "status": "unavailable",
                                         "reason": "本机无可用列举工具（7z/unar/bsdtar）", "count": 0})
                        continue
                    if tool == "zipfile":
                        got, err = list_zip(full, formats)
                    else:
                        got, err = list_other_archive(full, formats, tool)
                    for g in got:
                        g["root"] = str(root)
                        g["project"] = guess_project(full, root)
                    items.extend(got)
                    archives.append({"archive": str(full), "status": "ok" if err is None else "error",
                                     "reason": err or "", "count": len(got), "tool": tool})
        if progress:
            print(f"[扫描] {root} 累计 {len(items)} 张", file=sys.stderr)

    return {
        "schema": "cad-drawing-source/v1",
        "scanned_roots": [str(r) for r in roots],
        "formats": sorted(fmt),
        "include_archive": include_archive,
        "elapsed_seconds": round(time.time() - started, 2),
        "counts": {
            "total": len(items),
            "loose": sum(1 for i in items if not i["in_archive"]),
            "in_archive": sum(1 for i in items if i["in_archive"]),
            # key 与条目里的 format 一致（都不带前导点）
            "by_format": {f.lstrip("."): sum(1 for i in items if i["format"] == f.lstrip("."))
                          for f in sorted(fmt)},
        },
        "archives": archives,
        "items": items,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="图纸源发现（只列清单，不读内容）")
    ap.add_argument("--roots", nargs="*", help="扫描根；默认挂载盘优先（扩展盘最前）")
    ap.add_argument("--formats", nargs="*", default=list(FORMATS))
    ap.add_argument("--no-archive", action="store_true", help="不扫压缩包内")
    ap.add_argument("--json-out", help="清单 JSON 输出路径")
    ap.add_argument("--stats-only", action="store_true", help="只输出统计，不列明细")
    ap.add_argument("--progress", action="store_true")
    args = ap.parse_args()

    roots = [Path(x) for x in args.roots] if args.roots else default_roots()
    result = scan(roots, tuple(args.formats), not args.no_archive, args.progress)

    if args.stats_only:
        result.pop("items", None)
        result.pop("archives", None)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"已写入 {out}（{result['counts']['total']} 张）")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
