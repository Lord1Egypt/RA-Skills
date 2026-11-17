#!/usr/bin/env python3
"""
PDF Editor - Core Engine
Supports: text editing, image insertion, watermark, annotation, merge, split, page reorder, signature
"""

import os
import sys
import json
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime


class PDFEditor:
    """Core PDF editing engine."""

    def __init__(self, filepath=None):
        self.doc = None
        self.filepath = filepath
        if filepath:
            self.open(filepath)

    def open(self, filepath):
        """Open a PDF file."""
        self.filepath = filepath
        self.doc = fitz.open(filepath)
        return self

    def save(self, output_path=None):
        """Save PDF to file."""
        if not self.doc:
            raise ValueError("No PDF document opened")
        if not output_path:
            if self.filepath:
                base, ext = os.path.splitext(self.filepath)
                output_path = f"{base}_edited{ext}"
            else:
                output_path = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.doc.save(output_path)
        self.doc.close()
        self.doc = fitz.open(output_path)
        self.filepath = output_path
        return output_path

    def info(self):
        """Get document info."""
        if not self.doc:
            return {"error": "No document opened"}
        meta = self.doc.metadata
        return {
            "pages": len(self.doc),
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "subject": meta.get("subject", ""),
            "creator": meta.get("creator", ""),
            "filesize": os.path.getsize(self.filepath) if self.filepath and os.path.exists(self.filepath) else 0,
            "page_sizes": [f"{p.rect.width:.0f}x{p.rect.height:.0f}" for p in self.doc],
        }

    def get_page_text(self, page_num):
        """Get text content of a specific page. page_num is 1-based."""
        page = self.doc[page_num - 1]
        blocks = page.get_text("dict")["blocks"]
        result = []
        for block in blocks:
            if block["type"] == 0:  # Text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        result.append({
                            "text": span["text"],
                            "font": span["font"],
                            "size": round(span["size"], 1),
                            "bbox": [round(v, 1) for v in span["bbox"]],
                            "color": span["color"],
                        })
        return result

    def edit_text_at_rect(self, page_num, x0, y0, x1, y1, new_text, font_name="helv", font_size=None, color=None):
        """Edit text at a precise bounding box (BBox-based, not text-search).
        page_num is 1-based. x0/y0/x1/y1 are in PDF point coordinates.
        Returns the new rect of the inserted text."""
        page = self.doc[page_num - 1]
        rect = fitz.Rect(x0, y0, x1, y1)
        if not rect.is_infinite:
            rect = rect.normalize()

        # Determine font size and color from existing text at this location
        if font_size is None:
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        sr = fitz.Rect(span["bbox"])
                        if sr.intersects(rect):
                            font_size = span["size"]
                            if color is None:
                                color = span["color"]
                            break
        if font_size is None:
            font_size = 12
        if color is None:
            color = 0

        # White-out the old area
        page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()

        # Insert new text at same position
        text_point = fitz.Point(rect.x0, rect.y1 - 2)
        rc = color if color else 0
        page.insert_text(text_point, new_text, fontname=font_name,
                         fontsize=font_size, color=rc)
        return [round(rect.x0, 1), round(rect.y0, 1), round(rect.x1, 1), round(rect.y1, 1)]

    def add_text(self, page_num, text, x, y, font_size=12, font_name="helv", color=(0, 0, 0)):
        """Add new text at specific position."""
        page = self.doc[page_num]
        point = fitz.Point(x, y)
        page.insert_text(point, text, fontname=font_name, fontsize=font_size,
                        color=(color[0] * 255) if isinstance(color, tuple) else color)
        return True

    def delete_text(self, page_num, text_to_delete):
        """Delete text by redacting it (fills with white)."""
        page = self.doc[page_num]
        instances = page.search_for(text_to_delete)
        for rect in instances:
            page.add_redact_annot(rect, fill=(1, 1, 1))
            page.apply_redactions()
        return len(instances)

    def insert_image(self, page_num, image_path, x=0, y=0, width=None, height=None):
        """Insert an image onto a page."""
        page = self.doc[page_num]
        img = fitz.open(image_path)
        page_rect = page.rect
        img_rect = img[0].rect

        if width and height:
            pass  # Use specified dimensions
        elif width:
            height = width * img_rect.height / img_rect.width
        elif height:
            width = height * img_rect.width / img_rect.height
        else:
            # Default: 1/3 of page width
            width = page_rect.width / 3
            height = width * img_rect.height / img_rect.width

        rect = fitz.Rect(x, y, x + width, y + height)
        page.insert_image(rect, filename=image_path)
        img.close()
        return True

    def delete_image(self, page_num, image_index=0):
        """Delete an image from a page."""
        page = self.doc[page_num]
        images = page.get_images()
        if image_index < len(images):
            xref = images[image_index][0]
            page.delete_image(xref)
            return True
        return False

    def add_watermark(self, text=None, image_path=None, opacity=0.3,
                      font_size=50, angle=45, pages="all"):
        """Add watermark to pages."""
        page_range = self._parse_page_range(pages, len(self.doc))
        for pnum in page_range:
            page = self.doc[pnum]
            rect = page.rect
            if text:
                # Create watermark with text
                text_length = fitz.get_text_length(text, fontsize=font_size,
                                                    fontname="helv")
                # Center the text
                tx = (rect.width - text_length) / 2
                ty = rect.height / 2
                # Create a shape for rotation
                shape = page.new_shape()
                shape.insert_textbox(
                    fitz.Rect(0, 0, rect.width, rect.height),
                    text, fontsize=font_size, fontname="helv",
                    align=1, color=(0.5, 0.5, 0.5), opacity=opacity,
                    rotate=angle
                )
                shape.commit()
            elif image_path:
                page.insert_image(rect, filename=image_path, overlay=True,
                                opacity=opacity)
        return len(page_range)

    def add_annotation(self, page_num, text, x, y, icon="Note", color=(1, 0, 0)):
        """Add a text annotation (sticky note)."""
        page = self.doc[page_num]
        point = fitz.Point(x, y)
        annot = page.add_text_annot(point, text, icon=icon)
        annot.set_colors(stroke=color)
        annot.update()
        return True

    def add_highlight(self, page_num, text_to_highlight, color=(1, 1, 0)):
        """Highlight specific text on a page."""
        page = self.doc[page_num]
        instances = page.search_for(text_to_highlight)
        for rect in instances:
            highlight = page.add_highlight_annot(rect)
            highlight.set_colors(stroke=color)
            highlight.update()
        return len(instances)

    def add_signature(self, page_num, sig_image_path, x, y, width=150, height=50):
        """Add a signature image to a page."""
        return self.insert_image(page_num, sig_image_path, x, y, width, height)

    def merge(self, other_paths, output_path=None):
        """Merge multiple PDFs into one."""
        if not output_path:
            base, ext = os.path.splitext(self.filepath or "merged.pdf")
            output_path = f"{base}_merged{ext}"
        merged = fitz.open(self.filepath) if self.filepath else fitz.open()
        for path in other_paths:
            if os.path.exists(path) and path.lower().endswith(".pdf"):
                src = fitz.open(path)
                merged.insert_pdf(src)
                src.close()
        merged.save(output_path)
        merged.close()
        return output_path

    def split(self, output_dir=None, ranges=None):
        """Split PDF. If ranges provided, split by ranges. Otherwise split by page."""
        if not output_dir:
            output_dir = os.path.dirname(self.filepath or ".") or "."
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(self.filepath or "document"))[0]
        results = []

        if ranges:
            for i, r in enumerate(ranges):
                start, end = r
                new_doc = fitz.open()
                new_doc.insert_pdf(self.doc, from_page=start, to_page=end)
                out_path = os.path.join(output_dir, f"{base_name}_part{i+1}.pdf")
                new_doc.save(out_path)
                new_doc.close()
                results.append(out_path)
        else:
            for i in range(len(self.doc)):
                new_doc = fitz.open()
                new_doc.insert_pdf(self.doc, from_page=i, to_page=i)
                out_path = os.path.join(output_dir, f"{base_name}_page{i+1}.pdf")
                new_doc.save(out_path)
                new_doc.close()
                results.append(out_path)
        return results

    def reorder_pages(self, new_order):
        """Reorder pages. new_order is a list of page indices (0-based)."""
        new_doc = fitz.open()
        for idx in new_order:
            new_doc.insert_pdf(self.doc, from_page=idx, to_page=idx)
        new_path = self.save()
        # Overwrite with reordered version
        self.doc.close()
        self.doc = new_doc
        return True

    def delete_pages(self, page_nums):
        """Delete specific pages by index."""
        self.doc.delete_pages(page_nums)
        self.save()
        return True

    def extract_page_as_image(self, page_num, dpi=150, output_path=None):
        """Extract a page as an image file."""
        page = self.doc[page_num]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        if not output_path:
            output_path = f"page_{page_num + 1}.png"
        pix.save(output_path)
        return output_path

    def rotate_page(self, page_num, angle=90):
        """Rotate a page by degrees."""
        page = self.doc[page_num]
        page.set_rotation(angle)
        return True

    def _parse_page_range(self, spec, total):
        """Parse page range specification."""
        if spec == "all":
            return list(range(total))
        if isinstance(spec, str):
            if "-" in spec:
                start, end = spec.split("-")
                return list(range(int(start) - 1, int(end)))
            return [int(spec) - 1]
        if isinstance(spec, (list, tuple)):
            return spec
        return [spec]

    def get_page_thumbnail(self, page_num, dpi=72):
        """Get page thumbnail as base64 PNG for web UI."""
        page = self.doc[page_num]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        return pix.tobytes("png")

    def close(self):
        """Close the document."""
        if self.doc:
            self.doc.close()
            self.doc = None


