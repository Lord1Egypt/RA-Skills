#!/usr/bin/env python3
"""
ebook_organizer.py — 電子書圖書館管理器
自動分類：作者 / 叢書 / 格式 / 語言 → 資料夾結構
支援軟連結（不移動原檔）、書庫索引報告
"""

import sys
import json
import shutil
import argparse
import zipfile
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DATA_DIR = Path.home() / ".bookshelf-plus" / "converter"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── 從 EPUB 讀取作者 ─────────────────────────────────────────────────────────

def _epub_author(epub_path: Path) -> str:
    try:
        with zipfile.ZipFile(epub_path, "r") as zf:
            container = next((n for n in zf.namelist() if n.endswith("container.xml")), None)
            if not container: return ""
            opf = _find_opf(zf.read(container).decode("utf-8","replace"), epub_path, zf)
            if not opf: return ""
            tree = ET.fromstring(zf.read(opf).decode("utf-8","replace"))
            NS = {"dc":"http://purl.org/dc/elements/1.1/","opf":"http://www.idpf.org/2007/opf"}
            creator = tree.find(".//dc:creator", NS)
            return (creator.text or "").strip() if creator is not None else ""
    except Exception:
        return ""


def _find_opf(cxml, epub_path, zf) -> str | None:
    try:
        root = ET.fromstring(cxml)
        for rf in root.iter():
            if rf.tag.endswith("}rootfile"):
                return rf.get("full-path")
        for n in zf.namelist():
            if n.endswith(".opf"): return n
    except Exception:
        pass
    return None


def _pdf_author(pdf_path: Path) -> str:
    import subprocess
    try:
        cp = subprocess.run(["pdfinfo", str(pdf_path)],
                           capture_output=True, text=True, timeout=30)
        for line in cp.stdout.splitlines():
            if ":" in line and "Author" in line:
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return ""


# ── 書庫索引 ─────────────────────────────────────────────────────────────────

def scan_library(library_root: Path, recursive: bool = True) -> list[dict]:
    patterns = ["**/*.epub", "**/*.pdf", "**/*.mobi", "**/*.azw3", "**/*.fb2"] \
               if recursive else ["*.epub", "*.pdf", "*.mobi", "*.azw3", "*.fb2"]
    books = []
    for pat in patterns:
        for p in library_root.glob(pat):
            author = ""
            if p.suffix.lower() == ".epub":
                author = _epub_author(p)
            elif p.suffix.lower() == ".pdf":
                author = _pdf_author(p)
            books.append({
                "path":       p,
                "name":       p.name,
                "stem":       p.stem,
                "format":     p.suffix.lstrip(".").upper(),
                "author":     author or "未知作者",
                "size_kb":    round(p.stat().st_size / 1024, 1),
                "modified":   datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d"),
            })
    return sorted(books, key=lambda b: (b["author"], b["name"]))


# ── 組織策略 ─────────────────────────────────────────────────────────────────

def _safe_name(name: str) -> str:
    """Sanitize folder/file name for cross-platform compatibility"""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip()[:120]


def organize_by_author(books: list[dict], out_root: Path,
                       link_only: bool = False, dry_run: bool = False) -> list[str]:
    """依作者組織 → out_root/作者/書名.ext"""
    ops = []
    for b in books:
        author = _safe_name(b["author"])
        target = out_root / author / _safe_name(b["stem"]) / b["name"]
        ops.append((b["path"], target, author))
    return _execute_ops(ops, link_only, dry_run)


def organize_by_format(books: list[dict], out_root: Path,
                      link_only: bool = False, dry_run: bool = False) -> list[str]:
    """依格式組織 → out_root/EPUB/作者_書名.ext"""
    ops = []
    for b in books:
        fmt   = _safe_name(b["format"])
        fname = _safe_name(f"{b['author']}_{b['stem']}")
        target = out_root / fmt / fname / b["name"]
        ops.append((b["path"], target, fmt))
    return _execute_ops(ops, link_only, dry_run)


def organize_flat(books: list[dict], out_root: Path,
                  link_only: bool = False, dry_run: bool = False) -> list[str]:
    """展平（去衝突）→ out_root/作者_書名.ext"""
    ops = []
    seen = defaultdict(int)
    for b in books:
        base = f"{_safe_name(b['author'])}_{_safe_name(b['stem'])}"
        n    = seen[base]
        seen[base] += 1
        suffix = f"_{n}" if n > 0 else ""
        target = out_root / f"{base}{suffix}.{b['name'].split('.')[-1]}"
        ops.append((b["path"], target, "flat"))
    return _execute_ops(ops, link_only, dry_run)


