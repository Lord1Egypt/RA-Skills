---
name: gdrive
description: Access Google Drive in a privacy-safe way by only working inside an allow-listed set of approved folders. Use when the user wants to browse, read, search, or upload files in Google Drive but strictly within pre-approved folders.
---

# GDrive – Approved-Folder Google Drive Access

## What this skill does

This skill lets the agent interact with Google Drive **only inside explicitly approved folders**.  
It assumes there is some existing Google Drive access layer (CLI, API, or MCP server) and adds a strict, configurable **allow‑list** in front of it.

Core capabilities:

- List the approved folders and their permissions
- Browse the contents of an approved folder
- Read/download file contents
- Search for files within approved folders
- Upload files to approved folders (if allowed)
- Add or remove approved folders (admin‑only)

Everything outside the allow‑listed folders is treated as **off‑limits**.

---

## Configuration model

The skill uses an “approved folders” configuration that can be represented as JSON or any other config source with the same fields:

