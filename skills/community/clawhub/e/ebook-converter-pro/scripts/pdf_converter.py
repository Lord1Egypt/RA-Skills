#!/usr/bin/env python3
"""
pdf_converter.py — PDF 轉換工具
支援：PDF → TXT、PDF → Markdown、PDF → 圖片、批量轉換、頁面範圍裁剪
"""

import sys
import re
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / ".bookshelf-plus" / "converter"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── 工具檢測 ─────────────────────────────────────────────────────────────────

def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run(cmd: list[str], capture=True) -> tuple[int, str, str]:
    try:
        cp = subprocess.run(cmd, capture_output=capture,
                          text=True, timeout=120, errors="replace")
        return cp.returncode, cp.stdout or "", cp.stderr or ""
    except Exception as e:
        return 1, "", str(e)


# ── PDF → TXT（pdftotext，支援圖片 OCR）──────────────────────────────────────

def pdf_to_txt(pdf_path: Path, out_path: Path = None,
               pages: str = None, ocr: bool = False) -> Path:
    """pdftotext 若失敗則退到 OCR（pdftoppm + tesseract）"""
    out = out_path or pdf_path.with_suffix(".txt")
    tmp_raw = DATA_DIR / f"_raw_{pdf_path.stem}.txt"

    if _has("pdftotext"):
        cmd = ["pdftotext"]
        if pages:
            cmd += ["-f", str(pages.split("-")[0]),
                    "-l", str(pages.split("-")[-1])]
        cmd += ["-layout", str(pdf_path), str(tmp_raw)]
        rc, _, err = _run(cmd)
        if rc == 0 and tmp_raw.exists():
            text = tmp_raw.read_text(encoding="utf-8", errors="replace")
            tmp_raw.unlink()
        else:
            text = ""
    else:
        text = ""

    # OCR fallback
    if not text.strip() or ocr:
        text += _pdf_ocr(pdf_path, pages)

    out.write_text(text.strip(), encoding="utf-8")
    return out


def _pdf_ocr(pdf_path: Path, pages: str = None) -> str:
    if not _has("tesseract"):
        return ""
    if not _has("pdftoppm"):
        return ""

    # 轉圖片
    tmp_dir = DATA_DIR / f"_ocr_{pdf_path.stem}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["pdftoppm"]
    if pages:
        parts = pages.split("-")
        cmd += ["-f", parts[0], "-l", parts[-1]]
    cmd += ["-r", "200", "-png", str(pdf_path), str(tmp_dir / "page")]
    rc, _, _ = _run(cmd)
    if rc != 0:
        return ""

    pages_img = sorted(tmp_dir.glob("page-*.png"))
    lines = []
    for img in pages_img:
        rc, out, _ = _run(["tesseract", str(img), "stdout", "-l", "chi_tra+eng", "--psm", "6"])
        if rc == 0 and out.strip():
            lines.append(out.strip() + "\n\n")

    # 清理
    for f in tmp_dir.glob("*"):
        f.unlink()
    tmp_dir.rmdir()
    return "".join(lines)


# ── PDF → Markdown ───────────────────────────────────────────────────────────

def pdf_to_markdown(pdf_path: Path, out_path: Path = None,
                    pages: str = None) -> Path:
    """先生成 TXT，再作 Markdown 格式化（標題層次、列表識別）"""
    txt_path = DATA_DIR / f"_{pdf_path.stem}.txt"
    pdf_to_txt(pdf_path, txt_path, pages=pages)
    text = txt_path.read_text(encoding="utf-8", errors="replace")
    txt_path.unlink()

    # 簡單 Markdown 格式化
    lines = []
    in_code = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            lines.append("")
            continue
        # 已有 Markdown 語法
        if re.match(r"^#{1,6}\s", line):
            lines.append(line)
            continue
        # 目錄 / 列表
        if re.match(r"^[\d]+\.", line) or re.match(r"^[·\-\*]\s", line):
            lines.append(line)
            continue
        # 程式碼區塊
        if "```" in line:
            in_code = not in_code
            lines.append(line)
            continue
        if in_code:
            lines.append(line)
            continue
        # 短行（可能是標題）
        if len(line) < 80 and line == line.upper() and len(line.split()) < 8:
            lines.append(f"## {line}")
            continue
        lines.append(line)

    out = out_path or pdf_path.with_suffix(".md")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ── PDF → 圖片 ───────────────────────────────────────────────────────────────

def pdf_to_images(pdf_path: Path, out_dir: Path = None,
                  dpi: int = 150, pages: str = None, fmt: str = "png") -> list[Path]:
    if not _has("pdftoppm"):
        print("❌ 需要 pdftoppm（poppler-utils）")
        return []
    out_dir = out_dir or pdf_path.parent / f"{pdf_path.stem}_images"
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / f"page"

    cmd = ["pdftoppm"]
    if pages:
        parts = pages.split("-")
        cmd += ["-f", parts[0], "-l", parts[-1]]
    cmd += ["-r", str(dpi), "-{fmt}".format(fmt=fmt), str(pdf_path), str(prefix)]
    rc, _, err = _run(cmd)
    if rc != 0:
        print(f"❌ 轉圖片失敗：{err}")
        return []
    imgs = sorted(out_dir.glob(f"page-*.{fmt}"))
    return imgs


