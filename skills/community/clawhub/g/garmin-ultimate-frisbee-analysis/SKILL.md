---
name: garmin-frisbee-analysis
description: Ultimate Frisbee performance analytics powered by Garmin data. Analyzes and monitors game and training data . Generates interactive HTML dashboards for post-game review, tournament fatigue tracking, and season-long trend analysis. Supports four comparison modes: training vs training, tournament vs tournament, training vs game intensity, and early vs late season. Built for competitive Ultimate Frisbee players who want data-driven insight into performance, recovery, and fitness progression.
version: 1.1.3
author: Evelyn & Claude
homepage: https://github.com/EvelynDevelops/garmin-frisbee-analysis
env:
  - GARMIN_EMAIL
  - GARMIN_PASSWORD
install: pip install -r requirements.txt && python3 scripts/garmin_auth.py login
metadata: {"requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"pip-deps","kind":"shell","command":"pip3 install -r requirements.txt","label":"Install Python dependencies"},{"id":"garmin-auth","kind":"shell","command":"python3 scripts/garmin_auth.py login","label":"Authenticate with Garmin Connect"}],"tokenStorage":"~/.clawdbot/garmin/ (permissions 700, session tokens only, no plaintext credentials)","clawdbot":{"emoji":"🥏"}}
---

# Garmin Frisbee Analysis

Analyze Garmin health and performance data specifically for Ultimate Frisbee players. Generate interactive HTML dashboards for post-game review, tournament fatigue tracking, training load optimization, and season-long trend comparison.

## Two Installation Paths

1. **Clawdbot Skill** (this guide) — Use with Clawdbot for natural language queries and proactive monitoring
2. **MCP Server** ([see MCP setup guide](references/mcp_setup.md)) — Use with Claude Desktop as an MCP server

---

## Setup (first time only)

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

Pinned versions are in [requirements.txt](requirements.txt):
- `garminconnect>=0.2.19` — Garmin Connect API client
- `fitparse>=3.2.0` — FIT file parsing for activity data
- `gpxpy>=1.3.5` — GPX file parsing

### 2. Configure Credentials

> **Why email + password?** Garmin does not expose a public OAuth API. The `garminconnect` library authenticates via Garmin's SSO, the same flow as the Garmin Connect mobile app. The password is used **once** during login and is **never written to disk or logged**. The resulting session token is then stored locally at `~/.clawdbot/garmin/` (permissions 700); all subsequent API requests use that token, not the password.

Set `GARMIN_EMAIL` and `GARMIN_PASSWORD` in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"
```

### 3. Authenticate

```bash
python3 scripts/garmin_auth.py login
python3 scripts/garmin_auth.py status   # verify
```

---

## Frisbee Scripts

### Post-Game / Post-Training Analysis

Analyze a single activity in depth: sprints, speed, heart rate zones.

```bash
# Most recent activity
python3 scripts/frisbee_activity.py --latest

# Specific date
python3 scripts/frisbee_activity.py --date 2026-03-08

# Specific activity ID
python3 scripts/frisbee_activity.py --activity-id 12345678

# Save to file
python3 scripts/frisbee_activity.py --latest --output ~/Desktop/game.html
```

**Dashboard includes:**
- Summary cards: duration, distance, sprint count, top speed, sprint fatigue index, high-intensity distance
- Speed timeline with sprint highlight bands
- Sprint peak speed trend (detects fatigue: are later sprints slower?)
- Heart rate zone distribution (Zone 1–6)

**Sprint detection:** speed > 14.4 km/h sustained ≥ 2 seconds.
**Sprint Fatigue Index:** last 3 sprint peaks ÷ first 3 sprint peaks. < 0.85 = significant fatigue.

---

### Tournament Review Dashboard

Full overview of a multi-day tournament: fatigue curve, game intensity, heart rate recovery, overnight sleep/HRV.

```bash
python3 scripts/frisbee_tournament.py \
  --start 2026-03-08 \
  --end 2026-03-10 \
  --name "Spring Tournament 2026" \
  --output ~/Desktop/tournament.html
```

**Dashboard includes:**
- Body Battery fatigue curve across tournament days (includes day-before baseline)
- Per-game avg/max heart rate comparison
- Heart Rate Recovery curves post-game (30 min window, all games overlaid)
- Overnight sleep hours + HRV per tournament night
- Activity table with all detected games

---

### Comparison Analysis

Compare training sessions, games, or the full season.

```bash
# Training vs training (last 90 days)
python3 scripts/frisbee_compare.py --mode training --days 90

# Game vs game
python3 scripts/frisbee_compare.py --mode tournament --days 180

# Training intensity vs game intensity
python3 scripts/frisbee_compare.py --mode cross --days 60

# Full season overview
python3 scripts/frisbee_compare.py --mode season --days 180

# Save output
python3 scripts/frisbee_compare.py --mode season --days 180 --output ~/Desktop/season.html
```

**Activity classification** uses name keywords:
- Game: `game`, `match`, `tournament`, `vs`, `finals`
- Training: `practice`, `training`, `train`, `drill`, `scrimmage`

**Dashboard includes:**
- Top speed trend over time (training vs game color-coded in cross mode)
- Avg heart rate per activity (color by intensity)
- Morning HRV on day of each activity
- Volume trend: duration + distance over time
- Full activity table

---

## General Garmin Data

```bash
# Sleep
python3 scripts/garmin_data.py sleep --days 14

# Body Battery
python3 scripts/garmin_data.py body_battery --days 30

# HRV
python3 scripts/garmin_data.py hrv --days 30

# Heart rate
python3 scripts/garmin_data.py heart_rate --days 7

# Activities
python3 scripts/garmin_data.py activities --days 30

# Stress
python3 scripts/garmin_data.py stress --days 7

# Combined summary
python3 scripts/garmin_data.py summary --days 7

# Custom date range
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15
```

## General Health Charts

```bash
python3 scripts/garmin_chart.py sleep --days 30
python3 scripts/garmin_chart.py body_battery --days 30
python3 scripts/garmin_chart.py hrv --days 90
python3 scripts/garmin_chart.py activities --days 30
python3 scripts/garmin_chart.py dashboard --days 30
```

---

## Answering Frisbee Questions

| Player asks | Script | What to report |
|-------------|--------|----------------|
| "How many sprints did I hit?" | `frisbee_activity.py --latest` | sprint_count, sprint fatigue index |
| "What was my top speed?" | `frisbee_activity.py --latest` | top_speed_kmh from summary |
| "Was I fatigued at the end?" | `frisbee_activity.py --latest` | sprint_fatigue_index < 0.85 = yes |
| "How long was my heart rate elevated?" | `frisbee_activity.py --latest` | Zone 4-6 time percentage |
| "Did I recover fast enough between points?" | `frisbee_tournament.py` | HRR curves, slope comparison |
| "Was I ready for the tournament?" | `frisbee_tournament.py` | Pre-game Body Battery values |
| "Is my training intense enough?" | `frisbee_compare.py --mode cross` | Avg HR: training vs game |
| "Am I improving this season?" | `frisbee_compare.py --mode season` | Top speed + HRV trends |
| "How did I sleep during the tournament?" | `frisbee_tournament.py` | Recovery nights chart |

---

## Data Availability (Garmin 265S)

| Metric | Available |
|--------|-----------|
| Sprint count & speed | ✅ FIT file analysis |
| Top speed | ✅ FIT file `speed` field |
| Sprint fatigue index | ✅ Computed from speed time-series |
| Heart rate zones | ✅ FIT file HR + max HR |
| Heart Rate Recovery (HRR) | ✅ Intraday HR time-series |
| Body Battery | ✅ Garmin API |
| HRV (overnight) | ✅ Garmin API |
| Sleep stages & score | ✅ Garmin API |
| Total distance | ✅ FIT file + Garmin API |
| High-intensity distance | ✅ Computed from speed threshold |
| Ground Contact Time | ❌ Requires HRM-Run Pod (not wrist) |

---

## Key Frisbee Metrics Explained

### Sprint Fatigue Index
Ratio of last 3 sprint peak speeds to first 3: `≥ 0.95` stable, `0.85–0.95` mild decline, `< 0.85` significant fatigue. Use this to judge if you're losing speed output as the game progresses.

### Heart Rate Recovery (HRR)
How fast your HR drops after game ends. Steeper curve = better cardiovascular fitness and recovery. Flatter curves in later games of a tournament = cumulative fatigue.

### Body Battery (0–100)
Pre-game value is the key readiness indicator. `≥ 70` = ready to go, `50–69` = manageable, `< 50` = compromised performance likely.

### Heart Rate Zones
- **Zone 4 (70–80% max)**: Sustained hard effort — hallmark of well-executed frisbee
- **Zone 5–6 (80–100% max)**: Explosive sprints and close contests
- High Zone 4–6 in training = adequate game-prep intensity

---

## Troubleshooting

- **"FIT file download failed"**: Check activity ID; some activity types may not export FIT
- **No sprints detected**: Activity may not include speed data, or you used a non-GPS mode
- **HRR chart empty**: Intraday HR not available for that date; ensure "All-day HR monitoring" is on in Garmin settings
- **Activities not classified**: Name your activities with keywords like "game vs X" or "practice" — see classification keywords above
- **Tokens expired**: Re-run `python3 scripts/garmin_auth.py login`

---

## Privacy & Security

**Credentials**
- `GARMIN_EMAIL` and `GARMIN_PASSWORD` are read from environment variables at runtime only
- The Garmin password is **never written to disk or logged** — used only during the authentication step, then discarded
- No config file stores credentials

**Session tokens**
- Stored in `~/.clawdbot/garmin/` with directory permissions `700` (owner read/write/execute only)
- Managed by the `garth` library (part of `garminconnect`); format is an opaque token bundle, not plaintext password
- To revoke: `rm -rf ~/.clawdbot/garmin/` — next login will re-authenticate

**Network**
- Credentials are used only to authenticate with Garmin Connect and are not transmitted to any third-party service
- All API calls go to `connect.garmin.com` only
- Generated HTML dashboards load Chart.js from `cdn.jsdelivr.net` (versions pinned: `chart.js@4.4.0`, `chartjs-plugin-annotation@3.0.1`) — requires internet access when viewing dashboards

---

## References

- `references/api.md` — Garmin Connect API details
- `references/health_analysis.md` — Science-backed metric interpretation
- `references/mcp_setup.md` — Claude Desktop MCP setup

---

## Version Info

- **Version**: 1.1.3
- **Created**: 2026-03-11
- **Updated**: 2026-03-16
- **Author**: Evelyn & Claude
- **License**: MIT
- **Dependencies**: garminconnect, fitparse, gpxpy