def main():
    """CLI interface."""
    import argparse
    parser = argparse.ArgumentParser(description="PDF Editor CLI")
    parser.add_argument("action", choices=[
        "info", "edit_text", "add_text", "delete_text", "insert_image",
        "add_watermark", "add_annotation", "add_highlight", "add_signature",
        "merge", "split", "reorder", "delete_pages", "extract_image", "rotate",
        "get_text", "save"
    ])
    parser.add_argument("file", help="PDF file path")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--page", type=int, help="Page number (0-based)")
    parser.add_argument("--pages", help="Page range (e.g., '1-3' or 'all')")
    parser.add_argument("--old-text", help="Text to find for replacement")
    parser.add_argument("--new-text", help="Replacement text")
    parser.add_argument("--text", help="Text to add")
    parser.add_argument("--x", type=float, help="X position")
    parser.add_argument("--y", type=float, help="Y position")
    parser.add_argument("--font-size", type=int, default=12)
    parser.add_argument("--image", help="Image file path")
    parser.add_argument("--width", type=float, help="Width")
    parser.add_argument("--height", type=float, help="Height")
    parser.add_argument("--watermark-text", help="Watermark text")
    parser.add_argument("--watermark-image", help="Watermark image path")
    parser.add_argument("--opacity", type=float, default=0.3)
    parser.add_argument("--angle", type=float, default=45)
    parser.add_argument("--icon", default="Note")
    parser.add_argument("--other-files", nargs="+", help="Other PDF files for merge")
    parser.add_argument("--ranges", nargs="+", help="Page ranges for split (start-end)")
    parser.add_argument("--order", nargs="+", type=int, help="New page order")
    parser.add_argument("--delete-page", nargs="+", type=int, help="Pages to delete")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--rotate-angle", type=int, default=90)

    args = parser.parse_args()
    editor = PDFEditor(args.file)

    try:
        if args.action == "info":
            print(json.dumps(editor.info(), indent=2, ensure_ascii=False))

        elif args.action == "get_text":
            page = args.page or 0
            texts = editor.get_page_text(page)
            print(json.dumps(texts, indent=2, ensure_ascii=False))

        elif args.action == "edit_text":
            result = editor.edit_text(
                args.page, args.old_text, args.new_text, font_size=args.font_size)
            print(json.dumps({"replaced": len(result), "positions": result}))

        elif args.action == "add_text":
            editor.add_text(args.page, args.text, args.x, args.y, args.font_size)
            print("Text added")

        elif args.action == "delete_text":
            count = editor.delete_text(args.page, args.text)
            print(f"Deleted {count} instances")

        elif args.action == "insert_image":
            editor.insert_image(args.page, args.image, args.x, args.y,
                               args.width, args.height)
            print("Image inserted")

        elif args.action == "add_watermark":
            count = editor.add_watermark(
                args.watermark_text or args.watermark_image,
                image_path=args.watermark_image,
                opacity=args.opacity, font_size=args.font_size,
                angle=args.angle, pages=args.pages or "all")
            print(f"Watermark added to {count} pages")

        elif args.action == "add_annotation":
            editor.add_annotation(args.page, args.text, args.x, args.y, icon=args.icon)
            print("Annotation added")

        elif args.action == "add_highlight":
            count = editor.add_highlight(args.page, args.text)
            print(f"Highlighted {count} instances")

        elif args.action == "add_signature":
            editor.add_signature(args.page, args.image, args.x, args.y,
                                 args.width or 150, args.height or 50)
            print("Signature added")

        elif args.action == "merge":
            path = editor.merge(args.other_files, args.output)
            print(f"Merged: {path}")

        elif args.action == "split":
            ranges = None
            if args.ranges:
                ranges = []
                for r in args.ranges:
                    parts = r.split("-")
                    ranges.append((int(parts[0]) - 1, int(parts[1]) - 1))
            results = editor.split(output_dir=args.output, ranges=ranges)
            print(f"Split into {len(results)} files")

        elif args.action == "reorder":
            editor.reorder_pages(args.order)
            print("Pages reordered")

        elif args.action == "delete_pages":
            editor.delete_pages(args.delete_page)
            print("Pages deleted")

        elif args.action == "extract_image":
            path = editor.extract_page_as_image(args.page, args.dpi, args.output)
            print(f"Extracted: {path}")

        elif args.action == "rotate":
            editor.rotate_page(args.page, args.rotate_angle)
            print(f"Page rotated {args.rotate_angle}°")

        elif args.action == "save":
            path = editor.save(args.output)
            print(f"Saved: {path}")

        # Auto-save for modifying actions
        if args.action in ("edit_text", "add_text", "delete_text", "insert_image",
                          "add_watermark", "add_annotation", "add_highlight",
                          "add_signature", "reorder", "delete_pages", "rotate"):
            if not args.output:
                path = editor.save()
                print(f"Saved: {path}")

    finally:
        editor.close()


if __name__ == "__main__":
    main()
