---
name: apify
description: Run any Apify Actor to scrape web data (Instagram, TikTok, Reddit, Twitter, etc). Handles Actor discovery, quality filtering, probe testing, batched execution, and result collection. Use when user asks to scrape/crawl/extract data from websites or social media platforms, or mentions Apify directly.
---

# Apify Skill

Run any Apify Actor through a standardized workflow: search → validate → execute → collect results.

## Prerequisites

- `APIFY_TOKEN` env var, or a `config.json` with tokens (copy `config.json.example`)
- Python 3 with `requests` installed

## Workflow

### Step 1: Parse User Intent

Extract from the user's request:
- **Platform/target** (Instagram, TikTok, Reddit, etc.)
- **What to scrape** (posts, profiles, hashtags, comments, etc.)
- **Targets** (URLs, usernames, keywords)
- **Quantity/filters** (how many, time range, min likes, etc.)

### Step 2: Select Token

If user specifies a token name or the task maps to a specific account, use that. Otherwise use `default`.

Token can be provided via:
1. `--token` flag (highest priority)
2. `config.json` tokens map (by `--token-name`)
3. `APIFY_TOKEN` env var (fallback)

### Step 3: Search & Select Actor

Run the search script:

```bash
python3 scripts/search_actor.py "instagram scraper" --top 3
```

Output: ranked candidates with score, success rate, rating, pricing model.

**Quality filters (built into script):**
- `notice` = NONE (not deprecated)
- 30-day success rate ≥ 95%
- 30-day runs ≥ 1,000
- User rating ≥ 4.0

Pick the top-ranked candidate. If user has a preference or prior experience with a specific Actor, skip search.

### Step 4: Get Actor Schema & Build run_input

Fetch the Actor's documentation:

```bash
web_fetch https://apify.com/{actor_id}.md
```

Read the input schema section. Construct `run_input` JSON based on:
- The Actor's required/optional fields
- The user's targets and filters
- Sensible defaults from the documentation

**Do NOT ask the user to write JSON.** Build it from their natural language request.

### Step 5: Probe Test (Top 1 → Top 2 → Top 3 fallback)

Test with minimal input before committing to full run:

```bash
python3 scripts/apify_runner.py {actor_id} \
  --input '{...}' \
  --token {token} \
  --probe-only \
  --list-key {key}
```

The probe automatically uses the first 2 items from the list field.

**Checks:**
- Run starts successfully (no permission/billing errors)
- Run completes (no timeout/crash)
- Returns non-empty data

If probe fails → try next candidate Actor. If all 3 fail → report to user with Actor URLs for manual activation.

### Step 6: Full Execution

```bash
python3 scripts/apify_runner.py {actor_id} \
  --input '{...}' \
  --token {token} \
  --output /path/to/results.json \
  --list-key {key} \
  --batch-size 50 \
  --probe
```

**Key flags:**
| Flag | Purpose | Default |
|---|---|---|
| `--list-key` | Field in run_input containing the list to batch | None (no batching) |
| `--batch-size` | Items per batch | 50 |
| `--timeout` | Per-batch timeout (seconds) | 600 |
| `--probe` | Run probe before full execution | Off |
| `--output` | Save results to JSON file | Stdout |
| `--config` | Path to config.json for token lookup | None |
| `--token-name` | Which token to use from config | "default" |

**Batching rules:**
- ≤ batch-size items → single run
- \> batch-size items → auto-split, 3s pause between batches
- Each batch has independent timeout (default 10 min)

### Step 7: Return Results

- Report total items collected
- Save raw JSON to specified output path
- Summarize key stats (items count, batches, any failures)
- Let the caller handle filtering/reporting/delivery

## Common Actor Patterns

| Platform | Typical Actor | list_key | Example input |
|---|---|---|---|
| Instagram | `apify/instagram-scraper` | `directUrls` | `{"directUrls": ["https://instagram.com/user/"], "resultsType": "posts", "resultsLimit": 3}` |
| TikTok | `clockworks/tiktok-scraper` | `hashtags` | `{"hashtags": ["cooking"], "resultsPerPage": 50}` |
| Reddit | `trudax/reddit-scraper-lite` | `startUrls` | `{"startUrls": [{"url": "https://reddit.com/r/cooking/top/?t=month"}], "maxItems": 30}` |
| Twitter | `apidojo/tweet-scraper` | — | Check .md for current schema |

These are starting points. Always verify with the Actor's `.md` page for current schema.
