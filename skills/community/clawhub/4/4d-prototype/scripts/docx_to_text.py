#!/usr/bin/env python3
"""Convert a .docx requirement document into readable plain text and extract embedded images and attachments.

Usage:
    python3 -I docx_to_text.py <file.docx> [--out <dir>]

Output:
    - stdout (or <dir>/document.txt): paragraphs (prefixed with [style numbering-level]), tables (| separated, wrapped in <<TABLE>>),
      and position markers [image/object] for images / embedded objects.
    - <dir>/media/: images in the document (page sketches, system screenshots); view them one by one with Read.
    - <dir>/embeddings/: embedded attachments (e.g. a data template xlsx); inspect them further with xlsx_inspect.py.

Standard library only; the source file is never modified.
"""
import argparse
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def para_text(p):
    out = []
    for node in p.iter():
        tag = node.tag
        if tag == W + 't' and node.text:
            out.append(node.text)
        elif tag == W + 'tab':
            out.append('\t')
        elif tag == W + 'br':
            out.append('\n')
        elif tag.endswith('}drawing') or tag.endswith('}object') or tag.endswith('}pict'):
            out.append('[image/object]')
    return ''.join(out)


def para_style(p):
    ppr = p.find(W + 'pPr')
    if ppr is None:
        return ''
    parts = []
    s = ppr.find(W + 'pStyle')
    if s is not None:
        parts.append(s.get(W + 'val') or '')
    num = ppr.find(W + 'numPr')
    if num is not None:
        il = num.find(W + 'ilvl')
        parts.append('num' + (il.get(W + 'val') if il is not None else ''))
    return ' '.join(x for x in parts if x)


def render(body):
    lines = []
    for el in body:
        if el.tag == W + 'p':
            t = para_text(el)
            if t.strip():
                st = para_style(el)
                lines.append(f'[{st}] {t}' if st else t)
        elif el.tag == W + 'tbl':
            lines.append('<<TABLE>>')
            for tr in el.iter(W + 'tr'):
                cells = []
                for tc in tr.findall(W + 'tc'):
                    cells.append(' / '.join(para_text(p) for p in tc.iter(W + 'p') if para_text(p).strip()))
                lines.append(' | '.join(cells))
            lines.append('<<END TABLE>>')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('docx')
    ap.add_argument('--out', help='output directory: writes document.txt and extracts media/ and embeddings/')
    args = ap.parse_args()

    try:
        z = zipfile.ZipFile(args.docx)
    except (zipfile.BadZipFile, FileNotFoundError) as e:
        sys.exit(f'cannot open {args.docx}: {e} (save legacy .doc files as .docx first)')

    root = ET.fromstring(z.read('word/document.xml'))
    text = render(root.find(W + 'body'))

    if not args.out:
        print(text)
        return

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, 'document.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    extracted = {'media': [], 'embeddings': []}
    for name in z.namelist():
        for kind in extracted:
            prefix = f'word/{kind}/'
            if name.startswith(prefix) and not name.endswith('/'):
                dest = os.path.join(args.out, kind, os.path.basename(name))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, 'wb') as f:
                    f.write(z.read(name))
                extracted[kind].append(dest)
    print(f'document.txt: {len(text.splitlines())} lines → {os.path.join(args.out, "document.txt")}')
    for kind, files in extracted.items():
        print(f'{kind}: {len(files)} files')
        for p in files:
            print('  ', p)


if __name__ == '__main__':
    main()
