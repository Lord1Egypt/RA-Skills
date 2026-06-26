---
name: feedship
description: "Manage RSS/Atom feeds, subscribe to websites, search and read articles. Use when working with feeds, RSS, Atom, subscribing to content sources, managing an information pipeline, or fetching articles from subscribed feeds. Commands: feed add|list|remove, fetch, article list|view|open|related, search, discover, info."
metadata:
  openclaw:
    requires:
      bins:
        - uv
    cron:
      syntax: cron([minute,] [hour,] [day-of-month,] [month,] [day-of-week])
      default: "*/30 * * * *"  # Every 30 minutes
      description: "Fetch new articles from all subscribed feeds every 30 minutes"
---

# Feedship Skill

**Version:** 1.5
**For:** Claude Code and OpenClaw compatible agents
**Description:** Manage information feeds, subscribe to RSS/GitHub sources, and search articles

## Setup

Before using this skill, install feedship with ML and cloud extras:

```bash
uv tool install 'feedship[ml,cloudflare]' --python 3.12 --force
```

> **Note:** `cloudflare` extra provides scrapling (HTML fetching); `ml` extra provides
> sentence-transformers + chromadb (semantic search). Both are required for full functionality.

### China / Restricted Networks

For environments where PyPI or HuggingFace is not accessible, use mirrors:

```bash
# Add to ~/.bashrc for persistence
echo 'export HF_ENDPOINT=https://hf-mirror.com' >> ~/.bashrc
echo 'export PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/' >> ~/.bashrc
source ~/.bashrc

# Install
uv tool install 'feedship[cloudflare,ml]' --force
```

### Upgrade

```bash
# From PyPI (if accessible)
uv tool upgrade feedship

# From GitHub (latest commits)
uv tool install 'feedship @ git+https://github.com/yanpeipan/feedship.git' \
  --pip-args='-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com' \
  --include-deps --force
```

After installation, verify with: `feedship --version`

> **First-time setup for semantic search:** After installing, run `feedship fetch --all`
> to populate the vector database with article embeddings. Semantic search requires
> embeddings to be generated first (chromadb storage).

---

## Commands

### feed

Manage RSS/Atom feeds and GitHub release trackers.

#### feed add

```bash
feedship feed add <url> [options]
```

Add a new feed by URL with automatic provider detection.

**Options:**
- `--auto-discover/--no-auto-discover` — Enable feed auto-discovery (default: enabled)
- `--automatic on|off` — Automatically add all discovered feeds (default: off)
- `--discover-depth N` — Discovery crawl depth 1-10 (default: 1)
- `--weight FLOAT` — Feed weight for semantic search (default: 0.3)

**Examples:**
```bash
feedship feed add https://example.com
feedship feed add https://github.com/python/cpython --automatic on
feedship feed add https://example.com --discover-depth 3
```

#### feed list

```bash
feedship feed list [-v]
```

List all subscribed feeds with status.

**Options:**
- `-v, --verbose` — Show detailed output
- `--json` — Output in JSON format for programmatic consumption

#### feed remove

```bash
feedship feed remove <feed-id>
```

Remove a subscribed feed by ID.

---

### fetch

```bash
feedship fetch [--all|<feed-ids>] [--concurrency N]
```

Fetch new articles from subscribed feeds.

**Options:**
- `--all` — Fetch all subscribed feeds
- `--concurrency N` — Max concurrent fetches 1-100 (default: 10)

**Examples:**
```bash
feedship fetch --all
feedship fetch abc12345
feedship fetch abc12345 def67890 --concurrency 20
```

---

### article

Manage and view fetched articles.

#### article list

```bash
feedship article list [options]
```

**Options:**
- `--limit N` — Maximum articles (default: 20)
- `--feed-id <id>` — Filter by feed ID
- `--since <date>` — Start date (YYYY-MM-DD)
- `--until <date>` — End date (YYYY-MM-DD)
- `--on <date>` — Specific date (can repeat for multiple)
- `--json` — Output in JSON format for programmatic consumption

#### article view

```bash
feedship article view <article-id>
```

