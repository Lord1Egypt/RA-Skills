---
name: gety-local-search
description: This skill should be used when the user wants to search for local files or documents on their computer. Trigger phrases include "帮我找文件", "搜索本地文件", "查找文档", "本地搜索", "找一下XXX文件", "search local files", "find files", "搜一下本地有没有", "找一找电脑里", "帮我搜索", "查找本地", and any request to locate or retrieve locally stored documents, notes, or files by content or name.
---

# Gety Local Search

## Overview

To search local files and documents indexed by Gety, use the `gety` CLI. Gety is an AI-powered local file search engine that supports semantic search across all indexed content on the user's machine.

## Quick Start

To perform a basic search:

```bash
gety search "<query>"
```

To get structured JSON output (useful for further processing):

```bash
gety search "<query>" --json
```

## Core Operations

### Searching Documents

To search indexed content, use `gety search` with the user's query. Key options:

| Option | Description |
| --- | --- |
| `-n, --limit <n>` | Max results to return (default: 10) |
| `--offset <n>` | Pagination offset (default: 0) |
| `-c, --connector <name>` | Filter by connector name (repeatable or comma-separated) |
| `-e, --ext <ext>` | Filter by file extension (e.g. `pdf,docx`) |
| `--match-scope <scope>` | Filter by match type: `title`, `content`, `semantic` |
| `--sort-by <field>` | Sort by `default` or `update_time` |
| `--sort-order <dir>` | `ascending` or `descending` |
| `--update-time-from <iso8601>` | Filter by update time (from) |
| `--update-time-to <iso8601>` | Filter by update time (to) |
| `--no-semantic-search` | Disable semantic search (enabled by default) |

**Examples:**

```bash
# Basic search
gety search "meeting notes"

# Search with more results and pagination
gety search "roadmap" -n 20 --offset 20

# Filter by connector and file type
gety search "security review" -c "Folder: Work" -e pdf,docx

# Sort by most recently updated
gety search "design system" --match-scope title,content --sort-by update_time --sort-order descending

# JSON output for processing
gety search "project plan" --json
```

### Fetching a Specific Document

To retrieve detailed content of a specific document by its connector ID and document ID:

```bash
gety doc <connector_id> <doc_id>
gety doc <connector_id> <doc_id> --json
```

### Managing Connectors

Connectors define which local directories Gety indexes.

```bash
# List all available connectors
gety connector list

# Add a new directory to index
gety connector add /path/to/folder --name "Folder: Work"

# Remove a connector by ID
gety connector remove folder_1
```

## Workflow

1. **Receive the user's search request** — identify the query intent (file name, content topic, file type, date range, etc.)
2. **Run `gety connector list`** if unsure which connectors exist, to understand the indexed scope
3. **Run `gety search "<query>"`** with appropriate options based on the user's intent
4. **Present results clearly** — show file name, location, and a brief description of matched content
5. **Fetch full content if needed** — use `gety doc <connector_id> <doc_id>` when the user needs to read the document
6. **Handle no-results gracefully** — suggest broadening the query, checking connector coverage, or verifying the index is up to date
7. **Handle exit codes** — check the process exit code after each command:
   - `69`: Gety is not running — ask the user to start the Gety desktop app and retry
   - `77`: Quota exceeded — inform the user and suggest retrying later
   - `2`: Invalid arguments — check command syntax with `gety search --help`
   - `1`: General error — report the error message to the user
   - Full exit code reference: `references/gety_cli.md`

## References

Full CLI documentation is available in `references/gety_cli.md`.