# ── PDF 分割（頁面範圍）─────────────────────────────────────────────────────

def pdf_split(pdf_path: Path, ranges: list[str], out_dir: Path = None) -> list[Path]:
    """ranges: ["1-5", "10-", "20"]"""
    if not _has("pdftk"):
        print("❌ 需要 pdftk（sudo apt install pdftk | brew install pdftk）")
        return []
    out_dir = out_dir or pdf_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = []

    for i, rng in enumerate(ranges, 1):
        out = out_dir / f"{pdf_path.stem}_p{rng.replace('-','to')}.pdf"
        if "-" in rng:
            f, t = rng.split("-", 1)
            t = t or "end"
            cmd = ["pdftk", str(pdf_path), "cat", f"{f}-{t}", "output", str(out)]
        else:
            cmd = ["pdftk", str(pdf_path), "cat", rng, "output", str(out)]
        rc, _, err = _run(cmd)
        if rc == 0:
            outputs.append(out)
        else:
            print(f"❌ 分割 {rng} 失敗：{err}")
    return outputs


# ── PDF 合併 ─────────────────────────────────────────────────────────────────

def pdf_merge(pdf_files: list[Path], out_path: Path) -> Path:
    if not _has("pdftk"):
        print("❌ 需要 pdftk")
        return out_path
    cmd = ["pdftk"] + [str(f) for f in pdf_files] + ["output", str(out_path)]
    rc, _, err = _run(cmd)
    if rc != 0:
        print(f"❌ 合併失敗：{err}")
    return out_path


# ── PDF 元資訊 ───────────────────────────────────────────────────────────────

def pdf_info(pdf_path: Path) -> dict:
    info = {
        "file": str(pdf_path),
        "size_kb": round(pdf_path.stat().st_size / 1024, 1),
        "pages": 0,
        "title": "",
        "author": "",
        "creator": "",
    }
    if _has("pdfinfo"):
        rc, out, _ = _run(["pdfinfo", str(pdf_path)])
        if rc == 0:
            for line in out.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip(), v.strip()
                    if k == "Pages":      info["pages"] = int(v)
                    elif k == "Title":    info["title"] = v
                    elif k == "Author":   info["author"] = v
                    elif k == "Creator":  info["creator"] = v
    return info


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="PDF 轉換工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # to-txt
    p = sub.add_parser("txt",   help="PDF → TXT")
    p.add_argument("input", type=Path)
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("-p", "--pages", help="頁面範圍，如 1-5 或 10-end")
    p.add_argument("--ocr", action="store_true", help="同時 OCR 圖片頁面")

    # to-md
    p = sub.add_parser("md",   help="PDF → Markdown")
    p.add_argument("input", type=Path)
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("-p", "--pages",)

    # to-images
    p = sub.add_parser("images", help="PDF → 圖片")
    p.add_argument("input", type=Path)
    p.add_argument("-o", "--output-dir", type=Path)
    p.add_argument("-p", "--pages")
    p.add_argument("--dpi", type=int, default=150)
    p.add_argument("--fmt", choices=["png","jpg"], default="png")

    # split
    p = sub.add_parser("split", help="PDF 分割（按頁面範圍）")
    p.add_argument("input", type=Path)
    p.add_argument("ranges", nargs="+", help="如 1-5 10-15 20-")
    p.add_argument("-o", "--output-dir", type=Path)

    # merge
    p = sub.add_parser("merge", help="PDF 合併")
    p.add_argument("inputs", nargs="+", type=Path)
    p.add_argument("-o", "--output", type=Path, required=True)

    # info
    p = sub.add_parser("info",  help="PDF 元資訊")
    p.add_argument("input", type=Path)

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg): print(msg)

    if args.cmd == "txt":
        out = pdf_to_txt(args.input, args.output, args.pages, args.ocr)
        log(f"✅ TXT 已生成：{out}")

    elif args.cmd == "md":
        out = pdf_to_markdown(args.input, args.output, args.pages)
        log(f"✅ Markdown 已生成：{out}")

    elif args.cmd == "images":
        imgs = pdf_to_images(args.input, args.output_dir,
                             dpi=args.dpi, pages=args.pages, fmt=args.fmt)
        if imgs:
            log(f"✅ 圖片已生成（{len(imgs)} 頁）：{imgs[0].parent}")

    elif args.cmd == "split":
        outs = pdf_split(args.input, args.ranges, args.output_dir)
        for o in outs:
            log(f"✅ 已分割：{o}")

    elif args.cmd == "merge":
        out = pdf_merge(args.inputs, args.output)
        log(f"✅ 已合併：{out}")

    elif args.cmd == "info":
        info = pdf_info(args.input)
        log(f"\n📄 {info['file']}")
        log(f"   大小：{info['size_kb']} KB")
        log(f"   頁數：{info['pages']}")
        if info["title"]:   log(f"   標題：{info['title']}")
        if info["author"]:  log(f"   作者：{info['author']}")
        if info["creator"]: log(f"   建立：{info['creator']}")


if __name__ == "__main__":
    main()
