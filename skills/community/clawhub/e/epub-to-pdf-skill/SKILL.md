---
name: epub-to-pdf
description: "Convert EPUB e-books to PDF using ebooklib + WeasyPrint with proper CJK font support."
---

# EPUB → PDF

Convert `.epub` files to PDF. Works for Chinese/Japanese/Korean text.

## Prerequisites

```bash
apt-get install -y weasyprint
pip3 install --break-system-packages ebooklib beautifulsoup4 lxml
```

CJK fonts required:
- `/root/.openclaw/workspace/skills/pdf-maker/NotoSansCJKsc.ttf`
- `/root/.openclaw/workspace/skills/pdf-maker/NotoSansCJKscB.ttf`

## Usage

```bash
python3 scripts/epub2pdf.py <input.epub> <output.pdf>
```

## How it works

1. `ebooklib` reads all `ITEM_DOCUMENT` entries from the EPUB
2. `BeautifulSoup + lxml` strips `<script>`, `<style>`, `<link>`, `<meta>` tags
3. Injects CJK fonts via `@font-face` CSS
4. `WeasyPrint` renders combined HTML to A4 PDF (2cm margins, justified)

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| WeasyPrint import fails | `apt-get install weasyprint` |
| CJK characters garbled | Ensure font TTF path is correct (TTC collections won't work) |
| Empty / tiny PDF | EPUB has no readable document entries — check TNC count |
| calibre root sandbox error | Don't use calibre; use this script instead |
