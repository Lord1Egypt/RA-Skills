---
name: affine-cli
description: Command-line tool for managing Affine documents, tags, folders, collections, files, databases, comments, journals and workspaces. Supports both cloud (app.affine.pro) and self-hosted deployments.
homepage: https://github.com/woodcoal/affine-cli
tags: [affine, document-management, cli, markdown, notes, wiki, database, collaboration, self-hosted]
metadata:
  openclaw:
    requires:
      bins: [node, npm]
      env:
        AFFINE_API_TOKEN: required
        AFFINE_BASE_URL: "optional — defaults to https://app.affine.pro"
        AFFINE_WORKSPACE_ID: optional
    note: Configuration loads from: env > local .env > ~/.affine-cli/affine-cli.env
---

# Affine CLI

Command-line tool for managing Affine documents and workspaces. Works with both cloud and self-hosted Affine instances.

## Installation Check

First, verify affine-cli is installed:

```bash
which affine-cli || npm list -g affine-cli
```

If not installed, install globally:

```bash
npm install -g affine-cli
```

Or run directly with npx:

```bash
npx affine-cli <command>
```

## When to Use

- Managing documents, tags, folders, collections
- Working with databases, comments, journals
- Batch operations on Affine workspace
- Automating document workflows

## Quick Start

```bash
# 1. Login (get token from https://app.affine.pro/settings/tokens)
affine-cli auth login --token YOUR_TOKEN

# 2. Check status
affine-cli auth status

# 3. List workspaces
affine-cli workspace list

# 4. List documents
affine-cli doc list
```

**Self-hosted:**
```bash
affine-cli auth login --url https://your-affine.example.com --token YOUR_TOKEN
```

## Command Overview

| Module | Commands |
|--------|----------|
| **auth** | login, logout, status |
| **workspace** | list |
| **doc** | list, all, info, create, delete, copy, update, search, replace, append, publish, unpublish |
| **tags** | list, create, add, remove, delete, info |
| **folder** | all, list, create, delete, update, clear, add, move, remove |
| **collection** | list, info, create, update, delete, add, remove |
| **file** | upload, delete, clean |
| **database** | list, columns, query, create, insert, update, delete, remove |
| **comments** | list, create, update, delete, resolve |
| **journal** | list, create, info, append, update |

## Common Examples

### Daily Journal

```bash
# Create today's journal
affine-cli journal create

# Append to today's journal
affine-cli journal append --content "# Morning\n- Reviewed tasks\n- Team standup"

# Append to specific date
affine-cli journal append --date 2025-04-10 --content "# Notes\nMeeting with team"

# View journal
affine-cli journal info --date 2025-04-10

# List recent journals
affine-cli journal list --count 7
```

### Documents

```bash
# Find a document by title
affine-cli doc search -q "meeting notes"

# Create from file (README.md, etc.)
affine-cli doc create -t "Q2 Planning" -c "@planning.md"

# Create with tags
affine-cli doc create -t "Project Alpha" -c "# Project\nDetails" --tags "work,important" --icon "📁"

# View document content
affine-cli doc info -i DOC_ID --content markdown

# Add content to document
affine-cli doc append -i DOC_ID --content "\n\n## Update\nNew content here"

# Search with tag filter
affine-cli doc search -q "budget" --tag finance
```

### Tags

```bash
# Create tag
affine-cli tags create --name "review"

# Add tag to document
affine-cli tags add -d DOC_ID --tag review

# List all tags
affine-cli tags list

# Find documents with tag
affine-cli tags info --tag review
```

### Folders

```bash
# Create folder
affine-cli folder create --name "Projects"

# List root folders
affine-cli folder all

# List folder contents
affine-cli folder list --id FOLDER_ID

# Move document to folder
affine-cli folder move --id FOLDER_ID -d DOC_ID
```

### Databases

```bash
# List databases in a doc
affine-cli database list --doc DOC_ID

# Query data (filters)
affine-cli database query --doc DOC_ID --id DB_ID -q '[{"column":"Status","operator":"eq","value":"Done"}]'

# Insert new row
affine-cli database insert --doc DOC_ID --id DB_ID --content '[{"Task":"Review PR","Status":"Todo"}]'

# Update rows
affine-cli database update --doc DOC_ID --id DB_ID --values '{"Status":"Done"}' -q '[{"column":"Task","operator":"contains","value":"Review"}]'
```

## Configuration

**Priority**: env vars > local .env > global config

**Files:**
- Global: `~/.affine-cli/affine-cli.env`
- Local: `<project>/.env`

**Environment variables:**
- `AFFINE_API_TOKEN` - Required, get from Settings → Tokens
- `AFFINE_BASE_URL` - Server URL (default: https://app.affine.pro)
- `AFFINE_WORKSPACE_ID` - Default workspace

## Reference Files

- [commands/basics.md](commands/basics.md) - Auth, workspace, documents
- [commands/tags-folders.md](commands/tags-folders.md) - Tags and folders
- [commands/collections.md](commands/collections.md) - Collections
- [commands/files.md](commands/files.md) - File attachments
- [commands/databases.md](commands/databases.md) - Database operations
- [commands/comments.md](commands/comments.md) - Comments
- [commands/journals.md](commands/journals.md) - Journals

## Support

- GitHub: https://github.com/woodcoal/affine-cli
- Issues: https://github.com/woodcoal/affine-cli/issues
- Docs: https://deepwiki.com/toeverything/AFFiNE