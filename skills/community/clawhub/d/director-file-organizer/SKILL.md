---
name: file-organizer
description: Automatically organize, categorize, and clean up files. Use when user wants to (1) organize downloads or folders, (2) sort files by type/date/size, (3) find and remove duplicates, (4) bulk rename files, (5) clean up old/temp files, or (6) create folder structures for projects.
---

# File Organizer

Automatically organize and manage file collections.

## Core Functions

### 1. Sort by Type
Group files by extension:
```
/documents/    → .pdf, .doc, .docx, .txt
/images/       → .jpg, .png, .gif, .svg
/videos/       → .mp4, .mov, .avi
/archives/     → .zip, .rar, .7z
/audio/        → .mp3, .wav, .flac
/code/         → .js, .py, .html, .css
```

### 2. Sort by Date
Organize by modification time:
```
/2026/04/07/
/2026/04/06/
/2026/03/
```

### 3. Find Duplicates
```python
import hashlib

def find_duplicates(path):
    hashes = {}
    for file in Path(path).rglob('*'):
        if file.is_file():
            h = hashlib.md5(file.read_bytes()).hexdigest()
            hashes.setdefault(h, []).append(file)
    return {h: f for h, f in hashes.items() if len(f) > 1}
```

### 4. Bulk Rename
Patterns:
- `prefix_001.jpg`, `prefix_002.jpg`
- `2026-04-07_description.jpg`
- `file_v1.txt`, `file_v2.txt`

### 5. Cleanup Old Files
```python
from datetime import datetime, timedelta

def cleanup_old(path, days=90):
    threshold = datetime.now() - timedelta(days=days)
    for file in Path(path).rglob('*'):
        if file.is_file() and datetime.fromtimestamp(file.stat().st_mtime) < threshold:
            file.unlink()  # or move to trash
```

## Workflow

1. **Scan** - List all files in directory
2. **Analyze** - Get metadata (type, date, size, hash)
3. **Plan** - Show proposed organization
4. **Execute** - Move/copy/rename files
5. **Report** - Summary of changes

## Safety Rules

- **Always confirm** before deleting or moving
- **Use trash** instead of permanent delete when possible
- **Backup** important files first
- **Log** all changes for undo capability
- **Handle conflicts** - ask about name collisions
