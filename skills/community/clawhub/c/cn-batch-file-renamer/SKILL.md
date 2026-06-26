---
slug: cn-batch-file-renamer
name: Batch File Renamer
version: "1.0.0"
description: "Batch rename files with customizable patterns. Support prefix, suffix, sequential numbering. Dry-run mode available. Pure Python, no API key required."
keywords: rename, batch, file, tool
license: MIT-0
tags:
  - tools
---

# Batch File Renamer

Rename multiple files at once with patterns.

## Features

- Add prefix to filenames
- Add suffix before extension
- Sequential numbering (001, 002, ...)
- Dry-run mode (preview without changes)
- Pure Python, no external dependencies

## Usage

```
# Preview renaming
python3 scripts/batch_rename.py --dir ./photos --prefix "vacation_" --dry-run

# Actually rename
python3 scripts/batch_rename.py --dir ./photos --prefix "vacation_"
```

## Examples

Rename files in a directory:
- photo.jpg → vacation_001.jpg
- image.png → vacation_002.png
- pic.gif → vacation_003.gif

## Notes

- Preserves file extensions
- Does not overwrite existing files
- Use --dry-run first to preview changes

## Exit Codes

- 0: Success
- 1: Directory not found or permission error

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
