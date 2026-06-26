---
name: f1-cli
license: MIT
description: Query Formula 1 data using the f1-cli command-line tool (wraps OpenF1 API). Use when the user asks about F1 race results, lap times, driver standings, pit stops, telemetry, weather, team radio, overtakes, tire strategy, or any Formula 1 statistics. Also use when asked to compare drivers, analyze race performance, look up session data, or retrieve real-time F1 information. Triggers on mentions of F1, Formula 1, Grand Prix, specific driver names (Verstappen, Hamilton, Norris), or racing data queries. Even casual questions like "who won the last race" or "how fast was Max's fastest lap" should use this skill.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏎️",
        "requires": { "bins": ["f1"] },
      },
  }
---

# f1-cli — Formula 1 Data CLI

A Go CLI wrapping the [OpenF1 API](https://openf1.org) for querying F1 telemetry, timing, and session data.

## Installation

```bash
brew tap barronlroth/tap
brew install f1-cli
```

Or from source:
```bash
go install github.com/barronlroth/f1-cli/cmd/f1@latest
```

The binary name is `f1`.

## Quick Reference

### Global Flags (apply to all commands)

| Flag | Description |
|---|---|
| `--json` | Output as JSON (default: table) |
| `--csv` | Output as CSV |
| `--session KEY` | Session key — number or `latest` |
| `--meeting KEY` | Meeting key — number or `latest` |
| `--driver DRIVER` | Driver number (44) or 3-letter acronym (HAM) |
| `--limit N` | Limit results returned |
| `--filter EXPR` | Raw API filter, repeatable (e.g. `speed>=300`) |

### Commands → API Endpoints

| Command | Endpoint | What it returns |
|---|---|---|
| `f1 drivers` | `/drivers` | Driver info: name, team, number, acronym |
| `f1 sessions` | `/sessions` | Session list (FP1-3, Quali, Sprint, Race) |
| `f1 meetings` | `/meetings` | Grand Prix weekends (extra: `--year`, `--country`) |
| `f1 laps` | `/laps` | Lap times, sector times, speed traps |
| `f1 telemetry` | `/car_data` | Speed, RPM, gear, throttle, brake, DRS at ~3.7 Hz |
| `f1 pit` | `/pit` | Pit stop timing and duration |
| `f1 positions` | `/position` | Position changes throughout session |
| `f1 intervals` | `/intervals` | Gap to leader and car ahead (race only) |
| `f1 standings drivers` | `/championship_drivers` | Driver championship points (race sessions) |
| `f1 standings teams` | `/championship_teams` | Constructor standings (race sessions) |
| `f1 weather` | `/weather` | Track temp, air temp, humidity, wind, rain |
| `f1 race-control` | `/race_control` | Flags, safety car, incidents |
| `f1 radio` | `/team_radio` | Team radio recording URLs |
| `f1 stints` | `/stints` | Tire compound and stint laps |
| `f1 overtakes` | `/overtakes` | Position exchanges between drivers |
| `f1 location` | `/location` | Car XYZ position on track (~3.7 Hz) |
| `f1 doctor` | — | API connectivity check |

## Usage Patterns

### Finding the right session

Most commands need `--session`. Start with `latest` for the most recent session, or find a specific one:

```bash
# List sessions for the latest meeting
f1 sessions --meeting latest

# Find a specific Grand Prix
f1 meetings --year 2025 --country Singapore

# Then use the session_key from the output
f1 laps --session 9161 --driver VER
```

### Driver identification

The `--driver` flag accepts either a number or a 3-letter acronym. The CLI resolves acronyms automatically via the API.

```bash
# These are equivalent
f1 laps --session latest --driver 1
f1 laps --session latest --driver VER
```

Common driver acronyms: VER (Verstappen), NOR (Norris), HAM (Hamilton), LEC (Leclerc), PIA (Piastri), SAI (Sainz), RUS (Russell), ALO (Alonso).

### Filtering with comparison operators

The `--filter` flag passes raw query params to the API. Supports `>=`, `<=`, `>`, `<` operators. Can be repeated.

```bash
# Cars going over 315 km/h
f1 telemetry --session 9159 --driver 55 --filter "speed>=315"

# Pit stops under 2.5 seconds
f1 pit --session latest --filter "stop_duration<2.5"

# Combine multiple filters
f1 telemetry --session latest --driver VER --filter "speed>=300" --filter "throttle>=95"

# Laps under 90 seconds
f1 laps --session latest --filter "lap_duration<90"
```

### Output formats

```bash
# Default: aligned table
f1 drivers --session latest

# JSON for piping to jq or other tools
f1 telemetry --session latest --driver VER --json | jq '.[0].speed'

# CSV for spreadsheets
f1 laps --session latest --driver HAM --csv > hamilton_laps.csv
```

## Common Workflows

### "Who won the last race?"
```bash
# Always use standings for final race results
f1 standings drivers --session latest
```
**Do NOT use `f1 positions` for race results.** Positions is a time series — it records every position change throughout the session. Using `--limit` on positions gives you the *start* of the race, not the finish. Use `f1 standings drivers` for the final classification.

### "Compare two drivers' lap times"
```bash
f1 laps --session latest --driver VER --json > /tmp/ver.json
f1 laps --session latest --driver NOR --json > /tmp/nor.json
# Then compare the JSON files
```

### "What happened during the race?" (incidents, flags)
```bash
f1 race-control --session latest
```

### "Tire strategy breakdown"
```bash
f1 stints --session latest --driver VER
```

### "Weather conditions during the session"
```bash
f1 weather --session latest --limit 10
```

### "Fastest pit stops"
```bash
f1 pit --session latest --filter "stop_duration<3" --json | jq 'sort_by(.stop_duration)'
```

## Important Gotchas

- **`--limit` is client-side only.** The OpenF1 API does not support a `limit` query parameter. The CLI fetches all results then truncates locally. This means large telemetry/location queries still hit the API fully — use `--filter` to narrow server-side when possible.
- **`--filter` is server-side.** Filters like `speed>=300` are sent to the API and reduce the response. Always prefer `--filter` over `--limit` for performance.
- **`positions` is a time series, not a result.** It records every position change during a session. To get final race results, use `f1 standings drivers --session <key>`, not `f1 positions`. Using `positions --limit N` gives you lap 1 grid order, not the finish.
- **Driver numbers change between seasons.** Don't hardcode driver numbers — use acronyms (VER, HAM, NOR) which the CLI resolves automatically per session.
- **Norris is now #1.** For the 2026 season, Lando Norris drives car #1 (as reigning champion). Verstappen is #3.

## API Notes

- **Data availability:** Historical data from 2023 season onwards. No auth needed.
- **Rate limits:** 3 requests/second, 30 requests/minute (free tier). The CLI handles rate limiting internally with retry on 429.
- **`latest` keyword:** Works for both `--session` and `--meeting` to get the most recent.
- **Intervals and overtakes:** Only available during race sessions, not practice or qualifying.
- **Championship standings:** Only available for race sessions.
- **Telemetry and location:** High-frequency data (~3.7 Hz) — use `--filter` to narrow results server-side, then `--limit` to cap output.
- **Off-season:** `--session latest` returns 404 when no sessions exist. Use a known session_key from a past season instead.
