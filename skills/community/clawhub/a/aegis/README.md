# AEGIS — Automated Emergency Geopolitical Intelligence System

<div align="center">

**Civilian-first threat intelligence for conflict zones.**

*Know what's happening. Know what to do. Stay safe.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-aegis@3.2.0-orange.svg)](https://clawhub.com)

</div>

---

## What is AEGIS?

AEGIS is an open-source [OpenClaw](https://openclaw.ai) skill that monitors 30+ news and intelligence sources and delivers actionable threat assessments to your Telegram channel.

**Two delivery modes:**

| Mode | Frequency | Purpose |
|------|-----------|---------|
| 🔴 **CRITICAL scan** | Every 15 min | Imminent threats only — missiles inbound, shelter orders, airport shutdown |
| 📋 **Briefings** | 8am + 8pm local | Full situation report with summary, actions, daily impact, outlook |

**Optional:**

| Mode | Frequency | Purpose |
|------|-----------|---------|
| 📡 **Live feed** | Every 5 min | Verified OSINT event stream from LiveUAMap + World Monitor |

### What makes AEGIS different?

- **Civilian-first** — Written for a person in the affected area, not a military analyst
- **Action-oriented** — Every alert tells you what to DO, not just what happened
- **Anti-panic** — Calm, factual, follows official government guidance
- **Anti-hoax** — Multi-source verification. Social media excluded. Tier system for trust.
- **Zero API keys** — All 30+ sources are free (RSS, web scraping, public APIs)
- **Zero dependencies** — Python 3 stdlib only. No pip installs needed.
- **Optional LLM** — Add local Ollama or any OpenAI-compatible API for smarter CRITICAL filtering. Works fine without it.

## Quick Start

### 1. Install via ClawHub
```bash
clawhub install aegis
```

### 2. Run onboarding
```bash
python3 scripts/aegis_onboard.py
```
Creates config with your location, language, and alert preferences.

### 3. Set up cron jobs
```bash
# CRITICAL-only scan (every 15 min)
openclaw cron add --every 15m --message "Run AEGIS scan: python3 <skill-dir>/scripts/aegis_cron.py"

# Morning briefing (8am local — adjust UTC offset)
openclaw cron add --cron "0 4 * * *" --tz UTC --message "Run AEGIS briefing: python3 <skill-dir>/scripts/aegis_briefing.py morning"

# Evening briefing (8pm local)
openclaw cron add --cron "0 16 * * *" --tz UTC --message "Run AEGIS briefing: python3 <skill-dir>/scripts/aegis_briefing.py evening"
```

### 4. Optional: Telegram channel
Set env vars for channel delivery:
```bash
export AEGIS_BOT_TOKEN="your-bot-token"
export AEGIS_CHANNEL_ID="-100xxxxxxxxxx"
```

## Sources (30+)

| Tier | Type | Examples |
|------|------|---------|
| 0 🏛️ | Government | NCEMA, UAE MoD, GDACS, Embassies |
| 1 📰 | News RSS | Al Jazeera, Reuters, BBC, Gulf Business, Emirates 24/7 |
| 2 🔍 | OSINT | **World Monitor API**, **LiveUAMap** (SSR scraping), ACLED |
| 2 ✈️ | Aviation | FAA NOTAMs (DXB, AUH) |
| 3 📋 | Analysis | Crisis Group, War on the Rocks |

### Primary Intelligence Sources

**World Monitor** (`world-monitor.com/api/signal-markers`) — Real-time geopolitical intelligence. 150+ monitored locations with per-location analysis and summaries. Free public API.

**LiveUAMap** (`iran.liveuamap.com`) — Verified OSINT conflict mapping. Discrete event feed extracted from server-rendered HTML. Hundreds of events per page.

## Alert Classification

| Level | Meaning | Channel Post? |
|-------|---------|---------------|
| 🔴 CRITICAL | Immediate danger in your country | ✅ Instant |
| 🟠 HIGH | Significant regional threat | ❌ Morning/evening briefing |
| ℹ️ MEDIUM | Situational awareness | ❌ Morning/evening briefing |

**CRITICAL = "act now."** Everything else waits for the briefing to avoid notification fatigue.

## Situation Update Format

Every briefing answers 5 questions a civilian actually has:

```
📍 SITUATION UPDATE — Dubai, UAE
07 Mar 2026 — 08:00 GST
Status: 🟠 HIGH — Significant ongoing threat

What's happening (2-4 sentences, plain English, real numbers)

🛡️ Current safety status

📋 What you should do:
  → Concrete action 1
  → Concrete action 2
  → ...

🏙️ How this affects daily life:
  ✈️ Flights: ...
  🏫 Schools: ...
  💼 Work: ...
  🛒 Supplies: ...

🔮 Near-term outlook

📞 Emergency: 999 | NCEMA: 800-22-444
AEGIS — Open Source Emergency Intelligence
```

## Architecture

```
aegis_scanner.py    — Core: fetches 30+ sources, classifies threats, deduplicates
aegis_cron.py       — 15-min cron: CRITICAL-only channel posting with cooldown
aegis_feed.py       — 5-min feed: LiveUAMap + World Monitor live event stream
aegis_briefing.py   — Morning/evening: gathers intel for agent-powered synthesis
aegis_channel.py    — Telegram channel publisher (situation, critical, briefing formats)
aegis_onboard.py    — Interactive first-time setup
```

### Data Flow

```
Sources (30+) → Scanner → Classification → Dedup
                                              ↓
                              CRITICAL → Channel + DM (instant)
                              HIGH/MED → Stored for briefing
                                              ↓
                              Briefing cron → Agent synthesis → Channel (pinned)
```

## LLM Verification (Optional)

AEGIS v3.2 adds optional LLM-based CRITICAL alert verification. This catches false positives that regex alone misses (e.g., "cricket cancelled due to war" triggering CRITICAL).

| Mode | Config | Cost | Notes |
|------|--------|------|-------|
| **Local Ollama** | `"provider": "ollama"` | Free | Needs GPU. Best option if available. |
| **OpenAI-compatible** | `"provider": "openai"` | ~$0.001/check | Works with OpenRouter, Together, vLLM, LiteLLM, etc. |
| **No LLM** | `"provider": "none"` | Free | Default. Regex + negative patterns only. Slightly more false positives. |

Add to `aegis-config.json`:
```json
{
  "llm": {
    "enabled": true,
    "provider": "ollama",
    "endpoint": "http://localhost:11434",
    "model": "qwen3:8b"
  }
}
```

**Without LLM, AEGIS still works well.** The regex + negative pattern filter handles most cases. LLM just adds an extra layer of accuracy for CRITICAL alerts.

## Anti-Hoax Protocol

- **Tier 0-1** sources can trigger alerts directly
- **Tier 2+** require corroboration from ≥1 Tier 0-1 source
- **Social media** excluded entirely
- **Extraordinary claims** require ≥3 independent sources

## Preparedness Resources

See `references/preparedness/`:
- `go-bag-checklist.md` — Emergency evacuation packing list
- `communication-plan.md` — Family communication protocol
- `shelter-guidance.md` — Shelter-in-place instructions
- `evacuation-guidance.md` — Routes and embassy registration

## Adding Countries

Copy `references/country-profiles/_template.json`, fill in:
- Emergency contacts and hotlines
- Neighboring countries (for source filtering)
- Local threat keyword patterns (supports multiple languages)

Currently supported: **UAE** (`uae.json`)

## Cost

| Component | Cost |
|-----------|------|
| Sources (30+) | **Free** (RSS, web, public APIs) |
| LLM verification (Ollama) | **Free** (local GPU) |
| LLM verification (OpenRouter) | ~$0.001/check (~$0.10/day at 96 scans) |
| LLM verification (none) | **Free** (regex-only, no LLM needed) |
| OpenClaw briefings (Copilot) | **Free** with GitHub Copilot |
| OpenClaw briefings (commercial) | ~$0.03-0.05/day |
| Optional NewsAPI | Free tier (100 req/day) |

## License

MIT — Use it, fork it, save lives with it.

---

<div align="center">

*Built for people who need to know what's happening — and what to do about it.*

</div>
