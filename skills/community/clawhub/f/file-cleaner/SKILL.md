---
name: file-cleaner
description: A specialized skill for safely cleaning up temporary files and directories. Use this when you need to remove temp files, clear caches, or delete logs to free up space or maintain hygiene. Restricted to 'temp/', 'logs/', and 'cache/' directories for safety.
---

# File Cleaner

Safely removes files and directories. Built with strict safety checks to prevent accidental deletion of critical workspace files.

## Usage

```bash
node skills/file-cleaner/index.js <path>
```

## Examples

Clean a specific temp directory:
```bash
node skills/file-cleaner/index.js temp/my-experiment
```

Clean a log file:
```bash
node skills/file-cleaner/index.js logs/debug.log
```

## Safety

- ONLY deletes paths starting with `temp/`, `logs/`, or `cache/`.
- Will block attempts to delete workspace root, `skills/`, or other protected paths.
