---
name: follow-news
description: Generate tech news digests with unified source model, internal ranking, and multi-format output. Seven-source data collection from RSS feeds, Twitter/X KOLs, GitHub releases, GitHub Trending, Reddit, web search, and podcasts. Pipeline-based scripts with retry mechanisms and deduplication. Supports Discord, email, and markdown templates.
version: "3.18.0"
homepage: https://github.com/tangwz/follow-news
source: https://github.com/tangwz/follow-news
metadata: {"openclaw":{"requires":{"bins":["python3"]},"optionalBins":["opencli","mail","msmtp","gog","gh","openssl","weasyprint","yt-dlp"],"env":[{"name":"TWITTER_API_BACKEND","required":false,"description":"Twitter backend: auto, opencli, getxapi, twitterapiio, or official. Default: auto; auto tries OpenCLI first."},{"name":"OPENCLI_BIN","required":false,"description":"Optional path to the OpenCLI executable for Twitter/X and Xiaoyuzhou podcast sources. Used when OpenCLI is not available on PATH."},{"name":"OPENCLI_MAX_WORKERS","required":false,"description":"Optional OpenCLI concurrency limit. Defaults to 10."},{"name":"OPENCLI_CLOSE_TABS_AFTER_RUN","required":false,"description":"Close OpenCLI-created X/Twitter tabs after fetch when set to 1. Default: 1."},{"name":"OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN","required":false,"description":"Close OpenCLI-created Chrome automation windows on macOS when set to 1. Default: 1."},{"name":"GETX_API_KEY","required":false,"description":"GetXAPI key for Twitter/X fallback."},{"name":"X_BEARER_TOKEN","required":false,"description":"Twitter/X API bearer token for KOL monitoring."},{"name":"TWITTERAPI_IO_KEY","required":false,"description":"twitterapi.io API key for KOL monitoring."},{"name":"TAVILY_API_KEY","required":false,"description":"Tavily Search API key."},{"name":"WEB_SEARCH_BACKEND","required":false,"description":"Web search backend: auto, brave, or tavily."},{"name":"BRAVE_API_KEYS","required":false,"description":"Brave Search API keys, comma-separated for rotation."},{"name":"BRAVE_API_KEY","required":false,"description":"Brave Search API key, single key fallback."},{"name":"GITHUB_TOKEN","required":false,"description":"GitHub token for higher API rate limits."},{"name":"GH_APP_ID","required":false,"description":"GitHub App ID for automatic installation token generation."},{"name":"GH_APP_INSTALL_ID","required":false,"description":"GitHub App Installation ID for automatic token generation."},{"name":"GH_APP_KEY_FILE","required":false,"description":"Path to GitHub App private key PEM file."},{"name":"YTDLP_BIN","required":false,"description":"Optional path to the yt-dlp executable for YouTube podcast metadata and transcript fetching."}],"tools":[{"bin":"python3","required":true,"description":"Runs data collection and merge scripts."},{"bin":"opencli","required":false,"description":"Preferred Twitter/X backend in auto mode, required for Xiaoyuzhou metadata discovery, and the documented supported Xiaoyuzhou transcript path."},{"bin":"mail","required":false,"description":"msmtp-based mail command for email delivery."},{"bin":"msmtp","required":false,"description":"SMTP transport used by mail."},{"bin":"gog","required":false,"description":"Gmail CLI fallback for email delivery."},{"bin":"gh","required":false,"description":"GitHub CLI fallback for repository auth."},{"bin":"openssl","required":false,"description":"GitHub App JWT signing fallback."},{"bin":"weasyprint","required":false,"description":"PDF rendering backend."},{"bin":"yt-dlp","required":false,"description":"YouTube podcast metadata and transcript backend."},{"script":"scripts/fetch-podcast.py","required":false,"description":"Fetches RSS, YouTube, and Xiaoyuzhou podcast metadata, with optional transcript enrichment."}],"files":{"read":[{"path":"config/defaults/","description":"Default source and topic configurations."},{"path":"references/","description":"Prompt templates and output templates."},{"path":"scripts/","description":"Python pipeline scripts."},{"path":"<workspace>/archive/follow-news/","description":"Previous digests for deduplication."}],"write":[{"path":"/tmp/td-*.json","description":"Temporary pipeline intermediate outputs."},{"path":"/tmp/td-email.html","description":"Temporary email HTML body."},{"path":"/tmp/td-digest.pdf","description":"Generated PDF digest."},{"path":"<workspace>/archive/follow-news/","description":"Saved digest archives."}]}}}
---

# Follow News

## Runtime Declarations

