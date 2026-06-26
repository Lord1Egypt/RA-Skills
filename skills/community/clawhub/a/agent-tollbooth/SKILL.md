---
name: agent-tollbooth
version: 2.0.0
description: "Web access privileges for your agent. So your agent stops hitting walls."
homepage: https://github.com/highnoonoffice/agent-tollbooth
source: https://github.com/highnoonoffice/agent-tollbooth
license: MIT
metadata: ~
config:
  - $OPENCLAW_WORKSPACE/data/agent-tollbooth/web-access-log.json — event log written by scripts/web-log.py
  - $OPENCLAW_WORKSPACE/data/agent-tollbooth/cache/ — price and response cache written by fetch-crypto.py and fetch-prices.py
---

# Agent Tollbooth

You're mid-task. Your agent fires a Yahoo Finance request. Gets a 429. Stops. You don't know if it's rate limits, a bad endpoint, a missing header, or just bad luck. You try again. Same thing. You start debugging blind.

Tollbooth is the field notes that stop this from happening twice. Observed operating profiles for 16 external services — safe endpoints, sleep intervals, caching patterns, auth requirements — built from real API friction. Your agent checks the profile before calling, follows the safe pattern, and logs what happens. Next time it already knows.

Every external service has a threshold. This skill provides the map so agents learn them once and stop hitting them twice.

## Core Pattern

Before calling any external service:
1. Check `references/profiles.md` for an existing profile
2. Follow its safe pattern — endpoint, sleep, cache, auth
3. If no profile exists, observe behavior and add an entry after

## Caching

Always cache prices and API responses locally when TTL allows.

- Default TTL: 300s (5 minutes) for prices
- Cache file: `$OPENCLAW_WORKSPACE/data/agent-tollbooth/cache/`
- Serve from cache first — only hit the API when stale or forced

**Script:** `scripts/fetch-prices.py` implements cache + sequential Yahoo Finance fetching. Use it instead of raw requests. CoinGecko and other services are covered by profiles in `references/profiles.md`.

## How It Learns

Tollbooth grows with your usage. Three scripts form the learning loop:

**Before any external call:**
```bash
python3 scripts/check-profile.py coingecko.com
```
Returns the safe pattern if a profile exists. If not, logs the miss and returns exit code 1 — your agent can continue, but observation has started.

**During any call — log what happens:**
```python
from scripts.web_log import log_event
log_event("my-api.com", "429", "hit rate limit at 10 req/min", worked=None)
log_event("my-api.com", "success", "sequential 500ms sleep worked", worked="sequential + 500ms sleep")
```

**After enough observations — promote to a profile:**
```bash
python3 scripts/promote-profile.py           # dry run, see what's ready
python3 scripts/promote-profile.py --write   # append drafts to profiles.md
```
Default threshold: 5 events. Auto-drafted profiles include all observed friction and working patterns. Review before trusting — they're drafts, not finished entries.

Events are written to `$OPENCLAW_WORKSPACE/data/agent-tollbooth/web-access-log.json` — outside the skill bundle, never modifying packaged files. Cache files go to `$OPENCLAW_WORKSPACE/data/agent-tollbooth/cache/`. Set `OPENCLAW_WORKSPACE` before running (standard on any OpenClaw install).

## Workspace Access

This skill writes event logs and cache files to `$OPENCLAW_WORKSPACE/data/agent-tollbooth/`. No credentials are accessed. No sensitive data is written. No files outside this directory are touched.

## Service Profiles

See `references/profiles.md` for all current profiles:
- Yahoo Finance
- CoinGecko
- Ghost Admin API
- ClawHub API
- Telegram Bot API
- Replicate
- OpenAI API
- Anthropic API
- GitHub API
- Brave Search API
- Serper (Google Search)
- Notion API
- Airtable API
- Stripe API
- HuggingFace Inference API
- Firecrawl
