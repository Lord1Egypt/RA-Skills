# PDF Security Reference

Covers watermarks, encryption, permission flags, and metadata redaction.

---

## Watermarks

### Text watermark (diagonal, semi-transparent)

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter
import io

def make_text_watermark(
    text="CONFIDENTIAL",
    font_size=60,
    color="#D97757",
    alpha=0.12,
    angle=45,
    pagesize=A4,
) -> bytes:
    buf = io.BytesIO()
    c   = canvas.Canvas(buf, pagesize=pagesize)
    c.saveState()
    c.setFillColor(HexColor(color))
    c.setFillAlpha(alpha)
    c.setFont("Helvetica-Bold", font_size)
    c.translate(pagesize[0] / 2, pagesize[1] / 2)
    c.rotate(angle)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    buf.seek(0)
    return buf.read()

def apply_watermark(src: str, dst: str, watermark_bytes: bytes):
    wm_page = PdfReader(io.BytesIO(watermark_bytes)).pages[0]
    reader  = PdfReader(src)
    writer  = PdfWriter()
    for page in reader.pages:
        page.merge_page(wm_page)
        writer.add_page(page)
    with open(dst, "wb") as f:
        writer.write(f)
    print(f"✓ Watermarked → {dst}")

wm = make_text_watermark("DRAFT", color="#FF0000", alpha=0.08)
apply_watermark("doc.pdf", "doc_draft.pdf", wm)
```

### Image watermark

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
import io

def make_image_watermark(logo_path: str, opacity=0.15, pagesize=A4) -> bytes:
    buf = io.BytesIO()
    c   = canvas.Canvas(buf, pagesize=pagesize)
    c.saveState()
    c.setFillAlpha(opacity)
    W, H = pagesize
    img_w, img_h = 200, 200   # adjust to logo dimensions
    c.drawImage(logo_path, (W - img_w) / 2, (H - img_h) / 2,
                width=img_w, height=img_h, mask="auto")
    c.restoreState()
    c.save()
    buf.seek(0)
    return buf.read()
```

---

## Encryption

### AES-256 encrypt with permissions

```python
from pypdf import PdfReader, PdfWriter

def encrypt_pdf(
    src: str,
    dst: str,
    user_password: str,
    owner_password: str,
    allow_printing=True,
    allow_copying=False,
):
    reader = PdfReader(src)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Build permissions flag (bitmask)
    # Bit positions (1-indexed, from PDF spec):
    #   3  = print (low quality)
    #   4  = modify
    #   5  = copy / extract
    #   6  = add/modify annotations
    #   9  = fill forms
    #  10  = extract for accessibility
    #  11  = assemble (insert/delete pages)
    #  12  = print (high quality)
    perms = 0
    if allow_printing:
        perms |= (1 << 2)   # bit 3
        perms |= (1 << 11)  # bit 12 (high quality)
    if allow_copying:
        perms |= (1 << 4)   # bit 5

    writer.encrypt(
        user_password=user_password,
        owner_password=owner_password,
        use_128bit=False,        # False = AES-256
        permissions_flag=perms,
    )
    with open(dst, "wb") as f:
        writer.write(f)
    print(f"✓ Encrypted → {dst}")
```

### Decrypt / remove password

```python
# Python
reader = PdfReader("locked.pdf", password="secret")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
with open("unlocked.pdf", "wb") as f:
    writer.write(f)

# CLI (qpdf)
# qpdf --password=secret --decrypt locked.pdf unlocked.pdf
```

---

## Permission Flag Reference

| Bit | Value | Meaning |
|---|---|---|
| 3  | 0x004  | Allow printing (low quality) |
| 4  | 0x008  | Allow content modification |
| 5  | 0x010  | Allow text/image copying |
| 6  | 0x020  | Allow annotation/form modification |
| 9  | 0x100  | Allow form filling |
| 10 | 0x200  | Allow accessibility extraction |
| 11 | 0x400  | Allow document assembly |
| 12 | 0x800  | Allow high-quality printing |

Common combinations:
- **Read-only, printable**: bits 3 + 12 → `0x804`
- **Full access**: all bits → `0xFFC`
- **Locked (view only)**: `0x000`

---

## Metadata Redaction

```python
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, createStringObject

reader = PdfReader("doc.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

# Clear metadata
writer.add_metadata({
    "/Title":    "",
    "/Author":   "",
    "/Subject":  "",
    "/Creator":  "",
    "/Producer": "",
    "/Keywords": "",
})

with open("redacted_meta.pdf", "wb") as f:
    writer.write(f)
```