Required binary:
- `python3` - Runs data collection and merge scripts.

Optional binaries:
- `opencli` - Preferred Twitter/X backend in auto mode, required for Xiaoyuzhou metadata discovery, and the documented supported Xiaoyuzhou transcript path.
- `mail` - msmtp-based mail command for email delivery.
- `msmtp` - SMTP transport used by `mail`.
- `gog` - Gmail CLI fallback for email delivery.
- `gh` - GitHub CLI fallback for repository auth.
- `openssl` - GitHub App JWT signing fallback.
- `weasyprint` - PDF rendering backend.
- `yt-dlp` - YouTube podcast metadata and transcript backend.

Environment variables:

| Name | Required | Description |
| --- | --- | --- |
| `TWITTER_API_BACKEND` | No | Twitter backend: `auto`, `opencli`, `getxapi`, `twitterapiio`, or `official`. Default: `auto`; auto tries OpenCLI first. |
| `OPENCLI_BIN` | No | Optional path to the OpenCLI executable for Twitter/X and Xiaoyuzhou podcast sources. Used when OpenCLI is not available on PATH. |
| `OPENCLI_MAX_WORKERS` | No | Optional OpenCLI concurrency limit. Defaults to 10. |
| `OPENCLI_CLOSE_TABS_AFTER_RUN` | No | Close OpenCLI-created X/Twitter tabs after fetch when set to 1. Default: 1. |
| `OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN` | No | Close OpenCLI-created Chrome automation windows on macOS when set to 1. Default: 1. |
| `GETX_API_KEY` | No | GetXAPI key for Twitter/X fallback. |
| `X_BEARER_TOKEN` | No | Twitter/X API bearer token for KOL monitoring. |
| `TWITTERAPI_IO_KEY` | No | twitterapi.io API key for KOL monitoring. |
| `TAVILY_API_KEY` | No | Tavily Search API key. |
| `WEB_SEARCH_BACKEND` | No | Web search backend: `auto`, `brave`, or `tavily`. |
| `BRAVE_API_KEYS` | No | Brave Search API keys, comma-separated for rotation. |
| `BRAVE_API_KEY` | No | Brave Search API key, single key fallback. |
| `GITHUB_TOKEN` | No | GitHub token for higher API rate limits. |
| `GH_APP_ID` | No | GitHub App ID for automatic installation token generation. |
| `GH_APP_INSTALL_ID` | No | GitHub App Installation ID for automatic token generation. |
| `GH_APP_KEY_FILE` | No | Path to GitHub App private key PEM file. |
| `YTDLP_BIN` | No | Optional path to the `yt-dlp` executable for YouTube podcast metadata and transcript fetching. |

File access:

| Mode | Path | Purpose |
| --- | --- | --- |
| Read | `config/defaults/` | Default source and topic configurations. |
| Read | `references/` | Prompt templates and output templates. |
| Read | `scripts/` | Python pipeline scripts. |
| Read | `<workspace>/archive/follow-news/` | Previous digests for deduplication. |
| Write | `/tmp/td-*.json` | Temporary pipeline intermediate outputs. |
| Write | `/tmp/td-email.html` | Temporary email HTML body. |
| Write | `/tmp/td-digest.pdf` | Generated PDF digest. |
| Write | `<workspace>/archive/follow-news/` | Saved digest archives. |

## Execution Routing Policy

Use one of the following paths according to user intent:

1. **Default / on-demand digest**
   - When user asks for a digest, report, or latest news aggregation.
   - Run `run-pipeline.py` first, then render with the requested template.

2. **Configuration check**
   - When user asks about setup issues, source additions, or broken config.
   - Run `validate-config.py` before any long pipeline run.

3. **Single-source fallback**
   - When full pipeline has an obvious source failure and user asks for partial results.
   - Run only the requested source fetcher (e.g. `fetch-rss.py`, `fetch-web.py`, `fetch-github.py`, `fetch-podcast.py`).

4. **Health / troubleshooting mode**
   - When user reports errors, empty output, or stale data.
   - Run: config validation -> targeted 1h smoke fetch -> pipeline with verbose logs.

Priority rule:
- Operational/config queries take precedence over full news generation.
- When a source fails, keep the run result transparent: explicit success/failure source count and failure reason list.

Automated tech news digest system with unified data source model, internal ranking pipeline, and template-based output generation.

## Quick Start

