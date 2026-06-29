---
name: codia-document-deck
description: Use when the user asks to convert PDFs, screenshots, reports, documents, or existing marketing files into editable design data, PPTX slides, or both.
---

# codia-document-deck

Convert documents into editable design artifacts and presentation decks by coordinating Codia PDF-to-design, PDF-to-PPT, image-to-design, and optional image description workflows.

## When To Use

Use this skill for:

- PDF to editable design data
- PDF to PPT or PowerPoint deck conversion
- Requests that need both editable JSON and PPTX output
- Screenshot, poster, or scanned-page conversion into editable design data
- Document review where the user wants output files, not just a summary

For a direct PDF-to-PPT task only, use `codia-pdf-to-ppt`. For a direct screenshot-to-design task only, use `codia-image-to-design`.

## Inputs To Collect

- Source PDF, screenshot, poster, or image path/URL
- Page range for PDFs
- Whether the user wants editable design data, PPTX, or both
- Deck title, if a PPTX is requested
- Output directory

## Workflow

1. Use `codia-design` setup/auth guidance if the CLI is missing or not authenticated.
2. For PDFs, confirm page selection. Codia PDF APIs use zero-based page numbers: page `0` is the first page.
3. Run `codia-pdf-to-design` first when editable page structure, JSON output, or visual reconstruction is requested.
4. Run `codia-pdf-to-ppt --poll` when a PPTX deck is requested. Let the CLI download and validate the returned PPTX unless the user explicitly asks for JSON-only behavior.
5. Use `codia-image-to-design` for screenshots, poster images, exported pages, or scanned pages that are not available as PDF pages.
6. Use `codia-image-describe` only when the user also needs a plain-language visual summary, comparison, or extraction of design intent.
7. Do not rasterize the PDF locally or generate a substitute PPTX unless the user explicitly asks for a local fallback.

## Output

Return:

- Editable design JSON path or paths
- PPTX path when produced
- Downloaded local files
- Page range used
- Failed page, task ID, API error, or validation error when any step fails

If PPTX download or validation fails, report the API or validation error directly and treat the PPTX step as failed.
