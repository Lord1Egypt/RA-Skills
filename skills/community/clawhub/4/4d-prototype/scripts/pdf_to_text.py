#!/usr/bin/env python3
"""Convert a PDF into plain text separated by page, trying the available methods in turn:

    1. the pdftotext (poppler) command line
    2. pypdf
    3. PyMuPDF (fitz)
    4. macOS's built-in PDFKit (via osascript JXA, nothing to install)

Usage:
    python3 -I pdf_to_text.py <file.pdf> <out.txt>

Each page in the output starts with "=== PAGE n". If a scan yields no text, look at the page images with the Read tool's pages parameter.
"""
import importlib
import json
import shutil
import subprocess
import sys


def via_pdftotext(src):
    if not shutil.which('pdftotext'):
        return None
    pages = []
    i = 1
    while True:
        r = subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), src, '-'], capture_output=True, text=True)
        if r.returncode != 0:
            break
        pages.append(r.stdout)
        i += 1
        if i > 5000:
            break
    return pages or None


def via_pypdf(src):
    try:
        pypdf = importlib.import_module('pypdf')
    except ImportError:
        return None
    reader = pypdf.PdfReader(src)
    return [p.extract_text() or '' for p in reader.pages]


def via_fitz(src):
    try:
        fitz = importlib.import_module('fitz')
    except ImportError:
        return None
    doc = fitz.open(src)
    return [page.get_text() for page in doc]


JXA = r'''
ObjC.import("PDFKit");
function run(argv) {
  var d = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[0]));
  if (!d) return JSON.stringify(null);
  var out = [];
  for (var i = 0; i < d.pageCount; i++) out.push(d.pageAtIndex(i).string.js || "");
  return JSON.stringify(out);
}
'''


def via_pdfkit(src):
    if sys.platform != 'darwin' or not shutil.which('osascript'):
        return None
    r = subprocess.run(['osascript', '-l', 'JavaScript', '-e', JXA, src], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dest = sys.argv[1], sys.argv[2]
    for name, fn in (('pdftotext', via_pdftotext), ('pypdf', via_pypdf), ('fitz', via_fitz), ('PDFKit', via_pdfkit)):
        try:
            pages = fn(src)
        except Exception as e:  # if one method fails, try the next
            print(f'{name} failed: {e}', file=sys.stderr)
            continue
        if pages:
            with open(dest, 'w', encoding='utf-8') as f:
                for i, t in enumerate(pages, 1):
                    f.write(f'=== PAGE {i}\n{t}\n')
            chars = sum(len(t.strip()) for t in pages)
            print(f'{name}: {len(pages)} pages, {chars} characters → {dest}')
            if chars < 20 * len(pages):
                print('Very little text — probably a scan: view the page images with the Read tool\'s pages parameter.')
            return
    sys.exit('No PDF text extraction method available: install poppler (pdftotext) or pypdf, or view the pages with the Read tool\'s pages parameter.')


if __name__ == '__main__':
    main()