1. **Configuration Setup**: Default configs are in `config/defaults/`. Copy to workspace for customization:
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/follow-news-sources.json
   cp config/defaults/topics.json workspace/config/follow-news-topics.json
   ```

2. **Environment Variables**: 
   - `TWITTER_API_BACKEND` - Twitter backend: auto|opencli|getxapi|twitterapiio|official (optional, default: auto)
   - `OPENCLI_BIN` - OpenCLI executable path override for Twitter/X and Xiaoyuzhou podcast sources (optional)
   - `OPENCLI_MAX_WORKERS` - OpenCLI concurrency limit (optional, default: 10)
   - `OPENCLI_CLOSE_TABS_AFTER_RUN` - close OpenCLI-created X/Twitter tabs after fetch (optional, default: 1)
   - `OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN` - close Chrome automation windows opened by OpenCLI on macOS (optional, default: 1)
   - `GETX_API_KEY` - GetXAPI key for Twitter/X fallback (optional)
   - `TWITTERAPI_IO_KEY` - twitterapi.io API key for Twitter/X fallback (optional)
   - `X_BEARER_TOKEN` - Twitter/X official API bearer token for final fallback (optional)
   - `TAVILY_API_KEY` - Tavily Search API key, alternative to Brave (optional)
   - `WEB_SEARCH_BACKEND` - Web search backend: auto|brave|tavily (optional, default: auto)
   - `BRAVE_API_KEYS` - Brave Search API keys, comma-separated for rotation (optional)
   - `BRAVE_API_KEY` - Single Brave key fallback (optional)
   - `GITHUB_TOKEN` - GitHub personal access token (optional, improves rate limits)
   - `YTDLP_BIN` - yt-dlp executable path override for YouTube podcast metadata and transcripts (optional)

   OpenCLI is the preferred Twitter/X backend in `auto` mode. In OpenClaw environments where `jackwener/opencli` is installed, the agent should use that skill to validate `opencli doctor`, browser bridge state, and X login before asking for API keys.

   To use the OpenCLI backend, the user must install the OpenCLI executable and expose it on `PATH`, or set `OPENCLI_BIN` to its absolute path. OpenClaw users should also install the `jackwener/opencli` Skill so the agent can run `opencli doctor` and diagnose browser bridge or X login-state issues. OpenCLI requests default to 10 workers (`OPENCLI_MAX_WORKERS=10`). The fetcher closes X/Twitter tabs created during an OpenCLI run by default (`OPENCLI_CLOSE_TABS_AFTER_RUN=1`) and closes Chrome automation windows opened by OpenCLI on macOS (`OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN=1`) while preserving tabs and windows that existed before the run.

   Xiaoyuzhou podcast metadata discovery uses OpenCLI. The user must install, configure, and authenticate OpenCLI for Xiaoyuzhou metadata discovery. Xiaoyuzhou source URLs use `https://www.xiaoyuzhoufm.com/podcast/<podcast_id>` with `platform: "xiaoyuzhou"`. Xiaoyuzhou metadata discovery has no direct API or HTML fallback. For transcripts, backend `auto`/`opencli` uses OpenCLI for Xiaoyuzhou episodes. The `opencli` transcript backend is only valid for Xiaoyuzhou sources.

3. **Generate Digest**:
   ```bash
   # Unified pipeline (recommended) - runs all 7 source layers in parallel + merge
   python3 scripts/run-pipeline.py \
     --defaults config/defaults \
     --config workspace/config \
     --hours 24 --freshness pd \
     --archive-dir workspace/archive/follow-news/ \
     --output /tmp/td-merged.json --verbose --force
   ```

4. **Use Templates**: Apply Discord, email, or PDF templates to merged output

## Configuration Files

### `sources.json` - Unified Data Sources
```json
{
  "sources": [
    {
      "id": "openai-rss",
      "type": "rss",
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "ai-agent"],
      "note": "Official OpenAI updates"
    },
    {
      "id": "sama-twitter",
      "type": "twitter",
      "name": "Sam Altman",
      "handle": "sama",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "frontier-tech"],
      "note": "OpenAI CEO"
    },
    {
      "id": "training-data-podcast",
      "type": "podcast",
      "name": "Training Data",
      "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8",
      "platform": "youtube",
      "enabled": true,
      "priority": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": true,
        "backend": "yt-dlp",
        "languages": ["en", "zh", "zh-Hans"]
      },
      "note": "YouTube podcast playlist with optional transcript enrichment"
    },
    {
      "id": "xiaoyuzhou-example",
      "type": "podcast",
      "name": "Xiaoyuzhou Example",
      "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
      "platform": "xiaoyuzhou",
      "enabled": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": true,
        "backend": "opencli",
        "languages": ["zh"]
      },
      "note": "Xiaoyuzhou podcast using OpenCLI for metadata and transcripts"
    }
  ]
}
```