View full article content and metadata.

#### article open

```bash
feedship article open <article-id>
```

Open article in system browser.

#### article related

```bash
feedship article related <article-id> [--limit N]
```

Find semantically related articles.

---

### search

```bash
feedship search <query> [options]
```

Search articles using full-text or semantic search.

**Options:**
- `--limit N` — Maximum results (default: 20)
- `--feed-id <id>` — Filter by feed ID
- `--semantic` — Use semantic (vector) search instead of keyword
- `--rerank` — Apply Cross-Encoder reranking
- `--since <date>` — Start date filter
- `--until <date>` — End date filter
- `--on <date>` — Specific date filter
- `--json` — Output in JSON format for programmatic consumption

**Examples:**
```bash
feedship search "machine learning"
feedship search "python news" --semantic
feedship search "updates" --semantic --rerank
```

---

### discover

```bash
feedship discover <url> [--discover-depth N]
```

Discover RSS/Atom/RDF feeds on a website without subscribing.

**Options:**
- `--discover-depth N` — Crawl depth 1-10 (default: 1)
- `--json` — Output in JSON format for programmatic consumption

**Examples:**
```bash
feedship discover example.com
feedship discover example.com --discover-depth 3
```

### info

```bash
feedship info [options]
```

Display system information, configuration, and storage status.

**Options:**
- `--json` — Output in JSON format for programmatic consumption

**Output includes:**
- Version information
- Configuration file location
- Database/storage path
- Feed count and article count
- Installed extras (ml, cloudflare)

**Examples:**
```bash
feedship info
feedship info --json
```

---

## Output Formats

### Tables

`feed list`, `article list`, `search`, `discover` output Rich tables:
- Magenta headers
- Alternating row styles
- Truncated columns with overflow indicators

### Panels

`article view` uses Rich Panel:
- Title: Article title
- Subtitle: Feed name | Date
- Content: Full article text

### Progress Bars

`fetch` uses Rich progress bars showing:
- Current feed being fetched
- New articles count
- Elapsed time

---

## Common Patterns

### Initial Setup

```bash
# Add a website feed
feedship feed add https://example.com --automatic on

# Fetch all feeds
feedship fetch --all

# View recent articles
feedship article list --limit 50
```

### Daily Workflow

```bash
# Fetch new articles
feedship fetch --all

# Search for topics
feedship search "machine learning" --semantic

# Read an article
feedship article view abc12345

# Open in browser for full view
feedship article open abc12345
```

### Feed Management

```bash
# List feeds
feedship feed list -v

# Remove stale feed
feedship feed remove old123

# Discover new feeds on site
feedship discover news-site.com --discover-depth 2
```

### Scheduled Fetching (OpenClaw Best Practice)

For automated periodic fetching, use platform-specific schedulers:

**macOS (LaunchAgent):**
```xml
<!-- ~/Library/LaunchAgents/com.feedship.fetch.plist -->
<key>ProgramArguments</key><array><string>/usr/local/bin/feedship</string><string>fetch</string><string>--all</string></array>
<key>StartInterval</key><integer>3600</integer>  <!-- every hour -->
```

**Linux (systemd timer):**
```ini
# ~/.config/systemd/user/feedship.timer
[Timer] OnBootSec=5min OnUnitActiveSec=1h
```

**Cron:**
```bash
0 * * * * feedship fetch --all >> ~/.feedship/fetch.log 2>&1
```

**OpenClaw Cron (every 30 minutes):**
```bash
openclaw cron add \
  --name "feedship-fetch" \
  --agent agent \
  --cron "*/30 * * * *" \
  --tz Asia/Shanghai \
  --session isolated \
  --message "uv run --with feedship[ml,cloudflare] feedship fetch --all" \
  --timeout-seconds 1800
```

---

## Optional Dependencies

### ML Extra (`pip install feedship[ml]`)

Required for semantic search and related articles:
- sentence-transformers
- chromadb
- torch

### Cloudflare Extra (`pip install feedship[cloudflare]`)

For enhanced web scraping with:
- browserforge
- playwright
- curl-cffi
