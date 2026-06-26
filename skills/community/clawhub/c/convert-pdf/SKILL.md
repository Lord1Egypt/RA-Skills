---
name: web2pdf
description: Convert web pages to PDF files. Use when user wants to save a webpage as PDF, download a webpage offline, or create a PDF from a URL. Triggered by: "web to pdf", "convert url to pdf", "save webpage as pdf", "download webpage pdf".
---

# Web to PDF Converter

Convert web pages to PDF files using Playwright.

## Usage

```bash
python pdf2.py <url> [output_filename]
```

## Examples

```bash
# Convert a webpage to PDF (uses domain name as filename)
python pdf2.py https://example.com

# Specify custom output filename
python pdf2.py https://example.com my-document.pdf

# Short URL (https:// is added automatically)
python pdf2.py example.com output.pdf
```

## Setup

If playwright is not installed:

```bash
pip install playwright
playwright install chromium
```

## Script Location

The script is located at: `skills/web2pdf/scripts/pdf2.py`

## Notes

- The script uses Chromium via Playwright for accurate rendering
- Waits for network idle before PDF generation to ensure page is fully loaded
- Output is saved to the current working directory
- A4 format with 20px margins is used by default