### `topics.json` - Enhanced Topic Definitions
```json
{
  "topics": [
    {
      "id": "llm",
      "emoji": "🧠",
      "label": "LLM / Large Models",
      "description": "Large Language Models, foundation models, breakthroughs",
      "search": {
        "queries": ["LLM latest news", "large language model breakthroughs"],
        "must_include": ["LLM", "large language model", "foundation model"],
        "exclude": ["tutorial", "beginner guide"]
      },
      "display": {
        "max_items": 8,
        "style": "detailed"
      }
    }
  ]
}
```

## Scripts Pipeline

### `run-pipeline.py` - Unified Pipeline (Recommended)
```bash
python3 scripts/run-pipeline.py \
  --defaults config/defaults [--config CONFIG_DIR] \
  --hours 24 --freshness pd \
  --archive-dir workspace/archive/follow-news/ \
  --output /tmp/td-merged.json --verbose --force
```
- **Features**: Runs all 7 fetch steps in parallel, then merges, ranks, and deduplicates articles
- **Output**: Final merged JSON ready for report generation (~30s total)
- **Metadata**: Saves per-step timing and counts to `*.meta.json`
- **GitHub Auth**: Auto-generates GitHub App token if `$GITHUB_TOKEN` not set
- **Fallback**: If this fails, run individual scripts below

### Global execution constraints

- Concurrency defaults: use `OPENCLI_MAX_WORKERS=10` unless explicitly overridden.
- Retry policy: use exponential backoff + jitter where scripts support it; prefer shorter windows (`--hours`) for smoke checks before full-window runs.
- Failure behavior: mark partial completion explicitly (for example, sources succeeded/failed count and list).
- Rate-limited or flaky sources: pause and serialize before retrying.
- Output stability: keep report ordering deterministic so repeated runs produce stable section ordering.

### Individual Scripts (Fallback)

#### `fetch-rss.py` - RSS Feed Fetcher
```bash
python3 scripts/fetch-rss.py [--defaults DIR] [--config DIR] [--hours 24] [--output FILE] [--verbose]
```
- Parallel fetching (10 workers), retry with backoff, feedparser + regex fallback
- Timeout: 30s per feed, ETag/Last-Modified caching

#### `fetch-twitter.py` - Twitter/X KOL Monitor
```bash
python3 scripts/fetch-twitter.py [--defaults DIR] [--config DIR] [--hours 24] [--output FILE] [--backend auto|opencli|getxapi|twitterapiio|official]
```
- Backend auto-detection: tries OpenCLI first, then GetXAPI, twitterapi.io, and official X API v2
- Rate limit handling, engagement metrics, retry with backoff

#### `fetch-web.py` - Web Search Engine
```bash
python3 scripts/fetch-web.py [--defaults DIR] [--config DIR] [--freshness pd] [--output FILE]
```
- Auto-detects Brave API rate limit: paid plans → parallel queries, free → sequential
- Without Tavily or Brave credentials, the web search layer returns no articles and the pipeline continues with other sources

#### `fetch-github.py` - GitHub Releases Monitor
```bash
python3 scripts/fetch-github.py [--defaults DIR] [--config DIR] [--hours 24] [--output FILE]
```
- Parallel fetching (10 workers), 30s timeout
- Auth priority: `$GITHUB_TOKEN` → GitHub App auto-generate → `gh` CLI → unauthenticated (60 req/hr)


#### `fetch-github.py --trending` - GitHub Trending Repos
```bash
python3 scripts/fetch-github.py --trending [--hours 24] [--output FILE] [--verbose]
```
- Searches GitHub API for trending repos across supported trending topics (`llm`, `ai-agent`, `frontier-tech`)
- Internal ranking: base 5 + daily_stars_est / 10, max 15

#### `fetch-reddit.py` - Reddit Posts Fetcher
```bash
python3 scripts/fetch-reddit.py [--defaults DIR] [--config DIR] [--hours 24] [--output FILE]
```
- Parallel fetching (4 workers), public JSON API (no auth required)
- 8 subreddits with internal ranking filters

