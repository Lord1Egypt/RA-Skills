---
name: archive-tool
description: Extract and create archive files (zip, rar, 7z, tar, gz). Use when: (1) Extracting zip/rar/7z files, (2) Creating zip archives, (3) Viewing archive contents, (4) Batch extracting files.
version: 1.1.0
changelog: "v1.1.0: Added reasoning framework, decision tree, troubleshooting, self-checks"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📦"
    category: "utility"
    homepage: https://github.com/KeXu9/archive-skill
---

# Archive Tool

Extract and create archive files (zip, rar, 7z, tar, gz).

## When This Skill Activates

This skill triggers when user wants to extract, create, or list archive files.

## Reasoning Framework

| Step | Action | Why |
|------|--------|-----|
| 1 | **DETECT** | Identify archive format (zip/tar/gz/rar/7z) |
| 2 | **CHECK** | Verify tools available for format |
| 3 | **EXECUTE** | Extract, create, or list |
| 4 | **VERIFY** | Confirm success, report errors |

---

## Install

```bash
# Optional (for rar/7z support)
brew install unar p7zip
```

---

## Decision Tree

### What are you trying to do?

```
├── Extract archive
│   └── Use: archive.py extract file.zip -o ./output
│
├── Create archive
│   └── Use: archive.py create output.zip ./folder
│
├── View contents
│   └── Use: archive.py list file.zip
│
└── Batch extract
    └── Use: archive.py extract "*.zip"
```

---

## Features

| Feature | Description |
|---------|-------------|
| Extract | zip, tar, tar.gz, tgz, gz, rar, 7z |
| Create | zip, tar, tar.gz |
| List | View archive contents |
| Batch | Extract multiple files |

---

## Extract

### Command

```bash
python archive.py extract <file> [-o OUTPUT] [--password PASS]
```

### Examples

```bash
# Extract to current folder
python archive.py extract archive.zip

# Extract to specific folder
python archive.py extract archive.zip -o ./extracted

# Extract with password
python archive.py extract archive.rar --password secret

# Extract to current directory
python archive.py extract archive.7z -o ./

# Batch extract all zip files
python archive.py extract "*.zip"
```

---

## Create

### Command

```bash
python archive.py create <output> <source> [--compression LEVEL]
```

### Examples

```bash
# Create zip from folder
python archive.py create myfiles.zip ./myfolder

# Create tar from folder
python archive.py create backup.tar ./folder

# Create tar.gz
python archive.py create backup.tar.gz ./folder
```

---

## List

### Command

```bash
python archive.py list <file>
```

### Examples

```bash
# List contents
python archive.py list archive.zip

# View without extracting
python archive.py list backup.tar.gz
```

---

## Supported Formats

| Format | Extract | Create | Notes |
|--------|---------|--------|-------|
| zip | ✅ | ✅ | Python stdlib |
| tar | ✅ | ✅ | Python stdlib |
| tar.gz / tgz | ✅ | ✅ | Python stdlib |
| gz | ✅ | ❌ | Python stdlib |
| rar | ⚠️ | ❌ | Requires `unar` |
| 7z | ⚠️ | ❌ | Requires `p7zip` |

⚠️ = requires system tools

---

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output directory | current dir |
| `--password` | Archive password | none |
| `--compression` | 0-9 (zip only) | 6 |

---

## Troubleshooting

### Problem: "No module named 'zipfile'"

- **Cause:** Using Python 2
- **Fix:** Use `python3` instead of `python`

### Problem: "Unsupported archive format"

- **Cause:** Unknown format or corrupted file
- **Fix:** Verify file extension is correct

### Problem: "Password required"

- **Cause:** Encrypted archive
- **Fix:** Use `--password` flag

### Problem: "rar/7z extraction failed"

- **Cause:** Tools not installed
- **Fix:** `brew install unar p7zip`

### Problem: "Permission denied"

- **Cause:** No write permission in output folder
- **Fix:** Check folder permissions or use different output path

---

## Self-Check

- [ ] Using correct Python (python3)
- [ ] Archive file exists and is readable
- [ ] For rar/7z: required tools installed
- [ ] Output directory exists and is writable
- [ ] Password correct (if encrypted)

---

## Quick Reference

| Task | Command |
|------|---------|
| Extract zip | `python archive.py extract file.zip` |
| Extract to folder | `python archive.py extract file.zip -o ./out` |
| Extract rar | `python archive.py extract file.rar` |
| Create zip | `python archive.py create out.zip ./folder` |
| Create tar.gz | `python archive.py create out.tar.gz ./folder` |
| List contents | `python archive.py list file.zip` |

---
