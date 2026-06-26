---
name: fmt-tool
description: Simple text formatting and reflow tool. Use for reformatting paragraphs, removing extra whitespace, and cleaning up text files.
---
# Fmt - Text Reformatting Utility
Reformat paragraphs of text to a specified width, removing extra whitespace and producing clean, consistently formatted output.
## Usage
```bash
fmt-tool [options] [file...]
```
## Options
- `-w N`: Set output width (default: 75)
- `-u`: Uniform spacing (one space between words)
- `-s`: Split long lines only (don't join short ones)
## Examples
```bash
fmt-tool -w 80 messy.txt
fmt-tool -u notes.txt
```