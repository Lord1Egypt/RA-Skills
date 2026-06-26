---
name: file-management
description: Safe filesystem operations using built-in Unix tools and macOS utilities. Use when listing, searching, reading, organizing, or managing files and directories. Always confirm destructive operations before executing. Triggers on: "list files", "search for files", "find files", "organize files", "batch rename", "move files", "copy files", "delete files", "disk usage", "file search".
---

# File Management

Safe filesystem operations using only pre-installed system tools. No external dependencies, no network access, no install.

## Core Principle

**Safety first — always confirm destructive operations before executing.**

- `mv`, `cp`, `rm` are irreversible without a backup
- Prefer `ls -la` before touching anything
- For deletions, prefer `trash` (macOS) or `rm` as last resort

## Built-in Tools Only

### Guaranteed on all Unix/macOS

| Tool | Purpose | Notes |
|------|---------|-------|
| `ls` | List files | All Unix ✅ |
| `find` | Search files | All Unix ✅ |
| `grep` | Search file contents | All Unix ✅ |
| `cat` / `head` / `tail` | Read files | All Unix ✅ |
| `mv` | Move / rename | Write ⚠️ |
| `cp` | Copy files | Write ⚠️ |
| `mkdir` | Create directories | Write ⚠️ |
| `rm` | Delete files | Write ⚠️ last resort |
| `stat` | File metadata | All Unix ✅ |
| `du` | Disk usage | All Unix ✅ |
| `tar` | Archive files | All Unix ✅ |
| `xattr` | Extended attributes | macOS ✅ |

### macOS-specific (pre-installed)

| Tool | Purpose | Notes |
|------|---------|-------|
| `trash` | Move to Trash (recoverable) | macOS ✅ preferred |
| `pbcopy` / `pbpaste` | Clipboard | macOS ✅ |
| `mdls` | Spotlight metadata | macOS ✅ |
| `mdutil` | Spotlight index | macOS ✅ |

### Optional tools (may not be installed)

These are helpful but NOT guaranteed. Check with `which <tool>` before using:

- `tree` — directory tree view (install: `brew install tree`)
- `rg` (ripgrep) — faster grep (install: `brew install ripgrep`)
- `fd` — faster find (install: `brew install fd`)
- `dust` — better du (install: `brew install dust`)
- `bat` — better cat (install: `brew install bat`)

## Common Patterns

### List Directory Contents

```bash
# Basic listing
ls -la /path/to/dir

# Human-readable sizes, newest first
ls -lahF /path/to/dir | sort -k5 -rh

# Recursive depth
find /path -maxdepth 2 -type f

# Show hidden files
ls -la /path/to/dir
```

### Search for Files by Name

```bash
# Find by name pattern
find /path -name "*.txt" -type f

# Case-insensitive
find /path -iname "readme*"

# Modified in last N days
find /path -name "*.md" -mtime -7

# By size
find /path -size +100M
```

### Search File Contents

```bash
# Grep with context
grep -rn "search_term" /path

# Case-insensitive
grep -ri "search_term" /path

# Only filenames with matches
grep -rl "search_term" /path
```

### Disk Usage Analysis

```bash
# Total size of directory
du -sh /path/to/dir

# Per-subdirectory breakdown
du -h --max-depth=1 /path | sort -rh

# Find largest files (recursive)
find /path -type f -exec du -h {} + | sort -rh | head -20
```

### Move / Copy / Delete

```bash
# Move (rename)
mv source.txt /new/path/

# Copy (recursive for directories)
cp -r /source/dir /dest/dir

# Delete — ALWAYS confirm first
# Preferred on macOS (goes to Trash):
trash /path/to/file.txt
# Or rm as last resort:
rm /path/to/file.txt
```

### Batch Rename (pure bash)

```bash
# Rename all .txt to .md in current directory
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# Replace spaces with underscores
for f in *\ *; do mv "$f" "${f// /_}"; done
```

### Archive & Compress

```bash
# Create tar.gz
tar -czvf archive.tar.gz /path

# Extract
tar -xzvf archive.tar.gz

# Create zip
zip -r archive.zip /path

# Extract zip
unzip archive.zip
```

## Permission Model

**Read-only operations** — safe to execute without asking:
`ls`, `find`, `grep`, `cat`, `head`, `tail`, `du`, `stat`, `file`, `mdls`

**Write operations** — always confirm before executing:
`mv`, `cp`, `mkdir`, `trash`, `rm`, `zip`, `tar`

**For destructive operations:**
1. Show what will be affected first
2. Ask for confirmation with exact command
3. Prefer `trash` over `rm` on macOS

## Anti-Patterns (Never Do)

- ❌ `rm -rf /` or any recursive delete without confirming
- ❌ `chmod -R 777` or permission changes that break security
- ❌ Executing downloaded scripts directly without review
- ❌ Accessing paths outside user's home without asking
- ❌ `sudo` operations unless explicitly requested

## Quick Reference

```bash
# Where am I?
pwd

# What's in current directory?
ls -la

# Find all PDFs larger than 10MB
find ~ -name "*.pdf" -size +10M

# How much space is used?
du -sh ~/Library

# Search for TODO in code files
grep -rn --include="*.py" "TODO" ~/code/
```
