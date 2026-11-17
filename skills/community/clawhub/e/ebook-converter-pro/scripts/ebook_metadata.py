#!/usr/bin/env python3
"""
ebook_metadata.py — 電子書元資料讀寫工具
支援 EPUB / PDF  metadata 的讀取、編輯、匯出書目
"""

import sys
import json
import argparse
import zipfile
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date

DATA_DIR = Path.home() / ".bookshelf-plus" / "converter"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ── EPUB Metadata ──────────────────────────────────────────────────────────────

def epub_read_meta(epub_path: Path) -> dict:
    meta = {
        "file": str(epub_path),
        "size_kb": round(epub_path.stat().st_size / 1024, 1),
        "format": "EPUB",
        "title": "", "author": "", "publisher": "",
        "language": "", "isbn": "", "year": "",
        "description": "", "cover_exists": False,
        "chapters": 0,
    }
    try:
        with zipfile.ZipFile(epub_path, "r") as zf:
            names = zf.namelist()
            container = next((n for n in names if n.endswith("container.xml")), None)
            if not container:
                return meta
            opf_path = _find_opf(zf.read(container).decode("utf-8", errors="replace"), epub_path, zf)
            if not opf_path:
                return meta
            opf_raw = zf.read(opf_path).decode("utf-8", errors="replace")
            opf_dir = Path(opf_path).parent

            tree = ET.fromstring(opf_raw)
            NS = {"dc": "http://purl.org/dc/elements/1.1/",
                  "opf": "http://www.idpf.org/2007/opf"}

            def dc(tag):
                el = tree.find(f".//dc:{tag}", NS)
                return el.text.strip() if el is not None and el.text else ""

            meta["title"]     = dc("title")
            meta["author"]    = dc("creator")
            meta["publisher"] = dc("publisher")
            meta["language"]  = dc("language")
            meta["isbn"]      = dc("identifier")  # may or may not be ISBN
            meta["description"] = dc("description")

            # Year from date
            dt = tree.find(".//dc:date", NS) or tree.find(".//{http://purl.org/dc/elements/1.1/}date")
            if dt is not None and dt.text:
                yr = re.search(r"\b(\d{4})\b", dt.text)
                if yr:
                    meta["year"] = yr.group(1)

            # Cover
            cover_meta = tree.find(".//opf:meta[@name='cover']", NS)
            if cover_meta is not None:
                cid = cover_meta.get("content")
                item = tree.find(f".//opf:item[@id='{cid}']", NS)
                if item is not None:
                    href = item.get("href", "")
                    cover_path = (opf_dir / href).as_posix()
                    meta["cover_exists"] = any(
                        n.replace("\\", "/") == cover_path
                        for n in names
                    )

            # Chapter count
            spine = tree.findall(".//opf:itemref", NS)
            meta["chapters"] = len(spine) if spine else 0

    except Exception as e:
        meta["error"] = str(e)
    return meta


def _find_opf(container_xml: str, epub_path: Path, zf) -> str | None:
    try:
        root = ET.fromstring(container_xml)
        for rf in root.iter():
            if rf.tag.endswith("}rootfile"):
                return rf.get("full-path")
        # fallback: find first .opf in zip
        for n in zf.namelist():
            if n.endswith(".opf"):
                return n
    except Exception:
        pass
    return None


def epub_set_meta(epub_path: Path, out_path: Path, **fields) -> Path:
    """Write metadata fields to EPUB (requires zipfile rewrite)"""
    title    = fields.get("title")
    author   = fields.get("author")
    publisher = fields.get("publisher")
    year     = fields.get("year")
    language = fields.get("language")
    isbn     = fields.get("isbn")

    tmp = DATA_DIR / f"_meta_{epub_path.stem}.epub"
    with zipfile.ZipFile(epub_path, "r") as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".opf"):
                try:
                    text = data.decode("utf-8")
                    if title:    text = _replace_dc(text, "title", title)
                    if author:   text = _replace_dc(text, "creator", author)
                    if publisher: text = _replace_dc(text, "publisher", publisher)
                    if language: text = _replace_dc(text, "language", language)
                    if isbn:     text = _replace_dc(text, "identifier", isbn)
                    if year:
                        text = re.sub(
                            r"(<dc:date[^>]*>)[^<]*(</dc:date>)",
                            rf"\g<1>{year}-01-01\g<2>", text
                        )
                    data = text.encode("utf-8")
                except Exception:
                    pass
            zout.writestr(item, data)

    out = out_path or epub_path.with_suffix(".meta.epub")
    tmp.rename(out)
    return out


def _replace_dc(xml: str, tag: str, value: str) -> str:
    pat = rf'(<dc:{tag}[^>]*>)[^<]*(</dc:{tag}>)'
    replacement = rf'\g<1>{value}\g<2>'
    return re.sub(pat, replacement, xml, count=1)


# ── PDF Metadata ──────────────────────────────────────────────────────────────

