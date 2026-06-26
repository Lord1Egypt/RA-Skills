#!/usr/bin/env python3
"""
BRD review helper for DOCX workflows.

Commands:
- init-review: extract readable paragraphs from a BRD DOCX into a review JSON template.
- materialize: generate a reviewed DOCX with comments and tracked revisions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import zipfile
from pathlib import Path
from typing import Any

try:
    from lxml import etree
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: lxml. Install with `python -m pip install --user lxml python-docx`."
    ) from exc

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
XML_NS = "http://www.w3.org/XML/1998/namespace"

NS = {"w": W_NS, "r": R_NS}
W = f"{{{W_NS}}}"
R = f"{{{R_NS}}}"
CT = f"{{{CONTENT_TYPES_NS}}}"
PR = f"{{{PACKAGE_REL_NS}}}"
XML_SPACE = f"{{{XML_NS}}}space"

COMMENTS_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
COMMENTS_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"


def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def parse_xml(data: bytes) -> etree._Element:
    return etree.fromstring(data)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_docx_files(docx_path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(docx_path, "r") as archive:
        return {item.filename: archive.read(item.filename) for item in archive.infolist()}


def write_docx_files(output_docx: Path, original_docx: Path, files: dict[str, bytes]) -> None:
    ensure_parent(output_docx)
    with zipfile.ZipFile(original_docx, "r") as source_archive, zipfile.ZipFile(
        output_docx, "w", compression=zipfile.ZIP_DEFLATED
    ) as output_archive:
        for item in source_archive.infolist():
            payload = files.get(item.filename)
            if payload is not None:
                output_archive.writestr(item, payload)
        for name in sorted(files):
            if name not in source_archive.namelist():
                output_archive.writestr(name, files[name])


def paragraph_text(paragraph: etree._Element) -> str:
    parts: list[str] = []
    for node in paragraph.xpath(".//w:t | .//w:delText", namespaces=NS):
        if node.text:
            parts.append(node.text)
    return "".join(parts).strip()


def paragraph_style_id(paragraph: etree._Element) -> str:
    style = paragraph.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
    return style[0].strip() if style else ""


def is_heading_style(style_id: str) -> bool:
    return style_id.lower().startswith("heading")


def get_body_paragraphs(document_root: etree._Element) -> list[etree._Element]:
    return document_root.xpath(".//w:body//w:p", namespaces=NS)


def build_review_template(input_docx: Path) -> dict[str, Any]:
    files = read_docx_files(input_docx)
    document_root = parse_xml(files["word/document.xml"])
    paragraphs = get_body_paragraphs(document_root)

    extracted: list[dict[str, Any]] = []
    heading_stack: list[str] = []

    for index, paragraph in enumerate(paragraphs):
        text = paragraph_text(paragraph)
        if not text:
            continue

        style_id = paragraph_style_id(paragraph)
        if is_heading_style(style_id):
            level_text = "".join(ch for ch in style_id if ch.isdigit())
            level = int(level_text) if level_text else 1
            while len(heading_stack) >= level:
                heading_stack.pop()
            heading_stack.append(text)

        extracted.append(
            {
                "paragraph_index": index,
                "style_id": style_id,
                "heading_path": " > ".join(heading_stack),
                "source_text": text,
                "issue_tags": [],
                "needs_comment": False,
                "comment_question": "",
                "needs_revision": False,
                "proposed_replacement": "",
            }
        )

    if not extracted:
        raise ValueError("No readable paragraphs were found in the BRD.")

    return {
        "source_docx": str(input_docx),
        "prepared_at_utc": utc_now_iso(),
        "reviewer": "",
        "overall_notes": "",
        "paragraphs": extracted,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Review JSON must be a top-level object.")
    paragraphs = payload.get("paragraphs")
    if not isinstance(paragraphs, list):
        raise ValueError("Review JSON must include a 'paragraphs' list.")
    return payload


def set_preserve_space(node: etree._Element, text: str) -> None:
    if text != text.strip():
        node.set(XML_SPACE, "preserve")


def append_text_run(parent: etree._Element, text: str) -> None:
    run = etree.SubElement(parent, f"{W}r")
    text_node = etree.SubElement(run, f"{W}t")
    text_node.text = text
    set_preserve_space(text_node, text)


def ensure_track_revisions(settings_root: etree._Element) -> None:
    existing = settings_root.xpath("./w:trackRevisions", namespaces=NS)
    if existing:
        return
    settings_root.append(etree.Element(f"{W}trackRevisions"))


def replace_paragraph_with_revision(
    paragraph: etree._Element,
    original_text: str,
    replacement_text: str,
    revision_id: int,
    author: str,
    revision_date: str,
) -> None:
    paragraph_properties = paragraph.find(f"{W}pPr")
    for child in list(paragraph):
        if child is not paragraph_properties:
            paragraph.remove(child)

    deleted = etree.Element(f"{W}del")
    deleted.set(f"{W}id", str(revision_id))
    deleted.set(f"{W}author", author)
    deleted.set(f"{W}date", revision_date)
    deleted_run = etree.SubElement(deleted, f"{W}r")
    deleted_text = etree.SubElement(deleted_run, f"{W}delText")
    deleted_text.text = original_text
    set_preserve_space(deleted_text, original_text)

    inserted = etree.Element(f"{W}ins")
    inserted.set(f"{W}id", str(revision_id + 1))
    inserted.set(f"{W}author", author)
    inserted.set(f"{W}date", revision_date)
    inserted_run = etree.SubElement(inserted, f"{W}r")
    inserted_text = etree.SubElement(inserted_run, f"{W}t")
    inserted_text.text = replacement_text
    set_preserve_space(inserted_text, replacement_text)

    paragraph.append(deleted)
    paragraph.append(inserted)


def next_numeric_rid(rels_root: etree._Element) -> str:
    numeric_ids: list[int] = []
    for rel in rels_root.findall(f"{PR}Relationship"):
        rid = rel.get("Id", "")
        if rid.startswith("rId") and rid[3:].isdigit():
            numeric_ids.append(int(rid[3:]))
    return f"rId{max(numeric_ids, default=0) + 1}"


def ensure_comments_part(files: dict[str, bytes]) -> tuple[etree._Element, etree._Element, etree._Element]:
    content_types_root = parse_xml(files["[Content_Types].xml"])
    rels_root = parse_xml(files["word/_rels/document.xml.rels"])

    if "word/comments.xml" in files:
        comments_root = parse_xml(files["word/comments.xml"])
    else:
        comments_root = etree.Element(f"{W}comments", nsmap={"w": W_NS})
        files["word/comments.xml"] = etree.tostring(
            comments_root, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    has_override = any(
        node.get("PartName") == "/word/comments.xml"
        for node in content_types_root.findall(f"{CT}Override")
    )
    if not has_override:
        override = etree.SubElement(content_types_root, f"{CT}Override")
        override.set("PartName", "/word/comments.xml")
        override.set("ContentType", COMMENTS_CONTENT_TYPE)

    has_relationship = any(
        rel.get("Type") == COMMENTS_REL_TYPE and rel.get("Target") == "comments.xml"
        for rel in rels_root.findall(f"{PR}Relationship")
    )
    if not has_relationship:
        relationship = etree.SubElement(rels_root, f"{PR}Relationship")
        relationship.set("Id", next_numeric_rid(rels_root))
        relationship.set("Type", COMMENTS_REL_TYPE)
        relationship.set("Target", "comments.xml")

    return comments_root, content_types_root, rels_root


def next_comment_id(comments_root: etree._Element) -> int:
    existing_ids: list[int] = []
    for comment in comments_root.findall(f"{W}comment"):
        raw_id = comment.get(f"{W}id", "")
        if raw_id.isdigit():
            existing_ids.append(int(raw_id))
    return max(existing_ids, default=-1) + 1


def ensure_comment_anchor_runs(paragraph: etree._Element) -> list[etree._Element]:
    candidate_runs = [
        child
        for child in paragraph
        if child.tag == f"{W}r" and not child.xpath(".//w:commentReference", namespaces=NS)
    ]
    if candidate_runs:
        return candidate_runs

    run = etree.Element(f"{W}r")
    text_node = etree.SubElement(run, f"{W}t")
    text_node.text = ""
    paragraph.append(run)
    return [run]


def build_comment_element(comment_id: int, author: str, comment_text: str, comment_date: str) -> etree._Element:
    comment = etree.Element(f"{W}comment")
    comment.set(f"{W}id", str(comment_id))
    comment.set(f"{W}author", author)
    comment.set(f"{W}date", comment_date)
    paragraph = etree.SubElement(comment, f"{W}p")
    append_text_run(paragraph, comment_text)
    return comment


def attach_comment_to_paragraph(
    paragraph: etree._Element,
    comments_root: etree._Element,
    author: str,
    comment_text: str,
    comment_date: str,
) -> None:
    if not comment_text.strip():
        return

    runs = ensure_comment_anchor_runs(paragraph)
    first_run = runs[0]
    last_run = runs[-1]
    comment_id = next_comment_id(comments_root)

    comments_root.append(build_comment_element(comment_id, author, comment_text.strip(), comment_date))

    start = etree.Element(f"{W}commentRangeStart")
    start.set(f"{W}id", str(comment_id))
    end = etree.Element(f"{W}commentRangeEnd")
    end.set(f"{W}id", str(comment_id))

    first_run.addprevious(start)
    last_run.addnext(end)

    reference_run = etree.Element(f"{W}r")
    reference_props = etree.SubElement(reference_run, f"{W}rPr")
    reference_style = etree.SubElement(reference_props, f"{W}rStyle")
    reference_style.set(f"{W}val", "CommentReference")
    reference = etree.SubElement(reference_run, f"{W}commentReference")
    reference.set(f"{W}id", str(comment_id))
    end.addnext(reference_run)


def serialize_xml(root: etree._Element) -> bytes:
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def apply_review(
    input_docx: Path,
    review_payload: dict[str, Any],
    output_docx: Path,
    author: str,
) -> tuple[int, int]:
    files = read_docx_files(input_docx)
    document_root = parse_xml(files["word/document.xml"])
    settings_root = parse_xml(files["word/settings.xml"])
    comments_root, content_types_root, rels_root = ensure_comments_part(files)
    paragraphs = get_body_paragraphs(document_root)

    revision_date = utc_now_iso()
    comment_date = revision_date
    revisions_applied = 0
    comments_added = 0

    for item_index, item in enumerate(review_payload.get("paragraphs", []), start=1):
        if not isinstance(item, dict):
            continue
        paragraph_index = item.get("paragraph_index")
        if not isinstance(paragraph_index, int):
            continue
        if paragraph_index < 0 or paragraph_index >= len(paragraphs):
            continue

        paragraph = paragraphs[paragraph_index]
        original_text = paragraph_text(paragraph)

        if bool(item.get("needs_revision")):
            replacement = str(item.get("proposed_replacement", "")).strip()
            if replacement and original_text:
                replace_paragraph_with_revision(
                    paragraph=paragraph,
                    original_text=original_text,
                    replacement_text=replacement,
                    revision_id=item_index * 10,
                    author=author,
                    revision_date=revision_date,
                )
                revisions_applied += 1

        if bool(item.get("needs_comment")):
            comment_question = str(item.get("comment_question", "")).strip()
            if comment_question:
                attach_comment_to_paragraph(
                    paragraph=paragraph,
                    comments_root=comments_root,
                    author=author,
                    comment_text=comment_question,
                    comment_date=comment_date,
                )
                comments_added += 1

    ensure_track_revisions(settings_root)

    files["word/document.xml"] = serialize_xml(document_root)
    files["word/settings.xml"] = serialize_xml(settings_root)
    files["word/comments.xml"] = serialize_xml(comments_root)
    files["[Content_Types].xml"] = serialize_xml(content_types_root)
    files["word/_rels/document.xml.rels"] = serialize_xml(rels_root)

    write_docx_files(output_docx, input_docx, files)
    return comments_added, revisions_applied


def assert_docx_written(path: Path) -> None:
    if path.suffix.lower() != ".docx":
        raise ValueError(f"Output must be a .docx file: {path}")
    if not path.exists():
        raise FileNotFoundError(f"Output was not created: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Output is empty: {path}")


def command_init_review(args: argparse.Namespace) -> None:
    payload = build_review_template(args.input)
    write_json(args.output, payload)
    print(f"[OK] Wrote review template: {args.output}")
    print(f"[OK] Paragraphs detected: {len(payload['paragraphs'])}")


def command_materialize(args: argparse.Namespace) -> None:
    payload = load_json(args.review_json)
    comments_added, revisions_applied = apply_review(
        input_docx=args.input,
        review_payload=payload,
        output_docx=args.output,
        author=args.author,
    )
    assert_docx_written(args.output)
    print(f"[OK] Wrote reviewed BRD: {args.output}")
    print(f"[OK] Comments added: {comments_added}")
    print(f"[OK] Tracked revisions applied: {revisions_applied}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BRD DOCX extraction and redline materialization tool.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_review = subparsers.add_parser(
        "init-review",
        help="Extract readable BRD paragraphs into a review JSON template.",
    )
    init_review.add_argument("--input", type=Path, required=True, help="Source BRD .docx")
    init_review.add_argument("--output", type=Path, required=True, help="Output review .json")
    init_review.set_defaults(handler=command_init_review)

    materialize = subparsers.add_parser(
        "materialize",
        help="Create a reviewed DOCX with comments and tracked changes.",
    )
    materialize.add_argument("--input", type=Path, required=True, help="Source BRD .docx")
    materialize.add_argument(
        "--review-json",
        type=Path,
        required=True,
        help="Completed review JSON file.",
    )
    materialize.add_argument("--output", type=Path, required=True, help="Output reviewed .docx")
    materialize.add_argument(
        "--author",
        default="Codex BRD Reviewer",
        help="Author recorded in comments and tracked changes.",
    )
    materialize.set_defaults(handler=command_materialize)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
