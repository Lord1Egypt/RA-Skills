---
name: file-splitter
description: >
  Split large files into smaller chunks with semantic boundary detection.
  Supports JSON, Markdown, and TXT formats. Preserves data integrity by splitting
  at natural boundaries (JSON array elements, MD headings, TXT paragraphs).
  Use when: user needs to split large files, chunk datasets, segment corpora,
  or break down files into manageable pieces for processing or analysis.
  Triggers: split file, chunk, segment, file splitter, JSON split, MD split,
  TXT split, corpus segmentation, data chunking.
---

# File Splitter - Universal File Splitting Tool

Split large files into smaller, manageable chunks while preserving semantic structure.

## Quick Start

```bash
python <skill_dir>/scripts/split_files.py --input <input_folder> --output <output_folder> [options]
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--input` | Yes | - | Source folder containing files to split |
| `--output` | Yes | - | Output folder for split chunks |
| `--max-size` | No | 512000 (500KB) | Maximum bytes per chunk |
| `--min-size` | No | 409600 (400KB) | Minimum bytes per chunk |
| `--seq-digits` | No | 9 | Number of digits in sequence numbers |
| `--formats` | No | json,md,txt | File formats to process (comma-separated) |
| `--dry-run` | No | false | Preview mode - show what would be split without executing |

### Examples

```bash
# Default 500KB split
python split_files.py --input "./corpus" --output "./corpus/chunks"

# Custom 200KB chunks
python split_files.py --input "./notes" --output "./notes/chunks" --max-size 204800 --min-size 153600

# JSON files only
python split_files.py --input "./data" --output "./data/out" --formats json

# Preview mode
python split_files.py --input "./data" --output "./data/out" --dry-run
```

## Splitting Rules

### JSON Files
- Splits at JSON array element boundaries
- Each chunk is a valid JSON array `[...]`
- Automatically extracts list values if top-level is an object
- Never cuts individual records in half

### Markdown Files
- Splits at heading boundaries (`#` through `######`)
- Each chunk maintains complete heading structure
- Never cuts content within a heading section

### TXT Files
- Prefers splitting at paragraph boundaries (empty lines)
- Falls back to line-by-line splitting if no paragraphs exist
- Never cuts within a paragraph

## Output Naming Convention

Format: `{source_filename_without_extension}{9-digit_sequence_number}{extension}`

Examples:
- `dataset000000001.json`
- `dataset000000002.json`
- `notes000000001.md`

## Safety Features

1. **Source File Preservation**: Read-only access to source files; never deletes or modifies originals
2. **Duplicate Detection**: Automatically skips files that already have N-digit sequence suffixes to avoid re-splitting
3. **Small File Skip**: Files ≤ max-size are automatically skipped (no need to split)
4. **Sequential Processing**: Processes files one at a time to ensure stability
5. **Data Validation**: Compares total size/record count before and after splitting; reports verification results
6. **UTF-8 Encoding**: Forces UTF-8 for all read/write operations to avoid encoding issues on Windows

## Notes

- Console may display garbled Chinese characters on Windows, but functionality is unaffected
- If a single data block/paragraph exceeds max-size, it becomes its own chunk (integrity takes priority over size limits)
- Output folder is automatically created if it doesn't exist
- License: MIT-0
