---
name: ClawPDF Master
slug: clawpdf-master
version: 1.0.0
description: "Advanced PDF tool: text/table extraction, creation, merge/split, forms, OCR — PLUS unique feature: PDF-to-Markdown conversion, batch folder processing and automatic AI document summaries."
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["pdftotext","qpdf","python3"]}}}
---

# ClawPDF Master

Komplet PDF-håndteringsværktøj baseret på velafprøvede metoder (pypdf, pdfplumber,
reportlab, poppler), **forbedret med 3 unikke features** som ingen anden PDF-skill har:

## 🆕 Unikke features (findes ikke i originalen)

### Feature 1: PDF → Markdown-konvertering
Konverter enhver PDF til ren, struktureret Markdown (overskrifter, lister, tabeller som
GitHub-flavored markdown). Perfekt til AI-agenter der vil genbruge indhold.

```bash
python3 scripts/pdf_to_markdown.py input.pdf output.md
```

### Feature 2: Batch-behandling af mapper
Behandle HELE mapper med PDF'er på én gang — ekstraher, konverter eller merge alle filer:

```bash
python3 scripts/pdf_batch.py ./mappe --action extract --out ./resultater
python3 scripts/pdf_batch.py ./mappe --action merge --out samlet.pdf
```

### Feature 3: Automatisk dokument-resumé
Få et struktureret resumé af et dokument (emne, nøglepunkter, tal, datoer, handlinger)
uden at læse hele filen — perfekt til hurtig gennemgang af kontrakter og rapporter:

```bash
python3 scripts/pdf_summary.py kontrakt.pdf
```

---

## Standard-operationer (arvet + forbedret)

### Læs tekst
```python
from pypdf import PdfReader
reader = PdfReader("doc.pdf")
for page in reader.pages:
    print(page.extract_text())
```

### Læs tabeller (med layout-bevarelse)
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            print(table)
```

### Create PDF
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
c = canvas.Canvas("ny.pdf", pagesize=A4)
c.drawString(100, 800, "Hej verden!")
c.save()
```

### Merge / split / roter / vandmærke / krypter
```bash
# Merge
qpdf --empty --pages a.pdf b.pdf -- merged.pdf
# Split (side 1-5)
qpdf input.pdf --pages . 1-5 -- sider1-5.pdf
# Roter side 1 +90°
qpdf input.pdf output.pdf --rotate=+90:1
# Remove password
qpdf --password=hemmeligt --decrypt laas.pdf aaben.pdf
```

### OCR af scannede PDF'er
```bash
# Kræver: pip install pytesseract pdf2image + tesseract
python3 scripts/pdf_ocr.py scanned.pdf --lang dan --out tekst.txt
```

### Udfyld formularer
Se `docs/forms.md` for trin-for-trin (pdf-lib / pypdf).

---

## Hurtig reference

| Task | Tool | Command |
|--------|---------|----------|
| Læs tekst | pypdf/pdfplumber | `page.extract_text()` |
| Læs tabeller | pdfplumber | `page.extract_tables()` |
| Create PDF | reportlab | Canvas/Platypus |
| Merge | qpdf | `qpdf --empty --pages ...` |
| Split | qpdf | `qpdf input.pdf --pages . 1-5 -- out.pdf` |
| OCR | tesseract | `python3 scripts/pdf_ocr.py` |
| → Markdown | **unik** | `python3 scripts/pdf_to_markdown.py` |
| Batch-mappe | **unik** | `python3 scripts/pdf_batch.py ./mappe` |
| Summary | **unique** | `python3 scripts/pdf_summary.py doc.pdf` |

## Feedback
- Hjælpsom? → `clawhub star clawpdf-master`
- Opdateringer: `clawhub sync`
---
