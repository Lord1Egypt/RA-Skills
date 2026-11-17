#!/usr/bin/env python3
"""Synthetic PDF fixtures for the Phase 13 ingestion tests.

These PDFs are built byte-by-byte here so that the test suite never has to
commit a real, copyrighted third-party document just to exercise the PDF
extractor. Nothing here downloads anything, and no real source material is
used.

Three shapes are provided:

* :func:`build_text_pdf` -- a valid PDF whose pages carry a real text layer.
* :func:`build_textless_pdf` -- a structurally valid PDF that draws only a
  filled rectangle, i.e. the scanned/image-only case with no extractable text.
* :func:`build_corrupt_pdf` -- something that starts with a PDF signature but
  whose object structure is broken, i.e. not a valid PDF at all.
"""

from __future__ import annotations


def _pdf_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _build(objects: list[bytes], root_ref: int = 1) -> bytes:
    """Assemble numbered objects into a PDF with a correct xref table."""
    out = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii") + body + b"\nendobj\n"

    xref_at = len(out)
    count = len(objects) + 1
    out += f"xref\n0 {count}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {count} /Root {root_ref} 0 R >>\n"
        f"startxref\n{xref_at}\n%%EOF\n"
    ).encode("ascii")
    return bytes(out)


def _page_objects(contents: list[bytes]) -> list[bytes]:
    """Build catalog/pages/page/content/font objects for the given streams.

    Object numbering: 1=catalog, 2=pages, 3=font, then for each page a page
    object followed by its content stream.
    """
    n = len(contents)
    page_obj_numbers = [4 + 2 * i for i in range(n)]
    kids = " ".join(f"{num} 0 R" for num in page_obj_numbers)

    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [ {kids} ] /Count {n} >>".encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    for i, stream in enumerate(contents):
        page_num = page_obj_numbers[i]
        content_num = page_num + 1
        objects.append(
            (
                "<< /Type /Page /Parent 2 0 R /MediaBox [ 0 0 612 792 ] "
                "/Resources << /Font << /F1 3 0 R >> >> "
                f"/Contents {content_num} 0 R >>"
            ).encode("ascii")
        )
        objects.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"\nendstream"
        )
    return objects


def build_text_pdf(page_texts: list[str]) -> bytes:
    """A valid PDF with one text-bearing page per entry in ``page_texts``."""
    contents = []
    for text in page_texts:
        stream = (
            "BT\n/F1 24 Tf\n72 700 Td\n"
            f"({_pdf_escape(text)}) Tj\nET\n"
        ).encode("ascii")
        contents.append(stream)
    return _build(_page_objects(contents))


def build_textless_pdf(pages: int = 2) -> bytes:
    """A valid PDF that draws only a rectangle: no extractable text layer."""
    stream = b"0.2 0.4 0.9 rg\n100 100 400 500 re\nf\n"
    return _build(_page_objects([stream] * pages))


def build_corrupt_pdf() -> bytes:
    """Has a PDF signature but a structurally broken body."""
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 99 0 R >>\nendobj\n"
        b"\x00\x01\x02 not-a-pdf-body \xff\xfe\n"
        b"trailer\n<< /Size 2 /Root 1 0 R >>\n"
        b"startxref\n999999\n%%EOF\n"
    )
