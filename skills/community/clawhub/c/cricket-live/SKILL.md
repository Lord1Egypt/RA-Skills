# 🏏 Cricket Live

**Live cricket scores, IPL tracking, and match alerts for OpenClaw.**

Get real-time scores, upcoming schedules, detailed scorecards, and IPL standings — all from your OpenClaw agent. Powered by [CricketData.org](https://cricketdata.org) API (endpoint: `api.cricapi.com`).

---

## ✨ Features

- 🔴 **Live Scores** — All currently live matches with real-time scores, overs, and status
- 📋 **Match Details** — Full scorecards with batting and bowling stats
- 📅 **Upcoming Matches** — Next 7 days of scheduled matches, filterable by team
- ✅ **Recent Results** — Completed matches from the last 3 days
- 🏆 **IPL Hub** — Standings, upcoming IPL matches, live scores, and results
- 🔍 **Match Search** — Find any match by team name (supports aliases like "MI", "CSK", "AUS")
- 🔔 **Alerts** — Cron-ready script for wicket, century, and result notifications
- 💾 **Smart Caching** — Respects API quota with configurable TTL per endpoint
- 🇮🇳 **IST by Default** — All times displayed in Indian Standard Time

---

## 🚀 Quick Start

### 1. Get a Free API Key
Sign up at [cricketdata.org](https://cricketdata.org) — the free tier gives you **100 API calls/day**. (CricketData.org's API is served at `api.cricapi.com` — they are the same service.)

### 2. Set the Environment Variable
```bash
export CRICKET_API_KEY="your-api-key-here"
# Add to your shell profile or ~/.openclaw/.env for persistence
```

### 3. Run Any Script
```bash
bash scripts/live-scores.sh              # What's happening right now?
bash scripts/upcoming-matches.sh         # What's coming up?
bash scripts/ipl.sh standings            # IPL points table
```

---

## 📖 Usage

### Live Scores
```bash
bash scripts/live-scores.sh
```
Shows all currently live matches with scores, overs, and match status.

**Example output:**
```
🏏 LIVE CRICKET SCORES
━━━━━━━━━━━━━━━━━━━━━

🔴 India vs England — 3rd Test, Day 2
🇮🇳 India: 285/6 (78.2 ov)
🏴 England: 312 (98.4 ov)
📊 India trail by 27 runs

🔴 Australia vs South Africa — 1st ODI
🇦🇺 Australia: 156/3 (28.1 ov)
📊 In Progress
```

### Upcoming Matches
```bash
bash scripts/upcoming-matches.sh              # All upcoming
bash scripts/upcoming-matches.sh --team India  # Filter by team
bash scripts/upcoming-matches.sh MI            # Works with aliases
```

**Example output:**
```
📅 UPCOMING MATCHES (Next 7 Days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇮🇳 India vs England — 4th Test
📍 Ranchi
🕐 16 Feb 2026, 09:30 AM IST

🏏 Mumbai Indians vs Chennai Super Kings — IPL 2026
📍 Wankhede Stadium, Mumbai
🕐 18 Feb 2026, 07:30 PM IST
```

### Recent Results
```bash
bash scripts/recent-results.sh
```

**Example output:**
```
✅ RECENT RESULTS
━━━━━━━━━━━━━━━━━

🏆 India won by 5 wickets
India vs England — 2nd Test
📍 Visakhapatnam

🏆 Australia won by 73 runs
Australia vs Sri Lanka — 3rd ODI
📍 Melbourne
```

### IPL Hub
```bash
bash scripts/ipl.sh standings   # Points table
bash scripts/ipl.sh upcoming    # Upcoming IPL matches
bash scripts/ipl.sh live        # Live IPL scores
bash scripts/ipl.sh results     # Recent IPL results
```

### Match Details (Scorecard)
```bash
bash scripts/match-details.sh <match-id>
```
Get match IDs from live-scores or search results.

### Search Matches
```bash
bash scripts/search-match.sh "India vs Australia"
bash scripts/search-match.sh "MI vs CSK"
```

### Cricket Alerts (Cron)
```bash
bash scripts/cricket-alert.sh
```
Detects wickets, centuries, and match completions since last check. Outputs only when something notable happens — perfect for cron.

---

## 🗣️ Natural Language Mapping

| User says | Script |
|-----------|--------|
| "What's the score?" / "Live scores" | `live-scores.sh` |
| "Show me the scorecard for match X" | `match-details.sh <id>` |
| "Upcoming matches" / "What's coming up?" | `upcoming-matches.sh` |
| "Recent results" / "Who won?" | `recent-results.sh` |
| "IPL table" / "IPL standings" | `ipl.sh standings` |
| "IPL matches today" | `ipl.sh live` |
| "India vs Australia" | `search-match.sh "India vs Australia"` |

---

## ⚙️ Configuration

### `config/cricket.yaml`
Main configuration file. API key can be set here or via `CRICKET_API_KEY` env var (env var takes priority).

```yaml
api_key: ""                    # Set via env var recommended
favorite_teams:                # Teams for alert filtering
  - India
  - Mumbai Indians
alert_events:                  # Events that trigger alerts
  - wicket
  - century
  - match_end
cache_dir: /tmp/cricket-cache  # Cache directory
cache_ttl:                     # Cache TTL in seconds per endpoint
  live: 120
  upcoming: 1800
  results: 1800
  series: 86400
  scorecard: 300
```

### `config/teams.yaml`
Team name aliases for fuzzy matching. Maps shorthand names (MI, CSK, IND, AUS) to canonical API names. See `config/README.md` for details.

---

## ⏰ Cron Integration

Set up periodic match alerts:

```bash
# Check for notable events every 5 minutes during match hours
*/5 9-23 * * * CRICKET_API_KEY="your-key" bash /path/to/skills/cricket-scores/scripts/cricket-alert.sh

# Or use OpenClaw cron:
# Schedule cricket-alert.sh to run during IPL match times (7-11 PM IST)
```

The alert script tracks state in `/tmp/cricket-alert-state.json` and only outputs when something new happens (wicket, century, match result).

---

## 📊 API Quota Management

| Tier | Calls/Day | Cost |
|------|-----------|------|
| Free | 100 | $0 |
| Pro | 2,000 | $5.99/mo |

### How Caching Helps
All scripts cache API responses locally in `/tmp/cricket-cache/`:
- **Live scores:** 2 min TTL (fresh during matches)
- **Upcoming/Results:** 30 min TTL
- **Series info:** 24 hour TTL
- **Scorecards:** 5 min TTL

### Budget During a Match Day
~10 list calls + ~50 score checks + 40 ad-hoc = **100 calls** (fits free tier)

### When Quota is Exhausted
Scripts show a clear message: *"API quota exhausted (100 calls/day limit reached). Try again tomorrow or upgrade."*

---

## 📂 Output Format

All output is messaging-friendly:
- No markdown tables (works on WhatsApp, Discord, Telegram)
- Bullet point lists with emoji
- Times converted to IST
- Match IDs included for drill-down

---

## 📋 Requirements

- **bash** 4.0+
- **curl** (usually pre-installed)
- **jq** — `apt install jq` or `brew install jq`
- **CricketData.org API key** (free) — sign up at [cricketdata.org](https://cricketdata.org)

---

## 🔒 Security Notes

- **API key in URL query parameter:** The CricketData.org API (`api.cricapi.com`) requires the API key to be passed as a URL query parameter (`?apikey=...`). This means the key may appear in shell history, process listings, server access logs, and any HTTP proxy/inspection logs. Mitigations:
  - Set the key via the `CRICKET_API_KEY` environment variable (not hardcoded in config files).
  - Use the **free tier key** for this skill — it has limited scope and can be rotated easily.
  - Avoid running scripts in shared/multi-tenant environments where process arguments are visible to other users.
  - The CricketData.org API does **not** support header-based authentication, so query-param passing is unavoidable.

---

## 📄 License

MIT — see [LICENSE](LICENSE)
