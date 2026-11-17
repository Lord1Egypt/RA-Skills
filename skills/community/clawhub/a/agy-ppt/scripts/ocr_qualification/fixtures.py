"""Small project-owned synthetic sources for Phase 15.6 qualification."""
from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageDraw
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject, NumberObject


def pdf_fixture(*, pages: int = 1, rotation: int = 0, crop: bool = False, password: str | None = None) -> bytes:
    if isinstance(pages, bool) or not isinstance(pages, int) or pages < 1:
        raise ValueError("pages must be positive")
    writer = PdfWriter()
    for index in range(pages):
        page = writer.add_blank_page(width=72, height=48)
        page.mediabox = ArrayObject([FloatObject(0), FloatObject(0), FloatObject(72), FloatObject(48)])
        if crop and index == 0:
            page[NameObject("/CropBox")] = ArrayObject([FloatObject(6), FloatObject(6), FloatObject(66), FloatObject(42)])
        if rotation and index == 0:
            page[NameObject("/Rotate")] = NumberObject(rotation)
    if password is not None:
        writer.encrypt(password)
    stream = BytesIO()
    writer.write(stream)
    return stream.getvalue()


def image_fixture(format_name: str, *, mode: str = "RGB", exif_orientation: int | None = None) -> bytes:
    if format_name not in {"PNG", "JPEG", "TIFF"}:
        raise ValueError("unsupported qualification fixture format")
    size = (96, 48)
    color = {"RGB": "white", "L": 255, "RGBA": (255, 255, 255, 128), "CMYK": (0, 0, 0, 0)}[mode]
    image = Image.new(mode, size, color)
    drawing = ImageDraw.Draw(image)
    drawing.rectangle((4, 4, 91, 43), outline=0 if mode == "L" else "black")
    drawing.text((12, 16), "AGY OCR 15", fill=0 if mode in {"L", "CMYK"} else "black")
    output = BytesIO()
    options: dict[str, object] = {}
    if exif_orientation is not None:
        exif = Image.Exif()
        exif[274] = exif_orientation
        options["exif"] = exif
    image.save(output, format=format_name, **options)
    image.close()
    return output.getvalue()


def multipage_tiff_fixture() -> bytes:
    first = Image.new("RGB", (24, 16), "white")
    second = Image.new("RGB", (24, 16), "black")
    output = BytesIO()
    first.save(output, format="TIFF", save_all=True, append_images=[second])
    first.close()
    second.close()
    return output.getvalue()