def pdf_read_meta(pdf_path: Path) -> dict:
    import subprocess
    meta = {
        "file": str(pdf_path),
        "size_kb": round(pdf_path.stat().st_size / 1024, 1),
        "format": "PDF",
        "title": "", "author": "", "creator": "",
        "pages": 0, "year": "",
    }
    try:
        cp = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            capture_output=True, text=True, timeout=30, errors="replace"
        )
        if cp.returncode == 0:
            for line in cp.stdout.splitlines():
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if k == "Title":    meta["title"]   = v
                elif k == "Author": meta["author"]  = v
                elif k == "Creator":meta["creator"] = v
                elif k == "Pages":  meta["pages"]   = int(v)
                elif k == "Year":   meta["year"]    = v
    except Exception:
        pass
    return meta


# ── Unified Reader ────────────────────────────────────────────────────────────

def read_meta(path: Path) -> dict:
    ext = path.suffix.lower()
    if ext == ".epub":
        return epub_read_meta(path)
    elif ext == ".pdf":
        return pdf_read_meta(path)
    else:
        return {"file": str(path), "format": ext.lstrip("."), "error": "unsupported"}


# ── CLI ───────────────────────────────────────────────────────────────────────

def _format_meta(m: dict) -> str:
    lines = [
        f"\n📖 {m.get('file', '?').split('/')[-1]}",
        f"   格式：{m.get('format', '?')}",
    ]
    if m.get("title"):     lines.append(f"   書名：{m['title']}")
    if m.get("author"):    lines.append(f"   作者：{m['author']}")
    if m.get("publisher"): lines.append(f"   出版社：{m['publisher']}")
    if m.get("year"):      lines.append(f"   年份：{m['year']}")
    if m.get("isbn"):      lines.append(f"   ISBN：{m['isbn']}")
    if m.get("language"):  lines.append(f"   語言：{m['language']}")
    if m.get("pages"):     lines.append(f"   頁數：{m['pages']}")
    if m.get("chapters"):  lines.append(f"   章節：{m['chapters']}")
    if m.get("size_kb"):   lines.append(f"   大小：{m['size_kb']:.0f} KB")
    if m.get("description"):
        lines.append(f"   簡介：{m['description'][:100]}...")
    if m.get("error"):
        lines.append(f"   ⚠️  {m['error']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="📚 電子書元資料工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("read",   help="讀取元資料")
    p.add_argument("file", type=Path)

    p = sub.add_parser("edit",   help="編輯 EPUB 元資料")
    p.add_argument("file", type=Path)
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("-t", "--title")
    p.add_argument("-a", "--author")
    p.add_argument("-p", "--publisher")
    p.add_argument("-y", "--year")
    p.add_argument("-l", "--language")
    p.add_argument("-i", "--isbn")

    p = sub.add_parser("export", help="匯出書目（JSON/BibTeX）")
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("-f", "--format", choices=["json","bibtex","txt"], default="json")
    p.add_argument("-o", "--output", type=Path)

    p = sub.add_parser("batch-info", help="批量讀取元資料")
    p.add_argument("dir", type=Path)
    p.add_argument("-r", "--recursive", action="store_true")
    p.add_argument("-o", "--output", type=Path, help="輸出 JSON 檔案")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg): print(msg)

    if args.cmd == "read":
        m = read_meta(args.file)
        log(_format_meta(m))

    elif args.cmd == "edit":
        fields = {
            "title": args.title, "author": args.author,
            "publisher": args.publisher, "year": args.year,
            "language": args.language, "isbn": args.isbn,
        }
        fields = {k: v for k, v in fields.items() if v}
        out = epub_set_meta(args.file, args.output, **fields)
        log(f"✅ 元資料已更新：{out}")

    elif args.cmd == "export":
        records = [read_meta(f) for f in args.files]
        out = args.output or DATA_DIR / f"bibliography.{args.format}"

        if args.format == "json":
            out.write_text(
                json.dumps(records, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        elif args.format == "bibtex":
            lines = [_to_bibtex(r) for r in records]
            out.write_text("\n\n".join(lines), encoding="utf-8")
        else:
            lines = [_format_meta(r) for r in records]
            out.write_text("\n".join(lines), encoding="utf-8")
        log(f"✅ 書目已匯出：{out}")

    elif args.cmd == "batch-info":
        patterns = ["**/*.epub", "**/*.pdf"] if args.recursive else ["*.epub", "*.pdf"]
        files = []
        for pat in patterns:
            files.extend(args.dir.glob(pat))
        records = [read_meta(f) for f in files]
        for m in records:
            log(_format_meta(m))
        if args.output:
            args.output.write_text(
                json.dumps(records, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            log(f"\n✅ JSON 已儲存：{args.output}")


def _to_bibtex(m: dict) -> str:
    key = re.sub(r"[^a-z]", "",
                 (m.get("author","Author") + m.get("year","0000")).lower())[:12]
    lines = [f"@book{{{key},"]
    if t := m.get("title"):    lines.append(f'  title    = {{{t}}},')
    if a := m.get("author"):   lines.append(f'  author   = {{{a}}},')
    if p := m.get("publisher"):lines.append(f'  publisher = {{{p}}},')
    if y := m.get("year"):     lines.append(f'  year     = {{{y}}},')
    if isbn := m.get("isbn"):  lines.append(f'  isbn     = {{{isbn}}},')
    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