#### `fetch-podcast.py` - Podcast, YouTube, and Xiaoyuzhou Fetcher
```bash
python3 scripts/fetch-podcast.py [--defaults DIR] [--config DIR] [--hours 24] [--output FILE] [--verbose]
```
- Loads custom `type: "podcast"` sources from the unified source config.
- Supports RSS podcast feeds without extra tools.
- Supports YouTube playlists/channels via `platform: "youtube"` when `yt-dlp` is available.
- YouTube metadata and transcript fetching require `yt-dlp`; set `YTDLP_BIN` when it is not available on `PATH`.
- Supports Xiaoyuzhou podcasts via `platform: "xiaoyuzhou"` and URLs like `https://www.xiaoyuzhoufm.com/podcast/<podcast_id>`.
- Xiaoyuzhou metadata discovery requires installed, configured, and authenticated OpenCLI; set `OPENCLI_BIN` when it is not available on `PATH`.
- Transcript backends: `auto`, `yt-dlp`, or `opencli`; missing `yt-dlp` fails only that YouTube podcast source instead of the full pipeline.
- Xiaoyuzhou metadata discovery has no direct API or HTML fallback. For transcripts, backend `auto`/`opencli` uses OpenCLI for Xiaoyuzhou episodes. The `opencli` transcript backend is rejected for non-Xiaoyuzhou podcast sources.

#### `enrich-articles.py` - Article Full-Text Enrichment
```bash
python3 scripts/enrich-articles.py --input merged.json --output enriched.json [--min-score 10] [--max-articles 15] [--verbose]
```
- Fetches full article text for high-priority articles
- Cloudflare Markdown for Agents (preferred) → HTML extraction (fallback) → Skip (paywalled/social)
- Blog domain whitelist with a lower internal ranking threshold
- Parallel fetching (5 workers, 10s timeout)

#### `merge-sources.py` - Ranking & Deduplication
```bash
python3 scripts/merge-sources.py --rss FILE --twitter FILE --web FILE --github FILE --trending FILE --reddit FILE --podcast FILE
```
- Internal ranking, title similarity dedup (85%), previous digest penalty
- Output: topic-grouped articles in priority order

#### `validate-config.py` - Configuration Validator
```bash
python3 scripts/validate-config.py [--defaults DIR] [--config DIR] [--verbose]
```
- JSON schema validation, topic reference checks, duplicate ID detection

#### `generate-pdf.py` - PDF Report Generator
```bash
python3 scripts/generate-pdf.py --input report.md --output digest.pdf [--verbose]
```
- Converts markdown digest to styled A4 PDF with Chinese typography (Noto Sans CJK SC)
- Emoji icons, page headers/footers, blue accent theme. Requires `weasyprint`.

#### `sanitize-html.py` - Safe HTML Email Converter
```bash
python3 scripts/sanitize-html.py --input report.md --output email.html [--verbose]
```
- Converts markdown to XSS-safe HTML email with inline CSS
- URL whitelist (http/https only), HTML-escaped text content

#### `source-health.py` - Source Health Monitor
```bash
python3 scripts/source-health.py --rss FILE --twitter FILE --github FILE --reddit FILE --web FILE [--verbose]
```
- Tracks per-source success/failure history over 7 days
- Reports unhealthy sources (>50% failure rate)

#### `summarize-merged.py` - Merged Data Summary
```bash
python3 scripts/summarize-merged.py --input merged.json [--top N] [--topic TOPIC]
```
- Human-readable summary of merged data for LLM consumption
- Shows top articles per topic with source metrics

## User Customization

### Workspace Configuration Override
Place custom configs in `workspace/config/` to override defaults:

- **Sources**: Append new sources, disable defaults with `"enabled": false`
- **Topics**: Override topic definitions, search queries, display settings
- **Merge Logic**: 
  - Sources with same `id` → user version takes precedence
  - Sources with new `id` → appended to defaults
  - Topics with same `id` → user version completely replaces default

### Example Workspace Override
```json
// workspace/config/follow-news-sources.json
{
  "sources": [
    {
      "id": "simonwillison-rss",
      "enabled": false,
      "note": "Disabled: too noisy for my use case"
    },
    {
      "id": "my-custom-blog", 
      "type": "rss",
      "name": "My Custom Tech Blog",
      "url": "https://myblog.com/rss",
      "enabled": true,
      "priority": true,
      "topics": ["frontier-tech"]
    }
  ]
}
```

## User-facing output contract

- Keep outputs concise and structured for non-technical readers.
- Never expose internal implementation details (raw commands, file paths, env var names, rate-limit internals, cache state, retry counters).
- Preserve source links for every item.
- Keep sectioned numbering stable and clear so users can reference items quickly.
- In degraded mode, show scope explicitly (for example: `2/7 sources available`) and avoid claiming completeness.

## Templates & Output

### Summary References
- Twitter/X and KOL summaries: `references/summarize-tweets.md`
- Podcast remixes: `references/summarize-podcast.md`
- Chinese and bilingual translation: `references/translate.md`

### Discord Template (`references/templates/discord.md`)
- Bullet list format with link suppression (`<link>`)
- Mobile-optimized, emoji headers
- 2000 character limit awareness