def _execute_ops(ops: list, link_only: bool, dry_run: bool) -> list[str]:
    """Apply file/link operations. Returns log lines."""
    lines = []
    for src, tgt, _ in ops:
        if tgt.exists():
            lines.append(f"  ⏭ 已存在：{tgt.name}")
            continue
        if dry_run:
            lines.append(f"  📋 預備：{src.name} → {tgt.relative_to(tgt.parents[1])}")
            continue
        try:
            tgt.parent.mkdir(parents=True, exist_ok=True)
            if link_only:
                tgt.symlink_to(src.resolve())
            else:
                shutil.copy2(src, tgt)
            lines.append(f"  ✅ {src.name}")
        except Exception as e:
            lines.append(f"  ❌ {src.name}：{e}")
    return lines


# ── 書庫報告 ─────────────────────────────────────────────────────────────────

def generate_library_report(books: list[dict], out_path: Path = None) -> Path:
    by_author  = defaultdict(list)
    by_format  = defaultdict(list)
    total_size = 0

    for b in books:
        by_author[b["author"]].append(b)
        by_format[b["format"]].append(b)
        total_size += b["size_kb"]

    lines = [
        "# 📚 電子書庫報告",
        f"\n**生成時間：** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"\n**總計：** {len(books)} 本，{total_size/1024:.1f} MB",
        f"\n---\n",
        "## 📊 格式分布\n",
    ]
    for fmt, bs in sorted(by_format.items(), key=lambda x: -len(x[1])):
        mb = sum(b["size_kb"] for b in bs) / 1024
        lines.append(f"- **{fmt}**：{len(bs)} 本（{mb:.1f} MB）")

    lines.append("\n## 👤 作者分布（Top 20）\n")
    for author, bs in sorted(by_author.items(), key=lambda x: -len(x[1]))[:20]:
        pages = " / ".join(b["name"] for b in bs[:3])
        if len(bs) > 3:
            pages += f" …（共 {len(bs)} 本）"
        lines.append(f"- **{author}**：{len(bs)} 本\n  {pages}")

    out = out_path or DATA_DIR / "library_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📚 電子書圖書館管理器 — 按作者/格式/叢書自動分類",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="掃描書庫（不做變動）")
    p_scan.add_argument("library", type=Path)
    p_scan.add_argument("-r", "--recursive", action="store_true")
    p_scan.add_argument("-o", "--output", type=Path, help="輸出 JSON")

    p_org = sub.add_parser("organize", help="組織書庫")
    p_org.add_argument("library", type=Path, help="書庫根目錄")
    p_org.add_argument("-o", "--output", type=Path, required=True,
                       help="輸出根目錄")
    p_org.add_argument("-m", "--mode", choices=["author","format","flat"],
                       default="author", help="組織方式")
    p_org.add_argument("--link", action="store_true",
                       help="使用軟連結（不移動原檔）")
    p_org.add_argument("--dry-run", action="store_true",
                       help="預演模式（只顯示不執行）")

    p_report = sub.add_parser("report", help="生成書庫報告")
    p_report.add_argument("library", type=Path)
    p_report.add_argument("-r", "--recursive", action="store_true")
    p_report.add_argument("-o", "--output", type=Path)

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg=""): print(msg)

    if args.cmd in ("scan", "report"):
        log(f"🔍 掃描中：{args.library}")
        books = scan_library(args.library, getattr(args, "recursive", True))
        log(f"   找到 {len(books)} 本\n")
        for b in books:
            log(f"  {b['format']:6}  {b['author'][:15]:15}  {b['name']}")
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(books, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            log(f"\n✅ JSON 已儲存：{args.output}")
        if args.cmd == "report":
            out = generate_library_report(books, args.output)
            log(f"✅ 報告已生成：{out}")

    elif args.cmd == "organize":
        log(f"🔍 掃描中：{args.library}")
        books = scan_library(args.library, recursive=True)
        log(f"   找到 {len(books)} 本\n")

        modes = {
            "author": (organize_by_author, "作者"),
            "format": (organize_by_format, "格式"),
            "flat":   (organize_flat, "展平"),
        }
        fn, mode_name = modes[args.mode]
        log(f"📁 組織方式：{mode_name}（{'軟連結' if args.link else '複製'}"
            f"{' [預演]' if args.dry_run else ''}）\n")
        log(f"   輸出至：{args.output}\n")

        lines = fn(books, args.output, link_only=args.link, dry_run=args.dry_run)
        for l in lines:
            log(l)
        log(f"\n✅ 完成")


if __name__ == "__main__":
    main()
