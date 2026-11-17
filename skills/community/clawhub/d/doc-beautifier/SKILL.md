---
name: doc-beautifier
description: "Beautify Word documents (.docx) using a professional general template. Trigger when the user asks to: beautify/美化/排版/格式化 a Word document, apply a template/style to a .docx file, make a document look professional/clean/formatted, or clean up a document's formatting. Works by reading the source .docx, detecting document structure (title, headings, body), and applying consistent fonts, sizes, spacing, indentation, and page layout. Supports multiple template styles."
---

# doc-beautifier

Beautify .docx files with a professional general template. Preserves all original text content while applying consistent formatting.

## Quick Start

```bash
python3 scripts/beautify.py <input.docx> <output.docx>
# Optional template:
python3 scripts/beautify.py input.docx output.docx --template elegant
```

## Features

- **Structure Detection**: Heuristically identifies titles, headings (3 levels), and body paragraphs based on text patterns, length, and existing formatting
- **3 Built-in Templates**:
  - `standard` — Default professional template (A4, 微软雅黑 headings, 宋体 body, 1.5 line spacing)
  - `compact` — Tighter spacing, smaller margins, 1.25 line spacing (for dense documents)
  - `elegant` — Larger margins, refined colors, spacious layout (for formal reports)
- **Page Layout**: Sets A4 page size, proper margins, centered page numbers in footer
- **Content Preservation**: ALL original text is preserved; no content is added, removed, or reordered

## Template Specification

| Setting | standard | compact | elegant |
|---------|----------|---------|---------|
| Page margins | 2.54/3.18 cm | 2.0/2.5 cm | 3.0/3.5 cm |
| Title size | 22pt | 18pt | 26pt |
| H1 size | 16pt | 14pt | 16pt |
| H2 size | 14pt | 12pt | 14pt |
| H3 size | 12pt | 11pt | 12pt |
| Body size | 12pt(小四) | 11pt(五号) | 12pt(小四) |
| Line spacing | 1.5 | 1.25 | 1.5 |
| Body font | 宋体 | 宋体 | 宋体 |
| Heading font | 微软雅黑 | 微软雅黑 | 微软雅黑 |

## Workflow

1. **Locate** the user's input .docx file
2. **Run** `beautify.py` with desired template
3. **Validate** the output by unpacking or checking with python-docx
4. **Deliver** the beautified document path to the user

## Structure Detection Heuristics

The script identifies paragraph roles using:

- **First non-empty paragraph** → Document title
- **Already styled as Heading 1-3** → Preserve heading level
- **Bold + large font + short text (< 50 chars) without ending punctuation** → Heading
- **Starts with Chinese number (一、二、) or decimal (1.1, 2.3)** → Heading
- **Bold paragraphs under 60 chars** → Heading
- **Everything else** → Body text

## Customization

Edit the `TEMPLATES` dictionary in `scripts/beautify.py` to:

- Change colors, fonts, sizes
- Add new template variants
- Adjust line spacing or indentation
- Modify page margins

## Requirements

- `python-docx` (install: `pip install python-docx`)
- Python 3.8+