### Email Template (`references/templates/email.md`) 
- Rich metadata, technical stats, archive links
- Executive summary, top articles section
- HTML-compatible formatting

### PDF Template (`references/templates/pdf.md`)
- A4 layout with Noto Sans CJK SC font for Chinese support
- Emoji icons, page headers/footers with page numbers
- Generated via `scripts/generate-pdf.py` (requires `weasyprint`)

## Default Sources (163 total)

- **RSS Feeds (65)**: AI labs, engineering blogs, founder/operator writing, Chinese tech media
- **Twitter/X KOLs (61)**: AI researchers, builder accounts, product operators, technology commentators
- **GitHub Repos (23)**: Major open-source projects (LangChain, vLLM, DeepSeek, Llama, etc.)
- **Reddit (8)**: r/MachineLearning, r/LocalLLaMA, r/OpenAI, r/ExperiencedDevs, etc.
- **Default report topics (6)**: `llm`, `ai-agent`, `kol`, `hackernews`, `frontier-tech`, `podcast`
- **Web Search (4 query-backed topics)**: `llm`, `ai-agent`, `kol`, `frontier-tech`
- **Podcast (custom)**: RSS podcast feeds, YouTube podcast playlists/channels, and Xiaoyuzhou podcasts, with optional transcript enrichment

All sources pre-configured with appropriate topic tags and priority levels.

## Dependencies

```bash
pip install -r requirements.txt
```

**Optional but Recommended**:
- `feedparser>=6.0.0` - Better RSS parsing (fallback to regex if unavailable)
- `jsonschema>=4.0.0` - Configuration validation
- `yt-dlp` - Optional runtime binary for YouTube podcast metadata and transcripts. Set `YTDLP_BIN` to override lookup.
- `opencli` - Required for Xiaoyuzhou metadata discovery and the documented supported Xiaoyuzhou transcript path. Install, configure, and authenticate it for Xiaoyuzhou; set `OPENCLI_BIN` to override lookup.

**All scripts work with Python 3.8+ standard library only.**

## Monitoring & Operations

### Health Checks
```bash
# Validate configuration
python3 scripts/validate-config.py --verbose

# Test RSS feeds
python3 scripts/fetch-rss.py --hours 1 --verbose

# Check Twitter API
python3 scripts/fetch-twitter.py --hours 1 --verbose
```

### Minimum sanity checklist (before long runs)

1. `python3 scripts/validate-config.py --verbose`
2. `python3 scripts/fetch-rss.py --hours 1 --verbose`
3. `python3 scripts/run-pipeline.py --defaults config/defaults --hours 24 --freshness pd --archive-dir workspace/archive/follow-news/ --output /tmp/td-merged.json --verbose`

If all pass, run the default 24h pipeline, or pass a longer `--hours` window when the requested digest explicitly needs historical coverage.

### Archive Management
- Digests automatically archived to `<workspace>/archive/follow-news/`
- Previous digest titles used for duplicate detection
- Old archives cleaned automatically (90+ days)

### Error Handling
- **Network Failures**: Retry with exponential backoff
- **Rate Limits**: Automatic retry with appropriate delays
- **Invalid Content**: Graceful degradation, detailed logging
- **Configuration Errors**: Schema validation with helpful messages

### Error playbook

- `validate-config.py` fails:
  - Return actionable schema errors and stop pipeline execution.
  - Ask user to patch config first.
- Empty result from one source fetcher:
  - Continue with other sources.
  - Continue with a `partial` status and surface affected source.
- Pipeline succeeds but output is missing expected sections:
  - Re-run source fetch for the missing category with narrower windows (e.g. `--hours 24`) and compare.
- Repeated 429 / timeout:
  - Serialize retries, increase delay, and rerun narrowed.
- Single upstream provider failure:
  - Produce best-effort digest from healthy sources and expose degraded scope in output.

## API Keys & Environment

