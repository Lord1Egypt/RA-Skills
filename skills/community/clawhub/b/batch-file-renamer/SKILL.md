---
name: batch-file-renamer
description: Batch rename files with powerful patterns, regex support, and preview functionality. Use when organizing large numbers of files, standardizing naming conventions, adding timestamps, sequential numbering, or cleaning up messy filenames. Ideal for photo management, media libraries, log files, and project cleanup tasks.
---

# Batch File Renamer

Powerful batch file renaming with patterns, regex, and preview.

## When to Use

- Renaming hundreds of photos from `IMG_001.jpg` to `Vacation_2025_001.jpg`
- Adding timestamps to log files
- Cleaning up messy download folders
- Standardizing naming conventions across projects
- Sequential numbering for ordered content
- Removing special characters from filenames

## Quick Start

### Basic Rename

```python
import os
import re
from datetime import datetime

def batch_rename(directory, pattern, replacement):
    """
    Rename files matching pattern
    
    Args:
        directory: Path to files
        pattern: Regex pattern to match
        replacement: Replacement string
    """
    renamed = []
    for filename in os.listdir(directory):
        new_name = re.sub(pattern, replacement, filename)
        if new_name != filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            renamed.append((filename, new_name))
    return renamed

# Example: Add prefix
batch_rename('./photos', r'^(.*)$', r'Vacation_2025_\1')
```

### Sequential Numbering

```python
def number_files(directory, prefix='', digits=3, extension=None):
    """Add sequential numbers to files"""
    files = sorted([f for f in os.listdir(directory) 
                   if extension is None or f.endswith(extension)])
    
    renamed = []
    for i, filename in enumerate(files, 1):
        old_path = os.path.join(directory, filename)
        ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}{str(i).zfill(digits)}{ext}"
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        renamed.append((filename, new_name))
    
    return renamed

# Usage
number_files('./downloads', prefix='Project_', digits=3)
# Result: Project_001.pdf, Project_002.jpg, ...
```

### Add Timestamps

```python
def add_timestamp(directory, date_format='%Y%m%d'):
    """Add date prefix to files"""
    timestamp = datetime.now().strftime(date_format)
    
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        name, ext = os.path.splitext(filename)
        new_name = f"{timestamp}_{name}{ext}"
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)

# Usage
add_timestamp('./logs')
# Result: 20250303_error.log, 20250303_debug.log
```

### Preview Mode (Safe)

```python
def preview_rename(directory, pattern, replacement):
    """Preview changes without renaming"""
    changes = []
    for filename in os.listdir(directory):
        new_name = re.sub(pattern, replacement, filename)
        if new_name != filename:
            changes.append(f"{filename} -> {new_name}")
    return changes

# Preview first
preview = preview_rename('./files', r'IMG_(\d+)', r'Photo_\1')
for change in preview:
    print(change)
```

## Common Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `r'^IMG_(\d+)'` | Match IMG_ prefix | `IMG_001.jpg` |
| `r'\s+'` | Replace spaces | `My File.txt` → `My_File.txt` |
| `r'[^\w\.]'` | Remove special chars | `file@#$%.txt` → `file.txt` |
| `r'\.jpeg$'` | Change extension | `.jpeg` → `.jpg` |

## Best Practices

1. **Always preview first** - Use `preview_rename()` before actual rename
2. **Backup important files** - Renaming is irreversible
3. **Test on single file** - Verify pattern works as expected
4. **Use regex groups** - Capture parts of filename with `(\d+)` etc.

## Safety Features

```python
def safe_rename(directory, pattern, replacement, dry_run=True):
    """Safe rename with dry-run option"""
    changes = []
    
    for filename in os.listdir(directory):
        new_name = re.sub(pattern, replacement, filename)
        if new_name != filename:
            changes.append((filename, new_name))
    
    if dry_run:
        print("DRY RUN - Changes that would be made:")
        for old, new in changes:
            print(f"  {old} -> {new}")
        return changes
    else:
        for old, new in changes:
            os.rename(
                os.path.join(directory, old),
                os.path.join(directory, new)
            )
        return changes
```
