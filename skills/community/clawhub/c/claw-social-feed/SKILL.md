---
name: claw-social-feed
description: "Fetch social media content and save to Obsidian. Supports Twitter/X, Reddit, GitHub, HackerNews, Bilibili, Weibo, Xiaohongshu and 30+ platforms via bb-browser. Use when: (1) user asks to fetch/sync social media content to Obsidian; (2) user asks to set up scheduled sync; (3) user provides a list of accounts to track."
---

# claw-social-feed

Fetch social media timelines into Obsidian vaults. Multi-platform, incremental sync, smart filtering, auto-tagging.

**Core dependency**: `bb-browser` (via `--openclaw` flag to reuse the OpenClaw browser session). Supports 36 platforms via bb-browser adapters — see [references/platforms.md](references/platforms.md).

## Workflow

```
User config (config.yaml)
      │
      ▼
fetch_save.py
      │
      ├── Dedup accounts
      ├── Read state.json (last fetch cursor)
      │
      ▼
bb-browser site <platform>/<cmd> --openclaw --json
      │
      ▼
Filter → Tag → Write to Obsidian
      │
      ▼
Update state.json
```

## Quick Start

### 1. Install bb-browser

```bash
# Requires Node.js 18+
npm install -g bb-browser

# Verify
bb-browser --version
```

### 2. Configure accounts

Edit `config.yaml`:

```yaml
accounts:
  - platform: twitter
    username: your_target_handle
  - platform: hackernews
    username: your_username

vault_base: ~/Documents/Obsidian Vault/SocialFeed

fetch:
  count: 20

filters:
  min_text_length: 30
  skip_retweet_no_comment: true
  skip_link_only: true
  blocked_keywords: []

tagging:
  enabled: true
  keywords:
    AI / LLM / GPT / Claude: AI
    Python / JavaScript / Rust: coding
```

### 3. Run

```bash
python3 scripts/fetch_save.py --verbose
```

### 4. Check output

Content lands in `vault_base/@username/` — one `.md` file per post, with Obsidian YAML frontmatter (platform, author, date, URL, likes, tags).

---

## Config Reference

### accounts

```yaml
accounts:
  - platform: twitter
    username: dotey
```

- `platform`: must match a bb-browser supported platform (see [references/platforms.md](references/platforms.md))
- `username`: the platform-native user identifier
- **Deduplication**: `platform + username` must be unique within the list

### filters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_text_length` | int | 30 | Skip posts below this character count |
| `skip_retweet_no_comment` | bool | true | Skip retweets with no original comment |
| `skip_link_only` | bool | true | Skip posts that are links/images with little text |
| `blocked_keywords` | list | [] | Skip posts containing any of these keywords |

### tagging

Auto-tag based on keyword matching (case-insensitive, `/` separated synonyms = OR):

```yaml
tagging:
  enabled: true
  keywords:
    AI / LLM / 大模型: AI
    skill / Skills: skill
    Python / JavaScript: coding
```

### fetch.count

```yaml
fetch:
  count: 20  # default 20, max 100
```

`twitter/tweets` returns ~20 tweets newest-first by default. For scheduled syncs, set to 50–100 to avoid missing posts from high-frequency accounts between sync intervals.

---

## Incremental Sync

`state.json` tracks the last-fetched timestamp per account. On re-run:

1. Skips posts with `created_at ≤ last_fetch`
2. Saves only new content
3. Updates `last_fetch` timestamp

**Missed-run compensation**: if a cron job missed a run (e.g., machine was off), the next run will backfill content within `catchup_window_days` (default 3 days).

To force re-fetch an account: delete its entry in `state.json` or delete the corresponding `.md` files.

---

## Scheduled Sync

To enable automatic sync, ask the agent:

> "Sync every morning at 9am" or "Sync every Monday at 8am"

The agent will create a cron job that runs in isolated mode with incremental sync — no duplicates.

---

## Troubleshooting

**`bb-browser: command not found`**
The script auto-detects bb-browser PATH. If it still fails, confirm npm global bin is in your PATH, or install via `npm install -g bb-browser`.

**`twitter/search` returns webpack module error**
Use `twitter/tweets` instead of `twitter/search`. This is a known bb-browser adapter compatibility issue.

**Platform returns 401 Unauthorized**
The OpenClaw browser needs to be logged into that platform. Open the site manually in the browser, log in once, then retry.

**File already exists but want to re-fetch**
Delete the corresponding entry in `state.json` or delete the `.md` files for that account.