Set in `~/.zshenv` or similar:
```bash
# Twitter (at least one required for Twitter source)
export TWITTERAPI_IO_KEY="your_key"        # twitterapi.io key (preferred)
export X_BEARER_TOKEN="your_bearer_token"  # Official X API v2 (fallback)
export TWITTER_API_BACKEND="auto"          # auto|twitterapiio|official (default: auto)

# Web Search (optional, enables web search layer)
export WEB_SEARCH_BACKEND="auto"          # auto|brave|tavily (default: auto)
export TAVILY_API_KEY="tvly-xxx"           # Tavily Search API (free 1000/mo)

# Brave Search (alternative)
export BRAVE_API_KEYS="key1,key2,key3"     # Multiple keys, comma-separated rotation
export BRAVE_API_KEY="key1"                # Single key fallback
export BRAVE_PLAN="free"                   # Override rate limit detection: free|pro

# GitHub (optional, improves rate limits)
export GITHUB_TOKEN="ghp_xxx"              # PAT (simplest)
export GH_APP_ID="12345"                   # Or use GitHub App for auto-token
export GH_APP_INSTALL_ID="67890"
export GH_APP_KEY_FILE="/path/to/key.pem"

# Podcast transcripts (optional)
export YTDLP_BIN="/path/to/yt-dlp"          # Optional; defaults to yt-dlp on PATH
```

- **Twitter**: OpenCLI is preferred in `auto` mode; API backends fallback in this order: `GETX_API_KEY`, `TWITTERAPI_IO_KEY`, `X_BEARER_TOKEN`
- **Web Search**: Tavily (preferred in auto mode) or Brave. Without a configured search API key, the web search layer is skipped while the rest of the pipeline continues.
- **GitHub**: Auto-generates token from GitHub App if PAT not set; unauthenticated fallback (60 req/hr)
- **Reddit**: No API key needed (uses public JSON API)
- **Podcast**: RSS podcast feeds require no extra binary. YouTube podcast sources use `yt-dlp` for metadata and optional transcript fetching; set `YTDLP_BIN` if needed. Xiaoyuzhou podcast metadata discovery uses OpenCLI with `platform: "xiaoyuzhou"`; set `OPENCLI_BIN` if needed. Xiaoyuzhou metadata discovery has no direct API or HTML fallback. For transcripts, backend `auto`/`opencli` uses OpenCLI for Xiaoyuzhou episodes; non-Xiaoyuzhou podcast sources cannot use `opencli`.

## Cron / Scheduled Task Integration

### OpenClaw Cron (Recommended)

The cron prompt should **NOT** hardcode the pipeline steps. Instead, reference `references/digest-prompt.md` and only pass configuration parameters. This ensures the pipeline logic stays in the skill repo and is consistent across all installations.

#### Daily Digest Cron Prompt
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a daily digest.

Replace placeholders with:
- MODE = daily
- TIME_WINDOW = past 1-2 days
- FRESHNESS = pd
- RSS_HOURS = 48
- ITEMS_PER_SECTION = 3-5
- ENRICH = true
- BLOG_PICKS_COUNT = 3
- EXTRA_SECTIONS = (none)
- SUBJECT = Daily Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### Weekly Digest Cron Prompt
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a weekly digest.

Replace placeholders with:
- MODE = weekly
- TIME_WINDOW = past 7 days
- FRESHNESS = pw
- RSS_HOURS = 168
- ITEMS_PER_SECTION = 10-15
- ENRICH = true
- BLOG_PICKS_COUNT = 3-5
- EXTRA_SECTIONS = 📊 Weekly Trend Summary (2-3 sentences summarizing macro trends)
- SUBJECT = Weekly Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### Why This Pattern?
- **Single source of truth**: Pipeline logic lives in `digest-prompt.md`, not scattered across cron configs
- **Portable**: Same skill on different OpenClaw instances, just change paths and channel IDs
- **Maintainable**: Update the skill → all cron jobs pick up changes automatically
- **Anti-pattern**: Do NOT copy pipeline steps into the cron prompt — it will drift out of sync

#### Multi-Channel Delivery Limitation
OpenClaw enforces **cross-provider isolation**: a single session can only send messages to one provider (e.g., Discord OR Telegram, not both). If you need to deliver digests to multiple platforms, create **separate cron jobs** for each provider:

```
# Job 1: Discord + Email
- DISCORD_CHANNEL_ID = <your-discord-channel-id>
- EMAIL = user@example.com
- TEMPLATE = discord

# Job 2: Telegram DM
- DISCORD_CHANNEL_ID = (none)
- EMAIL = (none)
- TEMPLATE = telegram
```
Replace `DISCORD_CHANNEL_ID` delivery with the target platform's delivery in the second job's prompt.

This is a security feature, not a bug — it prevents accidental cross-context data leakage.

## Security Notes

### Execution Model
This skill uses a **prompt template pattern**: the agent reads `digest-prompt.md` and follows its instructions. This is the standard OpenClaw skill execution model — the agent interprets structured instructions from skill-provided files. All instructions are shipped with the skill bundle and can be audited before installation.

