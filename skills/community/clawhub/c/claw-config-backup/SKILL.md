---
name: clawbackup
description: Backup OpenClaw configuration file with hash-based change detection. Use when user asks to backup, create backup of, or save OpenClaw config (openclaw.json). Automatically skips backup if file hasn't changed.
---

# Clawbackup

Backup OpenClaw configuration file with automatic change detection.

## Quick Start

### Backup Config

From workspace directory:
```bash
python config_backup.py ..\openclaw.json
```

Or with custom backup directory:
```bash
python config_backup.py ..\openclaw.json -o backup
```

## Features

- **JSON5 Validation**: Validates config file before backup
- **Hash-based Change Detection**: Skips backup if file hasn't changed (compares SHA256 hash)
- **Timestamped Backups**: Creates backups with timestamp format: `openclaw_20260319_143052_123456.json`
- **Custom Output Directory**: Specify backup location with `-o` flag

## Script Location

The script is located in "scripts" directory

## Usage

```
usage: config_backup.py [-h] [-o OUTPUT] file

Validate JSON5 and backup with hash check

positional arguments:
  file                  JSON5 file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output   Backup directory (default: backup)
```

## Example Output

```
✅ JSON5 validate passed
📦 已备份: backup\openclaw_20260319_143052_123456.json
```

If file unchanged:
```
✅ JSON5 validate passed
⚠️ config file unchange, skip backup
```
