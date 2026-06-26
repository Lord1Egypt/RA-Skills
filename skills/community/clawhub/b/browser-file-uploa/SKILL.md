---
name: browser-file-upload
description: Browser automation skill for uploading files to web pages with flexible path specification. Use when Codex needs to: (1) Upload files to web forms, (2) Automate file selection dialogs, (3) Interact with file input elements via agent-browser CLI. Supports absolute paths, relative paths, environment variables, and workspace-relative paths.
---

# Browser File Upload

Automates file uploads to web pages using agent-browser CLI.

## Quick Start

Upload a file to a web page:

```bash
# Basic upload (auto-detects file input)
agent-browser open <url>
agent-browser find text 选择文件 click
agent-browser upload "#filePicker" <file-path>

# Or use the Python script
python scripts/upload_file.py <url> <file-path>
```

## Usage Patterns

### Upload to Specific Selector

When you know the file input selector:

```bash
agent-browser open https://example.com/upload
agent-browser click "#fileInput"
agent-browser upload "#fileInput" C:\path\to\file.xlsx
```

### Upload by Text Search

When file input has visible label text:

```bash
agent-browser open https://example.com/upload
agent-browser find text "上传文件" click
agent-browser upload "[type=file]" C:\path\to\file.xlsx
```

### Using Python Script

For reusable upload logic with flexible path specification:

```bash
python scripts/upload_file.py <url> <file-path> [selector] [wait_ms]
```

Arguments:
- `url` - Target page URL
- `file-path` - Path to file (supports multiple formats, see below)
- `selector` - Optional CSS selector for file input
- `wait_ms` - Optional wait time after page load (default: 2000)

## File Path Formats

The Python script supports multiple path formats:

| Format | Example | Description |
|--------|---------|-------------|
| Absolute | `C:\Users\name\file.xlsx` | Full path |
| Relative | `./data/file.xlsx` | Relative to current directory |
| Workspace | `workspace/file.xlsx` | Relative to OPENCLAW_WORKSPACE |
| Env Var | `${HOME}/file.xlsx` | Environment variable |
| Windows Env | `%USERPROFILE%\file.xlsx` | Windows environment variable |

### Path Examples

```bash
# Absolute path
python scripts/upload_file.py https://example.com C:\Users\陈\Documents\data.xlsx

# Relative path (from workspace)
python scripts/upload_file.py https://example.com ./test.xlsx

# Workspace-relative
python scripts/upload_file.py https://example.com workspace/data/test.xlsx

# With environment variable
python scripts/upload_file.py https://example.com ${HOME}/downloads/file.xlsx
```

## Common Selectors

| Selector | Description |
|----------|-------------|
| `#filePicker` | Common id for file inputs |
| `[type=file]` | Any file input element |
| `input[type=file]` | Explicit file input |
| `.upload-zone` | Drop zone containers |

## Troubleshooting

**File input not found:**
- Run `agent-browser snapshot` to inspect page elements
- Look for `[type=file]` or file-related buttons
- Try clicking the upload zone first

**Upload fails:**
- Ensure file path is absolute
- Check file exists: `test-path <file-path>`
- Try `agent-browser find text 选择文件 click` first

**Page not loaded:**
- Add `agent-browser wait 2000` after open
- Use `agent-browser wait --load networkidle` for slow pages

## Related Commands

```bash
# Inspect page elements
agent-browser snapshot

# Take screenshot
agent-browser screenshot

# Find elements by text
agent-browser find text "上传"

# Click element
agent-browser click <selector>

# Upload file
agent-browser upload <selector> <file-path>
```

## Example: Upload Excel to UU Tool

```bash
# Method 1: Direct agent-browser commands
agent-browser open https://uutool.cn/excel/
agent-browser wait 2000
agent-browser find text 选择文件 click
agent-browser upload "#filePicker" C:\Users\陈\.openclaw\workspace\test.xlsx

# Method 2: Using Python script with absolute path
python scripts/upload_file.py https://uutool.cn/excel/ C:\Users\陈\.openclaw\workspace\test.xlsx

# Method 3: Using Python script with workspace-relative path
python scripts/upload_file.py https://uutool.cn/excel/ workspace/test.xlsx

# Method 4: Using Python script with custom selector and wait time
python scripts/upload_file.py https://uutool.cn/excel/ workspace/test.xlsx "#filePicker" 3000
```