### Network Access
The Python scripts and configured helper CLIs make outbound requests to:
- RSS feed URLs and podcast feed URLs (configured in `follow-news-sources.json`)
- Twitter/X API (`api.x.com` or `api.twitterapi.io`)
- Brave Search API (`api.search.brave.com`)
- Tavily Search API (`api.tavily.com`)
- GitHub API (`api.github.com`)
- Reddit JSON API (`reddit.com`)
- YouTube URLs for `platform: "youtube"` podcast sources, resolved through `yt-dlp`
- OpenCLI browser/session traffic for Twitter/X and Xiaoyuzhou sources when the OpenCLI backend is selected

API keys are read from environment variables declared in the skill metadata. OpenCLI may reuse authenticated browser sessions managed by the user's local browser/OpenCLI setup for Twitter/X and Xiaoyuzhou.

### Shell Safety
Email delivery uses `send-email.py` which constructs proper MIME multipart messages with HTML body + optional PDF attachment. Subject formats are hardcoded (`Daily Tech Digest - YYYY-MM-DD`). PDF generation uses `generate-pdf.py` via `weasyprint`. The prompt template explicitly prohibits interpolating untrusted content (article titles, tweet text, etc.) into shell arguments. Email addresses and subjects must be static placeholder values only.

### File Access
Scripts read from `config/` and write to `workspace/archive/`. No files outside the workspace are accessed.

## Support & Troubleshooting

### Common Issues
1. **RSS feeds failing**: Check network connectivity, use `--verbose` for details
2. **Twitter rate limits**: Reduce sources or increase interval
3. **Configuration errors**: Run `validate-config.py` for specific issues
4. **No articles found**: Check time window (`--hours`) and source enablement

### Debug Mode
All scripts support `--verbose` flag for detailed logging and troubleshooting.

### Performance Tuning
- **Parallel Workers**: Adjust `MAX_WORKERS` in scripts for your system
- **Timeout Settings**: Increase `TIMEOUT` for slow networks
- **Article Limits**: Adjust `MAX_ARTICLES_PER_FEED` based on needs
## Security Considerations

### Shell Execution
The digest prompt instructs agents to run Python scripts via shell commands. All script paths and arguments are skill-defined constants — no user input is interpolated into commands. Two scripts use `subprocess`:
- `run-pipeline.py` orchestrates child fetch scripts (all within `scripts/` directory)
- `fetch-github.py` has two subprocess calls:
  1. `openssl dgst -sha256 -sign` for JWT signing (only if `GH_APP_*` env vars are set — signs a self-constructed JWT payload, no user content involved)
  2. `gh auth token` CLI fallback (only if `gh` is installed — reads from gh's own credential store)

No user-supplied or fetched content is ever interpolated into subprocess arguments. Email delivery uses `send-email.py` which builds MIME messages programmatically — no shell interpolation. PDF generation uses `generate-pdf.py` via `weasyprint`. Email subjects are static format strings only — never constructed from fetched data.

### Credential & File Access
Scripts do **not** directly read `~/.config/`, `~/.ssh/`, or any credential files. API tokens used directly by the scripts are read from environment variables declared in the skill metadata. OpenCLI-backed Twitter/X and Xiaoyuzhou sources delegate authentication to the user's configured OpenCLI/browser session. The GitHub auth cascade is:
1. `$GITHUB_TOKEN` env var (you control what to provide)
2. GitHub App token generation (only if you set `GH_APP_ID`, `GH_APP_INSTALL_ID`, and `GH_APP_KEY_FILE` — uses inline JWT signing via `openssl` CLI, no external scripts involved)
3. `gh auth token` CLI (delegates to gh's own secure credential store)
4. Unauthenticated (60 req/hr, safe fallback)

If you prefer no automatic credential discovery, simply set `$GITHUB_TOKEN` and the script will use it directly without attempting steps 2-3.

### Dependency Installation
This skill does **not** install any packages. `requirements.txt` lists optional dependencies (`feedparser`, `jsonschema`) for reference only. All scripts work with Python 3.8+ standard library. Users should install optional deps in a virtualenv if desired — the skill never runs `pip install`.

### Input Sanitization
- URL resolution rejects non-HTTP(S) schemes (javascript:, data:, etc.)
- RSS fallback parsing uses simple, non-backtracking regex patterns (no ReDoS risk)
- All fetched content is treated as untrusted data for display only

### Network Access
Scripts and helper CLIs make outbound HTTP requests to configured RSS feeds, podcast feeds, Twitter API, GitHub API, Reddit JSON API, Brave Search API, Tavily Search API, YouTube URLs handled by `yt-dlp`, and OpenCLI browser/session traffic for Twitter/X and Xiaoyuzhou sources. No inbound connections or listeners are created.
