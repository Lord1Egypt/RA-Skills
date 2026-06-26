#!/usr/bin/env python3
"""
docx-chapter 脚注 URL 超链接化后处理
将 Pandoc 生成的 DOCX 脚注中的纯文本 URL 转换为可点击的 <w:hyperlink>。
"""

import re
import sys
import shutil
import zipfile
import tempfile
import hashlib
import copy
from pathlib import Path
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

# 含中文标点的 URL 提取正则
URL_RE = re.compile(r'https?://[^\s<>"」。，；：\!\?」』（）、《》【】…—～０-９\[()]+')


def url_index(url: str) -> str:
    """Generate a safe rId suffix from URL hash (8 hex chars).
    rId must be a valid XML NCName; raw URLs contain /:?=&%# which are illegal."""
    return hashlib.md5(url.rstrip('/').encode()).hexdigest()[:8]


def process_footnotes(footnotes_path: str, rels_elems: list) -> etree.Element:
    """Transform footnote XML, adding hyperlinks around bare URLs."""
    tree = etree.parse(footnotes_path)
    root = tree.getroot()

    for fn_elem in root.findall('.//w:footnote', NS):
        fn_id = fn_elem.get(f'{{{NS["w"]}}}id', '')
        fn_type = fn_elem.get(f'{{{NS["w"]}}}type', '')
        if fn_id in ('0', '-1') or fn_type in ('separator', 'continuationSeparator', 'continuationNotice'):
            continue

        # Check existing hyperlinks for missing r:id
        for hl_elem in fn_elem.iter(f'{{{NS["w"]}}}hyperlink'):
            rid_attr = hl_elem.get(f'{{{NS["r"]}}}id')
            if not rid_attr and hl_elem.get(f'{{{NS["w"]}}}history') is None:
                print(f"Warning: hyperlink without r:id in footnote {fn_id}", file=sys.stderr)

        # Collect all <w:r> and <w:t> elements, wrap URLs in hyperlinks
        runs = fn_elem.findall('.//w:r', NS)
        for run in runs:
            t_elems = run.findall(f'w:t', NS)
            if not t_elems:
                continue

            for t_elem in t_elems:
                if not (t_elem.text and t_elem.text.strip()):
                    continue

                # Process URLs one at a time — while-loop handles multiple URLs in same run
                while True:
                    urls = URL_RE.findall(t_elem.text or '')
                    if not urls:
                        break

                    url = urls[0]  # process first URL
                    raw = t_elem.text
                    url_start = raw.find(url)
                    url_end = url_start + len(url)

                    parent = run.getparent()
                    run_idx = list(parent).index(run)

                    # Cache rPr and xml:space for reuse
                    rPr = run.find(f'{{{NS["w"]}}}rPr')
                    xml_space = t_elem.get('{http://www.w3.org/XML/1998/namespace}space')

                    # Text before URL → new run (copy rPr to preserve formatting)
                    if url_start > 0:
                        before_run = etree.Element(f'{{{NS["w"]}}}r')
                        if rPr is not None:
                            before_run.append(copy.deepcopy(rPr))
                        before_t = etree.SubElement(before_run, f'{{{NS["w"]}}}t')
                        before_t.text = raw[:url_start]
                        if xml_space:
                            before_t.set('{http://www.w3.org/XML/1998/namespace}space', xml_space)
                        parent.insert(run_idx, before_run)
                        run_idx += 1

                    # Hyperlink for the URL
                    hl = etree.SubElement(parent, f'{{{NS["w"]}}}hyperlink')
                    hl.set(f'{{{NS["r"]}}}id',
                           f'rId_url_{url_index(url)}')
                    parent.insert(run_idx, hl)
                    run_idx += 1

                    hl_run = etree.SubElement(hl, f'{{{NS["w"]}}}r')
                    # Apply Hyperlink character style for blue underline appearance
                    hl_rPr = copy.deepcopy(rPr) if rPr is not None else etree.Element(f'{{{NS["w"]}}}rPr')
                    hl_style = hl_rPr.find(f'{{{NS["w"]}}}rStyle')
                    if hl_style is None:
                        hl_style = etree.SubElement(hl_rPr, f'{{{NS["w"]}}}rStyle')
                    hl_style.set(f'{{{NS["w"]}}}val', 'Hyperlink')
                    hl_run.append(hl_rPr)
                    hl_t = etree.SubElement(hl_run, f'{{{NS["w"]}}}t')
                    hl_t.text = url
                    if xml_space:
                        hl_t.set('{http://www.w3.org/XML/1998/namespace}space', xml_space)

                    # Add relationship
                    rels_elems.append({
                        "Id": f"rId_url_{url_index(url)}",
                        "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                        "Target": url,
                        "TargetMode": "External",
                    })

                    # After URL: update t_elem.text to remainder, or remove run
                    if url_end < len(raw):
                        t_elem.text = raw[url_end:]
                        # continue while loop for remaining URLs in this run
                    else:
                        parent.remove(run)
                        break  # run removed, exit while loop

    return root


