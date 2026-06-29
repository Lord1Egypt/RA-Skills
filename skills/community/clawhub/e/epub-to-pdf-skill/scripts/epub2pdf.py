#!/usr/bin/env python3
"""
EPUB → PDF via ebooklib + BeautifulSoup + WeasyPrint.

Usage:
    python3 epub2pdf.py <input.epub> <output.pdf>

Dependencies:
    apt-get install -y weasyprint
    pip3 install --break-system-packages ebooklib beautifulsoup4 lxml

Requires CJK fonts at:
    /root/.openclaw/workspace/skills/pdf-maker/NotoSansCJKsc.ttf
    /root/.openclaw/workspace/skills/pdf-maker/NotoSansCJKscB.ttf
"""
import sys, os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS


def find_fonts():
    candidates = [
        ("/root/.openclaw/workspace/skills/pdf-maker/NotoSansCJKsc.ttf",
         "/root/.openclaw/workspace/skills/pdf-maker/NotoSansCJKscB.ttf"),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    ]
    for reg, bold in candidates:
        if os.path.isfile(reg):
            return reg, bold
    return None, None


def convert(in_path: str, out_path: str) -> str:
    font_reg, font_bold = find_fonts()
    if not font_reg:
        raise FileNotFoundError(
            "CJK font not found. Place NotoSansCJKsc.ttf at "
            "/root/.openclaw/workspace/skills/pdf-maker/"
        )

    print(f"📖 Reading EPUB: {in_path}")
    book = epub.read_epub(in_path)
    docs = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    print(f"  Chapters found: {len(docs)}")

    pages_html = []
    for item in docs:
        raw = item.get_content().decode("utf-8", errors="ignore")
        if not raw.strip():
            continue
        soup = BeautifulSoup(raw, "lxml")
        for tag in soup(["script", "style", "link", "meta"]):
            tag.decompose()
        body = soup.find("body")
        pages_html.append(
            "".join(str(c) for c in body.contents) if body else str(soup)
        )

    print(f"  Non-empty pages: {len(pages_html)}")

    # Inject CSS stylesheet with CJK font faces
    css_template = f"""<style>
@font-face {{ font-family: "NotoSC"; src: url("file://{font_reg}") format("truetype"); }}
@font-face {{ font-family: "NotoSC"; src: url("file://{font_bold}") format("truetype"); font-weight: bold; }}
@page {{
    size: A4;
    margin: 2cm 1.8cm;
    @bottom-center {{
        content: counter(page);
        font-family: "NotoSC";
        font-size: 9pt;
        color: #888;
    }}
}}
body {{
    font-family: "NotoSC", sans-serif;
    font-size: 12pt;
    line-height: 1.8;
    color: #222;
    text-align: justify;
}}
h1 {{ text-align: center; font-size: 22pt; margin: 2em 0 1em; border-bottom: 3px solid #333; padding-bottom: 0.5em; page-break-after: avoid; }}
h2 {{ font-size: 16pt; margin-top: 1.5em; border-left: 5px solid #555; padding-left: 0.8em; page-break-after: avoid; }}
h3 {{ font-size: 14pt; margin-top: 1em; page-break-after: avoid; }}
p {{ text-indent: 2em; margin: 0.6em 0; }}
img {{ max-width: 100%; height: auto; display: block; margin: 1em auto; }}
table {{ width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 10pt; }}
td, th {{ border: 1px solid #999; padding: 0.4em; text-align: left; }}
</style>"""

    combined = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
{css_template}
</head>
<body>
{"".join(pages_html)}
</body>
</html>"""

    with open("/tmp/epub_combined.html", "w", encoding="utf-8") as f:
        f.write(combined)
    print(f"🌐 Combined HTML: {len(combined):,} bytes")

    print(f"🖨️ Rendering PDF → {out_path}")
    html = HTML(filename="/tmp/epub_combined.html")
    html.write_pdf(out_path)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"✅ Done: {out_path}  ({size_kb:.0f} KB)")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.epub> <output.pdf>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
