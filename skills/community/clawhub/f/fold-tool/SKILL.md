---
name: fold-tool
description: Wrap long lines of text to a specified width. Use for formatting text files to fit within column limits.
---
# Fold - Line Wrapping Utility
Break long lines of text at a specified width, making them fit within terminal columns or document margins.
## Usage
```bash
fold-tool [options] [file...]
```
## Options
- `-w N`: Set line width to N characters (default: 80)
- `-s`: Break at spaces only (don't split words)
- `-b`: Count bytes instead of columns
## Examples
```bash
fold-tool -w 72 longlines.txt
fold-tool -w 100 -s paragraph.txt
```