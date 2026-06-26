---
name: aegis
description: "Automated Emergency Geopolitical Intelligence System — real-time threat monitoring and safety alerts for civilians in conflict zones. Use when: (1) setting up warzone/crisis safety monitoring for a location, (2) user asks about security situation or threat level, (3) configuring emergency alert delivery, (4) generating security briefings, (5) emergency preparedness planning."
homepage: "https://github.com/PleaseChooseUsername/aegis-openclaw-skill"
source: "https://github.com/PleaseChooseUsername/aegis-openclaw-skill"
requires:
  binaries:
    - curl
    - python3
  env: []
  optional_env:
    - AEGIS_DATA_DIR
    - AEGIS_BOT_TOKEN
    - AEGIS_CHANNEL_ID
  optional_config:
    - "api_keys.newsapi"
---

# AEGIS — Automated Emergency Geopolitical Intelligence System

Civilian-first threat intelligence for conflict zones. Monitors 28+ sources (RSS, web, APIs, OSINT aggregators) with two delivery modes:

1. **CRITICAL-only scan** (every 15 min) — Posts ONLY for verified, active emergencies (3-phase validation)
2. **Morning/evening briefings** (8am + 8pm local) — Agent-powered situation reports with actionable guidance

Powered by **World Monitor** (real-time geopolitical intelligence API) and **LiveUAMap** (verified OSINT event feed), supplemented by government sources, major news agencies, and aviation data.

**Not a panic tool.** Calm, factual, action-oriented. Follows official government guidance.

## Requirements

