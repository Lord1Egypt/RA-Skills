#!/usr/bin/env python3
"""Convert EPUB/MOBI files to PDF using ebooklib + weasyprint."""
import sys, os, glob
from ebooklib import epub
from weasyprint import HTML

def epub_to_pdf(epub_path, pdf_path=None):
    """Convert an EPUB file to PDF."""
    if pdf_path is None:
        pdf_path = epub_path.rsplit('.', 1)[0] + '.pdf'
    
    print(f"Converting: {epub_path} -> {pdf_path}")
    
    book = epub.read_epub(epub_path)
    
    html_parts = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_content().decode('utf-8', errors='ignore')
        html_parts.append(content)
    
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif; 
                   font-size: 11pt; line-height: 1.8; max-width: 700px; margin: 0 auto; padding: 40px; }}
            h1, h2, h3 {{ font-weight: bold; margin-top: 1.5em; }}
            p {{ text-indent: 2em; margin: 0.5em 0; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>{''.join(html_parts)}</body>
    </html>
    """
    
    HTML(string=full_html).write_pdf(pdf_path)
    size_mb = os.path.getsize(pdf_path) / (1024*1024)
    print(f"Done: {pdf_path} ({size_mb:.1f} MB)")
    return pdf_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: epub_to_pdf.py <file.epub|file.mobi> [output.pdf]")
        print("       epub_to_pdf.py --batch <directory>")
        sys.exit(1)
    
    if sys.argv[1] == '--batch':
        directory = sys.argv[2] if len(sys.argv) > 2 else '.'
        for ext in ('*.epub', '*.mobi'):
            for f in glob.glob(os.path.join(directory, ext)):
                try:
                    epub_to_pdf(f)
                except Exception as e:
                    print(f"Failed: {f} - {e}")
    else:
        epub_to_pdf(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
