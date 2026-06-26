# PDF Form Filling Guide

This file covers everything needed to read, inspect, and fill PDF forms —
both AcroForm (standard fillable fields) and more complex cases.

---

## Step 0: Check if the PDF has fillable fields

Always run this first:

```bash
python scripts/check_fillable_fields.py input.pdf
```

If no fields are found, the PDF is a flat (non-fillable) scan — use the
overlay annotation approach at the bottom of this file instead.

---

## AcroForm Filling with pypdf

### Read existing field values

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields()
if fields:
    for name, field in fields.items():
        ftype = field.get("/FT", "unknown")
        value = field.get("/V", "[empty]")
        print(f"  {name!r:30s}  type={ftype}  value={value}")
else:
    print("No fillable fields found.")
```

### Fill and save

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("blank_form.pdf")
writer = PdfWriter()
writer.append(reader)

writer.update_page_form_field_values(
    writer.pages[0],
    {
        "full_name":  "Alice Chen",
        "email":      "alice@example.com",
        "date":       "2025-03-12",
        "agree":      "Yes",   # checkbox: "Yes" or "Off"
        "department": "Engineering",
    },
    auto_regenerate=False,   # False = preserve visual appearance
)

with open("filled_form.pdf", "wb") as f:
    writer.write(f)
```

**Important:** Use the exact field name strings returned by `get_fields()`.
Field names are case-sensitive.

### Multi-page forms

```python
writer.append(reader)
for page in writer.pages:
    writer.update_page_form_field_values(page, data, auto_regenerate=False)
```

---

## pdf-lib (JavaScript) — Best for Complex Forms

Use pdf-lib when:
- pypdf fails to preserve visual appearance
- The form uses XFA (XML Forms Architecture)
- You need pixel-perfect field rendering

### Setup

```bash
npm install pdf-lib
```

### Fill form with pdf-lib

```javascript
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

async function fillForm(inputPath, outputPath, data) {
  const pdfBytes  = fs.readFileSync(inputPath);
  const pdfDoc    = await PDFDocument.load(pdfBytes);
  const form      = pdfDoc.getForm();

  // Text fields
  for (const [fieldName, value] of Object.entries(data.text || {})) {
    try {
      form.getTextField(fieldName).setText(value);
    } catch (e) {
      console.warn(`  ⚠ Text field not found: ${fieldName}`);
    }
  }

  // Checkboxes
  for (const [fieldName, checked] of Object.entries(data.checkboxes || {})) {
    try {
      const cb = form.getCheckBox(fieldName);
      checked ? cb.check() : cb.uncheck();
    } catch (e) {
      console.warn(`  ⚠ Checkbox not found: ${fieldName}`);
    }
  }

  // Dropdowns
  for (const [fieldName, value] of Object.entries(data.dropdowns || {})) {
    try {
      form.getDropdown(fieldName).select(value);
    } catch (e) {
      console.warn(`  ⚠ Dropdown not found: ${fieldName}`);
    }
  }

  // Flatten (make non-editable) — optional
  // form.flatten();

  const outBytes = await pdfDoc.save();
  fs.writeFileSync(outputPath, outBytes);
  console.log(`✓ Saved → ${outputPath}`);
}

fillForm("blank.pdf", "filled.pdf", {
  text:       { full_name: "Alice Chen", email: "alice@example.com" },
  checkboxes: { agree_terms: true },
  dropdowns:  { department: "Engineering" },
});
```

---

## Flat PDF Overlay (Non-Fillable Forms)

When the PDF has no fillable fields, place text directly on the page
using coordinate-based annotations.

### Step 1: Find coordinates

```python
# Use pdfplumber to inspect the page layout and find where to place text
import pdfplumber

with pdfplumber.open("flat_form.pdf") as pdf:
    page = pdf.pages[0]
    print(f"Page size: {page.width} x {page.height} pts")
    # Visually: (0,0) is bottom-left in PDF coordinates
    # pdfplumber uses top-left origin — convert: pdf_y = page.height - plumber_y
```

### Step 2: Overlay text with reportlab + merge

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter
import io

def create_overlay(fields: dict, pagesize=letter) -> bytes:
    """fields = {(x, y): 'text', ...}  — PDF coordinate system (bottom-left origin)"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=pagesize)
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0, 0, 0)
    for (x, y), text in fields.items():
        c.drawString(x, y, str(text))
    c.save()
    buf.seek(0)
    return buf.read()

overlay_data = create_overlay({
    (150, 640): "Alice Chen",
    (150, 610): "alice@example.com",
    (350, 610): "2025-03-12",
})

# Merge overlay onto original
overlay_reader = PdfReader(io.BytesIO(overlay_data))
orig_reader    = PdfReader("flat_form.pdf")
writer         = PdfWriter()

for i, page in enumerate(orig_reader.pages):
    if i < len(overlay_reader.pages):
        page.merge_page(overlay_reader.pages[i])
    writer.add_page(page)

with open("filled_flat.pdf", "wb") as f:
    writer.write(f)
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Fields appear blank after filling | Try `auto_regenerate=True` in pypdf |
| Field names not matching | Use `get_fields()` to list exact names |
| Visual appearance broken | Switch to pdf-lib (JS) |
| "XFA form" error | XFA not supported by pypdf; use pdf-lib |
| Flat form, no fields | Use overlay approach above |
| Text outside field bounds | Reduce font size or check coordinates |