- **curl** — used for all HTTP fetching (RSS, web, APIs). Pre-installed on most systems.
- **python3** (3.8+) — runs all scripts. No extra pip packages needed (stdlib only).
- **No API keys required** for baseline 23 sources. Optional: NewsAPI free tier for expanded coverage.
- **LLM (optional)** — Improves CRITICAL alert accuracy via semantic verification. See [LLM Verification](#llm-verification) below.

## Quick Start

### First-time setup (interactive)
```bash
python3 scripts/aegis_onboard.py
```
Creates `~/.openclaw/aegis-config.json` with location, language, and alert preferences.

### Manual config
Create `~/.openclaw/aegis-config.json`:
```json
{
  "location": {
    "country": "AE",
    "country_code": "AE",
    "city": "Dubai",
    "timezone": "Asia/Dubai"
  },
  "language": "en",
  "alerts": { "critical_instant": true, "high_batch_minutes": 30, "medium_digest_hours": 6 },
  "briefings": { "morning": "07:00", "evening": "22:00" },
  "scan_interval_minutes": 15,
  "api_keys": {}
}
```

### Run a scan
```bash
python3 scripts/aegis_scanner.py
```

### Set up cron monitoring
```
# CRITICAL-only scan (every 15 min) — posts ONLY for imminent threats
openclaw cron add --every 15m --message "Run AEGIS scan: python3 <skill-dir>/scripts/aegis_cron.py"

# Morning briefing (adjust time for user timezone — example: 4:00 UTC = 8:00 Dubai)
openclaw cron add --cron "0 4 * * *" --tz UTC --message "Run AEGIS morning briefing: python3 <skill-dir>/scripts/aegis_briefing.py morning"

# Evening briefing (example: 16:00 UTC = 20:00 Dubai)
openclaw cron add --cron "0 16 * * *" --tz UTC --message "Run AEGIS evening briefing: python3 <skill-dir>/scripts/aegis_briefing.py evening"

# Optional: Live feed (every 5 min) — for high-tempo situations only, disable during calm periods
openclaw cron add --cron "*/5 * * * *" --message "Run AEGIS live feed: python3 <skill-dir>/scripts/aegis_feed.py" --disabled
```

### Optional: Telegram channel delivery
Set environment variables for direct channel posting:
- `AEGIS_BOT_TOKEN` — Telegram bot token (from BotFather)
- `AEGIS_CHANNEL_ID` — Telegram channel ID

Or add to config:
```json
{
  "telegram": {
    "bot_token": "your-token",
    "channel_id": "-100xxxxxxxxxx"
  }
}
```

## Data Storage

AEGIS stores scan state in `~/.openclaw/aegis-data/` (or `$AEGIS_DATA_DIR` if set):
- `seen_hashes.json` — content dedup hashes (48h rolling window for scans, 6h for feed)
- `pending_alerts.json` — alerts awaiting batch delivery
- `scan_log.json` — recent scan results
- `last_scan.json` — most recent scan output (used by briefings)
- `feed_state.json` — live feed dedup state and last post timestamp
- `last_alert_time.json` — channel post cooldown tracker
- `scan_history.log` — rolling log of scan results (last 500 entries)

All files are local JSON. No data is sent to external servers beyond the listed sources in `source-registry.json`.

## Sources (30+)

All sources are defined in `references/source-registry.json`. The scanner **only** contacts URLs listed there.

| Tier | Type | Count | Examples |
|------|------|-------|----------|
| 0 🏛️ | Government & Emergency | 7 | GDACS, NCEMA, UAE MoD, US/UK embassies, MOFAIC |
| 1 📰 | Major News & RSS | 11 | Al Jazeera, Reuters, BBC, Gulf Business, Emirates 24/7, Gulf Today |
| 2 🔍 | OSINT & Conflict Mapping | 5 | World Monitor API, LiveUAMap (3 regions + feed) |
| 2 ✈️ | Aviation | 2 | FAA NOTAMs (DXB, AUH) |
| 3 📋 | Analysis | 2 | Crisis Group, War on the Rocks |
| 4 🔑 | API-Enhanced (optional) | 1+ | NewsAPI (free tier), GDELT |

### Outbound connections

The scanner contacts **only**:
1. URLs listed in `references/source-registry.json` (RSS feeds, news sites, government pages)
2. `https://world-monitor.com/api/signal-markers` (World Monitor public API)
3. LiveUAMap regional pages (e.g., `https://iran.liveuamap.com`)
4. Telegram Bot API (`https://api.telegram.org/bot.../sendMessage`) — only if channel delivery is configured

No telemetry. No analytics. No phone-home.

## Alert Classification

| Level | Meaning | Trigger |
|-------|---------|---------|
| 🔴 CRITICAL | Immediate physical danger **in user's country** | Missiles inbound, sirens, shelter orders, airport shutdown, CBRN |
| 🟠 HIGH | Significant regional threat | Attacks on neighbors, strait disrupted, flights cancelled, general "UAE hit by" context |
| ℹ️ MEDIUM | Situational awareness | Regional strikes, diplomacy, oil prices, sanctions |

CRITICAL is reserved for "act now, your life may be in danger." Regional developments and background context are HIGH.

### CRITICAL Validation Pipeline (v3.2)

CRITICAL alerts go through 3-phase validation to eliminate false positives:

1. **Regex pre-filter** — Tightened patterns match only active attacks, sirens, shelter orders
2. **Negative pattern filter** — Disqualifies: past tense ("has been hit"), sports, analysis, speculation, historical context
3. **LLM verification** (optional) — Confirms the item describes an ACTIVE emergency

Additionally:
- **Government trust** — Tier 0 sources (NCEMA, government) bypass LLM verification
- **Source corroboration** — Single source: 4h cooldown; 2+ sources: 1h cooldown
- **Fail-open safety** — If LLM unavailable or disabled, CRITICAL alerts pass through (safety first)

### LLM Verification

LLM verification is **optional** but recommended. It adds a semantic check that catches false positives the regex filters miss (e.g., "cricket match cancelled due to war" triggering CRITICAL).

**Three modes** (configured in `aegis-config.json` under `"llm"`):

| Mode | Provider | Cost | Accuracy | Setup |
|------|----------|------|----------|-------|
| **Local Ollama** | `"ollama"` | Free (runs on your GPU) | Best | Install [Ollama](https://ollama.ai), pull a model |
| **OpenAI-compatible API** | `"openai"` | ~$0.001/verification | Best | Any OpenAI-compatible endpoint (OpenRouter, Together, vLLM, LiteLLM, etc.) |
| **No LLM** | `"none"` | Free | Good (regex + negative patterns only) | No setup needed |

**Without LLM:** AEGIS still works well — the regex pre-filter and negative pattern filter catch most false positives. You may see occasional false CRITICAL alerts that would have been caught by LLM verification.

**Config examples:**

```json
// Local Ollama (recommended if you have a GPU)
"llm": { "enabled": true, "provider": "ollama", "endpoint": "http://localhost:11434", "model": "qwen3:8b" }

// OpenRouter (cheap cloud API)
"llm": { "enabled": true, "provider": "openai", "endpoint": "https://openrouter.ai/api", "model": "meta-llama/llama-3-8b-instruct", "api_key": "sk-or-..." }

// No LLM (regex-only, no external calls)
"llm": { "enabled": false, "provider": "none" }
```

The onboarding wizard (`aegis_onboard.py`) will help you choose during setup.

### Anti-Hoax Protocol
- Tier 0 sources: trusted directly (government/emergency)
- Tier 1+ CRITICAL candidates: must pass LLM semantic verification
- Tier 2+: require corroboration from ≥1 Tier 0-1 source for HIGH
- Social media: excluded entirely
- Extraordinary claims: require ≥3 independent sources

## Briefings

Morning and evening briefings use agent-powered synthesis to create human-readable situation updates:

### Situation Update Format
Each briefing includes:
- **Summary** — What happened in plain English with real numbers
- **Status** — Current safety status (threat level with description)
- **Actions** — 4-6 concrete things a civilian should do right now
- **Daily Impact** — Flights, schools, work, supplies, roads, hospitals
- **Outlook** — What to expect in the next 12-24 hours
- **Sources** — Where to verify and get more info

### Delivery Modes
| Mode | Frequency | Posts on |
|------|-----------|---------|
| **CRITICAL scan** | Every 15 min | Imminent danger only (missiles inbound, shelter orders) |
| **Morning briefing** | Once daily (8am local) | Full situation update with overnight summary |
| **Evening briefing** | Once daily (8pm local) | Full situation update with daytime summary |
| **Live feed** | Every 5 min (optional) | Discrete verified events from LiveUAMap + World Monitor |

### Anti-Spam
- CRITICAL scan: 4-hour cooldown (single source) / 1-hour cooldown (multi-source corroborated)
- Live feed: 5-minute batch interval, max 8 events per post
- Briefings: Agent-powered, pin to channel, once per cycle

## Country Profiles

Each supported country has a profile in `references/country-profiles/`. Profiles contain:
- Emergency contacts and hotlines
- Neighboring countries and regions of interest (for source filtering)
- Local threat keyword patterns
- Shelter and evacuation info

Currently available: **UAE** (`uae.json`). To add a country: copy `_template.json`, fill in details, submit PR.

## Preparedness Resources

See `references/preparedness/` for:
- `go-bag-checklist.md` — What to pack for emergency evacuation
- `communication-plan.md` — Family communication plan
- `shelter-guidance.md` — Shelter-in-place protocol
- `evacuation-guidance.md` — Routes, transport, embassy registration

## Configuration Reference

See `references/config-reference.md` for all configuration options.

## Cost

- **Sources (30+):** Free (RSS + web scraping + public APIs)
- **LLM verification (optional):** Free with Ollama; ~$0.001/check with cloud APIs; or disabled (regex-only)
- **Briefings:** Free with Copilot or local models; ~$0.03-0.05/day with commercial LLMs
- **Optional NewsAPI:** Free tier (100 req/day) is sufficient
