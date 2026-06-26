# Setup Guide

Read this file only when setup state is missing or when the user explicitly asks to reconfigure the skill.

## Goal

Configure **arxiv-to-zotero** so it can search arXiv and import new papers into Zotero in a predictable, organized way.

## Required First-Run Items

Collect and save these Zotero settings:

1. **Zotero library ID**
2. **Zotero library type** (`user` or `group`)
3. **ZOTERO_API_KEY**
   - required
   - store it in `~/.openclaw/.env`

## Fixed Paths

Non-secret config:

`config.json` in the skill root directory

Secrets:

`~/.openclaw/.env`

Use this format:

```env
ZOTERO_API_KEY=your_zotero_key
```

Setup-state file:

`~/.openclaw/config/skills/arxiv-to-zotero.setup.json`

## Write Back to Config

Write these values into `config.json` in the skill root directory:

- `zotero.library_id`
- `zotero.library_type`
- `zotero.target_collection_key` only if the user explicitly wants to override the default collection target

## Default Organization Rules

Unless the user explicitly wants something else, keep these defaults:

- `zotero.default_tags = ["arxiv-to-zotero"]`
- `zotero.target_collection_name = "arxiv-to-zotero"`
- `zotero.auto_create_collection = true`

This means the script will automatically place new imports into the `arxiv-to-zotero` collection and create that collection if it does not already exist.

## Optional Later Edits

These are optional advanced settings in `config.json`:

- `query`
- `zotero.default_tags`
- `zotero.target_collection_key`
- `zotero.target_collection_name`
- `zotero.auto_create_collection`
- `dedupe.*`
- `import_policy.require_pdf`
- `import_policy.max_new_items`
- `sources.arxiv.*`
- `run.*`

## After Setup

Create or update `~/.openclaw/config/skills/arxiv-to-zotero.setup.json`, then resume the original request exactly once.

## Query-Language Rule

Because this skill searches arXiv only, the agent should build the final `search_query` in English. When the user provides Chinese keywords, translate them into concise English technical terms before running the script.
