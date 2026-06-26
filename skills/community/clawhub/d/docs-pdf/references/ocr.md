# OCR Reference

Read this when dealing with scanned PDFs that have no selectable text.

---

## Full OCR Pipeline

```python
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

def ocr_pdf(
    pdf_path: str,
    output_txt: str = None,
    lang: str = "chi_sim+eng",   # language(s)
    dpi:  int = 300,             # 300 = standard; 600 = fine print
    psm:  int = 6,               # page segmentation mode (see below)
) -> str:
    print(f"Converting {pdf_path} to images at {dpi} DPI...")
    images = convert_from_path(pdf_path, dpi=dpi)

    pages = []
    for i, img in enumerate(images, 1):
        print(f"  OCR page {i}/{len(images)}...", end="\r")
        text = pytesseract.image_to_string(
            img,
            lang=lang,
            config=f"--psm {psm} --oem 3",
        )
        pages.append(f"=== Page {i} ===\n{text}")

    full_text = "\n\n".join(pages)
    if output_txt:
        Path(output_txt).write_text(full_text, encoding="utf-8")
        print(f"\n✓ OCR text → {output_txt}")
    return full_text
```

---

## Language Codes

| Language | Code |
|---|---|
| English | `eng` |
| Simplified Chinese | `chi_sim` |
| Traditional Chinese | `chi_tra` |
| Japanese | `jpn` |
| Korean | `kor` |
| French | `fra` |
| German | `deu` |
| Spanish | `spa` |
| Mixed | `chi_sim+eng` |

Install language packs:

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra tesseract-ocr-jpn

# macOS (Homebrew) — installs ALL language packs at once
brew install tesseract-lang
```

> ⚠️ **macOS 重要提示:** `brew install tesseract` 仅包含英文语言包。
> 中文、日文等其他语言需要额外执行 `brew install tesseract-lang`，否则 OCR 会输出乱码或空白结果。

List installed languages:
```bash
tesseract --list-langs
```

---

## Page Segmentation Modes (--psm)

| PSM | Description |
|---|---|
| 3 | Fully automatic (default) |
| 6 | Uniform block of text — **best for most scanned documents** |
| 4 | Single column, variable sizes |
| 11 | Sparse text — good for forms with scattered fields |
| 12 | Sparse text + OSD |
| 13 | Raw line — single text line |

---

## Image Preprocessing (Improve Accuracy)

Apply before passing to pytesseract:

```python
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

def preprocess(img: Image.Image, target_dpi=300) -> Image.Image:
    # 1. Grayscale
    img = img.convert("L")

    # 2. Upscale if needed (Tesseract works best at ~300 DPI)
    w, h = img.size
    if w < 1500:
        scale = 1500 / w
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # 3. Contrast boost
    img = ImageEnhance.Contrast(img).enhance(1.8)

    # 4. Sharpen
    img = img.filter(ImageFilter.SHARPEN)

    # 5. Binarize (simple threshold — swap for Otsu if needed)
    arr   = np.array(img)
    thresh = arr.mean()
    arr   = ((arr > thresh) * 255).astype(np.uint8)
    img   = Image.fromarray(arr)

    return img

# Usage
images = convert_from_path("scanned.pdf", dpi=300)
for img in images:
    clean = preprocess(img)
    text  = pytesseract.image_to_string(clean, lang="chi_sim+eng", config="--psm 6")
```

### Deskew (fix tilted scans)

```python
# pip install deskew
from deskew import determine_skew
import numpy as np
from PIL import Image

def deskew(img: Image.Image) -> Image.Image:
    arr   = np.array(img.convert("L"))
    angle = determine_skew(arr)
    if abs(angle) > 0.5:
        img = img.rotate(angle, expand=True, fillcolor=255)
    return img
```

---

## Get Bounding Boxes (word positions)

```python
data = pytesseract.image_to_data(
    img,
    lang="chi_sim+eng",
    output_type=pytesseract.Output.DICT,
)

for i, text in enumerate(data["text"]):
    if text.strip() and int(data["conf"][i]) > 60:   # confidence > 60%
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        print(f"{text!r:20s}  conf={data['conf'][i]}  @({x},{y},{w},{h})")
```

---

## Batch OCR Script

```python
# Run: python scripts/ocr_pdf.py --input ./scans/ --lang chi_sim+eng
from pathlib import Path
import argparse
from pdf2image import convert_from_path
import pytesseract

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--lang",  default="chi_sim+eng")
parser.add_argument("--dpi",   type=int, default=300)
args = parser.parse_args()

for pdf in Path(args.input).glob("*.pdf"):
    out = pdf.with_suffix(".txt")
    print(f"Processing {pdf.name}...")
    imgs = convert_from_path(str(pdf), dpi=args.dpi)
    text = "\n\n".join(
        pytesseract.image_to_string(img, lang=args.lang, config="--psm 6")
        for img in imgs
    )
    out.write_text(text, encoding="utf-8")
    print(f"  → {out.name}")
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Garbled Chinese / boxes | Install `tesseract-ocr-chi-sim`, use `lang="chi_sim"` |
| Very low accuracy | Increase DPI to 600, apply preprocessing |
| Slow on large PDFs | Process pages in parallel with `concurrent.futures` |
| Mixed columns detected as one block | Try `--psm 4` or `--psm 3` |
| Form fields missed | Use `--psm 11` (sparse text) |
