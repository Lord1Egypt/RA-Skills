---
name: calibre-convert
description: Use this skill when the user wants to convert ebook or document files between formats with Calibre, including EPUB to PDF, Markdown to EPUB, MOBI to EPUB, AZW3 to EPUB, HTML to EPUB, DOCX to EPUB, and similar source/target format pairs supported by ebook-convert.
---

# Calibre Convert

## Overview

`calibre-convert` uses Calibre's `ebook-convert` CLI to perform ebook and document format conversion. Use it when the user wants a direct file-to-file conversion and the desired input/output formats are supported by Calibre.

## Quick Start

1. Confirm the source file exists and decide the exact output path.
2. Check whether `ebook-convert` is available in `PATH`.
3. Run the helper script:

```bash
./scripts/convert_with_calibre.py /path/to/input.epub /path/to/output.pdf
```

4. If the user wants format-specific tuning, pass Calibre arguments after `--`:

```bash
./scripts/convert_with_calibre.py /path/to/book.md /path/to/book.epub -- --chapter "//h:h1" --authors "Example Author"
```

## Workflow

### 1. Validate inputs

- Ensure the input file exists.
- Ensure the output directory exists or create it if the task allows edits there.
- Infer the requested conversion from the output extension when the user says things like "convert EPUB to PDF".

### 2. Check Calibre availability

Use the bundled script first. It looks for `ebook-convert` in `PATH`, then common macOS install locations.

If Calibre is missing, stop and tell the user exactly which command is missing. Do not pretend the conversion succeeded.

### 3. Run conversion

The core command is:

```bash
ebook-convert input_file output_file [options...]
```

Common examples:

- EPUB -> PDF
- Markdown -> EPUB
- MOBI -> EPUB
- AZW3 -> EPUB
- HTML -> EPUB
- DOCX -> EPUB

When the user does not specify extra options, prefer the simplest possible conversion.

### 4. Verify result

- Confirm the output file was created.
- Report the final path back to the user.
- If Calibre emits warnings, summarize only the meaningful parts.

## Notes

- Calibre support varies by format pair and by installed version.
- PDF output quality depends heavily on source structure and metadata.
- Markdown input is handled by Calibre's parsers; if the output looks poor, try converting via HTML or adding explicit options.
- For large batches, loop over files and keep source/target extensions explicit instead of guessing.

## Resources

### scripts/

- `scripts/convert_with_calibre.py`: validates paths, finds `ebook-convert`, and forwards extra options safely.

### references/

- `references/examples.md`: ready-to-copy conversion examples and troubleshooting notes.
