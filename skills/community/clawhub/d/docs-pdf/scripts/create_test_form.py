#!/usr/bin/env python3
"""Create a sample fillable PDF form for testing form-filling workflows.

Usage:
    python scripts/create_test_form.py                      # → test_form.pdf
    python scripts/create_test_form.py -o my_form.pdf       # custom output path

The generated form contains common field types:
  - Text fields (name, email, date, notes)
  - Checkboxes (agree_terms)

Use with:
  python scripts/check_fillable_fields.py test_form.pdf     # inspect fields
  python scripts/fill_pdf_form.py test_form.pdf -o filled.pdf --set full_name="Alice"
"""
from __future__ import annotations

import argparse
import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    print("ERROR: reportlab is required. Install with:")
    print("  pip install reportlab --break-system-packages")
    sys.exit(1)

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import FreeText
    from pypdf.generic import (
        ArrayObject,
        BooleanObject,
        DictionaryObject,
        NameObject,
        NumberObject,
        TextStringObject,
    )
except ImportError:
    print("ERROR: pypdf is required. Install with:")
    print("  pip install pypdf --break-system-packages")
    sys.exit(1)

import io
from pathlib import Path


def create_fillable_form(output_path: str = "test_form.pdf") -> str:
    """Generate a fillable PDF form with common field types."""

    # --- Step 1: Create visual template with reportlab ---
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(72, h - 72, "Sample Registration Form")
    c.setFont("Helvetica", 10)
    c.drawString(72, h - 90, "(This is a fillable PDF form for testing)")

    # Labels
    c.setFont("Helvetica", 12)
    fields_layout = [
        ("Full Name:", 72, h - 140),
        ("Email:", 72, h - 180),
        ("Date:", 72, h - 220),
        ("Department:", 72, h - 260),
        ("Notes:", 72, h - 300),
        ("I agree to terms:", 72, h - 370),
    ]
    for label, x, y in fields_layout:
        c.drawString(x, y, label)

    # Draw field boxes (visual only)
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    field_boxes = [
        (180, h - 155, 300, 20),   # full_name
        (180, h - 195, 300, 20),   # email
        (180, h - 235, 150, 20),   # date
        (180, h - 275, 200, 20),   # department
        (180, h - 340, 300, 50),   # notes (multiline)
    ]
    for x, y, fw, fh in field_boxes:
        c.rect(x, y, fw, fh)

    # Checkbox box
    c.rect(180, h - 380, 14, 14)

    c.save()
    buf.seek(0)

    # --- Step 2: Add interactive form fields with pypdf ---
    reader = PdfReader(buf)
    writer = PdfWriter()
    writer.append(reader)

    page = writer.pages[0]

    # Create AcroForm fields
    field_defs = [
        {"name": "full_name",   "x": 180, "y": h - 155, "w": 300, "h": 20, "type": "text"},
        {"name": "email",       "x": 180, "y": h - 195, "w": 300, "h": 20, "type": "text"},
        {"name": "date",        "x": 180, "y": h - 235, "w": 150, "h": 20, "type": "text"},
        {"name": "department",  "x": 180, "y": h - 275, "w": 200, "h": 20, "type": "text"},
        {"name": "notes",       "x": 180, "y": h - 340, "w": 300, "h": 50, "type": "text",
         "multiline": True},
        {"name": "agree_terms", "x": 180, "y": h - 380, "w": 14,  "h": 14, "type": "checkbox"},
    ]

    for fd in field_defs:
        if fd["type"] == "text":
            field = DictionaryObject()
            field.update(
                {
                    NameObject("/Type"): NameObject("/Annot"),
                    NameObject("/Subtype"): NameObject("/Widget"),
                    NameObject("/FT"): NameObject("/Tx"),
                    NameObject("/T"): TextStringObject(fd["name"]),
                    NameObject("/V"): TextStringObject(""),
                    NameObject("/Rect"): ArrayObject(
                        [
                            NumberObject(fd["x"]),
                            NumberObject(fd["y"]),
                            NumberObject(fd["x"] + fd["w"]),
                            NumberObject(fd["y"] + fd["h"]),
                        ]
                    ),
                    NameObject("/DA"): TextStringObject("/Helv 11 Tf 0 g"),
                    NameObject("/Ff"): NumberObject(1 << 12 if fd.get("multiline") else 0),
                }
            )
            writer._add_object(field)
            if "/Annots" not in page:
                page[NameObject("/Annots")] = ArrayObject()
            page["/Annots"].append(field.indirect_reference)

        elif fd["type"] == "checkbox":
            field = DictionaryObject()
            field.update(
                {
                    NameObject("/Type"): NameObject("/Annot"),
                    NameObject("/Subtype"): NameObject("/Widget"),
                    NameObject("/FT"): NameObject("/Btn"),
                    NameObject("/T"): TextStringObject(fd["name"]),
                    NameObject("/V"): NameObject("/Off"),
                    NameObject("/Rect"): ArrayObject(
                        [
                            NumberObject(fd["x"]),
                            NumberObject(fd["y"]),
                            NumberObject(fd["x"] + fd["w"]),
                            NumberObject(fd["y"] + fd["h"]),
                        ]
                    ),
                }
            )
            writer._add_object(field)
            if "/Annots" not in page:
                page[NameObject("/Annots")] = ArrayObject()
            page["/Annots"].append(field.indirect_reference)

    # Set up AcroForm at document level
    writer._root_object[NameObject("/AcroForm")] = DictionaryObject(
        {
            NameObject("/Fields"): page["/Annots"],
            NameObject("/NeedAppearances"): BooleanObject(True),
            NameObject("/DA"): TextStringObject("/Helv 11 Tf 0 g"),
        }
    )

    out = Path(output_path)
    with open(out, "wb") as f:
        writer.write(f)

    print(f"✓ Created fillable form → {out}")
    print(f"  Fields: {', '.join(fd['name'] for fd in field_defs)}")
    print()
    print("  Test with:")
    print(f"    python scripts/check_fillable_fields.py {out}")
    print(f'    python scripts/fill_pdf_form.py {out} -o filled.pdf --set full_name="Alice Chen"')
    return str(out)


def main():
    parser = argparse.ArgumentParser(
        description="Create a sample fillable PDF form for testing."
    )
    parser.add_argument(
        "-o", "--output",
        default="test_form.pdf",
        help="Output PDF path (default: test_form.pdf)",
    )
    args = parser.parse_args()
    create_fillable_form(args.output)


if __name__ == "__main__":
    main()
