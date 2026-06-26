# Creating PDFs with reportlab

Read this file when you need to build a PDF from scratch — reports, invoices,
cover pages, branded documents, multi-page layouts with headers/footers.

---

## Two APIs

| API | When to use |
|---|---|
| **Platypus** (high-level) | Multi-page documents, flowing text, automatic pagination |
| **Canvas** (low-level) | Precise pixel/point control, diagrams, cover pages, overlays |

---

## Platypus: Flowing Documents

### Minimal example

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate(
    "output.pdf", pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2*cm,
)
styles = getSampleStyleSheet()
story  = []

story.append(Paragraph("Report Title", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Body text goes here.", styles["Normal"]))

doc.build(story)
```

### Custom paragraph styles

```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.colors import HexColor

body_style = ParagraphStyle(
    "body",
    parent=styles["Normal"],
    fontSize=10,
    fontName="Helvetica",
    leading=16,              # line height
    alignment=TA_JUSTIFY,
    spaceBefore=4,
    spaceAfter=4,
    textColor=HexColor("#1A1A2E"),
)

heading_style = ParagraphStyle(
    "h2",
    parent=styles["Normal"],
    fontSize=14,
    fontName="Helvetica-Bold",
    textColor=HexColor("#D97757"),
    spaceBefore=16,
    spaceAfter=6,
)
```

### Tables

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ["Name",  "Role",       "Department"],
    ["Alice", "Engineer",   "R&D"],
    ["Bob",   "Designer",   "Product"],
]

col_widths = [120, 120, 120]
t = Table(data, colWidths=col_widths)
t.setStyle(TableStyle([
    # Header row
    ("BACKGROUND",   (0, 0), (-1,  0), HexColor("#D97757")),
    ("TEXTCOLOR",    (0, 0), (-1,  0), colors.white),
    ("FONTNAME",     (0, 0), (-1,  0), "Helvetica-Bold"),
    # Body rows — alternating
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F8F4EF")]),
    # Grid
    ("GRID",         (0, 0), (-1, -1), 0.5, HexColor("#E0D8D0")),
    # Padding
    ("TOPPADDING",    (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING",   (0, 0), (-1, -1), 8),
]))
story.append(t)
```

### Page breaks & keep-together

```python
from reportlab.platypus import PageBreak, KeepTogether

story.append(PageBreak())

# Prevent a block from splitting across pages
story.append(KeepTogether([heading, paragraph]))
```

### Horizontal rule

```python
from reportlab.platypus import HRFlowable

story.append(HRFlowable(width="100%", thickness=1.5, color=HexColor("#D97757")))
```

### Images

```python
from reportlab.platypus import Image as RLImage

img = RLImage("logo.png", width=4*cm, height=2*cm)
story.append(img)
```

---

## Custom Page Template (Headers & Footers)

```python
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm

W, H = A4

def on_page(c, doc):
    c.saveState()
    # Header
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(HexColor("#1A1A2E"))
    c.drawString(2*cm, H - 1.5*cm, "My Document Title")
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#9E9E9E"))
    c.drawRightString(W - 2*cm, H - 1.5*cm, "Confidential")
    # Header rule
    c.setStrokeColor(HexColor("#E0D8D0"))
    c.setLineWidth(0.5)
    c.line(2*cm, H - 1.7*cm, W - 2*cm, H - 1.7*cm)
    # Footer page number
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#9E9E9E"))
    c.drawCentredString(W / 2, 1.2*cm, f"— {doc.page} —")
    c.restoreState()

frame = Frame(2*cm, 2*cm, W - 4*cm, H - 4.5*cm, id="body")
template = PageTemplate(id="main", frames=[frame], onPage=on_page)
doc = BaseDocTemplate("output.pdf", pageTemplates=[template])
doc.build(story)
```

---

## Canvas: Low-Level Drawing

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

W, H = A4
c = canvas.Canvas("drawing.pdf", pagesize=A4)

# Text
c.setFont("Helvetica-Bold", 24)
c.setFillColor(HexColor("#1A1A2E"))
c.drawString(50, H - 100, "Hello World")

# Colored rectangle
c.setFillColor(HexColor("#D97757"))
c.rect(50, H - 200, 200, 80, fill=1, stroke=0)

# Circle
c.setFillColor(HexColor("#F5A623"))
c.circle(300, H - 160, 40, fill=1, stroke=0)

# Line
c.setStrokeColor(HexColor("#E0D8D0"))
c.setLineWidth(1)
c.line(50, H - 220, W - 50, H - 220)

# New page
c.showPage()

c.save()
```

---

## Subscripts & Superscripts

**Never use Unicode** characters like ₂ ⁰ — they render as black boxes.

```python
# In Paragraph objects only:
Paragraph("H<sub>2</sub>O",         styles["Normal"])   # subscript
Paragraph("E = mc<super>2</super>", styles["Normal"])   # superscript

# In canvas drawString: manually shift baseline and reduce font size
c.setFont("Helvetica", 7)
c.drawString(x + offset, y + 4, "2")   # superscript
```

---

## Common Page Sizes (points)

| Name | Width | Height |
|---|---|---|
| A4 | 595 | 842 |
| Letter | 612 | 792 |
| Legal | 612 | 1008 |
| A3 | 842 | 1191 |

1 inch = 72 points = `1*inch` from `reportlab.lib.units`
