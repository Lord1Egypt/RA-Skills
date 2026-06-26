---
name: pdf-tool
description: Work with PDF files including merge, split, extract text, and convert. Use when user needs to combine multiple PDFs, split a PDF into pages, extract text from PDF, convert PDF to images, or compress PDF files.
---

# PDF Tool

Work with PDF files including merge, split, extract text, and convert.

## Quick Start

```bash
# Extract text from PDF
python scripts/pdf.py document.pdf --extract-text

# Merge PDFs
python scripts/pdf.py --merge file1.pdf file2.pdf --output combined.pdf
```

## Usage

```bash
python scripts/pdf.py [OPTIONS]

Options:
  --extract-text      Extract text from PDF
  --extract-images    Extract images from PDF
  --merge FILES       Merge multiple PDFs
  --split N           Split into N pages per file
  --page PAGE         Extract specific page
  --info              Show PDF information
  --output PATH       Output file path
```

## Examples

```bash
# Extract all text
python scripts/pdf.py doc.pdf --extract-text

# Extract page 5
python scripts/pdf.py doc.pdf --page 5 --output page5.pdf

# Merge files
python scripts/pdf.py --merge a.pdf b.pdf c.pdf --output merged.pdf

# Split into single pages
python scripts/pdf.py doc.pdf --split 1 --output split/

# Get PDF info
python scripts/pdf.py doc.pdf --info
```

## Features

- Extract text from PDF
- Extract images from PDF
- Merge multiple PDFs
- Split PDF into pages
- Extract specific pages
- Get PDF metadata
- Basic compression
