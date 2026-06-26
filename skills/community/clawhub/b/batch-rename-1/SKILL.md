---
name: batch-rename
description: |
  This skill should be used when the user wants to batch rename multiple files at once.
  It handles various rename patterns including sequential numbering, find/replace, prefix/suffix
  addition, regular expression matching, extension filtering, and recursive subfolder processing.
  This skill is triggered when the user mentions "批量重命名", "batch rename", "批量改名",
  "批量修改文件名", or similar requests for renaming multiple files simultaneously.
---

# Batch Rename Skill

## Purpose

Provides powerful batch file renaming capabilities with multiple pattern support. Rename files with sequential numbers, find/replace text, add prefixes/suffixes, use regex patterns, filter by extension, and process subfolders recursively.

## When to Use

Use this skill when user wants to:
- Rename multiple files at once (批量重命名)
- Add sequential numbers to filenames
- Find and replace text in filenames
- Add date prefixes or other prefixes/suffixes
- Use regex patterns for complex renaming
- Filter files by extension before renaming
- Process files in subfolders recursively

## Usage Workflow

### Step 1: Identify User's Rename Intent

Ask the user (or infer from their request):
1. Target directory/folder path
2. Rename pattern type:
   - **Sequential numbering**: `photo_{n}.jpg` → `photo_001.jpg`
   - **Find & replace**: Replace specific text in filenames
   - **Add prefix/suffix**: Add date or other text
   - **Regex pattern**: For complex transformations
3. File extension filter (optional)
4. Whether to process subfolders recursively

### Step 2: Construct Rename Command

Use the `scripts/batch_rename.py` script with appropriate arguments:

```bash
# Sequential numbering
python scripts/batch_rename.py --path "C:/folder" --pattern "number" --format "file_{n:03d}" --ext "jpg"

# Find and replace
python scripts/batch_rename.py --path "C:/folder" --pattern "replace" --find "old" --replace "new"

# Add prefix
python scripts/batch_rename.py --path "C:/folder" --pattern "prefix" --prefix "2026-" --ext "*"

# Add suffix
python scripts/batch_rename.py --path "C:/folder" --pattern "suffix" --suffix "_backup" --ext "*.txt"

# Regex pattern
python scripts/batch_rename.py --path "C:/folder" --pattern "regex" --regex "(\d+)" --replace "ID_$1"

# Recursive with extension filter
python scripts/batch_rename.py --path "C:/folder" --pattern "number" --format "doc_{n}" --ext "pdf" --recursive
```

### Step 3: Execute Rename

Run the command. The script will:
1. Scan the target directory
2. Apply filters (extension, recursive)
3. Perform renaming operations
4. Report results

### Step 4: Report Results

Present a summary showing:
- Number of files renamed successfully
- Any errors or skipped files
- Original → New name mappings for verification

## Script Arguments Reference

| Argument | Description | Required |
|----------|-------------|----------|
| `--path` | Target directory path | Yes |
| `--pattern` | Rename pattern: `number`, `replace`, `prefix`, `suffix`, `regex` | Yes |
| `--format` | Format string for numbering (e.g., `file_{n:03d}`) | For `--pattern number` |
| `--find` | Text to find | For `--pattern replace` |
| `--replace` | Replacement text | For `--pattern replace` |
| `--prefix` | Prefix to add | For `--pattern prefix` |
| `--suffix` | Suffix to add | For `--pattern suffix` |
| `--regex` | Regular expression pattern | For `--pattern regex` |
| `--ext` | File extension filter (e.g., `jpg`, `*` for all) | No (default: all) |
| `--recursive` | Process subfolders recursively | No |

## Examples

### Example 1: Add Sequential Numbers
```
User: "把 photos 文件夹里的图片重命名为 IMG_001, IMG_002..."
Command: python scripts/batch_rename.py --path "C:/Users/12891/photos" --pattern number --format "IMG_{n:03d}" --ext "jpg"
```

### Example 2: Find and Replace
```
User: "把所有文件名里的 '_v1' 改成 '_final'"
Command: python scripts/batch_rename.py --path "C:/folder" --pattern replace --find "_v1" --replace "_final"
```

### Example 3: Add Date Prefix
```
User: "给所有文档加上日期前缀 2026-04-10"
Command: python scripts/batch_rename.py --path "C:/docs" --pattern prefix --prefix "2026-04-10_" --ext "docx"
```

### Example 4: Regex to Normalize
```
User: "把所有文件名的空格替换成下划线"
Command: python scripts/batch_rename.py --path "C:/folder" --pattern regex --regex "\s+" --replace "_"
```

## Safety Notes

- Always report what will be renamed before executing
- For subfolder operations, be extra careful and confirm the scope
- Use `--ext` filter to limit scope when possible
- Script uses `os.rename()` which may fail if file already exists at target name
