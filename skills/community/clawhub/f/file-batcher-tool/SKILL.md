---
name: file-batcher
description: Batch file operations (rename, convert, organize). Use when user says "rename files", "batch rename", "convert files", "organize files", or wants to process multiple files.
---

# File Batcher

Batch file operations for efficient file management.

## Commands

### Batch Rename
When user says: "rename files in folder X", "batch rename with pattern Y"
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh rename "<folder>" "<pattern>"
```

Patterns:
- `prefix_*` - Add prefix
- `*_suffix` - Add suffix
- `img_###` - Sequential numbering
- `lowercase` - Convert to lowercase
- `uppercase` - Convert to uppercase

### Convert Images
When user says: "convert images to png", "convert folder to jpg"
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh convert "<folder>" "<format>"
```

Supported: jpg, png, webp, gif

### Organize by Type
When user says: "organize files by type", "sort files into folders"
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh organize "<folder>"
```

Creates folders: images/, documents/, videos/, audio/, archives/

### Find Duplicates
When user says: "find duplicate files"
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh duplicates "<folder>"
```

### Count Files
When user says: "count files in folder"
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh count "<folder>"
```

### List Large Files
When user says: "find large files", "show big files"
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh large "<folder>" [--size 100M]
```

## Examples

```bash
# Rename all photos with date prefix
bash skills/file-batcher-1.0.0/scripts/batcher.sh rename "./photos" "2026-03-10_###"

# Convert all images to PNG
bash skills/file-batcher-1.0.0/scripts/batcher.sh convert "./images" "png"

# Organize messy download folder
bash skills/file-batcher-1.0.0/scripts/batcher.sh organize "~/Downloads"

# Find files larger than 500MB
bash skills/file-batcher-1.0.0/scripts/batcher.sh large "~/Documents" --size 500M
```

## Response Format

When renaming:
```
📁 Batch Rename Complete
   Folder: ./photos
   Renamed: 15 files
   Pattern: 2026-03-10_###
```

When organizing:
```
📁 Organization Complete
   images/: 23 files
   documents/: 8 files
   videos/: 3 files
```
