---
name: birdx
description: X/Twitter CLI that reads Chrome cookies directly from disk — no browser session required after first auth. Supports reading tweets with viewCount/bookmarkCount, full thread replies, search with engagement metrics, and followers/following lists. Use when you need to fetch Twitter/X data, search tweets, read threads, or get user follower lists without a browser. No Twitter API key needed.
---

# birdx

CLI for X/Twitter via direct API calls. Reads Chrome cookies from disk (no browser needed after `birdx auth`).

## Install

```bash
bash <skill-dir>/scripts/install.sh
```

Or manually:
```bash
npm install --prefix ~/clawd ws jsdom x-client-transaction-id
ln -sf <skill-dir>/scripts/birdx.js /opt/homebrew/bin/birdx
birdx auth
```

## Auth

```bash
birdx auth          # Read Chrome cookies from disk (no browser needed)
birdx auth --cdp    # Use openclaw browser CDP fallback
```

Cookie cache: `~/.config/bird/birdx-cookies.json` (TTL ~5h, re-run auth to refresh)

## Commands

```bash
# Read single tweet (includes viewCount, bookmarkCount)
birdx read <tweet-url|id>

# Read thread + all replies (--sort relevance puts author thread first)
birdx replies <tweet-url|id> --sort relevance
birdx replies <tweet-url|id> --sort latest --total 40

# Search tweets (full metrics: views, likes, bookmarks, reposts)
birdx search "query" --sort top --total 20
birdx search "from:elonmusk" --sort latest

# Followers / following
birdx followers @username --total 50
birdx following @username --total 20

# JSON output
birdx read <url> --json
birdx search "query" --json
```

## Output Fields

- `viewCount` — total impressions
- `likeCount`, `repostCount`, `replyCount`, `bookmarkCount`
- `author.userName`, `author.fullName`, `author.isVerified`

## Environment

- `BIRDX_MODULES` — override node_modules path (default: `$HOME/clawd/node_modules`)
- Deps required: `ws`, `jsdom`, `x-client-transaction-id`
- Node 20+ required (uses `node:sqlite`)

## Notes

- Query ID cache auto-refreshes from X on first use. If stale: check `~/.config/bird/query-ids-cache.json`
- `birdx read` may fail behind certain VPNs; `birdx search` is more reliable
- Bookmark count is only available via birdx (not bird CLI)
