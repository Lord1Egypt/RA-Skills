---
name: file-share
description: Transfer files from OpenClaw workspace to external services using curl upload. Supports transfer.whalebone.io and similar file sharing services.
***

# File Share Skill 📁

## Overview 👀

This skill provides a simple way to transfer files from the OpenClaw workspace to external file sharing services using curl upload commands. It's designed for securely sharing files generated within OpenClaw (logs, reports, media, etc.) with external parties or services.

**Primary function:** Upload a specified file to transfer.whalebone.io using curl's --upload-file option. 🚀

## Quick Start ⚡

### Transfer a file 📤

Provide the path to a file (relative to OpenClaw workspace) to upload it to transfer.whalebone.io:

```txt
/home/ubuntu/.openclaw/workspace/logs/app.log
```

The skill will:
1. Validate the file exists ✅
2. Extract the filename for the upload URL 🔗
3. Execute: `curl --upload-file ./<filename> https://transfer.whalebone.io/<filename>`
4. Return the download URL provided by the service 📎

## Usage Examples 🧩

- `memory/2026-05-15.md` → Uploads your daily memory file 📝
- `logs/error.log` → Uploads an error log ⚠️
- `media/report.pdf` → Uploads a generated PDF report 📄
- `/home/ubuntu/.openclaw/workspace/location-skill.zip` → Uploads the location service skill ZIP 📦

## Technical Details 🛠️

- Uses curl for file uploads (pre-installed in most environments).
- Works with any file accessible from the OpenClaw workspace.
- Returns the direct download URL from transfer.whalebone.io.
- Handles both absolute and relative paths (relative to workspace root).
- Includes basic error handling for missing files and upload failures.
- No API keys or authentication required for basic usage.

## Security Notes 🔒

- Only files within or below the OpenClaw workspace can be transferred.
- The skill prevents directory traversal attacks by validating file paths.
- Original file remains unchanged in the workspace.
- Transfer.whalebone.io files typically expire after a set period (check their policy).

## Resources 📚

### scripts/
Contains the executable Python script for file transfers:

- `file_transfer.py` - Main script that handles file validation and upload execution.

### references/
Documentation about the transfer service and usage guidelines:

- `transfer_service.md` - Details about transfer.whalebone.io service.
- `examples.md` - Common use cases and example workflows.