---
name: PDF OCR using Gemini LLM
description: Extract text from PDFs using Google Gemini OCR. Use when extracting text from PDFs, performing OCR on scanned documents, or processing image-based PDFs.
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_API_KEY
    primaryEnv: GOOGLE_API_KEY
    install:
      - kind: uv
        package: google-genai
        label: "Python deps"
      - kind: uv
        package: pymupdf
      - kind: uv
        package: pydantic
      - kind: uv
        package: pydantic-settings
---

## Purpose

Use geminipdfocr to extract text from PDF documents via OCR (Google Gemini).

## Data and privacy

**Full page images/files are sent to Google's API.** PDFs are split into single-page files and each page is uploaded to Google Gemini for OCR. There are no hidden exfiltration endpoints or other data collection. Do not use with highly sensitive documents unless you accept that content is sent to Google.

## Setup (venv installation)

Before first use, create and activate the virtual environment:

```bash
cd geminipdfocr && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

Set `GOOGLE_API_KEY` in your environment before running (e.g. `export GOOGLE_API_KEY=your-key`).

## How to use

When requested to extract text or perform OCR on a PDF:

1. Run: `cd geminipdfocr && source venv/bin/activate && python -m geminipdfocr <path-to-pdf> [--json] [--output <file>]`
2. Use `--json` for structured data.
3. Use `--max-pages N` for testing or very long documents.
4. Use `--quiet` to suppress progress logs.

## Requirements

- A valid PDF file path.
- `GOOGLE_API_KEY` set in the process environment (e.g. `export GOOGLE_API_KEY=your-key`).

## CLI options

| Option | Description |
|--------|-------------|
| `pdf_path` | One or more PDF file paths (positional) |
| `--max-pages N` | Limit pages per PDF |
| `--json` | Output structured JSON instead of plain text |
| `--output FILE` | Write result to file (default: stdout) |
| `--quiet` | Suppress INFO/DEBUG logs |
