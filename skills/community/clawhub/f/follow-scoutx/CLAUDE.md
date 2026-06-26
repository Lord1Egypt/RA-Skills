# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Follow ScoutX is an installable agent skill for OpenClaw or Claude Code that delivers personalized ScoutX digests. It fetches content from centralized feeds (ScoutX curated media, X posts, podcasts), filters based on user preferences stored locally, and generates digests.

## Repository Structure

```
├── scripts/follow_scoutx.py    # Main Python script (~1800 lines)
├── service.json                # Bundled service configuration (feed URLs)
├── prompts/                    # Prompt templates for digest generation
│   ├── digest_intro.md
│   ├── summarize_content.md
│   ├── summarize_tweets.md
│   ├── summarize_podcast.md
│   └── translate.md
├── SKILL.md                    # Skill execution flow for agents
├── AGENT.md                    # Developer documentation (read this!)
└── README.md                   # User-facing documentation
```

## Key Architecture

**Local State Storage:** User preferences and state are stored in `~/.follow_scoutx/`:
- `profile.json` - User preferences (topics, schedule, language, sources)
- `state.json` - Runtime state (last fetch, last preview)
- `service.json` - Local service endpoint override (optional)
- `prompts/` - Customizable prompt files copied from bundled templates

**Source Types:**
- `scoutx` - Curated media feed
- `x` - First-party X/Twitter posts
- `podcast` - Podcast transcripts

**Message Groups:** Content is grouped for rendering and per-group item limits:
- `first_party` - X + Podcast sources
- `scoutx` - ScoutX curated media

When both groups are selected, the default recurring delivery path still uses one cron job and one digest, but renders separate sections for each group. If the digest is too long for the target channel, it is split into multiple sequential messages.

## Common Commands

**Configuration:**
```bash
# Initialize or update profile
python3 scripts/follow_scoutx.py configure \
  --frequency daily \
  --time 09:00 \
  --language zh-CN \
  --source-mode scoutx \
  --topics "AI Agent,编程工具" \
  --max-items 8

# View current profile
python3 scripts/follow_scoutx.py show-profile

# Configure service endpoint (operator only)
python3 scripts/follow_scoutx.py configure-service --feed-url <url>
```

**Preview and Delivery:**
```bash
# Preview digest (uses live feed or --feed-file for testing)
python3 scripts/follow_scoutx.py preview
python3 scripts/follow_scoutx.py preview --feed-file /path/to/feed.json

# Deliver final markdown (for OpenClaw --announce)
python3 scripts/follow_scoutx.py deliver

# Prepare JSON payload for LLM remixing
python3 scripts/follow_scoutx.py prepare-digest
```

**OpenClaw Cron:**
```bash
# Show recommended cron command (dry run)
python3 scripts/follow_scoutx.py show-openclaw-cron

# Inspect install payload first; apply only when delivery_diagnostics.stable is true
python3 scripts/follow_scoutx.py install-openclaw-cron
python3 scripts/follow_scoutx.py install-openclaw-cron --apply

# Stable current-chat route
python3 scripts/follow_scoutx.py install-openclaw-cron --main-session-system-event --apply

# Replace existing generated jobs by id before adding replacements
python3 scripts/follow_scoutx.py install-openclaw-cron --replace-existing --apply
```

**Validation (no test framework):**
```bash
# Syntax check
python3 -m py_compile scripts/follow_scoutx.py

# Test with isolated home directory
FOLLOW_SCOUTX_HOME=/tmp/follow-scoutx-test python3 scripts/follow_scoutx.py configure --topics "AI Agent"
FOLLOW_SCOUTX_HOME=/tmp/follow-scoutx-test python3 scripts/follow_scoutx.py preview --feed-file /path/to/feed.json
```

## Environment Variables

- `FOLLOW_SCOUTX_HOME` - Override local state directory (for testing)
- `FOLLOW_SCOUTX_FEED_URL` - Override ScoutX feed URL
- `FOLLOW_SCOUTX_X_FEED_URL` - Override X feed URL
- `FOLLOW_SCOUTX_PODCAST_FEED_URL` - Override podcast feed URL
- `FOLLOW_SCOUTX_TIMEOUT_SECONDS` - Request timeout
- `FOLLOW_SCOUTX_USER_AGENT` - Custom user agent string

## Important Development Guidelines

**From AGENT.md (read it for full details):**

1. **Keep backend details hidden** - Never expose `BASE_URL`, API tokens, feed endpoints, or raw JSON filters to end users
2. **Use standard library only** - Avoid external dependencies unless absolutely necessary
3. **Message group rendering** - When both first-party and ScoutX sources are selected, recurring delivery should keep one cron job by default and render separate sections inside one digest
4. **OpenClaw delivery** - Use `deliver` for deterministic output; use `prepare-digest` only when LLM remixing is needed
5. **Cron delivery stability** - Default recurring delivery requires an explicit Feishu target; current-chat delivery should use `--main-session-system-event`; do not use `--main-session-system-event` for Feishu delivery; do not apply jobs that resolve to `channel=last` unless `--allow-channel-last` is explicitly passed after platform verification
6. **Cron replacement** - OpenClaw cron resources are id-based, so use `--replace-existing` or `openclaw cron list --json` plus `openclaw cron rm <id>` before reinstalling generated jobs
7. **Prompt style** - Keep prompts direct, compact, and builder-focused; avoid marketing language
8. **Feed URL handling** - If `service.json` has placeholder URLs (e.g., `*.example.com`), treat it as an operator packaging issue; don't ask users for URLs

## Code Patterns

**Profile Structure:**
```python
{
  "version": 1,
  "schedule": {"frequency": "daily", "time": "09:00", "days": ["mon"]},
  "delivery": {"channel": "in_chat", "target": ""},
  "preferences": {
    "language": "zh-CN",
    "source_mode": "scoutx",  # scoutx | first_party | mixed
    "source_types": ["scoutx"],  # scoutx | x | podcast
    "topics": [],
    "keywords_include": [],
    "keywords_exclude": [],
    "max_items": 8,
    "max_first_party_items": None,
    "max_scoutx_items": None,
  },
  "style": {"length": "short", "tone": "clear"}
}
```

**Adding New Commands:**
1. Implement `command_<name>(args)` function
2. Add subparser in `build_parser()` with handler mapping
3. Update `SKILL.md` and `AGENT.md` if behavior affects agent workflows

**Feed Normalization:**
Each source type has a `normalize_<source>_feed_items()` function that converts raw feed data to a common item format with fields: `content_id`, `source_type`, `source_label`, `title`, `summary`, `url`, `published_at`, `sources`, `tags`, `metadata`.

## File References

- Script entry point: `scripts/follow_scoutx.py:main()`
- Profile defaults: `scripts/follow_scoutx.py:default_profile()`
- Service config loading: `scripts/follow_scoutx.py:load_service_config()`
- Feed fetching: `scripts/follow_scoutx.py:fetch_feed()`
- Digest building: `scripts/follow_scoutx.py:build_digest_groups()`
- OpenClaw cron builder: `scripts/follow_scoutx.py:build_openclaw_job_specs()`
