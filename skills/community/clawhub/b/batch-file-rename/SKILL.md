---
name: batch-file-rename
description: Batch file renaming utility with pattern matching, regex, sequence numbering, and dry-run preview. Supports prefix/suffix, case conversion, whitespace cleanup, and recursive directory processing.
metadata: {"openclaw":{"emoji":"📝"}}
---

# Batch File Rename

Rename multiple files using flexible patterns with safe dry-run preview.

## When to Use

- Bulk rename files in a directory (photos, downloads, exports)
- Normalize file names (trim whitespace, lowercase, replace separators)
- Add sequence numbers (e.g., `001-file.txt`, `002-file.txt`)
- Replace patterns with regex across many files
- Process directories recursively

## Prerequisites

- No external dependencies — uses only shell builtins and `sed`/`awk`

## Basic Steps

### 1. Dry-run preview (always do this first)

```bash
# Preview rename with prefix + sequence number
for f in *.txt; do
  [ -f "$f" ] || continue
  echo "Would rename: $f → photo-001-$f"
done
```

### 2. Prefix + sequence number

```bash
i=1
for f in *.jpg *.png; do
  [ -f "$f" ] || continue
  printf -v new "vacation-%03d-%s" "$i" "$f"
  echo "Renaming: $f → $new"
  mv -- "$f" "$new"
  ((i++))
done
```

### 3. Regex pattern replace

```bash
# Replace spaces with underscores, lowercase everything
for f in *; do
  [ -f "$f" ] || continue
  new=$(echo "$f" | tr '[:upper:] ' '[:lower:]_' | sed 's/[^a-z0-9._-]/_/g' | sed 's/_\+/_/g')
  [ "$f" != "$new" ] && mv -- "$f" "$new" && echo "$f → $new"
done
```

### 4. Strip prefix from all files

```bash
for f in report-*.pdf; do
  [ -f "$f" ] || continue
  new="${f#report-}"
  mv -- "$f" "$new" && echo "$f → $new"
done
```

### 5. Recursive rename in subdirectories

```bash
find . -type f -name "*.tmp" | while read -r f; do
  dir=$(dirname "$f")
  base=$(basename "$f" .tmp)
  new="$dir/$base.txt"
  mv -- "$f" "$new" && echo "$f → $new"
done
```

## Key Safety Rules

1. **Always dry-run first** — replace `mv` with `echo "Would rename:"` and verify output
2. **Quote variables** — `"$f"` not `$f` (handles spaces and special chars)
3. **Use `--` in mv** — `mv -- "$f" "$new"` prevents option injection
4. **Backup first** — `tar czf backup.tar.gz *.txt` before bulk operations
5. **Check collisions** — if two files map to the same name, the rename will fail or overwrite

## Example: Normalize Downloads Folder

```bash
cd ~/Downloads
# Dry run
for f in *; do
  [ -f "$f" ] || continue
  new=$(echo "$f" | tr '[:upper:] ' '[:lower:]_' | sed 's/[^a-z0-9._-]/_/g')
  echo "$f → $new"
done
# After verifying, apply:
for f in *; do
  [ -f "$f" ] || continue
  new=$(echo "$f" | tr '[:upper:] ' '[:lower:]_' | sed 's/[^a-z0-9._-]/_/g')
  [ "$f" != "$new" ] && mv -- "$f" "$new"
done
```

## Example: Sequential Numbering for Photos

```bash
i=1
for f in IMG_*.JPG; do
  [ -f "$f" ] || continue
  printf -v new "trip-2026-%03d.JPG" "$i"
  mv -- "$f" "$new"
  ((i++))
done
```
