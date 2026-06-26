---
name: archive-extractor
description: |
  Recursively extract archive files from a file or directory.
  Supports zip, tar, tar.gz, tar.bz2, tar.xz, tgz, rar, 7z, gz, bz2, xz.
  Works on Windows, Linux, macOS — requires only Python 3.8+, no local software.
  Use when the user wants to "unzip", "unpack", "extract", or "decompress" archives,
  especially for bulk extraction, nested archives, or when idempotent re-runs are needed.
---

# Archive Extractor

Extracts archives recursively using `scripts/extract.py`.

**Zero local-software dependency** — works on any machine with Python 3.8+.  
`.rar` and `.7z` formats use pure-Python libraries (`rarfile`, `py7zr`) that are
auto-installed on first use via pip. No 7-Zip, WinRAR, or unrar binary needed.

## How to run

```bash
python scripts/extract.py <PATH> [OPTIONS]
```

**Always use the absolute path to the script** when calling from a different working directory:

```bash
# Windows
python "C:\Users\<user>\.workbuddy\skills\archive-extractor\scripts\extract.py" "<PATH>"

# Linux / macOS
python ~/.workbuddy/skills/archive-extractor/scripts/extract.py "<PATH>"
```

### Options

| Flag | Description |
|------|-------------|
| `-f` / `--force` | Re-extract even if a `.extracted_success` marker already exists |
| `-d DIR` / `--dest DIR` | Write all output under a custom root directory |

## Supported formats

| Format | Backend |
|--------|---------|
| `.zip` | Python stdlib `zipfile` |
| `.tar` `.tar.gz` `.tar.bz2` `.tar.xz` `.tgz` `.tbz2` | Python stdlib `tarfile` |
| `.gz` `.bz2` `.xz` (single-file) | Python stdlib `gzip` / `bz2` / `lzma` |
| `.rar` | `rarfile` (pure-Python, auto-installed) |
| `.7z` | `py7zr` (pure-Python, auto-installed) |

## Key behaviours

- **Idempotent**: skips archives that already have a `.extracted_success` marker; use `-f` to override.
- **Recursive**: after extracting an archive, immediately scans the output for nested archives (up to 20 levels deep).
- **Auto-deps**: `rarfile` and `py7zr` are installed automatically via pip on first use — no manual setup needed.
- **Fault-tolerant**: corrupted or unsupported archives are logged as `[FAIL]` and skipped; remaining archives continue.

## Examples

```bash
# Extract everything in a directory (including sub-archives)
python extract.py "D:\jira\TICKET-123"

# Force clean re-extraction of a single file
python extract.py report.zip -f

# Extract to a separate output folder
python extract.py "D:\jira\TICKET-123" -d "D:\extracted"

# Glob pattern — extract all zips in current directory
python extract.py "*.zip"
```
