#!/usr/bin/env python3
"""
epub_converter.py — EPUB 萬用轉換器
支援：EPUB ↔ TXT、EPUB → Markdown、EPUB → HTML、批量轉換
"""

import sys
import re
import json
import zipfile
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# ── EPUB 解析 ────────────────────────────────────────────────────────────────

NS = {
    "opf":  "http://www.idpf.org/2007/opf",
    "dc":   "http://purl.org/dc/elements/1.1/",
    "ncx":  "http://www.daisy.org/z3986/2005/ncx/",
}

def _q(ns, tag):
    return f"{{{NS[ns]}}}{tag}"

def _parse_meta(container_path: Path) -> tuple[Path, dict]:
    """Parse container.xml → opf path + metadata dict"""
    tree = ET.parse(container_path)
    root = tree.getroot()
    rootfile = root.find(".//{http://openebook.org/namespaces/rootfile/}rootfile")
    if rootfile is None:
        # Fallback for older container format
        rootfile = root.find(".//rootfile")
    opf_path = rootfile.get("full-path") if rootfile else "OEBPS/content.opf"
    base = container_path.parent / opf_path
    opf_dir = base.parent

    opf_tree = ET.parse(base)
    opf_root = opf_tree.getroot()

    # Metadata
    meta = {}
    for tag in ["title", "creator", "publisher", "language", "description"]:
        el = opf_root.find(f".//dc:{tag}", NS)
        if el is None:
            el = opf_root.find(f".//{_q('dc', tag)}")
        meta[tag] = el.text.strip() if el is not None and el.text else ""

    # Cover
    cover_id = None
    meta_node = opf_root.find(".//opf:meta[@name='cover']", NS)
    if meta_node is None:
        meta_node = opf_root.find(".//{http://www.idpf.org/2007/opf}meta[@name='cover']")
    if meta_node is not None:
        cover_id = meta_node.get("content")

    cover_href = None
    if cover_id:
        item = opf_root.find(f".//opf:item[@id='{cover_id}']", NS)
        if item is None:
            item = opf_root.find(f".//{_q('opf','item')}[@id='{cover_id}']")
        if item is not None:
            cover_href = item.get("href")

    # Spine (ordered chapters)
    spine_items = []
    for itemref in opf_root.iter(_q("opf", "itemref")):
        idref = itemref.get("idref")
        manifest_item = opf_root.find(f".//opf:item[@id='{idref}']", NS)
        if manifest_item is None:
            manifest_item = opf_root.find(f".//{_q('opf','item')}[@id='{idref}']")
        if manifest_item is not None:
            href = manifest_item.get("href", "")
            if href.endswith(".html") or href.endswith(".xhtml") or href.endswith(".htm"):
                spine_items.append(href)

    return opf_dir, {"meta": meta, "cover_href": cover_href, "spine": spine_items}


def _strip_html(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, re.IGNORECASE)
    text = re.sub(r"</h[1-6]>", "\n\n", text, re.IGNORECASE)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _unhtml_entity(text: str) -> str:
    import html
    return html.unescape(text)


def read_epub(epub_path: Path) -> dict:
    """Return {metadata, chapters: [(title, html_content), ...], cover: bytes|None}"""
    with zipfile.ZipFile(epub_path, "r") as zf:
        names = zf.namelist()
        container_xml = next((n for n in names if n.endswith("container.xml")), None)
        if container_xml is None:
            return {"metadata": {}, "chapters": [], "cover": None}

        opf_dir, info = _parse_meta(zf.extract(container_xml, "/tmp/_epub_tmp"))
        opf_dir = Path(opf_dir)

        chapters = []
        for href in info["spine"]:
            try:
                raw = (opf_dir / href).read_text(encoding="utf-8", errors="replace")
                # Extract <title> or first <h1>/<h2>
                title = ""
                t = re.search(r"<title[^>]*>(.*?)</title>", raw, re.DOTALL | re.IGNORECASE)
                if t: title = _unhtml_entity(t.group(1).strip())
                if not title:
                    t = re.search(r"<h[12][^>]*>(.*?)</h[12]>", raw, re.DOTALL | re.IGNORECASE)
                    if t: title = _strip_html(t.group(1)).strip()
                chapters.append((title or f"Chapter {len(chapters)+1}", raw))
            except FileNotFoundError:
                pass

        # Cover image
        cover_data = None
        if info["cover_href"]:
            cover_path = opf_dir / info["cover_href"]
            if cover_path.exists():
                cover_data = cover_path.read_bytes()

    return {
        "metadata": info["meta"],
        "chapters": chapters,
        "cover": cover_data,
    }


