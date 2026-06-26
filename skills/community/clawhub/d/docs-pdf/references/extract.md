# Advanced Extraction Reference

Read this when you need more than basic `extract_text()` — coordinate-based
cropping, word-level data, complex tables, or embedded image extraction.

---

## pdfplumber: Full API

### Open options

```python
import pdfplumber

# Standard
with pdfplumber.open("doc.pdf") as pdf: ...

# Password-protected
with pdfplumber.open("locked.pdf", password="secret") as pdf: ...

# Laparams tuning (affects how characters are grouped into words/lines)
with pdfplumber.open("doc.pdf", laparams={"line_overlap": 0.5}) as pdf: ...
```

### Text extraction options

```python
page = pdf.pages[0]

# Basic — preserves line breaks, reasonable layout
text = page.extract_text(x_tolerance=3, y_tolerance=3)

# Word-level — returns list of dicts with coordinates
words = page.extract_words(
    x_tolerance=5,
    y_tolerance=3,
    keep_blank_chars=False,
    use_text_flow=True,      # respects reading order
    extra_attrs=["fontname", "size"],  # include font info
)
# Each word: {'text', 'x0', 'y0', 'x1', 'y1', 'doctop', 'top', 'bottom',
#             'upright', 'direction', 'fontname', 'size'}

# Character-level — maximum granularity
chars = page.chars
# Each char: {'text', 'x0', 'y0', 'x1', 'y1', 'fontname', 'size', 'stroking_color', ...}
```

### Crop to region

```python
# Coordinates: (x0, top, x1, bottom) — top-left origin, units = PDF points
# Page dimensions: page.width, page.height

# Extract only the top half of the page
top_half = page.crop((0, 0, page.width, page.height / 2))
text = top_half.extract_text()

# Extract a specific rectangle (e.g., a sidebar)
sidebar = page.crop((400, 100, page.width, 700))
```

### Table extraction settings

```python
tables = page.extract_tables({
    "vertical_strategy":   "lines",    # "lines" | "lines_strict" | "text" | "explicit"
    "horizontal_strategy": "lines",
    "snap_tolerance":       3,          # how close lines must be to snap together
    "join_tolerance":       3,
    "edge_min_length":     3,
    "min_words_vertical":  3,
    "min_words_horizontal":1,
    "text_tolerance":       3,
    "text_x_tolerance":    3,
    "text_y_tolerance":    3,
})

# For borderless tables, switch to text-based strategy:
tables = page.extract_tables({
    "vertical_strategy":   "text",
    "horizontal_strategy": "text",
})
```

### Convert all tables to DataFrames

```python
import pdfplumber, pandas as pd
from pathlib import Path

def extract_all_tables(pdf_path: str, output_xlsx: str):
    all_dfs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            for tbl_num, table in enumerate(page.extract_tables(), 1):
                if not table or len(table) < 2:
                    continue
                # First row = header (if it looks like one)
                headers = [str(h or f"col_{i}") for i, h in enumerate(table[0])]
                df = pd.DataFrame(table[1:], columns=headers)
                df.insert(0, "_page",  page_num)
                df.insert(1, "_table", tbl_num)
                all_dfs.append(df)
    if all_dfs:
        with pd.ExcelWriter(output_xlsx) as writer:
            for i, df in enumerate(all_dfs):
                df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
        print(f"✓ {len(all_dfs)} tables → {output_xlsx}")
    else:
        print("No tables found.")
```

---

## pypdf: Text Extraction (Basic)

Use pdfplumber for layout-sensitive work. pypdf's extract_text is simpler:

```python
from pypdf import PdfReader

reader = PdfReader("doc.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text(
        extraction_mode="layout",   # better than default for columns
        layout_mode_space_vertically=False,
    )
    print(f"--- Page {i+1} ---\n{text}")
```

---

## Extract Embedded Images

### Method 1: pypdf (Python)

```python
from pypdf import PdfReader
from pathlib import Path

def extract_images(pdf_path: str, out_dir: str = "."):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    reader = PdfReader(pdf_path)
    count = 0
    for p_num, page in enumerate(reader.pages):
        for img in page.images:
            ext  = img.name.split(".")[-1] or "png"
            name = f"{out_dir}/p{p_num+1}_{img.name}"
            Path(name).write_bytes(img.data)
            print(f"  Saved: {name}  size={img.image.size}")
            count += 1
    print(f"✓ {count} images extracted")
```

### Method 2: pdfimages CLI (lossless, recommended)

```bash
# Extract all images preserving original format
pdfimages -all input.pdf ./images/img

# JPEG only
pdfimages -j input.pdf ./images/img

# PNG only
pdfimages -png input.pdf ./images/img

# Specific pages
pdfimages -f 1 -l 5 input.pdf ./images/img
```

---

## Extract Metadata

```python
from pypdf import PdfReader

reader = PdfReader("doc.pdf")
meta   = reader.metadata

print(f"Title:    {meta.title}")
print(f"Author:   {meta.author}")
print(f"Subject:  {meta.subject}")
print(f"Creator:  {meta.creator}")
print(f"Producer: {meta.producer}")
print(f"Created:  {meta.creation_date}")
print(f"Modified: {meta.modification_date}")
print(f"Pages:    {len(reader.pages)}")
print(f"Encrypted:{reader.is_encrypted}")
```

---

## pdftotext CLI (poppler)

Fast and reliable for plain text extraction:

```bash
# Basic
pdftotext input.pdf output.txt

# Preserve layout
pdftotext -layout input.pdf output.txt

# Pages 1–5 only
pdftotext -f 1 -l 5 input.pdf output.txt

# HTML output (preserves some formatting)
pdftotext -htmlmeta input.pdf output.html
```