def update_rels(rels_path: str, new_rels: list[dict]):
    """Add relationships to word/_rels/footnotes.xml.rels."""
    tree = etree.parse(rels_path)
    root = tree.getroot()
    existing_ids = {r.get('Id') for r in root.findall(f'{{{NS["rel"]}}}Relationship')}

    for rel in new_rels:
        if rel["Id"] in existing_ids:
            continue
        elem = etree.SubElement(root, f'{{{NS["rel"]}}}Relationship')
        elem.set('Id', rel["Id"])
        elem.set('Type', rel["Type"])
        elem.set('Target', rel["Target"])
        elem.set('TargetMode', rel["TargetMode"])
        existing_ids.add(rel["Id"])

    tree.write(rels_path, xml_declaration=True, encoding='UTF-8', standalone=True)


def deduplicate_footnotes(all_files: dict) -> int:
    """Merge duplicate footnote entries (same text, different IDs) created by pandoc.
    Pandoc creates a new footnote entry for each inline reference, even for the same [^N].
    This merges them so each unique footnote text appears only once."""
    fn_xml = all_files.get('word/footnotes.xml')
    doc_xml = all_files.get('word/document.xml')
    if not fn_xml or not doc_xml:
        return 0

    fn_tree = etree.fromstring(fn_xml)
    doc_tree = etree.fromstring(doc_xml)

    # ── 1. Collect footnote entries with their normalized text ──
    fn_entries = {}  # id → (text, element)
    for fn_elem in fn_tree.findall(f'.//{{{NS["w"]}}}footnote'):
        fid = int(fn_elem.get(f'{{{NS["w"]}}}id', '-1'))
        if fid <= 0:
            continue
        texts = []
        for t in fn_elem.iter(f'{{{NS["w"]}}}t'):
            if t.text:
                texts.append(t.text)
        # Normalize: strip leading number-space, collapse whitespace
        full = ' '.join(texts)
        # Strip leading whitespace+number+dot pattern that pandoc adds
        normalized = full.strip()
        fn_entries[fid] = (normalized, fn_elem)

    # ── 2. Group by normalized text ──
    text_groups = {}  # normalized_text → [ids]
    for fid, (text, _) in fn_entries.items():
        text_groups.setdefault(text, []).append(fid)

    # ── 3. Build ID remap: duplicate → canonical (smallest ID) ──
    remap = {}
    merged = 0
    for text, ids in text_groups.items():
        if len(ids) > 1:
            canonical = min(ids)
            for fid in ids:
                if fid != canonical:
                    remap[fid] = canonical
                    merged += 1

    if merged == 0:
        return 0

    # ── 4. Rewrite document.xml footnoteReference IDs ──
    refs_changed = 0
    for ref in doc_tree.iter(f'{{{NS["w"]}}}footnoteReference'):
        old_id = int(ref.get(f'{{{NS["w"]}}}id', '0'))
        if old_id in remap:
            ref.set(f'{{{NS["w"]}}}id', str(remap[old_id]))
            refs_changed += 1

    # ── 5. Remove duplicate footnote entries from footnotes.xml ──
    fn_body = fn_tree  # The root is <w:footnotes>
    for fn_elem in list(fn_tree.findall(f'.//{{{NS["w"]}}}footnote')):
        fid = int(fn_elem.get(f'{{{NS["w"]}}}id', '-1'))
        if fid in remap:
            fn_body.remove(fn_elem)

    # Write back
    all_files['word/footnotes.xml'] = etree.tostring(fn_tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    all_files['word/document.xml'] = etree.tostring(doc_tree, xml_declaration=True, encoding='UTF-8', standalone=True)

    return merged


def separate_consecutive_footnotes(doc_data: bytes) -> bytes:
    """Insert a comma between adjacent <w:r> that both contain <w:footnoteReference>.
    Without this, Pandoc renders [^0][^1] as ¹² (no gap)."""
    doc_tmp = tempfile.NamedTemporaryFile(suffix='.xml', delete=False)
    doc_tmp.write(doc_data)
    doc_tmp.close()

    tree = etree.parse(doc_tmp.name)
    root = tree.getroot()
    w = NS["w"]

    # Collect all <w:r> elements that contain <w:footnoteReference>
    fn_ref_runs = []
    for run in root.iter(f'{{{w}}}r'):
        if run.find(f'{{{w}}}footnoteReference') is not None:
            fn_ref_runs.append(run)

    inserts = 0
    # Walk through footnote-reference runs; if two are adjacent siblings, insert comma
    for i in range(len(fn_ref_runs) - 1):
        run_a = fn_ref_runs[i]
        run_b = fn_ref_runs[i + 1]
        parent = run_a.getparent()
        if parent is None or parent != run_b.getparent():
            continue
        # Check they are adjacent (no other elements in between)
        idx_a = list(parent).index(run_a)
        idx_b = list(parent).index(run_b)
        if idx_b == idx_a + 1:
            # Insert a comma run between them
            comma_run = etree.Element(f'{{{w}}}r')
            comma_t = etree.SubElement(comma_run, f'{{{w}}}t')
            comma_t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            comma_t.text = ', '
            parent.insert(idx_a + 1, comma_run)
            inserts += 1

    result = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    Path(doc_tmp.name).unlink(missing_ok=True)
    return result, inserts


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path/to/file.docx> [output.docx]", file=sys.stderr)
        sys.exit(1)

    docx_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else docx_path

    if not Path(docx_path).exists():
        print(f"File not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    # Copy to temp and work on it
    tmp_docx = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    tmp_docx.close()
    shutil.copy2(docx_path, tmp_docx.name)

    try:
        rels_elems = []

        with zipfile.ZipFile(tmp_docx.name, 'r') as zf_in:
            all_files = {name: zf_in.read(name) for name in zf_in.namelist()}

        # Process footnotes.xml
        footnotes_data = all_files.get('word/footnotes.xml')
        if not footnotes_data:
            print("No footnotes.xml found", file=sys.stderr)
            sys.exit(0)

        # Write footnotes to temp, process, read back
        fn_tmp = tempfile.NamedTemporaryFile(suffix='.xml', delete=False)
        fn_tmp.write(footnotes_data)
        fn_tmp.close()

        new_root = process_footnotes(fn_tmp.name, rels_elems)
        new_footnotes_xml = etree.tostring(new_root, xml_declaration=True, encoding='UTF-8', standalone=True)
        all_files['word/footnotes.xml'] = new_footnotes_xml

        # Update relationships
        rels_data = all_files.get('word/_rels/footnotes.xml.rels')
        if rels_data:
            rels_tmp = tempfile.NamedTemporaryFile(suffix='.xml.rels', delete=False)
            rels_tmp.write(rels_data)
            rels_tmp.close()
            update_rels(rels_tmp.name, rels_elems)

            with open(rels_tmp.name, 'rb') as f:
                all_files['word/_rels/footnotes.xml.rels'] = f.read()

        # Process document.xml: insert commas between consecutive footnotes
        doc_data = all_files.get('word/document.xml')
        if doc_data:
            new_doc, comma_inserts = separate_consecutive_footnotes(doc_data)
            all_files['word/document.xml'] = new_doc

        # Deduplicate footnotes: pandoc creates duplicate entries for repeated [^N] references
        dup_merged = deduplicate_footnotes(all_files)

        # Write new DOCX
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
            for name, data in all_files.items():
                zf_out.writestr(name, data)

        # Cleanup temps
        Path(fn_tmp.name).unlink(missing_ok=True)
        if rels_data:
            Path(rels_tmp.name).unlink(missing_ok=True)

        msg = f"OK: {len(rels_elems)} hyperlinks added → {output_path}"
        if doc_data:
            msg += f" | {comma_inserts} consecutive footnote separators inserted"
        if dup_merged:
            msg += f" | {dup_merged} duplicate footnotes merged"
        print(msg)

    finally:
        Path(tmp_docx.name).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
