#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

try:
    from lxml import etree
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Missing lxml. Run with the Codex workspace Python or install lxml.") from exc


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def wqn(local: str) -> str:
    return f"{{{W_NS}}}{local}"


@dataclass
class FieldInfo:
    instr: str = ""
    result_runs: list[etree._Element] = field(default_factory=list)


def unzip_docx(src: Path, dest: Path):
    with zipfile.ZipFile(src) as zf:
        zf.extractall(dest)


def iter_complex_fields(root: etree._Element) -> list[FieldInfo]:
    fields: list[FieldInfo] = []
    current: FieldInfo | None = None
    in_result = False

    for run in root.findall(".//w:r", namespaces=NS):
        fld = run.find("w:fldChar", namespaces=NS)
        if fld is not None:
            fld_type = fld.get(wqn("fldCharType"))
            if fld_type == "begin":
                current = FieldInfo()
                in_result = False
            elif fld_type == "separate" and current is not None:
                in_result = True
            elif fld_type == "end" and current is not None:
                fields.append(current)
                current = None
                in_result = False
            continue

        if current is None:
            continue
        instr = run.find("w:instrText", namespaces=NS)
        if instr is not None and instr.text:
            current.instr += instr.text
        elif in_result:
            current.result_runs.append(run)

    return fields


def run_text(run: etree._Element) -> str:
    return "".join(t.text or "" for t in run.findall(".//w:t", namespaces=NS))


def is_superscript(run: etree._Element) -> bool:
    vert = run.find("w:rPr/w:vertAlign", namespaces=NS)
    return vert is not None and vert.get(wqn("val")) == "superscript"


def ref_anchor(instr: str) -> str | None:
    match = re.search(r"\bREF\s+(_RefBib[0-9]+)\b", instr)
    return match.group(1) if match else None


def paragraph_has_numpr(paragraph: etree._Element) -> bool:
    return paragraph.find("w:pPr/w:numPr", namespaces=NS) is not None


def validate(path: Path, args: argparse.Namespace) -> tuple[list[str], dict[str, int]]:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        unzip_docx(path, work)
        document_path = work / "word" / "document.xml"
        if not document_path.exists():
            return [f"{path} does not contain word/document.xml"], {}
        parser = etree.XMLParser(remove_blank_text=False)
        root = etree.parse(str(document_path), parser).getroot()

    issues: list[str] = []
    fields = iter_complex_fields(root)
    ref_fields = [field for field in fields if ref_anchor(field.instr)]
    hyperlink_fields = [
        field for field in fields if "HYPERLINK" in field.instr.upper() and "_RefBib" in field.instr
    ]
    hyperlink_elements = root.xpath('.//w:hyperlink[contains(@w:anchor, "_RefBib")]', namespaces=NS)

    bookmarks = root.xpath('.//w:bookmarkStart[starts-with(@w:name, "_RefBib")]', namespaces=NS)
    bookmark_names = {b.get(wqn("name")) for b in bookmarks}

    bib_bookmarks_with_numpr = 0
    for bookmark in bookmarks:
        parent = bookmark.getparent()
        if parent is not None and parent.tag == wqn("p") and paragraph_has_numpr(parent):
            bib_bookmarks_with_numpr += 1
        else:
            issues.append(f"Bookmark {bookmark.get(wqn('name'))} is not in an auto-numbered paragraph.")

    for field in ref_fields:
        anchor = ref_anchor(field.instr)
        if anchor and anchor not in bookmark_names:
            issues.append(f"REF field targets missing bookmark: {anchor}")
        visible_result_runs = [run for run in field.result_runs if run_text(run)]
        if args.require_superscript and not visible_result_runs:
            issues.append(f"REF field has no cached visible result: {field.instr.strip()}")
        if args.require_superscript:
            for run in visible_result_runs:
                if not is_superscript(run):
                    issues.append(
                        f"REF field cached result is not superscript: {field.instr.strip()}"
                    )

    if args.require_ref and not ref_fields:
        issues.append("No REF _RefBib fields found.")

    if args.forbid_hyperlinks and (hyperlink_fields or hyperlink_elements):
        issues.append(
            f"Found hyperlink-based bibliography citations: fields={len(hyperlink_fields)}, elements={len(hyperlink_elements)}"
        )

    if args.require_auto_numbered_bib and bookmarks and bib_bookmarks_with_numpr != len(bookmarks):
        issues.append(
            f"Not all bibliography bookmarks are in auto-numbered paragraphs: {bib_bookmarks_with_numpr}/{len(bookmarks)}"
        )

    if args.expect_bib_count is not None and len(bookmarks) != args.expect_bib_count:
        issues.append(
            f"Expected {args.expect_bib_count} bibliography bookmarks, found {len(bookmarks)}."
        )

    if args.expect_ref_fields is not None and len(ref_fields) != args.expect_ref_fields:
        issues.append(f"Expected {args.expect_ref_fields} REF fields, found {len(ref_fields)}.")

    counts = {
        "complex_fields": len(fields),
        "ref_fields": len(ref_fields),
        "hyperlink_fields": len(hyperlink_fields),
        "hyperlink_elements": len(hyperlink_elements),
        "bib_bookmarks": len(bookmarks),
        "bib_bookmarks_with_numpr": bib_bookmarks_with_numpr,
    }
    return issues, counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate DOCX REF citations and bibliography numbering.")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--expect-bib-count", type=int)
    parser.add_argument("--expect-ref-fields", type=int)
    parser.add_argument("--forbid-hyperlinks", action="store_true")
    parser.add_argument("--require-ref", action="store_true")
    parser.add_argument("--require-superscript", action="store_true")
    parser.add_argument("--require-auto-numbered-bib", action="store_true")
    args = parser.parse_args(argv)

    issues, counts = validate(args.docx, args)
    print("DOCX cross-reference report")
    for key, value in counts.items():
        print(f"- {key}: {value}")
    if issues:
        print("\nFAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
