---
name: file-browser
description: Read-only file browsing and reading in the OpenClaw workspace (/home/alfred/.openclaw/workspace). Use for listing directories or reading text files (up to 10k chars). Triggers on queries like "list files in [dir]", "read file [path]", "browse workspace [path]". Restrict to relative paths; reject absolutes or ../ escapes. NOT for writing, deleting, executing, or non-workspace access.
---

# File Browser Skill

## Quick Start
Resolve all paths relative to WORKSPACE=/home/alfred/.openclaw/workspace. Sanitize inputs to prevent escapes or absolutes.

- To list directory: exec("scripts/list_files.sh", [rel_path]) → JSON {success: bool, data: array of names, error: string}
- To read file: exec("scripts/read_file.sh", [rel_path]) → JSON {success: bool, data: string (text content), error: string}
- Handle errors: For binary/large/non-text files, return error JSON.

## Step-by-Step Workflow
1. Parse user query for action (list/read) and relative path.
2. Call appropriate script with sanitized rel_path.
3. Parse JSON output; respond to user with results or error message.
4. If path invalid or outside workspace, reject immediately.

## Safety Guidelines
- Enforce read-only: No writes, deletes, or exec beyond scripts.
- Log accesses if verbose mode enabled.
- For large files (>10k chars), truncate or summarize.

## Edge Cases
- Empty path: Default to "." (workspace root).
- Binary file: Return error "Non-text file".
- See references/examples.md for more (if added).

## Bundled Resources
- scripts/list_files.sh: Bash wrapper for ls.
- scripts/read_file.sh: Bash wrapper for cat with limits.
