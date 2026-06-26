---
name: doc-converter
description: Converts document files (.pdf, .docx, .xlsx, .pptx) to Markdown using the `markitdown` command.
---

# Document Converter

This skill converts a document file into Markdown text.

## Activation

Activate when asked to read a file with one of the following extensions:
- .pdf
- .docx
- .xlsx
- .pptx

## Execution

The skill executes the `markitdown` command on the input file path and outputs the resulting Markdown text.

```bash
markitdown "{file_path}"
```
