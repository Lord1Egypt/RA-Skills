---
name: ghost-writer-sync
description: Pulls published blog posts from Substack and Ghost into an Obsidian or Logseq vault for AI-assisted repurposing.
tools:
  - name: sync_posts
    description: Synchronizes all configured blog sources into the local vault. Fetches new posts from Substack and/or Ghost, converts HTML to Markdown, and writes files with proper frontmatter.
    arguments:
      - name: config
        description: "Path to the JSON config file (default: ghost-writer-sync.json)."
        type: string
        required: false
      - name: vault
        description: Override vault directory from config.
        type: string
        required: false
      - name: format
        description: 'Output format — "obsidian" (YAML frontmatter) or "logseq" (property list).'
        type: string
        required: false
    execution:
      command: python3 {{SKILL_DIR}}/sync.py sync --config "{{config}}" --vault "{{vault}}" --format "{{format}}"
      output_format: markdown
  - name: add_substack
    description: Adds a Substack publication as a sync source. The RSS feed is public so no API key is needed.
    arguments:
      - name: url
        description: "Publication URL (e.g. https://example.substack.com)."
        type: string
        required: true
      - name: config
        description: Path to the JSON config file.
        type: string
        required: false
    execution:
      command: python3 {{SKILL_DIR}}/sync.py add-substack --url "{{url}}" --config "{{config}}"
      output_format: markdown
  - name: add_ghost
    description: Adds a Ghost blog as a sync source. Requires a Ghost Content API key in id:secret format.
    arguments:
      - name: url
        description: "Ghost site URL (e.g. https://myblog.ghost.io)."
        type: string
        required: true
      - name: api_key
        description: "Ghost Content API key (id:secret format)."
        type: string
        required: true
      - name: config
        description: Path to the JSON config file.
        type: string
        required: false
    execution:
      command: python3 {{SKILL_DIR}}/sync.py add-ghost --url "{{url}}" --api-key "{{api_key}}" --config "{{config}}"
      output_format: markdown
  - name: list_sources
    description: Lists all configured blog sources and the current vault path.
    arguments: []
    execution:
      command: python3 {{SKILL_DIR}}/sync.py list --config "{{config}}"
      output_format: markdown
  - name: show_config
    description: Displays the current sync configuration.
    arguments: []
    execution:
      command: python3 {{SKILL_DIR}}/sync.py config --config "{{config}}"
      output_format: markdown
---

# Ghost-Writer Sync

Automatically pulls your published blog posts (Substack / Ghost) into your local Obsidian or Logseq vault for AI-assisted repurposing.

## How It Works

```
Blog Source  →  Fetch Posts  →  HTML → Markdown  →  Write to Vault
(Substack RSS / Ghost API)       (stdlib)         (frontmatter + body)
```

1. **Fetch** — Pulls published posts from each configured source
2. **Convert** — Transforms HTML content to clean Markdown using a stdlib-only converter
3. **Write** — Saves each post as a Markdown file with rich frontmatter in your vault

## Supported Sources

| Source | Auth | Notes |
|--------|------|-------|
| Substack | None (public RSS) | Reads the `/feed` endpoint |
| Ghost | Content API key (`id:secret`) | Uses Admin API JWT auth |

## Output Formats

| Format | Frontmatter | Filename |
|--------|-------------|----------|
| Obsidian | YAML block (`---` delimited) | `{slug}.md` |
| Logseq | Property list (`key:: value`) | `{date} {slug}.md` |

## Frontmatter Fields

Every synced post includes:

| Field | Description |
|-------|-------------|
| `title` | Post title |
| `source` | `substack` or `ghost` |
| `url` | Original post URL |
| `published` | Publication date |
| `synced` | Timestamp of last sync |
| `post_id` | Stable hash-based ID for dedup |
| `tags` | (Ghost only) Tag names |
| `excerpt` | (Ghost only) Post excerpt |
| `feature_image` | (Ghost only) Hero image URL |

## Usage

### Add a source

```bash
# Substack — just the URL
python3 sync.py add-substack --url https://example.substack.com

# Ghost — URL + API key
python3 sync.py add-ghost --url https://myblog.ghost.io --api-key abc123:def456...
```

### Run a sync

```bash
python3 sync.py sync --vault /path/to/obsidian-vault
```

### Check config

```bash
python3 sync.py list
python3 sync.py config
```

## Repurposing Workflow

Once posts are in your vault, use your AI assistant to:

- Rewrite posts as Twitter/X threads
- Generate LinkedIn summaries
- Create newsletter compilations
- Extract key quotes and talking points
- Draft follow-up posts based on themes

Posts land as standard Markdown files, so they work with any Obsidian plugin, Logseq graph, or AI tool that reads `.md` files.
