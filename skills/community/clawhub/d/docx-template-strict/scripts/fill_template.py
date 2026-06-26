#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fill_template.py

Strict template filler for DOCX.
- Preserves template layout by editing the underlying XML (word/document.xml)
- Replaces {{TOKEN}} placeholders with text
- Optionally replaces paragraph-only {{FIGn}} placeholders with an inline image (adds to word/media and relationships)

This is intentionally conservative: it avoids restructuring paragraphs/sections.

Usage:
  python3 fill_template.py --template T.docx --out OUT.docx --data data.json

Data JSON:
  {
    "TITLE_CN": "...",
    "REFERENCES": "[1] ...\n[2] ...",
    "FIG1": {"path": "/abs/path/to/fig.png"}
  }
"""

import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Optional

from lxml import etree

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "rels": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class DocxParts:
    document_xml: bytes
    document_rels_xml: bytes


def read_parts(docx_path: Path) -> DocxParts:
    with zipfile.ZipFile(docx_path, "r") as z:
        doc = z.read("word/document.xml")
        rels = z.read("word/_rels/document.xml.rels")
    return DocxParts(document_xml=doc, document_rels_xml=rels)


def write_docx_from_template(template_path: Path, out_path: Path, patch_fn) -> None:
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()

    with zipfile.ZipFile(template_path, "r") as zin, zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        # copy all first
        for item in zin.infolist():
            data = zin.read(item.filename)
            zout.writestr(item, data)

        # patch in-place by rewriting the same members
        patch_fn(zin, zout)

    tmp.replace(out_path)


def load_data(data_path: Path) -> Dict:
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def replace_tokens_in_text(text: str, data: Dict) -> str:
    def repl(m):
        key = m.group(1)
        val = data.get(key)
        if val is None:
            return m.group(0)
        if isinstance(val, (dict, list)):
            # images handled separately; leave token
            return m.group(0)
        return str(val)

    return TOKEN_RE.sub(repl, text)


def iter_text_nodes(root):
    # all w:t text nodes
    return root.xpath("//w:t", namespaces=NS)


def get_sectpr_count(root) -> int:
    return len(root.xpath("//w:sectPr", namespaces=NS))


def patch_document_xml(doc_xml: bytes, data: Dict) -> Tuple[bytes, int, int]:
    root = etree.fromstring(doc_xml)
    before_sect = get_sectpr_count(root)

    # token replacement at text-node granularity
    for t in iter_text_nodes(root):
        if t.text and "{{" in t.text and "}}" in t.text:
            t.text = replace_tokens_in_text(t.text, data)

    after_sect = get_sectpr_count(root)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"), before_sect, after_sect


def rels_next_rid(rels_root) -> str:
    ids = []
    for rel in rels_root.xpath("//rels:Relationship", namespaces=NS):
        rid = rel.get("Id")
        if rid and rid.startswith("rId"):
            try:
                ids.append(int(rid[3:]))
            except ValueError:
                pass
    n = max(ids) + 1 if ids else 1
    return f"rId{n}"


def media_next_image_name(existing: set, ext: str) -> str:
    i = 1
    while True:
        name = f"image{i}.{ext}"
        if name not in existing:
            return name
        i += 1


def detect_existing_media(zin: zipfile.ZipFile) -> set:
    names = set()
    for n in zin.namelist():
        if n.startswith("word/media/"):
            names.add(Path(n).name)
    return names


def build_inline_image_drawing(rid: str, filename: str, cx: int, cy: int) -> etree._Element:
    # Minimal inline drawing for WordprocessingML.
    # cx,cy in EMU.
    # NOTE: This keeps it simple; templates can style the paragraph; image sizing can be adjusted.
    
    w = "{" + NS['w'] + "}"
    r = "{" + NS['r'] + "}"
    wp = "{" + NS['wp'] + "}"
    a = "{" + NS['a'] + "}"
    pic = "{" + NS['pic'] + "}"

    drawing = etree.Element(w + "drawing")
    inline = etree.SubElement(drawing, wp + "inline")
    etree.SubElement(inline, wp + "extent", cx=str(cx), cy=str(cy))
    etree.SubElement(inline, wp + "effectExtent", l="0", t="0", r="0", b="0")
    docPr = etree.SubElement(inline, wp + "docPr", id="1", name=filename)
    etree.SubElement(inline, wp + "cNvGraphicFramePr")

    graphic = etree.SubElement(inline, a + "graphic")
    graphicData = etree.SubElement(graphic, a + "graphicData", uri=NS["pic"])

    pic_el = etree.SubElement(graphicData, pic + "pic")
    nvPicPr = etree.SubElement(pic_el, pic + "nvPicPr")
    etree.SubElement(nvPicPr, pic + "cNvPr", id="0", name=filename)
    etree.SubElement(nvPicPr, pic + "cNvPicPr")

    blipFill = etree.SubElement(pic_el, pic + "blipFill")
    blip = etree.SubElement(blipFill, a + "blip")
    blip.set(r + "embed", rid)
    stretch = etree.SubElement(blipFill, a + "stretch")
    etree.SubElement(stretch, a + "fillRect")

    spPr = etree.SubElement(pic_el, pic + "spPr")
    xfrm = etree.SubElement(spPr, a + "xfrm")
    etree.SubElement(xfrm, a + "off", x="0", y="0")
    etree.SubElement(xfrm, a + "ext", cx=str(cx), cy=str(cy))
    prstGeom = etree.SubElement(spPr, a + "prstGeom", prst="rect")
    etree.SubElement(prstGeom, a + "avLst")

    return drawing


def patch_figures(doc_xml: bytes, rels_xml: bytes, zin: zipfile.ZipFile, zout: zipfile.ZipFile, data: Dict) -> Tuple[bytes, bytes]:
    # Replace paragraphs that contain only {{FIGn}} with an image drawing.
    doc_root = etree.fromstring(doc_xml)
    rels_root = etree.fromstring(rels_xml)

    existing_media = detect_existing_media(zin)

    # find paragraphs
    paras = doc_root.xpath("//w:p", namespaces=NS)

    def para_text(p) -> str:
        ts = p.xpath(".//w:t", namespaces=NS)
        return "".join([t.text or "" for t in ts]).strip()

    for p in paras:
        t = para_text(p)
        m = re.fullmatch(r"\{\{(FIG\d+)\}\}", t)
        if not m:
            continue
        key = m.group(1)
        spec = data.get(key)
        if not isinstance(spec, dict) or "path" not in spec:
            continue

        img_path = Path(spec["path"]).expanduser()
        if not img_path.exists():
            raise FileNotFoundError(f"Image for {key} not found: {img_path}")

        ext = img_path.suffix.lower().lstrip(".")
        if ext not in ("png", "jpg", "jpeg"):
            raise ValueError(f"Unsupported image type: {img_path.suffix}. Use png/jpg/jpeg")
        if ext == "jpeg":
            ext = "jpg"

        img_name = media_next_image_name(existing_media, ext)
        existing_media.add(img_name)
        target = f"word/media/{img_name}"

        # add media file
        zout.writestr(target, img_path.read_bytes())

        # add relationship
        rid = rels_next_rid(rels_root)
        rel = etree.SubElement(rels_root, "{" + NS['rels'] + "}Relationship")
        rel.set("Id", rid)
        rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
        rel.set("Target", f"media/{img_name}")

        # replace paragraph content with drawing
        # Clear existing children and create: w:r / w:drawing
        for child in list(p):
            p.remove(child)

        r_el = etree.SubElement(p, "{" + NS['w'] + "}r")
        # size default: 4.2 inch width; preserve aspect if provided later
        # 1 inch = 914400 EMU
        cx = int(4.2 * 914400)
        cy = int(3.0 * 914400)
        drawing = build_inline_image_drawing(rid, img_name, cx, cy)
        r_el.append(drawing)

    return (
        etree.tostring(doc_root, xml_declaration=True, encoding="UTF-8", standalone="yes"),
        etree.tostring(rels_root, xml_declaration=True, encoding="UTF-8", standalone="yes"),
    )


def scan_unreplaced_tokens(doc_xml: bytes) -> Dict[str, int]:
    root = etree.fromstring(doc_xml)
    counts = {}
    for t in iter_text_nodes(root):
        if not t.text:
            continue
        for m in TOKEN_RE.finditer(t.text):
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--data', required=True)
    args = ap.parse_args()

    template = Path(args.template)
    out = Path(args.out)
    data = load_data(Path(args.data))

    def patch(zin, zout):
        parts = read_parts(template)
        patched_doc, before_sect, after_sect = patch_document_xml(parts.document_xml, data)
        if before_sect != after_sect:
            raise RuntimeError(f"Template sectPr count changed ({before_sect} -> {after_sect}); refusing to write.")

        # figures
        patched_doc2, patched_rels2 = patch_figures(patched_doc, parts.document_rels_xml, zin, zout, data)

        # final QA: tokens left
        left = scan_unreplaced_tokens(patched_doc2)
        # allow tokens that correspond to FIGn_CAPTION tokens if user didn't provide (but they should)
        if left:
            raise RuntimeError(f"Unreplaced tokens remain: {left}")

        # rewrite members
        zout.writestr('word/document.xml', patched_doc2)
        zout.writestr('word/_rels/document.xml.rels', patched_rels2)

    write_docx_from_template(template, out, patch)


if __name__ == '__main__':
    main()