# ── 轉換目標 ─────────────────────────────────────────────────────────────────

def to_txt(epub_path: Path, out_path: Path = None) -> Path:
    book = read_epub(epub_path)
    meta = book["metadata"]
    lines = []

    if meta.get("title"):
        lines.append(f"{'='*60}")
        lines.append(f"  《{meta['title']}》")
        if meta.get("creator"):
            lines.append(f"  作者：{meta['creator']}")
        lines.append(f"{'='*60}\n")

    for title, html in book["chapters"]:
        text = _strip_html(html)
        text = _unhtml_entity(text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        if text.strip():
            lines.append(f"\n{'─'*40}")
            if title:
                lines.append(f"  {title}")
            lines.append(f"{'─'*40}\n")
            lines.append(text)

    out = out_path or epub_path.with_suffix(".txt")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def to_markdown(epub_path: Path, out_path: Path = None) -> Path:
    book = read_epub(epub_path)
    meta = book["metadata"]
    lines = []

    if meta.get("title"):
        lines.append(f"# {meta['title']}")
        if meta.get("creator"):
            lines.append(f"\n**作者：** {meta['creator']}")
        if meta.get("publisher"):
            lines.append(f"**出版社：** {meta['publisher']}")
        lines.append("\n---\n")

    for title, html in book["chapters"]:
        text = _strip_html(html)
        text = _unhtml_entity(text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        if text.strip():
            lines.append(f"\n## {title or 'Chapter'}\n")
            lines.append(text)

    out = out_path or epub_path.with_suffix(".md")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def to_html_single(epub_path: Path, out_path: Path = None) -> Path:
    book = read_epub(epub_path)
    meta = book["metadata"]

    css = """
    body { font-family: -apple-system, 'PingFang TC', 'Microsoft JhengHei', sans-serif;
           max-width: 720px; margin: 2rem auto; padding: 0 1.5rem;
           line-height: 1.8; color: #333; }
    h1 { color: #1a1a1a; border-bottom: 2px solid #1a1a1a; padding-bottom: 0.5rem; }
    h2 { color: #2c2c2c; margin-top: 2rem; }
    .meta { color: #666; font-size: 0.9rem; margin-bottom: 2rem; }
    .chapter { margin-bottom: 2rem; }
    blockquote { border-left: 4px solid #ddd; margin-left: 0; padding-left: 1rem; color: #555; }
    img { max-width: 100%; }
    """

    html_parts = [
        "<!DOCTYPE html>",
        f"<html lang='{meta.get('language','zh')}'>",
        "<head>",
        f"<meta charset='utf-8'>",
        f"<title>{meta.get('title', epub_path.stem)}</title>",
        f"<style>{css}</style>",
        "</head>",
        "<body>",
    ]

    if meta.get("title"):
        html_parts.append(f"<h1>{meta['title']}</h1>")
        meta_parts = []
        if meta.get("creator"):  meta_parts.append(f"作者：{meta['creator']}")
        if meta.get("publisher"): meta_parts.append(f"出版社：{meta['publisher']}")
        if meta_parts:
            html_parts.append(f"<p class='meta'>{' | '.join(meta_parts)}</p>")
        html_parts.append("<hr>")

    for i, (title, content) in enumerate(book["chapters"], 1):
        if title:
            html_parts.append(f"<div class='chapter'>")
            html_parts.append(f"<h2>{i}. {title}</h2>")
        # Keep basic HTML tags for headings/paragraphs
        clean_html = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL|re.I)
        clean_html = re.sub(r"<style[^>]*>.*?</style>", "", clean_html, flags=re.DOTALL|re.I)
        html_parts.append(clean_html)
        if title:
            html_parts.append("</div>")

    html_parts.extend(["</body>", "</html>"])

    out = out_path or epub_path.with_suffix(".html")
    out.write_text("\n".join(html_parts), encoding="utf-8")
    return out


def to_json(epub_path: Path, out_path: Path = None) -> Path:
    book = read_epub(epub_path)
    out = out_path or epub_path.with_suffix(".json")
    data = {
        "file": str(epub_path),
        "converted_at": datetime.now().isoformat(),
        **book,
        "chapters": [(t, _strip_html(h)) for t, h in book["chapters"]],
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def extract_cover(epub_path: Path, out_path: Path = None) -> Path | None:
    book = read_epub(epub_path)
    if not book["cover"]:
        return None
    title = book["metadata"].get("title", epub_path.stem)
    ext = ".jpg"
    if book["cover"].startswith(b"\x89PNG"): ext = ".png"
    elif book["cover"].startswith(b"\xff\xd8"): ext = ".jpg"
    out = out_path or epub_path.with_suffix(f"_cover{ext}")
    out.write_bytes(book["cover"])
    return out


# ── CLI ──────────────────────────────────────────────────────────────────────

FORMATS = ["txt", "md", "html", "json"]


def main():
    parser = argparse.ArgumentParser(
        description="📖 EPUB 萬用轉換器 — EPUB → TXT / Markdown / HTML / JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", type=Path, help="輸入 EPUB 檔案")
    parser.add_argument("-o", "--output", type=Path, help="輸出檔案（目錄或檔名）")
    parser.add_argument("-f", "--format", choices=FORMATS, default="txt",
                        help="輸出格式（預設：txt）")
    parser.add_argument("--cover", action="store_true",
                        help="僅擷取封面圖片並儲存")
    parser.add_argument("--batch", action="store_true",
                        help="batch mode: input is a directory")
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg):
        if not args.quiet:
            print(msg)

    if args.batch:
        dirs = [args.input] if args.input.is_dir() else [args.input.parent]
        files = list(args.input.glob("*.epub")) if args.input.is_dir() else [args.input]
        if not files:
            print(f"❌ 目錄中找不到 EPUB 檔案：{args.input}")
            sys.exit(1)
        out_dir = args.output or args.input
        out_dir.mkdir(parents=True, exist_ok=True)

        converters = {"txt": to_txt, "md": to_markdown, "html": to_html_single, "json": to_json}
        convert = converters[args.format]

        success, failed = 0, []
        for f in files:
            try:
                out = convert(f, out_dir / (f.stem + "." + args.format))
                log(f"✅ {f.name} → {out.name}")
                success += 1
            except Exception as e:
                log(f"❌ {f.name}: {e}")
                failed.append(f.name)

        print(f"\n📦 批量完成：{success}/{len(files)} 成功" +
              (f"，失敗：{', '.join(failed)}" if failed else ""))

    elif args.cover:
        out = extract_cover(args.input)
        if out:
            log(f"✅ 封面已儲存：{out}")
        else:
            print(f"❌ 無法擷取封面：{args.input}")

    else:
        converters = {"txt": to_txt, "md": to_markdown, "html": to_html_single, "json": to_json}
        out = converters[args.format](args.input, args.output)
        log(f"✅ 已轉換：{out}")

        if args.format == "html":
            size = out.stat().st_size
            log(f"   📄 {size/1024:.1f} KB")


if __name__ == "__main__":
    main()
