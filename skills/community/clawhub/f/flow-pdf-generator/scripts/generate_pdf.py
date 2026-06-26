#!/usr/bin/env python3
"""Generate styled PDF documents from structured data."""

import sys
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors


def parse_args():
    """Parse command line arguments."""
    args = sys.argv[1:]
    input_data = {}
    output_path = "output.pdf"
    json_input = None

    for i, arg in enumerate(args):
        if arg == "--output" and i + 1 < len(args):
            output_path = args[i + 1]
        elif arg == "--data" and i + 1 < len(args):
            json_input = args[i + 1]
        elif arg == "--help" or arg == "-h":
            print_usage()
            sys.exit(0)

    # Handle JSON input
    if json_input:
        try:
            input_data = json.loads(json_input)
        except json.JSONDecodeError:
            with open(json_input) as f:
                input_data = json.load(f)
            if "output" in input_data:
                output_path = input_data["output"]

    # Handle positional arguments (JSON files)
    for arg in args:
        if not arg.startswith("--") and arg not in ("--data",):
            if os.path.exists(arg):
                with open(arg) as f:
                    input_data = json.load(f)
                    if "output" in input_data:
                        output_path = input_data["output"]
                break

    return input_data, output_path


def print_usage():
    usage = """Usage: generate_pdf.py [--output <path>] [--data '<json>'] [data.json]

JSON schema:
{
  "title": "Document Title",
  "subtitle": "Optional subtitle",
  "author": "Author Name",
  "date": "2026-04-27",
  "accent_color": "#e94560",
  "header_color": "#1a1a2e",
  "sections": [
    {"type": "heading", "text": "Section Title"},
    {"type": "text", "text": "Body text here."},
    {"type": "highlight", "text": "Important callout."},
    {"type": "list", "items": ["Item 1", "Item 2"]},
    {"type": "table", "data": [["Col1", "Col2"], ["Val1", "Val2"]]},
    {"type": "image", "path": "/path/to/image.png", "width": 100, "height": 60},
    {"type": "pagebreak"}
  ]
}"""
    print(usage)


def create_styles(custom_styles=None):
    """Create named styles for the document."""
    styles = getSampleStyleSheet()

    defaults = {
        "heading1": {"fontSize": 24, "leading": 30, "textColor": "#1a1a2e", "spaceAfter": 20, "fontName": "Helvetica-Bold"},
        "heading2": {"fontSize": 18, "leading": 24, "textColor": "#16213e", "spaceAfter": 12, "fontName": "Helvetica-Bold"},
        "heading3": {"fontSize": 14, "leading": 18, "textColor": "#0f3460", "spaceAfter": 8, "fontName": "Helvetica-Bold"},
        "body": {"fontSize": 11, "leading": 16, "textColor": "#2d2d2d", "spaceAfter": 8, "fontName": "Helvetica"},
        "caption": {"fontSize": 9, "leading": 12, "textColor": "#666666", "spaceAfter": 4, "fontName": "Helvetica-Oblique"},
        "highlight": {"fontSize": 12, "leading": 16, "textColor": "#e94560", "fontName": "Helvetica-Bold"},
    }

    custom = custom_styles or {}
    for name, props in {**defaults, **custom}.items():
        styles.add(ParagraphStyle(name=name, **props))

    return styles


def build_document(data, output_path, styles):
    """Build the PDF document from input data."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
        title=data.get("title", ""),
        author=data.get("author", ""),
        subject=data.get("subject", ""),
    )

    story = []

    # Header color
    if "header_color" in data:
        header_color = HexColor(data["header_color"])
    else:
        header_color = HexColor("#1a1a2e")

    # Title
    if "title" in data:
        story.append(Paragraph(data["title"], styles["heading1"]))
        story.append(Spacer(1, 5*mm))

    # Subtitle
    if "subtitle" in data:
        story.append(Paragraph(data["subtitle"], styles["heading3"]))
        story.append(Spacer(1, 10*mm))

    # Author/date line
    meta = []
    if "author" in data:
        meta.append(f"Autor: {data['author']}")
    if "date" in data:
        meta.append(f"Datum: {data['date']}")
    if meta:
        story.append(Paragraph(" | ".join(meta), styles["caption"]))
        story.append(Spacer(1, 15*mm))

    # Horizontal rule
    if "accent_color" in data:
        accent = HexColor(data["accent_color"])
    else:
        accent = HexColor("#e94560")

    rule_table = Table([[""]], colWidths=[170*mm], rowHeights=[2*mm])
    rule_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
    ]))
    story.append(rule_table)
    story.append(Spacer(1, 10*mm))

    # Sections
    for section in data.get("sections", []):
        sec_type = section.get("type", "text")

        if sec_type == "heading":
            story.append(Paragraph(section["text"], styles["heading2"]))
            story.append(Spacer(1, 5*mm))
        elif sec_type == "subheading":
            story.append(Paragraph(section["text"], styles["heading3"]))
            story.append(Spacer(1, 3*mm))
        elif sec_type == "text":
            story.append(Paragraph(section["text"], styles["body"]))
            story.append(Spacer(1, 3*mm))
        elif sec_type == "highlight":
            story.append(Paragraph(section["text"], styles["highlight"]))
            story.append(Spacer(1, 3*mm))
        elif sec_type == "list":
            for item in section.get("items", []):
                story.append(Paragraph(f"&#8226; {item}", styles["body"]))
            story.append(Spacer(1, 3*mm))
        elif sec_type == "table":
            table_data = section.get("data", [])
            if table_data and table_data[0]:
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), header_color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ]))
                story.append(t)
                story.append(Spacer(1, 8*mm))
        elif sec_type == "image":
            img_path = section.get("path", "")
            if img_path and os.path.exists(img_path):
                try:
                    w = section.get("width", 150*mm)
                    h = section.get("height", 80*mm)
                    img = Image(img_path, width=w, height=h)
                    story.append(img)
                    story.append(Spacer(1, 5*mm))
                except Exception:
                    pass
        elif sec_type == "pagebreak":
            story.append(PageBreak())

    doc.build(story)
    print(f"PDF created: {output_path}")
    return output_path


def main():
    data, output_path = parse_args()

    if not data:
        print_usage()
        sys.exit(1)

    styles = create_styles(data.get("styles"))
    build_document(data, output_path, styles)


if __name__ == "__main__":
    main()