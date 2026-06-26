---
name: daily-scan
description: "Scan photographed documents into searchable PDFs with OCR and stable file naming. Use when the user sends document photos and asks to scan, save, archive, OCR, or retrieve prior scans. Trigger words: 스캔 or scan for a single page, 스캔연속 or scan multi for a multi-page combined PDF, and 스캔찾아 or scan find for retrieval."
---

# Daily Scan

## Overview

Turn phone photos of documents into searchable PDFs with OCR and stable filenames based on capture date and headline text. Preserve the original photo, generate a readable scan-like PDF, and support later retrieval of saved scan files.

## Runtime Requirements

- Default OCR path: local Tesseract CLI
- Required local dependencies for the stable path:
  - `tesseract`
  - Python packages used by bundled scripts: `opencv-python` or `cv2`, `Pillow`, and either `reportlab` or `ocrmypdf` depending on the active PDF path
- Optional/experimental OCR path:
  - PaddleOCR-based script exists but is not the default stable engine
- No cloud upload is required for core operation
- The skill assumes bundled helper scripts under `scripts/` are present and callable by the host agent

## Workflow

1. Confirm the trigger.
 - `스캔` / `scan` — one-page processing
 - `스캔연속` / `scan multi` — combine multiple photos into one searchable PDF
 - `스캔찾아` / `scan find` — search previously saved scan files
2. Collect attached image files or search keywords.
3. Apply document-style cleanup when possible.
 - straighten or rotate when needed
 - improve contrast for readability
 - keep output practical rather than over-processed
4. Run OCR in Korean and English.
5. Build the filename as:
 - `YYYY-MM-DD + headline text`
 - derive headline text from the top 2 to 3 OCR lines
6. Create a searchable PDF.
7. Save output to the local storage destination.
8. Keep the original image with the processed result.
9. For retrieval requests, search by date, headline text, or OCR keyword in the configured scan storage path.
10. Return:
 - filename
 - save location
 - OCR title line

## Storage Rules

- Default local staging/search path: `daily-scan-storage/YYYY-MM`
- This skill is designed for local scan creation and retrieval only
- Use year/month folder structure
- Do not auto-classify document types

## Operating Rules

- For multi-page capture, combine pages into one PDF only when the trigger is `스캔연속` or `scan multi`
- OCR language defaults to Korean plus English
- Retrieval requests should search existing saved scan outputs before asking follow-up questions
- Keep replies concise

## Failure Handling

- If OCR fails, still save the PDF when possible
- If headline extraction fails, ask the user what title to use
- If OCR fails, explicitly report that OCR failed
- Preserve the original image unless the user later asks otherwise

## Current Limits

- Korean searchable PDF quality depends on OCR engine quality and PDF text-layer handling
- The Tesseract path is the current stable default
- The PaddleOCR path is experimental and should not be treated as the default engine
- This skill does not require external upload tools or cloud credentials

## Output Contract

Return only the practical result:
- saved filename
- save location
- extracted title line when available

## Resources

### scripts/
Bundled scripts are used for:
- image cleanup
- OCR execution
- searchable PDF generation
- saved scan retrieval

### references/
Store implementation notes for OCR engine choice and filename normalization if the skill grows more complex.
