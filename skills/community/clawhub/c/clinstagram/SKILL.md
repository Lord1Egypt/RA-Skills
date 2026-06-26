---
name: clinstagram
description: >
  Full Instagram CLI — posting, DMs, stories, analytics, followers, hashtags, likes, comments.
  Supports Meta Graph API (official, safe) and private API (full features).
  Three compliance modes: official-only, hybrid-safe, private-enabled.
metadata: {"openclaw": {"requires": {"bins": ["clinstagram"], "env": ["CLINSTAGRAM_CONFIG_DIR"]}, "primaryEnv": "CLINSTAGRAM_SECRETS_FILE", "emoji": "📸", "homepage": "https://github.com/199-biotechnologies/clinstagram", "install": [{"pip": "clinstagram"}]}}
---

# clinstagram

Hybrid Instagram CLI for AI agents. Routes between Meta Graph API and instagrapi private API based on compliance policy.

## Install

```bash
pip install clinstagram
```

## Critical: Global Flags Before Subcommand

```bash
clinstagram --json --account main dm inbox     # CORRECT
clinstagram dm inbox --json                    # WRONG — Typer limitation
```

Global flags: `--json`, `--account NAME`, `--backend auto|graph_ig|graph_fb|private`, `--proxy URL`, `--dry-run`, `--enable-growth-actions`

## Quick Start

```bash
# Check status
clinstagram --json auth status

# Set compliance mode
clinstagram config mode official-only    # Graph API only, zero risk
clinstagram config mode hybrid-safe      # Graph primary, private read-only (default)
clinstagram config mode private-enabled  # Full access, user accepts risk

# Connect backends
clinstagram auth connect-ig   # Instagram Login (posting, comments, analytics)
clinstagram auth connect-fb   # Facebook Login (adds DMs, stories, webhooks)
clinstagram auth login         # Private API (username/password/2FA via instagrapi)
```

## Commands

| Group | Commands | Notes |
|-------|----------|-------|
| `auth` | `status`, `login`, `connect-ig`, `connect-fb`, `probe`, `logout` | Start with `auth status --json` |
| `post` | `photo`, `video`, `reel`, `carousel` | Accepts local paths or URLs |
| `dm` | `inbox`, `thread ID`, `send @user "text"`, `send-media`, `search` | Cold DMs = private API only |
| `story` | `list [@user]`, `post-photo`, `post-video`, `viewers ID` | |
| `comments` | `list MEDIA_ID`, `add`, `reply`, `delete` | add/reply need `--enable-growth-actions` |
| `analytics` | `profile`, `post ID\|latest`, `hashtag TAG` | |
| `followers` | `list`, `following`, `follow @user`, `unfollow @user` | follow/unfollow need `--enable-growth-actions` |
| `user` | `info @user`, `search QUERY`, `posts @user` | |
| `hashtag` | `top TAG`, `recent TAG` | |
| `like` | `post MEDIA_ID`, `undo MEDIA_ID` | Needs `--enable-growth-actions` |
| `config` | `show`, `mode MODE`, `set KEY VAL` | Modes: `official-only`, `hybrid-safe`, `private-enabled` |

## JSON Output

Success:
```json
{"exit_code": 0, "data": {}, "backend_used": "graph_fb"}
```

Error:
```json
{"exit_code": 2, "error": "session_expired", "remediation": "Run: clinstagram auth login", "retry_after": null}
```

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Parse `data` |
| 1 | Bad arguments | Fix syntax |
| 2 | Auth error | Run `remediation` command |
| 3 | Rate limited | Wait `retry_after` seconds |
| 4 | API error | Retry |
| 5 | Challenge required | Check `challenge_type`, prompt user |
| 6 | Policy blocked | Change compliance mode |
| 7 | Capability unavailable | Connect another backend |

## Agent Workflow

```bash
# 1. Check what's available
clinstagram --json auth status

# 2. Probe capabilities
clinstagram --json auth probe

# 3. Preview before acting
clinstagram --dry-run --json post photo img.jpg --caption "test"

# 4. Execute
clinstagram --json dm inbox --unread --limit 20

# 5. On error, read remediation field and execute it
```

## Growth Actions (Disabled by Default)

Follow, unfollow, like, unlike, comment add/reply require `--enable-growth-actions`. This is a safety gate — confirm with user before enabling.

## Backend Capability Matrix

| Feature | graph_ig | graph_fb | private |
|---------|:--------:|:--------:|:-------:|
| Post | Y | Y | Y |
| DM inbox | - | Y | Y |
| Cold DM | - | - | Y |
| Stories | - | Y | Y |
| Comments | Y | Y | Y |
| Analytics | Y | Y | Y |
| Follow/Unfollow | - | - | Y |
| Hashtag | Y | Y | Y |

Preference order: `graph_ig` > `graph_fb` > `private`. Override with `--backend`.

## Examples

```bash
# Check DMs
clinstagram --json dm inbox --unread

# Reply to a message
clinstagram --json dm send @alice "Thanks!"

# Post a photo
clinstagram --json post photo /path/to/img.jpg --caption "Hello world"

# Get analytics
clinstagram --json analytics post latest

# Search users
clinstagram --json user search "coffee shops"

# Browse hashtag
clinstagram --json hashtag top photography --limit 10
```

## Config

File: `~/.clinstagram/config.toml`. Override dir with `CLINSTAGRAM_CONFIG_DIR` env var.
